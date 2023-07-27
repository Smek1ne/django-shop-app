from celery import shared_task

from django.core.mail import send_mail

from .models import Order


@shared_task
def order_created(order_id):
    """Sends an email if order is created"""
    order = Order.objects.get(id=order_id)
    subject = f"Order nr. {order_id}"
    message = f"""You have successfully placed and order. 
                  You order ID is {order_id}."""

    mail_sent = send_mail(subject, message, "admin@shop.com", [order.email])
    return mail_sent


"feat: email send(Celery task, RabbitMQ) when order is created"
