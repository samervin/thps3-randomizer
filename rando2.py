# coding: cp1252

import random
import re
import os

from rando.constants import *
from rando.level_foundry import LevelFoundry
from rando.level_canada import LevelCanada
from rando.level_rio import LevelRio
from rando.level_suburbia import LevelSuburbia
from rando.level_airport import LevelAirport
from rando.level_skaterisland import LevelSkaterIsland
from rando.level_losangeles import LevelLosAngeles
from rando.level_tokyo import LevelTokyo
from rando.level_cruiseship import LevelCruiseShip
from rando.tricks import Tricks
from rando.button_binds import ButtonBinds
from rando.boards import Boards
from rando.secrets import Secrets
from rando.skaters import Skaters

def _shuffle(any_list):
    shuffled = any_list.copy()
    random.shuffle(shuffled)
    return shuffled

def read_script_file(filename):
    with open(f'vanilla-qbs/Scripts/{filename}.qb', 'r') as f:
        return f.readlines()

def read_modified_script_file(filename):
    with open(f'modified-qbs/Scripts/{filename}.qb', 'r') as f:
        return f.read()

def memify(script):
    # make one long string, then split on lines, to include modified linebreaks
    script = ''.join(script)
    script = script.splitlines(keepends=True)
    output = []
    for i, line in enumerate(script):
        # substitute any memory address like #00000 with i (the current line number) zero-padded to 5 spaces
        output.append(re.sub(r'#\d{5}', f"#{i:05d}", line))
    return output

def write_script_file(filename, contents):
    contents = memify(contents)
    full_filename = f'outfiles/Scripts/{filename}.out'
    os.makedirs(os.path.dirname(full_filename), exist_ok=True)
    with open(full_filename, 'w', newline='\n') as fout:
        fout.writelines(contents)

def display_victory_requirements(gameqb):
    # Display (dummy) victory requirements on level select menu instead of (broken) level unlock requirements
    # You only get about 26 characters before the message grows beyond the menu bar
    rando_victory = "3 Golds with All Skaters"
    return gameqb.replace("{{rando_game_victory_text}}", rando_victory)

def get_random_level_order(end_on_comp=False):
    if end_on_comp:
        comp_levels = _shuffle([
            LevelRio(),
            LevelSkaterIsland(),
            LevelTokyo(),
        ])
        last_level = comp_levels.pop()
        regular_levels = [
            LevelFoundry(),
            LevelCanada(),
            LevelSuburbia(),
            LevelAirport(),
            LevelLosAngeles(),
            LevelCruiseShip(),
        ]
        return _shuffle(regular_levels + comp_levels) + [last_level]
    else:
        levels = [
            LevelFoundry(),
            LevelCanada(),
            LevelRio(),
            LevelSuburbia(),
            LevelAirport(),
            LevelSkaterIsland(),
            LevelLosAngeles(),
            LevelTokyo(),
            LevelCruiseShip(),
        ]
        return _shuffle(levels)

def randomize_level_requirements(levels, mainmenu, goal_scripts):
    # randomize level order and unlock conditions
    # default requirements:
    # Foundry = 0 goals
    # Canada = 3 goals
    # Rio = 10 goals
    # Suburbia = 1 medal
    # Airport = 18 goals
    # Skater Island = 26 goals
    # LA = 2 medals
    # Tokyo = 35 goals
    # Cruise Ship = 3 medals

    level_reqs = []
    total_goals = 0
    total_medals = 0
    level_reqs.append((0, "first"))

    for level in levels:
        match level.level_type:
            case "normal":
                req = random.randint(1, 1)# 9)
                total_goals = total_goals + req
                level_reqs.append((total_goals, "Goal"))
            case "comp":
                total_medals += 1
                level_reqs.append((total_medals, "Medal"))

    for i, level in enumerate(levels):
        match level.name_flag:
            case "FOUNDRY":
                unlock_var = "{{rando_mainmenu_unlock_foundry}}"
            case "CANADA":
                unlock_var = "{{rando_mainmenu_unlock_canada}}"
            case "RIO":
                unlock_var = "{{rando_mainmenu_unlock_rio}}"
            case "SUBURBIA":
                unlock_var = "{{rando_mainmenu_unlock_suburbia}}"
            case "AIRPORT":
                unlock_var = "{{rando_mainmenu_unlock_airport}}"
            case "SKATERISLAND":
                unlock_var = "{{rando_mainmenu_unlock_si}}"
            case "LOSANGELES":
                unlock_var = "{{rando_mainmenu_unlock_la}}"
            case "TOKYO":
                unlock_var = "{{rando_mainmenu_unlock_tokyo}}"
            case "SHIP":
                unlock_var = "{{rando_mainmenu_unlock_ship}}"
            case _:
                raise Exception("invalid level")

        if level_reqs[i][1] == "first": # initial level
            mainmenu = mainmenu.replace(unlock_var, "0 Goals")
        elif level_reqs[i][0] == 1: # 1 goal or medal
            mainmenu = mainmenu.replace(unlock_var, f"{level_reqs[i][0]} {level_reqs[i][1]}")
        else: # More than 1 goal or medal
            mainmenu = mainmenu.replace(unlock_var, f"{level_reqs[i][0]} {level_reqs[i][1]}s")

    # patch to unlock the first level instead of always unlocking Foundry
    mainmenu = mainmenu.replace("{{rando_mainmenu_first_level_unlock}}", f"LEVEL_UNLOCKED_{levels[0].name_flag}")

    # patch end-of-run level unlock conditions
    goal_scripts = goal_scripts.replace("{{rando_goal_scripts_unlock_2_requirement}}", f"{level_reqs[1][1]}sGreaterThan {level_reqs[1][0]-1}")
    goal_scripts = goal_scripts.replace("{{rando_goal_scripts_unlock_3_requirement}}", f"{level_reqs[2][1]}sGreaterThan {level_reqs[2][0]-1}")
    goal_scripts = goal_scripts.replace("{{rando_goal_scripts_unlock_4_requirement}}", f"{level_reqs[3][1]}sGreaterThan {level_reqs[3][0]-1}")
    goal_scripts = goal_scripts.replace("{{rando_goal_scripts_unlock_5_requirement}}", f"{level_reqs[4][1]}sGreaterThan {level_reqs[4][0]-1}")
    goal_scripts = goal_scripts.replace("{{rando_goal_scripts_unlock_6_requirement}}", f"{level_reqs[5][1]}sGreaterThan {level_reqs[5][0]-1}")
    goal_scripts = goal_scripts.replace("{{rando_goal_scripts_unlock_7_requirement}}", f"{level_reqs[6][1]}sGreaterThan {level_reqs[6][0]-1}")
    goal_scripts = goal_scripts.replace("{{rando_goal_scripts_unlock_8_requirement}}", f"{level_reqs[7][1]}sGreaterThan {level_reqs[7][0]-1}")
    goal_scripts = goal_scripts.replace("{{rando_goal_scripts_unlock_9_requirement}}", f"{level_reqs[8][1]}sGreaterThan {level_reqs[8][0]-1}")
    goal_scripts = goal_scripts.replace("{{rando_goal_scripts_unlock_2_flag}}", f"LEVEL_UNLOCKED_{levels[1].name_flag}")
    goal_scripts = goal_scripts.replace("{{rando_goal_scripts_unlock_3_flag}}", f"LEVEL_UNLOCKED_{levels[2].name_flag}")
    goal_scripts = goal_scripts.replace("{{rando_goal_scripts_unlock_4_flag}}", f"LEVEL_UNLOCKED_{levels[3].name_flag}")
    goal_scripts = goal_scripts.replace("{{rando_goal_scripts_unlock_5_flag}}", f"LEVEL_UNLOCKED_{levels[4].name_flag}")
    goal_scripts = goal_scripts.replace("{{rando_goal_scripts_unlock_6_flag}}", f"LEVEL_UNLOCKED_{levels[5].name_flag}")
    goal_scripts = goal_scripts.replace("{{rando_goal_scripts_unlock_7_flag}}", f"LEVEL_UNLOCKED_{levels[6].name_flag}")
    goal_scripts = goal_scripts.replace("{{rando_goal_scripts_unlock_8_flag}}", f"LEVEL_UNLOCKED_{levels[7].name_flag}")
    goal_scripts = goal_scripts.replace("{{rando_goal_scripts_unlock_9_flag}}", f"LEVEL_UNLOCKED_{levels[8].name_flag}")
    goal_scripts = goal_scripts.replace("{{rando_goal_scripts_unlock_2_name}}", levels[1].name)
    goal_scripts = goal_scripts.replace("{{rando_goal_scripts_unlock_3_name}}", levels[2].name)
    goal_scripts = goal_scripts.replace("{{rando_goal_scripts_unlock_4_name}}", levels[3].name)
    goal_scripts = goal_scripts.replace("{{rando_goal_scripts_unlock_5_name}}", levels[4].name)
    goal_scripts = goal_scripts.replace("{{rando_goal_scripts_unlock_6_name}}", levels[5].name)
    goal_scripts = goal_scripts.replace("{{rando_goal_scripts_unlock_7_name}}", levels[6].name)
    goal_scripts = goal_scripts.replace("{{rando_goal_scripts_unlock_8_name}}", levels[7].name)
    goal_scripts = goal_scripts.replace("{{rando_goal_scripts_unlock_9_name}}", levels[8].name)

    return goal_scripts, mainmenu

