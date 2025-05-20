from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from materials.models import Course, Lesson, Subscription
from users.serializer import PaymentsSerializer, UserSerializer


class LessonSerializer(ModelSerializer):
    course = serializers.StringRelatedField()
    # course = CourseSerializer(read_only=True)
    payment = PaymentsSerializer(many=True, read_only=True)

    class Meta:
        model = Lesson
        fields = ("id", "name", "description", "preview", "video_url", "course", "payment")


class CourseSerializer(ModelSerializer):
    lessons = LessonSerializer(many=True, read_only=True)
    lesson_count = serializers.SerializerMethodField()
    payment = PaymentsSerializer(many=True, read_only=True)

    def get_lessons(self, course):
        return [lesson.name for lesson in course.lessons.all()]

    def get_lesson_count(self, course):
        return course.lessons.count()

    class Meta:
        model = Course
        fields = ("id", "name", "description", "preview", "lessons", "lesson_count", "payment")


class SubscriptionSerializer(serializers.ModelSerializer):
    course = CourseSerializer(many=True, read_only=True)
    user = UserSerializer(many=True, read_only=True)
    course_id = serializers.PrimaryKeyRelatedField(queryset=Course.objects.all(), write_only=True)

    class Meta:
        model = Subscription
        fields = ['id', 'is_subscription', 'user', 'course', 'course_id']

    def create(self, validated_data):
        # Извлекаем course_id из validated_data
        course_id = validated_data.pop('course_id', None)  # Удаляем course_id из validated_data
        user = validated_data.pop('user', None)  # Удаляем user

        # Создаем подписку
        subscription = Subscription.objects.create(course_id=course_id, user=user, **validated_data)
        return subscription
