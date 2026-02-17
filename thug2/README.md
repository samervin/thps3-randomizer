This is a temporary holding place for my THUG2 work.

How to reproduce the silent hot rod (and presumably more such script changes):
- Use QScript.QDecompile.App.exe on manualtricks.qb
- Edit the `Trick_HotRod` struct to remove the `stream = Spec_JesseJ01` call
- Use QScript.QCompile.App.exe to recompile it
- Replace `manualtricks.qb` with the recompiled version
- Replace `qb_scripts.prx` in Game/Data/scripts/game/skater with an empty file with the same name
    - I got the idea to do this from the various custom skater mods in the THPSX discord, which require you to blank out the skaterparts, skaterparts_secret, and skaterparts_temp prx files

I found most of these tools in the THPSX Discord. QScript claims it works for both THUG and THUG2, it certainly worked on this file. THQBEditor and QScriptEd may only work for THPS3, certainly they did not play nice with the THUG2 files. RoQ did not seem to work for THUG2 either.

Other notes:
- byxor has a "NeverScript" repository that I haven't used, might be able to generate PRE/PRX files: https://github.com/byxor/NeverScript
- These links to various other tools are dead, but might be helpful for searching: https://thpsx.com/forums/index.php?topic=1693.0
- DCxDemo has a small number of tools available as well: https://github.com/DCxDemo?tab=repositories
- PARTY MAN X does some memory magic with THPS3 (for IL mode), check out all the partymods and the autosplitter: https://github.com/PARTYMANX?tab=repositories
