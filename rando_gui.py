import tkinter as tk
import thps3_randomizer
import subprocess
import shutil
from pathlib import Path
from tkinter import filedialog
import contextlib


class THPS3GUI:
    def __init__(self, root: tk.Tk):
        self.button_directory = tk.Button(
            root,
            text="Set THPS3 directory",
            command=self.click_directory,
        )
        self.label_directory = tk.Label(
            root,
            text="THPS3 directory not set",
        )
        self.button_initialize = tk.Button(
            root,
            text="Initialize files",
            command=self.click_initialize,
        )
        self.label_initialize = tk.Label(root, text="Ready to initialize files...")
        self.button_randomize = tk.Button(
            root,
            text="Randomize files",
            command=self.click_randomize,
        )
        self.label_randomize = tk.Label(root, text="Ready to randomize files...")
        self.button_launch = tk.Button(
            root,
            text="Launch game",
            command=self.click_launch,
        )
        self.label_launch = tk.Label(root, text="Ready to launch game...")
        self.button_remove_intro = tk.Button(
            root,
            text="Remove intro movies",
            command=self.click_remove_intro,
        )
        self.label_remove_intro = tk.Label(root, text="Ready to remove intro movies...")
        self.button_remove_music = tk.Button(
            root,
            text="Remove music",
            command=self.click_remove_music,
        )
        self.label_remove_music = tk.Label(root, text="Ready to remove music...")
        self.level_order_shuffle = tk.BooleanVar()
        self.level_order_end_on_comp = tk.BooleanVar(value=True)
        self.checkbutton_level_order_shuffle = tk.Checkbutton(
            root, text="Shuffle level order", variable=self.level_order_shuffle
        )
        self.checkbutton_level_order_end_on_comp = tk.Checkbutton(
            root, text="End on competition level", variable=self.level_order_end_on_comp
        )
        self.button_directory.pack()
        self.label_directory.pack()
        self.button_initialize.pack()
        self.label_initialize.pack()
        self.button_randomize.pack()
        self.label_randomize.pack()
        self.button_launch.pack()
        self.label_launch.pack()
        self.button_remove_intro.pack()
        self.label_remove_intro.pack()
        self.button_remove_music.pack()
        self.label_remove_music.pack()
        self.checkbutton_level_order_shuffle.pack()
        self.checkbutton_level_order_end_on_comp.pack()

    def click_directory(self):
        self.thps3_directory = filedialog.askdirectory(
            title="Select your THPS3 installation directory"
        )
        if self.thps3_directory:
            self.label_directory.config(
                text=f"Current THPS3 directory: {self.thps3_directory}"
            )

    def click_initialize(self):
        if self.thps3_directory:
            self.label_initialize.config(text="Initializing...")
            thps3_data_dir = Path(self.thps3_directory, "Data")
            thps3_rando_dir = Path(self.thps3_directory, "rando/Data")
            shutil.copytree(thps3_data_dir, thps3_rando_dir, dirs_exist_ok=True)
            self.label_initialize.config(text=f"Files initialized in {thps3_rando_dir}")

    def click_randomize(self):
        if self.thps3_directory:
            self.label_randomize.config(text="Randomizing...")
            # Randomize files
            thps3_randomizer.randomize(
                self.level_order_shuffle.get(), self.level_order_end_on_comp.get()
            )
            # Compile Java
            subprocess.run("javac -encoding Cp1252 qb_editor/*.java", shell=True)
            # Run Java
            thps3_data_dir = str(Path(self.thps3_directory, "rando/Data"))
            subprocess.run(
                f"java -cp qb_editor -Dfile.encoding=COMPAT WriteQBFiles {thps3_data_dir}/",
                shell=True,
            )
            thps3_qdir_dir = Path(self.thps3_directory, "rando/Data/Scripts/qdir.txt")
            shutil.copy("qbs_outfiles/qdir.txt", thps3_qdir_dir)
            # Done
            self.label_randomize.config(text="Files randomized!")

    def click_launch(self):
        if self.thps3_directory:
            self.label_launch.config(text="Launching game...")
            thps3_exe = Path(self.thps3_directory, "THPS3.exe")
            thps3_rando_dir = Path(self.thps3_directory, "rando")
            subprocess.Popen(thps3_exe, cwd=thps3_rando_dir)
            self.label_launch.config(text="Game launched!")

    def click_remove_intro(self):
        if self.thps3_directory:
            self.label_remove_intro.config(text="Removing intro movies...")
            thps3_movies_dir = Path(self.thps3_directory, "rando/Data/MOVIES")
            with contextlib.suppress(FileNotFoundError):
                Path(thps3_movies_dir, "ATVI.mpg").unlink()
                Path(thps3_movies_dir, "gearbox.mpg").unlink()
                Path(thps3_movies_dir, "NSLogo.mpg").unlink()
                Path(thps3_movies_dir, "THPS3.mpg").unlink()
            self.label_remove_intro.config(text="Intro movies removed!")

    def click_remove_music(self):
        if self.thps3_directory:
            self.label_remove_music.config(text="Removing music...")
            thps3_music_dir = Path(self.thps3_directory, "rando/Data/music")
            with contextlib.suppress(FileNotFoundError):
                Path(thps3_music_dir, "ace.mus").unlink()
                Path(thps3_music_dir, "adol.mus").unlink()
                Path(thps3_music_dir, "afi.mus").unlink()
                Path(thps3_music_dir, "antfarm.mus").unlink()
                Path(thps3_music_dir, "bodyjar.mus").unlink()
                Path(thps3_music_dir, "chilis.mus").unlink()
                Path(thps3_music_dir, "cky.mus").unlink()
                Path(thps3_music_dir, "del.mus").unlink()
                Path(thps3_music_dir, "gangsta.mus").unlink()
                Path(thps3_music_dir, "gangsta2.mus").unlink()
                Path(thps3_music_dir, "gutter.mus").unlink()
                Path(thps3_music_dir, "krs.mus").unlink()
                Path(thps3_music_dir, "mad.mus").unlink()
                Path(thps3_music_dir, "next.mus").unlink()
                Path(thps3_music_dir, "ozo.mus").unlink()
                Path(thps3_music_dir, "pain.mus").unlink()
                Path(thps3_music_dir, "ramones.mus").unlink()
                Path(thps3_music_dir, "redman.mus").unlink()
                Path(thps3_music_dir, "rev.mus").unlink()
                Path(thps3_music_dir, "rollins.mus").unlink()
                Path(thps3_music_dir, "xzibit.mus").unlink()
                Path(thps3_music_dir, "zebra.mus").unlink()
            self.label_remove_music.config(text="Music removed!")


def gui():
    root = tk.Tk()
    root.title("THPS3 Randomizer")
    root.minsize(500, 500)
    THPS3GUI(root)
    root.mainloop()


if __name__ == "__main__":
    gui()
