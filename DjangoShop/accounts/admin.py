from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User
from django.contrib.auth.models import Group


class CustomUserAdmin(UserAdmin):
    model = User
    list_display = ('username', 'email', 'phone_number')
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('phone_number', )}),
    )

    add_fieldsets = UserAdmin.add_fieldsets + (
        (None, {'fields': ('email', 'phone_number', )}),
    )


admin.site.register(User, CustomUserAdmin)
admin.site.unregister(Group)

