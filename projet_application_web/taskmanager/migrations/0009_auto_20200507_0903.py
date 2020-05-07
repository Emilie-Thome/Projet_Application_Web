# Generated by Django 2.2.12 on 2020-05-07 09:03

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('taskmanager', '0008_auto_20200503_2205'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='journal',
            options={'ordering': ['date'], 'verbose_name': 'journal'},
        ),
        migrations.AlterModelOptions(
            name='project',
            options={'ordering': ['name'], 'verbose_name': 'project'},
        ),
        migrations.AlterModelOptions(
            name='status',
            options={'verbose_name': 'status'},
        ),
        migrations.AlterModelOptions(
            name='task',
            options={'ordering': ['priority', 'status', 'due_date'], 'verbose_name': 'task'},
        ),
        migrations.AlterField(
            model_name='journal',
            name='author',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Journal author'),
        ),
        migrations.AlterField(
            model_name='journal',
            name='date',
            field=models.DateTimeField(default=django.utils.timezone.now, verbose_name='Post date'),
        ),
        migrations.AlterField(
            model_name='journal',
            name='entry',
            field=models.CharField(max_length=200, verbose_name='Journal entry'),
        ),
        migrations.AlterField(
            model_name='journal',
            name='task',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='taskmanager.Task', verbose_name='Journal task'),
        ),
        migrations.AlterField(
            model_name='project',
            name='members',
            field=models.ManyToManyField(to=settings.AUTH_USER_MODEL, verbose_name='Project members'),
        ),
        migrations.AlterField(
            model_name='project',
            name='name',
            field=models.CharField(max_length=80, verbose_name='Project name'),
        ),
        migrations.AlterField(
            model_name='status',
            name='name',
            field=models.CharField(max_length=30, verbose_name='Status name'),
        ),
        migrations.AlterField(
            model_name='task',
            name='assignee',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Task assignee'),
        ),
        migrations.AlterField(
            model_name='task',
            name='description',
            field=models.TextField(max_length=200, verbose_name='Task description'),
        ),
        migrations.AlterField(
            model_name='task',
            name='due_date',
            field=models.DateField(verbose_name='Task due date'),
        ),
        migrations.AlterField(
            model_name='task',
            name='name',
            field=models.CharField(max_length=80, verbose_name='Task name'),
        ),
        migrations.AlterField(
            model_name='task',
            name='project',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='taskmanager.Project', verbose_name='Task project'),
        ),
        migrations.AlterField(
            model_name='task',
            name='start_date',
            field=models.DateField(verbose_name='Task start date'),
        ),
        migrations.AlterField(
            model_name='task',
            name='status',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='taskmanager.Status', verbose_name='Task status'),
        ),
    ]