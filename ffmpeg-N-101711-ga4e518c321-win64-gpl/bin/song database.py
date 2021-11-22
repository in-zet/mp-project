# -*- coding: utf-8 -*-
import os
import glob
import eyed3
import youtube_dl
from tkinter import *
import mutagen
from mutagen.easyid3 import EasyID3
from mutagen.id3 import ID3, TIT2
from mutagen.mp4 import MP4Tags
from mutagen._file import *
import codecs
from pytube import YouTube
from moviepy.editor import *

urllist = []
namelist = []
artistlist = []
albumlist = []
bc = 2
this_is_dummy = 1

# ----------
# 이 프로젝트는 1차 실패하였습니다.
# 실패 이유 : MusicBee 이외의 프로그램에서의 재생 불가
# 추정 : youtube_dl 단계에서의 오류일 가능성이 높음
# 21.8.13 - 프로젝트 재가동중 (line 274; quality 320 -> 128, line 269; 주석 처리)
# 21.8.13 정상작동 확인(오류의 원인은 명확히 확보하지 못함, 아마도 line 269로 추정)
# 21.8.13 /v0.11/
# 21.10.22 /v0.2/
# 21.10.22 youtube-dll 의 속도저하 문제 해결 위한 pytube 모듈 도입
# ----------
# D:\python coding\ffmpeg-N-101711-ga4e518c321-win64-gpl\bin\song database.py
# ^ 베타 버전 -> 수정용
# D:\python coding\sdb\sd.py
# ^ 안정화 버전 -> 수정 X, 프로그램화 용
# * 안정될 때 복사하는 것 잊지 않기, 안정화 버전에서는 현재 사용되지 않는 [실험적] 코드 지우기
# ----------
# 중요 : python 파일이 있는 곳에 ffmpeg.exe 와 ffprobe.exe가 있어야지만 정상작동
# ----------
# [실험적]
# <정상작동>
# {오류 발생}

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
    global urllist
    global namelist
    global artistlist
    global albumlist
    urllist.append("https://www.youtube.com/watch?v=UnIhRpIT7nc")
    namelist.append("ラグトレイン")
    artistlist.append("歌愛ユキ")
    albumlist.append("稲葉曇")
    urllist.append("https://www.youtube.com/watch?v=e1xCOsgWG0M")
    namelist.append("ヴァンパイア")
    artistlist.append("初音ミク")
    albumlist.append("DECO*27")
    urllist.append("https://www.youtube.com/watch?v=emrt46SRyYs")
    namelist.append("DAYBREAK FRONTLINE")
    artistlist.append("IA")
    albumlist.append("Orangestar")
    urllist.append("https://www.youtube.com/watch?v=romqp_SB4tU")
    namelist.append("ノイローゼ")
    artistlist.append("v flower")
    albumlist.append("栗山夕璃")
    urllist.append("https://www.youtube.com/watch?v=ARt2fVT33Lw")
    namelist.append("SLoWMoTIoN")
    artistlist.append("初音ミク")
    albumlist.append("ピノキオピー")
    e5.delete(0, len(e5.get()))
    e5.insert(0, 'リストを確認してみて！')


# 리스트에 저장
def save():
    global urllist
    global namelist
    global artistlist
    global albumlist
    yturl = e1.get()
    filename = e2.get()
    artistn = e3.get()
    albumn = e4.get()
    e1.delete(0, len(e1.get()))
    e2.delete(0, len(e2.get()))
    e3.delete(0, len(e3.get()))
    e4.delete(0, len(e4.get()))
    e5.delete(0, len(e5.get()))

    isiticn = 0
    for i in range(len(f'{filename}')):
        if f'{filename[i]}' == '.' or f'{filename[i]}' == '/' or f'{filename[i]}' == '\\' or f'{filename[i]}' == ':' or f'{filename[i]}' == '*' or f'{filename[i]}' == '?' or f'{filename[i]}' == '"' or f'{filename[i]}' == '<' or f'{filename[i]}' == '>' or f'{filename[i]}' == '|' or f'{filename[i]}' == '%' or f'{filename[i]}' == '≒':
            isiticn = 1

    if yturl == None:
        e5.insert(0, 'incorrect youtube url')

    # [실험적]
    elif yturl == "vocaloid" or yturl == "vcl":
        vcl()

    elif filename == None:
        e5.insert(0, 'incorrect fliename')
    elif yturl == None:
        e5.insert(0, 'incorrect url')
    elif isiticn == 1:
        e5.insert(0, 'incorrent filename')
    else:
        urllist.append(yturl)
        namelist.append(filename)
        artistlist.append(artistn)
        albumlist.append(albumn)
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
    global n2window
    seelist = ""
    for i in range(len(namelist)):
        seelist += namelist[i] + " : " + urllist[i] + "\n"
    n2window = Toplevel(window)
    n2window.geometry('500x200')
    n2window.resizable(width=True, height=True)
    nl1 = Label(n2window, text=seelist)
    nl1.place(x=10, y=10)
    n2window.mainloop()


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


