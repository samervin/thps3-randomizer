class Trick:
    name = None # Displayed in trick string
    name_script = None # Internal script name
    name_goal = None # Descriptive name used for trickspot goals
    trick_type = None # grind, grab, flip, lip, manual
    is_special = False # true for special tricks
    is_extra = False # true for weird tricks like character-specific or secret flip combos

    def __init__(
        self, name, name_script, name_goal,
        trick_type, is_special=False, is_extra=False
    ):
        self.name = name
        self.name_script = name_script
        self.name_goal = name_goal
        self.trick_type = trick_type
        self.is_special = is_special
        self.is_extra = is_extra

class Tricks:

    def _get_regular_tricks_by_type(self, by_trick_type):
        return [t for t in self.all_tricks if t.trick_type == by_trick_type and t.is_special is False and t.is_extra is False]

    def get_regular_grinds(self):
        return self._get_regular_tricks_by_type("grind")

    def get_regular_grabs(self):
        return self._get_regular_tricks_by_type("grab")

    def get_regular_flips(self):
        return self._get_regular_tricks_by_type("flip")

    def get_regular_lips(self):
        return self._get_regular_tricks_by_type("lip")

    def get_all_special_tricks(self):
        return [t for t in self.all_tricks if t.is_special is True and t.is_extra is False]

    all_tricks = [ # TODO: Not actually all tricks yet!
        # Regular grinds (Grinds cannot normally be rebound and have FS/BS variations, so ignore script name)
        Trick("5-0", None, "5-0 Grind", "grind"),
        Trick("50-50", None, "50-50 Grind", "grind"),
        Trick("Bluntslide", None, "Bluntslide Grind", "grind"),
        Trick("Boardslide", None, "Boardslide Grind", "grind"),
        Trick("Crooked", None, "Crooked Grind", "grind"),
        Trick("Feeble", None, "Feeble Grind", "grind"),
        Trick("Lipslide", None, "Lipslide Grind", "grind"),
        Trick("Nosebluntslide", None, "Nosebluntslide Grind", "grind"),
        Trick("Nosegrind", None, "Nosegrind Grind", "grind"),
        Trick("Noseslide", None, "Noseslide Grind", "grind"),
        Trick("Overcrook", None, "Overcrook Grind", "grind"),
        Trick("Smith", None, "Smith Grind", "grind"),
        Trick("Tailslide", None, "Tailslide Grind", "grind"),
        # Special grinds
        Trick("5-0 Overturn", "Trick_GrindOverturn", "5-0 Overturn Grind", "grind", is_special=True),
        Trick("Big Hitter II", "Trick_BigHitter", "Big Hitter II Grind", "grind", is_special=True),
        Trick("Coffin", "Trick_Coffin", "Coffin Grind", "grind", is_special=True),
        Trick("Crail Slide", "Trick_CrailSlide", "Crail Slide Grind", "grind", is_special=True),
        Trick("BigSpin", "Trick_CrookedBigSpin", "Crook BigSpin Crook Grind", "grind", is_special=True),
        Trick("Darkslide", "Trick_DarkSlide", "Darkslide Grind", "grind", is_special=True),
        Trick("Fandangle", "Trick_Fandangle", "Fandangle Grind", "grind", is_special=True),
        Trick("Handstand 50-50", "Trick_Handstand5050", "Handstand 50-50 Grind", "grind", is_special=True),
        Trick("Hang Ten Nosegrind", "Trick_HangTenNoseGrind", "Hang Ten Nosegrind", "grind", is_special=True),
        Trick("Human Dart", "Trick_HumanDart", "Human Dart Grind", "grind", is_special=True),
        Trick("Hurricane", "Trick_Hurricane", "Hurricane Grind", "grind", is_special=True),
        Trick("Layback", "Trick_FeebleLayback", "Layback Sparks Grind", "grind", is_special=True),
        Trick("Nosegrind to Pivot", "Trick_NosegrindPivot", "Nosegrind to Pivot", "grind", is_special=True),
        Trick("Noseslide Lipslide", "Trick_NoseSlideLipSlide", "Noseslide Lipslide Grind", "grind", is_special=True),
        Trick("Rowley Darkslide", "Trick_RowleyDarkSlide", "Rowley Darkslide Grind", "grind", is_special=True),
        Trick("Salad Grind", "Trick_Salad", "Salad Grind", "grind", is_special=True),
        Trick("Tailblock Slide", "Trick_TailblockSlide", "Tailblock Slide Grind", "grind", is_special=True),
        # Regular grabs
        Trick("Airwalk", "Trick_Airwalk", "Airwalk Grab", "grab"),
        Trick("Benihana", "Trick_Benihana", "Benihana Grab", "grab"),
        Trick("Cannonball", "Trick_Cannonball", "Cannonball Grab", "grab"),
        Trick("Crail Grab", "Trick_Crail", "Crail Grab", "grab"),
        Trick("CrookedCop", "Trick_CrookedCop", "CrookedCop Grab", "grab"),
        Trick("Crossbone", "Trick_Crossbone", "Crossbone Grab", "grab"),
        Trick("Del Mar Indy", "Trick_DelMarIndy", "Del Mar Indy Grab", "grab"),
        Trick("FS Shifty", "Trick_FSShifty", "FS Shifty Grab", "grab"),
        Trick("Indy", "Trick_Indy", "Indy Grab", "grab"),
        Trick("Indy Nosebone", "Trick_IndyNosebone", "Indy Nosebone Grab", "grab"),
        Trick("Japan", "Trick_Japan", "Japan Grab", "grab"),
        Trick("Judo", "Trick_Judo", "Judo Grab", "grab"),
        Trick("Madonna", "Trick_Madonna", "Madonna Grab", "grab"),
        Trick("Melon", "Trick_Melon", "Melon Grab", "grab"),
        Trick("Method", "Trick_Method", "Method Grab", "grab"),
        Trick("Mute", "Trick_Mute", "Mute Grab", "grab"),
        Trick("Nosegrab", "Trick_Nosegrab", "Nosegrab", "grab"),
        Trick("One Foot Japan", "Trick_OneFootJapan", "One Foot Japan Grab", "grab"),
        Trick("RoastBeef", "Trick_Roastbeef", "Roast Beef Grab", "grab"),
        Trick("Rocket Air", "Trick_Rocket", "Rocket Air Grab", "grab"),
        Trick("Seatbelt Air", "Trick_Seatbelt", "Seatbelt Air Grab", "grab"),
        Trick("Stalefish", "Trick_Stalefish", "Stalefish Grab", "grab"),
        Trick("Stiffy", "Trick_Stiffy", "Stiffy Grab", "grab"),
        Trick("Tailgrab", "Trick_Tailgrab", "Tailgrab", "grab"),
        Trick("TuckKnee", "Trick_TuckKnee", "Tuck Knee Grab", "grab"),
        Trick("Wrap Around", "Trick_SaranWrap", "Wrap Around Grab", "grab"),
        # Special grabs (some of these look like flips, but you can tweak them)
        Trick("Casper Flip 360 Flip", "Trick_AirCasperFlip", "Casper Flip 360 Flip", "grab", is_special=True),
        Trick("Christ Air", "Trick_ChristAir", "Christ Air", "grab", is_special=True),
        Trick("Double Kickflip Madonna", "Trick_2KickMadonnaFlip", "Double Kickflip Madonna", "grab", is_special=True),
        Trick("Judo Madonna", "Trick_JudoMadonna", "Judo Madonna", "grab", is_special=True),
        Trick("Kickflip One Foot Tail", "Trick_KickFlipOneFootTail", "Kickflip One Foot Tail", "grab", is_special=True),
        Trick("Kickflip Superman", "Trick_KFSuperman", "Kickflip Superman", "grab", is_special=True),
        Trick("Pizza Guy", "Trick_PizzaGuy", "Pizza Guy", "grab", is_special=True),
        Trick("Sacktap", "Trick_SackTap", "Sacktap", "grab", is_special=True),
        # Regular flips
        Trick("180 Varial", "Trick_180Varial", "180 Varial Flip", "flip"),
        Trick("360 Flip", "Trick_360Flip", "360 Flip", "flip"),
        Trick("360 Varial", "Trick_360Varial", "360 Varial Flip", "flip"),
        Trick("Fingerflip", "Trick_Fingerflip", "Fingerflip", "flip"),
        Trick("Front Foot Impossible", "Trick_FFImpossible", "Front Foot Impossible Flip", "flip"),
        Trick("FS Shove-It", "Trick_FSShoveIt", "FS Shove-It Flip", "flip"), # TODO: 360/540 fs shove-it
        Trick("Hardflip", "Trick_Hardflip", "Hardflip", "flip"),
        Trick("Heelflip Varial Lien", "Trick_HFVarialLien", "Heelflip Varial Lien", "flip"),
        Trick("Heelflip", "Trick_Heelflip", "Heelflip", "flip"), # TODO: double/triple heelflip
        Trick("Impossible", "Trick_Impossible", "Impossible Flip", "flip"), # TODO: double/triple impossible
        Trick("Inward Heelflip", "Trick_InwardHeelflip", "Inward Heelflip", "flip"),
        Trick("Kickflip", "Trick_Kickflip", "Kickflip", "flip"), # TODO: double/triple kickflip
        Trick("Ollie Airwalk", "Trick_OllieAirwalk", "Ollie Airwalk Flip", "flip"),
        Trick("Ollie North", "Trick_OllieNorth", "Ollie North Flip", "flip"),
        Trick("Pop Shove-It", "Trick_PopShoveIt", "Pop Shove-It Flip", "flip"), # TODO: 360/540 shove-it
        Trick("Sal Flip", "Trick_SalFlip", "Sal Flip", "flip"),
        Trick("Varial", "Trick_Varial", "Varial Flip", "flip"),
        Trick("Varial Heelflip", "Trick_VarialKickflip", "Varial Heelflip", "flip"),
        Trick("Varial Kickflip", "Trick_VarialKickflip", "Varial Kickflip", "flip"),
        # Special flips (some of these aren't "flips" but unlike grabs, you can't tweak these)
        Trick("1-2-3-4", "Trick_1234", "1-2-3-4", "flip", is_special=True),
        Trick("360 Hardflip", "Trick_360Hardflip", "360 HardFlip", "flip", is_special=True),
        Trick("540 Flip", "Trick_540Flip", "540 Flip", "flip", is_special=True),
        Trick("540 Tailwhip", "Trick_540TailWhip", "540 Tailwhip", "flip", is_special=True),
        Trick("Double Kickflip Indy", "Trick_DoubleKFindy", "Double Kickflip Indy", "flip", is_special=True),
        Trick("Fingerflip Airwalk", "Trick_FingerFlipAirWalk", "Fingerflip Airwalk", "flip", is_special=True),
        Trick("FS 540", "Trick_FS540", "Special FS 540", "flip", is_special=True),
        Trick("FS 540 Heelflip", "Trick_FS540HeelFlip", "Special FS 540 Heelflip", "flip", is_special=True),
        Trick("Gazelle Underflip", "Trick_Gazelle", "Gazelle Underflip", "flip", is_special=True),
        Trick("Ghetto Bird", "Trick_GhettoBird", "Ghetto Bird Flip", "flip", is_special=True),
        Trick("Hardflip Late Flip", "Trick_HardFlipBackFootFlip", "Hardflip Late Flip", "flip", is_special=True),
        Trick("Kickflip Backflip", "Trick_KFBackflip", "Kickflip Backflip", "flip", is_special=True),
        Trick("Kickflip Underflip", "Trick_KickFlipUnderFlip", "Kickflip Underflip", "flip", is_special=True),
        Trick("Laser Flip", "Trick_LaserFlip", "Laser Flip", "flip", is_special=True),
        Trick("McTwist", "Trick_McTwist", "McTwist", "flip", is_special=True),
        Trick("Misty Flip", "Trick_MistyFlip", "Misty Flip", "flip", is_special=True),
        Trick("Nollie Flip Underflip", "Trick_NollieFlipUnderflip", "Nollie Flip Underflip", "flip", is_special=True),
        Trick("Quad Heelflip", "Trick_QuadrupleHeelFlip", "Quad Heelflip", "flip", is_special=True),
        Trick("Slamma Jamma", "Trick_BetweenLegsSlam", "Slamma Jamma", "flip", is_special=True),
        Trick("Stalefish Backflip", "Trick_StaleBackFlip", "Stalefish Backflip", "flip", is_special=True),
        Trick("Stalefish Frontflip", "Trick_StaleFrontFlip", "Stalefish Frontflip", "flip", is_special=True),
        Trick("The 900", "Trick_The900", "Special 900", "flip", is_special=True),
        Trick("The Jackass", "Trick_Jackass", "Jackass", "flip", is_special=True),
        # Regular lips
        Trick("Nose Stall", None, "Nose Stall Lip", "lip", is_special=False, is_extra=True), # Default lip trick, cannot normally be rebound
        Trick("Andrecht Invert", "Trick_AndrectInvert", "Andrect Invert Lip", "lip"),
        Trick("Axle Stall", "Trick_AxleStall", "Axle Stall Lip", "lip"),
        Trick("Blunt to Fakie", "Trick_Blunt", "Blunt to Fakie Lip", "lip"),
        Trick("BS Boneless", "Trick_BSFootplant", "BS Boneless Lip", "lip"),
        Trick("Disaster", "Trick_Disaster", "Disaster Lip", "lip"),
        Trick("Eggplant", "Trick_Eggplant", "Eggplant Lip", "lip"),
        Trick("FS Noseblunt", "Trick_Noseblunt", "FS Noseblunt Lip", "lip"),
        Trick("FS Nosepick", "Trick_Nosepick", "FS Nosepick Lip", "lip"),
        Trick("Gymnast Plant", "Trick_GymnastPlant", "Gymnast Plant Lip", "lip"),
        Trick("Invert", "Trick_MuteInvert", "Invert Lip", "lip"),
        Trick("One Foot Invert", "Trick_OneFootInvert", "One Foot Invert Lip", "lip"),
        Trick("Rock to Fakie", "Trick_RockToFakie", "Rock to Fakie Lip", "lip"),
        Trick("The Switcheroo", "Trick_Switcheroo", "Switcheroo Lip", "lip"),
        Trick("Varial Invert to Fakie", "Trick_Invert", "Varial Invert to Fakie Lip", "lip"),
        # Special lips
        Trick("Bigspin Flip to Tail", "Trick_BigSpinFliptoTail", "Bigspin Flip to Tail Lip", "lip", is_special=True),
        Trick("Dark Disaster", "Trick_DarkDisaster", "Dark Disaster Lip", "lip", is_special=True),
        Trick("BS Nose Comply", "Trick_BSNoseComply", "BS Nose Comply Lip", "lip", is_special=True),
        Trick("One Foot Blunt", "Trick_OneFootBlunt", "One Foot Blunt Lip", "lip", is_special=True),
        Trick("Russian Boneless", "Trick_Russian", "Russian Boneless Lip", "lip", is_special=True),
        Trick("The H Teeth Sweeper", "Trick_HTeethSweeper", "H Teeth Sweeper Lip", "lip", is_special=True),
        # Special manuals
        Trick("Anti Casper", "Trick_AntiCasper", "Anti Casper Manual", "manual", is_special=True),
        Trick("Casper", "Trick_Casper", "Casper Manual", "manual", is_special=True),
        Trick("Handstand", "Trick_Handstand", "Handstand Manual", "manual", is_special=True),
        Trick("Handstand 360 Hand Flip", "Trick_HandStand50Flip", "Handstand 360 Hand Flip Manual", "manual", is_special=True),
        Trick("Handstand Double Flip", "Trick_HandstandDoubleFlip", "Handstand Double Flip Manual", "manual", is_special=True),
        Trick("One Wheel Nosemanual", "Trick_OneFootOneWheel", "One Wheel Nosemanual", "manual", is_special=True),
        Trick("Primo", "Trick_PrimoSlide", "Primo Manual", "manual", is_special=True),
        Trick("Reemo Slide", "Trick_ReemoSlide", "Reemo Slide Manual", "manual", is_special=True),
        Trick("Sproing", "Trick_Sproing", "Sproing Manual", "manual", is_special=True),
        Trick("Truckstand", "Trick_Truckstand", "Truckstand Manual", "manual", is_special=True),
        Trick("ZZZZ Manual", "Trick_ZZZZManual", "ZZZZ Manual", "manual", is_special=True),
    ]
