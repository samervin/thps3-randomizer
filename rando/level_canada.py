from rando.level2 import Level2
import random

class LevelCanada(Level2):

    def __init__(self):
        self.name = "Canada"
        self.name_flag = "CANADA"
        self.level_type = "normal"
        self.filepath = "Can/can"
        self.filename = "can"
        self.location_vectors = [
            (5777.408, 504.1701, -7354.0566), # Secret tape
            (-899.97943, -140.22043, -6126.5093), # Deck 1
            (4400.712, 74.529945, -5524.069),
            (-522.8683, -6.069225, -7091.4814),
            (55.48668, -183.44315, -6871.7593), # SKATE 1
            (-2584.4258, -72.25653, -7013.3984),
            (-2584.845, -470.39392, -4839.827),
            (-1897.2305, -404.26462, -3077.323),
            (-1224.1876, -362.80075, -4180.8945),
            (-1007.47156, -260.41443, -6018.28), # SKATE 2
            (-1018.30164, -297.67218, -3412.2031),
            (-968.63904, -150.59337, -225.18188),
            (1167.6864, -75.82086, -547.2684),
            (1346.6444, -101.470795, -2321.2173),
            (2461.861, -298.02975, -7220.551), # SKATE 3
            (3782.8833, 173.50699, -8046.485),
            (5619.0566, 163.44263, -7583.656),
            (7627.016, -156.94495, -6745.6294),
            (9196.729, -27.40274, -5204.8794),
            (-2033.959, -485.29556, -4829.2144), # Stats 1
            (421.30203, -174.80338, -6133.572),
            (2221.754, -313.32602, -3394.379),
            (4441.5024, 0.0, -3561.5576),
            (3865.0378, -380.9708, -7220.951),
            (-1166.9951, -355.38177, -4210.8076), # Stats 2
            (-659.4756, -235.225, -6478.1875),
            (-894.6368, -263.27164, -6124.2373),
            (4480.3315, 157.55911, -7773.051),
            (6836.419, 0.0, -4923.892),
            (-2581.9644, -486.45868, -3766.6724), # Stats 3
            (2457.5527, 0.0, -6658.429),
            (498.82764, -254.18225, -2928.3389),
            (5988.236, 239.42007, -7455.1465),
            (5220.0107, 165.84673, -7023.859),
            (-1800.3221, -228.97916, -3069.9868), # Stats 4
            (1266.8137, -297.92496, -6490.1626),
            (973.1262, 0.0, -234.65845),
            (7268.462, -254.00351, -6337.111),
            (3530.3818, 99.633064, -6661.432),
        ]

    def _shuffle(self, any_list):
        shuffled = any_list.copy()
        random.shuffle(shuffled)
        return shuffled

    def shuffle_pedestrian_location_vectors(self, data):
        # note: default proxim vectors are not exact matches but are close enough to be reused
        default_skater_vectors = [
            (381.30197, -254.02527, -2167.938), # bully02 / proxim04 / LEVEL_FLAG_PED_5 / "bully2"
            (-1112.4061, -192.00003, 75.853546), # bully04 / proxim05 / LEVEL_FLAG_PED_4 / "bully4"
            (-691.54285, -180.00003, -3252.4006), # bully06 / proxim03 / LEVEL_FLAG_PED_3 / "bully3"
            (-913.89844, -300.96082, -6270.0073), # bully07 / proxim01 / LEVEL_FLAG_PED_2 / "bully2"
            (2315.6704, -180.00003, -6188.2744), # bully08 / proxim02 / LEVEL_FLAG_PED_1 / "bully1"
            # last position also used for bully01, but bully01 is only for the goal camera
        ]
        default_chuck_vector = [(386.28195, -352.99506, -7219.1826)]
        vectors = self._shuffle(default_chuck_vector + default_skater_vectors)

        for i in [1, 2, 3, 4, 5]:
            vector = vectors.pop()
            vector_value = f"VECTOR[{vector[0]}; {vector[1]}; {vector[2]}]"
            data = data.replace("{{" + f"rando_can_vector_bully{i}" + "}}", vector_value)

        # replace chuck
        vector = vectors.pop()
        vector_value = f"VECTOR[{vector[0]}; {vector[1]}; {vector[2]}]"
        data = data.replace("{{rando_can_vector_chuck}}", vector_value)

        return data

        # -X = farther from spawn
        # +X = closer to spawn
        # -Y = lower to ground
        # +Y = higher above ground
        # -Z = left of spawn
        # +Z = right of spawn

        # TODO: add custom locations
        # TODO: fix overlapping characters in goal cameras
        # TODO: always point camera at valid skater/chuck
        # TODO: move "laughers" near Chuck
        # TODO: change Chuck's path after getting unstuck (or accept the silliness of the existing behavior)
