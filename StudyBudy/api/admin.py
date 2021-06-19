from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import *
# Register your models here.


class AccountAdmin(UserAdmin):
    list_display = ('username', 'date_joined', 'last_login',
                    'is_admin', 'is_staff', 'phone_number', 'usn')
    search_fields = ('email', 'username', 'usn')
    readonly_fields = ('date_joined', 'last_login')


admin.site.register(User, AccountAdmin)
