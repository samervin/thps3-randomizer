import tkinter as tk
import thps3_randomizer
import subprocess
import shutil
from pathlib import Path
from tkinter import filedialog
import contextlib


class THPS3GUI:
    def __init__(self, root: tk.Tk):
        tk.Button(
            root,
            text="Set THPS3 directory",
            command=self.click_directory,
        ).pack()
        self.label_directory = tk.Label(
            root,
            text="THPS3 directory not set",
        )
        self.label_directory.pack()
        tk.Button(
            root,
            text="Initialize files",
            command=self.click_initialize,
        ).pack()
        self.label_initialize = tk.Label(root, text="Ready to initialize files...")
        self.label_initialize.pack()
        tk.Button(
            root,
            text="Randomize files",
            command=self.click_randomize,
        ).pack()
        self.label_randomize = tk.Label(root, text="Ready to randomize files...")
        self.label_randomize.pack()
        tk.Button(
            root,
            text="Launch game",
            command=self.click_launch,
        ).pack()
        self.label_launch = tk.Label(root, text="Ready to launch game...")
        self.label_launch.pack()
        tk.Button(
            root,
            text="Remove intro movies",
            command=self.click_remove_intro,
        ).pack()
        self.label_remove_intro = tk.Label(root, text="Ready to remove intro movies...")
        self.label_remove_intro.pack()
        tk.Button(
            root,
            text="Remove music",
            command=self.click_remove_music,
        ).pack()
        self.label_remove_music = tk.Label(root, text="Ready to remove music...")
        self.label_remove_music.pack()
        self.level_order_shuffle = tk.BooleanVar(value=False)
        self.level_order_end_on_comp = tk.BooleanVar(value=True)
        tk.Checkbutton(
            root, text="Shuffle level order", variable=self.level_order_shuffle
        ).pack()
        tk.Checkbutton(
            root, text="End on competition level", variable=self.level_order_end_on_comp
        ).pack()
        self.minimum_unlock_goals = tk.IntVar(value=3)
        self.maximum_unlock_goals = tk.IntVar(value=6)
        tk.Label(root, text="Minimum goals required per career level").pack()
        tk.Spinbox(root, from_=0, to=9, textvariable=self.minimum_unlock_goals).pack()
        tk.Label(root, text="Maximum goals required per career level").pack()
        tk.Spinbox(root, from_=0, to=9, textvariable=self.maximum_unlock_goals).pack()
        self.score_shuffle = tk.BooleanVar(value=False)
        tk.Checkbutton(root, text="Shuffle scores", variable=self.score_shuffle).pack()
        self.min_sick_score = tk.IntVar(value=60)
        self.max_sick_score = tk.IntVar(value=500)
        self.min_gold_score = tk.IntVar(value=120)
        self.max_gold_score = tk.IntVar(value=200)
        tk.Label(root, text="Minimum sick score (first career level)").pack()
        tk.Spinbox(root, from_=10, to=1000, textvariable=self.min_sick_score).pack()
        tk.Label(root, text="Maximum sick score (last career level)").pack()
        tk.Spinbox(root, from_=10, to=1000, textvariable=self.max_sick_score).pack()
        tk.Label(root, text="Minimum gold score (first competition level)").pack()
        tk.Spinbox(root, from_=10, to=1000, textvariable=self.min_gold_score).pack()
        tk.Label(root, text="Maximum gold score (last competition level)").pack()
        tk.Spinbox(root, from_=10, to=1000, textvariable=self.max_gold_score).pack()
        self.stat_default = tk.IntVar(value=5)
        tk.Label(root, text="Starting stat level for all characters").pack()
        tk.Spinbox(root, from_=0, to=10, textvariable=self.stat_default).pack()
        self.require_deck_for_tape = tk.BooleanVar(value=False)
        tk.Checkbutton(
            root,
            text="Require deck for secret tape",
            variable=self.require_deck_for_tape,
        ).pack()
        self.require_deck_for_medal = tk.BooleanVar(value=False)
        tk.Checkbutton(
            root,
            text="Require deck for competition medals",
            variable=self.require_deck_for_medal,
        ).pack()
        self.min_level_time = tk.IntVar(value=120)
        self.max_level_time = tk.IntVar(value=120)
        tk.Label(root, text="Minimum time limit for normal levels").pack()
        tk.Spinbox(root, from_=30, to=3600, textvariable=self.min_level_time).pack()
        tk.Label(root, text="Maximum time limit for normal levels").pack()
        tk.Spinbox(root, from_=30, to=3600, textvariable=self.max_level_time).pack()

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
                self.level_order_shuffle.get(),
                self.level_order_end_on_comp.get(),
                self.minimum_unlock_goals.get(),
                self.maximum_unlock_goals.get(),
                self.score_shuffle.get(),
                self.min_sick_score.get(),
                self.max_sick_score.get(),
                self.min_gold_score.get(),
                self.max_gold_score.get(),
                self.stat_default.get(),
                self.require_deck_for_tape.get(),
                self.require_deck_for_medal.get(),
                self.min_level_time.get(),
                self.max_level_time.get(),
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
