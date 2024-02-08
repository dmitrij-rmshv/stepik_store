from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.contrib.messages.views import SuccessMessageMixin
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.utils.timezone import now
from django.views.generic import (CreateView, DetailView, ListView,
                                  TemplateView, UpdateView)

from common.views import TitleMixin
from users.forms import (UserFeedbackForm, UserLoginForm, UserProfileForm,
                         UserRegistrationForm)
from users.models import EmailVerification, Feedback, User
from users.utilities import fb_statuses, fb_topics


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


class UserProfileView(TitleMixin, LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = User
    template_name = 'users/profile.html'
    form_class = UserProfileForm
    title = 'Личный кабинет'
    success_url = reverse_lazy('user:profile')
    success_message = 'Данные успешно обновлены!'

    def get_object(self, queryset=None):
        return self.request.user


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


class FeedbackListView(TitleMixin, LoginRequiredMixin, ListView):
    model = Feedback
    template_name = 'users/feedbacks.html'
    title = 'Мои обращения'


class FeedbackDetailView(TitleMixin, LoginRequiredMixin, DetailView):
    # model = Feedback
    template_name = 'users/feedback.html'
    title = 'Детали обращения'

    def get_object(self, queryset=None):
        fb_object = Feedback.objects.get(id=self.kwargs['pk'])
        if fb_object not in Feedback.objects.filter(from_user=self.request.user):
            fb_object.from_user = self.request.user
            fb_object.content = ''
            fb_object.answer = "You do not have permission to view this content"
        #     raise Exception  #  Надо корректно отсечь возможность просмотра чужых фидбеков !!!
        try:
            fb_object.topic = fb_topics()[fb_object.topic][1]
        except IndexError:
            fb_object.topic = fb_topics()[0][1]  # 'другая'
        try:
            fb_object.status = fb_statuses()[fb_object.status][1]
        except IndexError:
            fb_object.status = fb_statuses()[0][1]  # 'не просмотрено'
        return fb_object


class FeedbackCreateView(TitleMixin, LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Feedback
    template_name = 'users/feedback-create.html'
    form_class = UserFeedbackForm
    title = 'Обратная связь'

    def get_success_url(self):
        # return reverse_lazy('user:feedback_list', args=(self.object.from_user.id,))
        return reverse_lazy('user:feedback_list')

    def get_success_message(self, cleaned_data):
        return f'{self.object.from_user}, ваше обращение зарегистрировано'
    #     return f'Ваше обращение #{self.object.id} зарегистрировано'

    def form_valid(self, form):
        # self.object.from_user = self.request.user
        self.object = form.save(commit=False)
        self.object.from_user = self.request.user
        self.object.save()
        return super().form_valid(form)