def randomize_score_goals(levels, goal_scripts, comp_scripts):
    # randomize score goals
    # original scores, for reference:
    # foundry: 10k, 30k, 60k
    # canada: 35k, 70k, 120k
    # suburbia: 55k, 110k, 200k
    # airport: 75k, 150k, 300k
    # los angeles: 100k, 190k, 400k
    # cruise ship: 150k, 225k, 500k

    score_goals = []
    score_goals.append(random.randint(1, 1))#5, 45))
    for i in range(17):
        score_goals.append(score_goals[i] + random.randint(15, 45))

    # shuffle competition scores
    # calculation goes something like this:
    # getting the listed medal score for a level will give you the associated numeric ranking. there is randomness in the scores the judges give you but they will almost always average to the correct ranking.
    # so if you score 25k points in vanilla Rio, your ranking will be roughly 80. below 25k, and you will get some percentage of 80 as your ranking. above 25k but below 70k (the silver) will give you a ranking between 80 and 85. etc.
    # the other skaters get randomly generated ranking assigned to them every run. one skater will be near the gold ranking, one skater will be near the silver ranking, and the rest will be near the bronze ranking.
    # I can't tell for the life of me what the bails number does. It doesn't seem to react to being changed or make any difference on ranking in my testing.

    # original requirements for reference:
    # rio: bronze 80 = 25k, silver 85 = 70k, gold 90 = 120k, bail = .25
    # skater island: bronze 85 = 45k, silver 90 = 80k, gold 93 = 150k, bail = .35
    # tokyo: bronze 90 = 100k, silver 92.5 = 150k, gold 95 = 200k, bail = .5
    # note: these numbers are never displayed in-game

    # generate random number between each medal and the next medal, approximately
    # TODO: changing the ranking numbers would change the available margin of error

    comp_goals = []
    comp_goals.append(random.randint(15, 35))
    for i in range(8):
        comp_goals.append(comp_goals[i] + random.randint(15, 35))

    # patch score goals into goal scripts
    for i, level in enumerate(levels):
        match level.name_flag:
            case "FOUNDRY":
                foundry_high = score_goals.pop(0)
                foundry_pro = score_goals.pop(0)
                foundry_sick = score_goals.pop(0)
                goal_scripts = goal_scripts.replace("{{rando_goal_scripts_foundry_high}}", f"{foundry_high}000")
                goal_scripts = goal_scripts.replace("{{rando_goal_scripts_foundry_pro}}", f"{foundry_pro}000")
                goal_scripts = goal_scripts.replace("{{rando_goal_scripts_foundry_sick}}", f"{foundry_sick}000")
            case "CANADA":
                canada_high = score_goals.pop(0)
                canada_pro = score_goals.pop(0)
                canada_sick = score_goals.pop(0)
                goal_scripts = goal_scripts.replace("{{rando_goal_scripts_canada_high}}", f"{canada_high}000")
                goal_scripts = goal_scripts.replace("{{rando_goal_scripts_canada_pro}}", f"{canada_pro}000")
                goal_scripts = goal_scripts.replace("{{rando_goal_scripts_canada_sick}}", f"{canada_sick}000")
            case "RIO":
                rio_bronze = comp_goals.pop(0)
                rio_silver = comp_goals.pop(0)
                rio_gold = comp_goals.pop(0)
                comp_scripts = comp_scripts.replace("{{rando_comp_scripts_rio_bronze}}", f"{rio_bronze}000")
                comp_scripts = comp_scripts.replace("{{rando_comp_scripts_rio_silver}}", f"{rio_silver}000")
                comp_scripts = comp_scripts.replace("{{rando_comp_scripts_rio_gold}}", f"{rio_gold}000")
            case "SUBURBIA":
                suburbia_high = score_goals.pop(0)
                suburbia_pro = score_goals.pop(0)
                suburbia_sick = score_goals.pop(0)
                goal_scripts = goal_scripts.replace("{{rando_goal_scripts_suburbia_high}}", f"{suburbia_high}000")
                goal_scripts = goal_scripts.replace("{{rando_goal_scripts_suburbia_pro}}", f"{suburbia_pro}000")
                goal_scripts = goal_scripts.replace("{{rando_goal_scripts_suburbia_sick}}", f"{suburbia_sick}000")
            case "AIRPORT":
                airport_high = score_goals.pop(0)
                airport_pro = score_goals.pop(0)
                airport_sick = score_goals.pop(0)
                goal_scripts = goal_scripts.replace("{{rando_goal_scripts_airport_high}}", f"{airport_high}000")
                goal_scripts = goal_scripts.replace("{{rando_goal_scripts_airport_pro}}", f"{airport_pro}000")
                goal_scripts = goal_scripts.replace("{{rando_goal_scripts_airport_sick}}", f"{airport_sick}000")
            case "SKATERISLAND":
                skater_island_bronze = comp_goals.pop(0)
                skater_island_silver = comp_goals.pop(0)
                skater_island_gold = comp_goals.pop(0)
                comp_scripts = comp_scripts.replace("{{rando_comp_scripts_si_bronze}}", f"{skater_island_bronze}000")
                comp_scripts = comp_scripts.replace("{{rando_comp_scripts_si_silver}}", f"{skater_island_silver}000")
                comp_scripts = comp_scripts.replace("{{rando_comp_scripts_si_gold}}", f"{skater_island_gold}000")
            case "LOSANGELES":
                los_angeles_high = score_goals.pop(0)
                los_angeles_pro = score_goals.pop(0)
                los_angeles_sick = score_goals.pop(0)
                goal_scripts = goal_scripts.replace("{{rando_goal_scripts_la_high}}", f"{los_angeles_high}000")
                goal_scripts = goal_scripts.replace("{{rando_goal_scripts_la_pro}}", f"{los_angeles_pro}000")
                goal_scripts = goal_scripts.replace("{{rando_goal_scripts_la_sick}}", f"{los_angeles_sick}000")
            case "TOKYO":
                tokyo_bronze = comp_goals.pop(0)
                tokyo_silver = comp_goals.pop(0)
                tokyo_gold = comp_goals.pop(0)
                comp_scripts = comp_scripts.replace("{{rando_comp_scripts_tokyo_bronze}}", f"{tokyo_bronze}000")
                comp_scripts = comp_scripts.replace("{{rando_comp_scripts_tokyo_silver}}", f"{tokyo_silver}000")
                comp_scripts = comp_scripts.replace("{{rando_comp_scripts_tokyo_gold}}", f"{tokyo_gold}000")
            case "SHIP":
                cruise_ship_high = score_goals.pop(0)
                cruise_ship_pro = score_goals.pop(0)
                cruise_ship_sick = score_goals.pop(0)
                goal_scripts = goal_scripts.replace("{{rando_goal_scripts_ship_high}}", f"{cruise_ship_high}000")
                goal_scripts = goal_scripts.replace("{{rando_goal_scripts_ship_pro}}", f"{cruise_ship_pro}000")
                goal_scripts = goal_scripts.replace("{{rando_goal_scripts_ship_sick}}", f"{cruise_ship_sick}000")
            case _:
                raise Exception("invalid level")
    return comp_scripts, goal_scripts

