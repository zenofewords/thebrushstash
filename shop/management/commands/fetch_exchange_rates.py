import json
from decimal import Decimal
from urllib3 import poolmanager

from django.core.management.base import BaseCommand

from shop.constants import exchange_rate_url
from shop.models import ExchangeRate


class Command(BaseCommand):
    help = 'Fetch and save exchange rates from HNB API.'

    def _update_exchange_rates(self, exchange_rates):
        def to_decimal(key):
            return Decimal(self.exchange_rate[key].replace(',', '.'))

        for self.exchange_rate in exchange_rates:
            er = ExchangeRate.objects.get(currency_code=self.exchange_rate['sifra_valute'])
            er.buying_rate = to_decimal('kupovni_tecaj')
            er.middle_rate = to_decimal('srednji_tecaj')
            er.selling_rate = to_decimal('prodajni_tecaj')
            er.save()

    def _fetch(self):
        pm = poolmanager.PoolManager()
        payload = pm.request('get', exchange_rate_url)

        if payload.status == 200:
            self._update_exchange_rates(json.loads(payload.data.decode('utf-8')))

    def handle(self, *args, **options):
        self._fetch()
