from django.contrib import admin
from .models import *
# Register your models here.


@admin.register(UserDetails)
class UserDetailsAdmin(admin.ModelAdmin):
    list_display = ('username', 'created_at', 'last_updated')