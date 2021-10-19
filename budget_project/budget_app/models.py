from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

# Create your models here.


class ExpenseInfo(models.Model):
    username = models.CharField(max_length=255, default='NoName')
    expense_name = models.CharField(max_length=20)
    category = models.CharField(max_length=20)
    cost = models.FloatField()
    budget_id = models.CharField(default='0123456789', max_length=10)
    date_added = models.DateField()
    user_expense = models.CharField(max_length=20)


class Event(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
