from ast import Delete
from django.db import models
from pkg_resources import safe_extra


# # Create your models here.

class MusicTheme(models.Model):
    theme_name = models.CharField(max_length =100)
    theme_image = models.CharField(max_length =100)
    class Meta:
        db_table ='musictheme'

class MusicList(models.Model):
    name = models.CharField(max_length = 100)
    artist = models.CharField(max_length = 100)
    image_name = models.CharField(max_length =100,null =True)
    mp3_name = models.CharField(max_length = 100, null =True)
    music_theme = models.ForeignKey(MusicTheme, on_delete = models.SET_NULL, null = True)
    class Meta:
        db_table ='musiclist'

class AlarmList(models.Model):
    
    caption = models.CharField(max_length = 5000)
    music = models.ForeignKey(MusicList, on_delete = models.SET_NULL, null = True)
    hour = models.CharField(max_length = 100)
    minute = models.CharField(max_length = 100)
    class Meta:
        db_table = 'alarmlist'


class DayList(models.Model):
    date = models.CharField(max_length=100)
    alarm =models.ForeignKey(AlarmList, on_delete = models.SET_NULL, null = True)
    class Meta:
        db_table ='daylist'


