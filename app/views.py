from contextlib import redirect_stderr
from random import random
from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from .models import *
from django.forms.models import model_to_dict
from django.db.models import Q
import datetime as dt
from datetime import datetime



def createmusictheme(request):
    if request.method == 'POST':
        musicthemename = request.POST.get('musicthemename')
        musicthemeimage = request.POST.get('themeimage')
        savethemename = MusicTheme(theme_name = musicthemename ,theme_image = musicthemeimage )
        savethemename.save()
        themenamelist = MusicTheme.objects.all()
        context = {
            'themenamelist':themenamelist
            }
        return render(request, 'app/createmusicthemeok.html', context)
    else:
        return render(request, 'app/createmusictheme.html')
def createmusic(request):
    if request.method == 'POST':
        musicname = request.POST.get('musicname')
        musicartist = request.POST.get('musicartist')
        musicimage = request.POST.get('musicimage')
        musicmp3 = request.POST.get('musicmp3')
        music_theme = request.POST.get('music_theme')

        mt = MusicTheme.objects.get(id =music_theme)

        savemusicinfo = MusicList(
            name = musicname,
            artist = musicartist,
            image_name = musicimage,
            mp3_name = musicmp3,
            music_theme = mt
        )
        savemusicinfo.save()
        musiclist = MusicList.objects.all()
        context = {
            'musiclist':musiclist
            }
        return render(request, 'app/createmusicok.html', context)
    else:
        music_theme = MusicTheme.objects.all()
        return render(request, 'app/createmusic.html', {'music_theme':music_theme})

def newalarm(request):
    musictheme = MusicTheme.objects.all()
    return render(request, 'app/new.html', {'musictheme':musictheme})

def findmusic(request):

    musictheme = request.GET.get('musictheme')
    findmusictheme = MusicTheme.objects.get(theme_name__contains = musictheme)
    findmusiclist = findmusictheme.musiclist_set.all()
    list = []
    # i = model_to_dict(findmusiclist)
    for i in findmusiclist:
        i = model_to_dict(i)
        list.append(i)
    return JsonResponse(list, safe=False)
    # return HttpResponse(findmusiclist[0].name)
    
