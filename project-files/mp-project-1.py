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




# ----------
# 21.x.x /v0.1/ : 프로젝트 폐기 - 작동불능
# 21.8.13 /v0.11/ : 프로젝트 재가동중 - 정상작동 확인
# 21.10.22 /v0.2/ : youtube-dll 의 속도저하 문제 해결 위한 pytube 모듈 도입
# 21.11.22 /v0.21/ : Github에 업로드
# 21.12.04 /v0.22/ : 코드 최적화, mp4 폴더 분리, 변수 이름 변경
# ----------
# D:\python coding\ffmpeg-N-101711-ga4e518c321-win64-gpl\bin\song database.py
# ^ 베타 버전(구)
# ----------
# 중요 : python 파일이 있는 곳에 ffmpeg.exe 와 ffprobe.exe가 있어야지만 정상작동
# ----------


def bc1():
    global bc
    bc = 1
    pup()
def bc2():
    global bc
    bc = 2
    pup()
def bc3():
    global bc
    bc = 3
    pup()
def bc4():
    global bc
    bc = 4
    pup()
def bc5():
    global bc
    bc = 5
    pup()
def bc6():
    global bc
    bc = 6
    pup()
def bc7():
    global bc
    bc = 7
    pup()
def bc8():
    global bc
    bc = 8
    pup()


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


# 리스트에 저장
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


# 리스트 리셋
def reset():
    e1.delete(0, len(e1.get()))
    e2.delete(0, len(e2.get()))
    e3.delete(0, len(e3.get()))
    e4.delete(0, len(e4.get()))
    e5.delete(0, len(e5.get()))
    e5.insert(0, 'clear')


# 리스트 보기
def seel():
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
def pup2():
    loading = codecs.open('C:/Users/dongi/Desktop/min/info.txt', 'rb', 'utf-8')
    loadedinfo = loading.read()
    loading.close()
    nwindow = Toplevel(window)
    nwindow.geometry('300x300')
    nwindow.resizable(width=True, height=True)
    nl1 = Label(nwindow, text=loadedinfo)
    nl1.place(x=10, y=10)
    nwindow.mainloop()


# '정말입니까' 확인창
def pup():
    global nwindow
    nwindow = Toplevel(window)
    nwindow.geometry('100x80')
    nwindow.resizable(width=False, height=False)
    nl1 = Label(nwindow, text="정말입니까?")
    nl1.place(x=15, y=10)
    nb1 = Button(nwindow, text="yes", command=isyes)
    nb2 = Button(nwindow, text="no", command=isno)
    nb1.place(x=10, y=50)
    nb2.place(x=50, y=50)
    nwindow.mainloop()


# '정말입니까' 에서 예
def isyes():
    global nwindow
    global bc
    global fnc_list
    nwindow.destroy()
    fnc_list[bc-1]()


# '정말입니까' 에서 아니오
def isno():
    global nwindow
    nwindow.destroy()


# 리스트 마지막 하나 없애기
def rundo():
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
def listreset():
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


# 태그 작성 - mutagen
def tagging():
    try:

        for i in range(len(name_list)):
            for i in range(1, 3):
                path1 = "C:/Users/dongi/Desktop/min/mp3/%s.mp3" % name_list[i]
                try:
                    tag1 = EasyID3(path1)
                except mutagen.id3.ID3NoHeaderError:  # an MP4 tag already exists
                    tag1 = mutagen.File(path1, easy=True)
                    tag1.add_tags()
                if artist_list[i] != None:
                    tag1['artist'] = str(artist_list[i])
                if album_list[i] != None:
                    tag1['album'] = str(album_list[i])
                tag1.save(path1, v1=i)

        e5.delete(0, len(e5.get()))
        e5.insert(0, 'tagging completed')

    except Exception as e:
        e5.delete(0, len(e5.get()))
        e5.insert(0, 'error: ' + str(e))


