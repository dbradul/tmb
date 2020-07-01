from django.conf import settings
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView

from account.forms import AccountRegistrationForm, AccountProfileForm
from account.models import User


class CreateAccountView(CreateView):
    model = settings.AUTH_USER_MODEL
    template_name = 'registration.html'
    form_class = AccountRegistrationForm
    extra_context = {'title' : 'Register new user'}
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        result = super().form_valid(form)
        messages.success(self.request, "Great! New user has been successfully created!")
        return result

class AccountLoginView(LoginView):
    template_name = 'login.html'
    extra_context = {'title': 'Login as a user'}
    success_url = reverse_lazy('index')

    def form_valid(self, form):
        result = super().form_valid(form)
        messages.success(self.request, "Great! You've just successfully logged in!")
        return result


class AccountLogoutView(LoginRequiredMixin, LogoutView):
    template_name = 'logout.html'
    extra_context = {'title': 'Logged out from TMB'}
    login_url = reverse_lazy('login')

class AccountProfileView(LoginRequiredMixin, UpdateView):
    template_name = 'profile.html'
    extra_context = {'title': 'Edit current user profile'}
    form_class = AccountProfileForm
    success_url = reverse_lazy('profile')
    login_url = reverse_lazy('login')

    def get_object(self, *args):
        return self.request.user
