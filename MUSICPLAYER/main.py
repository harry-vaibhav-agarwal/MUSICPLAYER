from tkinter import *
import tkinter.messagebox
import tkinter.filedialog
from pygame import mixer
from mutagen.mp3 import MP3
import os

root = Tk()
mixer.init()  # initializing the mixer

root.title('MP3 MUSIC PLAYER')
root.geometry('400x400')
root.iconbitmap('images/melody.ico')

menubar = Menu(root)
root.config(menu=menubar)

fileSubmenu = Menu(menubar, tearoff=0)
helpSubmenu = Menu(menubar, tearoff=0)

menubar.add_cascade(label="File", menu=fileSubmenu)
menubar.add_cascade(label="Help", menu=helpSubmenu)


def browse_file():
    global filename
    filename = tkinter.filedialog.askopenfilename()


fileSubmenu.add_command(label="Open", command=browse_file)
fileSubmenu.add_command(label="Exit", command=root.destroy)

fileLabel = Label(root, text="Let's make some noise")  # creating a widget
fileLabel.pack(pady=10)  # packing widget to appear in window


lengthLabel=Label(root, text='Total Length : -- : -- ')
lengthLabel.pack(pady=10)

def show_Details():
    fileLabel['text'] = 'Playing ' + os.path.basename(filename)

    file_data = os.path.splitext(filename)  # we get a list list one is file location second one is extension

    if file_data[1] == ".mp3":
        audio = MP3(filename)  # getting metadata
        total_length = audio.info.length
    else :
        a = mixer.Sound(filename)
        total_length = a.get_length()


    #converting duration into seconds
    mins,secs=divmod(total_length,60)
    mins = round(mins)
    secs = round(secs)
    timeformat = '{:02d}:{:02d}'.format(mins,secs)
    lengthLabel['text'] = "Total Length" + ' - ' + timeformat


statusBar = Label(root, text='Welcome to Mp3 Music Player', relief=SUNKEN, anchor=W)
statusBar.pack(side=BOTTOM, fill=X)


def about_us():
    about_info = "This is a music player built using Python Tkinter where you can also create playlist"
    tkinter.messagebox.showinfo('About Music Player', about_info)


helpSubmenu.add_command(label="About", command=about_us)

play_photo = PhotoImage(file='images/play.png')
pause_photo = PhotoImage(file='images/pause.png')
stop_photo = PhotoImage(file='images/stop.png')
rewind_photo = PhotoImage(file='images/rewind.png')
volume_photo = PhotoImage(file='images/volume.png')
mute_photo = PhotoImage(file='images/mute.png')

middleFrame = Frame(root)
middleFrame.pack(pady=35)

paused=FALSE
def play_music():
    global paused
    if paused:
        mixer.music.unpause()
        statusBar['text'] = 'Music Resumes'
        paused=FALSE
    else:
        try:
            mixer.music.load(filename)
            mixer.music.play()
            statusBar['text'] = 'Playing music ' + os.path.basename(filename)
            show_Details()
        except :
            tkinter.messagebox.showerror('Error','Music Player cannot find the file.Please check it again')

def pause_music():
    global paused
    paused = TRUE
    mixer.music.pause()
    statusBar['text'] = 'Music Paused'


def stop_music():
    statusBar['text'] = 'Music Stopped'
    mixer.music.stop()


def set_vol(val):
    mixer.music.set_volume(int(val) / 100)


def rewind_music():
    play_music()
    statusBar['text'] = 'Music Rewinded'


muted = FALSE


def mute_music():
    global muted
    if muted:
        volumeBtn.config(image=volume_photo)
        mixer.music.set_volume(0.7)
        scale.set(70)
        muted = FALSE
    else:
        volumeBtn.config(image=mute_photo)
        mixer.music.set_volume(0)
        scale.set(0)
        muted = TRUE


playBtn = Button(middleFrame, image=play_photo, command=play_music)
playBtn.grid(row=0, column=0, padx=10)

pauseBtn = Button(middleFrame, image=pause_photo, command=pause_music)
pauseBtn.grid(row=0, column=1, padx=10)

stopBtn = Button(middleFrame, image=stop_photo, command=stop_music)
stopBtn.grid(row=0, column=2, padx=10)

# Bottom Frame for rewind volume,mute etc

bottomFrame = Frame(root)
bottomFrame.pack()

rewindBtn = Button(bottomFrame, image=rewind_photo, command=rewind_music)
rewindBtn.grid(row=0, column=0, pady=20)

volumeBtn = Button(bottomFrame, image=volume_photo, command=mute_music)
volumeBtn.grid(row=0, column=1, pady=20, padx=10)

scale = Scale(bottomFrame, from_=0, to=100, orient=HORIZONTAL, command=set_vol)
scale.set(70)  # default value
mixer.music.set_volume(0.7)
scale.grid(row=0, column=2, pady=20, padx=30)

root.mainloop()
