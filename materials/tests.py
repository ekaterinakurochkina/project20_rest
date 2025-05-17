from rest_framework import status
from rest_framework.test import APITestCase

from users.models import User  # Предполагается, что у вас есть модель User
from .models import Lesson, Course


class MaterialsTestCase(APITestCase):

    def setUp(self):
        self.user = User.objects.create(email="katifedr@mail.ru")
        self.course = Course.objects.create(name='Test Course', owner=self.user)
        # self.course = Course.objects.create(name="Математика")
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
                             {'id': 3, 'name': 'Устный счет', 'description': 'Счет для детей', 'preview': None,
                              'video_url': 'https://www.youtube.com/testlesson/', 'course': 'Test Course'},
                             {'id': 4, 'name': 'Test list', 'description': 'Test list', 'preview': None,
                              'video_url': '', 'course': None}]}
                         )

    def test_lesson_retrieve(self):
        """Тестирование просмотра урока"""
        response = self.client.get("/lessons/2/", format="json")
        print(response.json())

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json(),
                         {'id': 4, 'name': 'Устный счет', 'description': 'Счет для детей', 'preview': None,
                          'video_url': 'https://www.youtube.com/testlesson/', 'course': None}
                         )
        self.assertTrue(Lesson.objects.all().exists())

    # def test_lesson_update(self):
        """Тестирование вывода списка уроков"""
        # path("lessons/", LessonListApiView.as_view(), name="lessons_list"),
        # path("lessons/<int:pk>/", LessonRetrieveApiView.as_view(), name="lessons_retrieve"),
        # path("lessons/create/", LessonCreateApiView.as_view(), name="lessons_create"),
        # path("lessons/<int:pk>/delete/", LessonDestroyApiView.as_view(), name="lessons_delete"),
        # path("lessons/<int:pk>/update/", LessonUpdateApiView.as_view(), name="lessons_update"),
        # path("subscription/<int:pk>/", SubscriptionApiView.as_view(), name="subscription"),

    # def test_lesson_delete(self):
        """Тестирование удаления урока"""

    # def test_subscription(self):
        """Тестирование подписки"""

    # def test_lessons_retrieve(self):
    #     # url = reverse("materials:lessons_detail", args=(self.lessons.pk))
    #     response = self.client.get("/lessons/<int:pk>/", format="json")
    #     data = response.json()
    #     print(response.json())
    #     self.assertEqual(response.status_code, status.HTTP_200_OK)

# class CourseTestCase(APITestCase):
#
#     def setUp(self):
#         self.user = User.objects.create(email='katifedr@mail.ru')
#         self.course = Course.objects.create(name='Test Course', owner=self.user)
#
#     def test_course_create(self):
#         url = reverse('lessons_create')
#         data = {'name': 'New Course', 'owner': self.user.id}
#         response = self.client.post(url, data)
#         self.assertEqual(response.status_code, status.HTTP_201_CREATED)
#         self.assertTrue(Course.objects.filter(name='New Course').exists())
#
#     def test_course_list(self):
#         url = reverse('lessons_list')
#         response = self.client.get(url)
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#
#
# class LessonTestCase(APITestCase):
#     def setUp(self):
#         self.user = User.objects.create(email='katifedr@mail.ru')
#         self.course = Course.objects.create(name='Test Course', owner=self.user)
#         self.lesson = Lesson.objects.create(name='Test Lesson', course=self.course,
#                                             video_url='https://www.youtube.com/test')
#
#     def test_lessons_retrieve(self):
#         url = reverse('lessons_detail', args=[self.lesson.id])
#         response = self.client.get(url)
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         self.assertEqual(response.data['name'], 'Test Lesson')
#
#     def test_lessons_create(self):
#         url = reverse('lessons_create')
#         data = {
#             'name': 'New Lesson',
#             'course': self.course.id,
#             'video_url': 'https://www.youtube.com/newlesson'
#         }
#         response = self.client.post(url, data)
#         self.assertEqual(response.status_code, status.HTTP_201_CREATED)
#         self.assertTrue(Lesson.objects.filter(name='New Lesson').exists())

#     def test_lesson_update(self):
#         url = reverse('lessons_update', args=[self.lesson.id])
#         data = {'name': 'Updated Lesson'}
#         response = self.client.patch(url, data)
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         self.lesson.refresh_from_db()
#         self.assertEqual(self.lesson.name, 'Updated Lesson')
#
#     def test_lesson_delete(self):
#         url = reverse('lessons_delete', args=[self.lesson.id])
#         response = self.client.delete(url)
#         self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
#         self.assertFalse(Lesson.objects.filter(id=self.lesson.id).exists())
#
# class SubscriptionTestCase(APITestCase):
#     def setUp(self):
#         self.user = User.objects.create(email='katifedr@mail.ru')
#         self.course = Course.objects.create(name='Test Course', owner=self.user)
#
#     def test_subscription_create(self):
#         url = reverse('subscription', args=[self.course.id])
#         data = {'user': self.user.id, 'course': self.course.id, 'is_subscription': True}
#         response = self.client.post(url, data)
#         self.assertEqual(response.status_code, status.HTTP_201_CREATED)
#         self.assertTrue(Subscription.objects.filter(user=self.user, course=self.course).exists())
#
#     def test_unsubscription(self):
#         Subscription.objects.create(user=self.user, course=self.course, is_subscription=True)
#         url = reverse('subscription', args=[self.course.id])
#         response = self.client.delete(url)
#         self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
#         self.assertFalse(Subscription.objects.filter(user=self.user, course=self.course).exists())
