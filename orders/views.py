from django.shortcuts import render

from cart.cart import Cart
from .forms import OrderCreateForm

# from .services import create_order_items
from orders import services, tasks

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
            return render(
                request, "orders/order/created.html", {"order": order}
            )
    else:
        form = OrderCreateForm()
    return render(
        request, "orders/order/create.html", {"cart": cart, "form": form}
    )
