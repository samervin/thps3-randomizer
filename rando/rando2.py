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
                if level_reqs[i][1] == "first":
                    pass # Don't even add Foundry to the list, it's already unlocked!
                elif level_reqs[i][0] == 1:
                    mainmenu[1857] = f"          STRUCT{{\n            level = LevelNum_Foundry\n            {level_reqs[i][0]} {level_reqs[i][1]} }}\n"
                else:
                    mainmenu[1857] = f"          STRUCT{{\n            level = LevelNum_Foundry\n            {level_reqs[i][0]} {level_reqs[i][1]}s }}\n"
                continue # we handled Foundry separately, go to next level
            case "CANADA":
                mainmenu_line = 1835
            case "RIO":
                mainmenu_line = 1838
            case "SUBURBIA":
                mainmenu_line = 1841
            case "AIRPORT":
                mainmenu_line = 1844
            case "SKATERISLAND":
                mainmenu_line = 1847
            case "LOSANGELES":
                mainmenu_line = 1850
            case "TOKYO":
                mainmenu_line = 1853
            case "SHIP":
                mainmenu_line = 1856
            case _:
                raise Exception("invalid level")

        if level_reqs[i][1] == "first":
            mainmenu[mainmenu_line] = f"            0 Goals }}\n"
        elif level_reqs[i][0] == 1:
            mainmenu[mainmenu_line] = f"            {level_reqs[i][0]} {level_reqs[i][1]} }}\n"
        else:
            mainmenu[mainmenu_line] = f"            {level_reqs[i][0]} {level_reqs[i][1]}s }}\n"

    # patch main menu name
    mainmenu[672] = '                auto_id text = "THPS3 Rando"'

    # patch to unlock the first level instead of always unlocking Foundry
    mainmenu[2288] = f"#00000    SetGlobalFlag flag = LEVEL_UNLOCKED_{levels[0].name_flag}\n"

    # patch to give Foundry a proper GlobalFlag
    mainmenu[2318] = "            LevelNumber = LevelNum_Foundry\n            GlobalFlag = LEVEL_UNLOCKED_FOUNDRY\n"

    # patch to remove levelnums from cassettes (to work around career mode unlock requirement weirdness)
    mainmenu[2318] = "\n"
    mainmenu[2339] = "\n"
    mainmenu[2361] = "\n"
    mainmenu[2383] = "\n"
    mainmenu[2405] = "\n"
    mainmenu[2427] = "\n"
    mainmenu[2449] = "\n"
    mainmenu[2471] = "\n"
    mainmenu[2577] = "\n"

    # patch to remove false/empty info from level select (due to missing levelnums)
    mainmenu[2254:2283] = ["" for line in mainmenu[2254:2283]]

    # patch to only show cassettes if they are unlocked
    mainmenu[2328] = "#00000    IF GetGlobalFlag flag = LEVEL_UNLOCKED_FOUNDRY\n"
    mainmenu[2329] = "#00000    attachchild child = cassette_foundry\n"
    mainmenu[2331] = "#00000    END IF\n"

    mainmenu[2350] = "#00000    IF GetGlobalFlag flag = LEVEL_UNLOCKED_CANADA\n"
    mainmenu[2351] = "#00000    attachchild child = cassette_canada\n"
    mainmenu[2353] = "#00000    END IF\n"

    mainmenu[2372] = "#00000    IF GetGlobalFlag flag = LEVEL_UNLOCKED_RIO\n"
    mainmenu[2373] = "#00000    attachchild child = cassette_rio\n"
    mainmenu[2375] = "#00000    END IF\n"

    mainmenu[2394] = "#00000    IF GetGlobalFlag flag = LEVEL_UNLOCKED_SUBURBIA\n"
    mainmenu[2395] = "#00000    attachchild child = cassette_suburbia\n"
    mainmenu[2397] = "#00000    END IF\n"

    mainmenu[2416] = "#00000    IF GetGlobalFlag flag = LEVEL_UNLOCKED_AIRPORT\n"
    mainmenu[2417] = "#00000    attachchild child = cassette_airport\n"
    mainmenu[2419] = "#00000    END IF\n"

    mainmenu[2438] = "#00000    IF GetGlobalFlag flag = LEVEL_UNLOCKED_SKATERISLAND\n"
    mainmenu[2439] = "#00000    attachchild child = cassette_skater_island\n"
    mainmenu[2441] = "#00000    END IF\n"

    mainmenu[2460] = "#00000    IF GetGlobalFlag flag = LEVEL_UNLOCKED_LOSANGELES\n"
    mainmenu[2461] = "#00000    attachchild child = cassette_los_angeles\n"
    mainmenu[2463] = "#00000    END IF\n"

    mainmenu[2482] = "#00000    IF GetGlobalFlag flag = LEVEL_UNLOCKED_TOKYO\n"
    mainmenu[2483] = "#00000    attachchild child = cassette_tokyo\n"
    mainmenu[2485] = "#00000    END IF\n"

    # patch to set Cruise Ship as "seen" and possibly display cassette
    mainmenu[2486] = "#00000    SetGlobalFlag flag = SPECIAL_HAS_SEEN_SHIP\n"
    mainmenu[2487] = "#00000    IF GetGlobalFlag flag = LEVEL_UNLOCKED_SHIP\n"
    mainmenu[2488] = "#00000      CreateShipCassette\n"
    mainmenu[2489] = "#00000    END IF\n"
    mainmenu[2491] = "#00000    \n"
    mainmenu[2492] = "#00000    \n"
    mainmenu[2493] = "#00000    \n"

    # patch to prevent Cruise Ship from unlocking via 3 medals only
    goal_scripts[8809] = "#00000\n"
    goal_scripts[8810] = "#00000\n"
    goal_scripts[8811] = "\n"
    goal_scripts[8813] = "#00000\n"

    # patch end-of-run level unlock conditions
    goal_scripts[8204] = f"#00000    IF {level_reqs[1][1]}sGreaterThan {level_reqs[1][0]-1}\n"
    goal_scripts[8205] = f"#00000      IF GetGlobalFlag flag = LEVEL_UNLOCKED_{levels[1].name_flag}\n"
    goal_scripts[8208] = f'#00000        UnlockNormalLvl S_Name = "{levels[1].name}"\n'
    goal_scripts[8209] = f"              S_Flag = LEVEL_UNLOCKED_{levels[1].name_flag}\n"

    goal_scripts[8212] = f"#00000      IF {level_reqs[2][1]}sGreaterThan {level_reqs[2][0]-1}\n"
    goal_scripts[8213] = f"#00000        IF GetGlobalFlag flag = LEVEL_UNLOCKED_{levels[2].name_flag}\n"
    goal_scripts[8216] = f'#00000          UnlockNormalLvl S_Name = "{levels[2].name}"\n'
    goal_scripts[8217] = f"                S_Flag = LEVEL_UNLOCKED_{levels[2].name_flag}\n"

    goal_scripts[8220] = f"#00000        IF {level_reqs[3][1]}sGreaterThan {level_reqs[3][0]-1}\n"
    goal_scripts[8221] = f"#00000          IF GetGlobalFlag flag = LEVEL_UNLOCKED_{levels[3].name_flag}\n"
    goal_scripts[8224] = f'#00000            UnlockNormalLvl S_Name = "{levels[3].name}"\n'
    goal_scripts[8225] = f"                  S_Flag = LEVEL_UNLOCKED_{levels[3].name_flag}\n"

    goal_scripts[8228] = f"#00000          IF {level_reqs[4][1]}sGreaterThan {level_reqs[4][0]-1}\n"
    goal_scripts[8229] = f"#00000            IF GetGlobalFlag flag = LEVEL_UNLOCKED_{levels[4].name_flag}\n"
    goal_scripts[8232] = f'#00000              UnlockNormalLvl S_Name = "{levels[4].name}"\n'
    goal_scripts[8233] = f"                    S_Flag = LEVEL_UNLOCKED_{levels[4].name_flag}\n"

    goal_scripts[8236] = f"#00000            IF {level_reqs[5][1]}sGreaterThan {level_reqs[5][0]-1}\n"
    goal_scripts[8237] = f"#00000              IF GetGlobalFlag flag = LEVEL_UNLOCKED_{levels[5].name_flag}\n"
    goal_scripts[8240] = f'#00000                UnlockNormalLvl S_Name = "{levels[5].name}"\n'
    goal_scripts[8241] = f"                      S_Flag = LEVEL_UNLOCKED_{levels[5].name_flag}\n"

    goal_scripts[8244] = f"#00000              IF {level_reqs[6][1]}sGreaterThan {level_reqs[6][0]-1}\n"
    goal_scripts[8245] = f"#00000                IF GetGlobalFlag flag = LEVEL_UNLOCKED_{levels[6].name_flag}\n"
    goal_scripts[8248] = f'#00000                  UnlockNormalLvl S_Name = "{levels[6].name}"\n'
    goal_scripts[8249] = f"                        S_Flag = LEVEL_UNLOCKED_{levels[6].name_flag}\n"

    goal_scripts[8252] = f"#00000                IF {level_reqs[7][1]}sGreaterThan {level_reqs[7][0]-1}\n"
    goal_scripts[8253] = f"#00000                  IF GetGlobalFlag flag = LEVEL_UNLOCKED_{levels[7].name_flag}\n"
    goal_scripts[8256] = f'#00000                    UnlockNormalLvl S_Name = "{levels[7].name}"\n'
    goal_scripts[8257] = f"                          S_Flag = LEVEL_UNLOCKED_{levels[7].name_flag}\n"

    # add additional if-block to account for all 8 unlockable levels
    goal_scripts[8260] = f"#00000                  IF {level_reqs[8][1]}sGreaterThan {level_reqs[8][0]-1}\n"
    goal_scripts[8261] = f"#00000                    IF GetGlobalFlag flag = LEVEL_UNLOCKED_{levels[8].name_flag}\n"
    goal_scripts[8262] = f"""#00000                    ELSE
    #00000                      UnlockNormalLvl S_Name = "{levels[8].name}"
                                S_Flag = LEVEL_UNLOCKED_{levels[8].name_flag}
    #00000                    END IF
    """

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

    for i, level in enumerate(levels):
        match level.name_flag:
            case "FOUNDRY":
                foundry_high = score_goals.pop(0)
                foundry_pro = score_goals.pop(0)
                foundry_sick = score_goals.pop(0)
                goal_scripts[604] = f'          Goal_HighScore_Text = "Get a HIGH SCORE:| {foundry_high},000 Points"\n'
                goal_scripts[605] = f'          Goal_ProScore_Text = "Get a PRO SCORE:| {foundry_pro},000 Points"\n'
                goal_scripts[606] = f'          Goal_SickScore_Text = "Get a SICK SCORE:| {foundry_sick},000 Points"\n'
                goal_scripts[642] = f"#00000      SetScoreGoal Score = {foundry_high}000\n"
                goal_scripts[646] = f"#00000      SetScoreGoal Score = {foundry_pro}000\n"
                goal_scripts[650] = f"#00000      SetScoreGoal Score = {foundry_sick}000\n"
            case "CANADA":
                canada_high = score_goals.pop(0)
                canada_pro = score_goals.pop(0)
                canada_sick = score_goals.pop(0)
                goal_scripts[610] = f'          Goal_HighScore_Text = "Get a HIGH SCORE:| {canada_high},000 Points"\n'
                goal_scripts[611] = f'          Goal_ProScore_Text = "Get a PRO SCORE:| {canada_pro},000 Points"\n'
                goal_scripts[612] = f'          Goal_SickScore_Text = "Get a SICK SCORE:| {canada_sick},000 Points"\n'
                goal_scripts[657] = f"#00000      SetScoreGoal Score = {canada_high}000\n"
                goal_scripts[661] = f"#00000      SetScoreGoal Score = {canada_pro}000\n"
                goal_scripts[665] = f"#00000      SetScoreGoal Score = {canada_sick}000\n"
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
                goal_scripts[616] = f'          Goal_HighScore_Text = "Get a HIGH SCORE:| {suburbia_high},000 Points"\n'
                goal_scripts[617] = f'          Goal_ProScore_Text = "Get a PRO SCORE:| {suburbia_pro},000 Points"\n'
                goal_scripts[618] = f'          Goal_SickScore_Text = "Get a SICK SCORE:| {suburbia_sick},000 Points"\n'
                goal_scripts[672] = f"#00000      SetScoreGoal Score = {suburbia_high}000\n"
                goal_scripts[676] = f"#00000      SetScoreGoal Score = {suburbia_pro}000\n"
                goal_scripts[680] = f"#00000      SetScoreGoal Score = {suburbia_sick}000\n"
            case "AIRPORT":
                airport_high = score_goals.pop(0)
                airport_pro = score_goals.pop(0)
                airport_sick = score_goals.pop(0)
                goal_scripts[622] = f'          Goal_HighScore_Text = "Get a HIGH SCORE:| {airport_high},000 Points"\n'
                goal_scripts[623] = f'          Goal_ProScore_Text = "Get a PRO SCORE:| {airport_pro},000 Points"\n'
                goal_scripts[624] = f'          Goal_SickScore_Text = "Get a SICK SCORE:| {airport_sick},000 Points"\n'
                goal_scripts[690] = f"#00000      SetScoreGoal Score = {airport_high}000\n"
                goal_scripts[694] = f"#00000      SetScoreGoal Score = {airport_pro}000\n"
                goal_scripts[698] = f"#00000      SetScoreGoal Score = {airport_sick}000\n"
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
                goal_scripts[628] = f'          Goal_HighScore_Text = "Get a HIGH SCORE:| {los_angeles_high},000 Points"\n'
                goal_scripts[629] = f'          Goal_ProScore_Text = "Get a PRO SCORE:| {los_angeles_pro},000 Points"\n'
                goal_scripts[630] = f'          Goal_SickScore_Text = "Get a SICK SCORE:| {los_angeles_sick},000 Points"\n'
                goal_scripts[708] = f"#00000      SetScoreGoal Score = {los_angeles_high}000\n"
                goal_scripts[712] = f"#00000      SetScoreGoal Score = {los_angeles_pro}000\n"
                goal_scripts[716] = f"#00000      SetScoreGoal Score = {los_angeles_sick}000\n"
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
                goal_scripts[634] = f'          Goal_HighScore_Text = "Get a HIGH SCORE:| {cruise_ship_high},000 Points"\n'
                goal_scripts[635] = f'          Goal_ProScore_Text = "Get a PRO SCORE:| {cruise_ship_pro},000 Points"\n'
                goal_scripts[636] = f'          Goal_SickScore_Text = "Get a SICK SCORE:| {cruise_ship_sick},000 Points"\n'
                goal_scripts[726] = f"#00000      SetScoreGoal Score = {cruise_ship_high}000\n"
                goal_scripts[730] = f"#00000      SetScoreGoal Score = {cruise_ship_pro}000\n"
                goal_scripts[734] = f"#00000      SetScoreGoal Score = {cruise_ship_sick}000\n"
            case _:
                raise Exception("invalid level")
    return comp_scripts

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

