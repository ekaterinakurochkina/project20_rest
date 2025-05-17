from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from rest_framework import status
from rest_framework.generics import CreateAPIView, ListAPIView, UpdateAPIView, DestroyAPIView, RetrieveAPIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from materials.models import Course, Lesson
# from config.settings import EMAIL_HOST_USER
from users.models import Payments
from users.models import User
from users.serializer import PaymentsSerializer, UserSerializer


class PaymentsCreateApiView(CreateAPIView):
    queryset = Payments.objects.all()
    serializer_class = PaymentsSerializer

    def create(self, request, *args, **kwargs):
        course_id = request.data.get('course_id')
        lesson_id = request.data.get('lesson_id')
        payment_amount = request.data.get('payment_amount')
        payment_method = request.data.get('payment_method', 'transfer')  # Устанавливаем значение по умолчанию

        if course_id:
            course = Course.objects.get(id=course_id)
            payment = Payments.objects.create(user=request.user, course=course, payment_amount=payment_amount,
                                              payment_method=payment_method)
        elif lesson_id:
            lesson = Lesson.objects.get(id=lesson_id)
            payment = Payments.objects.create(user=request.user, lesson=lesson, payment_amount=payment_amount,
                                              payment_method=payment_method)
        else:
            return Response({'error': 'Необходимо указать курс или урок'}, status=status.HTTP_400_BAD_REQUEST)

        return Response(PaymentsSerializer(payment).data, status=status.HTTP_201_CREATED)


class PaymentsListApiView(ListAPIView):
    queryset = Payments.objects.all()
    serializer_class = PaymentsSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter, filters.SearchFilter]
    filterset_fields = ("course_id", "lesson_id", "payment_method",)
    ordering_fields = ("payment_date",)
    search_fields = ("user",)


class PaymentsRetrieveApiView(RetrieveAPIView):
    queryset = Payments.objects.all()
    serializer_class = PaymentsSerializer


class PaymentsUpdateApiView(UpdateAPIView):
    queryset = Payments.objects.all()
    serializer_class = PaymentsSerializer


class PaymentsDestroyApiView(DestroyAPIView):
    queryset = Payments.objects.all()
    serializer_class = PaymentsSerializer


class UserCreateApiView(CreateAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes = (AllowAny,)  # открыли доступ к классу регистрации пользователя

    def perform_create(self, serializer):
        user = serializer.save(is_active=True)
        user.set_password(user.password)
        user.save()


class UserUpdateApiView(UpdateAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()


class UserListApiView(UpdateAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()


class UserRetrieveApiView(RetrieveAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()


class UserDestroyApiView(DestroyAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()