# info
def pup2():
    global nwindow2
    loading = codecs.open('C:/Users/dongi/Desktop/min/info.txt', 'rb', 'utf-8')
    loadedinfo = loading.read()
    loading.close()
    nwindow2 = Toplevel(window)
    nwindow2.geometry('300x300')
    nwindow2.resizable(width=True, height=True)
    nl1 = Label(nwindow2, text=loadedinfo)
    nl1.place(x=10, y=10)
    nwindow2.mainloop()


# '정말입니까' 에서 예
def isyes():
    global nwindow
    global bc
    nwindow.destroy()
    if bc == 1:
        rundo()
    elif bc == 2:
        listreset()
    elif bc == 3:
        tagging2()
    elif bc == 4:
        dl2()
    elif bc == 5:
        dev()
    elif bc == 6:
        lyricwrite1()
    elif bc == 7:
        in_txt()
    elif bc == 8:
        ex_txt()


# '정말입니까' 에서 아니오
def isno():
    global nwindow
    nwindow.destroy()


# 리스트 마지막 하나 없애기
def rundo():
    global urllist
    global namelist
    global artistlist
    global albumlist
    del urllist[-1]
    del namelist[-1]
    del artistlist[-1]
    del albumlist[-1]
    e5.delete(0, len(e5.get()))
    e5.insert(0, 'undo completed')


# 리스트 리셋
def listreset():
    global urllist
    global namelist
    global artistlist
    global albumlist
    urllist = []
    namelist = []
    artistlist = []
    albumlist = []
    e5.delete(0, len(e5.get()))
    e5.insert(0, 'list reset completed')


# [실험적]
# 태그 작성 1식
# Without id3 tags: 'NoneType' object has no attribute 'tag'
def tagging1():
    try:
        for i in range(len(namelist)):
            path1 = "C:/Users/dongi/Desktop/min/mp3/%s.mp3" % namelist[i]
            tag1 = eyed3.load(path1)
            tag1.initTag()  # 'NoneType' object has no attribute 'initTag'
            tag1.tag.artist = str(artistlist[i])
            tag1.tag.album = str(albumlist[i])
            tag1.tag.save()
        e5.delete(0, len(e5.get()))
        e5.insert(0, 'tagging completed')
    except Exception as e:
        e5.delete(0, len(e5.get()))
        e5.insert(0, 'error ' + str(e))


# <정상작동>
# 태그 작성 2식
# not using eyed3
def tagging2():  # currently using
    try:

        for i in range(len(namelist)):
            path1 = "C:/Users/dongi/Desktop/min/mp3/%s.mp3" % namelist[i]
            """tag11 = ID3(path1)
            tag11.add(TIT2(encording=3, text="1"))
            tag11.save()"""
            try:
                tag1 = EasyID3(path1)
            except mutagen.id3.ID3NoHeaderError:  # an MP4 tag already exists
                tag1 = mutagen.File(path1, easy=True)
                tag1.add_tags()
            if artistlist[i] != None:
                tag1['artist'] = str(artistlist[i])
            if albumlist[i] != None:
                tag1['album'] = str(albumlist[i])
            tag1.save(path1, v1=2)

            path1 = "C:/Users/dongi/Desktop/min/mp3/%s.mp3" % namelist[i]
            try:
                tag1 = EasyID3(path1)
            except mutagen.id3.ID3NoHeaderError:  # an MP4 tag already exists
                tag1 = mutagen.File(path1, easy=True)
                tag1.add_tags()
            if artistlist[i] != None:
                tag1['artist'] = str(artistlist[i])
            if albumlist[i] != None:
                tag1['album'] = str(albumlist[i])
            tag1.save(path1, v1=1)
        e5.delete(0, len(e5.get()))
        e5.insert(0, 'tagging completed')

    except Exception as e:
        e5.delete(0, len(e5.get()))
        e5.insert(0, 'error: ' + str(e))


