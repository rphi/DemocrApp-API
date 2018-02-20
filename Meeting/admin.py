from django.contrib import admin
from .models import *


admin.site.register(Meeting)


class AuthTokenAdmin(admin.ModelAdmin):
    fields = ['proxy', 'token_set']
admin.site.register(AuthToken,AuthTokenAdmin)