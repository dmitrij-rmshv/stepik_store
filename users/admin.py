from django.contrib import admin

from products.admin import BasketAdmin
from users.models import EmailVerification, User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username',)
    inlines = (BasketAdmin,)
    fields = [
        ('username', 'password'),
        'is_active',
        ('last_login', 'date_joined', ),
        ('first_name', 'last_name'),
        ('is_staff', 'is_superuser'),
        'groups',
        'user_permissions',
        'image',
        ('email', 'is_verified_email')
    ]


@admin.register(EmailVerification)
class EmailVerificationAdmin(admin.ModelAdmin):
    list_display = ('code', 'user', 'expiration')
    fields = ('code', 'user', 'expiration', 'created')
    readonly_fields = ('created',)
