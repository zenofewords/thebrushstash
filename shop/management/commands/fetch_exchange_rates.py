import json
from decimal import Decimal
from urllib3 import poolmanager

from django.core.management.base import BaseCommand

from thebrushstash.constants import exchange_rate_url
from thebrushstash.models import ExchangeRate


class Command(BaseCommand):
    help = 'Fetch and save exchange rates from HNB API.'

    def _update_exchange_rates(self, exchange_rates):
        def to_decimal(exchange_rate, key):
            return Decimal(exchange_rate[key].replace(',', '.'))

        for exchange_rate in exchange_rates:
            currency = exchange_rate.get('valuta')
            currency_code = exchange_rate.get('sifra_valute')
            buying_rate = to_decimal(exchange_rate, 'kupovni_tecaj')
            middle_rate = to_decimal(exchange_rate, 'srednji_tecaj')
            selling_rate = to_decimal(exchange_rate, 'prodajni_tecaj')
            state_iso = exchange_rate.get('drzava_iso')

            er, created = ExchangeRate.objects.get_or_create(
                currency_code=exchange_rate['sifra_valute'],
                defaults={
                    'currency': currency,
                    'currency_code': currency_code,
                    'buying_rate': buying_rate,
                    'middle_rate': middle_rate,
                    'selling_rate': selling_rate,
                    'state_iso': state_iso,
                }
            )

            if not created:
                er.buying_rate = buying_rate
                er.middle_rate = middle_rate
                er.selling_rate = selling_rate
                er.save()

    def _fetch(self):
        pm = poolmanager.PoolManager()
        payload = pm.request('get', exchange_rate_url)

        if payload.status == 200:
            self._update_exchange_rates(json.loads(payload.data.decode('utf-8')))

    def handle(self, *args, **options):
        self._fetch()
