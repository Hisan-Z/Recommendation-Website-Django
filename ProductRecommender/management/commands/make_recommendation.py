import numpy as np
import pandas as pd
from django.core.management import BaseCommand
from sklearn.decomposition import TruncatedSVD
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel

from ...models import Product


class Command(BaseCommand):
    help = 'Recommend movies'

    def add_arguments(self, parser):
        pass

    def handle(self, *args, **kwargs):
        recommendation()

def recommendation():
    
    # Query all items from the Django model
    items = Product.objects.all()

    
    # Create a TF-IDF vectorizer
    tfidf_vectorizer = TfidfVectorizer()

    # Fit and transform item descriptions into TF-IDF vectors
    item_details = [item.details for item in items]
    tfidf_matrix = tfidf_vectorizer.fit_transform(item_details)

    # Compute the cosine similarity matrix
    cosine_sim = linear_kernel(tfidf_matrix, tfidf_matrix)

    # List of target item IDs
    target_item_ids = Product.objects.filter(brought=True).values_list('product_id',flat=True)  # Replace with your list of item IDs
    if target_item_ids:
        for target_item_id in target_item_ids:
            # Find the index of the target item in the items list
            target_item_index = next((index for index, item in enumerate(items) if item.product_id == target_item_id), None)

            if target_item_index is None:
                print(f"Item {target_item_id} not found.")
                continue

            # Get similar items based on cosine similarity
            similar_items = list(enumerate(cosine_sim[target_item_index]))

            # Sort similar items by score and recommend top N items
            N = 7  # Number of recommendations
            top_similar_items = sorted(similar_items, key=lambda x: x[1], reverse=True)[1:N+1]
            recommended_item_indices = [i for i, _ in top_similar_items]
            recommended_items = [items[i].title for i in recommended_item_indices]
            for i in recommended_item_indices:
                items[i].recommended = True
                items[i].save()
            print(f"Recommended items for item {target_item_id}:")
            for item in recommended_items:
                print("-", item)
            print()

