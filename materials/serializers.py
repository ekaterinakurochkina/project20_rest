from rest_framework import serializers


from materials.models import Course, Lesson, Subscription
from materials.validators import VideoUrlValidator
from users.serializer import PaymentsSerializer, UserSerializer


class LessonSerializer(serializers.ModelSerializer):
    course = serializers.StringRelatedField(read_only=True)
    # course = CourseSerializer(read_only=True)
    payment = PaymentsSerializer(many=True, read_only=True)

    class Meta:
        model = Lesson
        fields = ("id", "name", "description", "preview", "video_url", "course", "payment")
        video_url = serializers.CharField(validators=[VideoUrlValidator])

class CourseSerializer(serializers.ModelSerializer):
    lessons = LessonSerializer(many=True, read_only=True)
    lesson_count = serializers.SerializerMethodField()
    payment = PaymentsSerializer(many=True, read_only=True)
    is_subscribed = serializers.SerializerMethodField(read_only=True)  # Добавляем поле для проверки подписки

    def get_lessons(self, course):
        return [lesson.name for lesson in course.lessons.all()]

    def get_lesson_count(self, course):
        return course.lessons.count()

    def get_is_subscribed(self, obj):
        user = self.context['request'].user  # Получаем текущего пользователя из контекста
        return Subscription.objects.filter(user=user, course=obj).exists()  # Проверяем наличие подписки

    class Meta:
        model = Course
        fields = ("id", "name", "description", "preview", "lessons","lesson_count", "payment", "is_subscribed")



