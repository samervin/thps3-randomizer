# Competition scores

The calculation goes something like this:

- Getting the listed medal score for a level will generally give you the associated numeric ranking. 
- There is randomness in the scores the judges give you, but they will generally average to the correct ranking.
- Example:
    - If you score exactly 25k points in vanilla Rio, your ranking will be (roughly) 80.
    - If you score below 25k, you will get some percentage of 80 as your ranking.
    - If you score above 25k but below 70k (the silver) will give you a ranking between 80 and 85.
- The other skaters get randomly generated ranking assigned to them every run. 
    - One skater will be near the gold ranking
    - One skater will be near the silver ranking
    - All other skaters will be near the bronze ranking

I can't tell for the life of me what the bails number does. It doesn't seem to react to being changed or make any difference on ranking, though I could be wrong.

Vanilla requirements (these numbers are never displayed in-game):
    - Rio: bronze 80 = 25k, silver 85 = 70k, gold 90 = 120k, bail = .25
    - Skater Island: bronze 85 = 45k, silver 90 = 80k, gold 93 = 150k, bail = .35
    - Tokyo: bronze 90 = 100k, silver 92.5 = 150k, gold 95 = 200k, bail = .5

# Custom boards

Very doable. Just put image files in Data/Textures/Boards and refer to them in the script files.

The default boards are all 64x128. The game will accept files of any size (as long as it isn't too large), though they don't show up at a higher resolution in-game. The game will also accept files of any aspect ratio and will squash the texture to fit it on the board (in fact, it already does this with the built-in decks).

# List of features (current as of 2026/06/02)

- Change locations for SKATE, secret tape, deck, stat points
- Change level order and unlock requirements
- Change score requirements for normal and comp levels
- Change starting stats, normal tricks, and special tricks for all skaters
- Change street/vert for each skater
- Change tricks required for trickspot goals
- Change timer for normal levels
- Change locations for Chuck and skaters in Canada
- Change locations for thin man, axe, and pumpkins in Suburbia
- Change speed of ice cream truck in Suburbia
- Change who the thin man is in love with
- Change score requirements for Canada skaters and Neversoft girls
- Require collecting the deck before collecting the secret tape or earning a medal
- Lock all pro skaters behind arbitrary requirements
- Change secret skater/cheats unlock order and requirements
- Change deck and grip images
- Remove automatic prompt to save after each level
- (Not complete) Visual editor for settings and file management
- (Not complete) Change gaps required for trickspot goals
- (Not complete) Lock trick types to 0 points until "unlocked" via another flag
- (Not complete) Add additional locations and offsets to existing item locations
- (Not complete) Move other goal items (e.g. Foundry valves, Suburbia branches, Airport buddy)
- (Not complete) Gaps list
- (Not started) In-memory patching solution
- (Not started) Settings presets, saved custom settings
- (Not started) Different level order for different skaters, instead of being shared
- (Not started) Well-defined victory condition with in-game confirmation
- (Not started) Limit ability to edit stats
- (Not started) Limit ability to edit tricks
- (Not started) Limit ability to retry/end run early
- (Not started) Require other typically-optional items (e.g. stat points) for other goals
- (Not started) Require goals to be completed in a specific order
- (Not started) Hide HUD elements like current score and goal requirements
- (Not started) Alter the game's physics
- (Not started) Change each skater's default outfit/appearance
- (Not started) Change sounds and background noises
- (Not started) Change the lighting and skyboxes
- (Not started) Change the fonts and menu colors
- (Not started) Add goals to Warehouse, Burnside, Roswell

# Global and skater flags

Level flags:

- 1 goal_bronze
- 2 goal_silver
- 3 goal_gold
- 0 goal_highscore
- 1 goal_proscore
- 2 goal_sickscore
- 3 goal_skate
- 4 goal_trickspot
- 5 goal_tape
- 6-8 goal_scriptedx
- 9-27 (not defined)
- 28-36 wait_for_x
- 37-40 stat_set_x
- 41-43 deck_iconx
- 44-46 skate_linex
- 47 pacer (unused)
- 48 goal_bogus (unused)
- 49 goal_all_gaps (unused sadly)
- 50 goal_stat_points (unused, though there is an orphaned function)
- 51-55 goal_state_pointx
- 56 goal_deck
- 57-61 goal_letter_x
- 62 goal_all_goals
- 63 award_trickslot

Skater flags:

- 0 just_unlocked_level
- 1 prompt_for_save
- 2 show_credits
- 3 in_goal_movies (unused)
- 4-9 (not defined)
- 10-18 level_unlocked_x (career mode levels)
- 19-21 got_gold_x
- 22 shown_golds_movie (unused)
- 23 unlocked_secret
- 24-47 (not defined)
- 48-64 skateshop_just_got_x (skateshop_just_got_back is unused, the others are used)
- 65-71 skateshop_return_from_x (all unused: set but never checked)
- 72-99 (not defined)

Shared/Global flags:

- 100-102 level_unlocked_x (secret levels)
- 103-110 skater_unlocked_x (secret characters)
- 111 ship_secret_unlocked
- 112 all_secrets_unlocked
- 113 already_edited_cas
- 114 skateshop_first_time_done (unused)
- 115-119 (unused)
- 120-134 cheat_unlocked_x (1-11 are used, 12-15 are unused)
- 135-157 movie_unlocked_x
- 158 special_cas_career_done
- 159 special_has_seen_ship
- 160 special_has_seen_tutorials
- 161-182 secret_unlock_x
- 183-184 (not defined)
- 185-199 cheat_on_x (1-11 are used, 12-15 are unused)
- 200 skater_unlocked_doomguy
- 201 secret_unlocked_01 (unused)

Successful tests of unused/undefined flags:

- New skater flag 4
- New skater flag 47
- New skater flag 99
- New global flag 115
- New global flag 202 (past the range of values in code)
- New global flag 255 (8 bits)
- New global flag 2048 (suspicious)

Failed tests of unused/undefined flags:

- New global flags 256, 257, 260 (retry run becomes retry comp, very weird floating skater glitch; might be overwriting the wrong part of memory)
- New global flag 300 (crashes the game when trying to set)
- New global flag 1023 (it seems to be already set/on when starting a new game)

# Reference/archive links

- LegacyTHPS Discord server
- [Chapter-3 mod forums](http://chapter-3.net/thps3/v2/forumdisplay.php?fid=200)
- [LevelMod](https://github.com/Vadru93/LevelMod/)
- [partymod-thps3](https://github.com/PARTYMANX/partymod-thps3/)
- [THPSX forums](https://thpsx.com/forums/index.php?board=1.0)
- (No longer active) thmods.com and thps-mods.com