def home(request):
    if request.method == 'POST':
        time = request.POST.get('inputtime')#시간 출력형태 ex)4시
        minute = request.POST.get('inputminute')#분 출력형태 ex)15분
        ampm = request.POST.get('inputampm')#오전/오후
        week = request.POST.get('week')#이번주/다음주/다다음주
        musictheme = request.POST.get('selectedmusictheme')#스와이퍼에 나타나는 음악장르
        music = request.POST.get('selectedmusic')#스와이퍼 음악(가수명/음악명)
        artist=music.split('/')[0]#DB상가수명
        musicname=music.split('/')[1]#DB상음악명
        caption = request.POST.get('caption')#캡션(텍스트)
        day = request.POST.getlist('day')#['월/0','화/1' ...]
        daykolist  =[]#한국어 요일이 들어가는 리스트
        daynumlist = []#숫자요일이 들어가는 리스트
        #포스트로 얻어온 정보와 일치하는 뮤직테마 아이디
        musictheme_id = MusicTheme.objects.get(theme_name__contains=musictheme)
        music_id = musictheme_id.musiclist_set.all()#그 음악장르에 해당하는 모든 곡 쿼리셋     
        list =[]#음악장르속 많은곡들중에 받아온 음악/가수정보와 일치하는 단 하나의 곡이 들어갈 리스트
        for i in music_id:
            if i.artist == artist and i.name == musicname:#음악이름과 아티스트를 필터링하는 과정
                list.append(i)
            else:
                pass
        savemusicinfo = list[0]#저장될 음악의 테이블 행 정보
        saveartist = savemusicinfo.artist#저장될 음악의 아티스트 명
        savename = savemusicinfo.name#저장될 음악의 이름
        #포스트로 가져온 정보들로 알람리스트 새 행 작성 과정
        if ampm =='오전':
            hour = int(time[:-1])
        else:
            hour = int(time[:-1]) + 12
        saveAlarmList = AlarmList(caption = caption, music_id = list[0].id,
         hour = hour, minute=minute[:-1])
        saveAlarmList.save()
        

        for i in day:
            daykolist.append(i.split('/')[0])
            daynumlist.append(i.split('/')[1])
        settingdatelist = []
        for i in daynumlist:
                if week=='이번주':
                    now = dt.datetime.now()
                    nowday = now.weekday()
                    x = int(i)-int(nowday)
                    settingdate = now+dt.timedelta(days=x)
                    settingdate = settingdate.strftime("%Y-%m-%d")
                    settingdatelist.append(settingdate)
                elif week=='다음주':
                    now = dt.datetime.now()
                    nowday = now.weekday()
                    x = int(i)-int(nowday)+7
                    settingdate = now+dt.timedelta(days=x)
                    settingdate = settingdate.strftime("%Y-%m-%d")
                    settingdatelist.append(settingdate)
                else:
                    now = dt.datetime.now()
                    nowday = now.weekday()
                    x = int(i)-int(nowday)+14
                    settingdate = now+dt.timedelta(days=x)
                    settingdate = settingdate.strftime("%Y-%m-%d")
                    settingdatelist.append(settingdate)
        for i in settingdatelist:
            savedaylist = DayList(alarm = saveAlarmList, date = i)
            savedaylist.save()

        
    
        setalarmlist = AlarmList.objects.all()
        list1 = []
        count = 0
        for i in setalarmlist:
            if int(i.hour)<12:
                selectampm = '오전'
                hour = i.hour
            else:
                hour= int(i.hour)-12
                selectampm = '오후'
            if int(i.minute)<10:
                minute = '0'+str(i.minute)
            else:
                minute = i.minute
            dayiters = i.daylist_set.all()
            dayinfo =''
            days2 = ['월요일', '화요일', '수요일', '목요일', '금요일', '토요일', '일요일']
            for x in dayiters:
                h=x.date
                g=h.split('-')
                qwe = dt.datetime(int(g[0]),int(g[1]),int(g[2])).weekday()
                weekdays = days2[qwe]
                dayinfo = dayinfo+weekdays

            xday = dayiters[0].date
            today = dt.datetime.now().weekday()
            delta = 6-int(today)
            thissunday = dt.datetime.now() + dt.timedelta(days = delta)
            xday = datetime.strptime(xday, "%Y-%m-%d")
            minus = xday - thissunday
            minus = minus.days
            if minus <1:
                week ='이번주'
            elif minus > 0 and minus <8:
                week ='다음주'
            else:
                week = '다다음주'
            dic ={}
            id = i.id
            caption = i.caption
            mname = i.music.name
            martist = i.music.artist
            dic['id'] = id
            dic['hour']=hour
            dic['minute']=minute
            dic['mname']=mname
            dic['martist']=martist
            dic['caption']=caption
            dic['ampm']=selectampm
            dic['dayinfo']=dayinfo
            dic['week']=week
            list1.append(dic)
        context = {
            'alarmlist':setalarmlist,
            'mnamelist':list1
        }
        return redirect('/app/home/')
    else:
        setalarmlist = AlarmList.objects.all()
        list1 = []
        for i in setalarmlist:
            if int(i.hour)<12:
                selectampm = '오전'
                hour = i.hour
            else:
                hour= int(i.hour)-12
                selectampm = '오후'
            if int(i.minute)<10:
                minute = '0'+str(i.minute)
            else:
                minute = i.minute
            dayiters = i.daylist_set.all()
            dayinfo =''
            days2 = ['월요일', '화요일', '수요일', '목요일', '금요일', '토요일', '일요일']
            for x in dayiters:
                h=x.date
                g=h.split('-')
                qwe = dt.datetime(int(g[0]),int(g[1]),int(g[2])).weekday()
                weekdays = days2[qwe]
                dayinfo = dayinfo+weekdays

            xday = dayiters[0].date
            today = dt.datetime.now().weekday()
            delta = 6-int(today)
            thissunday = dt.datetime.now() + dt.timedelta(days = delta)
            xday = datetime.strptime(xday, "%Y-%m-%d")
            minus = xday - thissunday
            minus = minus.days
            if minus <1:
                week ='이번주'
            elif minus > 0 and minus <8:
                week ='다음주'
            else:
                week = '다다음주'
            
            id = i.id
            caption = i.caption
            mname = i.music.name
            martist = i.music.artist
            dic ={}
            dic['id'] = id
            dic['hour']=hour
            dic['minute']=minute
            dic['mname']=mname
            dic['martist']=martist
            dic['caption']=caption
            dic['ampm']=selectampm
            dic['dayinfo']=dayinfo
            dic['week']=week
            list1.append(dic)
        context = {
            'alarmlist':setalarmlist,
            'mnamelist':list1
        }
        return render(request, 'app/home.html', context)
def deleterecord(request):
    deleterecordid = request.GET.get('deleteid')
    alarmrecord = AlarmList.objects.get(id = deleterecordid)
    alarmrecord.delete()
    return HttpResponse('삭제완료')
def deleteall(request):
    alarmrecord = AlarmList.objects.all()
    alarmrecord.delete()
    return HttpResponse('삭제완료')



# Create your views here.
