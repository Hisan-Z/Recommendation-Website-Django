# context_processors.py

from .models import Product


def liked_products(request):
    liked_products = []
    if request.user.is_authenticated:
        liked_products = Product.objects.filter(liked=request.user)
    return {'liked_products': liked_products}
def brought_products(request):
    brought_products = []
    if request.user.is_authenticated:
        brought_products = Product.objects.filter(brought=request.user)
    return {'brought_products': brought_products}
