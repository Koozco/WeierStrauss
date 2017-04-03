import argparse
import copy
from logic import *
from music import *


def parse():
    parser = argparse.ArgumentParser()
    parser.add_argument("-a", default=2, type=float,
                        help="The 'a' param of Weierstrass function. Should be > 1. Default: 2.")
    parser.add_argument("-b", default=2, type=float,
                        help="The 'b' param of Weierstrass function. Default: 2.")
    parser.add_argument("-p", "--plot", default="draw", choices=["no-draw", "draw"],
                        help ="Draw plot of generated function. Default draw.")
    parser.add_argument("-c", default=16, type=int,
                        help="Count of sounds in one riff. Default: 16.")
    parser.add_argument("--octaves", default=1, choices=[1, 3, 5], type=int,
                        help="Number of octaves used. Default: 1.")
    key_choices = ["C", "C#", "D", "Eb", "E", "F", "F#", "G", "G#", "A", "Bb", "B"]
    parser.add_argument("-k", "--key", default="C", choices=key_choices,
                        help="Main note of main scale. Default: C.")
    parser.add_argument("--kind", default="minor", choices=["major", "minor"],
                        help="Kind of scale. Default: minor.")
    parser.add_argument("-r", "--riffs", default=8, type=int,
                        help="Number of riffs in file. Default: 8.")
    parser.add_argument("-i", "--iterations", default=2, type=int,
                        help="Number of mutation iterations. Default: 2.")
    parser.add_argument("--bpm", default=240, type=int,
                        help="Bits per minute. Default: 240.")
    parser.add_argument("--interval", default=1, type=float,
                        help="Distance between 2 sounds (in bits, float). Default: 1.")
    parser.add_argument("-o", "--output", default="myfile.mid",
                        help="Destination of output file. Default myfile.mid")
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
    # create copies of main riff to modified
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
