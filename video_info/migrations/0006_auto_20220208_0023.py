# Generated by Django 3.2.9 on 2022-02-07 16:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('video_info', '0005_auto_20220208_0008'),
    ]

    operations = [
        migrations.AlterField(
            model_name='videoinfo',
            name='created',
            field=models.DateTimeField(null=True),
        ),
        migrations.AlterField(
            model_name='videoinfo',
            name='duration',
            field=models.BigIntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='videoinfo',
            name='size',
            field=models.FloatField(blank=True, default=0),
        ),
        migrations.AlterField(
            model_name='videoinfo',
            name='title',
            field=models.CharField(default='20220208_002309', max_length=100, unique=True),
        ),
    ]
