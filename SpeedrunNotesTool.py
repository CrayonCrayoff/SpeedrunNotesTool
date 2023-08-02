#Import all the needed libraries and such.
#For the GUI.
import tkinter as tk
import tkinter.scrolledtext as tkscrolled
from tkinter import ttk
from PIL import Image, ImageTk, ImageOps

#For listening to key presses, finding directories, and threading so the program doesn't crash on close.
import keyboard
import os
import threading
import time
import re
import yaml



#Set up window to display things in.
with open("config.yaml", "r") as f:
    config = yaml.load(f, Loader=yaml.FullLoader)
    

    root = tk.Tk()
    root.minsize(width=120, height=120)
    root.geometry(config["screenDimensions"])
    root.title("SpeedrunScrollableNotesTool")
    root.config(background="grey18")



#Finds the current working directory, store it as original working directory for later use.
origiworkDir = os.getcwd()



#Generate list of notes, separated by split. End of split is indicated in text file by the string "#####", followed by a newline.
#Final list for use is called splitsNotesList.
    #This probably needs to be updated later to allow user input through the GUI.
temporaryList = []
splitsNotesList = []

#Add the ReadMe file as the first "splits" notes.
with open('ReadMe.txt', 'r') as file:
    textLines = file.readlines()
    for line in textLines:
        temporaryList.append(line)
    splitText = "".join(temporaryList)
    splitsNotesList.append(splitText)
    temporaryList = []

#Add the actual notes.
with open('TheNotes.txt', 'r', encoding="utf-8", errors="ignore") as file:
    textLines = file.readlines()

for line in textLines:
    if re.search("^##End of Split##", line):
        splitText = "".join(temporaryList)
        splitsNotesList.append(splitText)
        temporaryList = []
    else:
        temporaryList.append(line)
    
#Add one final "split" so everything lines up with LiveSplit functionality.
goodJob = """Great job on finishing your run!\n\nPat yourself on the back, rehydrate with some water, stretch a little.\n
            \nIf you want to do another run, just press the button for "Next Split" or for "Reset".\n
            \nOf course you can also call it a day and close the program."""
splitsNotesList.append(goodJob)


#Looks in folder called maps and makes an alphabetized list of the names of all the files in it.
mapsPath = "maps"
dirmapsList = os.listdir(mapsPath)
listMapNames = sorted(dirmapsList)

#Generates a list called mapsList, containing all the file names.
mapsNameList = []
for name in listMapNames:
    pathAndName = origiworkDir + "\maps\\" + name
    mapsNameList.append(pathAndName)    

#Starting values for list indeces and such
currentSplit = 0
currentMap = -1
screenWidth = root.winfo_width()
screenHeight = root.winfo_height()
global mode
mode = "Notes"

startingImage = origiworkDir + "\maps\\" + mapsNameList[0]

global finalImage



#Create the label in the window to display images.
label = tk.Label(master=root,
    font=("Consolas",10),
    image="",
    justify="left",
    anchor="nw",
    foreground="white",
    background="grey18",
    height=screenHeight,
    width=screenWidth,
    padx=10,
    pady=10)

#Create the text widget to display text. Allows for scrolling if necessary.
text = tkscrolled.ScrolledText(master=root,
    font=("Consolas",10),
    selectbackground="grey35",
    bg="grey18",
    fg="white",
    wrap=tk.WORD,
    height = screenHeight,
    width = screenWidth,
    relief=tk.FLAT)
text.vbar.config(width="0")
text.pack(fill="both", expand="True")

text.insert(tk.END, splitsNotesList[0])
text.config(state=tk.DISABLED)




#Call display function to resize textwrap size or image size, depending on current mode.
def resize(e):
    #Store the screen's dimensions and position in the YAML config file.
    latestDimensions = root.winfo_geometry() 
    with open("config.yaml", "r") as f:
        config = yaml.load(f, Loader=yaml.FullLoader)
    
    config["screenDimensions"] = latestDimensions
    with open("config.yaml", "w") as f:
        config = yaml.dump(config, stream=f, default_flow_style=False, sort_keys=False)
    with open("config.yaml") as f:
        config = yaml.load(f, Loader=yaml.FullLoader)    
    
    global mode
    if mode == "Maps":
        displayMaps()
    else:
        pass



#Show text on screen.
def displayNotes():
    #Resizes the text widget to fit the screen.
    global mode
    global splitsNotesList
    global currentSplit
    
    mode = "Notes" 
    label.pack_forget()
    text.config(state=tk.NORMAL)
    text.delete("0.0", tk.END)
    text.insert(tk.END, splitsNotesList[currentSplit % len(splitsNotesList)])
    text.config(state=tk.DISABLED)
    text.pack(fill="both", expand="True")

    print("xview is: ", text.xview())
    print("yview is: ", text.yview())

#Needlessly complicated way to display an image on the screen.
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

    #Remove the text widget.
    text.pack_forget()

    #Overwrite old image with new image.    
    finalImage = ImageTk.PhotoImage(resizedImage)
    label.config(image=finalImage)
    label.image = finalImage
    label.pack(fill="both", expand="True")



#Waits for a keyboard input, checks for certain keys.
    #This needs to be updated later, to allow the user to set their own hotkeys. 
def waitkeyPress():
    running = True
    while running:
        event = keyboard.read_event()

        if event.event_type == keyboard.KEY_UP:
            if event.name == '0' and event.is_keypad == True:
                nextSplit()
            elif event.name == '-' and event.is_keypad == True: 
                undoSplit()
            elif event.name == '+' and event.is_keypad == True:
                skipSplit()
            elif event.name == 'space':
                nextMap()
            elif event.name == 'backspace':
                previousMap()
            elif event.name == '/' and event.is_keypad == True:
                resetAll()
            elif event.name == 'delete':
                modeSwap()
            #Closes the window. Only triggers if the window is in focus, to prevent accidental closing.
            elif event.name == 'q' or event.name == 'esc':
                if root.focus_displayof():
                    root.destroy()
            else:
                pass



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
        


def main():
    # start a seperate thread that waits for a global keyboard input
    t = threading.Thread(target=waitkeyPress, daemon=True)
    t.start()

    root.bind("<Configure>", resize)
    root.mainloop()

    
if __name__ == "__main__":
    main()