# 가사 작성 - mutagen
def lyricwrite():
    path_dir_mp3 = 'C:/Users/dongi/Desktop/min/mp3'
    path_dir_lyrics = 'C:/Users/dongi/Desktop/min/lyrics'
    mp3_list = os.listdir(path_dir_mp3)
    lyrics_list = os.listdir(path_dir_lyrics)
    rightnum = 0

    if len(mp3_list) < len(lyrics_list):
        for i in range(len(mp3_list)):
            for j in range(len(lyrics_list)):
                if f'{mp3_list[i][:-4]}' == f'{lyrics_list[j][:-4]}':
                    rightnum = j
            mp3path = 'C:/Users/dongi/Desktop/min/mp3/' + mp3_list[i]
            lyricspath = 'C:/Users/dongi/Desktop/min/lyrics/' + lyrics_list[rightnum]
            tag1 = EasyID3(mp3path)
            ln1 = open(lyricspath, 'r')
            lyr1 = ln1.read()
            tag1['lyricist'] = str(lyr1)
            tag1.save(mp3path, v1=2)
            ln1.close()
            e5.delete(0, len(e5.get()))
            e5.insert(0, 'lyric completed')

    elif len(mp3_list) == len(lyrics_list):
        for i in range(len(mp3_list)):
            mp3path = 'C:/Users/dongi/Desktop/min/mp3/' + mp3_list[i]
            lyricspath = 'C:/Users/dongi/Desktop/min/lyrics/' + lyrics_list[i]
            tag1 = EasyID3(mp3path)
            ln1 = open(lyricspath, 'r')
            lyr1 = ln1.read()
            tag1['lyricist'] = str(lyr1)
            tag1.save(mp3path, v1=2)
            ln1.close()
            e5.delete(0, len(e5.get()))
            e5.insert(0, 'lyric completed')

    else:
        e5.delete(0, len(e5.get()))
        e5.insert(0, 'the number of mp3s and lyrics are not same')


# 유튜브에서 노래 다운로드 - pytube
def downloading():
    global url_list
    global name_list
    global artist_list
    global album_list
    path_dir_mp3 = 'C:/Users/dongi/Desktop/min/mp3'
    path_dir_lyrics = 'C:/Users/dongi/Desktop/min/lyrics'
    mp3_list = os.listdir(path_dir_mp3)
    lyrics_list = os.listdir(path_dir_lyrics)
    if_again_mp3 = 0
    if_again_lyric = 0

    try:
        for i in range(len(name_list)):
            for j in range(len(lyrics_list)):
                if name_list[i] == f'{lyrics_list[j][:-4]}':  # 중복가사파일확인
                    if_again_lyric = 1

            if if_again_lyric == 0:
                _ = open("C:/Users/dongi/Desktop/min/lyrics/%s.txt" % name_list[i], 'w')
            elif if_again_lyric == 1:
                if_again_lyric = 0
                print("\n%s lyric file skipped\n" % name_list[i])

        for i in range(len(name_list)):
            for j in range(len(mp3_list)):
                if name_list[i] == f'{mp3_list[j][:-4]}':  # 중복음악파일확인
                    if_again_mp3 = 1

            if if_again_mp3 == 0:
                download_path = "C:/Users/dongi/Desktop/min/mp3/%s" % name_list[i]
                url1 = url_list[i]

                print("\n%s" % name_list[i])  # checking in console
                print("%s\n" % url1)

                yt = YouTube(url1)
                yt.streams.filter(progressive=True, file_extension='mp4').order_by('resolution').desc().first().download(path_dir_mp3, "C:/Users/dongi/Desktop/min/mp4/%s.mp4" % name_list[i])

                vv = VideoFileClip(os.path.join("C:/Users/dongi/Desktop/min/mp4", "C:/Users/dongi/Desktop/min/mp4", "C:/Users/dongi/Desktop/min/mp4/%s.mp4" % name_list[i]))
                vv.audio.write_audiofile(os.path.join("C:/Users/dongi/Desktop/min/mp3", "C:/Users/dongi/Desktop/min/mp3", "C:/Users/dongi/Desktop/min/mp3/%s.mp3" % name_list[i]))

            elif if_again_mp3 == 1:
                if_again_mp3 = 0
                print("\n%s mp3 file skipped\n" % name_list[i])

        e5.delete(0, len(e5.get()))
        e5.insert(0, 'downloded')
        print("\nFIN\n")

    except Exception as e:
        e5.delete(0, len(e5.get()))
        e5.insert(0, 'error: ' + str(e))


