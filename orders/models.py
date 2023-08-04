from django.conf import settings
from django.db import models
from django.db.models import PositiveIntegerField

from shop.models import Product
from coupons.models import Coupon
from django.core.validators import MinValueValidator, MaxValueValidator
from decimal import Decimal


# Create your models here.
class Order(models.Model):
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    email = models.EmailField()
    address = models.CharField(max_length=250)
    postal_code = models.CharField(max_length=200)
    city = models.CharField(max_length=200)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    paid = models.BooleanField(default=False)
    stripe_id = models.CharField(max_length=250, blank=True)

    coupon = models.ForeignKey(
        Coupon, null=True, blank=True, on_delete=models.SET_NULL
    )
    discount = models.IntegerField(
        default=0, validators=[MinValueValidator(0), MaxValueValidator(100)]
    )

    class Meta:
        ordering = ["-created"]
        indexes = [
            models.Index(
                fields=["-created"],
            )
        ]

    def __str__(self):
        return f"Order {self.id}"

    def get_cost_before_discount(self):
        return sum(item.get_cost() for item in self.items.all())

    def get_discount(self):
        if self.discount:
            cost = self.get_cost_before_discount()
            return self.discount / Decimal(100) * cost
        return Decimal(0)

    def get_total_cost(self):
        return self.get_cost_before_discount() - self.get_discount()

    def get_stripe_url(self):
        if not self.stripe_id:
            return ""
        if "_test_" in settings.STRIPE_SECRET_KEY:
            return "/test/"
        else:
            return f"https://dashboard.stripe.com/payments/{self.stripe_id}"


class OrderItem(models.Model):
    order = models.ForeignKey(
        Order, related_name="items", on_delete=models.CASCADE
    )
    product = models.ForeignKey(
        Product, related_name="order_items", on_delete=models.CASCADE
    )
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = PositiveIntegerField(default=1)

    def __str__(self):
        return str(self.id)

    def get_cost(self):
        return self.price * self.quantity
