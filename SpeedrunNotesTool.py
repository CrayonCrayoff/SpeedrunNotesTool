#Import all the needed libraries and such.
#For the GUI.
import tkinter as tk
import tkinter.scrolledtext as tkscrolled
from tkinter import ttk
from tkinter import Toplevel
from PIL import Image, ImageTk, ImageOps

#For listening to key presses, finding directories, and threading so the program doesn't crash on close.
import keyboard
import os
import threading
import time
import re
import yaml



global settingsMenu
global configFile
global screenWidth
global screenHeight
global splitsNotesList
global mapsNameList
global mode
global currentSplit
global currentMap
global finalImage

#Load in saved settings
with open("config.yaml", "r") as f:
    configFile = yaml.load(f, Loader=yaml.FullLoader)



#Set up window to display things in.
root = tk.Tk()
root.minsize(width=120, height=120)
root.geometry(configFile["screenDimensions"])
root.title("Speedrun Notes Tool v1.0.0")
root.config(background="grey18")


root.columnconfigure(0, weight=1)
root.columnconfigure(1, weight=1)
root.rowconfigure(1, weight=1)

#Set a variable with the screen width and height for later use.
root.update()
screenWidth = root.winfo_width()
screenHeight = root.winfo_height()

#Create a button in the 0th column.
startButton = tk.Button(root, text="Start running", command=lambda: startRun())
startButton.grid(column=0, row=0, padx=5, pady=5, sticky=tk.E)


#Create a button in the 1st column.
settingsButton = tk.Button(root, text="Settings", command=lambda: openSettingsMenu())
settingsButton.grid(column=1, row=0, padx=5, pady=5, sticky=tk.W)


#Create the label in the window to display images.
label = tk.Label(master=root,
    font=("Consolas",configFile["Text Size"]),
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
    font=("Consolas",configFile["Text Size"]),
    selectbackground="grey35",
    bg="grey18",
    fg="white",
    wrap=tk.WORD,
    width=screenWidth,
    height=screenHeight,
    relief=tk.FLAT,
    cursor="arrow")
text.vbar.config(width="0")
text.grid(column=0, row=1, sticky=tk.NSEW, columnspan=2)


#Add the ReadMe file as the opening text.
temporaryList = []

with open('ReadMe.txt', 'r') as file:
    textLines = file.readlines()
    for line in textLines:
        temporaryList.append(line)
    openingText = "".join(temporaryList)
    temporaryList = []


text.insert(tk.END, openingText)
text.config(state=tk.DISABLED)



#Add the actual notes.
splitsNotesList = []

gettingReadyText = "This is a waiting screen for the start of your run. The program is listening to your keyboard inputs. Press the \"Next Split\" button to start the run."

splitsNotesList.append(gettingReadyText)
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
origiworkDir = os.getcwd()
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

mode = "Notes"

startingImage = origiworkDir + "\maps\\" + mapsNameList[0]




#Define the slider behaviour in the settingsMenu.
def textSizeChange(e):
    global oldTextSize
    oldTextSize = configFile["Text Size"]
    global slider
    configFile["Text Size"] = slider.get()
    global previewText
    #previewText.config(state=tk.NORMAL)
    previewText.config(font=("Consolas",configFile["Text Size"]))
    text.config(font=("Consolas",configFile["Text Size"]))

def openSettingsMenu():
    #Set up settings window.
    global settingsMenu
    settingsMenu = Toplevel()
    settingsMenu.minsize(width=120, height=120)
    settingsMenu.geometry("500x600+600+100")
    settingsMenu.title("SpeedrunScrollableNotesTool")
    settingsMenu.config(background="grey18")
    settingsMenu.resizable(0,0)

    settingsMenu.columnconfigure(0, weight=1)
    settingsMenu.columnconfigure(1, weight=1)
    settingsMenu.columnconfigure(2, weight=1)
    settingsMenu.columnconfigure(3, weight=1)

    settingsMenu.rowconfigure(10, weight=1)
    settingsMenu.focus_force()
    settingsMenu.grab_set()
    
    print("Opened settings menu")
    
    #Set up the Settings Menu widgets.
    hotkeyNames = ["Next Split", "Undo Split", "Skip Split", "Next Map", "Previous Map", "Swap to Text/Maps", "Reset", "Quit Program"]
    
    #Loop through the hoykeyNames, creating a Label with the name, accompanied by a textbox and a button.
    for index, name in enumerate(hotkeyNames):
        hotkeyName = tk.Label(master=settingsMenu, bg="grey18", fg="white", text=name)
        hotkeyName.grid(column=0, row=index, padx=5, pady=5, sticky=tk.W)
        
        textBox = tk.Label(master=settingsMenu, bg="white", fg="black", relief=tk.SUNKEN, justify=tk.LEFT, width=100)
        currentKey = "Current: "
        if configFile[name]["is_keypad"] == True:
            currentKey = currentKey + "Numpad "
        currentKey += str(configFile[name]["name"])
        textBox.config(text=currentKey)
        textBox.grid(column=1, columnspan=2, row=index, padx=5, pady=5, sticky=tk.EW)
        
        setButton = tk.Button(master=settingsMenu, text="Set Hotkey", command=lambda i=index, name=name: hotkeyButton(i, name))
        setButton.grid(column=3, row=index, padx=5, pady=5, sticky=tk.W)


    
    global slider
    slider = tk.Scale(master=settingsMenu, from_=10, to=20, length=300, orient=tk.HORIZONTAL, command=textSizeChange)
    slider.set(configFile["Text Size"])
    slider.grid(column=1, row=9, columnspan =2)
    
    global previewText
    previewText = tkscrolled.ScrolledText(master=settingsMenu,
        font=("Consolas",configFile["Text Size"]),
        selectbackground="grey35",
        bg="grey18",
        fg="white",
        wrap=tk.WORD,
        width=screenWidth,
        height=20,
        relief=tk.FLAT,
        cursor="arrow")
    
    previewText.vbar.config(width="0")
    previewText.grid(column=0, row=10, columnspan=4)

    previewText.insert(tk.END, "This is just preview text. Use the slider to adjust font size.")
    previewText.config(state=tk.DISABLED)

    cancelButton = tk.Button(master=settingsMenu, text="Close Settings Menu", command=lambda: closeWindow())
    cancelButton.grid(column=1, columnspan=2, row=11, padx=5, pady=5, sticky=tk.W)



