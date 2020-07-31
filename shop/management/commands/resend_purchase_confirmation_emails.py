from datetime import timedelta

from django.core.management.base import BaseCommand
from django.utils import timezone, translation

from shop.models import (
    Invoice,
    InvoiceStatus,
)
from thebrushstash.utils import (
    send_purchase_email,
    update_inventory,
)


class Site:
    domain = 'shop.thebrushstash.com'
    name = 'shop.thebrushstash.com'


class Command(BaseCommand):
    help = 'Resends purchase confirmation emails for flagged invoices.'

    def handle(self, *args, **options):
        flagged_invoices = Invoice.objects.filter(
            resend_purchase_confirmation_email=True
        ).exclude(
            status=InvoiceStatus.COMPLETED
        )

        for flagged_invoice in flagged_invoices:
            update_inventory(flagged_invoice)

            with translation.override(flagged_invoice.region.language):
                send_purchase_email(Site, flagged_invoice)
            flagged_invoice.resend_purchase_confirmation_email = False
            flagged_invoice.status = InvoiceStatus.COMPLETED
            flagged_invoice.save()
