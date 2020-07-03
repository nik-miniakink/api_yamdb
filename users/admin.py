from django.contrib import admin

from .models import CustomUser


@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'role', 'first_name', 'last_name', 'bio', 'is_superuser')
    fields = ('username', 'email', 'role', 'first_name', 'last_name', 'bio', 'is_superuser')
    search_fields = ('username', 'email', 'role')
    list_filter = ('username', 'email')
    empty_value_display = '-пусто-'
