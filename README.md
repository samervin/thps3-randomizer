# THPS3 Randomizer

A work-in-progress randomizer for THPS3 for PC.

## Running locally

Prerequisites:
- THPS3 installed, ideally in a user-owned folder (i.e. _not_ Program Files, otherwise you will need admin permissions for everything)
    - Highly recommended: [PARTYMOD](https://github.com/PARTYMANX/partymod-thps3) installed
- Python installed (I have 3.10 installed myself)
- Java JDK installed (I have 21.0.2 installed myself)

To randomize THPS3, run these commands:
- `cd rando`
- `py rando.py`
- You'll need to write the files generated by the randomizer (see below)

To write the files generated by the randomizer in `/outfiles`, run these commands:
- `cd qb-editor`
- `set THPS3_DATA_FOLDER=C:/Path/To/THPS3/Data/`
- `javac -encoding Cp1252 *.java && java -Dfile.encoding=COMPAT WriteQBFiles`

All the QB files that ship with THPS3 are included in `/vanilla-qbs` but if you want to regenerate them, the process is similar:
- `cd qb-editor`
- `set THPS3_DATA_FOLDER=C:/Path/To/THPS3/Data/`
- `javac -encoding Cp1252 *.java && java -Dfile.encoding=COMPAT ReadQBFiles`

### Thanks

- byxor for helping me get started and providing information on scripting and engine functions
- Vadru and inoX for creating THQBEditor, from which much of the `/qb-editor` code comes from (with permission)
