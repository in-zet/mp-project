# -*- coding: utf-8 -*-
import os
import glob
from tkinter import *
import mutagen
from mutagen.easyid3 import EasyID3
from mutagen.id3 import ID3, TIT2
from mutagen.mp4 import MP4Tags
from mutagen._file import *
import codecs
from pytube import YouTube
from moviepy.editor import *

#from downloads import *
#from porters import *
#from settings import *
#from lists import *

# ----------
# 21.x.x /v0.1/ : 프로젝트 폐기 - 작동불능
# 21.8.13 /v0.11/ : 프로젝트 재가동중 - 정상작동 확인
# 21.10.22 /v0.2/ : youtube-dll 의 속도저하 문제 해결 위한 pytube 모듈 도입
# 21.11.22 /v0.21/ : Github에 업로드
# 21.12.04 /v0.22/ : 코드 최적화, mp4 폴더 분리, 변수 이름 변경, eyed3 사용 중지 및 제거
# ----------
# D:\python coding\ffmpeg-N-101711-ga4e518c321-win64-gpl\bin\song database.py
# ^ 베타 버전(구)
# ----------
# 중요 : python 파일이 있는 곳에 ffmpeg.exe 와 ffprobe.exe가 있어야지만 정상작동
# ----------

# =================================================다운로드==================================================
# =================================================다운로드==================================================
# =================================================다운로드==================================================

def downloading():
    global url_list
    global name_list
    global artist_list
    global album_list
    global settings_dict
    global e5


    def download_mp4():  # mp4 download from youtube
        yt = YouTube(url_list[i])
        yt.streams.filter(progressive=True, file_extension='mp4').order_by(
            'resolution').desc().first().download(None, settings_dict['path'] + "/min/mp4/%s.mp4" % name_list[i])


    def transfer_mp3():  # transfer mp4 to mp3
        vv = VideoFileClip(os.path.join(settings_dict['path'] + "/min/mp4",
            settings_dict['path'] + "/min/mp4/%s.mp4" % name_list[i]))
        vv.audio.write_audiofile(os.path.join(settings_dict['path'] + "/min/mp3",
            settings_dict['path'] + "/min/mp3/%s.mp3" % name_list[i]))


    def delete_mp4(name):
        os.remove(settings_dict['path'] + "/min/mp4/%s.mp4" % name)


    mp3_list = os.listdir(settings_dict['path'] + '/min/mp3')
    mp4_list = os.listdir(settings_dict['path'] + '/min/mp4')
    lyrics_list = os.listdir(settings_dict['path'] + '/min/lyrics')
    if_again_mp3 = 0
    if_again_mp4 = 0
    if_again_lyric = 0

    try:
        for i in range(len(name_list)):

            for j in range(len(lyrics_list)):
                if name_list[i] == f'{lyrics_list[j][:-4]}':  # 중복가사파일확인
                    if_again_lyric = 1

            for j in range(len(mp3_list)):
                if name_list[i] == f'{mp3_list[j][:-4]}':  # 중복음악파일확인
                    if_again_mp3 = 1

            for j in range(len(mp4_list)):
                if name_list[i] == f'{mp4_list[j][:-4]}':  # 중복영상파일확인
                    if_again_mp4 = 1

            if settings_dict['iscreatelyric'] == 1:  # 가사파일생성
                if if_again_lyric == 0:
                    _ = open(settings_dict['path'] + "/min/lyrics/%s.txt" % name_list[i], 'w')
                elif if_again_lyric == 1:
                    if_again_lyric = 0
                    print("%s lyric file skipped\n" % name_list[i])

            if settings_dict['ismp4'] == 1 or settings_dict['ismp3'] == 1:

                if if_again_mp4 == 0:  # mp4 not exist
                    print("\n" + name_list[i] + "\n%s\n" % url_list[i])  # checking in console

                    download_mp4()

                elif if_again_mp4 == 1:  # mp4 exist
                    if_again_mp4 = 0
                    print("%s mp4 file skipped\n" % name_list[i])

                if settings_dict['ismp3'] == 1:
                    if if_again_mp3 == 0:  # mp3 not exist

                        transfer_mp3()

                    elif if_again_mp3 == 1:  # mp3 exist
                        if_again_mp3 = 0
                        print("%s mp3 file skipped\n" % name_list[i])

                if settings_dict['ismp3'] == 1:

                    delete_mp4(name_list[i])

            e5.delete(0, len(e5.get()))
            e5.insert(0, ' NOW downloding...')

        e5.delete(0, len(e5.get()))
        e5.insert(0, 'downloded')
        print("\nFIN\n")

    except Exception as e:
        e5.delete(0, len(e5.get()))
        e5.insert(0, 'error: ' + str(e))


def mp4_all_delete():
    global name_list
    global settings_dict
    global e5

    try:
        for i in range(len(name_list)):
            os.remove(settings_dict['path'] + "/min/mp4/%s.mp4" % name_list[i])
        e5.delete(0, len(e5.get()))
        e5.insert(0, 'MP4 file deleted')
    except Exception as e:
        e5.delete(0, len(e5.get()))
        e5.insert(0, 'error: ' + str(e))

# =================================================태그=================================================
# =================================================태그=================================================
# =================================================태그=================================================

def tagging():
    global name_list
    global artist_list
    global album_list
    global setting_dict
    global e5

    try:
        for i in range(len(name_list)):
            try:
                tag1 = EasyID3(settings_dict['path'] + "/min/mp3/%s.mp3" % name_list[i])
            except mutagen.id3.ID3NoHeaderError:  # an MP4 tag already exists
                tag1 = mutagen.File(settings_dict['path'] + "/min/mp3/%s.mp3" % name_list[i], easy=True)
                tag1.add_tags()
            if artist_list[i] != None:
                tag1['artist'] = str(artist_list[i])
            if album_list[i] != None:
                tag1['album'] = str(album_list[i])
            tag1.save(settings_dict['path'] + "/min/mp3/%s.mp3" % name_list[i], v1=1)
            tag1.save(settings_dict['path'] + "/min/mp3/%s.mp3" % name_list[i], v1=2)

        e5.delete(0, len(e5.get()))
        e5.insert(0, 'tagging completed')

    except Exception as e:
        e5.delete(0, len(e5.get()))
        e5.insert(0, 'error: ' + str(e))


