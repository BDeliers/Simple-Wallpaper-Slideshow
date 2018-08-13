#!/usr/bin/python3
# -*-coding:Utf-8 -*

#CALL SAMPLE : ./simple-wallpaper-slideshow.py /path/to/folder recurrencyInSeconds
#CALL EXAMPLE : ./simple-wallpaper-slideshow.py /home/bdeliers/Pictures/WallpaperSlideshow 30

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
# Visual notification
import notify2

class WallpaperSlideshow:
	"""

		Simple wallpaper slideshow
		by BDeliers, August 2018
		Under GPL 3.0 License

		Simple wallpaper changer which changes your wallpaper randomly from a given directory on a defined interval on GNOME/Gconf based Linux desktop environments

	"""

	def __init__(self, wallpapersDir, interval):
		# Get window manager
		self._X_SERVER = environ["XDG_CURRENT_DESKTOP"]
		# Gconf setting
		self._GCONF_WALLPAPER = {
							"Deepin" : "com.deepin.wrap.gnome.desktop.background",
							"GNOME" : "org.gnome.desktop.background",
							"X-Cinnamon" : "org.cinnamon.desktop.background",
							"ubuntu:GNOME" : "org.gnome.desktop.background",
							"Unity" : "org.gnome.desktop.background"
						}

		# Remove '/' of end of dir
		if wallpapersDir.endswith('/'):
			wallpapersDir = wallpapersDir[:-1]

		# If valid directory and interval
		if (isdir(wallpapersDir) and int(interval) > 0):
			# Wallpapers directory
			self.wallpapersDir = wallpapersDir
			# Seconds between wallpaper change
			self.interval = int(interval)
			#
		else:
			raise Exception("Invalid wallpapers path or time interval")

	def listWallpapers(self):
		"""
			List all wallpapers from given directory path
		"""

		self.wallpapers = []

		# For all elements in directory
		for element in listdir(self.wallpapersDir):
			# If is png, jpeg or jpg, append to wallpapers list
			if (isfile(element) and element.lower().endswith(".png") or element.lower().endswith(".jpeg") or element.lower().endswith(".jpg")):
				self.wallpapers.append(element)

		self.wallpapers.sort()

	def setWallpaper(self, wallpaper):
		"""
			Set wallpaper with gsettings
		"""

		call("gsettings set {} picture-uri '{}'".format(self._GCONF_WALLPAPER[self._X_SERVER] ,wallpaper), shell=True)

	def runSlideshow(self):
		"""
			Run the slideshow
		"""

		# Get wallpapers
		self.listWallpapers()

		# Prepare notification
		notify2.init("Wallpaper Slideshow")
		notif = notify2.Notification("Wallpaper Slideshow", "Slideshow has started !", "settings")

		# Show notification
		notif.show()

		while True:
			# Shuffle wallpapers list
			shuffle(self.wallpapers)

			for wallpaper in self.wallpapers:
				# Set wallpaper
				self.setWallpaper("{}/{}".format(self.wallpapersDir, wallpaper))

				# Sleep
				sleep(self.interval)


if __name__ == "__main__":
	slideshow = WallpaperSlideshow(argv[1], argv[2])
	slideshow.runSlideshow()
