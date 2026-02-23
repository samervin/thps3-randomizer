class Skater:
    name = None  # Name of skater
    script_name = None  # Shorthand name as defined in skater_profile
    is_secret = False  # Whether the character is a vanilla secret

    def __init__(self, name, script_name, is_secret):
        self.name = name
        self.script_name = script_name
        self.is_secret = is_secret


class Skaters:
    all_skaters = [
        Skater("Tony Hawk", "hawk", False),
        Skater("Steve Caballero", "caballero", False),
        Skater("Kareem Campbell", "campbell", False),
        Skater("Rune Glifberg", "glifberg", False),
        Skater("Eric Koston", "koston", False),
        Skater("Bucky Lasek", "lasek", False),
        Skater("Bam Margera", "margera", False),
        Skater("Rodney Mullen", "mullen", False),
        Skater("Chad Muska", "muska", False),
        Skater("Andrew Reynolds", "reynolds", False),
        Skater("Geoff Rowley", "rowley", False),
        Skater("Elissa Steamer", "steamer", False),
        Skater("Jamie Thomas", "thomas", False),
        Skater("Darth Maul", "maul", True),
        Skater("Wolverine", "wolverine", True),
        Skater("Officer Dick", "dick", True),
        Skater("Private Carrera", "carrera", True),
        Skater("Ollie the Magic Bum", "ollie", True),
        Skater("Kelly Slater", "slater", True),
        Skater("Demoness", "demoness", True),
        Skater("Neversoft Eyeball", "eyeball", True),
        Skater("DOOM Guy", "doomguy", True),
        Skater("Custom Skater", "custom", False),
    ]
