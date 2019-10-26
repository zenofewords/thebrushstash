#!/bin/bash
cd /home/anarniel/thebrushstash
source ../.virtualenvs/thebrushstash/bin/activate
python manage.py update_product_prices