def lyric_tagging():
    global setting_dict
    global e5

    mp3_list = os.listdir(settings_dict['path'] + '/min/mp3')
    lyrics_list = os.listdir(settings_dict['path'] + '/min/lyrics')
    rightnum = 0

    if len(mp3_list) <= len(lyrics_list):
        for i in range(len(mp3_list)):
            for j in range(len(lyrics_list)):
                if f'{mp3_list[i][:-4]}' == f'{lyrics_list[j][:-4]}':
                    rightnum = j
            tag1 = EasyID3(settings_dict['path'] + '/min/mp3/' + mp3_list[i])
            ln1 = open(settings_dict['path'] + '/min/lyrics/' + lyrics_list[rightnum], 'r')
            lyr1 = ln1.read()
            ln1.close()
            tag1['lyricist'] = str(lyr1)
            tag1.save(settings_dict['path'] + '/min/mp3/' + mp3_list[i], v1=2)

            e5.delete(0, len(e5.get()))
            e5.insert(0, 'lyric completed')

    else:
        e5.delete(0, len(e5.get()))
        e5.insert(0, 'the number of mp3s and lyrics are not same')

# =================================================불러오기//내보내기=================================================
# =================================================불러오기//내보내기=================================================
# =================================================불러오기//내보내기=================================================


def in_txt():
    global url_list
    global name_list
    global artist_list
    global album_list
    global settings_dict
    global e5

    url_list = []
    name_list = []
    artist_list = []
    album_list = []
    loading = codecs.open('%s/min/save/_save_url.txt' % settings_dict['path'], 'rb', 'utf-8')
    url_list = loading.read().replace('\r', '').split('\n')
    loading.close()
    loading = codecs.open('%s/min/save/_save_name.txt' % settings_dict['path'], 'rb', 'utf-8')
    name_list = loading.read().replace('\r', '').split('\n')
    loading.close()
    loading = codecs.open('%s/min/save/_save_artist.txt' % settings_dict['path'], 'rb', 'utf-8')
    artist_list = loading.read().replace('\r', '').split('\n')
    loading.close()
    loading = codecs.open('%s/min/save/_save_album.txt' % settings_dict['path'], 'rb', 'utf-8')
    album_list = loading.read().replace('\r', '').split('\n')
    loading.close()
    if len(url_list) != len(name_list) or len(name_list) != len(artist_list) or len(artist_list) != len(
            album_list) or len(url_list) != len(album_list):
        e5.delete(0, len(e5.get()))
        e5.insert(0, 'error : different lines')
        url_list = []
        name_list = []
        artist_list = []
        album_list = []
    else:
        e5.delete(0, len(e5.get()))
        e5.insert(0, 'import completed')


def ex_txt():
    global url_list
    global name_list
    global artist_list
    global album_list
    global settings_dict
    global e5

    save_data = ""
    saving = codecs.open('%s/min/save/_save_url.txt' % settings_dict['path'], 'w', 'utf-8')
    for i in range(len(name_list)):
        save_data += url_list[i] + "\n"
    saving.write(save_data[:-1])
    saving.close()
    save_data = ""
    saving = codecs.open('%s/min/save/_save_name.txt' % settings_dict['path'], 'w', 'utf-8')
    for i in range(len(name_list)):
        save_data += name_list[i] + "\n"
    saving.write(save_data[:-1])
    saving.close()
    save_data = ""
    saving = codecs.open('%s/min/save/_save_artist.txt' % settings_dict['path'], 'w', 'utf-8')
    for i in range(len(name_list)):
        save_data += artist_list[i] + "\n"
    saving.write(save_data[:-1])
    saving.close()
    save_data = ""
    saving = codecs.open('%s/min/save/_save_album.txt' % settings_dict['path'], 'w', 'utf-8')
    for i in range(len(name_list)):
        save_data += album_list[i] + "\n"
    saving.write(save_data[:-1])
    saving.close()
    e5.delete(0, len(e5.get()))
    e5.insert(0, 'export completed')


def in_settings():
    global settings_dict
    global e5

    try:
        loading = codecs.open('%s/min/settings.txt' % settings_dict['path'], 'rb', 'utf-8')
        settings_list = loading.read().replace('\r', '').split('\n')
        loading.close()
        for i in range(len(settings_dict)):
            try:
                settings_dict[settings_list[i].split('=')[0]] = int(settings_list[i].split('=')[1])
            except:
                settings_dict[settings_list[i].split('=')[0]] = settings_list[i].split('=')[1]

        e5.delete(0, len(e5.get()))
        e5.insert(0, 'settings loaded')
    except:
        ex_settings()


def ex_settings():
    global settings_dict
    global e5

    save_data = ""
    saving = codecs.open('%s/min/settings.txt' % settings_dict['path'], 'w', 'utf-8')
    for i in range(len(settings_dict)):
        save_data += str(list(settings_dict.keys())[i]) + "=" + str(list(settings_dict.values())[i]) + "\n"
    saving.write(save_data[:-1])
    saving.close()

    e5.delete(0, len(e5.get()))
    e5.insert(0, 'settings exported')

# =================================================설정=================================================
# =================================================설정=================================================
# =================================================설정=================================================

