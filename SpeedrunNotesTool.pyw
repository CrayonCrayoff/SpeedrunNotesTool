#Import all the needed libraries and such.
#For the GUI.
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk, ImageOps

#For listening to key presses, finding directories, and threading so the program doesn't crash on close.
import keyboard
import os
import threading
import time
import re


#Set up window to display things in.
root = tk.Tk()
root.minsize(width=120, height=120)
root.geometry("520x800+1388+0")
root.title("SpeedrunNotesTool")
root.config(background="grey18")


#Finds the current working directory, store it as original working directory for later use.
origiworkDir = os.getcwd()


#Generate list of notes, separated by split. End of split is indicated in text file by the string "#####", followed by a newline.
#Final list for use is called splitsNotesList.
    #This probably needs to be updated later to allow user input through the GUI.
temporaryList = []
splitsNotesList = []

with open('ReadMe.txt', 'r') as file:
    textLines = file.readlines()
    for line in textLines:
        temporaryList.append(line)
    splitText = "".join(temporaryList)
    splitsNotesList.append(splitText)
    temporaryList = []

with open('TheNotes.txt', 'r', encoding="utf-8", errors="ignore") as file:
    textLines = file.readlines()

for line in textLines:
    if re.search("^##End of Split##", line):
        splitText = "".join(temporaryList)
        splitsNotesList.append(splitText)
        temporaryList = []
    else:
        temporaryList.append(line)
    

#Looks in folder called maps and makes an alphabetized list of the names of all the files in it.
mapsPath = "maps"
dirmapsList = os.listdir(mapsPath)
listMapNames = sorted(dirmapsList)

#Generates a list of all the images called mapsList, which will be used later.
mapsNameList = []
for name in listMapNames:
    pathAndName = origiworkDir + "\maps\\" + name
    mapsNameList.append(pathAndName)    

#Starting values for list stuffs and such
currentSplit = 0
currentMap = -1
screenWidth = root.winfo_width()
screenHeight = root.winfo_height()
global mode
mode = "Notes"

startingImage = origiworkDir + "\maps\\" + mapsNameList[0]

global finalImage



#Create the label in the window to display text and images.
label = tk.Label(root, text=splitsNotesList[0],
    font=("Consolas",10),
    image="",
    wraplength=986,
    justify="left",
    anchor="nw",
    foreground="white",
    background="grey18",
    padx=10,
    pady=10)
label.place(relx=0.0,
            rely=0.0,
            anchor="nw")


 
#Function that's called when text needs to be on screen. 
def displayNotes():
    global splitsNotesList
    global currentSplit
    global screenWidth
    global mode

    screenWidth = root.winfo_width()
    wraptext = screenWidth - 12
    
    mode = "Notes"
    
    label.config(image="")
    label.image = "",
    label.config(text=splitsNotesList[currentSplit % len(splitsNotesList)],
        image="",
        justify="left",
        anchor="nw",
        wraplength=wraptext,
        foreground="white",
        background="grey18")
    label.place(relx=0.0,
                rely=0.0)


    
#Function that's called when a map needs to be on screen.
def displayMaps():
    global mapsNameList
    global currentMap
    global finalImage
    global screenWidth
    global screenHeight
    global mode

    mode = "Maps"

    #Open image.
    originalImage = Image.open(str(mapsNameList[currentMap % len(mapsNameList)]))
    preppedImage = ImageTk.PhotoImage(originalImage)

    #Find ratio between screen width/image width and screen height/image height.
    screenWidth = root.winfo_width()
    screenHeight = root.winfo_height()
    widthRatio = screenWidth / preppedImage.width()
    heightRatio = screenHeight / preppedImage.height()
    
    #Check which of the two ratios is smaller. Use that one. 
    if widthRatio < heightRatio:
        resizeModifier = screenWidth / preppedImage.width()
    else: 
        resizeModifier = screenHeight / preppedImage.height()
    
    #Resize the image according to the previously determined modifier.
    newWidth = preppedImage.width() * resizeModifier
    newWidth = round(newWidth) - 4
    newHeight = preppedImage.height() * resizeModifier
    newHeight = round(newHeight) - 4
    resizedImage = originalImage.resize((newWidth, newHeight))

    #Overwrite old image with new image.    
    finalImage = ImageTk.PhotoImage(resizedImage)
    label.config(image=finalImage)
    label.image = finalImage
    label.place(relx=0.0,
                rely=0.0,
                anchor="nw")
    
    print("New Width is: " + str(newWidth))
    print("New Height is: " + str(newHeight))
    print(root.winfo_geometry())




#Set up how the lists change for all the hotkeys, and which display function to call.
def nextSplit():
    global currentSplit
    currentSplit += 1
    displayNotes()

def undoSplit():
    global currentSplit
    currentSplit -= 1
    displayNotes()
    
def skipSplit():
    global currentSplit
    currentSplit += 1
    displayNotes()
    
def nextMap():
    global currentMap
    currentMap += 1
    displayMaps()

def previousMap():
    global currentMap
    currentMap -= 1
    displayMaps()

def resetAll():
    global currentMap
    global currentSplit   
    currentMap = -1
    currentSplit = 0 
    displayNotes()
    
def modeSwap():
    global mode
    if mode == "Notes":
        #mode = "Maps"
        displayMaps()
        
    elif mode == "Maps":
        #mode = "Notes"
        displayNotes()
        
    else:
        pass
    

#Call display function to resize textwrap size or image size, depending on current mode.
def resize(e):
    global mode
    if mode == "Notes":
        displayNotes()
    elif mode == "Maps":
        displayMaps()
    else:
        print("You dun goofed")





#Waits for a keyboard input, checks for certain keys.
#This needs to be updated later, to allow the user to set their own hotkeys. 
def waitkeyPress():
    running = True
    while running:
        event = keyboard.read_event()
        if event.event_type == keyboard.KEY_UP:
            if event.name == 'f1':
                nextSplit()
            elif event.name == 'f3': 
                undoSplit()
            elif event.name == 'f4':
                skipSplit()
            elif event.name == 'f5':
                nextMap()
            elif event.name == 'f6':
                previousMap()
            elif event.name == 'f2':
                resetAll()
            elif event.name == 'f8':
                modeSwap()
            #Closes the window. Only triggers if the window is in focus, to prevent accidental closing.
            elif event.name == 'esc' and not event.name == '1':
                if root.focus_displayof():
                    root.destroy()
            else:
                pass



def main():
    running = True

    # start a seperate thread that waits for a global keyboard input
    t = threading.Thread(target=waitkeyPress, daemon=True)
    t.start()

    root.bind("<Configure>", resize)
    root.mainloop()

    
if __name__ == "__main__":
    main()