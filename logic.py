from math import pi
from math import sin
from random import random
from random import sample
from music import Sound
from miditime.miditime import MIDITime

import matplotlib as mpl

mpl.use('Agg')
# has to be imported after mpl.use('Agg')
import matplotlib.pyplot as plt


def weierstrass_function(n, a, b):
    def function(x):
        def sequence_elem(k):
            return ((1 / a) ** k) * sin((b ** k) * x)

        sequence = [sequence_elem(k) for k in range(0, n + 1)]
        return sum(sequence)

    return function


# draw function and select points to be tranformed into notes
def draw_function(a, b, draw, count, folder):
    d = 10000
    weier = weierstrass_function(30, a, b)
    xs = [2 * pi / d * k for k in range(1, d + 1)]
    ys = [weier(x) for x in xs]

    points = [k for k in range(0, d) if k % (d // count) == 0]

    n1 = [xs[k] for k in points]
    n2 = [ys[k] for k in points]

    if draw:

        plt.plot(n1, n2, 'ro')
        plt.axis([0, 3.15 * 2, min(ys) - 0.1, max(ys) + 0.1])
        plt.savefig(folder + 'chosen_notes.png')

        fig = plt.figure()
        ax = fig.add_subplot(111)
        ax.plot(ys)
        fig.savefig(folder + 'function_graph.png')

    min_val = min(ys)
    max_val = max(ys)
    # return chosen points and range of values
    return {"values": n2, "max": max_val, "min": min_val}


def generate_riff(scale, values, max_val, min_val):
    # transform range from (min, max) to (0, num_of_notes)
    # and then map func values to notes
    max_val -= min_val
    transform = len(scale.notes) / max_val
    riff = [Sound(scale.notes[int((y - min_val) * transform)]) for y in values]
    return riff


def mutate(riff, kind):
    # mutation probabilites
    elongation_pro = 0.15
    chord_pro = 0.1
    change_pro = 0.15
    riff_reverse_pro = 0.2
    # mutation probabilites

    def riff_reversion():
        riff.reverse()

    def elongation(sound):
        sound.elongation = sample([1, 2, 3], 1)[0]

    def mutate_to_chord(sound):
        if kind == "minor":
            sound.sounds.append(sound.sounds[0] + 3)
            sound.sounds.append(sound.sounds[0] + 7)
        elif kind == "major":
            sound.sounds.append(sound.sounds[0] + 4)
            sound.sounds.append(sound.sounds[0] + 7)

    def change_sound(sound):
        change = sample([-2, -1, 1, 2], 1)[0]
        for s in sound.sounds:
            s += change

    r = random()
    if r <= riff_reverse_pro:
        riff_reversion()

    for s in riff:
        r = random()
        if r <= elongation_pro:
            elongation(s)
        r = random()
        if r <= change_pro:
            change_sound(s)
        if r <= chord_pro:
            mutate_to_chord(s)


def generate_midi(sounds, bpm, folder, name):
    mymidi = MIDITime(bpm, folder + name)

    midinotes = []
    for s in sounds:
        for n in s.sounds:
            midinotes.append([s.time, n, s.velocity, s.duration])
            print(s.time, n, s.velocity, s.duration)

    # Add a track with those notes
    mymidi.add_track(midinotes)

    # Output the .mid file
    mymidi.save_midi()
