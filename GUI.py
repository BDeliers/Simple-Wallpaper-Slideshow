#!/usr/bin/python3
# -*-coding:Utf-8 -*

# Tkinter
import tkinter as tk
from tkinter import filedialog
# Wallpaper Slideshow
from WallpaperSlideshow import WallpaperSlideshow

class UI(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent
        self.wallpapersDir = "/home"
        self.slideshow = WallpaperSlideshow("/home", 30)

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

        for wallpaper in self.slideshow.wallpapers:
            self.filesList.insert(tk.END, wallpaper.split('.')[0])

    def runButtonAction(self):
        self.slideshow.interval = int(self.intervalEntry.get())
        #self.slideshow.runSlideshow()


    def directoryFrame(self):
        self.directoryFrame = tk.Frame(master=self)
        self.directoryFrame.grid(pady=8, padx=8, row=0)

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
        self.onrunupButton = tk.Button(self.settingsFrame, text="Launch on Linux startup")
        self.onrunupButton.grid(row=1, column=1, pady=2)

if __name__ == "__main__":
    root = tk.Tk()
    root.title("Wallpaper Changer")

    app = UI(root)
    app.pack()

    app.mainloop()
