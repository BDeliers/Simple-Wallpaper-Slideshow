#!/usr/bin/python3
# -*-coding:Utf-8 -*

# Tkinter
import tkinter as tk
from tkinter import filedialog
# Theming Tkinter
import tkinter.ttk as ttk
from ttkthemes import ThemedTk
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

class UI(ttk.Frame):
    def __init__(self, parent, *args, **kwargs):
        ttk.Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent
        self.wallpapersDir = "/home"
        self.slideshow = WallpaperSlideshow("/home", 30)

        self._script = "{}/.WallpaperSlideshow.py".format(HOME)
        self._desktopEntry = "{}/.config/autostart/wallpaper-slideshow.desktop".format(HOME)

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

        self.filesList.delete(*self.filesList.get_children())

        for wallpaper in self.slideshow.wallpapers:
            self.filesList.insert('', "end", text=wallpaper.split('.')[0])

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

            desktopEntry = desktopEntryCreator("Wallpaper Slideshow", "Wallpaper Slideshow", "Simple wallpaper slideshow", "python3 {} {} {}".format(self._script, self.slideshow.wallpapersDir, self.slideshow.interval), self.slideshow.interval)

            copyfile("./WallpaperSlideshow.py", self._script)

            f = open(self._desktopEntry, "w+")
            f.write(desktopEntry)
            f.close()

            self.onStartupButton["text"] = "Added to startup"
            self.removeStartupButton["text"] = "Remove from startup"

    def removeStartupButtonAction(self):
        if isfile(self._script):
            remove(self._script)

        if isfile(self._desktopEntry):
            remove(self._desktopEntry)
            self.removeStartupButton["text"] = "Removed from startup"
            self.onStartupButton["text"] = "Launch on startup"

    def directoryFrame(self):
        self.directoryFrame = ttk.Frame(master=self)
        self.directoryFrame.grid(pady=8, padx=8, row=0, sticky=tk.W)

        ttk.Label(self.directoryFrame, text="Wallpapers Directory:").grid(row=0, column=0, sticky=tk.W, padx=4)

        self.pathEntry = ttk.Entry(self.directoryFrame)
        self.pathEntry.grid(row=0, column=1, columnspan=2, sticky=tk.W, padx=2)

        self.browseButton = ttk.Button(self.directoryFrame, text="Browse", command=self.browseButtonAction)
        self.browseButton.grid(row=0, column=3, padx=4, sticky=tk.E)

    def filesListFrame(self):
        self.filesFrame = ttk.Frame(master=self)
        self.filesFrame.grid(padx=8, pady=8, row=1, sticky=tk.W)

        ttk.Label(self.filesFrame, text="Your wallpapers:").grid(row=0, column=0, sticky=tk.NW, padx=4)

        self.refreshButton = ttk.Button(self.filesFrame, text="Refresh", command=self.refreshButtonAction)
        self.refreshButton.grid(row=1, column=1, pady=4)

        self.filesList = ttk.Treeview(self.filesFrame)
        self.filesList.grid(row=0, column=1)

        self.scrollbar = ttk.Scrollbar(self.filesFrame, orient=tk.VERTICAL)
        self.scrollbar.config(command=self.filesList.yview)

        self.filesList.config(yscrollcommand=self.scrollbar.set)

        self.scrollbar.grid(row=0, column=2, sticky=tk.N+tk.S+tk.W)

    def settingsFrame(self):
        self.settingsFrame = ttk.Frame(master=self)
        self.settingsFrame.grid(padx=8, row=2)
        ttk.Label(self.settingsFrame, text="Change interval (in sec):").grid(row=0, column=0, sticky=tk.W)

        self.intervalEntry = ttk.Combobox(self.settingsFrame, values=(30, 60, 120, 300, 600, 900, 1200, 1800, 3600))
        self.intervalEntry.set(30)
        self.intervalEntry.grid(row=0, column=1, sticky=tk.W, padx=2)

        self.runButton = ttk.Button(self.settingsFrame, text="Run", command=self.runButtonAction)
        self.runButton.grid(row=1, column=0, pady=8)
        self.onStartupButton = ttk.Button(self.settingsFrame, text="Launch on startup", command=self.onStartupButtonAction)
        self.onStartupButton.grid(row=1, column=1, pady=8, sticky=tk.E)
        self.removeStartupButton = ttk.Button(self.settingsFrame, text="Remove from startup", command=self.removeStartupButtonAction)
        self.removeStartupButton.grid(row=1, column=2, pady=8, sticky=tk.E)

if __name__ == "__main__":
    root = ThemedTk()
    root.title("Wallpaper Changer")

    img = tk.PhotoImage(file="./icon.png")

    root.tk.call("wm", "iconphoto", root._w, img)

    root.set_theme("arc")

    root.grid_columnconfigure(0, weight=1)

    app = UI(root)
    app.pack()

    app.mainloop()
