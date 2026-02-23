class Secret:
    name = None # Name of skater, level, or cheat
    secret_type = None # "skater", "level", or "cheat"

    def __init__(self, name, secret_type):
        self.name = name
        self.secret_type = secret_type

class Secrets:

    def get_secrets(self, secret_type=None):
        if secret_type:
            return [s for s in self.all_secrets if s.secret_type == secret_type]
        return self.all_secrets.copy()

    all_secrets = [
        Secret("Darth Maul", "skater"),
        Secret("Wolverine", "skater"),
        Secret("Warehouse", "level"),
        Secret("Officer Dick", "skater"),
        Secret("Private Carrera", "skater"),
        Secret("Burnside", "level"),
        Secret("Ollie the Bum", "skater"),
        Secret("Kelly Slater", "skater"),
        Secret("Roswell", "level"),
        Secret("The Demoness", "skater"),
        Secret("Snowboard Mode", "cheat"), # currently tied to Cheat menu being unlocked
        Secret("Always Special Mode", "cheat"),
        Secret("Perfect Rail Balance Mode", "cheat"),
        Secret("Super Stats Mode", "cheat"),
        Secret("Giant Mode", "cheat"),
        Secret("Slowmo Mode", "cheat"),
        Secret("Perfect Manual Balance Mode", "cheat"),
        Secret("Tiny Mode", "cheat"),
        Secret("Moon Physics Mode", "cheat"),
        Secret("Expert Mode", "cheat"),
        Secret("Neversoft Eyeball", "skater"),
        Secret("First Person Mode", "cheat"), # currently contains "Entire Game Complete" check
        Secret("DOOM Guy", "skater"),
    ]

    secret_flags = [
        "SKATER_UNLOCKED_MAUL",
        "SKATER_UNLOCKED_WOLVERINE",
        "LEVEL_UNLOCKED_WAREHOUSE",
        "SKATER_UNLOCKED_DICK",
        "SKATER_UNLOCKED_CARRERA",
        "LEVEL_UNLOCKED_BURNSIDE",
        "SKATER_UNLOCKED_BUM",
        "SKATER_UNLOCKED_SLATER",
        "LEVEL_UNLOCKED_ROSWELL",
        "SKATER_UNLOCKED_DEMONESS",
        "CHEAT_UNLOCKED_1",
        "CHEAT_UNLOCKED_2",
        "CHEAT_UNLOCKED_3",
        "CHEAT_UNLOCKED_4",
        "CHEAT_UNLOCKED_5",
        "CHEAT_UNLOCKED_6",
        "CHEAT_UNLOCKED_7",
        "CHEAT_UNLOCKED_8",
        "CHEAT_UNLOCKED_9",
        "CHEAT_UNLOCKED_10",
        "SKATER_UNLOCKED_EYEBALL",
        "CHEAT_UNLOCKED_11",
        "SKATER_UNLOCKED_DOOMGUY",
    ]

    secret_flags_levels = [
        "LEVEL_UNLOCKED_WAREHOUSE",
        "LEVEL_UNLOCKED_BURNSIDE",
        "LEVEL_UNLOCKED_ROSWELL",
    ]

    secret_flags_cheats = [
        "CHEAT_UNLOCKED_1",
        "CHEAT_UNLOCKED_2",
        "CHEAT_UNLOCKED_3",
        "CHEAT_UNLOCKED_4",
        "CHEAT_UNLOCKED_5",
        "CHEAT_UNLOCKED_6",
        "CHEAT_UNLOCKED_7",
        "CHEAT_UNLOCKED_8",
        "CHEAT_UNLOCKED_9",
        "CHEAT_UNLOCKED_10",
        # "CHEAT_UNLOCKED_11", # TODO: This is first-person mode, but we don't want to shuffle it in
    ]
