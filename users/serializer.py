from django_filters import filters
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import serializers
from rest_framework.fields import SerializerMethodField
from rest_framework.serializers import ModelSerializer, Serializer
from users.models import Payments
from rest_framework import filters

class PaymentsSerializer(ModelSerializer):
    payments = serializers.SerializerMethodField()
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter, filters.SearchFilter]
    filterset_fields = ("payment_course", "payment_lesson", "payment_method",)
    ordering_fields = ("payment_date",)
    search_fields = ("user",)

    def get_payments(self, payments):
        return payments.lessons.count()

    class Meta:
        model = Payments
        fields = ("user", "payment_date", "payment_course", "payment_lesson", "payment_amount", "payment_method")