# -*- coding: utf-8 -*-
import mutagen
from mutagen.easyid3 import EasyID3
from mutagen.id3 import ID3, TIT2
from mutagen.mp4 import MP4Tags
from mutagen._file import *
from pytube import YouTube
from moviepy.editor import *


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


# ----------------------------------------------------------------------------------------------------------------------


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
