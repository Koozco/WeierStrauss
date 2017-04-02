import argparse
import copy
from logic import *
from music import *


def parse():
    helps = {
        "a": "The 'a' param of Weierstrass function. Default set to 2.",
        "b": "The 'b' param of Weierstrass function. Default set to 2.",
        "p": "Draw plot of generated function. Default draw.",
        "c": "Count of sounds in one riff. Default set to 16.",
        "octaves": "Number of octaves used. Default set to 1.",
        "k": "Main note of main scale. Default C.",
        "kind": "Kind of scale. Default minor.",
        "r": "Number of riffs in file. Default 8.",
        "i": "Number of mutation iterations. Default 2.",
        "bpm": "Bits per minute. Default 240.",
        "interval": "Distance between 2 sounds (in bits, float). Default 1",
        "o": "Destination of output file."
    }
    parser = argparse.ArgumentParser()
    parser.add_argument("-a", default=2, help=helps["a"], type=int)
    parser.add_argument("-b", default=2, help=helps["b"], type=int)
    parser.add_argument("-p", "--plot", default="draw",
                        help=helps["p"], choices=["no-draw", "draw"])
    parser.add_argument("-c", default=16, help=helps["c"], type=int)
    parser.add_argument("--octaves", default=1,
                        help=helps["octaves"], choices=[1, 3, 5], type=int)
    key_choices = ["C", "C#", "D", "Eb", "E", "F",
                   "F#", "G", "G#", "A", "Bb", "B"]
    parser.add_argument("-k", "--key", default="C",
                        help=helps["k"], choices=key_choices)
    parser.add_argument("--kind", default="minor",
                        help=helps["kind"], choices=["major", "minor"])
    parser.add_argument("-r", "--riffs", default=8,
                        help=helps["r"], type=int)
    parser.add_argument("-i", "--iterations", default=2,
                        help=helps["i"], type=int)
    parser.add_argument("--bpm", default=240,
                        help=helps["bpm"], type=int)
    parser.add_argument("--interval", default=1,
                        help=helps["interval"], type=float)
    parser.add_argument("-o", "--output", default="myfile.midi",
                        help=helps["o"])
    args = parser.parse_args()
    global a, b, draw, count, octaves, key, kind, \
        riffs_num, iterations, bpm, interval, dest, folder
    a = args.a
    b = args.b
    draw = args.plot == "draw"
    count = args.c
    octaves = args.octaves
    key = args.key
    kind = args.kind
    riffs_num = args.riffs
    iterations = args.iterations
    bpm = args.bpm
    interval = args.interval
    dest = args.output
    folder = []
    for p in dest.split('/')[:-1]:
        folder += p
        folder += "/"


def main():
    parse()

    pre_data = draw_function(a, b, draw, count, folder)
    scale = Scale(octaves, key, kind)
    main_riff = generate_riff(scale, pre_data["values"],
                              pre_data["max"], pre_data["min"])
    riffs = [main_riff]
    for i in range(0, riffs_num - 1):
        new_riff = copy.deepcopy(main_riff)
        riffs.append(new_riff)

    for i in range(0, iterations):
        for riff in riffs:
            mutate(riff, kind)

    sounds = []
    for riff in riffs:
        sounds += riff

    for i, n in enumerate(sounds):
        n.time = interval * i
        n.duration += n.elongation

    generate_midi(sounds, bpm, dest)


if __name__ == '__main__':
    main()
