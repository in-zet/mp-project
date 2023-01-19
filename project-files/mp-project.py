# -*- coding: utf-8 -*-
import codecs
import json
import os
import random
import shlex
import subprocess
from functools import partial
from tkinter import *
from tkinter import ttk
from tkinter.filedialog import askdirectory

import clipboard
from mutagen.easyid3 import EasyID3
from mutagen.id3 import ID3, TIT2, TALB, TPE1, TPE2, COMM, TCOM, TCON, TDRC, TRCK
from niconico import NicoNico
from pytube import YouTube

###################################################
# 21.03.25 /v0.0.1/ : 프로젝트 시작
# 21.03.26 /v0.0.2/ : 프로젝트 폐기 - 작동불능
# 21.08.13 /v0.0.3/ : 프로젝트 재가동중 - 정상작동 확인
#
# 21.10.22 /v0.1.0/ : youtube-dll 의 속도저하 문제 해결 위한 pytube 모듈 도입  // 백업
# 21.11.22 /v0.1.1/ : Github에 업로드
#
# 21.12.04 /v0.2.0/ : 코드 최적화, mp4 폴더 분리, 변수 이름 변경, eyed3 사용 중지 및 제거
# 22.03.11 /v0.2.1/ : pytube 버전 업 (0.11.2 -> 0.12)
# 22.07.26 /v0.2.2/ : mp4 삭제 안되는 오류 해결 - 왜 되는지 모름 - 안됨
#
# 22.07.27 /v0.3.0/ : 다른 환경에서도 작동 가능성 확보 // 백업
#
# 22.08.01 /v0.4.0/ : 니코동 지원, %s 대신 f'{}' 사용 시작
# 22.08.03 /v0.4.1/ : mp4 삭제 안되는 오류 해결 - time.sleep(0.3)으로 해결(?) // 백업
#
# 22.08.04 /v0.5.0/ : 클립보드에서 붙여넣기, 줄 단위 삭제 버튼 추가
#
# 22.08.05 /v0.6.0/ : moviepy 버리고 ffmpeg로 갈아탐, 음질 및 화질 개선 - ffmpeg가 안꺼지는 문제 재발 - 해결(communicate())
# 22.10.13 /v0.6.1/ : 텅 빈 파일 인식으로부터 비롯된 버그 제거, \n이 같이 입력되지 않게 처리 // 백업
# 22.10.14 /v0.6.2/ : 입력 불가능한 글자를 입력하면 자동으로 전각으로 바뀌게 함
# 23.01.04 /v0.6.3/ : 단축키 사용 시 앞에 문자열이 삽입되는 버그 제거 // 백업
#
# 23.01.13 /v1.0.0/ : UI 대폭 개선, 코드 리포매팅(Black), 기능 분리 -> 메뉴화, 태깅 로직 개선, 태그 종류 추가, 리스트 조작 추가,
#                     mp3 변환 로직 수정, 경로 설정 개선, 자료 저장 개선 -> json 도입, 불필요 기능 삭제, 버그 수정, 핫키 분리,
#                     핫키 무제한화
# 23.01.14 /v1.0.1/ : 리포매팅(yield문 제거 -> partial() 사용)
#
###################################################
# 중요 : python 파일이 있는 곳에 ffmpeg.exe 와 ffprobe.exe가 있어야지만 정상작동
###################################################


########################################################################################################################
#####################################################                ###################################################
#####################################################    기초 셋팅    ####################################################
#####################################################                ###################################################
########################################################################################################################


current_version = (1, 0, 0)
list_mode = 0
selected_index = -1

path = os.getcwd().replace("\\", "/")
settings = {
    "ismp3": 1,
    "ismp4": 0,
    "playlistmode": 0,
    "splitmode": 0,
    "tags": ["artist", "album", "composer"],
    "hotkeys": [],
}
properties = []
property_str_list = [
    "title",
    "artist",
    "band",
    "album",
    "comment",
    "year",
    "track",
    "genre",
    "composer",
    "timing",
]
# url, filename, title, artist, band, album, comment, year: int, track: int, genre, composer, timing


def enformat(content: str) -> str:
    if content == "":
        return f"__No_Title_{random.randint(1000, 9999)}__"
    return (
        content.replace(" ", "__sb__")
        .replace(".", "__pe__")
        .replace("'", "__qu__")
        .replace("\n", "")
    )


def deformat(content: str) -> str:
    return content.replace("__sb__", " ").replace("__pe__", ".").replace("__qu__", "'")


def msg(content: str, index: int = 0) -> None:
    ei.delete(index, len(ei.get()))
    ei.insert(index, content)


def window_set(
    window: Tk or Toplevel, geomatry: str, title: str, resizable: bool = False
) -> None:
    window.geometry(geomatry)
    window.title(title)
    window.resizable(resizable, resizable)


def mouse_track(window: Tk or Toplevel) -> None:
    window.bind("<Motion>", lambda e: print("(%d, %d)" % (e.x, e.y)))


