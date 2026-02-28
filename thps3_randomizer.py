# coding: cp1252
import os
import re
from dataclasses import dataclass

import random

import rando2
from rando.level2 import Level2
from rando.level_foundry import LevelFoundry
from rando.level_canada import LevelCanada
from rando.level_rio import LevelRio
from rando.level_suburbia import LevelSuburbia
from rando.level_airport import LevelAirport
from rando.level_skaterisland import LevelSkaterIsland
from rando.level_losangeles import LevelLosAngeles
from rando.level_tokyo import LevelTokyo
from rando.level_cruiseship import LevelCruiseShip


@dataclass
class ScriptQBs:
    """Container for all modified QB files in the Scripts directory."""

    airtricks_qb: str
    ajc_scripts_qb: str
    alf_scripts_qb: str
    bdj_scripts_qb: str
    boardselect_qb: str
    cjr_scripts_qb: str
    comp_scripts_qb: str
    cpf_scripts_qb: str
    game_qb: str
    gameflow_qb: str
    gamemode_qb: str
    goal_scripts_qb: str
    judges_qb: str
    levels_qb: str
    mainmenu_qb: str
    protricks_qb: str
    sk3_pedscripts_qb: str
    skater_profile_qb: str
    # TODO: Add method for string replacement here


def _shuffle(any_list):
    shuffled = any_list.copy()
    random.shuffle(shuffled)
    return shuffled


def memify_script(script: str) -> str:
    """Update memory addresses in a script string to prepare for writing."""
    # make one long string, then split on lines, to include modified linebreaks
    script = "".join(script)
    scriptlines = script.splitlines(keepends=True)
    output = []
    for i, line in enumerate(scriptlines):
        # substitute any memory address like #00000 with i (the current line number) zero-padded to 5 spaces
        output.append(re.sub(r"#\d{5}", f"#{i:05d}", line))
    return "".join(output)


def read_modified_script_qb(filename: str) -> str:
    with open(f"qbs_modified/Scripts/{filename}.qb", "r") as f:
        return f.read()


def write_modified_script_outfile(filename: str, contents: str) -> None:
    contents = memify_script(contents)
    full_filename = f"qbs_outfiles/Scripts/{filename}.out"
    os.makedirs(os.path.dirname(full_filename), exist_ok=True)
    with open(full_filename, "w", newline="\n") as fout:
        fout.write(contents)


def read_modified_script_qbs() -> ScriptQBs:
    # airtricks used for trick type locking
    # ajc used in trickspot trick randomization and impress pedestrian goals
    # alf used in trickspot trick randomization and suburbia junk
    # bdj used in trickspot trick randomization and impress pedestrian goals
    # boardselect used to randomize decks
    # cjr used in trickspot trick randomization and foundry gap randomization
    # comp_scripts randomizes competition score goals and requires deck for medals
    # cpf used in trickspot trick randomization
    # gameflow used only to bypass save dialog after runs, not randomized
    # game used to change level display requirements
    # gamemode randomizes time limit for normal levels
    # goal_scripts randomizes level unlock requirements and score goals,
    #     as well as requiring the deck for the tape + randomizing secret unlocks
    # judges used to require deck for medals
    # levels used only to load files from the correct directory, not randomized
    # mainmenu randomizes level unlock requirements
    # protricks randomizes trick sets for all skaters
    # sk3_pedscripts randomizes impress pedestrian goals
    # skater_profile randomizes stats, trickstyles, specials,
    #    and whether a skater starts locked, for all skaters
    return ScriptQBs(
        airtricks_qb=read_modified_script_qb("airtricks"),
        ajc_scripts_qb=read_modified_script_qb("ajc_scripts"),
        alf_scripts_qb=read_modified_script_qb("alf_scripts"),
        bdj_scripts_qb=read_modified_script_qb("bdj_scripts"),
        boardselect_qb=read_modified_script_qb("boardselect"),
        cjr_scripts_qb=read_modified_script_qb("cjr_scripts"),
        comp_scripts_qb=read_modified_script_qb("comp_scripts"),
        cpf_scripts_qb=read_modified_script_qb("cpf_scripts"),
        game_qb=read_modified_script_qb("game"),
        gameflow_qb=read_modified_script_qb("gameflow"),
        gamemode_qb=read_modified_script_qb("gamemode"),
        goal_scripts_qb=read_modified_script_qb("goal_scripts"),
        judges_qb=read_modified_script_qb("judges"),
        levels_qb=read_modified_script_qb("levels"),
        mainmenu_qb=read_modified_script_qb("mainmenu"),
        protricks_qb=read_modified_script_qb("protricks"),
        sk3_pedscripts_qb=read_modified_script_qb("sk3_pedscripts"),
        skater_profile_qb=read_modified_script_qb("skater_profile"),
    )


