from decimal import Decimal

from django.conf import settings

from coupons.models import Coupon
from shop.models import Product


class Cart:
    def __init__(self, request):
        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID)

        if not cart:
            cart = self.session[settings.CART_SESSION_ID] = {}
        self.cart = cart
        self.coupon_id = self.session.get("coupon_id")

    def add(self, product, quantity=1, override_quantity=False):
        """Add product to cart"""
        product_id = str(product.id)
        if product_id not in self.cart:
            self.cart[product_id] = {"quantity": 0, "price": str(product.price)}

        if override_quantity:
            self.cart[product_id]["quantity"] = quantity
        else:
            self.cart[product_id]["quantity"] += quantity

        self.save()

    def save(self):
        """Mark session as modified"""
        self.session.modified = True

    def remove(self, product):
        """Remove product from cart"""
        product_id = str(product.id)

        if product_id is self.cart:
            del self.cart[product_id]
            self.save()

    def __iter__(self):
        product_ids = self.cart.keys()
        products = Product.objects.filter(id__in=product_ids)
        cart = self.cart.copy()

        for product in products:
            cart[str(product.id)]["product"] = product

        for item in cart.values():
            item["price"] = Decimal(item["price"])
            item["total_price"] = item["price"] * item["quantity"]
            yield item

    def __len__(self):
        """Calc products in the cart"""
        return sum(item["quantity"] for item in self.cart.values())

    def get_total_price(self):
        """Total price of all products in the cart"""
        return sum(
            item["quantity"] * Decimal(item["price"])
            for item in self.cart.values()
        )

    def clear(self):
        """Delete cart from the session"""
        del self.session[settings.CART_SESSION_ID]
        self.save()

    @property
    def coupon(self):
        """Coupon object if coupon in session or None"""
        if self.coupon_id:
            try:
                return Coupon.objects.get(id=self.coupon_id)
            except Coupon.DoesNotExist:
                pass
        return None

    def get_discount(self):
        """Discount for all products in the cart"""
        if self.coupon:
            return self.coupon.discount / Decimal(100) * self.get_total_price()
        return Decimal(0)

    def get_total_price_after_discount(self):
        return self.get_total_price() - self.get_discount()
