# Simple Wallpaper Slideshow
Simple wallpaper changer which changes your wallpaper randomly from a given directory on a defined interval.  
Works on GNOME/gsettings based Linux distros.  
**by BDeliers, August 2018**  
Under GPL V3 License  

---

This program features a GUI to select the wallpapers diretory and the time interval. After that, you can run the wallpaper slideshow or add it to your system startup.  
Standalone compiled version is available in the "Release" pane.

For now, it supports these desktop environments :

    - Deepin Linux DDE
    - GNOME
    - Cinnamon
    - Unity
    - Ubuntu GNOME

If your desktop environment is GNOME-based and not listed above, contact me and I'll try to add it !

### Screenshot :
![Screenshot](https://raw.githubusercontent.com/BDeliers/Simple-Wallpaper-Slideshow/master/Sreenshot.png)

---

### How it works

It's a Python-based UI made with TKinter.
The code sets wallpaper with gsettings.
When you choose to add the script to startup, it creates a .desktop file in `~/.config/autostart` executing the program, which is stored to `~/.WallpaperSlideshow`.
