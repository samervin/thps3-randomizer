import os
from pathlib import Path

parent_folder = Path().cwd().parent
outfile_folder = parent_folder.joinpath("outfiles/")
data_folder = parent_folder.joinpath("fake-data/")

def read_windows_file(filepath):
    with open(filepath, 'r') as f:
        return f.readlines()

def write_qb_file(data, filepath):
    filepath.parent.mkdir(exist_ok=True, parents=True)
    with open(filepath, 'w', newline='\n') as f:
        f.writelines(data)

for outfile_path in outfile_folder.rglob("*.out"):
    data = read_windows_file(outfile_path)
    relative_path = outfile_path.relative_to(outfile_folder)
    data_path = data_folder.joinpath(relative_path).with_suffix(".qb")
    write_qb_file(data, data_path)
