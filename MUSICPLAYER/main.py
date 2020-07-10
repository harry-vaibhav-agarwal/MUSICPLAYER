from tkinter import *
import tkinter.messagebox
import tkinter.filedialog
from pygame import mixer
import os

root = Tk()
mixer.init()  #initializing the mixer



root.title('MP3 MUSIC PLAYER')
root.geometry('400x400')
root.iconbitmap('melody.ico')

menubar = Menu(root)
root.config( menu = menubar)

fileSubmenu = Menu(menubar, tearoff=0)
helpSubmenu = Menu(menubar, tearoff=0)

menubar.add_cascade(label="File",menu=fileSubmenu)
menubar.add_cascade(label="Help",menu=helpSubmenu)


def browse_file():
    global filename
    filename=tkinter.filedialog.askopenfilename()
    print(filename)

fileSubmenu.add_command(label="Open", command=browse_file)
fileSubmenu.add_command(label="Exit", command=root.destroy)


text = Label(root, text="Let's make some noise")  # creating a widget
text.pack(pady=10)  # packing widget to appear in window







def about_us():
    about_info = "This is a music player built using Python Tkinter where you can also create playlist"
    tkinter.messagebox.showinfo('About Music Player', about_info)



helpSubmenu.add_command(label="About", command=about_us)



play_photo = PhotoImage(file='play.png')
pause_photo=PhotoImage(file='pause.png')
stop_photo=PhotoImage(file='stop.png')


middleFrame=Frame(root)
middleFrame.pack(padx=10,pady=10)


def play_music():
    try:
        paused                           #paused button initialised or not
    except NameError:                    #not initialized nameerror will be thrown and this code will execute we are playing for first time
        try:
            mixer.music.load(filename)
            mixer.music.play()
            statusBar['text'] = 'Playing music '+os.path.basename(filename)
        except:
            tkinter.messagebox.showerror('Error','Music Player cannot find the file.Please check it again')

    else:
        mixer.music.unpause()
        statusBar['text'] = 'Music Resumes'



def pause_music():
    global paused
    paused = TRUE
    mixer.music.pause()
    statusBar['text']='Music Paused'

def stop_music():
    statusBar['text'] = 'Music Stopped'
    mixer.music.stop()


def set_vol(val):
    mixer.music.set_volume(int(val) / 100)


playBtn = Button(middleFrame, image=play_photo, command=play_music)
playBtn.pack(side=LEFT, padx=10)


pauseBtn=Button(middleFrame,image=pause_photo,command=pause_music)
pauseBtn.pack(side=LEFT, padx=10)

stopBtn = Button(middleFrame, image=stop_photo, command=stop_music)
stopBtn.pack(side=LEFT, padx=10)


statusBar = Label(root, text = 'Welcome to Mp3 Music Player',relief= SUNKEN,anchor=W)
statusBar.pack(side=BOTTOM, fill=X)

scale = Scale(root, from_=0, to=100, orient=HORIZONTAL,command = set_vol)
scale.set(70)  #default value
mixer.music.set_volume(0.7)
scale.pack(pady=20)
root.mainloop()


