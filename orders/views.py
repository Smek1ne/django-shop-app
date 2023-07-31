from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse

from cart.cart import Cart

# from .services import create_order_items
from orders import services, tasks
from .forms import OrderCreateForm
from .models import Order


# Create your views here.


def order_create(request):
    """
    Creates order, order_items and starts task(email sending) if POST
    or renders creation form if GET
    """
    cart = Cart(request)
    if request.method == "POST":
        form = OrderCreateForm(request.POST)
        if form.is_valid():
            order = form.save()
            services.create_order_items(order, cart)
            cart.clear()
            tasks.order_created.delay(order.id)
            request.session["order_id"] = order.id
            return redirect(reverse("payment:process"))
    else:
        form = OrderCreateForm()
    return render(
        request, "orders/order/create.html", {"cart": cart, "form": form}
    )


def order_detail(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    return render(request, "admin/orders/order/detail.html", {"order": order})
