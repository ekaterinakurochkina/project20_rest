import stripe

from config.settings import STRIPE_API_KEY

stripe.api_key = STRIPE_API_KEY
from forex_python.converter import CurrencyRates


def convert_rub_to_dollars(amount):
    """Конвертирует рубли в доллары"""
    c = CurrencyRates()
    rate = c.get_rate('RUB', 'USD')  # курс рубля к доллару, float
    return int(amount * rate)


def create_stripe_price(amount):
    """Создает цену в страйпе"""
    return stripe.Price.create(
        currency="usd",
        unit_amount=amount * 100,  # т.к. на вход страйп получает центы
        # currency="rub",
        # unit_amount=amount * 100, # умножаем на 100, чтобы цена была в рублях, а не копейках
        # recurring={"interval": "month"}, # периодичность платежа раз в месяц нам не нужна
        product_data={"name": "Donation"},
    )


def create_stripe_session(price):
    """Создает сессию на оплату в страйпе"""
    session = stripe.checkout.Session.create(
        success_url="https://127.0.0.1:8000",
        line_items=[{"price": price.get("id"), "quantity": 1}],
        mode="payment",
    )
    return session.get("id"), session.get("url")
