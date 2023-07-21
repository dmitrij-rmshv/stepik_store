from django.contrib.auth.views import LoginView
from django.contrib.messages.views import SuccessMessageMixin
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.utils.timezone import now
from django.views.generic import CreateView, TemplateView, UpdateView

from common.views import TitleMixin
from users.forms import UserLoginForm, UserProfileForm, UserRegistrationForm
from users.models import EmailVerification, User


class UserLoginView(TitleMixin, LoginView):
    template_name = 'users/login.html'
    form_class = UserLoginForm
    title = 'Авторизация'


class UserRegistrationView(TitleMixin, SuccessMessageMixin, CreateView):
    model = User
    template_name = 'users/register.html'
    form_class = UserRegistrationForm
    title = 'Регистрация'
    success_url = reverse_lazy('user:login')
    success_message = 'Вы успешно зарегистрированы'


class UserProfileView(TitleMixin, UpdateView):
    model = User
    template_name = 'users/profile.html'
    form_class = UserProfileForm
    title = 'Личный кабинет'

    def get_success_url(self):
        return reverse_lazy('user:profile', args=(self.object.id,))

    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data()
    #     context['baskets'] = Basket.objects.filter(user=self.object)
    #     return context


class EmailVerificationView(TitleMixin, TemplateView):
    template_name = 'users/email_verification.html'
    title = 'Подтверждение электронной почты'

    def get(self, request, *args, **kwargs):
        code = kwargs['code']
        try:
            user = User.objects.get(email=kwargs['email'])
        except ObjectDoesNotExist:
            return HttpResponseRedirect(reverse('index'))
        if EmailVerification.objects.filter(code=code, user=user, expiration__gte=now()).exists():
            user.is_verified_email = True
            user.save()
        else:
            return HttpResponseRedirect(reverse('index'))
        return super().get(request, *args, **kwargs)