########################################################################################################################
######################################################               ###################################################
######################################################    다운로드    ###################################################
######################################################               ###################################################
########################################################################################################################


def downloading():  # mp3 / mp4 파일 다운로드
    global properties
    client = NicoNico()
    mp3_list = os.listdir(f"{path}/min/mp3")
    mp4_list = os.listdir(f"{path}/min/mp4")

    try:
        for i in properties:  # 각각의 곡 마다 실행
            fname = enformat(i["filename"])
            print(f"\n{properties.index(i) + 1} / {len(properties)}")

            if "youtube" in i["url"]:  # 유튜브에서 다운로드
                print(f'\n{i["filename"]}\n{i["url"]}\n')

                yt = YouTube(i["url"])

                if (
                    settings["ismp4"]
                    and f'{i["filename"]}.mp4' not in mp4_list
                    and f"{fname}.mp4" not in mp4_list
                ):
                    yt.streams.filter(only_video=True).order_by(
                        "resolution"
                    ).desc().first().download(None, f"{path}/min/mp4/{fname}_video.mp4")
                    yt.streams.filter(only_audio=True).order_by(
                        "abr"
                    ).desc().first().download(None, f"{path}/min/mp4/{fname}_audio.mp4")

                    command = f"ffmpeg -y -i {path}/min/mp4/{fname}_video.mp4 -i {path}/min/mp4/{fname}_audio.mp4 {path}/min/mp4/{fname}.mp4"
                    p = subprocess.Popen(
                        shlex.split(command),
                        stdout=subprocess.PIPE,
                        stderr=subprocess.PIPE,
                    )
                    p.communicate()

                    print(f'{i["filename"]} video downloaded')

                    if (
                        settings["ismp3"]
                        and f'{i["filename"]}.mp3' not in mp3_list
                        and f"{fname}.mp3" not in mp3_list
                    ):
                        command = f"ffmpeg -i {path}/min/mp4/{fname}_audio.mp4 -y {path}/min/mp3/{fname}.mp3"
                        p = subprocess.Popen(
                            shlex.split(command),
                            stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE,
                        )
                        p.communicate()

                        print(f'{i["filename"]} audio downloaded')

                elif (
                    settings["ismp3"]
                    and f'{i["filename"]}.mp3' not in mp3_list
                    and f"{fname}.mp3" not in mp3_list
                ):
                    yt.streams.filter(only_audio=True).order_by(
                        "abr"
                    ).desc().first().download(None, f"{path}/min/mp4/{fname}_audio.mp4")

                    command = f"ffmpeg -i {path}/min/mp4/{fname}_audio.mp4 -y {path}/min/mp3/{fname}.mp3"
                    p = subprocess.Popen(
                        shlex.split(command),
                        stdout=subprocess.PIPE,
                        stderr=subprocess.PIPE,
                    )
                    p.communicate()

                    print(f'{i["filename"]} audio downloaded')

            elif "nicovideo" in i["url"]:  # 니코동에서 다운로드
                print(f'\n{i["filename"]}\n{i["url"]}\n')

                if (settings["ismp4"] and f'{i["filename"]}.mp4' not in mp4_list) or (
                    settings["ismp3"] and f'{i["filename"]}.mp3' not in mp3_list
                ):
                    with client.video.get_video(i["url"]) as ni:
                        ni.download(f"{path}/min/mp4/{fname}.mp4")

                    print(f'{i["filename"]} video downloaded')

                    if settings["ismp3"] and f'{i["filename"]}.mp3' not in mp3_list:
                        command = f"ffmpeg -i {path}/min/mp4/{fname}.mp4 -y {path}/min/mp3/{fname}.mp3"
                        p = subprocess.Popen(
                            shlex.split(command),
                            stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE,
                        )
                        p.communicate()

                        print(f'{i["filename"]} audio downloaded')

            else:  # 유튜브, 니코동 둘 다 아닐 때
                print(f'{i["url"]} is a wrong path')

            if "timing" in list(i.keys()):  # 타이밍 값이 있어서 자르게 될 경우
                times = [j.split(":") for j in i["timing"].split("-")]
                if len(times) == 1:
                    if i["timing"][0] == "-":
                        times.insert(0, ["0", "00", "00"])

                for j in times:
                    while len(j) < 3:
                        j.insert(0, "0")
                    for k in range(1, 3):
                        if len(j[k]) == 1:
                            j[k] = "0" + str(j[k])

                if settings["ismp3"] == 1:
                    os.rename(
                        f"{path}/min/mp3/{fname}.mp3",
                        f"{path}/min/mp3/{fname}_orginal.mp3",
                    )

                    try:
                        command = f"ffmpeg -i {path}/min/mp3/{fname}_orginal.mp3 -ss {times[0][0]}:{times[0][1]}:{times[0][2]} -to {times[1][0]}:{times[1][1]}:{times[1][2]} -c copy {path}/min/mp3/{fname}.mp3"
                        p = subprocess.Popen(
                            shlex.split(command),
                            stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE,
                        )
                        p.communicate()

                    except Exception as e:
                        print(f"\nerror: {e}\n")
                        p.communicate()
                        if f"{path}/min/mp3/{fname}.mp3" in os.listdir(
                            f"{path}/min/mp3"
                        ):
                            os.remove(f"{path}/min/mp3/{fname}.mp3")
                        os.rename(
                            f"{path}/min/mp3/{fname}_orginal.mp3",
                            f"{path}/min/mp3/{fname}.mp3",
                        )

                if settings["ismp4"] == 1:
                    os.rename(
                        f"{path}/min/mp4/{fname}.mp4",
                        f"{path}/min/mp4/{fname}_orginal.mp4",
                    )

                    try:
                        command = f"ffmpeg -i {path}/min/mp4/{fname}_orginal.mp4 -ss {times[0][0]}:{times[0][1]}:{times[0][2]} -to {times[1][0]}:{times[1][1]}:{times[1][2]} {path}/min/mp4/{fname}.mp4"
                        p = subprocess.Popen(
                            shlex.split(command),
                            stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE,
                        )
                        p.communicate()

                    except Exception as e:
                        print(f"\nerror: {e}\n")
                        p.communicate()
                        if f"{path}/min/mp4/{fname}.mp4" in os.listdir(
                            f"{path}/min/mp4"
                        ):
                            os.remove(f"{path}/min/mp4/{fname}.mp4")
                        os.rename(
                            f"{path}/min/mp4/{fname}_orginal.mp4",
                            f"{path}/min/mp4/{fname}.mp4",
                        )

        for i in os.listdir(f"{path}/min/mp4"):  # 사용된 비디오만 / 오디오만 / 자르지 않은 파일 삭제
            if "_audio" in i or "_video" in i or "_orginal" in i:
                os.remove(f"{path}/min/mp4/{i}")
        for i in os.listdir(f"{path}/min/mp3"):
            if "_orginal" in i:
                os.remove(f"{path}/min/mp3/{i}")

        for i in os.listdir(f"{path}/min/mp4"):  # 공백, 온점 되돌리기
            os.rename(f"{path}/min/mp4/{i}", f"{path}/min/mp4/{deformat(i)}")
        for i in os.listdir(f"{path}/min/mp3"):
            os.rename(f"{path}/min/mp3/{i}", f"{path}/min/mp3/{deformat(i)}")

        if settings["ismp4"] == 0:  # mp4 파일 미필요
            for i in properties:  # mp4 파일 삭제
                try:
                    os.remove(f'{path}/min/mp4/{i["filename"]}.mp4')
                except:
                    pass

        tagging()

        msg("Completed")
        print("\nCompleted\n")

    except Exception as e:
        print(f"\nerror: {e}\n")
        msg(f"error: {e}")


