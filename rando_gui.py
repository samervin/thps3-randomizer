import tkinter as tk
import rando2
import subprocess
import shutil
from pathlib import Path
from tkinter import filedialog
import contextlib

root = tk.Tk()
root.title("THPS3 Randomizer")
root.minsize(500, 500)

#########
# Globals
#########
thps3_directory = None

############
# Get folder
############
def click_directory():
    global thps3_directory
    thps3_directory = filedialog.askdirectory(title="Select your THPS3 installation directory")
    label_directory.config(text=f"Current THPS3 directory: {thps3_directory}")

button_directory = tk.Button(
    root,
    text="Set THPS3 directory",
    command=click_directory,
)
label_directory = tk.Label(
    root,
    text="THPS3 directory not set",
)

############
# Initialize
############
def click_initialize():
    label_initialize.config(text="Initializing...")
    thps3_data_dir = Path(thps3_directory, "Data")
    thps3_rando_dir = Path(thps3_directory, "rando/Data")
    shutil.copytree(thps3_data_dir, thps3_rando_dir, dirs_exist_ok=True)
    label_initialize.config(text=f"Files initialized in {thps3_rando_dir}")

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
    # Compile
    subprocess.run("javac -encoding Cp1252 qb-editor/*.java", shell=True)
    # Run
    thps3_data_dir = str(Path(thps3_directory, "rando/Data"))
    subprocess.run(f"java -cp qb-editor -Dfile.encoding=COMPAT WriteQBFiles {thps3_data_dir}/", shell=True)
    thps3_qdir_dir = Path(thps3_directory, "rando/Data/Scripts/qdir.txt")
    shutil.copy("outfiles/qdir.txt", thps3_qdir_dir)
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
    thps3_exe = Path(thps3_directory, "THPS3.exe")
    thps3_rando_dir = Path(thps3_directory, "rando")
    subprocess.Popen(thps3_exe, cwd=thps3_rando_dir)
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
    thps3_movies_dir = Path(thps3_directory, "rando/Data/MOVIES")
    with contextlib.suppress(FileNotFoundError):
        Path(thps3_movies_dir, "ATVI.mpg").unlink()
        Path(thps3_movies_dir, "gearbox.mpg").unlink()
        Path(thps3_movies_dir, "NSLogo.mpg").unlink()
        Path(thps3_movies_dir, "THPS3.mpg").unlink()
    
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

button_directory.pack()
label_directory.pack()
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