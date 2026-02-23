from rando.level2 import Level2
import random

class LevelSuburbia(Level2):

    def __init__(self):
        self.name = "Suburbia"
        self.name_flag = "SUBURBIA"
        self.level_type = "normal"
        self.filepath = "Sub/sub"
        self.filename = "sub"
        self.location_vectors = [
            (-1206.6799, 583.3293, -1351.7134),
            (977.0913, 459.43713, -1825.2423),
            (1908.6509, 417.40054, 588.1387),
            (1438.8392, 281.23767, -1323.8839),
            (640.66473, 185.79524, 1325.8542),
            (-359.1256, 337.87106, 1957.1946),
            (-2777.7969, 309.0816, 980.39575),
            (-1125.7509, 146.92953, -1287.7339),
            (720.19824, 237.78598, -1986.6615),
            (-1559.7197, 128.7738, 34.60319),
            (-1620.0673, 275.67316, 3104.954),
            (-604.89667, 120.74312, 1658.2446),
            (2691.0354, 303.62897, 1092.9321),
            (1906.1544, 426.63766, -1248.7202),
            (639.19183, 209.45209, -3164.4043),
            (3119.7224, 289.0555, -1330.9768),
            (-951.4291, 179.55133, 2110.8115),
            (-1917.8657, 298.41306, 368.63776),
            (-1057.4191, 356.19952, -2264.9758),
            (-1202.1332, 348.51923, -2837.4229),
            (1313.641, 295.9112, 123.34546),
            (1810.5798, 194.54764, -2765.8652),
            (-819.6379, 276.37128, 1069.0684),
            (-2679.0085, 183.74683, -653.9723),
            (-1202.1411, 348.51923, -2837.3691),
            (-2162.181, 201.35524, 2452.124),
            (465.544, 412.1003, 959.56995),
            (2612.6018, 125.12059, -1838.7396),
            (-276.96967, 206.95187, -2607.2837),
            (-1202.1411, 348.51923, -2837.3691),
            (269.3046, 252.0085, 1465.047),
            (-937.2649, 171.38205, 1496.9655),
            (1046.2705, 410.65912, 1779.4335),
            (-1875.1726, 183.41791, -489.5361),
            (-1202.1411, 348.51923, -2837.3691),
            (285.6929, 282.79004, 2245.5283),
            (-884.47156, 313.07306, 690.7351),
            (359.56247, 179.40479, -2605.6328),
            (1907.2192, 525.86304, -865.0955),
        ]

    def _shuffle(self, any_list):
        shuffled = any_list.copy()
        random.shuffle(shuffled)
        return shuffled

    def shuffle_pedestrian_location_vectors(self, data):
        # thin man, axe, 5 pumpkins, 4 power line branches
        thinman_vector = [(-2078.4802, 109.50501, -1663.9464)]
        axe_vector = [(1169.342, 70.39346, -2917.8477)]
        pumpkin_vectors = [ # squashed vectors are nearly identical
            (-348.44818, 41.118557, 1888.2429),
            (-1148.2771, 220.72224, -2312.6445),
            (-1910.3761, 203.29803, -298.4276),
            (2082.5012, 155.27545, 1111.7013),
            (2546.8457, 261.66766, -1331.6865),
        ]
        # branch_names = [
        #     'SUB_Branch01', # links 1879 (TRG_SparkController01) 1880 (SPARKS_01)
        #     'SUB_Branch02',
        #     'SUB_Branch03',
        #     'SUB_Branch04',
        # ]
        # branch_bounce_names = [ # after you hit the branch, they bounce around
        #     'SAT_BRANCH_01',
        #     'SAT_BRANCH_02',
        #     'SAT_BRANCH_03',
        #     'SAT_BRANCH_04',
        # ]
        # spark_names = [
        #     'SPARKS_01', # no links
        #     'SPARKS_02',
        #     'SPARKS_03',
        #     'SPARKS_04',
        # ]
        # spark_controller_names = [
        #     'TRG_SparkController01', # links 2047 (SUB_Spark01)
        #     'TRG_SparkController02',
        #     'TRG_SparkController03',
        #     'TRG_SparkController04',
        # ]
        # sub_spark_names = [
        #     'SUB_Spark01', # no links
        #     'SUB_Spark02',
        #     'SUB_Spark03',
        #     'SUB_Spark04',
        # ]
        # branch_vectors = [ # related vectors are nearly identical
        #     'VECTOR[1391.3225; 263.507; 967.53644]',
        #     'VECTOR[859.3812; 263.507; 1447.506]',
        #     'VECTOR[1629.691; 386.94537; 981.3468]',
        #     'VECTOR[934.3149; 382.8921; 1610.2545]',
        # ]

        # TODO: Moving the branches doesn't seem to do anything until _after_ they are removed from the wires
        vectors = self._shuffle(thinman_vector + axe_vector + pumpkin_vectors)

        for i in [1, 2, 3, 4, 5]:
            vector = vectors.pop()
            vector_value = f"VECTOR[{vector[0]}; {vector[1]}; {vector[2]}]"
            data = data.replace("{{" + f"rando_sub_vector_pumpkin{i}" + "}}", vector_value)

        thinman_vector = vectors.pop()
        thinman_vector_value = f"VECTOR[{thinman_vector[0]}; {thinman_vector[1]-15}; {thinman_vector[2]}]"
        data = data.replace("{{rando_sub_vector_thin_man}}", thinman_vector_value)

        axe_vector = vectors.pop()
        axe_vector_value = f"VECTOR[{axe_vector[0]}; {axe_vector[1]}; {axe_vector[2]}]"
        data = data.replace("{{rando_sub_vector_axe}}", axe_vector_value)

        # for i in range(7,10):
        #     branch_regex = re.compile(r"(?<=Position = ).+(?=\n.+Angles = .+\n.+Name = " + branch_names[i-7] + ")")
        #     bounce_regex = re.compile(r"(?<=Position = ).+(?=\n.+Angles = .+\n.+Name = " + branch_bounce_names[i-7] + ")")
        #     spark_regex = re.compile(r"(?<=Position = ).+(?=\n.+Angles = .+\n.+Name = " + spark_names[i-7] + ")")
        #     spark_controller_regex = re.compile(r"(?<=Position = ).+(?=\n.+Angles = .+\n.+Name = " + spark_controller_names[i-7] + ")")
        #     sub_spark_regex = re.compile(r"(?<=Position = ).+(?=\n.+Angles = .+\n.+Name = " + sub_spark_names[i-7] + ")")
        #     data = branch_regex.sub(vectors[i], data)
        #     data = bounce_regex.sub(vectors[i], data)
        #     data = spark_regex.sub(vectors[i], data)
        #     data = spark_controller_regex.sub(vectors[i], data)
        #     data = sub_spark_regex.sub(vectors[i], data)

        return data
