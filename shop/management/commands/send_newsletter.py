from django.conf import settings
from django.core.management.base import BaseCommand
from django.db.models import Q
from django.utils import timezone

from account.models import NewsletterRecipient
from shop.models import (
    Newsletter,
    NewsletterStatus,
)
from thebrushstash.utils import send_newsletter


class Command(BaseCommand):
    help = 'Check for pending newsletter, send to recipients.'

    def process_newsletter(self, newsletter):
        if newsletter.recipient_list.count() > 0:
            for newsletter_recipient in newsletter.recipient_list.all():
                send_newsletter(newsletter_recipient, newsletter)
        elif not settings.DEBUG:
            recipients = NewsletterRecipient.objects.filter(subscribed=True)
            for newsletter_recipiet in recipients:
                send_newsletter(newsletter_recipiet, newsletter)

    def handle(self, *args, **options):
        newsletter = Newsletter.objects.filter(
            send=True
        ).filter(
            Q(schedule_at__isnull=True) | Q(schedule_at__lte=timezone.now())
        ).first()

        if newsletter:
            newsletter.send = False
            newsletter.status = NewsletterStatus.IN_PROGRESS
            newsletter.save()

            try:
                self.process_newsletter(newsletter)

                if newsletter.recipient_list:
                    newsletter.status_message = 'Success, sent to selected recipients.'
                else:
                    newsletter.status_message = 'Success, sent to all recipients.'

                newsletter.status = NewsletterStatus.FINISHED
            except Exception as error:
                newsletter.status = NewsletterStatus.FAILED
                newsletter.status_message = error

            newsletter.completed_at = timezone.now()
            newsletter.save()
