# Generated by Django 2.2 on 2020-09-21 00:05

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('habits', '0012_auto_20200819_2113'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='commentlike',
            options={'ordering': ['timestamp']},
        ),
        migrations.AlterModelOptions(
            name='postcomment',
            options={'ordering': ['timestamp']},
        ),
        migrations.AlterModelOptions(
            name='postlike',
            options={'ordering': ['timestamp']},
        ),
        migrations.AlterField(
            model_name='commentlike',
            name='comment',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comment_likes', to='habits.PostComment'),
        ),
        migrations.AlterField(
            model_name='postcomment',
            name='parent',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='replies', to='habits.PostComment'),
        ),
        migrations.AlterField(
            model_name='postcomment',
            name='post',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='habits.HabitPost'),
        ),
        migrations.AlterField(
            model_name='postlike',
            name='post',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='post_likes', to='habits.HabitPost'),
        ),
    ]
