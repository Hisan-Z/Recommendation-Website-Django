from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel

from .models import Product


def product_detail(request, product_id):
    if request.user.is_authenticated:
        product = get_object_or_404(Product, pk=product_id)

        product.viewed.add(request.user)
        product.save()

        similar_products_list = get_recommended_items(product.product_id, request.user)

        # similar=[]
        # for i in similar_products_list:
        #     similar.append(Product.objects.filter(product_id=i))
        similar = Product.objects.filter(product_id__in=similar_products_list)
        context = {"product": product, "similar_products": similar}

        return render(request, "product_page.html", {"context": context})
    else:
        return render(
            request, "product_page.html", {"error": "Please Login to view the product"}
        )


def get_recommended_items(target_item_id, user):
    # Query the target item from the Django model

    target_item = Product.objects.get(product_id=target_item_id)
    # print(target_item)
    # Query all items from the Django model except the target item
    # items = Product.objects.exclude(product_id=target_item_id)
    items = Product.objects.all()

    # Create a TF-IDF vectorizer
    tfidf_vectorizer = TfidfVectorizer()

    # Fit and transform item details into TF-IDF vectors
    item_details = [item.details for item in items]
    tfidf_matrix = tfidf_vectorizer.fit_transform(item_details)

    # Compute the cosine similarity matrix
    cosine_sim = linear_kernel(tfidf_matrix, tfidf_matrix)

    # Find the index of the target item in the items list
    target_item_index = None
    for index, item in enumerate(items):
        if item.product_id == target_item_id:
            target_item_index = index
            break

    # Ensure that the target item was found before proceeding
    if target_item_index is None:
        return []  # Return an empty list if target item not found

    # Get similar items based on cosine similarity
    similar_items = list(enumerate(cosine_sim[target_item_index]))
    N = 15  # Number of recommendations
    top_similar_items = sorted(similar_items, key=lambda x: x[1], reverse=True)[:N]
    recommended_item_indices = [i for i, _ in top_similar_items]
    recommended_items = [items[i] for i in recommended_item_indices]
    # print(recommended_items)

    for item in recommended_items:
        if item.product_id in [_.product_id for _ in recommended_items]:
            item.recommended.add(user)
            item.save()

    recommended_item_ids = [
        item.product_id for item in recommended_items if item.recommended
    ]

    return recommended_item_ids

    # return recommended_items


def product_category(request, product_category):
    # Get the brand filter from the request
    try:
        # Get the brand filter from the request
        min_price = request.GET.get("min_price")
        max_price = request.GET.get("max_price")
        brand_filter = request.GET.get("brand")
        selected_discounts = request.GET.getlist("discount")
        selected_ratings = request.GET.getlist("rating")

        print(brand_filter)
        # Get all products for the given category
        products = Product.objects.filter(category=product_category)
        
        if product_category == "all": 
            search_query = request.GET.get("search_keyword")
            products = Product.objects.filter( 
                Q(title__icontains=search_query)
                | Q(category__icontains=search_query)
            )
            print(len(products))
        print(len(products))
        # Apply brand filtering if a brand filter is provided
        get_brand = request.GET.getlist("selected_brands")
        print(get_brand)
        if get_brand:
            products = products.filter(brand__in=get_brand)
        print(products)
        print(len(products))
        # Apply price range filtering
        if min_price:
            products = products.filter(selling_price__gte=min_price)
        if max_price:
            products = products.filter(selling_price__lte=max_price)

        # Apply discount filtering
        if selected_discounts:
            discount_filters = [
                Q(discount__gte=discount) for discount in selected_discounts
            ]
            discount_filter = Q()
            for q in discount_filters:
                discount_filter |= q
            products = products.filter(discount_filter)

        # Apply rating filtering
        if selected_ratings:
            rating_filters = [
                Q(average_rating__gte=rating) for rating in selected_ratings
            ]
            rating_filter = Q()
            for q in rating_filters:
                rating_filter |= q
            products = products.filter(rating_filter)

        items_per_page = 15

        # Create a Paginator object for the filtered products
        paginator = Paginator(products, items_per_page)

        # Get the current page number from the request
        page_number = request.GET.get("page")

        # Get the Page object for the current page
        page = paginator.get_page(page_number)

        # Calculate the page_range centered around the current page
        visible_page_count = 7
        half_visible_page_count = visible_page_count // 2
        total_pages = paginator.num_pages
        current_page = page.number

        if total_pages <= visible_page_count:
            page_range = range(1, total_pages + 1)
        elif current_page <= half_visible_page_count:
            page_range = range(1, visible_page_count + 1)
        elif current_page >= total_pages - half_visible_page_count:
            page_range = range(total_pages - visible_page_count + 1, total_pages + 1)
        else:
            page_range = range(
                current_page - half_visible_page_count,
                current_page + half_visible_page_count + 1,
            )
        current_query_params = request.GET.copy()
        if 'page' in current_query_params:
            del current_query_params['page']
            
        print(current_query_params)
        # Pass the filtered products, brands, page, and page_range to the template
        context = {
            "page": page,
            "brands":Product.objects.filter(category=product_category, brand__icontains=brand_filter).values_list("brand", flat=True)
            .distinct()
            .order_by("brand") if brand_filter else Product.objects.filter(category=product_category).values_list("brand", flat=True)
            .distinct()
            .order_by("brand"),
            "page_range": page_range,
            "selected_brands": get_brand,
            "selected_discounts": selected_discounts,
            "selected_ratings": selected_ratings,
            "selected_min": min_price,
            "selected_max": max_price,
            "current_query_params": current_query_params.urlencode(),
            "category":product_category
        }

        return render(request, "product_list.html", context)
    except Exception as e:
        # Handle exceptions gracefully and return an error page or a redirect as needed
        return render(request, "product_list.html", {"error_message": str(e)})


