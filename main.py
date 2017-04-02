import argparse
import copy
from logic import *
from music import *


def parse():
    parser = argparse.ArgumentParser()
    parser.add_argument("-a", default=2, help="The 'a' param of Weierstrass function. Default set to 2.", type=int)
    parser.add_argument("-b", default=2, help="The 'b' param of Weierstrass function. Default set to 2.", type=int)
    parser.add_argument("-p", "--plot", default="draw", help="Draw plot of generated function. Default draw.",
                        choices=["no-draw", "draw"])
    parser.add_argument("-c", default=16, help="Count of sounds in one riff. Default set to 16.", type=int)
    parser.add_argument("--octaves", default=1, help="Number of octaves used. Default set to 1.", choices=[1, 3, 5],
                        type=int)
    key_choices = ["C", "C#", "D", "Eb", "E", "F", "F#", "G", "G#", "A", "Bb", "B"]
    parser.add_argument("-k", "--key", default="C", help="Main note of main scale. Default C.", choices=key_choices)
    parser.add_argument("--kind", default="minor", help="Kind of scale. Default minor.", choices=["major", "minor"])
    parser.add_argument("-r", "--riffs", help="Number of riffs in file. Default 8.", default=8, type=int)
    parser.add_argument("-i", "--iterations", help="Number of mutation iterations. Default 2.", default=2, type=int)
    parser.add_argument("--bpm", help="Bits per minute. Default 240.", default=240, type=int)
    parser.add_argument("--interval", help="Distance between 2 sounds (in bits). Default 1", default=1, type=float)
    parser.add_argument("-o", "--output", help="Destination of output file.", default="myfile.midi")
    args = parser.parse_args()
    global a, b, draw, count, octaves, key, kind, riffs_num, iterations, bpm, interval, dest, folder
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
    main_riff = generate_riff(scale, pre_data["values"], pre_data["max"], pre_data["min"])
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
