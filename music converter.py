import tkinter as tk
from tkinter import filedialog
from pydub import AudioSegment
from pathlib import Path
import ntpath
import os
import sys
import time

if getattr(sys,"frozen",False):
    ffmpeg_path = os.path.join(os.path.dirname(sys.executable),"ffmpeg.exe")
else:
    ffmpeg_path = "ffmpeg.exe"
    
AudioSegment.converter = str(ffmpeg_path)
AudioSegment.ffmpeg = str(ffmpeg_path)

converting = False
selected = []
folder = ""
errors = 0
formats = ".wav .ogg .flv .mp3 .wma"

root = tk.Tk()
root.resizable(0,0)
root.geometry("250x200")

root.title("MSCMC")

frame = tk.Frame(root)
selectT = tk.Label(frame,text="No files selected")
folderT = tk.Label(frame,text="No folder selected")
convertT = tk.Label(frame,text="Waiting...",foreground="black")
progressT = tk.Label(frame,text="0/0")

def selectFiles():
    global converting
    if converting == True:
        return
    
    files = filedialog.askopenfilenames(filetypes=[("Music files",formats)],
                                        initialdir=os.path.expanduser("~\\Music"))
    selected.clear()
    for x in files:
        selected.append(x)
    if len(selected) != 0:
        selectT.config(text=str(len(selected))+" files selected",foreground="black")
    else:
        selectT.config(text="No files selected",foreground="black")
    progressT.config(text="0/"+str(len(selected)))

def selectFolder():
    global converting
    if converting == True:
        return
    
    global folder
    folder = filedialog.askdirectory(
        initialdir="C:\Program Files (x86)\Steam\steamapps\common\My Summer Car")
    if folder != "":
        if len(folder) > 30:
            folderT.config(text="..."+folder[-30:],foreground="black")
        else:
            folderT.config(text=folder,foreground="black")

def convert():
    global converting
    if converting:
        return
    
    if len(selected) == 0:
        selectT.config(text="Select files to convert",foreground="red")
        return
    if folder == "":
        folderT.config(text="Select destination path",foreground="red")
        return
    
    converting = True
    errors = 0
    skipNum = 0
    
    for i,x in enumerate(selected):
        try:
            convertT.config(text="Converting "+ntpath.basename(x),
                            foreground="DarkOrange1")
            root.update()
            audio = AudioSegment.from_file(x, format=os.path.splitext(x)[1][1:])
            newAudio = audio.export(folder+"/track"+str(i+1)+".ogg",format="ogg")
        except Exception as e:
            print(e)
            errors += 1
            convertT.config(text="Error converting "+ntpath.basename(x),
                            foreground="red")
            root.update()
            time.sleep(1)
        progressT.config(text=str(i+1)+"/"+str(len(selected)))

    converting = False
    convertT.config(text="Done with "+str(errors)+" errors!",foreground="green")

selectB = tk.Button(frame,text="Select Music Files", command=selectFiles)
folderB = tk.Button(frame,text="Select Destination", command=selectFolder)
startB = tk.Button(frame,text="Start Conversion", command=convert,
                   background="pale green")

frame.place(relx=0.5,rely=0.5,anchor="center")
selectB.pack()
selectT.pack()
folderB.pack()
folderT.pack()
startB.pack()
convertT.pack()
progressT.pack()

root.mainloop()