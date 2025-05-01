from rest_framework import serializers
from rest_framework.fields import SerializerMethodField
from rest_framework.serializers import ModelSerializer, Serializer
from materials.models import Course, Lesson
from users.models import User, Payments
from users.serializer import PaymentsSerializer

class CourseSerializer(ModelSerializer):
    lessons = serializers.SerializerMethodField()
    payment = PaymentsSerializer(many=True, read_only=True)

    def get_lessons(self, course):
        # return course.lessons.count()
        return [lesson.name for lesson in course.lessons.all()]

    class Meta:
        model = Course
        fields = ("id", "name", "description", "preview", "lessons", "payment")

class LessonSerializer(ModelSerializer):
    course = CourseSerializer(read_only=True)
    payment = PaymentsSerializer(many=True, read_only=True)

    class Meta:
        model = Lesson
        fields = ("id", "course", "name", "description", "preview", "video_url", "payment")
