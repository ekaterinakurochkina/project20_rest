from rest_framework import serializers
from rest_framework.fields import SerializerMethodField
from rest_framework.serializers import ModelSerializer, Serializer
from materials.models import Course, Lesson


class CourseSerializer(ModelSerializer):
    lessons = serializers.SerializerMethodField()

    def get_lessons(self, course):
        return course.lessons.count()

    class Meta:
        model = Course
        fields = ("name", "description", "preview", "lessons")

class LessonSerializer(ModelSerializer):
    course = CourseSerializer(read_only=True)

    class Meta:
        model = Lesson
        fields = "__all__"