# [실험적]
# 유튜브에서 노래 다운로드 - youtube_dll 1식 (속도 매우느림)
def dl():
    global urllist
    global namelist
    global artistlist
    global albumlist
    path_dir_mp3 = 'C:/Users/dongi/Desktop/min/mp3'
    path_dir_lyrics = 'C:/Users/dongi/Desktop/min/lyrics'
    mp3_list = os.listdir(path_dir_mp3)
    lyrics_list = os.listdir(path_dir_lyrics)
    isitagainm = 0
    isitagainl = 0

    try:
        for i in range(len(namelist)):
            for j in range(len(lyrics_list)):
                if namelist[i] == f'{lyrics_list[j][:-4]}':  # 중복가사파일확인
                    isitagainl = 1

            if isitagainl == 0:
                _ = open("C:/Users/dongi/Desktop/min/lyrics/%s.txt" % namelist[i], 'w')
            elif isitagainl == 1:
                isitagainl = 0
                print("\n%s lyric file skipped\n" % namelist[i])

        for i in range(len(namelist)):
            for j in range(len(mp3_list)):
                if namelist[i] == f'{mp3_list[j][:-4]}':  # 중복음악파일확인
                    isitagainm = 1

            if isitagainm == 0:
                download_path = "C:/Users/dongi/Desktop/min/mp3/%s" % namelist[i]
                url1 = urllist[i]

                print("\n%s" % namelist[i])  # checking in console
                print("%s\n" % url1)

                ydl_opts = {
                    # 'format': 'bestaudio/best', -> 오류의 원인으로 추정됨
                    'outtmpl': download_path,
                    'postprocessors': [{
                        'key': 'FFmpegExtractAudio',
                        'preferredcodec': 'mp3',
                        'preferredquality': '128',
                    }],
                }
                with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                    ydl.download([url1])

            elif isitagainm == 1:
                isitagainm = 0
                print("\n%s mp3 file skipped\n" % namelist[i])

        e5.delete(0, len(e5.get()))
        e5.insert(0, 'downloded')
        print("\nFIN\n")

    except Exception as e:
        e5.delete(0, len(e5.get()))
        e5.insert(0, 'error: ' + str(e))


# <정상작동>
# 유튜브에서 노래 다운로드 - pytube 2식
def dl2():
    global urllist
    global namelist
    global artistlist
    global albumlist
    path_dir_mp3 = 'C:/Users/dongi/Desktop/min/mp3'
    path_dir_lyrics = 'C:/Users/dongi/Desktop/min/lyrics'
    mp3_list = os.listdir(path_dir_mp3)
    lyrics_list = os.listdir(path_dir_lyrics)
    isitagainm = 0
    isitagainl = 0

    try:
        for i in range(len(namelist)):
            for j in range(len(lyrics_list)):
                if namelist[i] == f'{lyrics_list[j][:-4]}':  # 중복가사파일확인
                    isitagainl = 1

            if isitagainl == 0:
                _ = open("C:/Users/dongi/Desktop/min/lyrics/%s.txt" % namelist[i], 'w')
            elif isitagainl == 1:
                isitagainl = 0
                print("\n%s lyric file skipped\n" % namelist[i])

        for i in range(len(namelist)):
            for j in range(len(mp3_list)):
                if namelist[i] == f'{mp3_list[j][:-4]}':  # 중복음악파일확인
                    isitagainm = 1

            if isitagainm == 0:
                download_path = "C:/Users/dongi/Desktop/min/mp3/%s" % namelist[i]
                url1 = urllist[i]

                print("\n%s" % namelist[i])  # checking in console
                print("%s\n" % url1)

                yt = YouTube(url1)
                #yt.streams.filter(only_audio=True).all()  .filter(only_audio=True)
                yt.streams.filter(progressive=True, file_extension='mp4').order_by('resolution').desc().first().download(path_dir_mp3, "C:/Users/dongi/Desktop/min/mp3/%s.mp4" % namelist[i])

                vv = VideoFileClip(os.path.join("C:/Users/dongi/Desktop/min/mp3", "C:/Users/dongi/Desktop/min/mp3", "C:/Users/dongi/Desktop/min/mp3/%s.mp4" % namelist[i]))
                vv.audio.write_audiofile(os.path.join("C:/Users/dongi/Desktop/min/mp3", "C:/Users/dongi/Desktop/min/mp3", "C:/Users/dongi/Desktop/min/mp3/%s.mp3" % namelist[i]))

                """
                try:   # 추정: 헤더가 바뀌지 않고 확장자만 바뀌어서 문제 생김
                    os.rename("C:/Users/dongi/Desktop/min/mp3/%s.mp4" % namelist[i], "C:/Users/dongi/Desktop/min/mp3/%s.mp3" % namelist[i])
                except Exception as e:
                    e5.delete(0, len(e5.get()))
                    e5.insert(0, 'error: ' + str(e))
                    return
                    """

            elif isitagainm == 1:
                isitagainm = 0
                print("\n%s mp3 file skipped\n" % namelist[i])

        e5.delete(0, len(e5.get()))
        e5.insert(0, 'downloded')
        print("\nFIN\n")

    except Exception as e:
        e5.delete(0, len(e5.get()))
        e5.insert(0, 'error: ' + str(e))