def write_modified_script_outfiles(script_qbs: ScriptQBs) -> None:
    write_modified_script_outfile("airtricks", script_qbs.airtricks_qb)
    write_modified_script_outfile("ajc_scripts", script_qbs.ajc_scripts_qb)
    write_modified_script_outfile("alf_scripts", script_qbs.alf_scripts_qb)
    write_modified_script_outfile("bdj_scripts", script_qbs.bdj_scripts_qb)
    write_modified_script_outfile("boardselect", script_qbs.boardselect_qb)
    write_modified_script_outfile("cjr_scripts", script_qbs.cjr_scripts_qb)
    write_modified_script_outfile("comp_scripts", script_qbs.comp_scripts_qb)
    write_modified_script_outfile("cpf_scripts", script_qbs.cpf_scripts_qb)
    write_modified_script_outfile("game", script_qbs.game_qb)
    write_modified_script_outfile("gameflow", script_qbs.gameflow_qb)
    write_modified_script_outfile("gamemode", script_qbs.gamemode_qb)
    write_modified_script_outfile("goal_scripts", script_qbs.goal_scripts_qb)
    write_modified_script_outfile("judges", script_qbs.judges_qb)
    write_modified_script_outfile("levels", script_qbs.levels_qb)
    write_modified_script_outfile("mainmenu", script_qbs.mainmenu_qb)
    write_modified_script_outfile("protricks", script_qbs.protricks_qb)
    write_modified_script_outfile("sk3_pedscripts", script_qbs.sk3_pedscripts_qb)
    write_modified_script_outfile("skater_profile", script_qbs.skater_profile_qb)


def get_level_order(shuffle: bool, end_on_comp: bool) -> list[Level2]:
    """
    Get the order of levels in career mode, which will apply to all skaters. If shuffle
    is False, the level order will be vanilla, and end_on_comp will be ignored. Else, if
    end_on_comp is True, the final career mode level will always be one of Rio, Skater
    Island, or Tokyo.
    """
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
    if not shuffle:
        return levels
    if not end_on_comp:
        return _shuffle(levels)
    else:
        comp_levels = _shuffle(
            [
                LevelRio(),
                LevelSkaterIsland(),
                LevelTokyo(),
            ]
        )
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


def display_victory_requirements(script_qbs: ScriptQBs):
    """
    Display victory requirements on the level select menu. The built-in display of level
    unlock requirements doesn't work in the randomizer. You have about 26 characters
    before the message grows beyond the UI.
    """
    script_qbs.game_qb = script_qbs.game_qb.replace(
        "{{rando_game_victory_text}}", "Thanks for playing rando!"
    )