# mp4 파일 삭제
def delx():
    global name_list
    try:
        for i in range(len(name_list)):
            os.remove("C:/Users/dongi/Desktop/min/mp3/%s.mp4" % name_list[i])
        e5.delete(0, len(e5.get()))
        e5.insert(0, 'deleted')
    except Exception as e:
        e5.delete(0, len(e5.get()))
        e5.insert(0, 'error: ' + str(e))


# [실험적]
# 관리 기능, 현재 : 리스트 콘솔로 추출
def dev():
    global nwindow
    nwindow.destroy()
    print(url_list)
    print(name_list)
    print(artist_list)
    print(album_list)
    """[os.remove(f) for f in glob.glob("C:/Users/dongi/Desktop/min/mp3/*.mp3")]
    [os.remove(f) for f in glob.glob("C:/Users/dongi/Desktop/min/lyrics/*.txt")]"""
    e5.delete(0, len(e5.get()))
    e5.insert(0, 'dev')


# 정보 불러오기
def in_txt():
    global url_list
    global name_list
    global artist_list
    global album_list
    url_list = []
    name_list = []
    artist_list = []
    album_list = []
    loading = codecs.open('C:/Users/dongi/Desktop/min/save/_save_url.txt', 'rb', 'utf-8')
    url_list = loading.read().split('\n')
    loading.close()
    loading = codecs.open('C:/Users/dongi/Desktop/min/save/_save_name.txt', 'rb', 'utf-8')
    name_list = loading.read().split('\n')
    loading.close()
    loading = codecs.open('C:/Users/dongi/Desktop/min/save/_save_artist.txt', 'rb', 'utf-8')
    artist_list = loading.read().split('\n')
    loading.close()
    loading = codecs.open('C:/Users/dongi/Desktop/min/save/_save_album.txt', 'rb', 'utf-8')
    album_list = loading.read().split('\n')
    loading.close()
    if len(url_list) != len(name_list) or len(name_list) != len(artist_list) or len(artist_list) != len(album_list) or len(url_list) != len(album_list):
        e5.delete(0, len(e5.get()))
        e5.insert(0, 'error : different lines')
        url_list = []
        name_list = []
        artist_list = []
        album_list = []
    else:
        e5.delete(0, len(e5.get()))
        e5.insert(0, 'import completed')


# 정보 내보내기
def ex_txt():
    global url_list
    global name_list
    global artist_list
    global album_list
    save_data = ""
    saving = codecs.open('C:/Users/dongi/Desktop/min/save/_save_url.txt', 'w', 'utf-8')
    for i in range(len(name_list)):
        save_data += url_list[i] + "\n"
    saving.write(save_data[:-1])
    saving.close()
    save_data = ""
    saving = codecs.open('C:/Users/dongi/Desktop/min/save/_save_name.txt', 'w', 'utf-8')
    for i in range(len(name_list)):
        save_data += name_list[i] + "\n"
    saving.write(save_data[:-1])
    saving.close()
    save_data = ""
    saving = codecs.open('C:/Users/dongi/Desktop/min/save/_save_artist.txt', 'w', 'utf-8')
    for i in range(len(name_list)):
        save_data += artist_list[i] + "\n"
    saving.write(save_data[:-1])
    saving.close()
    save_data = ""
    saving = codecs.open('C:/Users/dongi/Desktop/min/save/_save_album.txt', 'w', 'utf-8')
    for i in range(len(name_list)):
        save_data += album_list[i] + "\n"
    saving.write(save_data[:-1])
    saving.close()
    e5.delete(0, len(e5.get()))
    e5.insert(0, 'export completed')


# 자동 보카로 입력기
def hotkey_input_1():
    e3.insert(0, '初音ミク')
def hotkey_input_2():
    e3.insert(0, '鏡音リン')
def hotkey_input_3():
    e3.insert(0, '/')
def hotkey_input_4():
    e3.insert(0, '鏡音レン')
def hotkey_input_5():
    e3.insert(0, '鏡音リン · レン')
def hotkey_input_6():
    e2.insert(0, ' - ')
def hotkey_input_7():
    e3.insert(0, 'GUMI')
