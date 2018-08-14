#!/usr/bin/python3
# -*-coding:Utf-8 -*

# Tkinter
import tkinter as tk
from tkinter import filedialog
# Wallpaper Slideshow
from WallpaperSlideshow import WallpaperSlideshow
# Copy file
from shutil import copyfile
# User directory, is file
from os.path import expanduser, isfile
# Remove file
from os import remove

# Home folder
HOME = expanduser("~")

def desktopEntryCreator(name, genericName, comment, command, autostartDelay):
    text = "[Desktop Entry]\n"
    text += "Version=1.0\n"
    text += "Name={}\n".format(name)
    text += "GenericName={}\n".format(name)
    text += "Comment={}\n".format(comment)
    text += "Exec={}\n".format(command)
    text += "Type=Application\n"
    text += "Terminal=false\n"
    text += "X-GNOME-Autostart-Delay={}\n".format(autostartDelay)

    return text

class UI(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent
        self.wallpapersDir = "/home"
        self.slideshow = WallpaperSlideshow("/home", 30)

        self._script = "{}/.WallpaperSlideshow.py".format(HOME)
        self._desktopEntry = "{}/.config/autostart/wallpaper-slideshow.desktop".format(HOME)

        self.parent.option_add("*Font", "Helvetica 10")

        self.directoryFrame()
        self.filesListFrame()
        self.settingsFrame()

    def browseButtonAction(self):
        self.wallpapersDir = filedialog.askdirectory(initialdir="~/")
        self.pathEntry.delete(0, tk.END)
        self.pathEntry.insert(0, self.wallpapersDir)

        self.refreshButtonAction()

    def refreshButtonAction(self):
        self.wallpapersDir = self.pathEntry.get()
        self.slideshow.wallpapersDir = self.wallpapersDir
        self.slideshow.listWallpapers()

        self.filesList.delete(0, tk.END)

        for wallpaper in self.slideshow.wallpapers:
            self.filesList.insert(tk.END, wallpaper.split('.')[0])

    def runButtonAction(self):
        if self.runButton["text"] == "Run":
            self.slideshow.interval = int(self.intervalEntry.get())
            self.slideshow.runSlideshow()
            self.runButton["text"] = "Stop"
        else:
            self.slideshow.stopSlideshow()
            self.runButton["text"] = "Run"

    def onStartupButtonAction(self):
        self.slideshow.interval = int(self.intervalEntry.get())

        if len(self.slideshow.wallpapers) and self.slideshow.interval > 0:

            desktopEntry = desktopEntryCreator("Wallpaper Slideshow", "Wallpaper Slideshow", "Simple wallpaper slideshow", "python3 {}".format(self._script), self.slideshow.interval)

            copyfile("./WallpaperSlideshow.py", self._script)

            f = open(self._desktopEntry, "w+")
            f.write(desktopEntry)
            f.close()

            self.onStartupButton["text"] = "Added to startup"

    def removeStartupButtonAction(self):
        if isfile(self._script):
            remove(self._script)

        if isfile(self._desktopEntry):
            remove(self._desktopEntry)
            self.removeStartupButton["text"] = "Removed from startup"
            self.onStartupButton["text"] = "Add to startup"

    def directoryFrame(self):
        self.directoryFrame = tk.Frame(master=self)
        self.directoryFrame.grid(pady=8, padx=8, row=0, sticky=tk.W)

        tk.Label(self.directoryFrame, text="Wallpapers Directory:").grid(row=0, column=0, sticky=tk.W, padx=4)

        self.pathEntry = tk.Entry(self.directoryFrame)
        self.pathEntry.grid(row=0, column=1, columnspan=2, sticky=tk.W, padx=2)

        self.browseButton = tk.Button(self.directoryFrame, text="Browse", command=self.browseButtonAction)
        self.browseButton.grid(row=0, column=3, padx=4, sticky=tk.E)

    def filesListFrame(self):
        self.filesFrame = tk.Frame(master=self)
        self.filesFrame.grid(padx=8, pady=8, row=1, sticky=tk.W)

        tk.Label(self.filesFrame, text="Your wallpapers:").grid(row=0, column=0, sticky=tk.NW, padx=4)

        self.refreshButton = tk.Button(self.filesFrame, text="Refresh", command=self.refreshButtonAction)
        self.refreshButton.grid(row=1, column=1, pady=4)

        self.filesList = tk.Listbox(self.filesFrame)
        self.filesList.grid(row=0, column=1)

        self.scrollbar = tk.Scrollbar(self.filesFrame, orient=tk.VERTICAL)
        self.scrollbar.config(command=self.filesList.yview)

        self.filesList.config(yscrollcommand=self.scrollbar.set)

        self.scrollbar.grid(row=0, column=2)

    def settingsFrame(self):
        self.settingsFrame = tk.Frame(master=self)
        self.settingsFrame.grid(pady=8, padx=8, row=2)

        tk.Label(self.settingsFrame, text="Change interval (in sec):").grid(row=0, column=0, sticky=tk.W)

        self.intervalEntry = tk.Spinbox(self.settingsFrame, from_=0, values=(30, 60, 120, 300, 600, 900, 1200, 1800, 3600))
        self.intervalEntry.grid(row=0, column=1, sticky=tk.W, padx=2)

        self.runButton = tk.Button(self.settingsFrame, text="Run", command=self.runButtonAction)
        self.runButton.grid(row=1, column=0, pady=2)
        self.onStartupButton = tk.Button(self.settingsFrame, text="Launch on startup", command=self.onStartupButtonAction)
        self.onStartupButton.grid(row=1, column=1, pady=2, sticky=tk.E)
        self.removeStartupButton = tk.Button(self.settingsFrame, text="Remove from startup", command=self.removeStartupButtonAction)
        self.removeStartupButton.grid(row=1, column=2, pady=2, sticky=tk.E)

if __name__ == "__main__":
    root = tk.Tk()
    root.title("Wallpaper Changer")

    img = tk.PhotoImage(file="./icon.png")

    root.tk.call("wm", "iconphoto", root._w, img)

    app = UI(root)
    app.pack()

    app.mainloop()
