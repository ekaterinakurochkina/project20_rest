from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from users.models import User  # Предполагается, что у вас есть модель User
from .models import Lesson, Course, Subscription


class MaterialsTestCase(APITestCase):

    def setUp(self):
        self.user = User.objects.create(email="test@test.ru")
        self.course = Course.objects.create(
            name="test_course", description="test_description", owner=self.user
        )
        self.lesson = Lesson.objects.create(
            name="test_lesson", course=self.course, owner=self.user
        )
        self.ubscription = Subscription.objects.create(course=self.course, user=self.user)
        self.client.force_authenticate(user=self.user)

    def test_lesson_retrieve(self):
        """Тестирование просмотра урока"""
        url = reverse("materials:lessons_retrieve", args=(self.lesson.pk,))
        response = self.client.get(url)
        data = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data.get("name"), self.lesson.name)

    def test_lesson_create(self):
        """Тестирование создания урока"""
        url = reverse("materials:lessons_create")
        data = {
            "name": "Геометрические фигуры",
            "description": "Простейшие фигуры",
            "preview": None,
            "video_url": "https://www.youtube.com/testlesson/",
            "course": 1,
            "payment": {}
        }
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Lesson.objects.all().count(), 2)