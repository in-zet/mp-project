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

from downloads import *
from porters import *
from settings import *
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


# [실험적]
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


# 리스트 리셋
def reset():
    e1.delete(0, len(e1.get()))
    e2.delete(0, len(e2.get()))
    e3.delete(0, len(e3.get()))
    e4.delete(0, len(e4.get()))
    e5.delete(0, len(e5.get()))
    e5.insert(0, 'clear')


# 리스트 보기
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


# info
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


# 리스트 마지막 하나 없애기
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


# 리스트 리셋
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


# 자동 보카로 입력기
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
b311 = Button(window, text="dev", command=None)
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

# to line 425 ~
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

try:
    in_txt()
except:
    pass
window.mainloop()
