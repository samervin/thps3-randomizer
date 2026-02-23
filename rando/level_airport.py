from rando.level2 import Level2
import random

class LevelAirport(Level2):

    def __init__(self):
        self.name = "The Airport"
        self.name_flag = "AIRPORT"
        self.level_type = "normal"
        self.filepath = "Ap/ap"
        self.filename = "ap"
        self.location_vectors = [
            (-2482.7217, -617.9677, -826.6797),
            (-2507.896, -614.01624, -8632.869),
            (3668.6519, -170.61533, 1346.9893),
            (3533.4453, -313.46106, -3555.8994),
            (4800.2026, 310.4785, 6088.829),
            (4295.666, -202.59496, -1731.2842),
            (2035.9762, -480.613, -5022.936),
            (-1448.335, -582.26, -3544.3164),
            (-1865.8955, -616.92346, -1501.624),
            (4456.992, 59.109474, 5719.401),
            (3806.5874, -100.58186, 788.38965),
            (-1162.5713, -743.374, -4779.6587),
            (-2237.1792, -1209.9019, -8444.701),
            (-2459.3276, -1272.9603, -910.0703),
            (5441.92, 125.93911, 7409.8076),
            (2974.3835, -344.81647, 531.2533),
            (1621.4966, -618.26117, -4747.6797),
            (-1859.9258, -582.26, -7980.539),
            (-101.806946, -1240.7891, -4729.9565),
            (4037.764, 175.39815, 5518.4717),
            (2503.146, 3.504364, 6042.002),
            (3798.2876, -153.09264, 1378.5479),
            (3617.1963, -250.62161, -3002.6885),
            (-343.9536, -631.9649, -2565.627),
            (4030.8525, 206.22589, 6877.295),
            (3512.8972, 4.572266, 6044.904),
            (4154.902, -136.95657, 1376.7871),
            (3534.6619, -346.99194, -1443.6416),
            (-332.52637, -628.90857, -6955.6973),
            (4039.692, 209.71304, 7468.8843),
            (3256.4805, -382.7985, 2696.0596),
            (3621.0715, -222.54279, -1677.5664),
            (3547.683, -343.90195, -3060.7842),
            (-1455.6289, -585.1545, -5941.162),
            (4785.0312, 276.10318, 4811.976),
            (3322.967, -225.46773, 3034.3887),
            (4300.166, -231.01527, -2973.3477),
            (1201.6841, -637.08093, -4701.9434),
            (-1894.7393, -614.4857, -2494.5352),
        ]
        # -X = right of spawn
        # +X = left of spawn
        # -Y = lower to ground
        # +Y = higher above ground
        # -Z = farther from spawn
        # +Z = closer to spawn

    def _shuffle(self, any_list):
        shuffled = any_list.copy()
        random.shuffle(shuffled)
        return shuffled

    def shuffle_pedestrian_location_vectors(self, data):
        default_buddy_vector = [(-1474.0542, -1003.2954, -7001.33)]
        buddy2_offset_x = -22
        buddy2_offset_z = -56
        custom_buddy_vectors = [
            (4232.0, -12.0, 7570.0), # Upper area on right
        ]

        vectors = self._shuffle(default_buddy_vector + custom_buddy_vectors)

        vector = vectors.pop()
        vector_value = f"VECTOR[{vector[0]}; {vector[1]}; {vector[2]}]"
        vector2_value = f"VECTOR[{vector[0] + buddy2_offset_x}; {vector[1]}; {vector[2] + buddy2_offset_z}]"
        data = data.replace("{{" + "rando_ap_vector_ticket_buddy1" + "}}", vector_value)
        data = data.replace("{{" + "rando_ap_vector_ticket_buddy2" + "}}", vector2_value)
        return data
