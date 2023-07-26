from .models import OrderItem


def create_order_items(order, cart):
    for item in cart:
        OrderItem.objects.create(
            order=order,
            product=item["product"],
            item=item["price"],
            quantity=item["quantity"],
        )