def randomize_item_locations(levels):
    for level in levels:
        level.randomize(include_extras=True)

def randomize_stats(skater_profile):
    # this game lets you remap all stats for all characters, so there is not much point to random stats
    # note: these stats only apply to fresh unsaved games
    stat_presets = ["max"]#, "easy", "default", "hard", "impossible"]
    stat_presets = _shuffle(stat_presets)

    match stat_presets[0]:
        case "max":
            stat_num = 10
        case "easy":
            stat_num = 7
        case "default":
            stat_num = 5
        case "hard":
            stat_num = 2
        case "impossible":
            stat_num = 0
        case _:
            raise Exception("invalid stat preset: " + stat_presets[0])

    skater_profile = skater_profile.replace("{{rando_skater_profile_global_stat}}", str(stat_num))
    return skater_profile

def _get_random_trickstyle():
    trickstyles = ['vert', 'street']
    return random.choice(trickstyles)

def randomize_trickstyle(skater_profile):
    # randomize whether each skater is street or vert
    for skater in Skaters().all_skaters:
        skater_profile = skater_profile.replace(
            "{{" + f"rando_skater_profile_{skater.script_name}_trickstyle" + "}}",
            _get_random_trickstyle()
        )
    return skater_profile

def require_deck_for_tape(goal_scripts):
    # require the deck to be collected before the tape goal will complete
    # note: as currently implemented, if you get the tape before the deck, you will have to retry the run to respawn the tape
    deck_required_for_tape = True
    if deck_required_for_tape:
        # Got_Secret_TapeIfDeck is a custom function added to the modified QB
        goal_scripts = goal_scripts.replace("{{rando_goal_scripts_tape_script}}", "Got_Secret_TapeIfDeck")
    else:
        # Got_Secret_Tape2 is the default with no additional requirements
        goal_scripts = goal_scripts.replace("{{rando_goal_scripts_tape_script}}", "Got_Secret_Tape2")
    return goal_scripts

def require_deck_for_medal(judges, comp_scripts):
    flag_medal_req = "{{rando_judges_medal_requirement}}"
    comp_scripts_medal_req = "{{rando_comp_scripts_medal_requirement}}"
    medal_message = "{{rando_comp_scripts_medal_message}}"

    deck_required_for_medal = True
    if deck_required_for_medal:
        # require the deck to be collected before getting any medal, or else you will lose the competition
        judges = judges.replace(flag_medal_req, "GetFlag flag = GOAL_DECK")
        comp_scripts = comp_scripts.replace(medal_message, "Must Find Deck To Medal")
        comp_scripts = comp_scripts.replace(comp_scripts_medal_req, "GetFlag flag = GOAL_DECK")
    else:
        # GetGlobalFlag flag = 159 will resolve to True as long as SPECIAL_HAS_SEEN_SHIP is set in mainmenu.qb
        judges = judges.replace(flag_medal_req, "GetGlobalFlag flag = 159")
        comp_scripts = comp_scripts.replace(medal_message, "Bails Hurt Scores")
        comp_scripts = comp_scripts.replace(comp_scripts_medal_req, "GetGlobalFlag flag = 159")

    return judges, comp_scripts

def randomize_level_timer(gamemode):
    # randomize the time limit for normal levels
    # the time limit for competition levels might not be scriptable
    time_limit = random.randint(90, 150)
    gamemode = gamemode.replace("{{rando_gamemode_career_time}}", str(time_limit))
    return gamemode

def randomize_trickspot_tricks(trick_type, ajc, alf, bdj, cjr, cpf):
    # Change required tricks for the street/vert goals
    n_grinds = _shuffle(Tricks().get_regular_grinds())
    n_grabs = _shuffle(Tricks().get_regular_grabs())
    n_flips = _shuffle(Tricks().get_regular_flips())
    n_lips = _shuffle(Tricks().get_regular_lips())

    match trick_type:
        case "ignore": # do not perform randomization
            return
        case "match": # randomize grinds into other grinds, flips into flips, etc.
            foundry_street_trick = n_grinds.pop()
            foundry_vert_trick = n_grabs.pop()
            canada_street_trick = n_grinds.pop()
            canada_vert_trick = n_grabs.pop()
            suburbia_street_trick = n_flips.pop()
            suburbia_vert_trick = n_grabs.pop()
            airport_street_trick = n_grinds.pop()
            airport_vert_trick = n_grabs.pop()
            la_street_trick = n_flips.pop()
            la_vert_trick = n_grabs.pop()
            ship_street_trick = n_grinds.pop()
            ship_vert_trick = n_lips.pop()
        case "wild": # randomize all normal tricks together
            n_tricks = _shuffle(n_grinds + n_grabs + n_flips + n_lips)
            foundry_street_trick = n_tricks.pop()
            foundry_vert_trick = n_tricks.pop()
            canada_street_trick = n_tricks.pop()
            canada_vert_trick = n_tricks.pop()
            suburbia_street_trick = n_tricks.pop()
            suburbia_vert_trick = n_tricks.pop()
            airport_street_trick = n_tricks.pop()
            airport_vert_trick = n_tricks.pop()
            la_street_trick = n_tricks.pop()
            la_vert_trick = n_tricks.pop()
            ship_street_trick = n_tricks.pop()
            ship_vert_trick = n_tricks.pop()
        case _:
            raise Exception("invalid trickspot trick type")

    cjr = cjr.replace("{{rando_cjr_trickspot_street_text}}", foundry_street_trick.name_goal)
    cjr = cjr.replace("{{rando_cjr_trickspot_vert_text}}", foundry_vert_trick.name_goal)
    cjr = cjr.replace("{{rando_cjr_trickspot_street_trick}}", foundry_street_trick.name)
    cjr = cjr.replace("{{rando_cjr_trickspot_vert_trick}}", foundry_vert_trick.name)
    ajc = ajc.replace("{{rando_ajc_trickspot_street_text}}", canada_street_trick.name_goal)
    ajc = ajc.replace("{{rando_ajc_trickspot_vert_text}}", canada_vert_trick.name_goal)
    ajc = ajc.replace("{{rando_ajc_trickspot_street_trick}}", canada_street_trick.name)
    ajc = ajc.replace("{{rando_ajc_trickspot_vert_trick}}", canada_vert_trick.name)
    alf = alf.replace("{{rando_alf_trickspot_street_text}}", suburbia_street_trick.name_goal)
    alf = alf.replace("{{rando_alf_trickspot_vert_text}}", suburbia_vert_trick.name_goal)
    alf = alf.replace("{{rando_alf_trickspot_street_trick}}", suburbia_street_trick.name)
    alf = alf.replace("{{rando_alf_trickspot_vert_trick}}", suburbia_vert_trick.name)
    cpf = cpf.replace("{{rando_cpf_airport_trickspot_street_text}}", airport_street_trick.name_goal)
    cpf = cpf.replace("{{rando_cpf_airport_trickspot_vert_text}}", airport_vert_trick.name_goal)
    cpf = cpf.replace("{{rando_cpf_airport_trickspot_street_trick}}", airport_street_trick.name)
    cpf = cpf.replace("{{rando_cpf_airport_trickspot_vert_trick}}", airport_vert_trick.name)
    cpf = cpf.replace("{{rando_cpf_la_trickspot_street_text}}", la_street_trick.name_goal)
    cpf = cpf.replace("{{rando_cpf_la_trickspot_vert_text}}", la_vert_trick.name_goal)
    cpf = cpf.replace("{{rando_cpf_la_trickspot_street_trick}}", la_street_trick.name)
    cpf = cpf.replace("{{rando_cpf_la_trickspot_vert_trick}}", la_vert_trick.name)
    bdj = bdj.replace("{{rando_bdj_trickspot_street_text}}", ship_street_trick.name_goal)
    bdj = bdj.replace("{{rando_bdj_trickspot_vert_text}}", ship_vert_trick.name_goal)
    bdj = bdj.replace("{{rando_bdj_trickspot_street_trick}}", ship_street_trick.name)
    bdj = bdj.replace("{{rando_bdj_trickspot_vert_trick}}", ship_vert_trick.name)

    return [
        foundry_street_trick, foundry_vert_trick, canada_street_trick, canada_vert_trick,
        suburbia_street_trick, suburbia_vert_trick, airport_street_trick, airport_vert_trick,
        la_street_trick, la_vert_trick, ship_street_trick, ship_vert_trick
    ], ajc, alf, bdj, cjr, cpf

