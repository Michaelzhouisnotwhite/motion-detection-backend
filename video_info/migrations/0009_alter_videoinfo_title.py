# Generated by Django 3.2.9 on 2022-02-08 11:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('video_info', '0008_alter_videoinfo_title'),
    ]

    operations = [
        migrations.AlterField(
            model_name='videoinfo',
            name='title',
            field=models.CharField(default='20220208_192203', max_length=100, unique=True),
        ),
    ]