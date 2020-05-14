# Generated by Django 2.1.15 on 2020-05-11 06:52

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('taskmanager', '0009_auto_20200507_0903'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='task',
            options={'ordering': ['priority', 'status', 'due_date', 'modified'], 'verbose_name': 'task'},
        ),
        migrations.AddField(
            model_name='task',
            name='modified',
            field=models.DateTimeField(default=django.utils.timezone.now, verbose_name='Modified date'),
        ),
    ]
