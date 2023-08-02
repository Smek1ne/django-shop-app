import stripe
from django.conf import settings
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from orders.models import Order
from payment.tasks import payment_completed


@csrf_exempt
def stripe_webhook(request):
    event = None
    try:
        event = stripe.Webhook.construct_event(
            payload=request.body,
            sig_header=request.META("HTTP_STRIPE_SIGNATURE"),
            secret=settings.STRIPE_WEBHOOK_SECRET,
        )
    except (ValueError, stripe.error.SignatureError):
        return HttpResponse(status=400)

    if event.type == "checkout.session.completed":
        session = event.data.object

        if session.mode == "payment" and session.payment_status == "paid":
            try:
                order = Order.objects.get(id=session.client_reference_id)
            except Order.DoesNotExist:
                return HttpResponse(status=404)

            order.paid = True
            order.stripe_id = session.payment_intent
            order.save()
            payment_completed.delay(order.id)

    return HttpResponse(status=200)
