# Generated by Django 4.1 on 2022-10-13 00:30

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("app", "0002_alter_musiclist_image_name_alter_musiclist_mp3_name"),
    ]

    operations = [
        migrations.DeleteModel(name="AlarmList",),
        migrations.DeleteModel(name="MusicList",),
        migrations.DeleteModel(name="MusicTheme",),
        migrations.DeleteModel(name="TimeList",),
    ]