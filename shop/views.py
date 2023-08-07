from django.shortcuts import render, get_object_or_404
from cart.forms import CartAddProductForm

from .models import Category, Product
from .recomender import Recommender


def product_list(request, category_slug=None):
    """All products or filtered by slug if given."""
    category = None
    categories = Category.objects.all()
    products = Product.objects.filter(available=True)

    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(slug=category_slug)

    return render(
        request,
        "shop/product/list.html",
        {"category": category, "categories": categories, "products": products},
    )


def product_detail(request, id, slug):
    """One product"""
    product = get_object_or_404(Product, id=id, slug=slug, available=True)
    cart_product_form = CartAddProductForm()
    r = Recommender()
    recommended = r.suggest_products_for([product], 4)
    return render(
        request,
        "shop/product/detail.html",
        {
            "product": product,
            "cart_product_form": cart_product_form,
            "recommended_products": recommended,
        },
    )
