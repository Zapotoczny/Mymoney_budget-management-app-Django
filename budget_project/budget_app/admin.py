from django.contrib import admin
from .models import ExpenseInfo, Event

# Register your models here.

admin.site.register(ExpenseInfo)
admin.site.register(Event)