def settings_open():
    global settings_dict
    global window

    window.destroy()

    setting_window = Tk()
    setting_window.geometry('250x300')
    setting_window.resizable(width=False, height=False)
    setting_window.configure()


    def winres1():
        print(cv11.get())
        if cv11.get() == 0:
            setting_window.geometry('250x300')
            setting_window.resizable(width=False, height=False)
        elif cv11.get() == 1:
            setting_window.geometry('420x900')
            setting_window.resizable(width=True, height=True)


    def apply():
        settings_dict['path'] = str(e1.get()).replace('\\', '/')
        settings_dict['iscreatelyric'] = int(e2.get())
        settings_dict['ismp3'] = int(e3.get())
        settings_dict['ismp4'] = int(e4.get())
        settings_dict['isdevmode'] = int(e5.get())
        for i in range(len(tge_list)):
            settings_dict['hotkeyslot' + str(int(i)+1)] = tge_list[i].get()
        for i in range(len(tges_list)):
            if tges_list[i].get() != 1 or 2 or 3 or 4:
                continue
            settings_dict['hotkeyslotwhere' + str(int(i)+1)] = tges_list[i].get()

        print(settings_dict)

        setting_window.destroy()

        main_loop()


    cv11 = IntVar()  # 버튼 체크시 1, 비 체크시 0
    cb11 = Checkbutton(setting_window, text="Hotkey EDIT OPEN", variable=cv11, command=winres1)
    cb11.pack()
    cb11.place(x=10, y=220)
    # 체크박스 눌렀을 때 - 크기조정


    l1 = Label(setting_window, text='settings\n주의:경로에 있는 역슬래시\n슬래시로 다 바꾸고\n마지막 슬래시 빼고\nmin전의 폴더주소 입력', fg='red', font='helvetica 13 bold')
    l2 = Label(setting_window, text='path: ')

    l1.place(x=15, y=10)
    l2.place(x=10, y=110)

    e1 = Entry(setting_window)
    e1.place(x=50, y=110)

    e2 = IntVar()
    ev2 = Checkbutton(setting_window, text="create lyric file", variable=e2)
    ev2.pack()
    ev2.place(x=20, y=130)

    e3 = IntVar()
    ev3 = Checkbutton(setting_window, text="create mp3 file", variable=e3)
    ev3.pack()
    ev3.place(x=20, y=150)

    e4 = IntVar()
    ev4 = Checkbutton(setting_window, text="create mp4 file", variable=e4)
    ev4.pack()
    ev4.place(x=20, y=170)

    e5 = IntVar()
    ev5 = Checkbutton(setting_window, text="devmode", variable=e5)
    ev5.pack()
    ev5.place(x=20, y=190)

    sv1 = Button(setting_window, text="apply", command=apply)
    sv1.place(x=30, y=250)

    tg1 = Label(setting_window, text='text1: ')
    tg2 = Label(setting_window, text='text2: ')
    tg3 = Label(setting_window, text='text3: ')
    tg4 = Label(setting_window, text='text4: ')
    tg5 = Label(setting_window, text='text5: ')
    tg6 = Label(setting_window, text='text6: ')
    tg7 = Label(setting_window, text='text7: ')
    tg8 = Label(setting_window, text='text8: ')
    tg9 = Label(setting_window, text='text9: ')
    tg10 = Label(setting_window, text='text10: ')
    tg11 = Label(setting_window, text='text11: ')
    tg12 = Label(setting_window, text='text12: ')
    tg13 = Label(setting_window, text='text13: ')
    tg14 = Label(setting_window, text='text14: ')
    tg15 = Label(setting_window, text='text15: ')
    tg16 = Label(setting_window, text='text16: ')
    tg17 = Label(setting_window, text='text17: ')
    tg18 = Label(setting_window, text='text18: ')
    tg19 = Label(setting_window, text='text19: ')
    tg20 = Label(setting_window, text='text20: ')

    tg1.place(x=10, y=300)
    tg2.place(x=10, y=330)
    tg3.place(x=10, y=360)
    tg4.place(x=10, y=390)
    tg5.place(x=10, y=420)
    tg6.place(x=10, y=450)
    tg7.place(x=10, y=480)
    tg8.place(x=10, y=510)
    tg9.place(x=10, y=540)
    tg10.place(x=10, y=570)
    tg11.place(x=10, y=600)
    tg12.place(x=10, y=630)
    tg13.place(x=10, y=660)
    tg14.place(x=10, y=690)
    tg15.place(x=10, y=720)
    tg16.place(x=10, y=750)
    tg17.place(x=10, y=780)
    tg18.place(x=10, y=810)
    tg19.place(x=10, y=840)
    tg20.place(x=10, y=870)

    tge1 = Entry(setting_window)
    tge2 = Entry(setting_window)
    tge3 = Entry(setting_window)
    tge4 = Entry(setting_window)
    tge5 = Entry(setting_window)
    tge6 = Entry(setting_window)
    tge7 = Entry(setting_window)
    tge8 = Entry(setting_window)
    tge9 = Entry(setting_window)
    tge10 = Entry(setting_window)
    tge11 = Entry(setting_window)
    tge12 = Entry(setting_window)
    tge13 = Entry(setting_window)
    tge14 = Entry(setting_window)
    tge15 = Entry(setting_window)
    tge16 = Entry(setting_window)
    tge17 = Entry(setting_window)
    tge18 = Entry(setting_window)
    tge19 = Entry(setting_window)
    tge20 = Entry(setting_window)

    tge1.place(x=50, y=300)
    tge2.place(x=50, y=330)
    tge3.place(x=50, y=360)
    tge4.place(x=50, y=390)
    tge5.place(x=50, y=420)
    tge6.place(x=50, y=450)
    tge7.place(x=50, y=480)
    tge8.place(x=50, y=510)
    tge9.place(x=50, y=540)
    tge10.place(x=50, y=570)
    tge11.place(x=50, y=600)
    tge12.place(x=50, y=630)
    tge13.place(x=50, y=660)
    tge14.place(x=50, y=690)
    tge15.place(x=50, y=720)
    tge16.place(x=50, y=750)
    tge17.place(x=50, y=780)
    tge18.place(x=50, y=810)
    tge19.place(x=50, y=840)
    tge20.place(x=50, y=870)

    tgs1 = Label(setting_window, text='where(1,2,3,4): ')
    tgs2 = Label(setting_window, text='where(1,2,3,4): ')
    tgs3 = Label(setting_window, text='where(1,2,3,4): ')
    tgs4 = Label(setting_window, text='where(1,2,3,4): ')
    tgs5 = Label(setting_window, text='where(1,2,3,4): ')
    tgs6 = Label(setting_window, text='where(1,2,3,4): ')
    tgs7 = Label(setting_window, text='where(1,2,3,4): ')
    tgs8 = Label(setting_window, text='where(1,2,3,4): ')
    tgs9 = Label(setting_window, text='where(1,2,3,4): ')
    tgs10 = Label(setting_window, text='where(1,2,3,4): ')
    tgs11 = Label(setting_window, text='where(1,2,3,4): ')
    tgs12 = Label(setting_window, text='where(1,2,3,4): ')
    tgs13 = Label(setting_window, text='where(1,2,3,4): ')
    tgs14 = Label(setting_window, text='where(1,2,3,4): ')
    tgs15 = Label(setting_window, text='where(1,2,3,4): ')
    tgs16 = Label(setting_window, text='where(1,2,3,4): ')
    tgs17 = Label(setting_window, text='where(1,2,3,4): ')
    tgs18 = Label(setting_window, text='where(1,2,3,4): ')
    tgs19 = Label(setting_window, text='where(1,2,3,4): ')
    tgs20 = Label(setting_window, text='where(1,2,3,4): ')

    tgs1.place(x=160, y=300)
    tgs2.place(x=160, y=330)
    tgs3.place(x=160, y=360)
    tgs4.place(x=160, y=390)
    tgs5.place(x=160, y=420)
    tgs6.place(x=160, y=450)
    tgs7.place(x=160, y=480)
    tgs8.place(x=160, y=510)
    tgs9.place(x=160, y=540)
    tgs10.place(x=160, y=570)
    tgs11.place(x=160, y=600)
    tgs12.place(x=160, y=630)
    tgs13.place(x=160, y=660)
    tgs14.place(x=160, y=690)
    tgs15.place(x=160, y=720)
    tgs16.place(x=160, y=750)
    tgs17.place(x=160, y=780)
    tgs18.place(x=160, y=810)
    tgs19.place(x=160, y=840)
    tgs20.place(x=160, y=870)

    tges1 = Entry(setting_window)
    tges2 = Entry(setting_window)
    tges3 = Entry(setting_window)
    tges4 = Entry(setting_window)
    tges5 = Entry(setting_window)
    tges6 = Entry(setting_window)
    tges7 = Entry(setting_window)
    tges8 = Entry(setting_window)
    tges9 = Entry(setting_window)
    tges10 = Entry(setting_window)
    tges11 = Entry(setting_window)
    tges12 = Entry(setting_window)
    tges13 = Entry(setting_window)
    tges14 = Entry(setting_window)
    tges15 = Entry(setting_window)
    tges16 = Entry(setting_window)
    tges17 = Entry(setting_window)
    tges18 = Entry(setting_window)
    tges19 = Entry(setting_window)
    tges20 = Entry(setting_window)

    tges1.place(x=250, y=300)
    tges2.place(x=250, y=330)
    tges3.place(x=250, y=360)
    tges4.place(x=250, y=390)
    tges5.place(x=250, y=420)
    tges6.place(x=250, y=450)
    tges7.place(x=250, y=480)
    tges8.place(x=250, y=510)
    tges9.place(x=250, y=540)
    tges10.place(x=250, y=570)
    tges11.place(x=250, y=600)
    tges12.place(x=250, y=630)
    tges13.place(x=250, y=660)
    tges14.place(x=250, y=690)
    tges15.place(x=250, y=720)
    tges16.place(x=250, y=750)
    tges17.place(x=250, y=780)
    tges18.place(x=250, y=810)
    tges19.place(x=250, y=840)
    tges20.place(x=250, y=870)

    tge_list = [tge1, tge2, tge3, tge4, tge5, tge6, tge7, tge8, tge9, tge10, tge11, tge12, tge13, tge14, tge15, tge16, tge17,
        tge18, tge19, tge20]
    tges_list = [tges1, tges2, tges3, tges4, tges5, tges6, tges7, tges8, tges9, tges10, tges11, tges12, tges13, tges14, tges15,
        tges16, tges17, tges18, tges19, tges20]

    e1.insert(0, settings_dict['path'])
    if settings_dict['iscreatelyric'] == 1:
        ev2.toggle()
    if settings_dict['ismp3'] == 1:
        ev3.toggle()
    if settings_dict['ismp4'] == 1:
        ev4.toggle()
    if settings_dict['isdevmode'] == 1:
        ev5.toggle()
    for i in range(len(tge_list)):
        tge_list[i].insert(0, settings_dict['hotkeyslot' + str(int(i) + 1)])
    for i in range(len(tges_list)):
        tges_list[i].insert(0, settings_dict['hotkeyslotwhere' + str(int(i) + 1)])

    setting_window.mainloop()

