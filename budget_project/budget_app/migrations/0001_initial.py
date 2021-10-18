# Generated by Django 3.2.7 on 2021-09-21 15:19

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='ExpenseInfo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(default='NoName', max_length=255)),
                ('expense_name', models.CharField(max_length=20)),
                ('cost', models.FloatField()),
                ('budget_id', models.CharField(default='0123456789', max_length=10)),
                ('date_added', models.DateField()),
                ('user_expense', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
