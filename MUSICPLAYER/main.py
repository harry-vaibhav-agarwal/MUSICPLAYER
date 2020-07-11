from tkinter import *
import tkinter.messagebox
import tkinter.filedialog
from pygame import mixer
from mutagen.mp3 import MP3
from tkinter import ttk
from ttkthemes import ThemedTk
import threading
import time
import os

root =  ThemedTk(theme="radiance")
mixer.init()  # initializing the mixer

root.title('MP3 MUSIC PLAYER')
root.iconbitmap('images/melody.ico')

menubar = Menu(root)
root.config(menu=menubar)

fileSubmenu = Menu(menubar, tearoff=0)
helpSubmenu = Menu(menubar, tearoff=0)

menubar.add_cascade(label="File", menu=fileSubmenu)
menubar.add_cascade(label="Help", menu=helpSubmenu)



play_photo = PhotoImage(file='images/play.png')
pause_photo = PhotoImage(file='images/pause.png')
stop_photo = PhotoImage(file='images/stop.png')
rewind_photo = PhotoImage(file='images/rewind.png')
volume_photo = PhotoImage(file='images/volume.png')
mute_photo = PhotoImage(file='images/mute.png')
add_photo = PhotoImage(file='images/add.png')
delete_photo = PhotoImage(file='images/delete.png')


#Root-LeftFrame,RightFrame
#LeftFrame-Playlit,Add Button,DeleteButton
#RightFrame-TopFrame,MiddleFrame,BottomFrame

statusBar = ttk.Label(root, text='Welcome to Mp3 Music Player', relief=SUNKEN, anchor=W,font='Times 12 italic')
statusBar.pack(side=BOTTOM, fill=X)


leftFrame = Frame(root)
leftFrame.pack(side=LEFT, padx=40, pady=20)

playListBox = Listbox(leftFrame)
playListBox.pack()


playList=[]

#playlist contains filename with path
#playlistbox only contains filename not the path
#we need path for  mixer.music.load function

def add_to_playlist(filename):

    filename=os.path.basename(filename)
    index=0
    playListBox.insert(index, filename)
    playList.insert(index,filename_path)
    index+=1


def del_song():
    selected_song=playListBox.curselection()
    selected_song = int(selected_song[0])
    playListBox.delete(selected_song)
    playList.pop(selected_song)



def browse_file():
    global filename_path
    filename_path = tkinter.filedialog.askopenfilename()
    add_to_playlist(filename_path)


addBtn = ttk.Button(leftFrame,image = add_photo,command=browse_file)
addBtn.pack(side=LEFT,pady=10,padx=5)

deleteBtn = ttk.Button(leftFrame,image = delete_photo,command=del_song)
deleteBtn.pack(side=LEFT,pady=10,padx=5)


fileSubmenu.add_command(label="Open", command=browse_file)
fileSubmenu.add_command(label="Exit", command=root.destroy)






rightFrame = Frame(root)
rightFrame.pack(pady=30)

topFrame = Frame(rightFrame)
topFrame.pack()

lengthLabel = ttk.Label(topFrame, text='Total Length : -- : -- ',font='Arial 10 bold')
lengthLabel.pack(pady=10)

currentTimeLabel = ttk.Label(topFrame, text='Time remaining : -- : -- ', relief=GROOVE,font='Arial 10 bold')
currentTimeLabel.pack(pady=10)


#convert function sets the remaining time correctly of the song that is playing
def convert(total_length):
    global paused
    t = total_length
    while t >= 0 and mixer.music.get_busy():
        if paused:
            continue
        else:
            mins, secs = divmod(t, 60)
            mins = round(mins)
            secs = round(secs)
            timeformat = '{:02d}:{:02d}'.format(mins, secs)
            currentTimeLabel['text'] = "Time remaining " + ' - ' + timeformat + ' '
            t -= 1
            time.sleep(1)


def show_Details(file):
    file_data = os.path.splitext(file)  # we get a list list one is file location second one is extension

    if file_data[1] == ".mp3":
        audio = MP3(file)  # getting metadata
        total_length = audio.info.length
    else:
        a = mixer.Sound(file)
        total_length = a.get_length()

    # converting duration into seconds
    mins, secs = divmod(total_length, 60)
    mins = round(mins)
    secs = round(secs)
    timeformat = '{:02d}:{:02d}'.format(mins, secs)
    lengthLabel['text'] = "Total Length" + ' - ' + timeformat
    thread = threading.Thread(target=convert, args=(total_length,))
    thread.start()


def about_us():
    about_info = "This is a music player built using Python Tkinter where you can also create playlist"
    tkinter.messagebox.showinfo('About Music Player', about_info)


helpSubmenu.add_command(label="About", command=about_us)

middleFrame = Frame(rightFrame)
middleFrame.pack(pady=35)

paused = FALSE


def play_music():
    global paused
    if paused:
        mixer.music.unpause()
        statusBar['text'] = 'Music Resumes'
        paused = FALSE
    else:
        try:
            stop_music()
            time.sleep(1)
            selected_song = playListBox.curselection()
            selected_song = int(selected_song[0])
            play_it = playList[selected_song]
            mixer.music.load(play_it)
            mixer.music.play()
            statusBar['text'] = 'Playing music ' + os.path.basename(play_it)
            show_Details(play_it)
        except:
            tkinter.messagebox.showerror('Error', 'Music Player cannot find the file.Please check it again')


def pause_music():
    global paused
    paused = TRUE
    mixer.music.pause()
    statusBar['text'] = 'Music Paused'


def stop_music():
    statusBar['text'] = 'Music Stopped'
    mixer.music.stop()


def set_vol(val):
    mixer.music.set_volume(float(val) / 100)


def rewind_music():
    play_music()
    statusBar['text'] = 'Music Rewinded'


muted = FALSE


#muting umnuting and toggling the photo
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


#Middle frame for play,pause and stop

playBtn = ttk.Button(middleFrame, image=play_photo, command=play_music)
playBtn.grid(row=0, column=0, padx=20)

pauseBtn = ttk.Button(middleFrame, image=pause_photo, command=pause_music)
pauseBtn.grid(row=0, column=1, padx=20)

stopBtn = ttk.Button(middleFrame, image=stop_photo, command=stop_music)
stopBtn.grid(row=0, column=2, padx=20)

# Bottom Frame for rewind volume,mute etc

bottomFrame = Frame(rightFrame)
bottomFrame.pack()

rewindBtn = ttk.Button(bottomFrame, image=rewind_photo, command=rewind_music)
rewindBtn.grid(row=0, column=0, pady=20)

volumeBtn = ttk.Button(bottomFrame, image=volume_photo, command=mute_music)
volumeBtn.grid(row=0, column=1, pady=20, padx=10)

scale = ttk.Scale(bottomFrame, from_=0, to=100, orient=HORIZONTAL, command=set_vol)
scale.set(70)  # default value
mixer.music.set_volume(0.7)
scale.grid(row=0, column=2, pady=20, padx=30)


def on_closing():
    stop_music()         #stopping music first then closing the window
    root.destroy()


root.protocol("WM_DELETE_WINDOW", on_closing)  # overriding default functionality of close
root.mainloop()