# =================================================리스트=================================================
# =================================================리스트=================================================
# =================================================리스트=================================================

def save():
    global url_list
    global name_list
    global artist_list
    global album_list
    yturl = e1.get()
    filename = e2.get()
    artistname = e3.get()
    albumname = e4.get()
    e1.delete(0, len(e1.get()))
    e2.delete(0, len(e2.get()))
    e3.delete(0, len(e3.get()))
    e4.delete(0, len(e4.get()))
    e5.delete(0, len(e5.get()))

    if_incorrect = 0
    for i in range(len(f'{filename}')):
        if f'{filename[i]}' == '.' or f'{filename[i]}' == '/' or f'{filename[i]}' == '\\' or f'{filename[i]}' == ':'\
            or f'{filename[i]}' == '*' or f'{filename[i]}' == '?' or f'{filename[i]}' == '"' or f'{filename[i]}' == '<'\
            or f'{filename[i]}' == '>' or f'{filename[i]}' == '|' or f'{filename[i]}' == '%' or f'{filename[i]}' == '≒':
            if_incorrect = 1

    if yturl == None:
        e5.insert(0, 'incorrect youtube url')

    # [실험적]
    elif yturl == "vocaloid" or yturl == "vcl":
        vcl()

    elif filename == None:
        e5.insert(0, 'incorrect fliename')
    elif yturl == None:
        e5.insert(0, 'incorrect url')
    elif if_incorrect == 1:
        e5.insert(0, 'incorrent filename')
    else:
        url_list.append(yturl)
        name_list.append(filename)
        artist_list.append(artistname)
        album_list.append(albumname)
        e5.insert(0, 'saved - %s' % filename)


