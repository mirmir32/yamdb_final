from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from api_yamdb.settings import EMPTY_VALUE_DISPLAY

from .forms import CustomUserChangeForm, CustomUserCreationForm
from .models import CustomUser


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser
    list_display = (
        'pk',
        'username',
        'email',
        'bio',
        'role',
        'confirmation_code')
    search_fields = ('username',)
    list_filter = ('username',)
    empty_value_display = EMPTY_VALUE_DISPLAY