def explore(request):
    categories = Product.objects.values_list("category", flat=True).distinct()
    # print(categories)
    return render(request, "explore.html", {"categories": categories})


def get_recommended_item_list(product_list, user):
    # Create a TF-IDF vectorizer
    tfidf_vectorizer = TfidfVectorizer()

    # Fit and transform item details into TF-IDF vectors
    item_details = [item.details for item in product_list]
    tfidf_matrix = tfidf_vectorizer.fit_transform(item_details)

    # Compute the cosine similarity matrix
    cosine_sim = linear_kernel(tfidf_matrix, tfidf_matrix)

    # Initialize a set to store recommended items
    recommended_items = set()

    # Iterate through each product in the list
    for target_item_index, product in enumerate(product_list):
        # Get similar items based on cosine similarity
        similar_items = list(enumerate(cosine_sim[target_item_index]))
        N = 20  # Number of recommendations
        top_similar_items = sorted(similar_items, key=lambda x: x[1], reverse=True)[:N]
        recommended_item_indices = [i for i, _ in top_similar_items]

        # Add recommended items to the set
        for index in recommended_item_indices:
            recommended_items.add(product_list[index])

    # Convert the set of recommended items to a list
    recommended_items_list = list(recommended_items)

    # Update the 'recommended' field to True for recommended items in the database
    for item in recommended_items_list:
        if not item.recommended:
            item.recommended.add(user)
            item.save()

    return recommended_items_list


def home(request):
    context = {}
    trending = Product.objects.order_by("-average_rating")[:9]
    context["trending"] = trending
    if request.user.is_authenticated:
        brought_count = [_ for _ in Product.objects.filter(brought=request.user)]
        viewed = [_ for _ in Product.objects.filter(viewed=request.user)]
        liked = [_ for _ in Product.objects.filter(liked=request.user)]
        comb = brought_count + viewed + liked
        brought = [_.product_id for _ in brought_count]
        print(liked)
        liked_not_brought = set(liked) - set(brought)

        recommended = get_recommended_item_list(comb, request.user) if comb else []
        print(recommended)

        recommended_counts = len(recommended)
        print(recommended_counts)
        rec_len = Product.objects.filter(recommended=request.user).count()
        liked = Product.objects.filter(liked=request.user)

        if recommended_counts == 0:
            category_list = (
                Product.objects.all().values_list("category", flat=True).distinct()
            )
            for category in category_list:
                product = Product.objects.filter(category=category).order_by(
                    "-average_rating"
                )[:10]
                context[category] = product

            return render(
                request,
                "home.html",
                {"context": context, "continue": liked_not_brought},
            )

        else:
            # Get the top voted, unbrought  and recommended products
            products = Product.objects.filter(recommended=request.user).order_by(
                "-total_ratings"
            )[:30]
            category_list = (
                Product.objects.filter(recommended=request.user)
                .values_list("category", flat=True)
                .distinct()
            )
            for category in category_list:
                product = Product.objects.filter(category=category).order_by(
                    "-average_rating"
                )[:10]
                context[category] = product
            # print(context)
            return render(
                request,
                "home.html",
                {
                    "recommended": products,
                    "context": context,
                    "continue": list(liked_not_brought),
                },
            )

    else:
        categories = Product.objects.values_list("category", flat=True).distinct()

        for category in categories:
            product = Product.objects.filter(category=category).order_by(
                "average_rating"
            )[:10]
            context[category] = product

        return render(request, "home.html", {"context": context})


@login_required
def like_product(request, product_id):
    previous_url = request.META.get("HTTP_REFERER")
    product = get_object_or_404(Product, pk=product_id)

    product.liked.add(request.user)
    product.save()
    # url=reverse("product_detail",args=[product_id])
    return redirect(previous_url)


@login_required
def buy_product(request, product_id):
    previous_url = request.META.get("HTTP_REFERER")

    product = get_object_or_404(Product, pk=product_id)

    product.brought.add(request.user)
    product.save()
    return redirect(previous_url)


@login_required
def show_brought(request):
    product = Product.objects.filter(brought=request.user)

    if len(product) > 0:
        return render(request, "brought.html", {"products": product})
    else:
        return render(request, "brought.html")


def remove_brought(request, product_id):
    previous_url = request.META.get("HTTP_REFERER")

    product = get_object_or_404(Product, pk=product_id)
    product.brought.remove(request.user)
    product.save()
    return redirect(previous_url)


def remove_liked(request, product_id):
    previous_url = request.META.get("HTTP_REFERER")

    product = get_object_or_404(Product, pk=product_id)
    product.liked.remove(request.user)
    product.save()
    return redirect(previous_url)