def randomize_trick_sets(protricks, trickspot_tricks):
    # ensure tricks used in trickspots are shuffled into default binds
    # note: current method can cause duplicate tricks, but the game already lets you do this anyway
    trickspot_lips = [t for t in trickspot_tricks if t.trick_type == "lip"]
    trickspot_grabs = [t for t in trickspot_tricks if t.trick_type == "grab"]
    trickspot_flips = [t for t in trickspot_tricks if t.trick_type == "flip"]

    vert_lips = _shuffle(Tricks().get_regular_lips())[:(8-len(trickspot_lips))] # first 8 entries, fewer if trickspots exist
    vert_lips = _shuffle(vert_lips + trickspot_lips)
    protricks = protricks.replace("{{rando_protricks_vertlip_ul}}", vert_lips.pop().name_script)
    protricks = protricks.replace("{{rando_protricks_vertlip_ur}}", vert_lips.pop().name_script)
    protricks = protricks.replace("{{rando_protricks_vertlip_dl}}", vert_lips.pop().name_script)
    protricks = protricks.replace("{{rando_protricks_vertlip_dr}}", vert_lips.pop().name_script)
    protricks = protricks.replace("{{rando_protricks_vertlip_l}}", vert_lips.pop().name_script)
    protricks = protricks.replace("{{rando_protricks_vertlip_r}}", vert_lips.pop().name_script)
    protricks = protricks.replace("{{rando_protricks_vertlip_d}}", vert_lips.pop().name_script)
    protricks = protricks.replace("{{rando_protricks_vertlip_u}}", vert_lips.pop().name_script)
    street_lips = _shuffle(Tricks().get_regular_lips())[:(8-len(trickspot_lips))] # first 8 entries, fewer if trickspots exist
    street_lips = _shuffle(street_lips + trickspot_lips)
    protricks = protricks.replace("{{rando_protricks_streetlip_ul}}", street_lips.pop().name_script)
    protricks = protricks.replace("{{rando_protricks_streetlip_ur}}", street_lips.pop().name_script)
    protricks = protricks.replace("{{rando_protricks_streetlip_dl}}", street_lips.pop().name_script)
    protricks = protricks.replace("{{rando_protricks_streetlip_dr}}", street_lips.pop().name_script)
    protricks = protricks.replace("{{rando_protricks_streetlip_l}}", street_lips.pop().name_script)
    protricks = protricks.replace("{{rando_protricks_streetlip_r}}", street_lips.pop().name_script)
    protricks = protricks.replace("{{rando_protricks_streetlip_d}}", street_lips.pop().name_script)
    protricks = protricks.replace("{{rando_protricks_streetlip_u}}", street_lips.pop().name_script)
    hawk_lips = _shuffle(Tricks().get_regular_lips())[:(8-len(trickspot_lips))] # first 8 entries, fewer if trickspots exist
    hawk_lips = _shuffle(hawk_lips + trickspot_lips)
    protricks = protricks.replace("{{rando_protricks_hawklip_ul}}", hawk_lips.pop().name_script)
    protricks = protricks.replace("{{rando_protricks_hawklip_ur}}", hawk_lips.pop().name_script)
    protricks = protricks.replace("{{rando_protricks_hawklip_dl}}", hawk_lips.pop().name_script)
    protricks = protricks.replace("{{rando_protricks_hawklip_dr}}", hawk_lips.pop().name_script)
    protricks = protricks.replace("{{rando_protricks_hawklip_l}}", hawk_lips.pop().name_script)
    protricks = protricks.replace("{{rando_protricks_hawklip_r}}", hawk_lips.pop().name_script)
    protricks = protricks.replace("{{rando_protricks_hawklip_d}}", hawk_lips.pop().name_script)
    protricks = protricks.replace("{{rando_protricks_hawklip_u}}", hawk_lips.pop().name_script)

    all_around_grabs = _shuffle(Tricks().get_regular_grabs())[:(12-len(trickspot_grabs))] # first 12 entries, fewer if trickspots exist
    all_around_grabs = _shuffle(all_around_grabs + trickspot_grabs)
    protricks = protricks.replace("{{rando_protricks_allaroundgrabs_ul}}", all_around_grabs.pop().name_script)
    protricks = protricks.replace("{{rando_protricks_allaroundgrabs_ur}}", all_around_grabs.pop().name_script)
    protricks = protricks.replace("{{rando_protricks_allaroundgrabs_dl}}", all_around_grabs.pop().name_script)
    protricks = protricks.replace("{{rando_protricks_allaroundgrabs_dr}}", all_around_grabs.pop().name_script)
    protricks = protricks.replace("{{rando_protricks_allaroundgrabs_l}}", all_around_grabs.pop().name_script)
    protricks = protricks.replace("{{rando_protricks_allaroundgrabs_r}}", all_around_grabs.pop().name_script)
    protricks = protricks.replace("{{rando_protricks_allaroundgrabs_d}}", all_around_grabs.pop().name_script)
    protricks = protricks.replace("{{rando_protricks_allaroundgrabs_u}}", all_around_grabs.pop().name_script)
    protricks = protricks.replace("{{rando_protricks_allaroundgrabs_ll}}", all_around_grabs.pop().name_script)
    protricks = protricks.replace("{{rando_protricks_allaroundgrabs_rr}}", all_around_grabs.pop().name_script)
    protricks = protricks.replace("{{rando_protricks_allaroundgrabs_uu}}", all_around_grabs.pop().name_script)
    protricks = protricks.replace("{{rando_protricks_allaroundgrabs_dd}}", all_around_grabs.pop().name_script)
    street_grabs = _shuffle(Tricks().get_regular_grabs())[:(12-len(trickspot_grabs))] # first 12 entries, fewer if trickspots exist
    street_grabs = _shuffle(street_grabs + trickspot_grabs)
    protricks = protricks.replace("{{rando_protricks_streetgrabs_ul}}", street_grabs.pop().name_script)
    protricks = protricks.replace("{{rando_protricks_streetgrabs_ur}}", street_grabs.pop().name_script)
    protricks = protricks.replace("{{rando_protricks_streetgrabs_dl}}", street_grabs.pop().name_script)
    protricks = protricks.replace("{{rando_protricks_streetgrabs_dr}}", street_grabs.pop().name_script)
    protricks = protricks.replace("{{rando_protricks_streetgrabs_l}}", street_grabs.pop().name_script)
    protricks = protricks.replace("{{rando_protricks_streetgrabs_r}}", street_grabs.pop().name_script)
    protricks = protricks.replace("{{rando_protricks_streetgrabs_d}}", street_grabs.pop().name_script)
    protricks = protricks.replace("{{rando_protricks_streetgrabs_u}}", street_grabs.pop().name_script)
    protricks = protricks.replace("{{rando_protricks_streetgrabs_ll}}", street_grabs.pop().name_script)
    protricks = protricks.replace("{{rando_protricks_streetgrabs_rr}}", street_grabs.pop().name_script)
    protricks = protricks.replace("{{rando_protricks_streetgrabs_uu}}", street_grabs.pop().name_script)
    protricks = protricks.replace("{{rando_protricks_streetgrabs_dd}}", street_grabs.pop().name_script)
    vert_grabs = _shuffle(Tricks().get_regular_grabs())[:(12-len(trickspot_grabs))] # first 12 entries, fewer if trickspots exist
    vert_grabs = _shuffle(vert_grabs + trickspot_grabs)
    protricks = protricks.replace("{{rando_protricks_vertgrabs_ul}}", vert_grabs.pop().name_script)
    protricks = protricks.replace("{{rando_protricks_vertgrabs_ur}}", vert_grabs.pop().name_script)
    protricks = protricks.replace("{{rando_protricks_vertgrabs_dl}}", vert_grabs.pop().name_script)
    protricks = protricks.replace("{{rando_protricks_vertgrabs_dr}}", vert_grabs.pop().name_script)
    protricks = protricks.replace("{{rando_protricks_vertgrabs_l}}", vert_grabs.pop().name_script)
    protricks = protricks.replace("{{rando_protricks_vertgrabs_r}}", vert_grabs.pop().name_script)
    protricks = protricks.replace("{{rando_protricks_vertgrabs_d}}", vert_grabs.pop().name_script)
    protricks = protricks.replace("{{rando_protricks_vertgrabs_u}}", vert_grabs.pop().name_script)
    protricks = protricks.replace("{{rando_protricks_vertgrabs_ll}}", vert_grabs.pop().name_script)
    protricks = protricks.replace("{{rando_protricks_vertgrabs_rr}}", vert_grabs.pop().name_script)
    protricks = protricks.replace("{{rando_protricks_vertgrabs_uu}}", vert_grabs.pop().name_script)
    protricks = protricks.replace("{{rando_protricks_vertgrabs_dd}}", vert_grabs.pop().name_script)

    vert_flips = _shuffle(Tricks().get_regular_flips())[:(12-len(trickspot_flips))] # first 12 entries, fewer if trickspots exist
    vert_flips = _shuffle(vert_flips + trickspot_flips)
    protricks = protricks.replace("{{rando_protricks_vertflips_ul}}", vert_flips.pop().name_script)
    protricks = protricks.replace("{{rando_protricks_vertflips_ur}}", vert_flips.pop().name_script)
    protricks = protricks.replace("{{rando_protricks_vertflips_dl}}", vert_flips.pop().name_script)
    protricks = protricks.replace("{{rando_protricks_vertflips_dr}}", vert_flips.pop().name_script)
    protricks = protricks.replace("{{rando_protricks_vertflips_l}}", vert_flips.pop().name_script)
    protricks = protricks.replace("{{rando_protricks_vertflips_r}}", vert_flips.pop().name_script)
    protricks = protricks.replace("{{rando_protricks_vertflips_d}}", vert_flips.pop().name_script)
    protricks = protricks.replace("{{rando_protricks_vertflips_u}}", vert_flips.pop().name_script)
    protricks = protricks.replace("{{rando_protricks_vertflips_ll}}", vert_flips.pop().name_script)
    protricks = protricks.replace("{{rando_protricks_vertflips_rr}}", vert_flips.pop().name_script)
    protricks = protricks.replace("{{rando_protricks_vertflips_uu}}", vert_flips.pop().name_script)
    protricks = protricks.replace("{{rando_protricks_vertflips_dd}}", vert_flips.pop().name_script)
    freestyle_flips = _shuffle(Tricks().get_regular_flips())[:(12-len(trickspot_flips))] # first 12 entries, fewer if trickspots exist
    freestyle_flips = _shuffle(freestyle_flips + trickspot_flips)
    protricks = protricks.replace("{{rando_protricks_freestyleflips_ul}}", freestyle_flips.pop().name_script)
    protricks = protricks.replace("{{rando_protricks_freestyleflips_ur}}", freestyle_flips.pop().name_script)
    protricks = protricks.replace("{{rando_protricks_freestyleflips_dl}}", freestyle_flips.pop().name_script)
    protricks = protricks.replace("{{rando_protricks_freestyleflips_dr}}", freestyle_flips.pop().name_script)
    protricks = protricks.replace("{{rando_protricks_freestyleflips_l}}", freestyle_flips.pop().name_script)
    protricks = protricks.replace("{{rando_protricks_freestyleflips_r}}", freestyle_flips.pop().name_script)
    protricks = protricks.replace("{{rando_protricks_freestyleflips_d}}", freestyle_flips.pop().name_script)
    protricks = protricks.replace("{{rando_protricks_freestyleflips_u}}", freestyle_flips.pop().name_script)
    protricks = protricks.replace("{{rando_protricks_freestyleflips_ll}}", freestyle_flips.pop().name_script)
    protricks = protricks.replace("{{rando_protricks_freestyleflips_rr}}", freestyle_flips.pop().name_script)
    protricks = protricks.replace("{{rando_protricks_freestyleflips_uu}}", freestyle_flips.pop().name_script)
    protricks = protricks.replace("{{rando_protricks_freestyleflips_dd}}", freestyle_flips.pop().name_script)
    street_flips = _shuffle(Tricks().get_regular_flips())[:(12-len(trickspot_flips))] # first 12 entries, fewer if trickspots exist
    street_flips = _shuffle(street_flips + trickspot_flips)
    protricks = protricks.replace("{{rando_protricks_streetflips_ul}}", street_flips.pop().name_script)
    protricks = protricks.replace("{{rando_protricks_streetflips_ur}}", street_flips.pop().name_script)
    protricks = protricks.replace("{{rando_protricks_streetflips_dl}}", street_flips.pop().name_script)
    protricks = protricks.replace("{{rando_protricks_streetflips_dr}}", street_flips.pop().name_script)
    protricks = protricks.replace("{{rando_protricks_streetflips_l}}", street_flips.pop().name_script)
    protricks = protricks.replace("{{rando_protricks_streetflips_r}}", street_flips.pop().name_script)
    protricks = protricks.replace("{{rando_protricks_streetflips_d}}", street_flips.pop().name_script)
    protricks = protricks.replace("{{rando_protricks_streetflips_u}}", street_flips.pop().name_script)
    protricks = protricks.replace("{{rando_protricks_streetflips_ll}}", street_flips.pop().name_script)
    protricks = protricks.replace("{{rando_protricks_streetflips_rr}}", street_flips.pop().name_script)
    protricks = protricks.replace("{{rando_protricks_streetflips_uu}}", street_flips.pop().name_script)
    protricks = protricks.replace("{{rando_protricks_streetflips_dd}}", street_flips.pop().name_script)

    return protricks

