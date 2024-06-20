from django.contrib import admin
from . models import Task, Label
from rest_framework.authtoken.admin import TokenAdmin
from rest_framework.authtoken.models import Token

# Register your models here.
admin.site.register(Task)
admin.site.register(Label)
admin.site.register(Token, TokenAdmin)
