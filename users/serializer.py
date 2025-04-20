from rest_framework import serializers
from rest_framework.fields import SerializerMethodField
from rest_framework.serializers import ModelSerializer, Serializer
from users.models import Payments


class PaymentsSerializer(ModelSerializer):
    payments = serializers.SerializerMethodField()

    def get_payments(self, payments):
        return payments.lessons.count()

    class Meta:
        model = Payments
        fields = ("user", "payment_date", "payment_course", "payment_lesson", "payment_amount", "payment_method")