# Generated by Django 4.1 on 2022-10-17 01:06

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("app", "0009_alarmlist_specialnum"),
    ]

    operations = [
        migrations.RemoveField(model_name="musiclist", name="music_theme",),
        migrations.RemoveField(model_name="timelist", name="alarm",),
        migrations.DeleteModel(name="AlarmList",),
        migrations.DeleteModel(name="MusicList",),
        migrations.DeleteModel(name="MusicTheme",),
        migrations.DeleteModel(name="TimeList",),
    ]
