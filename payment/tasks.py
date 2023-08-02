from django.core.mail import EmailMessage
from django.http import HttpResponse

from orders.models import Order
from orders.services import render_to_pdf
from celery import shared_task


@shared_task
def payment_completed(order_id):
    order = Order.objects.filter(id=order_id)
    email = EmailMessage(
        f"My Shop – Invoice no. {order.id}",
        "Please, find attached the invoice for your recent purchase.",
        'admin@myshop.com',
        [order.email],
    )
    pdf = render_to_pdf("orders/order/pdf.html", {order: order})
    email.attach(f"order_{order.id}.pdf", pdf, "application/pdf")
    email.send()
