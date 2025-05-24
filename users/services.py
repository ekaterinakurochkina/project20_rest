import stripe
from django.conf import settings

stripe.api_key = settings.STRIPE_API_KEY


def stripe_create_product(obj):
    """Создает продукт в страйпе"""
    return stripe.Product.create(name=obj.name)


def create_stripe_price(obj, payment_amount):
    """Создает цену в страйпе"""
    return stripe.Price.create(
        currency="rub",
        unit_amount=payment_amount * 100,  # умножаем на 100, чтобы цена была в рублях, а не копейках
        product_data={"name": obj.get("name")},
    )


def create_stripe_session(price):
    """Создает сессию на оплату в страйпе"""
    session = stripe.checkout.Session.create(
        success_url="https://127.0.0.1:8000/",
        line_items=[{"price": price.get("id"), "quantity": 1}],
        mode="payment",
    )
    return session.get("id"), session.get("url")
