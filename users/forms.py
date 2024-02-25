from django import forms
from django.contrib.auth.forms import (AuthenticationForm, UserChangeForm,
                                       UserCreationForm)

from users.models import Feedback, User
from users.tasks import send_email_verification
from users.utilities import fb_topics


class UserLoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={
        'class': "form-control py-4", 'placeholder': "Введите имя пользователя"}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': "form-control py-4", 'placeholder': "Введите пароль"}))

    class Meta:
        model = User
        fields = ('username', 'password')


class UserRegistrationForm(UserCreationForm):
    first_name = forms.CharField(widget=forms.TextInput(attrs={
        'class': "form-control py-4", 'placeholder': "Введите имя"}))
    last_name = forms.CharField(widget=forms.TextInput(attrs={
        'class': "form-control py-4", 'placeholder': "Введите фамилию"}))
    username = forms.CharField(widget=forms.TextInput(attrs={
        'class': "form-control py-4", 'placeholder': "Введите имя пользователя", 'aria-describedby': "usernameHelp"}))
    email = forms.CharField(widget=forms.EmailInput(attrs={
        'class': "form-control py-4", 'placeholder': "Введите адрес эл. почты", 'aria-describedby': "emailHelp"}))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': "form-control py-4", 'placeholder': "Введите пароль"}))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': "form-control py-4", 'placeholder': "Подтверждение пароля"}))

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'image', 'username', 'email')

    def save(self, commit=True):
        user = super().save(commit=True)
        send_email_verification.delay(user.id)
        return user


class UserProfileForm(UserChangeForm):

    first_name = forms.CharField(widget=forms.TextInput(attrs={'class': "form-control py-4"}))
    last_name = forms.CharField(widget=forms.TextInput(attrs={'class': "form-control py-4"}))
    image = forms.ImageField(widget=forms.FileInput(attrs={'class': "custom-file-input"}), required=False)
    username = forms.CharField(widget=forms.TextInput(attrs={
        'class': "form-control py-4", 'aria-describedby': "usernameHelp", 'readonly': True}))
    email = forms.CharField(widget=forms.EmailInput(attrs={
        'class': "form-control py-4", 'aria-describedby': "emailHelp", 'readonly': True}))

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'image', 'username', 'email')


class UserFeedbackForm(forms.ModelForm):

    topic = forms.ChoiceField(
        widget=forms.widgets.Select(attrs={'size': 1, 'class': "form-control py-4"}),
        choices=fb_topics(), required=False, initial=fb_topics()[3]
    )
    content = forms.CharField(
        widget=forms.widgets.Textarea(attrs={'class': "form-control py-4", 'placeholder': "Изложите суть обращения"})
    )

    class Meta:
        model = Feedback
        fields = ('topic', 'content')
