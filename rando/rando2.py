# coding: cp1252

import random
import re
import os

from constants import *
from level_foundry import LevelFoundry
from level_canada import LevelCanada
from level_rio import LevelRio
from level_suburbia import LevelSuburbia
from level_airport import LevelAirport
from level_skaterisland import LevelSkaterIsland
from level_losangeles import LevelLosAngeles
from level_tokyo import LevelTokyo
from level_cruiseship import LevelCruiseShip
from tricks import Tricks
from button_binds import ButtonBinds
from boards import Boards
from secrets import Secrets

def _shuffle(any_list):
    shuffled = any_list.copy()
    random.shuffle(shuffled)
    return shuffled

def read_script_file(filename):
    with open(f'../vanilla-qbs/Scripts/{filename}.qb', 'r') as f:
        return f.readlines()

def read_modified_script_file(filename):
    with open(f'../modified-qbs/Scripts/{filename}.qb', 'r') as f:
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
    full_filename = f'../outfiles/Scripts/{filename}.out'
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
                req = random.randint(3, 9)
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
    score_goals.append(random.randint(15, 45))
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

    stat_presets = ["max", "easy", "default", "hard", "impossible"]
    stat_presets = _shuffle(stat_presets)

    match stat_presets[0]:
        case "max":
            stat_num = 10
        case "easy":
            stat_num = 7
        case "default":
            stat_num = None
        case "hard":
            stat_num = 2
        case "impossible":
            stat_num = 0
        case _:
            stat_num = None

    if stat_num is not None:
        skater_profile = ''.join(skater_profile)
        skater_profile = re.sub(r'(?<=air = )\d+', str(stat_num), skater_profile)
        skater_profile = re.sub(r'(?<=hangtime = )\d+', str(stat_num), skater_profile)
        skater_profile = re.sub(r'(?<=ollie = )\d+', str(stat_num), skater_profile)
        skater_profile = re.sub(r'(?<=speed = )\d+', str(stat_num), skater_profile)
        skater_profile = re.sub(r'(?<=spin = )\d+', str(stat_num), skater_profile)
        skater_profile = re.sub(r'(?<=switch = )\d+', str(stat_num), skater_profile)
        skater_profile = re.sub(r'(?<=rail_balance = )\d+', str(stat_num), skater_profile)
        skater_profile = re.sub(r'(?<=lip_balance = )\d+', str(stat_num), skater_profile)
        skater_profile = re.sub(r'(?<=manual_balance = )\d+', str(stat_num), skater_profile)
        skater_profile = skater_profile.splitlines(keepends=True)

    return skater_profile

def _get_random_trickstyle():
    trickstyles = ['vert', 'street']
    return random.choice(trickstyles)

def randomize_trickstyle(skater_profile):
    # randomize whether each skater is street or vert
    for index, line in enumerate(skater_profile):
        skater_profile[index] = re.sub(r'(?<=trickstyle = )\w+', _get_random_trickstyle(), line)

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

