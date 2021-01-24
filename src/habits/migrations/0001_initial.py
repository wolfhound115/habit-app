# Generated by Django 2.2 on 2020-06-10 01:57

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import recurrence.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='HabitModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user', models.ForeignKey(default=1, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='HabitTrack',
            fields=[
                ('habitmodel_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='habits.HabitModel')),
                ('track_name', models.CharField(max_length=100)),
                ('description', models.CharField(max_length=2200)),
                ('cover_image', models.ImageField(blank=True, null=True, upload_to='image/')),
                ('recurrences', recurrence.fields.RecurrenceField(null=True)),
                ('start_date', models.DateTimeField(blank=True, null=True)),
            ],
            bases=('habits.habitmodel',),
        ),
        migrations.CreateModel(
            name='HabitPost',
            fields=[
                ('habitmodel_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='habits.HabitModel')),
                ('slug', models.SlugField(unique=True)),
                ('description', models.CharField(max_length=2200)),
                ('image', models.ImageField(blank=True, null=True, upload_to='image/')),
                ('publish_date', models.DateTimeField(blank=True, null=True)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('track', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='habits.HabitTrack')),
            ],
            options={
                'ordering': ['-publish_date', '-timestamp'],
            },
            bases=('habits.habitmodel',),
        ),
        migrations.CreateModel(
            name='HabitEvent',
            fields=[
                ('habitmodel_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='habits.HabitModel')),
                ('date', models.DateTimeField(null=True)),
                ('post', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='habits.HabitPost')),
                ('track', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='habits.HabitTrack')),
            ],
            bases=('habits.habitmodel',),
        ),
    ]
