
*StreamHelper* is a program to centralize and simplify the creation and updating of textfiles with set names.

It is mainly intended for small to semi-professional streamers, who need to control a rather large amount of textfiles while streaming (e. g. OBS, Streamlabs, etc.)


#### These third party libraries are being used by the program:

 -  [PyQt5 Gui, Widgets, Core](https://pypi.org/project/PyQt5/)
 - [pyperclip](https://pypi.org/project/pyperclip/)
 
StreamHelper is implemented in **python** and is being distributed with the help of  [pyinstaller](https://www.pyinstaller.org/) and [innoSetup](https://jrsoftware.org/isinfo.php) 

## Installation
Since this is *not* a signed installer, Windows Smart Screen will warn you on installation. This is normal and perfectly fine and cannot be circumvented at the moment. 

GitHub download speeds are sometimes pretty low. To ease access to the installer, I also uploaded the file on mega:
https://mega.nz/folder/JOxmABTQ#Dn8tYTcBoKMxezW61TWK0A

1. Open the installer by double-clicking
2. Select, if you want to install the program for *all users (recommended)* or just the current one
3. Accept the license and set the path
4. Read the FAQ and the changelog
5. Start the  program from the location or your desktop

0.3.1 has not been packed into an installer. If you want to use it, download from mega, extract where you want to and run.

There shouldn't be any issues, since this process is straightforward.
*Note (Pre-0.3.1): StreamHelper can only be started from the wizard if you gave it elevated privileges, otherwise it will fail. This is expected, since the program is only able to run with elevation!*

## Startup
On startup, a folder will be created at *C:\Users\\<username\>\AppData\Local\StreamHelper* and all basic files will get created. This includes:

- The  autosave
	
- The config file
		
- The folder *textfiles* with all subfolders *Lists*, *eSports* and *API (unused in 0.3)*

The program on any version before 0.3.1 will *not* start if you don't have elevated privileges! 
From this version onwards, the program will ask for these privileges as soon as it needs it.

## Usage
Using this program is straightforward and rather simple, there are tooltips for most buttons and sections. However, there are some things to know before starting to produce with it:

- The eSports tab will auto-update every line edit to the corresponding text file when its focus is lost (if you click somewhere else), to save the contents to the autosave though, you will have to use the "save" button on each section
- The "auto-update lists" setting is only applicable for list items and will update them as soon as you click somewhere else. If it is turned off, the files will only update if you manually press the "update" button. To autosave them, you will still need to use the "update" button regardless of the setting.
- Resetting the settings only takes full effect on a restart of the application
- Swapping two items/contents automatically updates the corresponding textfiles.
- Naming the lists only has an effect if "List-Split" is activated.
- You can export settings by copying your "config.json" somewhere else. If you move it instead your settings get reset.
- Deleting folders manually while using the program might cause StreamHelper to crash (known bug)
- Keyboard shortcuts "ctrl+l, ctrl+v" for loading of files is deactivated (known bug)

A complete list of changes, documentation and bugs is in the works, however, since interest on this project is low at best, these will take some time.

More will be added to this list until I have a proper documentation with tutorials. Currently though, since the application isn't too big, please bear with me if I focus on programming.

If you happen to have any questions regarding usage of this program, feel free to ask me, write me an e-mail or dm me on Discord (Witheria #4806)!

## Deinstallation
You can deinstall StreamHelper from the "installed programs" section within your PC's settings. 

0.3.1: Simply delete the directory you decided to put the files and the appdata folder.


### Thank you for being a part of this project!


[Donate...](https://www.paypal.com/donate?hosted_button_id=825RPFTRDCW7A)




    © Toni Schmidbauer 2020 / Released under GPL v3
 
    Bugs, problems, critique: schmidbauer.biz@gmail.com
