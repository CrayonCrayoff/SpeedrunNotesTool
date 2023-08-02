This is CrayonCrayoff's SpeedrunNotesTool. It can show text and images. 

Essentially, it keeps track of two lists: one for notes and one for maps. 

For maps, it checks the folder called "maps". It takes all the files in this folder (please make sure there are only images in there), and then puts them in alphabetical order. So to get the maps to show up in the right order, the file names need to be in alphabetical order.

For the text notes, it will check the text file called TheNotes.txt and read all the lines from it. It determines where the end of a split is by looking for lines that start with the exact phrase "##End of Split##" (it's also case-sensitive). You can edit the text file to add in your own notes. 

The hotkeys it responds to are hard-coded in. There is currently no way to edit these, but I'm hoping to add that functionality sometime soon. The hotkeys for this build are as follows:

Next Split		= F1
Undo Split		= F3
Skip Split		= F4
Next Map		= F5
Previous Map		= F6
Reset		= F2
Swap Modes		= F8
Close Program 		= Escape

All of these hotkeys will work even if the program is running in the background. It doesn't need to be in focus. To prevent accidental closing of the program, the "Close Program" hotkey will only work if the program is in focus. 

You can quit the program by pressing the close button at the top right. 

Finally, the tool can be resized to whatever size you like. It will adjust horizontal text wrapping (for notes) and image size (for maps) to fit the screen. Unfortunately, it won't save these dimensions (also something I will add eventually), so it will always start up with the same dimensions. 