def patch_view_goals_menu(goal_scripts):
    # patch goal menu to actually wait a sec before it lets you back out
    goal_scripts[8285] = "#00000    ListAllGoals\n"
    goal_scripts[8286] = "#00000    wait 1 second\n"

def require_deck_for_tape(goal_scripts):
    # require the deck to be collected before the tape goal will complete
    # note: as currently implemented, if you get the tape before the deck, you will have to retry the run to respawn the tape

    goal_scripts[2101] = "#00000    SpawnScript Got_Secret_TapeIfDeck\n"
    goal_scripts[9298] = """#00000  FUNCTION Got_Secret_TapeIfDeck
    #00000    IF GetFlag flag = GOAL_DECK

    #00000      SetGoal goal = GOAL_TAPE

    #00000      wait 4 frames
    #00000      WaitForGoalCompletionTextFree
    #00000      SetFlag flag = WAIT_FOR_TAPE

    #00000      LaunchLocalMessage id = GoalName
                "Secret Tape!" panel_message_goalcomplete
    #00000      LaunchLocalMessage id = complete
                "Complete" panel_message_goalcompleteline2
    #00000      SetGlobalFlag flag = SKATESHOP_JUST_GOT_GOAL

    #00000      PlaySound goaldone Vol = 100

    #00000      wait 2 seconds
    #00000      UnSetFlag flag = WAIT_FOR_TAPE

    #00000      MidGameCheckGoals
    #00000    ELSE
    #00000      LaunchLocalMessage id = GoalName
                "Secret tape lost..." panel_message_goalcomplete
    #00000      LaunchLocalMessage id = complete
                "You need the deck first!" panel_message_goalcompleteline2

    #00000      PlaySound GUI_buzzer01 Vol = 100
    #00000    END IF

    #00000  END FUNCTION
    """

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
    gamemode[275] = f"          default_time_limit = {time_limit}\n"

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
    for i in range(4, 12):
        protricks[i] = f"          {ButtonBinds().get_regular_lip_binds()[i-4].name} = {vert_lips.pop().name_script}\n"
    street_lips = _shuffle(Tricks().get_regular_lips())[:(8-len(trickspot_lips))] # first 8 entries, fewer if trickspots exist
    street_lips = _shuffle(street_lips + trickspot_lips)
    for i in range(17, 25):
        protricks[i] = f"          {ButtonBinds().get_regular_lip_binds()[i-17].name} = {street_lips.pop().name_script}\n"
    hawk_lips = _shuffle(Tricks().get_regular_lips())[:(8-len(trickspot_lips))] # first 8 entries, fewer if trickspots exist
    hawk_lips = _shuffle(hawk_lips + trickspot_lips)
    for i in range(30, 38):
        protricks[i] = f"          {ButtonBinds().get_regular_lip_binds()[i-30].name} = {hawk_lips.pop().name_script}\n"
    all_around_grabs = _shuffle(Tricks().get_regular_grabs())[:(12-len(trickspot_grabs))] # first 12 entries, fewer if trickspots exist
    all_around_grabs = _shuffle(all_around_grabs + trickspot_grabs)
    for i in range(43, 55):
        protricks[i] = f"          {ButtonBinds().get_regular_grab_binds()[i-43].name} = {all_around_grabs.pop().name_script}\n"
    street_grabs = _shuffle(Tricks().get_regular_grabs())[:(12-len(trickspot_grabs))] # first 12 entries, fewer if trickspots exist
    street_grabs = _shuffle(street_grabs + trickspot_grabs)
    for i in range(60, 72):
        protricks[i] = f"          {ButtonBinds().get_regular_grab_binds()[i-60].name} = {street_grabs.pop().name_script}\n"
    vert_grabs = _shuffle(Tricks().get_regular_grabs())[:(12-len(trickspot_grabs))] # first 12 entries, fewer if trickspots exist
    vert_grabs = _shuffle(vert_grabs + trickspot_grabs)
    for i in range(77, 89):
        protricks[i] = f"          {ButtonBinds().get_regular_grab_binds()[i-77].name} = {vert_grabs.pop().name_script}\n"
    vert_flips = _shuffle(Tricks().get_regular_flips())[:(12-len(trickspot_flips))] # first 12 entries, fewer if trickspots exist
    vert_flips = _shuffle(vert_flips + trickspot_flips)
    for i in range(94, 106):
        protricks[i] = f"          {ButtonBinds().get_regular_flip_binds()[i-94].name} = {vert_flips.pop().name_script}\n"
    freestyle_flips = _shuffle(Tricks().get_regular_flips())[:(12-len(trickspot_flips))] # first 12 entries, fewer if trickspots exist
    freestyle_flips = _shuffle(freestyle_flips + trickspot_flips)
    for i in range(111, 123):
        protricks[i] = f"          {ButtonBinds().get_regular_flip_binds()[i-111].name} = {freestyle_flips.pop().name_script}\n"
    street_flips = _shuffle(Tricks().get_regular_flips())[:(12-len(trickspot_flips))] # first 12 entries, fewer if trickspots exist
    street_flips = _shuffle(street_flips + trickspot_flips)
    for i in range(128, 140):
        protricks[i] = f"          {ButtonBinds().get_regular_flip_binds()[i-128].name} = {street_flips.pop().name_script}\n"
    # Tony Hawk doesn't get to be special anymore
    protricks[289] = f"          HawkLip VertFlips VertGrabs ExtraSlot1 = Trick_Revert\n          ExtraSlot2 = Trick_Revert\n          JumpSlot = Trick_Fastplant\n"
    protricks[290:316] = ["" for line in protricks[290:316]]

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
    grips = _shuffle(Boards().get_grips())
    # Randomize default grip tapes (don't change the descriptions here!)
    for i in range(32):
        boardselect[1957 + (i*5)] = f'            texture = "{grips[i].texture}"\n'
    # Randomize selectable grip tapes in the skate shop menu
    for i in range(10):
        boardselect[292 + (i*4)] = f'                GripTapeDescription = "{grips[i].name}"\n'
        boardselect[293 + (i*4)] = f'                GripTapeTexture = "{grips[i].texture}"\n'
    for i in range(10):
        boardselect[339 + (i*4)] = f'                GripTapeDescription = "{grips[i+10].name}"\n'
        boardselect[340 + (i*4)] = f'                GripTapeTexture = "{grips[i+10].texture}"\n'
    for i in range(10):
        boardselect[386 + (i*4)] = f'                GripTapeDescription = "{grips[i+20].name}"\n'
        boardselect[387 + (i*4)] = f'                GripTapeTexture = "{grips[i+20].texture}"\n'

    decks = _shuffle(Boards().get_decks())
    for i in range(230):
        # TODO: Change name too
        boardselect[802 + (i*5)] = f'            texture = "{decks[i].texture}"\n'