def randomize_trickspot_tricks(trick_type, ajc, alf, cjr, cpf, bdj):
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

    cjr[1275] = f'          Goal_TrickSpotStreet_Text = "{foundry_street_trick.name_goal}| TC\'s Rail"\n'
    cjr[1276] = f'          Goal_TrickSpotVert_Text = "{foundry_vert_trick.name_goal}| Over the Half Pipe"\n'
    cjr[4623] = f'#00000      StartGapTrick TrickText = "{foundry_street_trick.name}"\n'
    cjr[4614] = f'#00000      StartGapTrick TrickText = "{foundry_vert_trick.name}"\n'
    ajc[20] = f'          Goal_TrickspotStreet_Text = "{canada_street_trick.name_goal}| Around the Horn"\n'
    ajc[21] = f'          Goal_TrickspotVert_Text = "{canada_vert_trick.name_goal}| Over the Blade"\n'
    ajc[2567] = f'#00000      StartGapTrick tricktext = "{canada_street_trick.name}"\n'
    ajc[2576] = f'#00000      StartGapTrick tricktext = "{canada_vert_trick.name}"\n'
    alf[214] = f'          Goal_TrickspotStreet_Text = "{suburbia_street_trick.name_goal}| the Trailer Hop"\n'
    alf[215] = f'          Goal_TrickspotVert_Text = "{suburbia_vert_trick.name_goal}| Between the Ramps"\n'
    alf[734] = f'#00000        StartGapTrick tricktext = "{suburbia_street_trick.name}"\n'
    alf[721] = f'#00000        StartGapTrick tricktext = "{suburbia_vert_trick.name}"\n'
    cpf[23] = f'          Goal_TrickspotStreet_Text = "{airport_street_trick.name_goal}| Around the Baggage Claim"\n'
    cpf[24] = f'          Goal_TrickspotVert_Text = "{airport_vert_trick.name_goal}| Over an Escalator"\n'
    cpf[6838] = f'#00000      StartGapTrick tricktext = "{airport_street_trick.name}"\n'
    cpf[6771] = f'#00000      StartGapTrick tricktext = "{airport_vert_trick.name}"\n'
    cpf[255] = f'          Goal_TrickspotStreet_Text = "{la_street_trick.name_goal}| the Tower Rails Gap"\n'
    cpf[256] = f'          Goal_TrickspotVert_Text = "{la_vert_trick.name_goal}| the Tower Poppin\' Transfer"\n'
    cpf[6874] = f'#00000      StartGapTrick tricktext = "{la_street_trick.name}"\n'
    cpf[6909] = f'#00000      StartGapTrick tricktext = "{la_vert_trick.name}"\n'
    bdj[78] = f'          Goal_TrickspotStreet_Text = "{ship_street_trick.name_goal}| an Awning"\n'
    bdj[79] = f'          Goal_TrickspotVert_Text = "{ship_vert_trick.name_goal}| the High Wires"\n'
    bdj[286] = f'#00000    StartGapTrick TrickText = "{ship_street_trick.name}"\n'
    bdj[278] = f'#00000        StartGapTrick TrickText = "{ship_vert_trick.name}"\n'

    return [
        foundry_street_trick, foundry_vert_trick, canada_street_trick, canada_vert_trick,
        suburbia_street_trick, suburbia_vert_trick, airport_street_trick, airport_vert_trick,
        la_street_trick, la_vert_trick, ship_street_trick, ship_vert_trick
    ]

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
    default_special_lines = [ # one per character for now
        1468, # 1472, 1476, 1480,
        1544, # 1548, 1552, 1556,
        1620, # 1624, 1628, 1632,
        1696, # 1700, 1704, 1708,
        1772, # 1776, 1780, 1784,
        1848, # 1852, 1856, 1860,
        1924, # 1928, 1932, 1936,
        2000, # 2004, 2008, 2012,
        2076, # 2080, 2084, 2088,
        2152, # 2156, 2160, 2164,
        2228, # 2232, 2236, 2240,
        2304, # 2308, 2312, 2316,
        2380, # 2384, 2388, 2392,
        2457, # 2461, 2465, 2469,
        2534, # 2538, 2542, 2546,
        2611, # 2615, 2619, 2623,
        2688, # 2692, 2696, 2700,
        2765, # 2769, 2773, 2777,
        2842, # 2846, 2850, 2854,
        2919, # 2923, 2927, 2931,
        2996, # 3000, 3004, 3008,
        3073, # 3077, 3081, 3085,
        3150, # 3154, 3158, 3162,
    ]
    for line in default_special_lines:
        four_specials = _shuffle(Tricks().get_all_special_tricks())[:4]
        binds = ButtonBinds()
        grind_binds = binds.get_special_grind_binds(difficulty)
        air_binds = binds.get_special_air_binds(difficulty)
        lip_binds = binds.get_special_lip_binds(difficulty)
        manual_binds = binds.get_special_manual_binds(difficulty)
        for i, special in enumerate(four_specials):
            skater_profile[(i*4)+line+1] = f"                  trickname = {special.name_script}\n"
            match special.trick_type:
                case "grind":
                    skater_profile[(i*4)+line] = f"                  trickslot = {grind_binds.pop().name}\n"
                case "grab" | "flip":
                    skater_profile[(i*4)+line] = f"                  trickslot = {air_binds.pop().name}\n"
                case "lip":
                    skater_profile[(i*4)+line] = f"                  trickslot = {lip_binds.pop().name}\n"
                case "manual":
                    skater_profile[(i*4)+line] = f"                  trickslot = {manual_binds.pop().name}\n"
                case _:
                    raise Exception("invalid trick type")