def delx():
    global namelist
    path_dir_mp3 = 'C:/Users/dongi/Desktop/min/mp3'
    try:
        for i in range(len(namelist)):
            os.remove("C:/Users/dongi/Desktop/min/mp3/%s.mp4" % namelist[i])
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
    print(urllist)
    print(namelist)
    print(artistlist)
    print(albumlist)
    """[os.remove(f) for f in glob.glob("C:/Users/dongi/Desktop/min/mp3/*.mp3")]
    [os.remove(f) for f in glob.glob("C:/Users/dongi/Desktop/min/lyrics/*.txt")]"""
    e5.delete(0, len(e5.get()))
    e5.insert(0, 'dev')


# <정상작동>
# 가사 작성 1식
# Without id3 tags: 'NoneType' object has no attribute 'tag'
def lyricwrite1():  # currently using
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
            tg1 = eyed3.load(mp3path)
            ln1 = codecs.open(lyricspath, 'r', 'utf-8')
            lyr1 = ln1.read()
            tg1.tag.lyrics.set(lyr1)
            tg1.tag.save()
            ln1.close()
            e5.delete(0, len(e5.get()))
            e5.insert(0, 'lyric completed')

    elif len(mp3_list) == len(lyrics_list):
        for i in range(len(mp3_list)):
            mp3path = 'C:/Users/dongi/Desktop/min/mp3/' + mp3_list[i]
            lyricspath = 'C:/Users/dongi/Desktop/min/lyrics/' + lyrics_list[i]
            tg1 = eyed3.load(mp3path)
            ln1 = codecs.open(lyricspath, 'r', 'utf-8')
            lyr1 = ln1.read()
            tg1.tag.lyrics.set(lyr1)
            tg1.tag.save()
            ln1.close()
            e5.delete(0, len(e5.get()))
            e5.insert(0, 'lyric completed')
    else:
        e5.delete(0, len(e5.get()))
        e5.insert(0, 'the number of mp3s and lyrics are not same')


# [실험적]
# 가사 작성 2식
# not using eyed3
def lyricwrite2():
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


# <정상작동>
# 정보 불러오기
def in_txt():
    global urllist
    global namelist
    global artistlist
    global albumlist
    urllist = []
    namelist = []
    artistlist = []
    albumlist = []
    loading = codecs.open('C:/Users/dongi/Desktop/min/save/_save_url.txt', 'rb', 'utf-8')
    urllist = loading.read().split('\n')
    loading.close()
    loading = codecs.open('C:/Users/dongi/Desktop/min/save/_save_name.txt', 'rb', 'utf-8')
    namelist = loading.read().split('\n')
    loading.close()
    loading = codecs.open('C:/Users/dongi/Desktop/min/save/_save_artist.txt', 'rb', 'utf-8')
    artistlist = loading.read().split('\n')
    loading.close()
    loading = codecs.open('C:/Users/dongi/Desktop/min/save/_save_album.txt', 'rb', 'utf-8')
    albumlist = loading.read().split('\n')
    loading.close()
    if len(urllist) != len(namelist) or len(namelist) != len(artistlist) or len(artistlist) != len(albumlist) or len(urllist) != len(albumlist):
        e5.delete(0, len(e5.get()))
        e5.insert(0, 'error : different lines')
        urllist = []
        namelist = []
        artistlist = []
        albumlist = []
    else:
        e5.delete(0, len(e5.get()))
        e5.insert(0, 'import completed')


