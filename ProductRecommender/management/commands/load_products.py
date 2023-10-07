import csv

import pandas as pd
from django.core.management import BaseCommand

from ...models import Product


class Command(BaseCommand):
    help = "Load a products csv file into the database"

    def add_arguments(self, parser):
        parser.add_argument("--path", type=str)

    def handle(self, *args, **kwargs):
        # Remove any existing data
        print("Clean old product data")
        Product.objects.all().delete()
        path = kwargs["path"]
        # Read the product csv file as a dataframe
        product_df = pd.read_csv(path)
        # Iterate each row in the dataframe
        for index, row in product_df.iterrows():
            product_id = row["product_id"]
            brand = row["brand"]
            title = row["product_title"]
            actual_price = row["actual_price"]
            selling_price = row["special_price"]
            average_rating = row["average_rating"]
            total_ratings=row['total_ratings']
            category = row["category"]
            subcategory = row["sub_category"]
            img_path = row["extra_image"]
            poster=row['product_image']
            discount=row['discount']
            description = row["description"]
            details = row["details"]
            url = row["url"]
            # Populate Product object for each row
            product = Product(
                product_id=product_id,
                brand=brand,
                title=title,
                actual_price=actual_price,
                selling_price=selling_price,
                average_rating=average_rating,
                total_ratings=total_ratings,
                category=category,
                subcategory=subcategory,
                poster=poster,
                img_path=img_path,
                description=description,
                details=details,
                discount=discount,
                url=url,
            )
            # Save product object
            product.save()
            print(f"Product: {product_id}, {title} saved...")


# python manage.py load_products --path csv file name