def set_level_unlock_requirements(
    script_qbs: ScriptQBs,
    levels: list[Level2],
    minimum_unlock_goals: int,
    maximum_unlock_goals: int,
):
    """
    Set the number of goals and medals required to unlock each career mode level.
    Level order dictates which levels require goals and which require medals.
    minimum_unlock_goals is clamped to 0 or greater, though 0 is not recommended
    maximum_unlock_goals is clamped to 9 or fewer, as well as minimum or greater
    """
    if minimum_unlock_goals < 0:
        minimum_unlock_goals = 0
    if maximum_unlock_goals > 9:
        maximum_unlock_goals = 9
    if maximum_unlock_goals < minimum_unlock_goals:
        maximum_unlock_goals = minimum_unlock_goals
    level_reqs = [(0, "first")]
    total_goals = 0
    total_medals = 0

    for level in levels:
        match level.level_type:
            case "normal":
                # TODO: Add options to this value
                req = random.randint(minimum_unlock_goals, maximum_unlock_goals)
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

        if level_reqs[i][1] == "first":  # initial level
            script_qbs.mainmenu_qb = script_qbs.mainmenu_qb.replace(
                unlock_var, "0 Goals"
            )
        elif level_reqs[i][0] == 1:  # 1 goal or medal
            script_qbs.mainmenu_qb = script_qbs.mainmenu_qb.replace(
                unlock_var, f"{level_reqs[i][0]} {level_reqs[i][1]}"
            )
        else:  # More than 1 goal or medal
            script_qbs.mainmenu_qb = script_qbs.mainmenu_qb.replace(
                unlock_var, f"{level_reqs[i][0]} {level_reqs[i][1]}s"
            )

    # Unlock the first level instead of always unlocking Foundry
    script_qbs.mainmenu_qb = script_qbs.mainmenu_qb.replace(
        "{{rando_mainmenu_first_level_unlock}}", f"LEVEL_UNLOCKED_{levels[0].name_flag}"
    )

    for i in range(1, 9):
        script_qbs.goal_scripts_qb = script_qbs.goal_scripts_qb.replace(
            f"{{{{rando_goal_scripts_unlock_{i + 1}_requirement}}}}",
            f"{level_reqs[i][1]}sGreaterThan {level_reqs[i][0] - 1}",
        )
        script_qbs.goal_scripts_qb = script_qbs.goal_scripts_qb.replace(
            f"{{{{rando_goal_scripts_unlock_{i + 1}_flag}}}}",
            f"LEVEL_UNLOCKED_{levels[i].name_flag}",
        )
        script_qbs.goal_scripts_qb = script_qbs.goal_scripts_qb.replace(
            f"{{{{rando_goal_scripts_unlock_{i + 1}_name}}}}", levels[i].name
        )