def vcl():  # for test
    global url_list
    global name_list
    global artist_list
    global album_list
    url_list.append("https://www.youtube.com/watch?v=UnIhRpIT7nc")
    name_list.append("ラグトレイン")
    artist_list.append("歌愛ユキ")
    album_list.append("稲葉曇")
    url_list.append("https://www.youtube.com/watch?v=e1xCOsgWG0M")
    name_list.append("ヴァンパイア")
    artist_list.append("初音ミク")
    album_list.append("DECO*27")
    url_list.append("https://www.youtube.com/watch?v=emrt46SRyYs")
    name_list.append("DAYBREAK FRONTLINE")
    artist_list.append("IA")
    album_list.append("Orangestar")
    url_list.append("https://www.youtube.com/watch?v=romqp_SB4tU")
    name_list.append("ノイローゼ")
    artist_list.append("v flower")
    album_list.append("栗山夕璃")
    url_list.append("https://www.youtube.com/watch?v=ARt2fVT33Lw")
    name_list.append("SLoWMoTIoN")
    artist_list.append("初音ミク")
    album_list.append("ピノキオピー")
    e5.delete(0, len(e5.get()))
    e5.insert(0, 'リストを確認してみて！')


def reset():
    e1.delete(0, len(e1.get()))
    e2.delete(0, len(e2.get()))
    e3.delete(0, len(e3.get()))
    e4.delete(0, len(e4.get()))
    e5.delete(0, len(e5.get()))
    e5.insert(0, 'clear')


def see_list():
    seelist = ""
    for i in range(len(name_list)):
        seelist += name_list[i] + " : " + url_list[i] + "\n"
    nwindow = Toplevel(window)
    nwindow.geometry('500x200')
    nwindow.resizable(width=True, height=True)
    nl1 = Label(nwindow, text=seelist)
    nl1.place(x=10, y=10)
    nwindow.mainloop()


def one_delete():
    global url_list
    global name_list
    global artist_list
    global album_list
    del url_list[-1]
    del name_list[-1]
    del artist_list[-1]
    del album_list[-1]
    e5.delete(0, len(e5.get()))
    e5.insert(0, 'undo completed')


def list_reset():
    global url_list
    global name_list
    global artist_list
    global album_list
    url_list = []
    name_list = []
    artist_list = []
    album_list = []
    e5.delete(0, len(e5.get()))
    e5.insert(0, 'list reset completed')

# =================================================창=================================================
# =================================================창=================================================
# =================================================창=================================================

def info():
    loading = codecs.open('C:/Users/dongi/Desktop/min/info.txt', 'rb', 'utf-8')
    loadedinfo = loading.read()
    loading.close()
    nwindow = Toplevel(window)
    nwindow.geometry('300x300')
    nwindow.resizable(width=True, height=True)
    nl1 = Label(nwindow, text=loadedinfo)
    nl1.place(x=10, y=10)
    nwindow.mainloop()

