from django.contrib import admin
from django.urls import path

from . import views

urlpatterns=[
   path('',views.home,name='home'),
   path('explore/',views.explore, name='explore'),
   path('products/<int:product_id>/', views.product_detail, name='product_detail'),
   path('category/<str:product_category>/', views.product_category, name='category'),
   path('buy/<int:product_id>/',views.buy_product,name="buy"),
   path('like/<int:product_id>/',views.like_product,name="like"),
   path('purchaseHistory/',views.show_brought,name="showbrought"),
   path('removebrought/<int:product_id>/',views.remove_brought,name="remove-brought"),
   path('removeliked/<int:product_id>/',views.remove_liked,name="remove-like"),
   
]   