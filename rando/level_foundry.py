from level import Level

class LevelFoundry(Level):

    def __init__(self):
        self.name = "The Foundry"
        self.name_flag = "FOUNDRY"
        self.level_type = "normal"
        self.filename = "Foun/foun"
        self.location_vectors = [
            'VECTOR[-4060.664; 429.0006; -243.57791]', # Secret tape
            'VECTOR[-5110.666; 113.99924; -824.4385]',
            'VECTOR[-4060.6682; 262.62546; 1516.309]',
            'VECTOR[-3402.1516; 347.9992; -4572.282]',
            'VECTOR[-5082.1665; -108.00067; -1424.4391]', # SKATE 1
            'VECTOR[-4390.6626; -84.000656; -3254.9324]',
            'VECTOR[-3694.6687; -199.70175; -824.43866]',
            'VECTOR[-3209.5544; -6.1E-4; 1556.6754]',
            'VECTOR[-5082.167; -108.00067; -224.438]',
            'VECTOR[-3291.425; -23.999695; -1053.1389]', # SKATE 2
            'VECTOR[-3745.669; -84.000656; -3254.934]',
            'VECTOR[-4464.17; -132.00072; -824.43866]',
            'VECTOR[-4911.7803; -6.56E-4; 1556.6754]',
            'VECTOR[-3622.668; -47.999207; 397.28503]',
            'VECTOR[-4060.6677; -138.0014; -2425.1675]', # SKATE 3
            'VECTOR[-3754.669; -148.70175; -824.43866]',
            'VECTOR[-4060.6675; 12.000687; 517.28534]',
            'VECTOR[-4992.166; -144.00076; -824.43665]',
            'VECTOR[-4719.1885; 347.99927; -4572.2817]',
            'VECTOR[-3028.8079; 300.08707; -2591.8809]', # Stats 1
            'VECTOR[-4419.17; -252.00082; -824.4385]',
            'VECTOR[-4339.6685; 12.000793; 1515.5597]',
            'VECTOR[-4675.668; -18.001404; -2545.1685]',
            'VECTOR[-3460.669; 624.0007; -213.57718]',
            'VECTOR[-3445.669; -18.001404; -2027.6837]', # Stats 2
            'VECTOR[-4228.669; 35.9993; -824.43854]',
            'VECTOR[-3291.4253; 36.000305; -595.7379]',
            'VECTOR[-3292.6711; 395.99933; 1739.0812]',
            'VECTOR[-4060.67; 347.99924; -4375.2197]',
            'VECTOR[-5035.769; 300.0683; -2782.4988]', # Stats 3
            'VECTOR[-4060.6665; 383.99933; -1332.9507]',
            'VECTOR[-4498.6675; -47.999268; 517.28503]',
            'VECTOR[-3690.671; 0.001434; 1755.5587]',
            'VECTOR[-3460.667; -84.000656; -3254.9343]',
            'VECTOR[-4208.282; 120.0615; -2546.658]', # Stats 4
            'VECTOR[-4060.6655; -234.00067; -824.4388]',
            'VECTOR[-4828.665; 395.99933; 1739.0817]',
            'VECTOR[-3110.0479; -34.50052; -764.43774]',
            'VECTOR[-4060.669; -18.001404; -2027.6853]',
        ]
        # -X = left of spawn
        # +X = right of spawn
        # -Y = lower to ground
        # +Y = higher above ground
        # -Z = closer to spawn
        # +Z = farther from spawn
        self.extra_vectors = [
            'VECTOR[-4060.664; 197.99927; -5012.2817]', # secret room entrance
            'VECTOR[-3560.664; 897.99927; -5512.2817]', # secret room, top of spiral
        ]
        self.gaps = [
            "Back End Rail 2 Rail",
            "Bucket o' Hot Sauce",
            "Catwalk Balancing Act",
            "Catwalk Grind",
            "Catwalk Tight Lip",
            "CG's SKDK 2 STFK",
            "Circus Act Around The Bend!",
            "Control Booth Transfer",
            "Deep Fried Transfer",
            "Don't Look Down!",
            "Edge O' the Tub Extension",
            "From Way Down Town!",
            "Furnace Row Extension",
            "Furnace Topper Rail",
            "Furnace Walk Rail 2 Rail!",
            "Furnace Walk",
            "Generator Hop",
            "Generator Transfer",
            "Hardway over the Hot Tub",
            "High Voltage Walkway Lip",
            "Hot Tub Jump",
            "Just Passing Through",
            "Lil' Rail Hop",
            "Low Current Walkway Lip",
            "Nausea Grind!!!",
            "Nice View Up Here!",
            "Over the Pipe!",
            "Poolside Over Under Gap",
            "Porch Rail Tap",
            "Press Booth Rail 2 Rail",
            "Press Box Kink",
            "Press Walk Rail 2 Rail!",
            "Rail Hop",
            "Railin' on Furnace Row",
            "Roll In Hop",
            "Roll In Transfer",
            "Round the Bend!!!",
            "Split the Wickets!",
            "Stair Steppin'",
            "Stomp the Presses!",
            "TC's Rail",
            "Tub Rail Tap",
            "Up And Over!!!",
            "Walkin' A Thin Line!",
        ]

# Change required gap for the Foundry goal

# TODO: classify these tricks into types, and optionally require grind tricks for grind gaps, etc.
# TODO: some of these gaps are in the foundry file, most are in cjr_scripts

# foundry vert: CJR_Foun_RailTrickGap
# foundry street: CJR_Foun_PipeTrickGap

# remove existing gapscripts
# foundry = foundry.splitlines(keepends=True)
# foundry[16626] = ""
# foundry[16633] = ""
# foundry[17890] = ""
# foundry[18479] = ""
# foundry[18487] = ""
# foundry[18792] = ""
# foundry[18821] = ""
# foundry[18835] = ""
# foundry[18864] = ""
# foundry[18872] = ""
# foundry[18886] = ""
# foundry = ''.join(foundry)

# foundry_gap_street = foundry_gaps.pop()
# foundry_gap_vert = foundry_gaps.pop()
# cjr[1275] = f'          Goal_TrickSpotStreet_Text = "{foundry_street_trick} | {foundry_gap_street}"\n'
# cjr[1276] = f'          Goal_TrickSpotVert_Text = "{foundry_vert_trick} | {foundry_gap_vert}"\n'
# cjr[4614] = f'#00000      StartGapTrick TrickText = "{foundry_vert_trick}"\n'
# cjr[4623] = f'#00000      StartGapTrick TrickText = "{foundry_street_trick}"\n'

# # add new scripts
# cjr = ''.join(cjr)
# regex = re.compile(r'(?<=Text = "' + foundry_gap_street + r'") (?=\n)')
# cjr = regex.sub("\n          GapScript = CJR_Foun_RailTrickGap\n", cjr)
# regex = re.compile(r'(?<=Text = "' + foundry_gap_vert + r'") (?=\n)')
# cjr = regex.sub("\n          GapScript = CJR_Foun_PipeTrickGap\n", cjr)