def main_loop():
    global window
    global e1
    global e2
    global e3
    global e4
    global e5

    # GUI 창
    window = Tk()
    window.geometry('260x390')
    window.resizable(width=False, height=False)
    window.configure()


    # 체크박스 눌렀을 때 - 크기조정
    def winres():
        if cv1.get() == 0:
            window.geometry('260x390')
            window.resizable(width=False, height=False)
        elif cv1.get() == 1:
            window.geometry('280x650')
            window.resizable(width=True, height=True)


    l1 = Label(window, text='Mp3 downloader', fg='red', font='helvetica 16 bold')
    l2 = Label(window, text='url: ')
    l3 = Label(window, text='set name: ')
    l4 = Label(window, text='artist: ')
    l5 = Label(window, text='album: ')

    l1.place(x=15, y=10)
    l2.place(x=10, y=40)
    l3.place(x=10, y=70)
    l4.place(x=10, y=100)
    l5.place(x=10, y=130)

    e1 = Entry(window)
    e2 = Entry(window)
    e3 = Entry(window)
    e4 = Entry(window)
    e5 = Entry(window)

    e1.place(x=75, y=40)
    e2.place(x=75, y=70)
    e3.place(x=75, y=100)
    e4.place(x=75, y=130)
    e5.place(x=75, y=200)

    # to line 50 ~
    b001 = Button(window, text="정보 저장", command=save)
    b002 = Button(window, text="리셋", command=reset)

    b001.place(x=60, y=160)
    b002.place(x=150, y=160)

    b111 = Button(window, text="1개 취소", command=one_delete)
    b112 = Button(window, text="리스트 리셋", command=list_reset)
    b113 = Button(window, text="리스트 보기", command=see_list)
    b211 = Button(window, text="태그하기", command=tagging)
    b212 = Button(window, text="다운로드", command=downloading)
    b213 = Button(window, text="정리(재실행)", command=mp4_all_delete)
    b311 = Button(window, text="설정", command=settings_open)
    b312 = Button(window, text="가사태그하기", command=lyric_tagging)
    b313 = Button(window, text="설정불러오기", command=in_settings)
    b411 = Button(window, text="불러오기", command=in_txt)
    b412 = Button(window, text="내보내기", command=ex_txt)
    b413 = Button(window, text="설정내보내기", command=ex_settings)


    b111.place(x=10, y=230)
    b112.place(x=80, y=230)
    b113.place(x=170, y=230)
    b211.place(x=10, y=260)
    b212.place(x=80, y=260)
    b213.place(x=170, y=260)
    b311.place(x=10, y=290)
    b312.place(x=80, y=290)
    b313.place(x=170, y=290)
    b411.place(x=10, y=320)
    b412.place(x=80, y=320)
    b413.place(x=170, y=320)


    cv1 = IntVar()  # 버튼 체크시 1, 비 체크시 0
    cb1 = Checkbutton(window, text="모드 vcl", variable=cv1, command=winres)
    cb1.pack()
    cb1.place(x=10, y=350)

    bsp1 = Button(window, text="정보", command=info)
    bsp1.place(x=150, y=350)

    b0211 = Button(window, text=settings_dict['hotkeyslot1'], command=hotkey_input_1)
    b0212 = Button(window, text=settings_dict['hotkeyslot2'], command=hotkey_input_2)
    b0213 = Button(window, text=settings_dict['hotkeyslot3'], command=hotkey_input_3)
    b0221 = Button(window, text=settings_dict['hotkeyslot4'], command=hotkey_input_4)
    b0222 = Button(window, text=settings_dict['hotkeyslot5'], command=hotkey_input_5)
    b0223 = Button(window, text=settings_dict['hotkeyslot6'], command=hotkey_input_6)
    b0231 = Button(window, text=settings_dict['hotkeyslot7'], command=hotkey_input_7)
    b0232 = Button(window, text=settings_dict['hotkeyslot8'], command=hotkey_input_8)
    b0241 = Button(window, text=settings_dict['hotkeyslot9'], command=hotkey_input_9)
    b0242 = Button(window, text=settings_dict['hotkeyslot10'], command=hotkey_input_10)
    b0251 = Button(window, text=settings_dict['hotkeyslot11'], command=hotkey_input_11)
    b0252 = Button(window, text=settings_dict['hotkeyslot12'], command=hotkey_input_12)
    b0261 = Button(window, text=settings_dict['hotkeyslot13'], command=hotkey_input_13)
    b0262 = Button(window, text=settings_dict['hotkeyslot14'], command=hotkey_input_14)
    b0271 = Button(window, text=settings_dict['hotkeyslot15'], command=hotkey_input_15)
    b0272 = Button(window, text=settings_dict['hotkeyslot16'], command=hotkey_input_16)
    b0281 = Button(window, text=settings_dict['hotkeyslot17'], command=hotkey_input_17)
    b0282 = Button(window, text=settings_dict['hotkeyslot18'], command=hotkey_input_18)
    b0291 = Button(window, text=settings_dict['hotkeyslot19'], command=hotkey_input_19)
    b0292 = Button(window, text=settings_dict['hotkeyslot20'], command=hotkey_input_20)

    b0211.place(x=10, y=400)
    b0212.place(x=100, y=400)
    b0213.place(x=200, y=400)
    b0221.place(x=10, y=425)
    b0222.place(x=100, y=425)
    b0223.place(x=200, y=425)
    b0231.place(x=10, y=450)
    b0232.place(x=100, y=450)
    b0241.place(x=10, y=475)
    b0242.place(x=100, y=475)
    b0251.place(x=10, y=500)
    b0252.place(x=100, y=500)
    b0261.place(x=10, y=525)
    b0262.place(x=100, y=525)
    b0271.place(x=10, y=550)
    b0272.place(x=100, y=550)
    b0281.place(x=10, y=575)
    b0282.place(x=100, y=575)
    b0291.place(x=10, y=600)
    b0292.place(x=100, y=600)

    window.mainloop()

# =================================================핫키입력=================================================
# =================================================핫키입력=================================================
# =================================================핫키입력=================================================

def hotkey_input_1():
    if settings_dict['hotkeyslotwhere1'] == 1:
        e1.insert(0, settings_dict['hotkeyslot1'])
    elif settings_dict['hotkeyslotwhere1'] == 2:
        e2.insert(0, settings_dict['hotkeyslot1'])
    elif settings_dict['hotkeyslotwhere1'] == 3:
        e3.insert(0, settings_dict['hotkeyslot1'])
    elif settings_dict['hotkeyslotwhere1'] == 4:
        e4.insert(0, settings_dict['hotkeyslot1'])
def hotkey_input_2():
    if settings_dict['hotkeyslotwhere2'] == 1:
        e1.insert(0, settings_dict['hotkeyslot2'])
    elif settings_dict['hotkeyslotwhere2'] == 2:
        e2.insert(0, settings_dict['hotkeyslot2'])
    elif settings_dict['hotkeyslotwhere2'] == 3:
        e3.insert(0, settings_dict['hotkeyslot2'])
    elif settings_dict['hotkeyslotwhere2'] == 4:
        e4.insert(0, settings_dict['hotkeyslot2'])
def hotkey_input_3():
    if settings_dict['hotkeyslotwhere3'] == 1:
        e1.insert(0, settings_dict['hotkeyslot3'])
    elif settings_dict['hotkeyslotwhere3'] == 2:
        e2.insert(0, settings_dict['hotkeyslot3'])
    elif settings_dict['hotkeyslotwhere3'] == 3:
        e3.insert(0, settings_dict['hotkeyslot3'])
    elif settings_dict['hotkeyslotwhere3'] == 4:
        e4.insert(0, settings_dict['hotkeyslot3'])