def mp4_all_delete():  # mp3 / mp4 파일 일괄 삭제
    try:
        for i in os.listdir(f"{path}/min/mp4"):
            os.remove(f"{path}/min/mp4/{i}")
        for i in os.listdir(f"{path}/min/mp3"):
            os.remove(f"{path}/min/mp3/{i}")
        msg("MP4/MP3 file deleted")

    except Exception as e:
        print(f"\nerror: {e}\n")
        msg(f"error: {e}")


########################################################################################################################
######################################################           #######################################################
######################################################    태그    #######################################################
######################################################           #######################################################
########################################################################################################################


def tagging():  # mp3 파일 태그
    global settings

    try:
        for i in properties:
            if f'{i["filename"]}.mp3' in os.listdir(f"{path}/min/mp3"):
                tags = ID3(f'{path}/min/mp3/{i["filename"]}.mp3')
                tags.delete()
                tags = ID3()

                if "title" in i.keys():
                    tags["TIT2"] = TIT2(encoding=3, text=i["title"])

                if "album" in i.keys():
                    tags["TALB"] = TALB(encoding=3, text=i["album"])

                if "band" in i.keys():
                    tags["TPE2"] = TPE2(encoding=3, text=i["band"])

                if "comment" in i.keys():
                    tags["COMM"] = COMM(encoding=3, text=i["comment"])
                    # tags["COMM"] = COMM(encoding=3, lang=u'eng', desc='desc', text=i["title"])

                if "artist" in i.keys():
                    tags["TPE1"] = TPE1(encoding=3, text=i["artist"])

                if "composer" in i.keys():
                    tags["TCOM"] = TCOM(encoding=3, text=i["composer"])

                if "genre" in i.keys():
                    tags["TCON"] = TCON(encoding=3, text=i["genre"])

                if "year" in i.keys():
                    tags["TDRC"] = TDRC(encoding=3, text=i["year"])

                if "track" in i.keys():
                    tags["TRCK"] = TRCK(encoding=3, text=i["track"])

                tags.save(f'{path}/min/mp3/{i["filename"]}.mp3')

        msg("tagging completed")

    except Exception as e:
        print(f"\nerror: {e}\n")
        msg(f"error: {e}")


