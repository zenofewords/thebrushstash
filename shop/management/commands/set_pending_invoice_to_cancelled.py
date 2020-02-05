from datetime import timedelta

from django.core.management.base import BaseCommand
from django.utils import timezone

from shop.models import (
    Invoice,
    InvoiceStatus,
)


class Command(BaseCommand):
    help = 'Update stale pending invoices to cancelled status.'

    def handle(self, *args, **options):
        stale_invoices = Invoice.objects.filter(
            status=InvoiceStatus.PENDING,
            modified_at__lte=timezone.now() - timedelta(days=3)
        )
        for stale_invoice in stale_invoices:
            stale_invoice.status = InvoiceStatus.CANCELLED
            stale_invoice.save()