def randomize_special_tricks(skater_profile, difficulty=None):
    for skater in Skaters().all_skaters:
        four_specials = _shuffle(Tricks().get_all_special_tricks())[:4]
        binds = ButtonBinds()
        grind_binds = _shuffle(binds.get_special_grind_binds(difficulty))
        air_binds = _shuffle(binds.get_special_air_binds(difficulty))
        lip_binds = _shuffle(binds.get_special_lip_binds(difficulty))
        manual_binds = _shuffle(binds.get_special_manual_binds(difficulty))

        for i, special in enumerate(four_specials):
            skater_profile = skater_profile.replace(
                "{{" + f"rando_skater_profile_{skater.script_name}_special_name_{i}" + "}}",
                special.name_script
            )
            match special.trick_type:
                case "grind":
                    skater_profile = skater_profile.replace(
                        "{{" + f"rando_skater_profile_{skater.script_name}_special_slot_{i}" + "}}",
                        grind_binds.pop().name
                    )
                case "grab" | "flip":
                    skater_profile = skater_profile.replace(
                        "{{" + f"rando_skater_profile_{skater.script_name}_special_slot_{i}" + "}}",
                        air_binds.pop().name
                    )
                case "lip":
                    skater_profile = skater_profile.replace(
                        "{{" + f"rando_skater_profile_{skater.script_name}_special_slot_{i}" + "}}",
                        lip_binds.pop().name
                    )
                case "manual":
                    skater_profile = skater_profile.replace(
                        "{{" + f"rando_skater_profile_{skater.script_name}_special_slot_{i}" + "}}",
                        manual_binds.pop().name
                    )
                case _:
                    raise Exception("invalid trick type")
    return skater_profile