def set_score_goals(
    script_qbs: ScriptQBs,
    levels: list[Level2],
    shuffle: bool,
    min_sick_score: int,
    max_sick_score: int,
    min_gold_score: int,
    max_gold_score: int,
):
    """
    Set the scores required for high/pro/sick score goals as well as competition medals.
    If shuffle is false, all scores will match vanilla (possibly in different levels if
    level order is shuffled), and the other parameters will be ignored.
    min_sick_score will be the sick score requirement on the first normal career level,
    max_sick_score will be the sick score on the last level, and all other scores will
    be calculated from those.
    Similarly, min_gold_score sets the (approximate) score required for a gold medal on
    the first comp level, max_gold_score sets the score required for a gold on the third,
    and the other medals will be calculated from there.
    Both minimum scores are clamped to 10 or greater
    Both maximum scores are clamped to 1000 or fewer, as well as minimum or greater
    See mod_notes for information on medal score calculation.
    """
    if not shuffle:
        score_goals = [
            10,
            30,
            60,
            35,
            70,
            120,
            55,
            110,
            200,
            75,
            150,
            300,
            100,
            190,
            400,
            150,
            225,
            500,
        ]
        medal_goals = [25, 70, 120, 45, 80, 150, 100, 150, 200]
    else:
        if min_sick_score < 10:
            min_sick_score = 10
        if min_gold_score < 10:
            min_gold_score = 10
        if max_sick_score < min_sick_score:
            max_sick_score = min_sick_score
        if max_gold_score < min_gold_score:
            max_gold_score = min_gold_score
        sick_score_gap = int((max_sick_score - min_sick_score) / 5)
        sick_scores = [
            min_sick_score,
            min_sick_score + 1 * sick_score_gap,
            min_sick_score + 2 * sick_score_gap,
            min_sick_score + 3 * sick_score_gap,
            min_sick_score + 4 * sick_score_gap,
            max_sick_score,
        ]
        score_goals = []
        for sick in sick_scores:
            score_goals.append(int(sick / 4))  # High score
            score_goals.append(int(sick / 2))  # Pro score
            score_goals.append(sick)  # Sick score
        gold_scores = [
            min_gold_score,
            int((min_gold_score + max_gold_score) / 2),
            max_gold_score,
        ]
        medal_goals = []
        for gold in gold_scores:
            medal_goals.append(int(gold / 4))  # Bronze medal
            medal_goals.append(int(gold / 2))  # Silver medal
            medal_goals.append(gold)  # Gold medal

    for level in levels:
        match level.name_flag:
            case "FOUNDRY":
                foundry_high = score_goals.pop(0)
                foundry_pro = score_goals.pop(0)
                foundry_sick = score_goals.pop(0)
                script_qbs.goal_scripts_qb = script_qbs.goal_scripts_qb.replace(
                    "{{rando_goal_scripts_foundry_high}}", f"{foundry_high}000"
                )
                script_qbs.goal_scripts_qb = script_qbs.goal_scripts_qb.replace(
                    "{{rando_goal_scripts_foundry_pro}}", f"{foundry_pro}000"
                )
                script_qbs.goal_scripts_qb = script_qbs.goal_scripts_qb.replace(
                    "{{rando_goal_scripts_foundry_sick}}", f"{foundry_sick}000"
                )
            case "CANADA":
                canada_high = score_goals.pop(0)
                canada_pro = score_goals.pop(0)
                canada_sick = score_goals.pop(0)
                script_qbs.goal_scripts_qb = script_qbs.goal_scripts_qb.replace(
                    "{{rando_goal_scripts_canada_high}}", f"{canada_high}000"
                )
                script_qbs.goal_scripts_qb = script_qbs.goal_scripts_qb.replace(
                    "{{rando_goal_scripts_canada_pro}}", f"{canada_pro}000"
                )
                script_qbs.goal_scripts_qb = script_qbs.goal_scripts_qb.replace(
                    "{{rando_goal_scripts_canada_sick}}", f"{canada_sick}000"
                )
            case "RIO":
                rio_bronze = medal_goals.pop(0)
                rio_silver = medal_goals.pop(0)
                rio_gold = medal_goals.pop(0)
                script_qbs.comp_scripts_qb = script_qbs.comp_scripts_qb.replace(
                    "{{rando_comp_scripts_rio_bronze}}", f"{rio_bronze}000"
                )
                script_qbs.comp_scripts_qb = script_qbs.comp_scripts_qb.replace(
                    "{{rando_comp_scripts_rio_silver}}", f"{rio_silver}000"
                )
                script_qbs.comp_scripts_qb = script_qbs.comp_scripts_qb.replace(
                    "{{rando_comp_scripts_rio_gold}}", f"{rio_gold}000"
                )
            case "SUBURBIA":
                suburbia_high = score_goals.pop(0)
                suburbia_pro = score_goals.pop(0)
                suburbia_sick = score_goals.pop(0)
                script_qbs.goal_scripts_qb = script_qbs.goal_scripts_qb.replace(
                    "{{rando_goal_scripts_suburbia_high}}", f"{suburbia_high}000"
                )
                script_qbs.goal_scripts_qb = script_qbs.goal_scripts_qb.replace(
                    "{{rando_goal_scripts_suburbia_pro}}", f"{suburbia_pro}000"
                )
                script_qbs.goal_scripts_qb = script_qbs.goal_scripts_qb.replace(
                    "{{rando_goal_scripts_suburbia_sick}}", f"{suburbia_sick}000"
                )
            case "AIRPORT":
                airport_high = score_goals.pop(0)
                airport_pro = score_goals.pop(0)
                airport_sick = score_goals.pop(0)
                script_qbs.goal_scripts_qb = script_qbs.goal_scripts_qb.replace(
                    "{{rando_goal_scripts_airport_high}}", f"{airport_high}000"
                )
                script_qbs.goal_scripts_qb = script_qbs.goal_scripts_qb.replace(
                    "{{rando_goal_scripts_airport_pro}}", f"{airport_pro}000"
                )
                script_qbs.goal_scripts_qb = script_qbs.goal_scripts_qb.replace(
                    "{{rando_goal_scripts_airport_sick}}", f"{airport_sick}000"
                )
            case "SKATERISLAND":
                skater_island_bronze = medal_goals.pop(0)
                skater_island_silver = medal_goals.pop(0)
                skater_island_gold = medal_goals.pop(0)
                script_qbs.comp_scripts_qb = script_qbs.comp_scripts_qb.replace(
                    "{{rando_comp_scripts_si_bronze}}", f"{skater_island_bronze}000"
                )
                script_qbs.comp_scripts_qb = script_qbs.comp_scripts_qb.replace(
                    "{{rando_comp_scripts_si_silver}}", f"{skater_island_silver}000"
                )
                script_qbs.comp_scripts_qb = script_qbs.comp_scripts_qb.replace(
                    "{{rando_comp_scripts_si_gold}}", f"{skater_island_gold}000"
                )
            case "LOSANGELES":
                los_angeles_high = score_goals.pop(0)
                los_angeles_pro = score_goals.pop(0)
                los_angeles_sick = score_goals.pop(0)
                script_qbs.goal_scripts_qb = script_qbs.goal_scripts_qb.replace(
                    "{{rando_goal_scripts_la_high}}", f"{los_angeles_high}000"
                )
                script_qbs.goal_scripts_qb = script_qbs.goal_scripts_qb.replace(
                    "{{rando_goal_scripts_la_pro}}", f"{los_angeles_pro}000"
                )
                script_qbs.goal_scripts_qb = script_qbs.goal_scripts_qb.replace(
                    "{{rando_goal_scripts_la_sick}}", f"{los_angeles_sick}000"
                )
            case "TOKYO":
                tokyo_bronze = medal_goals.pop(0)
                tokyo_silver = medal_goals.pop(0)
                tokyo_gold = medal_goals.pop(0)
                script_qbs.comp_scripts_qb = script_qbs.comp_scripts_qb.replace(
                    "{{rando_comp_scripts_tokyo_bronze}}", f"{tokyo_bronze}000"
                )
                script_qbs.comp_scripts_qb = script_qbs.comp_scripts_qb.replace(
                    "{{rando_comp_scripts_tokyo_silver}}", f"{tokyo_silver}000"
                )
                script_qbs.comp_scripts_qb = script_qbs.comp_scripts_qb.replace(
                    "{{rando_comp_scripts_tokyo_gold}}", f"{tokyo_gold}000"
                )
            case "SHIP":
                cruise_ship_high = score_goals.pop(0)
                cruise_ship_pro = score_goals.pop(0)
                cruise_ship_sick = score_goals.pop(0)
                script_qbs.goal_scripts_qb = script_qbs.goal_scripts_qb.replace(
                    "{{rando_goal_scripts_ship_high}}", f"{cruise_ship_high}000"
                )
                script_qbs.goal_scripts_qb = script_qbs.goal_scripts_qb.replace(
                    "{{rando_goal_scripts_ship_pro}}", f"{cruise_ship_pro}000"
                )
                script_qbs.goal_scripts_qb = script_qbs.goal_scripts_qb.replace(
                    "{{rando_goal_scripts_ship_sick}}", f"{cruise_ship_sick}000"
                )
            case _:
                raise Exception("invalid level")


