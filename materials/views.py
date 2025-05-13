from rest_framework.generics import CreateAPIView, ListAPIView, UpdateAPIView, DestroyAPIView, RetrieveAPIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.viewsets import ModelViewSet

from materials.models import Course, Lesson, Subscription
from materials.serializers import CourseSerializer, LessonSerializer, SubscriptionSerializer
from users.permissions import IsModer, IsOwner


class CourseViewSet(ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer

    def get_permissions(self):
        if self.action == "create":
            self.permission_classes = (~IsModer,)
        elif self.action in ["update", "retrieve"]:
            self.permission_classes = (IsModer | IsOwner,)
        elif self.action == "destroy":
            self.permission_classes = (~IsModer | IsOwner,)
        elif self.action == "list":
            self.permission_classes = (AllowAny,)
        return super().get_permissions()

    def perform_create(self, serializer):
        course = serializer.save()
        course.owner = self.request.user
        course.save()

class LessonCreateApiView(CreateAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = (~IsModer, IsAuthenticated)

    def perform_create(self, serializer):
        lesson = serializer.save()
        lesson.owner = self.request.user
        lesson.save()

class LessonListApiView(ListAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = (IsAuthenticated)

    def get_queryset(self):
        queryset = super().get_queryset()
        if self.request.query_params.get('pk'):
            queryset = queryset.filter(course_id=int(self.request.query_params.get('pk')))
        return queryset


class LessonRetrieveApiView(RetrieveAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = (IsAuthenticated, IsModer | IsOwner)


class LessonUpdateApiView(UpdateAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = (IsAuthenticated, IsModer | IsOwner)

class LessonDestroyApiView(DestroyAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = (IsAuthenticated, ~IsModer, IsOwner)

# class SubscriptionApiView(CreateAPIView):
#     queryset = Subscription.objects.all()
#     serializer_class = SubscriptionSerializer
#     permission_classes = (IsAuthenticated)
#
#     def post(self, *args, **kwargs):
#         user = self.requests.course_id
#         self.reqests.data
#         course_item = получаем
#
#         # Если подписка у пользователя на этот курс есть - удаляем ее
#         if subs_item.exists():
#             ...
#             message = 'подписка удалена'
#         # Если подписки у пользователя на этот курс нет - создаем ее
#         else:
#             ...
#             message = 'подписка добавлена'
#         # Возвращаем ответ в API
#         return Response({"message": message})
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from .models import Subscription, Course  # Импортируйте ваши модели
from .serializers import SubscriptionSerializer  # Импортируйте ваш сериализатор

class SubscriptionApiView(APIView):
    permission_classes = [IsAuthenticated]  # Ограничьте доступ только для авторизованных пользователей

    def post(self, request, *args, **kwargs):
        serializer = SubscriptionSerializer(data=request.data)  # Создаем экземпляр сериализатора с данными запроса
        serializer.is_valid(raise_exception=True)  # Проверяем валидность данных

        user = request.user  # Получаем пользователя из запроса
        course_id = serializer.validated_data['course_id']  # Получаем ID курса из валидированных данных

        # Получаем объект курса или возвращаем 404, если курс не найден
        course_item = get_object_or_404(Course, id=course_id)

        # Получаем подписку для текущего пользователя и курса
        subs_item = Subscription.objects.filter(user=user, course=course_item)

        # Если подписка у пользователя на этот курс есть - удаляем ее
        if subs_item.exists():
            subs_item.delete()  # Удаляем подписку
            message = 'Подписка удалена'
        # Если подписки у пользователя на этот курс нет - создаем ее
        else:
            Subscription.objects.create(user=user, course=course_item, is_subscription=True)  # Создаем новую подписку
            message = 'Подписка добавлена'

        # Возвращаем ответ в API
        return Response({"message": message}, status=status.HTTP_200_OK)