def randomize_impress_ped_scores(ajc, bdj, sk3_pedscripts):
    ped_canada_score = random.randint(2, 25) * 1000
    ped_canada_chatter = int(ped_canada_score/2) # Used for voice lines
    ped_ship_score = random.randint(2, 25) * 1000
    ped_ship_chatter = int(ped_ship_score/2) # Used for voice lines
    sk3_pedscripts = sk3_pedscripts.replace("{{rando_sk3_pedscripts_skater_chatter}}", str(ped_canada_chatter))
    sk3_pedscripts = sk3_pedscripts.replace("{{rando_sk3_pedscripts_skater_score}}", str(ped_canada_score))
    sk3_pedscripts = sk3_pedscripts.replace("{{rando_sk3_pedscripts_girl_chatter}}", str(ped_ship_chatter))
    sk3_pedscripts = sk3_pedscripts.replace("{{rando_sk3_pedscripts_girl_score}}", str(ped_ship_score))
    ajc = ajc.replace("{{rando_ajc_skater_points}}", str(ped_canada_score))
    bdj = bdj.replace("{{rando_bdj_girl_points}}", str(ped_ship_score))
    return ajc, bdj, sk3_pedscripts

def randomize_decks(boardselect):
    # Randomize grip tape textures and skater default grip tapes
    # TODO: Changing your grip still doesn't match between the skateshop and in-level
    grips = _shuffle(Boards().get_grips())
    for i in range(32):
        boardselect = boardselect.replace("{{" + f"rando_boardselect_grip_texture_{i}" + "}}", grips[i].texture)
        boardselect = boardselect.replace("{{" + f"rando_boardselect_grip_description_{i}" + "}}", grips[i].name)
    # Randomize deck textures
    # TODO: Change the in-game names too?
    decks = _shuffle(Boards().get_decks())
    for i in range(230):
        boardselect = boardselect.replace("{{" + f"rando_boardselect_deck_texture_{i}" + "}}", decks[i].texture)
    return boardselect

def randomize_secrets(goal_scripts):
    # UnlockNextSecret is a builtin which keys off the SecretScripts array

    # Rewrite ExecuteNextSecret_20to29 to fit in 23rd secret condition (Doomguy)
    # Global secret flags are hardcoded (SECRET_UNLOCK_#) but CHEAT_UNLOCKED_12 is not used so we use it in place of the missing SECRET_UNLOCK_23

    # TODO: For now, first person mode is always 23rd/last:
    # It contains "Entire Game complete" logic and the last secret cannot be a skater anyway

    # Shuffle the remaining secrets 1-22
    secrets = _shuffle([1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22])
    goal_scripts = goal_scripts.replace("{{rando_goal_scripts_secret_a}}", f"THPS3_secretScript_{secrets.pop()}")
    goal_scripts = goal_scripts.replace("{{rando_goal_scripts_secret_b}}", f"THPS3_secretScript_{secrets.pop()}")
    goal_scripts = goal_scripts.replace("{{rando_goal_scripts_secret_c}}", f"THPS3_secretScript_{secrets.pop()}")
    goal_scripts = goal_scripts.replace("{{rando_goal_scripts_secret_d}}", f"THPS3_secretScript_{secrets.pop()}")
    goal_scripts = goal_scripts.replace("{{rando_goal_scripts_secret_e}}", f"THPS3_secretScript_{secrets.pop()}")
    goal_scripts = goal_scripts.replace("{{rando_goal_scripts_secret_f}}", f"THPS3_secretScript_{secrets.pop()}")
    goal_scripts = goal_scripts.replace("{{rando_goal_scripts_secret_g}}", f"THPS3_secretScript_{secrets.pop()}")
    goal_scripts = goal_scripts.replace("{{rando_goal_scripts_secret_h}}", f"THPS3_secretScript_{secrets.pop()}")
    goal_scripts = goal_scripts.replace("{{rando_goal_scripts_secret_i}}", f"THPS3_secretScript_{secrets.pop()}")
    goal_scripts = goal_scripts.replace("{{rando_goal_scripts_secret_j}}", f"THPS3_secretScript_{secrets.pop()}")
    goal_scripts = goal_scripts.replace("{{rando_goal_scripts_secret_k}}", f"THPS3_secretScript_{secrets.pop()}")
    goal_scripts = goal_scripts.replace("{{rando_goal_scripts_secret_l}}", f"THPS3_secretScript_{secrets.pop()}")
    goal_scripts = goal_scripts.replace("{{rando_goal_scripts_secret_m}}", f"THPS3_secretScript_{secrets.pop()}")
    goal_scripts = goal_scripts.replace("{{rando_goal_scripts_secret_n}}", f"THPS3_secretScript_{secrets.pop()}")
    goal_scripts = goal_scripts.replace("{{rando_goal_scripts_secret_o}}", f"THPS3_secretScript_{secrets.pop()}")
    goal_scripts = goal_scripts.replace("{{rando_goal_scripts_secret_p}}", f"THPS3_secretScript_{secrets.pop()}")
    goal_scripts = goal_scripts.replace("{{rando_goal_scripts_secret_q}}", f"THPS3_secretScript_{secrets.pop()}")
    goal_scripts = goal_scripts.replace("{{rando_goal_scripts_secret_r}}", f"THPS3_secretScript_{secrets.pop()}")
    goal_scripts = goal_scripts.replace("{{rando_goal_scripts_secret_s}}", f"THPS3_secretScript_{secrets.pop()}")
    goal_scripts = goal_scripts.replace("{{rando_goal_scripts_secret_t}}", f"THPS3_secretScript_{secrets.pop()}")
    goal_scripts = goal_scripts.replace("{{rando_goal_scripts_secret_u}}", f"THPS3_secretScript_{secrets.pop()}")
    goal_scripts = goal_scripts.replace("{{rando_goal_scripts_secret_v}}", f"THPS3_secretScript_{secrets.pop()}")

    # TODO: Edit Cheat menu to appear when the first cheat is unlocked, rather than only Snowboard mode

    golds_required_for_secret = True
    if golds_required_for_secret:
        goal_scripts = goal_scripts.replace("{{rando_goal_scripts_secret_gold_rio}}", "GOT_GOLD_RIO")
        goal_scripts = goal_scripts.replace("{{rando_goal_scripts_secret_gold_si}}", "GOT_GOLD_SI")
        goal_scripts = goal_scripts.replace("{{rando_goal_scripts_secret_gold_tokyo}}", "GOT_GOLD_TOKYO")
    else:
        # Flag 159 is always true
        goal_scripts = goal_scripts.replace("{{rando_goal_scripts_secret_gold_rio}}", "159")
        goal_scripts = goal_scripts.replace("{{rando_goal_scripts_secret_gold_si}}", "159")
        goal_scripts = goal_scripts.replace("{{rando_goal_scripts_secret_gold_tokyo}}", "159")

    goals_required_for_secret = 0
    goal_scripts = goal_scripts.replace("{{rando_goal_scripts_secret_goals}}", str(goals_required_for_secret))

    # For normal levels, secret unlock check is moved so that all goals are not required
    # TODO: move secret unlock for comp levels as well
    return goal_scripts

