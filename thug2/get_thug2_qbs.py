import os
import subprocess
from pathlib import Path

all_paths: list[Path] = []

for root, dirs, files in os.walk("C:/Users/Sam/Documents/THUG2/Game/Data/levels"):
    for file in files:
        if(file.endswith('.qb')):
            all_paths.append(Path(root, file))

for path in all_paths:
    outpath = Path("C:/Users/Sam/Documents/thps3-randomizer/thug2/thug2-qbs/levels") / path.relative_to("C:/Users/Sam/Documents/THUG2/Game/Data/levels")
    subprocess.run(f"C:/Users/Sam/Documents/thps3-randomizer/thug2/QScript/QScript.QDecompile.App.exe -input {path} -output {outpath}", shell=True)