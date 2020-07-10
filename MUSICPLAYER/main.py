from tkinter import *
import tkinter.messagebox
from pygame import mixer


root = Tk()
mixer.init()  #initializing the mixer



root.title('MP3 MUSIC PLAYER')
root.geometry('500x500')
root.iconbitmap('melody.ico')


menubar = Menu(root)
root.config( menu = menubar)

fileSubmenu = Menu(menubar, tearoff=0)
helpSubmenu = Menu(menubar, tearoff=0)

menubar.add_cascade(label="File",menu=fileSubmenu)
menubar.add_cascade(label="Help",menu=helpSubmenu)

fileSubmenu.add_command(label="Open")
fileSubmenu.add_command(label="Exit")


def about_us():
    about_info = "This is a music player built using Python Tkinter where you can also create playlist"
    tkinter.messagebox.showinfo('About Music Player', about_info)



helpSubmenu.add_command(label="About", command=about_us)

text = Label(root, text="Let's make some noise\n")  # creating a widget
text.pack()  # packing widget to appear in window

play_photo = PhotoImage(file='play.png')
stop_photo=PhotoImage(file='stop.png')

def play_music():
    mixer.music.load('song1.mp3')
    mixer.music.play()
    print('Playing..')

def stop_music():
    print('Pausing...')
    mixer.music.stop()


def set_vol(val):
    print('Setting volume')
    mixer.music.set_volume(int(val) / 100)


playBtn = Button(root, image=play_photo, command=play_music)
playBtn.pack()

stopBtn = Button(root, image=stop_photo, command=stop_music)
stopBtn.pack()

scale = Scale(root, from_=0, to=100, orient=HORIZONTAL,command = set_vol)
scale.set(70)  #default value
mixer.music.set_volume(0.7)
scale.pack()
root.mainloop()