def randomize_secrets(goal_scripts):
    # UnlockNextSecret is a builtin, but seems to key off the SecretScripts array

    # There are 22 "normal" secrets for 100% completion, add a 23rd for Doomguy
    goal_scripts[7489] = "          THPS3_secret_1 THPS3_secret_2 THPS3_secret_3 THPS3_secret_4 THPS3_secret_5 THPS3_secret_6 THPS3_secret_7 THPS3_secret_8 THPS3_secret_9 THPS3_secret_10 THPS3_secret_11 THPS3_secret_12 THPS3_secret_13 THPS3_secret_14 THPS3_secret_15 THPS3_secret_16 THPS3_secret_17 THPS3_secret_18 THPS3_secret_19 THPS3_secret_20 THPS3_secret_21 THPS3_secret_22 THPS3_secret_23\n"
    # Rewrite ExecuteNextSecret_20to29 to fit in 23rd secret condition
    # Global flags seem to be hardcoded, but CHEAT_UNLOCKED_12 is not used, so we can repurpose it here
    goal_scripts[9211:9227] = ["" for line in goal_scripts[9211:9227]]
    goal_scripts[9210] = """#00000  FUNCTION ExecuteNextSecret_20to29
    #00000    IF GetGlobalFlag flag = CHEAT_UNLOCKED_12
    #00000      THPS3_secretScript_23
    #00000    ELSE
    #00000      IF GetGlobalFlag flag = SECRET_UNLOCK_22
    #00000        THPS3_secretScript_22
    #00000      ELSE
    #00000        IF GetGlobalFlag flag = SECRET_UNLOCK_21
    #00000          THPS3_secretScript_21
    #00000        ELSE
    #00000          IF GetGlobalFlag flag = SECRET_UNLOCK_20
    #00000            THPS3_secretScript_20
    #00000          ELSE
    #00000          END IF
    #00000        END IF
    #00000      END IF
    #00000    END IF
    #00000  END FUNCTION
    """
    # TODO: For now, first person mode is always 23rd/last:
    # It contains "Entire Game complete" logic and the last secret cannot be a skater anyway
    goal_scripts[7624] = "#00000  FUNCTION THPS3_secretScript_23\n"
    # Shuffle the remaining secrets 1-22
    secrets = _shuffle([1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22])
    goal_scripts[7492] = f"#00000  FUNCTION THPS3_secretScript_{secrets.pop()} \n"
    goal_scripts[7500] = f"#00000  FUNCTION THPS3_secretScript_{secrets.pop()} \n"
    goal_scripts[7508] = f"#00000  FUNCTION THPS3_secretScript_{secrets.pop()} \n"
    goal_scripts[7514] = f"#00000  FUNCTION THPS3_secretScript_{secrets.pop()} \n"
    goal_scripts[7520] = f"#00000  FUNCTION THPS3_secretScript_{secrets.pop()} \n"
    goal_scripts[7526] = f"#00000  FUNCTION THPS3_secretScript_{secrets.pop()} \n"
    goal_scripts[7532] = f"#00000  FUNCTION THPS3_secretScript_{secrets.pop()} \n"
    goal_scripts[7538] = f"#00000  FUNCTION THPS3_secretScript_{secrets.pop()} \n"
    goal_scripts[7544] = f"#00000  FUNCTION THPS3_secretScript_{secrets.pop()} \n"
    goal_scripts[7550] = f"#00000  FUNCTION THPS3_secretScript_{secrets.pop()} \n"
    goal_scripts[7556] = f"#00000  FUNCTION THPS3_secretScript_{secrets.pop()} \n"
    goal_scripts[7564] = f"#00000  FUNCTION THPS3_secretScript_{secrets.pop()} \n"
    goal_scripts[7570] = f"#00000  FUNCTION THPS3_secretScript_{secrets.pop()} \n"
    goal_scripts[7576] = f"#00000  FUNCTION THPS3_secretScript_{secrets.pop()} \n"
    goal_scripts[7582] = f"#00000  FUNCTION THPS3_secretScript_{secrets.pop()} \n"
    goal_scripts[7588] = f"#00000  FUNCTION THPS3_secretScript_{secrets.pop()} \n"
    goal_scripts[7594] = f"#00000  FUNCTION THPS3_secretScript_{secrets.pop()} \n"
    goal_scripts[7600] = f"#00000  FUNCTION THPS3_secretScript_{secrets.pop()} \n"
    goal_scripts[7606] = f"#00000  FUNCTION THPS3_secretScript_{secrets.pop()} \n"
    goal_scripts[7612] = f"#00000  FUNCTION THPS3_secretScript_{secrets.pop()} \n"
    goal_scripts[7618] = f"#00000  FUNCTION THPS3_secretScript_{secrets.pop()} \n"
    goal_scripts[7645] = f"#00000  FUNCTION THPS3_secretScript_{secrets.pop()} \n"
    # Add new method at the bottom of goal_scripts, again reusing CHEAT_UNLOCKED_12
    # Memory addresses account for require_deck_for_tape function defined elsewhere
    goal_scripts.append(f"\n#00000  FUNCTION THPS3_secret_23\n#00000    SetGlobalFlag flag = CHEAT_UNLOCKED_12\n#00000  END FUNCTION\n")

    # TODO: Edit Cheat menu to appear when the first cheat is unlocked, rather than only Snowboard mode

    # Demonstration: Remove medal requirements from secret unlock
    # goal_scripts[8820:8826] = ["\n" for line in goal_scripts[8820:8826]]
    # goal_scripts[8847:8850] = ["\n" for line in goal_scripts[8847:8850]]
    # Demonstration: Reduce goal requirements down to 1
    goal_scripts[8826] = "#00000          IF GoalsGreaterThan 0\n"

    # Move secret unlock check for normal levels so that all goals are not required
    goal_scripts[6887] = "#00000      GoalViewAllGoalCompleteCheck From_movies\n#00000      Goal_UnlockingSecrets\n"
    goal_scripts[6897] = "\n"
    # TODO: move secret unlock for comp levels as well

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
    mainmenu = read_script_file('mainmenu')
    goal_scripts = read_script_file('goal_scripts')
    skater_profile = read_script_file('skater_profile')
    gamemode = read_script_file('gamemode')
    ajc = read_script_file('ajc_scripts')
    alf = read_script_file('alf_scripts')
    bdj = read_script_file('bdj_scripts')
    cjr = read_script_file('cjr_scripts')
    cpf = read_script_file('cpf_scripts')
    protricks = read_script_file('protricks')
    sk3_pedscripts = read_script_file('sk3_pedscripts')
    boardselect = read_script_file('boardselect')

    # read modified QBs
    comp_scripts = read_modified_script_file('comp_scripts')
    gameqb = read_modified_script_file('game')
    judges = read_modified_script_file('judges')
    levelsqb = read_modified_script_file('levels')

    # randomize QBs
    levels = get_random_level_order(end_on_comp=True)
    print(
        levels[0].name, levels[1].name, levels[2].name,
        levels[3].name, levels[4].name, levels[5].name,
        levels[6].name, levels[7].name, levels[8].name,
    )
    patch_view_goals_menu(goal_scripts)

    gameqb = display_victory_requirements(gameqb)
    randomize_level_requirements(levels, mainmenu, goal_scripts)
    comp_scripts = randomize_score_goals(levels, goal_scripts, comp_scripts)
    randomize_item_locations(levels)
    skater_profile = randomize_stats(skater_profile)
    randomize_trickstyle(skater_profile)
    randomize_level_timer(gamemode)
    trickspot_tricks = randomize_trickspot_tricks("wild", ajc, alf, cjr, cpf, bdj)
    randomize_trick_sets(protricks, trickspot_tricks)
    randomize_special_tricks(skater_profile, "easy")
    randomize_impress_ped_scores(sk3_pedscripts, ajc, bdj)
    randomize_decks(boardselect)

    require_deck_for_tape(goal_scripts)
    judges, comp_scripts = require_deck_for_medal(judges, comp_scripts)

    randomize_secrets(goal_scripts)
    lock_characters(skater_profile)

    junk_suburbia(alf)

    # write vanilla QBs
    write_script_file('mainmenu', mainmenu)
    write_script_file('goal_scripts', goal_scripts)
    write_script_file('skater_profile', skater_profile)
    write_script_file('gamemode', gamemode)
    write_script_file('ajc_scripts', ajc)
    write_script_file('alf_scripts', alf)
    write_script_file('bdj_scripts', bdj)
    write_script_file('cjr_scripts', cjr)
    write_script_file('cpf_scripts', cpf)
    write_script_file('protricks', protricks)
    write_script_file('sk3_pedscripts', sk3_pedscripts)
    write_script_file('boardselect', boardselect)

    # write modified QBs
    write_script_file('comp_scripts', comp_scripts)
    write_script_file('game', gameqb)
    write_script_file('judges', judges)
    write_script_file('levels', levelsqb)
