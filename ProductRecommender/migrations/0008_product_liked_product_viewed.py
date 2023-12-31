# Generated by Django 4.2.4 on 2023-10-03 13:27

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("ProductRecommender", "0007_remove_product_brought_product_brought"),
    ]

    operations = [
        migrations.AddField(
            model_name="product",
            name="liked",
            field=models.ManyToManyField(
                related_name="liked", to=settings.AUTH_USER_MODEL
            ),
        ),
        migrations.AddField(
            model_name="product",
            name="viewed",
            field=models.ManyToManyField(
                related_name="viewed", to=settings.AUTH_USER_MODEL
            ),
        ),
    ]
