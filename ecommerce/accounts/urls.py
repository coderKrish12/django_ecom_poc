from django.urls import path
from .views import UserRegistrationView, UserLoginView, UserProfileView, UserLogoutView
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    path('register/', UserRegistrationView.as_view(), name='user-registration'),
    path('login/', UserLoginView.as_view(), name='user-login'),
    path('user-data/', UserProfileView.as_view(), name='user-data'),
    path('logout/', UserLogoutView.as_view(), name='user-logout'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token-refresh'),
]