#Show text on screen.
def displayNotes():
    #Resizes the text widget to fit the screen.
    global mode
    mode = "Notes" 
    label.pack_forget()
    text.config(state=tk.NORMAL)
    text.delete("0.0", tk.END)
    text.insert(tk.END, splitsNotesList[currentSplit % len(splitsNotesList)])
    text.config(state=tk.DISABLED)
    text.pack(fill="both", expand="True")

#Needlessly complicated way to display an image on the screen.
def displayMaps():
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




#Function that gets called when either the settings window or the main window listens to the keyboard.
def waitkeyPress(name=None, listening=False, running=False, i=None):
    while listening:
        event = keyboard.read_event()

        if event.event_type == keyboard.KEY_UP:
            attributeList = {"event_type": event.event_type, "scan_code": event.scan_code, "name": event.name, "is_keypad": event.is_keypad}
            configFile[name] = attributeList
            
            textDisplay = settingsMenu.grid_slaves(row=i, column=1)
            recordedKey = "Recorded: "
            if attributeList["is_keypad"] == True:
                recordedKey = recordedKey + "Numpad "
            
            recordedKey += str(attributeList["name"])
            
            textDisplay[0].config(text=recordedKey)
            
            listening = False
    while running:
        event = keyboard.read_event()
        attributeList = {"event_type": event.event_type, "scan_code": event.scan_code, "name": event.name, "is_keypad": event.is_keypad}
        
        if event.event_type == keyboard.KEY_UP:
            with open("config.yaml", "r") as f:
                keysToCheck = yaml.safe_load(f)
                if attributeList == keysToCheck["Next Split"]:
                    nextSplit()
                elif attributeList == keysToCheck["Undo Split"]:
                    undoSplit()
                elif attributeList == keysToCheck["Skip Split"]:
                    skipSplit()
                elif attributeList == keysToCheck["Next Map"]:
                    nextMap()
                elif attributeList == keysToCheck["Previous Map"]:
                    previousMap()
                elif attributeList == keysToCheck["Swap to Text/Maps"]:
                    modeSwap()
                elif attributeList == keysToCheck["Reset"]:
                    resetAll()
                elif attributeList == keysToCheck["Quit Program"]:
                    closeWindow()
                else:
                    print("Unrecognized hotkey")
    while not running and not listening:
        event = keyboard.read_event()
        attributeList = {"event_type": event.event_type, "scan_code": event.scan_code, "name": event.name, "is_keypad": event.is_keypad}
        
        if event.event_type == keyboard.KEY_UP:
            with open("config.yaml", "r") as f:
                keysToCheck = yaml.safe_load(f)
                if attributeList == keysToCheck["Quit Program"]:
                    closeWindow()
        
        
#Define button functionalities in Settings Menu.
#Button to set the corresponding hotkey
def hotkeyButton(i, name):
    textDisplay = settingsMenu.grid_slaves(row=i, column=1)
   
    textDisplay[0].config(text="Listening...")
    
    # start a seperate thread that waits for a global keyboard input
    t = threading.Thread(target=waitkeyPress, kwargs={"name": name, "listening": True, "i": i}, daemon=True)
    t.start()


#Define button functionality in the Main Menu.
def startRun():
    print("Started run")
    startButton.destroy()
    settingsButton.destroy()
    t = threading.Thread(target=waitkeyPress, kwargs={"running": True}, daemon=True)
    t.start()

    displayNotes()


#Save the window dimensions whenever the window is resized.
def resizedWindow(e):
    #Store the screen's dimensions and position in the YAML config file.
    latestDimensions = root.winfo_geometry() 

    configFile["screenDimensions"] = latestDimensions
    with open("config.yaml", "w") as f:
        settings = configFile
        settings = yaml.dump(settings, stream=f, default_flow_style=False, sort_keys=False)




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




def closeWindow():
    try: 
        if settingsMenu.focus_displayof():
            settingsMenu.destroy()
        else: 
            root.focus_displayof()
            root.destroy()
    except:
        if root.focus_displayof():
            root.destroy()

def closeSettingsMenu():
    settingsMenu.destroy()

def main():
    t = threading.Thread(target=waitkeyPress, daemon=True)
    t.start()
    
    text.bind("<Button-1>", lambda event: "break")
    root.bind("<Configure>", resizedWindow)
    root.mainloop()

if __name__ == "__main__":
    main()