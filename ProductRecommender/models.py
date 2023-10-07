from django.contrib.auth.models import User
from django.db import models
from django_postgres_extensions.models.fields import ArrayField

# Create your models here.

class Product(models.Model):
    
    # Product id
    product_id=models.CharField(max_length=50,null=False)
    # Brand
    brand= models.CharField(max_length=20)
    #Title
    title=models.CharField(max_length=100,null=False)
    # Actual Price
    actual_price= models.FloatField(max_length=10, null=False)
    # Selling Price
    selling_price= models.FloatField(max_length=10, null=True)
    # Average Rating
    average_rating= models.FloatField(max_length=5, null=False)
    # Total Rating
    total_ratings=models.IntegerField(default=0)
    # Category
    category=models.CharField(max_length=40,null=False)
    # Image Path
    img_path= models.CharField(max_length=64)
    # Subcategory
    subcategory= models.CharField(max_length=30,null=True)
    #Poster
    poster=models.CharField(max_length=160,null=False,default='https://www.flipkart.com')
    # discount
    discount= models.IntegerField(default=0)
    # Brought
    brought= models.ManyToManyField(User)

    #Description
    description=models.TextField(max_length=200)
    #Details
    details=models.CharField(max_length=150,null=True)
    #URL
    url=models.URLField(default='https://www.flipkart.com/')
    
    viewed=models.ManyToManyField(User,related_name="viewed")
    
    liked=models.ManyToManyField(User,related_name="liked")
    
    # If this product will be recommended
    recommended= models.ManyToManyField(User,related_name="recommended")

