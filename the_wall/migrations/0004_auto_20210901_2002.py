# Generated by Django 3.2.5 on 2021-09-02 00:02

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('the_wall', '0003_auto_20210901_1957'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comments',
            name='post',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='the_wall.posts'),
        ),
        migrations.AlterField(
            model_name='comments',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='the_wall.users'),
        ),
    ]
