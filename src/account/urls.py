from django.urls import path

from account.views import CreateAccountView, AccountLoginView, AccountLogoutView, AccountProfileView

urlpatterns = [
    path('register/', CreateAccountView.as_view(), name='registration'),
    path('login/', AccountLoginView.as_view(), name='login'),
    path('logout/', AccountLogoutView.as_view(), name='logout'),
    path('profile/', AccountProfileView.as_view(), name='profile'),
]
