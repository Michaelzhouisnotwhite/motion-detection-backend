# Generated by Django 3.2.9 on 2022-02-07 15:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('video_info', '0002_auto_20220207_2323'),
    ]

    operations = [
        migrations.AlterField(
            model_name='videoinfo',
            name='title',
            field=models.CharField(max_length=100, unique=True),
        ),
    ]