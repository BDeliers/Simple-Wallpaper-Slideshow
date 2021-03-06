from cx_Freeze import setup, Executable

# Import python modules
from sys import path
path.append("./src")

executable = Executable(
                script = "./src/GUI.py",
                icon = "./src/icon.png",
                targetName = "WallpaperSlideshow",
            )

includefiles = ["./src/icon.png"]
packages = ["WallpaperSlideshow"]
includes = ["tkinter", "ttkthemes", "shutil", "os", "sys", "time", "random", "subprocess", "threading", "notify2"]

setup(
    name = "WallpaperSlideshow",
    version = "1.0",
    description = "Simple wallpaper slideshow GUI manager",
    executables = [executable],
    author = "BDeliers",
    options = {"build_exe" : {"include_files" : includefiles, "packages" : packages, "includes" : includes}},
)
