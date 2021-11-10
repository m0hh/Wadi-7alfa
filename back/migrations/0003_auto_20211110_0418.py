# Generated by Django 3.2.8 on 2021-11-10 04:18

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('back', '0002_auto_20211109_1806'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='timetaskhistory',
            name='after',
        ),
        migrations.RemoveField(
            model_name='timetaskhistory',
            name='before',
        ),
        migrations.RemoveField(
            model_name='timetaskhistory',
            name='date',
        ),
        migrations.RemoveField(
            model_name='timetaskhistory',
            name='field',
        ),
        migrations.AddField(
            model_name='timetaskhistory',
            name='ended',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='timetaskhistory',
            name='started',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='timetaskhistory',
            name='time',
            field=models.CharField(blank=True, max_length=300, null=True),
        ),
        migrations.AlterField(
            model_name='timetaskhistory',
            name='id',
            field=models.CharField(max_length=400, primary_key=True, serialize=False),
        ),
        migrations.CreateModel(
            name='Space',
            fields=[
                ('id', models.CharField(max_length=400, primary_key=True, serialize=False)),
                ('name', models.CharField(blank=True, max_length=300, null=True)),
                ('private', models.BooleanField()),
                ('creator', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='spaces', to='back.userinfo')),
            ],
        ),
        migrations.CreateModel(
            name='List',
            fields=[
                ('id', models.CharField(max_length=300, primary_key=True, serialize=False)),
                ('name', models.CharField(blank=True, max_length=200, null=True)),
                ('space', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='lists', to='back.space')),
            ],
        ),
        migrations.AddField(
            model_name='task',
            name='list',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='tasks', to='back.list'),
        ),
    ]