def lyric_tagging():  # mp3 파일 가사 태그
    global settings

    mp3_list = os.listdir(f"{path}/min/mp3")
    lyrics_list = os.listdir(f"{path}/min/lyrics")

    if len(mp3_list) <= len(lyrics_list):  # mp3 파일과 가사 파일의 수가 정상
        for i in range(len(mp3_list)):
            for j in range(len(lyrics_list)):
                if f"{mp3_list[i][:-4]}" == f"{lyrics_list[j][:-4]}":
                    tag1 = EasyID3(f"{path}/min/mp3/{mp3_list[i]}")
                    ln1 = open(f"{path}/min/lyrics/{lyrics_list[j]}", "r")
                    lyr1 = ln1.read()
                    ln1.close()
                    tag1["lyricist"] = str(lyr1)
                    tag1.save(f"{path}/min/mp3/{mp3_list[i]}", v1=2)

            msg("lyric completed")

    else:
        msg("the number of mp3s and lyrics are not same")


########################################################################################################################
#################################################                      #################################################
#################################################    불러오기/내보내기    #################################################
#################################################                      #################################################
########################################################################################################################


def in_txt():  # 작업 리스트 불러오기
    global properties
    try:
        with open(f"{path}/min/savelist.json") as f:
            properties = json.load(f)
        msg("List Imported")

    except Exception as e:
        print(f"\nerror: {e}\n")


def ex_txt():  # 작업 리스트 내보내기
    try:
        with open(f"{path}/min/savelist.json", "w") as f:
            json.dump(properties, f, indent=2)
        msg("List Exported")

    except Exception as e:
        print(f"\nerror: {e}\n")


def in_settings():  # 설정 불러오기
    global settings
    try:
        with open(f"{path}/min/settings.json") as f:
            settings = json.load(f)

    except Exception as e:
        print(f"\nerror: {e}\n")


def ex_settings():  # 설정 내보내기
    try:
        with open(f"{path}/min/settings.json", "w") as f:
            json.dump(settings, f, indent=2)

    except Exception as e:
        print(f"\nerror: {e}\n")


########################################################################################################################
######################################################           #######################################################
######################################################    설정    #######################################################
######################################################           #######################################################
########################################################################################################################


