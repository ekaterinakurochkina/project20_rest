from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from users.models import User  # Предполагается, что у вас есть модель User
from .models import Lesson, Course


class MaterialsTestCase(APITestCase):

    def setUp(self):
        self.user = User.objects.create(email="katifedr@mail.ru")
        self.course = Course.objects.create(name='Test Course', owner=self.user)
        self.lesson = Lesson.objects.create(name="Устный счет", description="Счет для детей", owner=self.user,
                                            preview=None, video_url="https://www.youtube.com/testlesson/",
                                            course=self.course)
        self.client.force_authenticate(user=self.user)

    def test_lesson_create(self):
        """Тестирование создания урока"""
        data = {
            "id": 2,
            "name": "Геометрические фигуры",
            "description": "Простейшие фигуры",
            "preview": None,
            "video_url": "https://www.youtube.com/testlesson/",
            "course": 1,
            "payment": {}
        }
        response = self.client.post("/lessons/create/", data=data, format="json")
        print(response.json())

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Lesson.objects.all().count(), 2)
        self.assertEqual(response.json(),
                         {'id': 2, 'name': 'Геометрические фигуры', 'description': 'Простейшие фигуры', 'preview': None,
                          'video_url': 'https://www.youtube.com/testlesson/', 'course': None}
                         )
        self.assertTrue(Lesson.objects.all().exists())

    def test_list_lessons(self):
        """Тестирование вывода списка уроков"""

        Lesson.objects.create(name="Test list", description="Test list")
        response = self.client.get("/lessons/")
        print(response.json())
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json(),
                         {'count': 2, 'next': None, 'previous': None, 'results': [
                             {'id': 6, 'name': 'Устный счет', 'description': 'Счет для детей', 'preview': None,
                              'video_url': 'https://www.youtube.com/testlesson/', 'course': 'Test Course'},
                             {'id': 7, 'name': 'Test list', 'description': 'Test list', 'preview': None,
                              'video_url': '', 'course': None}]}
                         )

    def test_lesson_retrieve(self):
        """Тестирование просмотра урока"""
        response = self.client.get("/lessons/3/", format="json")
        print(response.json())

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json(),
                         {'id': 3, 'name': 'Устный счет', 'description': 'Счет для детей', 'course': 'Test Course',
                          'description': 'Счет для детей', 'id': 3, 'name': 'Устный счет', 'preview': None,
                          'video_url': 'https://www.youtube.com/testlesson/'}
                         )
        self.assertTrue(Lesson.objects.all().exists())

    def test_lesson_update(self):
        """Тестирование обновления урока"""
        update_data = {
            'id': 6,
            'name': 'Устный счет (обновленный)',
            'description': 'Обновленное описание для устного счета',
            'preview': None,
            'video_url': 'https://www.youtube.com/testlesson/updated',
            'course': self.course.id,
        }

        response = self.client.put("/lessons/6/update/", data=update_data, format="json")

        print(response.json())

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.lesson.refresh_from_db()  # Обновляем объект из базы данных
        self.assertEqual(self.lesson.name, 'Устный счет (обновленный)')
        self.assertEqual(self.lesson.description, 'Обновленное описание для устного счета')
        self.assertEqual(self.lesson.video_url, 'https://www.youtube.com/testlesson/updated')



        # path("lessons/", LessonListApiView.as_view(), name="lessons_list"),
        # path("lessons/<int:pk>/", LessonRetrieveApiView.as_view(), name="lessons_retrieve"),
        # path("lessons/create/", LessonCreateApiView.as_view(), name="lessons_create"),
        # path("lessons/<int:pk>/delete/", LessonDestroyApiView.as_view(), name="lessons_delete"),
        # path("lessons/<int:pk>/update/", LessonUpdateApiView.as_view(), name="lessons_update"),
        # path("subscription/<int:pk>/", SubscriptionApiView.as_view(), name="subscription"),

    def test_lesson_delete(self):
        """Тестирование удаления урока"""

        response = self.client.delete("lessons/5/", format="json")

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(Course.objects.all().count(), 0)


        # def test_subscription(self):
        """Тестирование подписки"""

