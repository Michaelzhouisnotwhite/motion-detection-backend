# Generated by Django 3.2.9 on 2022-02-07 16:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('video_info', '0004_alter_videoinfo_title'),
    ]

    operations = [
        migrations.AlterField(
            model_name='videoinfo',
            name='duration',
            field=models.TimeField(blank=True, default='0'),
        ),
        migrations.AlterField(
            model_name='videoinfo',
            name='title',
            field=models.CharField(default='20220208_000852', max_length=100, unique=True),
        ),
    ]