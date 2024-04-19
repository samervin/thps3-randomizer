import random
import constants
import re
import os

class Level:

    name = None # used in level unlock message
    name_flag = None # used in LEVEL_UNLOCKED_ flags
    level_type = None # "normal" or "comp"
    filename = None # name of QB file
    location_vectors = []
    extra_vectors = []
    gaps = []

    def __init__(self):
        pass

    def _shuffle(self, any_list):
        shuffled = any_list.copy()
        random.shuffle(shuffled)
        return shuffled

    def read_level_file(self):
        with open(f'../vanilla-qbs/Levels/{self.filename}.qb', 'r') as f:
            return f.read()

    def memify(self, script):
        # make one long string, then split on lines, to include modified linebreaks
        script = ''.join(script)
        script = script.splitlines(keepends=True)
        output = []
        for i, line in enumerate(script):
            # substitute any #01234 with i (the current line number) zero-padded to 5 spaces
            output.append(re.sub(r'#\d{5}', f"#{i:05d}", line))
        return output

    def write_level_file(self, contents):
        contents = self.memify(contents)
        full_filename = f'../outfiles/Levels/{self.filename}.out'
        os.makedirs(os.path.dirname(full_filename), exist_ok=True)
        with open(full_filename, 'w', newline='\n') as fout:
            fout.writelines(contents)

    def get_shuffled_vectors(self, include_extras=False):
        vectors = self.location_vectors
        if include_extras:
            vectors = vectors + self.extra_vectors
        return self._shuffle(vectors)

    def shuffle_location_vectors(self, data, include_extras=False):
        vectors = self.get_shuffled_vectors(include_extras)
        match self.level_type:
            case "normal":
                location_names = constants.location_names
            case "comp":
                location_names = constants.competition_location_names
            case _:
                raise Exception("invalid type")
        for loc in location_names:
            regex = re.compile(r"(?<=Position = ).+(?=\n.+Angles = .+\n.+Name = " + loc + ")")
            data = regex.sub(vectors.pop(), data)
        return data

    def shuffle_pedestrian_location_vectors(self, data):
        # Overwrite me in levels that have pedestrians!
        return data

    def randomize(self, include_extras=False):
        data = self.read_level_file()
        data = self.shuffle_location_vectors(data, include_extras)
        data = self.shuffle_pedestrian_location_vectors(data)
        self.write_level_file(data)
