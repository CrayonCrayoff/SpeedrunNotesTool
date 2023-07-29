# SpeedrunNotesTool

Latest build: https://github.com/CrayonCrayoff/SpeedrunNotesTool/releases/tag/SpeedrunNotesToolv0.0.2

A simple tool to show notes and maps during a speedrun.

This is my custom tool to display either text notes or maps. I use it for when I'm speedrunning.

Essentially, it keeps track of two lists: one for notes and one for maps.

For maps, it checks the folder called "maps". It takes all the files in this folder (please make sure there are only images in there), and then puts them in alphabetical order. So to get the maps to show up in the right order, the file names need to be in alphabetical order.

For the text notes, it will check the text file called TheNotes.txt and read all the lines from it. It determines where the end of a split is by looking for lines that start with the exact phrase "##End of Split##" (it's also case-sensitive). You can edit the text file to add in your own notes.
