from django.contrib import admin

from products.admin import BasketAdmin
from users.models import EmailVerification, Feedback, User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'is_verified_email', 'is_staff', 'date_joined')
    inlines = (BasketAdmin,)
    fields = [
        ('username', 'password'),
        'is_active',
        ('last_login', 'date_joined', ),
        ('first_name', 'last_name'),
        ('image', 'email', 'is_verified_email'),
        ('is_staff', 'is_superuser'),
        'groups',
        'user_permissions'
    ]
    search_fields = ('username', 'first_name', 'last_name')


@admin.register(EmailVerification)
class EmailVerificationAdmin(admin.ModelAdmin):
    list_display = ('code', 'user', 'expiration')
    fields = ('code', 'user', 'expiration', 'created')
    readonly_fields = ('created',)


@admin.register(Feedback)
class FeedbackAdmin(admin.ModelAdmin):
    list_display = ('from_user', 'topic', 'created', 'status')
    fields = [
        ('created', 'from_user', 'topic'),
        'content',
        'answer',
        ('status', 'answered'),
    ]
    readonly_fields = ('created', 'from_user', 'topic')
    search_fields = ('from_user',)
