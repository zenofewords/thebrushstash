from django.conf import settings
from django.core.management.base import BaseCommand
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
        if newsletter.recipient_list:
            for newsletter_recipient in newsletter.recipient_list.all():
                send_newsletter(newsletter_recipient, newsletter)
        elif not settings.DEBUG:
            recipients = NewsletterRecipient.objects.filter(subscribed=True)
            for newsletter_recipiet in recipients:
                send_newsletter(newsletter_recipiet, newsletter)

    def handle(self, *args, **options):
        newsletter = Newsletter.objects.filter(
            status=NewsletterStatus.READY,
            schedule_at__lte=timezone.now()
        ).first()

        if newsletter:
            try:
                newsletter.status = NewsletterStatus.IN_PROGRESS
                newsletter.save()
                self.process_newsletter(newsletter)

                newsletter.status = NewsletterStatus.FINISHED

                if newsletter.recipient_list:
                    newsletter.status_message = 'Success, sent to selected recipients.'
                else:
                    newsletter.status_message = 'Success, sent to all recipients.'
                newsletter.save()
            except Exception as error:
                newsletter.status = NewsletterStatus.FAILED
                newsletter.status_message = error
                newsletter.save()
