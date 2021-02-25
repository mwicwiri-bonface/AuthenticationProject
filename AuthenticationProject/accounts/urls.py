from django.urls import path
from .views import SignUpView, ActivateAccount, user_login, profile, change_password

urlpatterns = [
    path('signup/', SignUpView.as_view(), name='sign-up'),
    path('activate/<uidb64>/<token>/', ActivateAccount.as_view(), name='activate'),
    path('login/', user_login, name='login'),
    path('profile/', profile, name='profile'),
    path('change-password/', change_password, name='change-password'),
]