def settings_open():  # 설정 창
    global settings, path

    try:
        window.destroy()  # 메인루프 창 파괴
    except:
        pass

    setting_window = Tk()
    window_set(setting_window, "250x260", "설정")

    def apply():  # 확정 시 - 쓰여진 정보 저장
        global path
        path = str(ee1.get()).replace("\\", "/")
        settings["ismp3"] = int(ee3.get())
        settings["ismp4"] = int(ee4.get())
        settings["playlistmode"] = int(ee5.get())
        settings["splitmode"] = int(ee6.get())

        setting_window.destroy()
        main_loop()  # 다시 메인루프로

    Label(setting_window, text="경로:").place(x=5, y=5)

    ee1 = ttk.Entry(setting_window, width=28)
    ee1.place(x=40, y=5)

    ee3 = IntVar()
    ev3 = ttk.Checkbutton(setting_window, text="음원", variable=ee3)
    ev3.place(x=130, y=60)

    ee4 = IntVar()
    ev4 = ttk.Checkbutton(setting_window, text="영상", variable=ee4)
    ev4.place(x=130, y=80)

    def ev5_rev():
        if ee5.get() and ee6.get():
            ev6.invoke()

    def ev6_rev():
        if ee6.get() and ee5.get():
            ev5.invoke()

    ee5 = IntVar()
    ev5 = ttk.Checkbutton(
        setting_window, text="재생목록 모드", variable=ee5, command=lambda: ev5_rev()
    )
    ev5.place(x=130, y=120)

    ee6 = IntVar()
    ev6 = ttk.Checkbutton(
        setting_window, text="분할 모드", variable=ee6, command=lambda: ev6_rev()
    )
    ev6.place(x=130, y=140)

    def add_tags(x, objection):
        global settings
        if off != 1:
            if x.get() == 1:
                settings["tags"].append(objection)
            elif x.get() == 0:
                settings["tags"].remove(objection)

    off = 1

    ete1 = IntVar()
    ete2 = IntVar()
    ete3 = IntVar()
    ete4 = IntVar()
    ete5 = IntVar()
    ete6 = IntVar()
    ete7 = IntVar()
    ete8 = IntVar()
    ete9 = IntVar()
    ete10 = IntVar()

    et1 = ttk.Checkbutton(
        setting_window,
        text="title",
        variable=ete1,
        command=lambda: add_tags(ete1, "title"),
    )
    et2 = ttk.Checkbutton(
        setting_window,
        text="artist",
        variable=ete2,
        command=lambda: add_tags(ete2, "artist"),
    )
    et3 = ttk.Checkbutton(
        setting_window,
        text="band",
        variable=ete3,
        command=lambda: add_tags(ete3, "band"),
    )
    et4 = ttk.Checkbutton(
        setting_window,
        text="album",
        variable=ete4,
        command=lambda: add_tags(ete4, "album"),
    )
    et5 = ttk.Checkbutton(
        setting_window,
        text="comment",
        variable=ete5,
        command=lambda: add_tags(ete5, "comment"),
    )
    et6 = ttk.Checkbutton(
        setting_window,
        text="year",
        variable=ete6,
        command=lambda: add_tags(ete6, "year"),
    )
    et7 = ttk.Checkbutton(
        setting_window,
        text="track",
        variable=ete7,
        command=lambda: add_tags(ete7, "track"),
    )
    et8 = ttk.Checkbutton(
        setting_window,
        text="genre",
        variable=ete8,
        command=lambda: add_tags(ete8, "genre"),
    )
    et9 = ttk.Checkbutton(
        setting_window,
        text="composer",
        variable=ete9,
        command=lambda: add_tags(ete9, "composer"),
    )
    et10 = ttk.Checkbutton(
        setting_window,
        text="timing",
        variable=ete10,
        command=lambda: add_tags(ete10, "timing"),
    )

    et1.place(x=20, y=40)
    et2.place(x=20, y=60)
    et3.place(x=20, y=80)
    et4.place(x=20, y=100)
    et5.place(x=20, y=120)
    et6.place(x=20, y=140)
    et7.place(x=20, y=160)
    et8.place(x=20, y=180)
    et9.place(x=20, y=200)
    et10.place(x=20, y=220)

    et_list = [et1, et2, et3, et4, et5, et6, et7, et8, et9, et10]

    def import_reload():
        in_settings()
        setting_window.destroy()
        settings_open()

    def find_path():
        choosepath()
        ee1.delete(0, len(ee1.get()))
        ee1.insert(0, path)

    ttk.Button(setting_window, text="찾기", command=find_path).place(x=150, y=30)
    ttk.Button(setting_window, text="저장", command=apply).place(x=140, y=220)

    menubar = Menu(setting_window)
    menu_1 = Menu(menubar, tearoff=0)
    menu_1.add_command(label="설정불러오기", command=import_reload)
    menu_1.add_command(label="설정내보내기", command=ex_settings)
    menubar.add_cascade(label="파일", menu=menu_1)

    setting_window.config(menu=menubar)

    ee1.insert(0, path)
    if settings["ismp3"] == 1:
        ev3.invoke()
    if settings["ismp4"] == 1:
        ev4.invoke()
    if settings["playlistmode"] == 1:
        ev5.invoke()
    elif settings["splitmode"] == 1:
        ev6.invoke()

    for i in settings["tags"]:
        et_list[property_str_list.index(i)].invoke()

    off = 0

    setting_window.mainloop()


########################################################################################################################
######################################################             #####################################################
######################################################    리스트    #####################################################
######################################################             #####################################################
########################################################################################################################


def save():  # 정보 저장
    global properties, selected_index
    if list_mode == 0:
        properties.append({})

    url = e1.get().replace("\n", "")
    if url != "":
        properties[selected_index]["url"] = url
    else:
        msg("incorrect youtube url")
        return

    if e2.get() != "":
        properties[selected_index]["filename"] = (
            e2.get()
            .replace("\n", "")
            .replace("/", "／")
            .replace("\\", "＼")
            .replace(":", "：")
            .replace("*", "＊")
            .replace("?", "？")
            .replace('"', "＂")
            .replace("<", "＜")
            .replace(">", "＞")
            .replace("|", "｜")
        )
    else:
        try:
            properties[selected_index]["filename"] = (
                YouTube(url)
                .title.replace("\n", "")
                .replace("/", "／")
                .replace("\\", "＼")
                .replace(":", "：")
                .replace("*", "＊")
                .replace("?", "？")
                .replace('"', "＂")
                .replace("<", "＜")
                .replace(">", "＞")
                .replace("|", "｜")
            )
        except:
            properties[selected_index][
                "filename"
            ] = f"__No_Title_{str(random.randint(0, 9)) + str(random.randint(0, 9)) + str(random.randint(0, 9)) + str(random.randint(0, 9))}__"

    for i in range(len(settings["tags"])):
        if e_list[i + 2].get() != "":
            properties[selected_index][settings["tags"][i]] = (
                e_list[i + 2].get().replace("\n", "")
            )

    properties[selected_index]["playlist"] = cbv1.get()
    properties[selected_index]["split"] = cbv2.get()

    if list_mode == 1:
        e2.config(values=[i["filename"] for i in properties])
    else:
        for i in e_list:
            i.delete(0, len(i.get()))

    msg(f"saved - {properties[selected_index]['filename']}")


