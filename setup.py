from cx_Freeze import setup, Executable

executable = Executable(
                script = "./GUI.py",
                icon = "./icon.png",
                targetName = "WallpaperSlideshow",
            )

includefiles = ["./icon.png"]

setup(
    name = "WallpaperSlideshow",
    version = "1.0",
    description = "Simple wallpaper slideshow GUI manager",
    executables = [executable],
    author = "BDeliers",
    options = {"build_exe" : {"include_files" : includefiles}},
)
