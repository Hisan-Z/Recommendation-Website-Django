#!/usr/bin/env bash
# exit on error
set -o errexit
echo "BUILD START"
pip install -r requirements.txt
echo "req done"

python3.9 manage.py collectstatic --no-input
python3.9 manage.py migrate
echo "moigrated"
python3.9 manage.py load_products --path merge_product4.csv

echo "BUILD END"