def vcl():  # for test
    global properties
    properties = [
        {
            "url": "https://www.youtube.com/watch?v=UnIhRpIT7nc",
            "filename": "ラグトレイン",
            "artist": "歌愛ユキ",
            "composer": "稲葉曇",
        },
        {
            "url": "https://www.youtube.com/watch?v=emrt46SRyYs",
            "filename": "DAYBREAK FRONTLINE",
            "artist": "IA",
            "composer": "Orangestar",
        },
        {
            "url": "https://www.nicovideo.jp/watch/sm23648996",
            "filename": "SLoWMoTIoN",
            "artist": "初音ミク",
            "composer": "ピノキオピー",
        },
        {
            "url": "https://www.youtube.com/watch?v=e1xCOsgWG0M",
            "filename": "ヴァンパイア",
            "artist": "初音ミク",
            "composer": "DECO*27",
        },
    ]

    msg("リストを確認してみて！")


def reset():
    e1.delete(0, len(e1.get()))
    e2.delete(0, len(e2.get()))
    for i in e_list:
        i.delete(0, len(i.get()))
    msg("clear")


########################################################################################################################
########################################################          ######################################################
########################################################    창    ######################################################
########################################################          ######################################################
########################################################################################################################


def info():
    loading = codecs.open(f"{path}/min/info.txt", "rb", "utf-8")
    loadedinfo = loading.read()
    loading.close()
    nwindow = Toplevel(window)
    window_set(nwindow, "300x300", "경로 설정", True)
    nl1 = Label(nwindow, text=loadedinfo)
    nl1.place(x=10, y=10)

    nwindow.mainloop()


def choosepath():
    global path

    path = askdirectory(title="min 폴더가 있는 경로, 또는 새로 만들고 싶은 경로를 선택").replace("min", "")
    if path != "":
        path = path.replace("\\", "/")
    else:
        path = os.getcwd().replace("\\", "/")

    if path[-1] == "/":
        path = path[:-1]

    try:  # min 생성 + 필수파일생성
        os.mkdir(f"{path}/min")
        os.mkdir(f"{path}/min/extensions")
        os.mkdir(f"{path}/min/mp4")
        os.mkdir(f"{path}/min/mp3")
    except:
        pass

    try:
        if "settings.json" not in os.listdir(f"{path}/min"):
            creating = codecs.open(f"{path}/min/settings.json", "w", "utf-8")
            creating.close()
        else:
            in_settings()
    except:
        pass

    try:
        if "savelist.json" not in os.listdir(f"{path}/min"):
            creating = codecs.open(f"{path}/min/savelist.json", "w", "utf-8")
            creating.close()
    except:
        pass