def hotkey_input_8():
    e3.insert(0, 'IA')
def hotkey_input_9():
    e3.insert(0, 'v flower')
def hotkey_input_10():
    e3.insert(0, '巡音ルカ')
def hotkey_input_11():
    e3.insert(0, '結月ゆかり')
def hotkey_input_12():
    e3.insert(0, '小春六花')
def hotkey_input_13():
    e3.insert(0, '可不')
def hotkey_input_14():
    e3.insert(0, '歌愛ユキ')
def hotkey_input_15():
    e3.insert(0, 'MEIKO')
def hotkey_input_16():
    e3.insert(0, 'KAITO')
def hotkey_input_17():
    e3.insert(0, '音街ウナ')
def hotkey_input_18():
    e3.insert(0, '神威がくぽ')
def hotkey_input_19():
    e3.insert(0, '音街ウナ')
def hotkey_input_20():
    e3.insert(0, '神威がくぽ')


url_list = []
name_list = []
artist_list = []
album_list = []
bc = 2
this_is_dummy = 1
fnc_list = [rundo, listreset, tagging, downloading, dev, lyricwrite, in_txt, ex_txt]


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
e5.place(x=75, y=200)

# to line 50 ~
b001 = Button(window, text="정보 저장", command=save)
b002 = Button(window, text="리셋", command=reset)

b001.place(x=60, y=160)
b002.place(x=150, y=160)

b111 = Button(window, text="1개 취소", command=bc1)
b112 = Button(window, text="리스트 리셋", command=bc2)
b113 = Button(window, text="리스트 보기", command=seel)
b211 = Button(window, text="태그하기", command=bc3)
b212 = Button(window, text="다운로드", command=bc4)
b213 = Button(window, text="정리(재실행)", command=delx)
b311 = Button(window, text="dev", command=bc5)
b312 = Button(window, text="가사태그하기", command=bc6)
b411 = Button(window, text="불러오기", command=bc7)
b412 = Button(window, text="내보내기", command=bc8)

b111.place(x=10, y=230)
b112.place(x=80, y=230)
b113.place(x=170, y=230)
b211.place(x=10, y=260)
b212.place(x=80, y=260)
b213.place(x=170, y=260)
b311.place(x=10, y=290)
b312.place(x=80, y=290)
b411.place(x=10, y=320)
b412.place(x=80, y=320)

cv1 = IntVar()  # 버튼 체크시 1, 비 체크시 0
cb1 = Checkbutton(window, text="모드 vcl", variable=cv1, command=winres)
cb1.pack()
cb1.place(x=10, y=350)

bsp1 = Button(window, text="정보", command=pup2)
bsp1.place(x=150, y=350)

# to line 425 ~
b0211 = Button(window, text="初音ミク", command=hotkey_input_1)
b0212 = Button(window, text="鏡音リン", command=hotkey_input_2)
b0213 = Button(window, text="/", command=hotkey_input_3)
b0221 = Button(window, text="鏡音レン", command=hotkey_input_4)
b0222 = Button(window, text="鏡音リン · レン", command=hotkey_input_5)
b0223 = Button(window, text="* - ", command=hotkey_input_6)
b0231 = Button(window, text="GUMI", command=hotkey_input_7)
b0232 = Button(window, text="IA", command=hotkey_input_8)
b0241 = Button(window, text="v flower", command=hotkey_input_9)
b0242 = Button(window, text="巡音ルカ", command=hotkey_input_10)
b0251 = Button(window, text="結月ゆかり", command=hotkey_input_11)
b0252 = Button(window, text="小春六花", command=hotkey_input_12)
b0261 = Button(window, text="可不", command=hotkey_input_13)
b0262 = Button(window, text="歌愛ユキ", command=hotkey_input_14)
b0271 = Button(window, text="MEIKO", command=hotkey_input_15)
b0272 = Button(window, text="KAITO", command=hotkey_input_16)
b0281 = Button(window, text="音街ウナ", command=hotkey_input_17)
b0282 = Button(window, text="神威がくぽ", command=hotkey_input_18)
b0291 = Button(window, text="音街ウナ", command=hotkey_input_19)
b0292 = Button(window, text="神威がくぽ", command=hotkey_input_20)

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