def lock_characters(skater_profile):
    lock_pros = False
    if lock_pros:
        # Lock custom skater and all non-Tony pro skaters behind a non-character global secret flag
        noncharacter_flags = Secrets().secret_flags_levels + Secrets().secret_flags_cheats
        noncharacter_flags = _shuffle(noncharacter_flags)
        skater_profile = skater_profile.replace("{{rando_skater_profile_caballero_unlock_flag}}", f"unlock_flag = {noncharacter_flags.pop()}")
        skater_profile = skater_profile.replace("{{rando_skater_profile_campbell_unlock_flag}}", f"unlock_flag = {noncharacter_flags.pop()}")
        skater_profile = skater_profile.replace("{{rando_skater_profile_glifberg_unlock_flag}}", f"unlock_flag = {noncharacter_flags.pop()}")
        skater_profile = skater_profile.replace("{{rando_skater_profile_koston_unlock_flag}}", f"unlock_flag = {noncharacter_flags.pop()}")
        skater_profile = skater_profile.replace("{{rando_skater_profile_lasek_unlock_flag}}", f"unlock_flag = {noncharacter_flags.pop()}")
        skater_profile = skater_profile.replace("{{rando_skater_profile_margera_unlock_flag}}", f"unlock_flag = {noncharacter_flags.pop()}")
        skater_profile = skater_profile.replace("{{rando_skater_profile_mullen_unlock_flag}}", f"unlock_flag = {noncharacter_flags.pop()}")
        skater_profile = skater_profile.replace("{{rando_skater_profile_muska_unlock_flag}}", f"unlock_flag = {noncharacter_flags.pop()}")
        skater_profile = skater_profile.replace("{{rando_skater_profile_reynolds_unlock_flag}}", f"unlock_flag = {noncharacter_flags.pop()}")
        skater_profile = skater_profile.replace("{{rando_skater_profile_rowley_unlock_flag}}", f"unlock_flag = {noncharacter_flags.pop()}")
        skater_profile = skater_profile.replace("{{rando_skater_profile_steamer_unlock_flag}}", f"unlock_flag = {noncharacter_flags.pop()}")
        skater_profile = skater_profile.replace("{{rando_skater_profile_thomas_unlock_flag}}", f"unlock_flag = {noncharacter_flags.pop()}")
        skater_profile = skater_profile.replace("{{rando_skater_profile_custom_unlock_flag}}", f"unlock_flag = {noncharacter_flags.pop()}")
    else:
        skater_profile = skater_profile.replace("{{rando_skater_profile_caballero_unlock_flag}}", "")
        skater_profile = skater_profile.replace("{{rando_skater_profile_campbell_unlock_flag}}", "")
        skater_profile = skater_profile.replace("{{rando_skater_profile_glifberg_unlock_flag}}", "")
        skater_profile = skater_profile.replace("{{rando_skater_profile_koston_unlock_flag}}", "")
        skater_profile = skater_profile.replace("{{rando_skater_profile_lasek_unlock_flag}}", "")
        skater_profile = skater_profile.replace("{{rando_skater_profile_margera_unlock_flag}}", "")
        skater_profile = skater_profile.replace("{{rando_skater_profile_mullen_unlock_flag}}", "")
        skater_profile = skater_profile.replace("{{rando_skater_profile_muska_unlock_flag}}", "")
        skater_profile = skater_profile.replace("{{rando_skater_profile_reynolds_unlock_flag}}", "")
        skater_profile = skater_profile.replace("{{rando_skater_profile_rowley_unlock_flag}}", "")
        skater_profile = skater_profile.replace("{{rando_skater_profile_steamer_unlock_flag}}", "")
        skater_profile = skater_profile.replace("{{rando_skater_profile_thomas_unlock_flag}}", "")
        skater_profile = skater_profile.replace("{{rando_skater_profile_custom_unlock_flag}}", "")
    return skater_profile

def junk_suburbia(alf):
    # Increase ice cream truck from 20 mph
    alf = alf.replace("{{rando_alf_icecreamtruck_speed}}", "100")
    # Make the thin man fall in love with Tony Hawk
    alf = alf.replace("{{rando_alf_thinman_hearts_skater}}", "hawk")
    return alf

