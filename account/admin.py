from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth import admin as auth_admin

from account.forms import CustomUserForm, ChangeForm
from account.models import CustomUser


class CustomUserAdmin(UserAdmin):
    model = CustomUser
    fieldsets = (
        (None, {'fields': ('email', 'password', )}),
        ('Personal info', {'fields': ('first_name', 'last_name', )}),
        ('Address info', {'fields': ('country', 'city', 'state_county', 'zip_code', 'note', 'company_name', 'company_address', 'company_uin', )}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions', )}),
        ('Important dates', {'fields': ('last_login', 'date_joined', )}),
    )
    limited_fieldsets = (
        (None, {'fields': ('email', )}),
        ('Personal info', {'fields': ('first_name', 'last_name', )}),
        ('Important dates', {'fields': ('last_login', 'date_joined', )}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide', ),
            'fields': ('email', 'password1', 'password2', )}),
    )
    form = ChangeForm
    add_form = CustomUserForm
    change_password_form = auth_admin.AdminPasswordChangeForm
    list_display = ('email', 'first_name', 'last_name', 'is_superuser', )
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'groups', )
    search_fields = ('first_name', 'last_name', 'email', )
    ordering = ('email', )
    readonly_fields = ('last_login', 'date_joined', )


admin.site.register(CustomUser, CustomUserAdmin)