def main_loop():
    global window, e_list, e1, e2, e3, e4, e5, e6, e7, e8, e9, e10, e11, e12, ei, ea_list, list_mode, selected_index, cbv1, cbv2

    window = Tk()
    window_set(window, f'360x{250 + 55 * len(settings["tags"])}', "ＭＰＳ", resizable=True)

    mouse_track(window)

    Label(
        window,
        text="MaschinenPistole Speichermedien",
        font="helvetica 16 bold",
        cursor="dot",
    ).place(x=5, y=1)

    ei = ttk.Entry(window, width=49)
    ei.place(x=7, y=220 + 55 * len(settings["tags"]))

    def url_title(x):
        try:
            x.insert(len(x.get()), YouTube(e1.get()).title)
        except:
            pass

    def url_author(x):
        try:
            x.insert(len(x.get()), YouTube(e1.get()).author)
        except:
            pass

    def one_delete():
        global properties
        del properties[-1]
        msg("undo-ed")

    def current_delete():
        global properties
        del properties[selected_index]
        e2.config(values=[i["filename"] for i in properties])
        if properties == []:
            slst_rev()

    def list_clear():
        properties.clear()
        slst_rev()

    def list_mode_set(dummy):
        global selected_index
        selected_index = [i["filename"] for i in properties].index(e2.get())

        e1.delete(0, len(e1.get()))
        for i in e_list[2::]:
            i.delete(0, len(i.get()))

        e1.insert(0, properties[selected_index]["url"])
        for i in range(len(settings["tags"])):
            if settings["tags"][i] in list(properties[selected_index].keys()):
                e_list[i + 2].insert(0, properties[selected_index][settings["tags"][i]])

    ttk.Button(window, text="정보 저장", command=save).place(
        x=40, y=160 + 55 * len(settings["tags"])
    )

    ttk.Button(window, text="다운로드", command=downloading).place(
        x=130, y=187 + 55 * len(settings["tags"])
    )

    cbv1 = IntVar()
    cbv2 = IntVar()

    ttk.Checkbutton(window, text="재생목록 모드", variable=cbv1).place(x=222, y=162 + 55 * len(settings["tags"]))
    ttk.Checkbutton(window, text="분할 모드", variable=cbv2).place(x=222, y=189 + 55 * len(settings["tags"]))

    if list_mode == 0:
        ttk.Button(window, text="리셋", command=reset).place(
            x=130, y=160 + 55 * len(settings["tags"])
        )
        ttk.Button(window, text="1개 취소", command=one_delete).place(
            x=40, y=187 + 55 * len(settings["tags"])
        )
        e2 = ttk.Entry(window, width=40)
    else:
        ttk.Button(window, text="삭제", command=current_delete).place(
            x=130, y=160 + 55 * len(settings["tags"])
        )
        ttk.Button(window, text="리스트 초기화", command=list_clear).place(
            x=40, y=187 + 55 * len(settings["tags"])
        )
        e2 = ttk.Combobox(window, width=38, values=[i["filename"] for i in properties])
        e2.bind("<<ComboboxSelected>>", list_mode_set)

    e1 = ttk.Entry(window, width=40)
    e3 = ttk.Entry(window, width=40)
    e4 = ttk.Entry(window, width=40)
    e5 = ttk.Entry(window, width=40)
    e6 = ttk.Entry(window, width=40)
    e7 = ttk.Entry(window, width=40)
    e8 = ttk.Entry(window, width=40)
    e9 = ttk.Entry(window, width=40)
    e10 = ttk.Entry(window, width=40)
    e11 = ttk.Entry(window, width=40)
    e12 = ttk.Entry(window, width=40)
    ea_list = [e1, e2, e3, e4, e5, e6, e7, e8, e9, e10, e11, e12]

    e1.place(x=65, y=40)
    e2.place(x=65, y=95)
    Label(window, text="url:").place(x=1, y=40)
    Label(window, text="filename:").place(x=1, y=95)
    ttk.Button(
        window,
        text="붙여넣기",
        command=lambda: e1.insert(len(e1.get()), str(clipboard.paste())),
    ).place(x=65, y=65)
    ttk.Button(
        window,
        text="붙여넣기",
        command=lambda: e2.insert(len(e2.get()), str(clipboard.paste())),
    ).place(x=65, y=120)
    ttk.Button(window, text="삭제", command=lambda: e1.delete(0, len(e1.get()))).place(
        x=155, y=65
    )
    ttk.Button(window, text="삭제", command=lambda: e2.delete(0, len(e2.get()))).place(
        x=155, y=120
    )
    ttk.Button(window, text="가져오기", command=lambda: url_title(e2)).place(x=245, y=120)
    e_list = [e1, e2]

    for i in range(len(settings["tags"])):
        ea_list[2:][i].place(x=65, y=150 + 55 * i)
        Label(window, text=f'{settings["tags"][i]}:').place(x=1, y=150 + 55 * i)
        e_list.append(ea_list[2:][i])
        bt_copy_arg, bt_del_arg = partial(
            lambda x: x.insert(len(x.get()), str(clipboard.paste())), ea_list[2:][i]
        ), partial(lambda x: x.delete(0, len(x.get())), ea_list[2:][i])
        ttk.Button(window, text="붙여넣기", command=bt_copy_arg).place(x=65, y=175 + 55 * i)
        ttk.Button(window, text="삭제", command=bt_del_arg).place(x=155, y=175 + 55 * i)

    if "artist" in settings["tags"]:
        ttk.Button(
            window,
            text="가져오기",
            command=lambda: url_author(ea_list[2:][settings["tags"].index("artist")]),
        ).place(x=245, y=175 + 55 * settings["tags"].index("artist"))

    if "title" in settings["tags"]:
        ttk.Button(
            window,
            text="가져오기",
            command=lambda: url_title(ea_list[2:][settings["tags"].index("title")]),
        ).place(x=245, y=175 + 55 * settings["tags"].index("title"))

    ttk.Button(
        window,
        text="창 리셋",
        command=lambda: window_set(
            window,
            f'360x{250 + 55 * len(settings["tags"])}',
            window.title() + "：ＲＥ",
            resizable=True,
        ),
    ).place(x=10, y=275 + 55 * len(settings["tags"]))

    def slst_rev():
        global list_mode, selected_index
        if properties:
            if list_mode == 0:
                list_mode = 1
            else:
                list_mode = 0
                selected_index = -1
            window.destroy()
            main_loop()
        elif list_mode == 1:
            list_mode = 0
            selected_index = -1
            window.destroy()
            main_loop()

    def hotkey_settings_enter():
        window.destroy()
        hotkey_settings()

    menubar = Menu(window)
    menu_1 = Menu(menubar, tearoff=0)
    menu_1.add_command(label="설정", command=settings_open)
    menu_1.add_command(label="목록 모드 토글", command=slst_rev)
    menu_1.add_command(label="목록 불러오기", command=in_txt)
    menu_1.add_command(label="목록 내보내기", command=ex_txt)
    menubar.add_cascade(label="파일", menu=menu_1)

    menu_2 = Menu(menubar, tearoff=0)
    menu_2.add_command(label="핫키", command=hotkey_floatings)
    menu_2.add_command(label="핫키 설정", command=hotkey_settings_enter)
    menubar.add_cascade(label="핫키", menu=menu_2)

    menu_3 = Menu(menubar, tearoff=0)
    menu_3.add_command(label="재생목록/분할")
    menu_3.add_command(label="가사 태그기")
    menubar.add_cascade(label="확장", menu=menu_3)

    menu_4 = Menu(menubar, tearoff=0)
    menu_4.add_command(label="정보")
    menu_4.add_command(label="경로 정리", command=mp4_all_delete)
    menu_4.add_command(label="테스트", command=vcl)
    menubar.add_cascade(label="기타", menu=menu_4)

    window.config(menu=menubar)

    window.mainloop()


