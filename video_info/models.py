from django.utils import timezone
from django.db import models

def get_default_title():
    now_time = timezone.localtime(timezone.now())
    return now_time.strftime("%Y%m%d_%H%M%S")


# Create your models here.
class VideoInfo(models.Model):
    title = models.CharField(max_length=100, unique=True, default=get_default_title(),blank=False, null=False)
    # 单位：MB
    size = models.FloatField(blank=True, default=0)
    duration = models.BigIntegerField(default=0)
    
    created = models.DateTimeField(null=True)
    falling = models.BooleanField(default=False)
    file_path = models.CharField(max_length=2048, null=True)
    
    class Meta:
        db_table='video_info'