#!/usr/bin/python3
# -*-coding:Utf-8 -*

"""

	Simple wallpaper slideshow
	by BDeliers, August 2018
	Under GPL 3.0 License

	Simple wallpaper changer which chnages your wallpaper randomly from a given directory on a defined interval

	CALL SAMPLE : ./simple-wallpaper-slideshow.py /path/to/folder recurrencyInSeconds
	CALL EXAMPLE : ./simple-wallpaper-slideshow.py /home/bdeliers/Pictures/WallpaperSlideshow 30

"""

# Environment variables, list directory
from os import environ, listdir
# Is directory, is file
from os.path import isdir, isfile
# Argv
from sys import argv
# Sleep
from time import sleep
# Shuffle list
from random import shuffle
# Call bash command
from subprocess import call

# Get window manager
X_SERVER = environ["XDG_CURRENT_DESKTOP"]
# Gconf setting
GCONF_WALLPAPER = {
					"Deepin" : "com.deepin.wrap.gnome.desktop.background",
					"GNOME" : "org.gnome.desktop.background",
					"X-Cinnamon" : "org.cinnamon.desktop.background",
					"ubuntu:GNOME" : "org.gnome.desktop.background",
					"Unity" : "org.gnome.desktop.background"
				}

# Wallpapers directory
WALLPAPERS_PATH = argv[1]
# Seconds between wallpaper change
RECURRENCY = int(argv[2])

# If invalid arguments
if (RECURRENCY < 0 or isdir(WALLPAPERS_PATH) == False):
	print("ERROR : INVALID RECURRENCY OR PATH OR EMPTY DESTINATION DIRECTORY")
	exit()

wallpapers = []

# For all elements in directory
for element in listdir(WALLPAPERS_PATH):
	# If is png, jpeg or jpg, append to wallpapers list
	if (isfile(element) and element.lower().endswith(".png") or element.lower().endswith(".jpeg") or element.lower().endswith(".jpg")):
		wallpapers.append(element)

# Shuffle directory
shuffle(wallpapers)
i = 0

# Forever
while True:
	# Set wallpaper
	call("gsettings set " + GCONF_WALLPAPER[X_SERVER] + " picture-uri " + WALLPAPERS_PATH + '/' + wallpapers[i], shell=True)

	i += 1
	if i == len(wallpapers):
		i = 0

	# Pause between 2 changes
	sleep(RECURRENCY)
