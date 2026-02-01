import tkinter as tk
from tkinter import ttk
import importlib
import rando2
import subprocess

root = tk.Tk()
root.title("THPS3 Randomizer")
root.minsize(500, 500)

def on_click():
    rando2.rando()

button = tk.Button(
    root,
    text="Randomize files",
    command=on_click,
)
button.pack(padx=5, pady=5)

root.mainloop()