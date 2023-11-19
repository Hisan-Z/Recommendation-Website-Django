#!/usr/bin/env bash
# exit on error
set -o errexit
echo "BUILD START"
pip install -r requirements.txt

# python manage.py collectstatic --no-input
python manage.py migrate
python manage.py load_products --path merge_product4.csv

echo "BUILD END"