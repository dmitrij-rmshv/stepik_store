from datetime import datetime

from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.core.mail import send_mail
from django.db import models
from django.urls import reverse

from users.utilities import fb_statuses, fb_topics


class User(AbstractUser):
    image = models.ImageField(upload_to='users_images', null=True, blank=True)
    is_verified_email = models.BooleanField(verbose_name='акт-ван?', default=False)
    email = models.EmailField(unique=True, blank=True)

    def __str__(self):
        return ' '.join((self.first_name, self.last_name))


class EmailVerification(models.Model):
    code = models.UUIDField(unique=True)
    user = models.ForeignKey(to=User, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    expiration = models.DateTimeField()

    class Meta:
        verbose_name = 'Подтверждение регистрации'
        verbose_name_plural = 'Подтверждения регистрации'

    def __str__(self):
        return f'EmailVerification object for {self.user.email}'

    def send_verification_email(self):
        link = reverse('user:email_verification', kwargs={
            'email': self.user.email,
            'code': self.code
        })
        verification_link = f'{settings.DOMAIN_NAME}{link}'
        subject = f'Подтверждение учетной записи для {self.user.username}'
        message = 'Для подтверждения учетной записи для {} перейдите по ссылке {}'
        message = message.format(self.user.email, verification_link)
        send_mail(
            subject=subject,
            message=message,
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[self.user.email, ],
            fail_silently=False,
        )


class Feedback(models.Model):

    # class Status(models.IntegerChoices):
    #     UNWATCHED = 0, 'не просмотрено'
    #     VIEWED = 1, 'просмотрено'
    #     REJECTED = 2, 'отклонено'
    #     ON_THE_GO = 3, 'в работе'
    #     DONE = 4, 'отработано'

    from_user = models.ForeignKey(verbose_name='обращающийся', to=User, on_delete=models.CASCADE)
    # topic = models.SmallIntegerField(verbose_name='тема', choices=fb_topics(), default=fb_topics()[3])
    topic = models.SmallIntegerField(verbose_name='тема', choices=fb_topics())
    content = models.TextField(verbose_name='содержание')
    created = models.DateTimeField(verbose_name='создано', auto_now_add=True)
    status = models.SmallIntegerField(verbose_name='статус', choices=fb_statuses(), default=fb_statuses()[0][0])
    answer = models.TextField(verbose_name='ответ')
    answered = models.DateTimeField(verbose_name='реализовано', null=True, blank=True)

    class Meta:
        verbose_name = 'Обращение'
        verbose_name_plural = 'Обращения'
        ordering = ('-id',)

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        # if not hasattr(self, 'from_user'):
        #     self.from_user = self.request.user
        if self.answer and not self.answered:
            self.answered = datetime.now()
        super().save(force_insert=False, force_update=False, using=None, update_fields=None)

    def __str__(self):
        try:
            reason = list(filter(lambda x: x[0] == self.topic, fb_topics()))[0][1]
        except IndexError:
            reason = 'вне темы'
        return f'{reason} от {self.from_user.username}'
