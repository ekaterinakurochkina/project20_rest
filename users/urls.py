from django.contrib.auth.views import LoginView
from django.urls import path
from rest_framework.decorators import permission_classes
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from users.apps import UsersConfig
from users.views import PaymentsCreateApiView, PaymentsUpdateApiView, PaymentsRetrieveApiView, PaymentsDestroyApiView, \
    PaymentsListApiView, UserCreateApiView

app_name = UsersConfig.name

urlpatterns = [
    # path('login/', LoginView.as_view(template_name="login.html"), name='login'),
    # path('logout/', logout_view, name='logout'),
    # path('register/', UserCreateView.as_view(template_name="user_form.html"), name='register'),
    # path('email-confirm/<str:token>/', email_verification, name='email-confirm'),
    # path('list/', UserListView.as_view(), name='user_list'),
    # path('<int:pk>/delete/', UserDeleteView.as_view(), name='user_delete'),
    # path('<int:pk>/edit/', UserUpdateView.as_view(), name='user_edit'),
    path("payments/", PaymentsListApiView.as_view(), name="payments_list"),
    path("payments/<int:pk>/", PaymentsRetrieveApiView.as_view(), name="payment_retrieve"),
    path("payments/create/", PaymentsCreateApiView.as_view(), name="payment_create"),
    path("payments/<int:pk>/delete/", PaymentsDestroyApiView.as_view(), name="payment_delete"),
    path("payments/<int:pk>/update/", PaymentsUpdateApiView.as_view(), name="payment_update"),

    path('login/', TokenObtainPairView.as_view(permission_classes=(AllowAny,)), name='login'),
	path('token/refresh/', TokenRefreshView.as_view(permission_classes=(AllowAny,)), name='token_refresh'),
    path('register/', UserCreateApiView.as_view(), name='register'),
]