# <정상작동>
# 정보 내보내기
def ex_txt():
    global urllist
    global namelist
    global artistlist
    global albumlist
    save_data = ""
    saving = codecs.open('C:/Users/dongi/Desktop/min/save/_save_url.txt', 'w', 'utf-8')
    for i in range(len(namelist) - 1):
        save_data += urllist[i] + "\n"
    save_data += urllist[-1]
    saving.write(save_data)
    saving.close()
    save_data = ""
    saving = codecs.open('C:/Users/dongi/Desktop/min/save/_save_name.txt', 'w', 'utf-8')
    for i in range(len(namelist) - 1):
        save_data += namelist[i] + "\n"
    save_data += namelist[-1]
    saving.write(save_data)
    saving.close()
    save_data = ""
    saving = codecs.open('C:/Users/dongi/Desktop/min/save/_save_artist.txt', 'w', 'utf-8')
    for i in range(len(namelist) - 1):
        save_data += artistlist[i] + "\n"
    save_data += artistlist[-1]
    saving.write(save_data)
    saving.close()
    save_data = ""
    saving = codecs.open('C:/Users/dongi/Desktop/min/save/_save_album.txt', 'w', 'utf-8')
    for i in range(len(namelist) - 1):
        save_data += albumlist[i] + "\n"
    save_data += albumlist[-1]
    saving.write(save_data)
    saving.close()
    e5.delete(0, len(e5.get()))
    e5.insert(0, 'export completed')


# 자동 보카로 입력기
def miku():
    e3.insert(0, '初音ミク')
def rin():
    e3.insert(0, '鏡音リン')
def slash():
    e3.insert(0, '/')
def Len():
    e3.insert(0, '鏡音レン')
def rin_len():
    e3.insert(0, '鏡音リン · レン')
def dash():
    e2.insert(0, ' - ')
def gumi():
    e3.insert(0, 'GUMI')
def ia():
    e3.insert(0, 'IA')
def flower():
    e3.insert(0, 'v flower')
def luka():
    e3.insert(0, '巡音ルカ')
def yukari():
    e3.insert(0, '結月ゆかり')
def rikka():
    e3.insert(0, '小春六花')
def kahu():
    e3.insert(0, '可不')
def yuki():
    e3.insert(0, '歌愛ユキ')
def meiko():
    e3.insert(0, 'MEIKO')
def kaito():
    e3.insert(0, 'KAITO')
def una():
    e3.insert(0, '音街ウナ')
def gakupo():
    e3.insert(0, '神威がくぽ')


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
b0211 = Button(window, text="初音ミク", command=miku)
b0212 = Button(window, text="鏡音リン", command=rin)
b0213 = Button(window, text="/", command=slash)
b0221 = Button(window, text="鏡音レン", command=Len)
b0222 = Button(window, text="鏡音リン · レン", command=rin_len)
b0223 = Button(window, text="* - ", command=dash)
b0231 = Button(window, text="GUMI", command=gumi)
b0232 = Button(window, text="IA", command=ia)
b0241 = Button(window, text="v flower", command=flower)
b0242 = Button(window, text="巡音ルカ", command=luka)
b0251 = Button(window, text="結月ゆかり", command=yukari)
b0252 = Button(window, text="小春六花", command=rikka)
b0261 = Button(window, text="可不", command=kahu)
b0262 = Button(window, text="歌愛ユキ", command=yuki)
b0271 = Button(window, text="MEIKO", command=meiko)
b0272 = Button(window, text="KAITO", command=kaito)
b0281 = Button(window, text="音街ウナ", command=una)
b0282 = Button(window, text="神威がくぽ", command=gakupo)

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

try:
    in_txt()
except:
    True
window.mainloop()
