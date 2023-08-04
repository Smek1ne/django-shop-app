from django.shortcuts import render, redirect
from django.utils import timezone
from django.views.decorators.http import require_POST
from .forms import CouponForm
from .models import Coupon


@require_POST
def coupon_apply(request):
    form = CouponForm(request.POST)
    if form.is_valid():
        now = timezone.now()
        code = form.cleaned_data["code"]
        try:
            coupon = Coupon.objects.get(
                code__iexact=code,
                valid_from__lte=now,
                valid_to__gte=now,
                active=True,
            )
            request.session["coupon_id"] = coupon.id

        except Coupon.DoesNotExist:
            request.session["coupon_id"] = None

        return redirect("cart:cart_detail")
