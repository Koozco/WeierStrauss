class Scale:
    major_formula = [2, 2, 1, 2, 2, 2, 1]
    minor_formula = [2, 1, 2, 2, 1, 2, 2]

    note_values = {"C": 60, "C#": 61, "D": 62, "Eb": 63,
                   "E": 64, "F": 65, "F#": 66, "G": 67,
                   "G#": 68, "A": 69, "Bb": 70, "B": 71}

    def __init__(self, octaves, key, scale_type):

        self.formula = self.major_formula \
            if scale_type == "major" else self.minor_formula
        self.key_note = self.note_values[key]
        self.notes = [self.key_note]

        for i in range(0, octaves):
            d = i * 12
            for n in self.formula:
                d += n
                self.notes.append(self.key_note + d)

        offset = 12 * (octaves // 2)
        self.notes = [n - offset for n in self.notes]


class Sound:
    def __init__(self, sound):
        self.sounds = [sound]
        self.velocity = 127
        self.elongation = 0
        self.time = 0
        self.duration = 1

    def add_sound(self, sound):
        self.sounds.append(sound)
