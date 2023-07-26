from django.shortcuts import render

from cart.cart import Cart
from .forms import OrderCreateForm
import services

# Create your views here.


def order_create(request):
    cart = Cart(request)
    if request.method == "POST":
        form = OrderCreateForm(request.POST)
        if form.is_valid():
            order = form.save()
            services.create_order_items(order, cart)
            cart.clear()
            return render(
                request, "orders/order/created.html", {"order": order}
            )
    else:
        form = OrderCreateForm()
    return render(
        request, "orders/order/create.html", {"cart": cart, "form": form}
    )
