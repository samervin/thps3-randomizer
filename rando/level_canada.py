from level import Level
import re
import random

class LevelCanada(Level):

    def __init__(self):
        self.name = "Canada"
        self.name_flag = "CANADA"
        self.level_type = "normal"
        self.filename = "Can/can"
        self.location_vectors = [
            'VECTOR[5777.408; 504.1701; -7354.0566]', # Secret tape
            'VECTOR[-899.97943; -140.22043; -6126.5093]', # Deck 1
            'VECTOR[4400.712; 74.529945; -5524.069]',
            'VECTOR[-522.8683; -6.069225; -7091.4814]',
            'VECTOR[55.48668; -183.44315; -6871.7593]', # SKATE 1
            'VECTOR[-2584.4258; -72.25653; -7013.3984]',
            'VECTOR[-2584.845; -470.39392; -4839.827]',
            'VECTOR[-1897.2305; -404.26462; -3077.323]',
            'VECTOR[-1224.1876; -362.80075; -4180.8945]',
            'VECTOR[-1007.47156; -260.41443; -6018.28]', # SKATE 2
            'VECTOR[-1018.30164; -297.67218; -3412.2031]',
            'VECTOR[-968.63904; -150.59337; -225.18188]',
            'VECTOR[1167.6864; -75.82086; -547.2684]',
            'VECTOR[1346.6444; -101.470795; -2321.2173]',
            'VECTOR[2461.861; -298.02975; -7220.551]', # SKATE 3
            'VECTOR[3782.8833; 173.50699; -8046.485]',
            'VECTOR[5619.0566; 163.44263; -7583.656]',
            'VECTOR[7627.016; -156.94495; -6745.6294]',
            'VECTOR[9196.729; -27.40274; -5204.8794]',
            'VECTOR[-2033.959; -485.29556; -4829.2144]', # Stats 1
            'VECTOR[421.30203; -174.80338; -6133.572]',
            'VECTOR[2221.754; -313.32602; -3394.379]',
            'VECTOR[4441.5024; 0.0; -3561.5576]',
            'VECTOR[3865.0378; -380.9708; -7220.951]',
            'VECTOR[-1166.9951; -355.38177; -4210.8076]', # Stats 2
            'VECTOR[-659.4756; -235.225; -6478.1875]',
            'VECTOR[-894.6368; -263.27164; -6124.2373]',
            'VECTOR[4480.3315; 157.55911; -7773.051]',
            'VECTOR[6836.419; 0.0; -4923.892]',
            'VECTOR[-2581.9644; -486.45868; -3766.6724]', # Stats 3
            'VECTOR[2457.5527; 0.0; -6658.429]',
            'VECTOR[498.82764; -254.18225; -2928.3389]',
            'VECTOR[5988.236; 239.42007; -7455.1465]',
            'VECTOR[5220.0107; 165.84673; -7023.859]',
            'VECTOR[-1800.3221; -228.97916; -3069.9868]', # Stats 4
            'VECTOR[1266.8137; -297.92496; -6490.1626]',
            'VECTOR[973.1262; 0.0; -234.65845]',
            'VECTOR[7268.462; -254.00351; -6337.111]',
            'VECTOR[3530.3818; 99.633064; -6661.432]',
        ]

    def _shuffle(self, any_list):
        shuffled = any_list.copy()
        random.shuffle(shuffled)
        return shuffled

    def shuffle_pedestrian_location_vectors(self, data):
        skater_names = [
            'TRG_Conc_Park_Bully02',
            'TRG_Conc_Park_Bully04',
            'TRG_Conc_Park_Bully06',
            'TRG_Conc_Park_Bully07',
            'TRG_Conc_Park_Bully08',
        ]
        skater_proxim_names = [
            'TRG_Conc_Park_Bully_Proxim04',
            'TRG_Conc_Park_Bully_Proxim05',
            'TRG_Conc_Park_Bully_Proxim03',
            'TRG_Conc_Park_Bully_Proxim01',
            'TRG_Conc_Park_Bully_Proxim02',
        ]
        # note: default proxim vectors are not _exact_ matches but are close enough
        default_skater_vectors = [
            'VECTOR[381.30197; -254.02527; -2167.938]', # bully02 / proxim04 / LEVEL_FLAG_PED_5
            'VECTOR[-1112.4061; -192.00003; 75.853546]', # bully04 / proxim05 / LEVEL_FLAG_PED_4
            'VECTOR[-691.54285; -180.00003; -3252.4006]', # bully06 / proxim03 / LEVEL_FLAG_PED_3
            'VECTOR[-913.89844; -300.96082; -6270.0073]', # bully07 / proxim01 / LEVEL_FLAG_PED_2
            'VECTOR[2315.6704; -180.00003; -6188.2744]', # bully08 / proxim02 / LEVEL_FLAG_PED_1 (position also used for bully01, but bully01 is only for the goal camera)
        ]
        chuck_name = 'TRG_Ped_Tongue_Stuck01'
        default_chuck_vector = ['VECTOR[386.28195; -352.99506; -7219.1826]']
        # -X = farther from spawn
        # +X = closer to spawn
        # -Y = lower to ground
        # +Y = higher above ground
        # -Z = left of spawn
        # +Z = right of spawn
        custom_ped_vectors = self._shuffle(default_chuck_vector + default_skater_vectors)

        # replace skater vectors and proxims
        for i, name in enumerate(skater_names):
            regex = re.compile(r"(?<=Position = ).+(?=\n.+Angles = .+\n.+Name = " + name + ")")
            data = regex.sub(custom_ped_vectors[i], data)
        for i, name in enumerate(skater_proxim_names):
            regex = re.compile(r"(?<=Position = ).+(?=\n.+Angles = .+\n.+Name = " + name + ")")
            data = regex.sub(custom_ped_vectors[i], data)
        # replace chuck
        chuck_regex = re.compile(r"(?<=Position = ).+(?=\n.+Angles = .+\n.+Name = " + chuck_name + ")")
        data = chuck_regex.sub(custom_ped_vectors[5], data)

        # TODO: add custom locations
        # TODO: fix overlapping characters in goal cameras
        # TODO: always point camera at valid skater/chuck
        # TODO: move "laughers" near Chuck
        # TODO: change Chuck's path after getting unstuck (or accept the silliness of the existing behavior)

        return data
