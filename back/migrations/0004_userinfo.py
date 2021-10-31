# Generated by Django 3.2.8 on 2021-10-31 17:00

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('back', '0003_auto_20211029_1801'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserInfo',
            fields=[
                ('id', models.CharField(max_length=200, primary_key=True, serialize=False)),
                ('team_id', models.IntegerField()),
                ('name', models.CharField(default='Guest', max_length=200)),
                ('site_id', models.IntegerField()),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='info', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]