# THPS3 Randomizer

A work-in-progress randomizer for THPS3 for PC.

## Running locally

Prerequisites:
- THPS3 installed, ideally in a user-owned folder (i.e. _not_ Program Files, otherwise you will need admin permissions for everything)
    - Highly recommended: [PARTYMOD](https://github.com/PARTYMANX/partymod-thps3) installed
- Python installed (I have 3.14.2 installed myself)
- Java JDK installed (I have 25.0.2 installed myself)

To randomize THPS3, run `py rando_gui.py` and do the following:
- Set your THPS3 directory
- "Initialize" the randomizer
- Randomize files
- Optionally, remove the sound and music
- Launch the now-randomized game

### Thanks

- byxor for helping me get started and providing information on scripting and engine functions
- Vadru and inoX for creating THQBEditor, from which much of the `/qb-editor` code comes from (with permission)
