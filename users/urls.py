from django.urls import path
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from users.apps import UsersConfig
from users.views import PaymentsCreateApiView, PaymentsUpdateApiView, PaymentsRetrieveApiView, PaymentsDestroyApiView, \
    PaymentsListApiView, UserCreateApiView

app_name = UsersConfig.name

urlpatterns = [
    path("payments/", PaymentsListApiView.as_view(), name="payments_list"),
    path("payments/<int:pk>/", PaymentsRetrieveApiView.as_view(), name="payment_retrieve"),
    path("payments/create/", PaymentsCreateApiView.as_view(), name="payment_create"),
    path("payments/<int:pk>/delete/", PaymentsDestroyApiView.as_view(), name="payment_delete"),
    path("payments/<int:pk>/update/", PaymentsUpdateApiView.as_view(), name="payment_update"),

    path('login/', TokenObtainPairView.as_view(permission_classes=(AllowAny,)), name='login'),
    path('token/refresh/', TokenRefreshView.as_view(permission_classes=(AllowAny,)), name='token_refresh'),
    path('register/', UserCreateApiView.as_view(), name='register'),

]