def hotkey_input_4():
    if settings_dict['hotkeyslotwhere4'] == 1:
        e1.insert(0, settings_dict['hotkeyslot4'])
    elif settings_dict['hotkeyslotwhere4'] == 2:
        e2.insert(0, settings_dict['hotkeyslot4'])
    elif settings_dict['hotkeyslotwhere4'] == 3:
        e3.insert(0, settings_dict['hotkeyslot4'])
    elif settings_dict['hotkeyslotwhere4'] == 4:
        e4.insert(0, settings_dict['hotkeyslot4'])
def hotkey_input_5():
    if settings_dict['hotkeyslotwhere5'] == 1:
        e1.insert(0, settings_dict['hotkeyslot5'])
    elif settings_dict['hotkeyslotwhere5'] == 2:
        e2.insert(0, settings_dict['hotkeyslot5'])
    elif settings_dict['hotkeyslotwhere5'] == 3:
        e3.insert(0, settings_dict['hotkeyslot5'])
    elif settings_dict['hotkeyslotwhere5'] == 4:
        e4.insert(0, settings_dict['hotkeyslot5'])
def hotkey_input_6():
    if settings_dict['hotkeyslotwhere6'] == 1:
        e1.insert(0, settings_dict['hotkeyslot6'])
    elif settings_dict['hotkeyslotwhere6'] == 2:
        e2.insert(0, settings_dict['hotkeyslot6'])
    elif settings_dict['hotkeyslotwhere6'] == 3:
        e3.insert(0, settings_dict['hotkeyslot6'])
    elif settings_dict['hotkeyslotwhere6'] == 4:
        e4.insert(0, settings_dict['hotkeyslot6'])
def hotkey_input_7():
    if settings_dict['hotkeyslotwhere7'] == 1:
        e1.insert(0, settings_dict['hotkeyslot7'])
    elif settings_dict['hotkeyslotwhere7'] == 2:
        e2.insert(0, settings_dict['hotkeyslot7'])
    elif settings_dict['hotkeyslotwhere7'] == 3:
        e3.insert(0, settings_dict['hotkeyslot7'])
    elif settings_dict['hotkeyslotwhere7'] == 4:
        e4.insert(0, settings_dict['hotkeyslot7'])
def hotkey_input_8():
    if settings_dict['hotkeyslotwhere8'] == 1:
        e1.insert(0, settings_dict['hotkeyslot8'])
    elif settings_dict['hotkeyslotwhere8'] == 2:
        e2.insert(0, settings_dict['hotkeyslot8'])
    elif settings_dict['hotkeyslotwhere8'] == 3:
        e3.insert(0, settings_dict['hotkeyslot8'])
    elif settings_dict['hotkeyslotwhere8'] == 4:
        e4.insert(0, settings_dict['hotkeyslot8'])
def hotkey_input_9():
    if settings_dict['hotkeyslotwhere9'] == 1:
        e1.insert(0, settings_dict['hotkeyslot9'])
    elif settings_dict['hotkeyslotwhere9'] == 2:
        e2.insert(0, settings_dict['hotkeyslot9'])
    elif settings_dict['hotkeyslotwhere9'] == 3:
        e3.insert(0, settings_dict['hotkeyslot9'])
    elif settings_dict['hotkeyslotwhere9'] == 4:
        e4.insert(0, settings_dict['hotkeyslot9'])
def hotkey_input_10():
    if settings_dict['hotkeyslotwhere10'] == 1:
        e1.insert(0, settings_dict['hotkeyslot10'])
    elif settings_dict['hotkeyslotwhere10'] == 2:
        e2.insert(0, settings_dict['hotkeyslot10'])
    elif settings_dict['hotkeyslotwhere10'] == 3:
        e3.insert(0, settings_dict['hotkeyslot10'])
    elif settings_dict['hotkeyslotwhere10'] == 4:
        e4.insert(0, settings_dict['hotkeyslot10'])
def hotkey_input_11():
    if settings_dict['hotkeyslotwhere11'] == 1:
        e1.insert(0, settings_dict['hotkeyslot11'])
    elif settings_dict['hotkeyslotwhere11'] == 2:
        e2.insert(0, settings_dict['hotkeyslot11'])
    elif settings_dict['hotkeyslotwhere11'] == 3:
        e3.insert(0, settings_dict['hotkeyslot11'])
    elif settings_dict['hotkeyslotwhere11'] == 4:
        e4.insert(0, settings_dict['hotkeyslot11'])
def hotkey_input_12():
    if settings_dict['hotkeyslotwhere12'] == 1:
        e1.insert(0, settings_dict['hotkeyslot12'])
    elif settings_dict['hotkeyslotwhere12'] == 2:
        e2.insert(0, settings_dict['hotkeyslot12'])
    elif settings_dict['hotkeyslotwhere12'] == 3:
        e3.insert(0, settings_dict['hotkeyslot12'])
    elif settings_dict['hotkeyslotwhere12'] == 4:
        e4.insert(0, settings_dict['hotkeyslot12'])
def hotkey_input_13():
    if settings_dict['hotkeyslotwhere13'] == 1:
        e1.insert(0, settings_dict['hotkeyslot13'])
    elif settings_dict['hotkeyslotwhere13'] == 2:
        e2.insert(0, settings_dict['hotkeyslot13'])
    elif settings_dict['hotkeyslotwhere13'] == 3:
        e3.insert(0, settings_dict['hotkeyslot13'])
    elif settings_dict['hotkeyslotwhere13'] == 4:
        e4.insert(0, settings_dict['hotkeyslot13'])
