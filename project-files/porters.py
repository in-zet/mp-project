# -*- coding: utf-8 -*-
import codecs


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

        if __name__ == '__main__':  # FOR_TEST
            print('in')
            return

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

    if __name__ == '__main__' :  # FOR_TEST
        print('out')
        return

    e5.delete(0, len(e5.get()))
    e5.insert(0, 'settings exported')


# FOR_TEST
# if __name__ == '__main__' : ... 은 인터프리터에서 직접 실행될 경우에만 작동
# 0 = false, 1 = true
# 윈도우에서는 파일경로처리에 역슬래시 사용, 파이썬에서는 슬래시 사용 => 변환 필요
if __name__ == '__main__':
    settings_dict = {'path': 'C:/Users/dongi/Desktop', 'iscreatelyric': 0, 'ismp3': 1, 'ismp4': 0, 'isdevmode': 0,
        'hotkeyslot1': '', 'hotkeyslot2': '', 'hotkeyslot3': '', 'hotkeyslot4': '', 'hotkeyslot5': '',
        'hotkeyslot6': '', 'hotkeyslot7': '', 'hotkeyslot8': '', 'hotkeyslot9': '', 'hotkeyslot10': '',
        'hotkeyslot11': '', 'hotkeyslot12': '', 'hotkeyslot13': '', 'hotkeyslot14': '', 'hotkeyslot15': '',
        'hotkeyslot16': '', 'hotkeyslot17': '', 'hotkeyslot18': '', 'hotkeyslot19': '', 'hotkeyslot20': '',
        'hotkeyslotwhere1': '', 'hotkeyslotwhere2': '', 'hotkeyslotwhere3': '', 'hotkeyslotwhere4': '', 'hotkeyslotwhere5': '',
        'hotkeyslotwhere6': '', 'hotkeyslotwhere7': '', 'hotkeyslotwhere8': '', 'hotkeyslotwhere9': '', 'hotkeyslotwhere10': '',
        'hotkeyslotwhere11': '', 'hotkeyslotwhere12': '', 'hotkeyslotwhere13': '', 'hotkeyslotwhere14': '', 'hotkeyslotwhere15': '',
        'hotkeyslotwhere16': '', 'hotkeyslotwhere17': '', 'hotkeyslotwhere18': '', 'hotkeyslotwhere19': '', 'hotkeyslotwhere20': ''
        }

    ex_settings('C:/Users/dongi/Desktop')
