import tkinter as tk
import rando2
import subprocess
import shutil
import pathlib

root = tk.Tk()
root.title("THPS3 Randomizer")
root.minsize(500, 500)

############
# Initialize
############
def click_initialize():
    label_initialize.config(text="Initializing...")
    shutil.copytree("C:/Users/Sam/Documents/THPS3/Data/", "C:/Users/Sam/Documents/THPS3/rando/Data/", dirs_exist_ok=True)
    label_initialize.config(text="Files initialized!")

button_initialize = tk.Button(
    root,
    text="Initialize files",
    command=click_initialize,
)
label_initialize = tk.Label(
    root,
    text="Ready to initialize files..."
)

###########
# Randomize
###########
def click_randomize():
    label_randomize.config(text="Randomizing...")
    rando2.rando()
    label_randomize.config(text="Files randomized!")

button_randomize = tk.Button(
    root,
    text="Randomize files",
    command=click_randomize,
)
label_randomize = tk.Label(
    root,
    text="Ready to randomize files..."
)

############
# Copy files
############
def click_copy():
    label_copy.config(text="Copying files...")
    subprocess.run("javac -encoding Cp1252 qb-editor/*.java", shell=True)
    subprocess.run("java -cp qb-editor -Dfile.encoding=COMPAT WriteQBFiles", shell=True)
    shutil.copy("outfiles/qdir.txt", "C:/Users/Sam/Documents/THPS3/rando/Data/Scripts/qdir.txt")
    label_copy.config(text="Files copied!")

button_copy = tk.Button(
    root,
    text="Copy files",
    command=click_copy,
)
label_copy = tk.Label(
    root,
    text="Ready to copy files..."
)

#############
# Launch game
#############
def click_launch():
    label_launch.config(text="Launching game...")
    subprocess.Popen("C:/Users/Sam/Documents/THPS3/THPS3.exe", cwd="C:/Users/Sam/Documents/THPS3/rando/")
    label_launch.config(text="Game launched!")

button_launch = tk.Button(
    root,
    text="Launch game",
    command=click_launch,
)
label_launch = tk.Label(
    root,
    text="Ready to launch game..."
)

##############
# Remove intro
##############
def click_remove_intro():
    label_remove_intro.config(text="Removing intro movies...")
    pathlib.Path("C:/Users/Sam/Documents/THPS3/rando/Data/MOVIES/ATVI.mpg").unlink()
    pathlib.Path("C:/Users/Sam/Documents/THPS3/rando/Data/MOVIES/gearbox.mpg").unlink()
    pathlib.Path("C:/Users/Sam/Documents/THPS3/rando/Data/MOVIES/NSLogo.mpg").unlink()
    pathlib.Path("C:/Users/Sam/Documents/THPS3/rando/Data/MOVIES/THPS3.mpg").unlink()
    label_remove_intro.config(text="Intro movies removed!")

button_remove_intro = tk.Button(
    root,
    text="Remove intro movies",
    command=click_remove_intro,
)
label_remove_intro = tk.Label(
    root,
    text="Ready to remove intro movies..."
)

button_initialize.pack()
label_initialize.pack()
button_randomize.pack()
label_randomize.pack()
button_copy.pack()
label_copy.pack()
button_launch.pack()
label_launch.pack()
button_remove_intro.pack()
label_remove_intro.pack()
root.mainloop()