def randomize_foundry_trickspot_gaps(cjr):
    # TODO: This doesn't really belong here longterm
    # TODO: This can't yet randomize the gaps in foun.qb
    # CJR_Foun_PipeTrickGap
    # CJR_Foun_RailTrickGap
    # NullScript
    foundry_gaps = [
        ("rando_cjr_gap01_gapscript", "Back End Rail 2 Rail"),
        ("rando_cjr_gap02_gapscript", "Bucket o' Hot Sauce"),
        ("rando_cjr_gap03_gapscript", "Catwalk Balancing Act"),
        ("rando_cjr_gap04_gapscript", "Catwalk Grind"),
        # ("rando_cjr_gap05_gapscript", "Catwalk Tight Lip"), # vanilla: CJR_Foun_Create_Porch_Talker
        ("rando_cjr_gap06_gapscript", "CG's SKDK 2 STFK"),
        ("rando_cjr_gap07_gapscript", "Circus Act Around The Bend!"),
        ("rando_cjr_gap08_gapscript", "Control Booth Transfer"),
        ("rando_cjr_gap09_gapscript", "Deep Fried Transfer"),
        ("rando_cjr_gap10_gapscript", "Don't Look Down!"),
        ("rando_cjr_gap11_gapscript", "Edge O' the Tub Extension"),
        ("rando_cjr_gap12_gapscript", "From Way Down Town!"),
        ("rando_cjr_gap13_gapscript", "Furnace Row Extension"),
        ("rando_cjr_gap14_gapscript", "Furnace Topper Rail"),
        ("rando_cjr_gap15_gapscript", "Furnace Walk Rail 2 Rail!"),
        # ("rando_cjr_gap16_gapscript", "Furnace Walk"), # vanilla: foun.qb
        ("rando_cjr_gap17_gapscript", "Generator Hop"),
        ("rando_cjr_gap18_gapscript", "Generator Transfer"),
        ("rando_cjr_gap19_gapscript", "Hardway over the Hot Tub"),
        ("rando_cjr_gap20_gapscript", "High Voltage Walkway Lip"),
        ("rando_cjr_gap21_gapscript", "Hot Tub Jump"),
        ("rando_cjr_gap22_gapscript", "Just Passing Through"),
        ("rando_cjr_gap23_gapscript", "Lil' Rail Hop"),
        ("rando_cjr_gap24_gapscript", "Low Current Walkway Lip"),
        ("rando_cjr_gap25_gapscript", "Nausea Grind!!!"),
        ("rando_cjr_gap26_gapscript", "Nice View Up Here!"),
        # ("rando_cjr_gap27_gapscript", "Over the Pipe!"), # vanilla: foun.qb
        ("rando_cjr_gap28_gapscript", "Poolside Over Under Gap"),
        ("rando_cjr_gap29_gapscript", "Porch Rail Tap"),
        ("rando_cjr_gap30_gapscript", "Press Booth Rail 2 Rail"),
        # ("rando_cjr_gap31_gapscript", "Press Box Kink"), # vanilla: foun.qb
        ("rando_cjr_gap32_gapscript", "Press Walk Rail 2 Rail!"),
        ("rando_cjr_gap33_gapscript", "Rail Hop"),
        ("rando_cjr_gap34_gapscript", "Railin' on Furnace Row"),
        ("rando_cjr_gap35_gapscript", "Roll In Hop"),
        ("rando_cjr_gap36_gapscript", "Roll In Transfer"),
        # ("rando_cjr_gap37_gapscript", "Round the Bend!!!"), # vanilla: foun.qb
        ("rando_cjr_gap38_gapscript", "Split the Wickets!"),
        ("rando_cjr_gap39_gapscript", "Stair Steppin'"),
        ("rando_cjr_gap40_gapscript", "Stomp the Presses!"),
        # ("rando_cjr_gap41_gapscript", "TC's Rail"), # vanilla: foun.qb
        ("rando_cjr_gap42_gapscript", "Tub Rail Tap"),
        # ("rando_cjr_gap43_gapscript", "Up And Over!!!"), # vanilla: foun.qb
        ("rando_cjr_gap44_gapscript", "Walkin' A Thin Line!"),
    ]
    foundry_gaps = _shuffle(foundry_gaps)
    vert_gap = foundry_gaps.pop()
    street_gap = foundry_gaps.pop()
    print(vert_gap[1])
    print(street_gap[1])
    cjr = cjr.replace("{{" + vert_gap[0] + "}}", "CJR_Foun_PipeTrickGap")
    cjr = cjr.replace("{{" + street_gap[0] + "}}", "CJR_Foun_RailTrickGap")
    cjr = cjr.replace("{{rando_cjr_trickspot_vert_gap}}", vert_gap[1])
    cjr = cjr.replace("{{rando_cjr_trickspot_street_gap}}", street_gap[1])
    for foundry_gap in foundry_gaps:
        cjr = cjr.replace("{{" + foundry_gap[0] + "}}", "NullScript")
    return cjr


def unlock_trick_scores(airtricks, levels):
    # Trick types will score only 1 unless you have unlocked the corresponding level
    # TODO: Add additional trick types and unlock flags
    unlock_trick_scores = False
    if unlock_trick_scores:
        airtricks = airtricks.replace("{{rando_airtricks_fliptrick_score}}", "CAN_FLIP_TRICK")
        airtricks = airtricks.replace("{{rando_airtricks_grabtrick_score}}", "CAN_FLIP_TRICK")
        airtricks = airtricks.replace("{{rando_airtricks_flipgrabblend_score}}", "CAN_FLIP_TRICK")
    else:
        airtricks = airtricks.replace("{{rando_airtricks_fliptrick_score}}", "159")
        airtricks = airtricks.replace("{{rando_airtricks_grabtrick_score}}", "159")
        airtricks = airtricks.replace("{{rando_airtricks_flipgrabblend_score}}", "159")
    return airtricks

def rando():
    # read modified QBs
    airtricks = read_modified_script_file('airtricks')
    ajc = read_modified_script_file('ajc_scripts')
    alf = read_modified_script_file('alf_scripts')
    bdj = read_modified_script_file('bdj_scripts')
    boardselect = read_modified_script_file('boardselect')
    cjr = read_modified_script_file('cjr_scripts')
    comp_scripts = read_modified_script_file('comp_scripts')
    cpf = read_modified_script_file('cpf_scripts')
    gameflow = read_modified_script_file('gameflow')
    gameqb = read_modified_script_file('game')
    gamemode = read_modified_script_file('gamemode')
    goal_scripts = read_modified_script_file('goal_scripts')
    judges = read_modified_script_file('judges')
    levelsqb = read_modified_script_file('levels')
    mainmenu = read_modified_script_file('mainmenu')
    # physics = read_modified_script_file('physics')
    protricks = read_modified_script_file('protricks')
    sk3_pedscripts = read_modified_script_file('sk3_pedscripts')
    skater_profile = read_modified_script_file('skater_profile')

    # randomize QBs
    levels = get_random_level_order(end_on_comp=False)
    print(
        levels[0].name, levels[1].name, levels[2].name,
        levels[3].name, levels[4].name, levels[5].name,
        levels[6].name, levels[7].name, levels[8].name,
    )

    gameqb = display_victory_requirements(gameqb)
    goal_scripts, mainmenu = randomize_level_requirements(levels, mainmenu, goal_scripts)
    comp_scripts, goal_scripts = randomize_score_goals(levels, goal_scripts, comp_scripts)
    randomize_item_locations(levels)
    skater_profile = randomize_stats(skater_profile)
    skater_profile = randomize_trickstyle(skater_profile)
    gamemode = randomize_level_timer(gamemode)
    trickspot_tricks, ajc, alf, bdj, cjr, cpf = randomize_trickspot_tricks("wild", ajc, alf, bdj, cjr, cpf)
    protricks = randomize_trick_sets(protricks, trickspot_tricks)
    skater_profile = randomize_special_tricks(skater_profile, "easy")
    ajc, bdj, sk3_pedscripts = randomize_impress_ped_scores(ajc, bdj, sk3_pedscripts)
    boardselect = randomize_decks(boardselect)

    goal_scripts = require_deck_for_tape(goal_scripts)
    judges, comp_scripts = require_deck_for_medal(judges, comp_scripts)
    airtricks = unlock_trick_scores(airtricks, levels)

    goal_scripts = randomize_secrets(goal_scripts)
    skater_profile = lock_characters(skater_profile)

    alf = junk_suburbia(alf)
    cjr = randomize_foundry_trickspot_gaps(cjr)

    # write modified QBs
    write_script_file('airtricks', airtricks)
    write_script_file('alf_scripts', alf)
    write_script_file('ajc_scripts', ajc)
    write_script_file('bdj_scripts', bdj)
    write_script_file('boardselect', boardselect)
    write_script_file('cjr_scripts', cjr)
    write_script_file('comp_scripts', comp_scripts)
    write_script_file('cpf_scripts', cpf)
    write_script_file('game', gameqb)
    write_script_file('gameflow', gameflow)
    write_script_file('gamemode', gamemode)
    write_script_file('goal_scripts', goal_scripts)
    write_script_file('judges', judges)
    write_script_file('levels', levelsqb)
    write_script_file('mainmenu', mainmenu)
    # write_script_file('physics', physics)
    write_script_file('protricks', protricks)
    write_script_file('sk3_pedscripts', sk3_pedscripts)
    write_script_file('skater_profile', skater_profile)


if __name__ == "__main__":
    rando()