def hotkey_input_14():
    if settings_dict['hotkeyslotwhere14'] == 1:
        e1.insert(0, settings_dict['hotkeyslot14'])
    elif settings_dict['hotkeyslotwhere14'] == 2:
        e2.insert(0, settings_dict['hotkeyslot14'])
    elif settings_dict['hotkeyslotwhere14'] == 3:
        e3.insert(0, settings_dict['hotkeyslot14'])
    elif settings_dict['hotkeyslotwhere14'] == 4:
        e4.insert(0, settings_dict['hotkeyslot14'])
def hotkey_input_15():
    if settings_dict['hotkeyslotwhere15'] == 1:
        e1.insert(0, settings_dict['hotkeyslot15'])
    elif settings_dict['hotkeyslotwhere15'] == 2:
        e2.insert(0, settings_dict['hotkeyslot15'])
    elif settings_dict['hotkeyslotwhere15'] == 3:
        e3.insert(0, settings_dict['hotkeyslot15'])
    elif settings_dict['hotkeyslotwhere15'] == 4:
        e4.insert(0, settings_dict['hotkeyslot15'])
def hotkey_input_16():
    if settings_dict['hotkeyslotwhere16'] == 1:
        e1.insert(0, settings_dict['hotkeyslot16'])
    elif settings_dict['hotkeyslotwhere16'] == 2:
        e2.insert(0, settings_dict['hotkeyslot16'])
    elif settings_dict['hotkeyslotwhere16'] == 3:
        e3.insert(0, settings_dict['hotkeyslot16'])
    elif settings_dict['hotkeyslotwhere16'] == 4:
        e4.insert(0, settings_dict['hotkeyslot16'])
def hotkey_input_17():
    if settings_dict['hotkeyslotwhere17'] == 1:
        e1.insert(0, settings_dict['hotkeyslot17'])
    elif settings_dict['hotkeyslotwhere17'] == 2:
        e2.insert(0, settings_dict['hotkeyslot17'])
    elif settings_dict['hotkeyslotwhere17'] == 3:
        e3.insert(0, settings_dict['hotkeyslot17'])
    elif settings_dict['hotkeyslotwhere17'] == 4:
        e4.insert(0, settings_dict['hotkeyslot17'])
def hotkey_input_18():
    if settings_dict['hotkeyslotwhere18'] == 1:
        e1.insert(0, settings_dict['hotkeyslot18'])
    elif settings_dict['hotkeyslotwhere18'] == 2:
        e2.insert(0, settings_dict['hotkeyslot18'])
    elif settings_dict['hotkeyslotwhere18'] == 3:
        e3.insert(0, settings_dict['hotkeyslot18'])
    elif settings_dict['hotkeyslotwhere18'] == 4:
        e4.insert(0, settings_dict['hotkeyslot18'])
def hotkey_input_19():
    if settings_dict['hotkeyslotwhere19'] == 1:
        e1.insert(0, settings_dict['hotkeyslot19'])
    elif settings_dict['hotkeyslotwhere19'] == 2:
        e2.insert(0, settings_dict['hotkeyslot19'])
    elif settings_dict['hotkeyslotwhere19'] == 3:
        e3.insert(0, settings_dict['hotkeyslot19'])
    elif settings_dict['hotkeyslotwhere19'] == 4:
        e4.insert(0, settings_dict['hotkeyslot19'])
def hotkey_input_20():
    if settings_dict['hotkeyslotwhere20'] == 1:
        e1.insert(0, settings_dict['hotkeyslot20'])
    elif settings_dict['hotkeyslotwhere20'] == 2:
        e2.insert(0, settings_dict['hotkeyslot20'])
    elif settings_dict['hotkeyslotwhere20'] == 3:
        e3.insert(0, settings_dict['hotkeyslot20'])
    elif settings_dict['hotkeyslotwhere20'] == 4:
        e4.insert(0, settings_dict['hotkeyslot20'])

# =================================================기초셋팅=================================================
# =================================================기초셋팅=================================================
# =================================================기초셋팅=================================================

url_list = []
name_list = []
artist_list = []
album_list = []
this_is_dummy = 1
settings_dict = {'path': '', 'iscreatelyric': 0, 'ismp3': 1, 'ismp4': 0, 'isdevmode': 0,
        'hotkeyslot1': '', 'hotkeyslot2': '', 'hotkeyslot3': '', 'hotkeyslot4': '', 'hotkeyslot5': '',
        'hotkeyslot6': '', 'hotkeyslot7': '', 'hotkeyslot8': '', 'hotkeyslot9': '', 'hotkeyslot10': '',
        'hotkeyslot11': '', 'hotkeyslot12': '', 'hotkeyslot13': '', 'hotkeyslot14': '', 'hotkeyslot15': '',
        'hotkeyslot16': '', 'hotkeyslot17': '', 'hotkeyslot18': '', 'hotkeyslot19': '', 'hotkeyslot20': '',
        'hotkeyslotwhere1': '', 'hotkeyslotwhere2': '', 'hotkeyslotwhere3': '', 'hotkeyslotwhere4': '', 'hotkeyslotwhere5': '',
        'hotkeyslotwhere6': '', 'hotkeyslotwhere7': '', 'hotkeyslotwhere8': '', 'hotkeyslotwhere9': '', 'hotkeyslotwhere10': '',
        'hotkeyslotwhere11': '', 'hotkeyslotwhere12': '', 'hotkeyslotwhere13': '', 'hotkeyslotwhere14': '', 'hotkeyslotwhere15': '',
        'hotkeyslotwhere16': '', 'hotkeyslotwhere17': '', 'hotkeyslotwhere18': '', 'hotkeyslotwhere19': '', 'hotkeyslotwhere20': ''
        }

# =================================================구동부=================================================
# =================================================구동부=================================================
# =================================================구동부=================================================

try:
    in_txt()
except:
    pass

main_loop()
