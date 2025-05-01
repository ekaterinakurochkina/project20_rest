from django_filters import filters
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import serializers
from rest_framework.fields import SerializerMethodField
from rest_framework.serializers import ModelSerializer, Serializer

from django.db import models
from materials.models import Course, Lesson
from users.models import Payments
from rest_framework import filters

class PaymentsSerializer(ModelSerializer):
    payments = serializers.SerializerMethodField()
    course = models.ForeignKey(Course, related_name='payments', null=True, blank=True, on_delete=models.CASCADE)
    lesson = models.ForeignKey(Lesson, related_name='payments', null=True, blank=True, on_delete=models.CASCADE)
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter, filters.SearchFilter]
    filterset_fields = ("payment_course", "payment_lesson", "payment_method",)
    ordering_fields = ("payment_date",)
    search_fields = ("user",)

    def get_payments(self, payments):
        related_payments = payments.course.payment.all() if payments.course else payments.lesson.payment.all()

    class Meta:
        model = Payments
        fields = ['id', 'user', 'course', 'lesson', 'payment_amount', 'payment_date', 'payments']