def set_starting_stats(script_qbs: ScriptQBs, stat_default: int):
    """
    Set the starting level for all stats on characters (on a new save file). Stats can
    still be redistributed at any time.
    stat_default is clamped between 0 and 10.
    If stat_default is less than 5, you will not be able to reach maximum stats with
    any character.
    """
    if stat_default < 0:
        stat_default = 0
    elif stat_default > 10:
        stat_default = 10
    script_qbs.skater_profile_qb = script_qbs.skater_profile_qb.replace(
        "{{rando_skater_profile_global_stat}}", str(stat_default)
    )


def set_deck_required_for_tape(script_qbs: ScriptQBs, require_deck_for_tape: bool):
    """
    If require_deck_for_tape is True, collecting the secret tape before collecting the
    secret deck will show a message and not mark the goal as complete. If you collect
    the deck after collecting the tape in a run, you will have to retry the run for
    the tape to appear again.
    """
    if require_deck_for_tape:
        # Got_Secret_TapeIfDeck is a custom function added to the modified QB
        script_qbs.goal_scripts_qb = script_qbs.goal_scripts_qb.replace(
            "{{rando_goal_scripts_tape_script}}", "Got_Secret_TapeIfDeck"
        )
    else:
        # Got_Secret_Tape2 is the default with no additional requirements
        script_qbs.goal_scripts_qb = script_qbs.goal_scripts_qb.replace(
            "{{rando_goal_scripts_tape_script}}", "Got_Secret_Tape2"
        )