def randomize_impress_ped_scores(sk3_pedscripts, ajc, bdj):
    ped_canada_score = random.randint(2, 25)
    ped_canada_chatter = int(ped_canada_score/2) # Used for voice lines
    ped_ship_score = random.randint(2, 25)
    ped_ship_chatter = int(ped_ship_score/2) # Used for voice lines
    sk3_pedscripts[265] = f"          MinPropsScoreDuring = {ped_ship_chatter}000\n"
    sk3_pedscripts[266] = f"          MinPropsScoreDuring2 = {ped_ship_score}000\n"
    sk3_pedscripts[267] = f"          MinPropsScoreLanding = {ped_ship_chatter}000\n"
    sk3_pedscripts[268] = f"          MinPropsScoreLanding2 = {ped_ship_score}000\n"
    sk3_pedscripts[484] = f"          MinPropsScoreDuring = {ped_canada_chatter}000\n"
    sk3_pedscripts[485] = f"          MinPropsScoreDuring2 = {ped_canada_score}000\n"
    sk3_pedscripts[486] = f"          MinPropsScoreLanding = {ped_canada_chatter}000\n"
    sk3_pedscripts[487] = f"          MinPropsScoreLanding2 = {ped_canada_score}000\n"
    ajc[23] = f'          Goal_Scripted2_Text = "Impress the Skaters| With {ped_canada_score},000 Points"\n'
    bdj[82] = f'          Goal_Scripted3_Text = "Impress Neversoft Girls| With {ped_ship_score},000 Points"\n'

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
    # Global flags are hardcoded, but CHEAT_UNLOCKED_12 is not used, so we repurpose it for the 23rd secret

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
    noncharacter_flags = Secrets().secret_flags_levels + Secrets().secret_flags_cheats
    noncharacter_flags = _shuffle(noncharacter_flags)
    skater_profile[1539] = f"            default_trick_mapping = CaballeroTricks\n            unlock_flag = {noncharacter_flags.pop()}\n"
    skater_profile[1615] = f"            default_trick_mapping = CampbellTricks\n            unlock_flag = {noncharacter_flags.pop()}\n"
    skater_profile[1691] = f"            default_trick_mapping = GlifbergTricks\n            unlock_flag = {noncharacter_flags.pop()}\n"
    skater_profile[1767] = f"            default_trick_mapping = KostonTricks\n            unlock_flag = {noncharacter_flags.pop()}\n"
    skater_profile[1843] = f"            default_trick_mapping = LasekTricks\n            unlock_flag = {noncharacter_flags.pop()}\n"
    skater_profile[1919] = f"            default_trick_mapping = MargeraTricks\n            unlock_flag = {noncharacter_flags.pop()}\n"
    skater_profile[1995] = f"            default_trick_mapping = MullenTricks\n            unlock_flag = {noncharacter_flags.pop()}\n"
    skater_profile[2071] = f"            default_trick_mapping = MuskaTricks\n            unlock_flag = {noncharacter_flags.pop()}\n"
    skater_profile[2147] = f"            default_trick_mapping = ReynoldsTricks\n            unlock_flag = {noncharacter_flags.pop()}\n"
    skater_profile[2223] = f"            default_trick_mapping = RowleyTricks\n            unlock_flag = {noncharacter_flags.pop()}\n"
    skater_profile[2299] = f"            default_trick_mapping = SteamerTricks\n            unlock_flag = {noncharacter_flags.pop()}\n"
    skater_profile[2375] = f"            default_trick_mapping = ThomasTricks\n            unlock_flag = {noncharacter_flags.pop()}\n"
    skater_profile[3145] = f"            default_trick_mapping = CustomTricks\n            unlock_flag = {noncharacter_flags.pop()}\n"

def junk_suburbia(alf):
    # Increase ice cream truck from 20 mph
    alf[2977] = '#00000    Obj_SetPathVelocity 100 mph '
    # Make the thin man fall in love with Tony Hawk
    alf[2010] = '#00000        IF ProfileEquals Is_Named = hawk '


if __name__ == "__main__":
    # read vanilla QBs
    skater_profile = read_script_file('skater_profile')
    ajc = read_script_file('ajc_scripts')
    alf = read_script_file('alf_scripts')
    bdj = read_script_file('bdj_scripts')
    cjr = read_script_file('cjr_scripts')
    cpf = read_script_file('cpf_scripts')
    sk3_pedscripts = read_script_file('sk3_pedscripts')

    # read modified QBs
    boardselect = read_modified_script_file('boardselect')
    comp_scripts = read_modified_script_file('comp_scripts')
    gameqb = read_modified_script_file('game')
    gamemode = read_modified_script_file('gamemode')
    goal_scripts = read_modified_script_file('goal_scripts')
    judges = read_modified_script_file('judges')
    levelsqb = read_modified_script_file('levels')
    mainmenu = read_modified_script_file('mainmenu')
    protricks = read_modified_script_file('protricks')

    # randomize QBs
    levels = get_random_level_order(end_on_comp=True)
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
    randomize_trickstyle(skater_profile)
    gamemode = randomize_level_timer(gamemode)
    trickspot_tricks = randomize_trickspot_tricks("wild", ajc, alf, cjr, cpf, bdj)
    protricks = randomize_trick_sets(protricks, trickspot_tricks)
    randomize_special_tricks(skater_profile, "easy")
    randomize_impress_ped_scores(sk3_pedscripts, ajc, bdj)
    boardselect = randomize_decks(boardselect)

    goal_scripts = require_deck_for_tape(goal_scripts)
    judges, comp_scripts = require_deck_for_medal(judges, comp_scripts)

    goal_scripts = randomize_secrets(goal_scripts)
    lock_characters(skater_profile)

    junk_suburbia(alf)

    # write vanilla QBs
    write_script_file('skater_profile', skater_profile)
    write_script_file('ajc_scripts', ajc)
    write_script_file('alf_scripts', alf)
    write_script_file('bdj_scripts', bdj)
    write_script_file('cjr_scripts', cjr)
    write_script_file('cpf_scripts', cpf)
    write_script_file('sk3_pedscripts', sk3_pedscripts)

    # write modified QBs
    write_script_file('boardselect', boardselect)
    write_script_file('comp_scripts', comp_scripts)
    write_script_file('game', gameqb)
    write_script_file('gamemode', gamemode)
    write_script_file('goal_scripts', goal_scripts)
    write_script_file('judges', judges)
    write_script_file('levels', levelsqb)
    write_script_file('mainmenu', mainmenu)
    write_script_file('protricks', protricks)
