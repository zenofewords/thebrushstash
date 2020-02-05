#!/bin/bash
cd /home/anarniel/thebrushstash
source ../.virtualenvs/thebrushstash/bin/activate
python manage.py set_pending_invoice_to_cancelled