def set_deck_required_for_medal(script_qbs: ScriptQBs, require_deck_for_medal: bool):
    """
    If require_deck_for_medal is True, achieving the score threshold for a medal before
    collecting the secret deck will show a message and prevent you from earning a medal.
    """
    flag_medal_req = "{{rando_judges_medal_requirement}}"
    comp_scripts_medal_req = "{{rando_comp_scripts_medal_requirement}}"
    medal_message = "{{rando_comp_scripts_medal_message}}"
    if require_deck_for_medal:
        script_qbs.judges_qb = script_qbs.judges_qb.replace(
            flag_medal_req, "GetFlag flag = GOAL_DECK"
        )
        script_qbs.comp_scripts_qb = script_qbs.comp_scripts_qb.replace(
            medal_message, "Must Find Deck To Medal"
        )
        script_qbs.comp_scripts_qb = script_qbs.comp_scripts_qb.replace(
            comp_scripts_medal_req, "GetFlag flag = GOAL_DECK"
        )
    else:
        # GetGlobalFlag flag = 159 is always True, because the randomizer sets
        # SPECIAL_HAS_SEEN_SHIP to True upon loading mainmenu.qb
        script_qbs.judges_qb = script_qbs.judges_qb.replace(
            flag_medal_req, "GetGlobalFlag flag = 159"
        )
        script_qbs.comp_scripts_qb = script_qbs.comp_scripts_qb.replace(
            medal_message, "Bails Hurt Scores"
        )
        script_qbs.comp_scripts_qb = script_qbs.comp_scripts_qb.replace(
            comp_scripts_medal_req, "GetGlobalFlag flag = 159"
        )


def randomize(
    level_order_shuffle: bool,
    level_order_end_on_comp: bool,
    minimum_unlock_goals: int,
    maximum_unlock_goals: int,
    score_shuffle: bool,
    min_sick_score: int,
    max_sick_score: int,
    min_gold_score: int,
    max_gold_score: int,
    stat_default: int,
    require_deck_for_tape: bool,
    require_deck_for_medal: bool,
):
    script_qbs = read_modified_script_qbs()
    levels = get_level_order(
        shuffle=level_order_shuffle, end_on_comp=level_order_end_on_comp
    )
    display_victory_requirements(script_qbs)
    set_level_unlock_requirements(
        script_qbs, levels, minimum_unlock_goals, maximum_unlock_goals
    )
    set_score_goals(
        script_qbs,
        levels,
        score_shuffle,
        min_sick_score,
        max_sick_score,
        min_gold_score,
        max_gold_score,
    )
    set_starting_stats(script_qbs, stat_default)
    set_deck_required_for_tape(script_qbs, require_deck_for_tape)
    set_deck_required_for_medal(script_qbs, require_deck_for_medal)

    # TODO: Replace method calls below this comment with new versions
    rando2.randomize_item_locations(levels)
    script_qbs.skater_profile_qb = rando2.randomize_trickstyle(
        script_qbs.skater_profile_qb
    )
    script_qbs.gamemode_qb = rando2.randomize_level_timer(script_qbs.gamemode_qb)
    (
        trickspot_tricks,
        script_qbs.ajc_scripts_qb,
        script_qbs.alf_scripts_qb,
        script_qbs.bdj_scripts_qb,
        script_qbs.cjr_scripts_qb,
        script_qbs.cpf_scripts_qb,
    ) = rando2.randomize_trickspot_tricks(
        "wild",
        script_qbs.ajc_scripts_qb,
        script_qbs.alf_scripts_qb,
        script_qbs.bdj_scripts_qb,
        script_qbs.cjr_scripts_qb,
        script_qbs.cpf_scripts_qb,
    )
    script_qbs.protricks_qb = rando2.randomize_trick_sets(
        script_qbs.protricks_qb, trickspot_tricks
    )
    script_qbs.skater_profile_qb = rando2.randomize_special_tricks(
        script_qbs.skater_profile_qb, "easy"
    )
    (
        script_qbs.ajc_scripts_qb,
        script_qbs.bdj_scripts_qb,
        script_qbs.sk3_pedscripts_qb,
    ) = rando2.randomize_impress_ped_scores(
        script_qbs.ajc_scripts_qb,
        script_qbs.bdj_scripts_qb,
        script_qbs.sk3_pedscripts_qb,
    )
    script_qbs.boardselect_qb = rando2.randomize_decks(script_qbs.boardselect_qb)
    script_qbs.airtricks_qb = rando2.unlock_trick_scores(
        script_qbs.airtricks_qb, levels
    )
    script_qbs.goal_scripts_qb = rando2.randomize_secrets(script_qbs.goal_scripts_qb)
    script_qbs.skater_profile_qb = rando2.lock_characters(script_qbs.skater_profile_qb)
    script_qbs.alf_scripts_qb = rando2.junk_suburbia(script_qbs.alf_scripts_qb)
    script_qbs.cjr_scripts_qb = rando2.randomize_foundry_trickspot_gaps(
        script_qbs.cjr_scripts_qb
    )

    write_modified_script_outfiles(script_qbs)
