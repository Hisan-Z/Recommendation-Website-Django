from django.contrib import admin

from .models import Product


class ProductAdmin(admin.ModelAdmin):
    fields = ['product_id', 'title','selling_price','average_rating','brought','viewed','liked','recommended']
    list_display = ('product_id', 'title','selling_price','average_rating')
    search_fields = ['title', 'selling_price']
# Register your models here.
admin.site.register(Product,ProductAdmin)
