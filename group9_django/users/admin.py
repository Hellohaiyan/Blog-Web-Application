from django.contrib import admin

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User

from .models import UserBio, UserAvatar

class UserBioInline(admin.StackedInline):
    model = UserBio
    can_delete = False
    verbose_name_plural = 'Bio'

class UserAvatarInline(admin.StackedInline):
    model = UserAvatar
    can_delete = False
    verbose_name_plural = 'Avatar'

class UserAdmin(BaseUserAdmin):
    inlines = (UserBioInline, UserAvatarInline)

admin.site.unregister(User)
admin.site.register(User, UserAdmin)

