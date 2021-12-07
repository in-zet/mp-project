# -*- coding: utf-8 -*-
from tkinter import *


def settings_open():
    global settings_dict

    setting_window = Tk()
    setting_window.geometry('250x300')
    setting_window.resizable(width=False, height=False)
    setting_window.configure()


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


    def winres1():
        if cv1.get() == 0:
            setting_window.geometry('250x300')
            setting_window.resizable(width=False, height=False)
        elif cv1.get() == 1:
            setting_window.geometry('420x900')
            setting_window.resizable(width=True, height=True)


    cv1 = IntVar()  # 버튼 체크시 1, 비 체크시 0
    cb1 = Checkbutton(setting_window, text="Hotkey EDIT OPEN", variable=cv1, command=winres1)
    cb1.pack()
    cb1.place(x=10, y=220)
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

# FOR_TEST
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
    settings_open()