########################################################################################################################
######################################################               ###################################################
######################################################    핫키 입력    ###################################################
######################################################               ###################################################
########################################################################################################################


def hotkey_settings():
    global properties, settings

    hkwindow = Tk()
    window_set(hkwindow, f"450x{len(settings['hotkeys']) * 30 + 110}", "핫키 설정", True)

    # url, filename, title, artist, band, album, comment, year: int, track: int, genre, composer, timing
    hkentry_list = []
    str_values = [
        "url",
        "filename",
        "title",
        "artist",
        "band",
        "album",
        "comment",
        "year",
        "track",
        "genre",
        "composer",
        "timing",
    ]

    for i in settings["hotkeys"]:
        hkentry_list.append(
            [
                ttk.Entry(hkwindow, width=27),
                ttk.Combobox(hkwindow, values=str_values, state="readonly"),
            ]
        )
        hkentry_list[-1][0].place(x=20, y=(len(hkentry_list) * 30 + 20))
        hkentry_list[-1][0].insert(0, i["contents"])
        hkentry_list[-1][1].place(x=240, y=(len(hkentry_list) * 30 + 20))
        hkentry_list[-1][1].set(i["location"])

    Label(hkwindow, text="contents").place(x=20, y=20)
    Label(hkwindow, text="location").place(x=240, y=20)

    def hotkey_extend():
        hkentry_list.append(
            [
                ttk.Entry(hkwindow, width=27),
                ttk.Combobox(hkwindow, values=str_values, state="readonly"),
            ]
        )
        hkentry_list[-1][0].place(x=20, y=(len(hkentry_list) * 30 + 20))
        hkentry_list[-1][1].place(x=240, y=(len(hkentry_list) * 30 + 20))
        hb1.place(x=20, y=(len(hkentry_list) * 30 + 50))
        hb2.place(x=130, y=(len(hkentry_list) * 30 + 50))
        hb3.place(x=240, y=(len(hkentry_list) * 30 + 50))
        window_set(hkwindow, f"450x{len(hkentry_list) * 30 + 110}", "핫키 설정", True)

    def hotkey_del():
        global settings
        settings["hotkeys"] = []
        hkwindow.destroy()
        main_loop()

    def hotkey_apply():
        global settings
        settings["hotkeys"] = []
        for i in hkentry_list:
            settings["hotkeys"].append({"contents": i[0].get(), "location": i[1].get()})
        hkwindow.destroy()
        main_loop()

    hb1 = ttk.Button(hkwindow, text="확장", command=hotkey_extend)
    hb2 = ttk.Button(hkwindow, text="초기화", command=hotkey_del)
    hb3 = ttk.Button(hkwindow, text="확정", command=hotkey_apply)

    hb1.place(x=20, y=(len(hkentry_list) * 30 + 50))
    hb2.place(x=130, y=(len(hkentry_list) * 30 + 50))
    hb3.place(x=240, y=(len(hkentry_list) * 30 + 50))


def hotkey_floatings():
    hkft_window = Toplevel(window)
    window_set(
        hkft_window, f"320x{((len(settings['hotkeys']) - 1) // 2) * 30 + 50}", "핫키"
    )
    bt_list = []

    def text_insert(content, loaction):
        if loaction == "url":
            e1.insert(len(e1.get()), content)
        elif loaction == "filename":
            e2.insert(len(e2.get()), content)
        else:
            if loaction in settings["tags"]:
                e_list[settings["tags"].index(loaction) + 2].insert(
                    len(e_list[settings["tags"].index(loaction) + 2].get()), content
                )

    for i in settings["hotkeys"]:
        bt_list.append(ttk.Button(hkft_window, text=i["contents"], width=11))
        Label(hkft_window, text=i["location"]).place(
            x=(100 + 150 * ((len(bt_list) - 1) % 2)),
            y=(((len(bt_list) - 1) // 2) * 30 + 10),
        )
        bt_list[-1].place(
            x=(10 + 150 * ((len(bt_list) - 1) % 2)),
            y=(((len(bt_list) - 1) // 2) * 30 + 10),
        )
        text_insert_arg = partial(text_insert, i["contents"], i["location"])
        bt_list[-1].configure(command=text_insert_arg)


########################################################################################################################
######################################################             #####################################################
######################################################    구동부    #####################################################
######################################################             #####################################################
########################################################################################################################


choosepath()
main_loop()
