# coding: cp1252
import os
import re
from dataclasses import dataclass

import rando2


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


def randomize():
    script_qbs = read_modified_script_qbs()

    # TODO: Yep, this is really messy. We'll pass around script_qbs directly soon.
    levels = rando2.get_random_level_order(end_on_comp=True)
    script_qbs.game_qb = rando2.display_victory_requirements(script_qbs.game_qb)
    script_qbs.goal_scripts_qb, script_qbs.mainmenu_qb = (
        rando2.randomize_level_requirements(
            levels, script_qbs.mainmenu_qb, script_qbs.goal_scripts_qb
        )
    )
    script_qbs.comp_scripts_qb, script_qbs.goal_scripts_qb = (
        rando2.randomize_score_goals(
            levels, script_qbs.goal_scripts_qb, script_qbs.comp_scripts_qb
        )
    )
    rando2.randomize_item_locations(levels)
    script_qbs.skater_profile_qb = rando2.randomize_stats(script_qbs.skater_profile_qb)
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
    script_qbs.goal_scripts_qb = rando2.require_deck_for_tape(
        script_qbs.goal_scripts_qb
    )
    script_qbs.judges_qb, script_qbs.comp_scripts_qb = rando2.require_deck_for_medal(
        script_qbs.judges_qb, script_qbs.comp_scripts_qb
    )
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
