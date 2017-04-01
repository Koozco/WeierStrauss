import argparse
import copy
from logic import *
from music import *


def parse():
    parser = argparse.ArgumentParser()
    parser.add_argument("-a", default=2, help="The 'a' param of Weierstrass function. Default set to 2.", type=int)
    parser.add_argument("-b", default=2, help="The 'b' param of Weierstrass function. Default set to 2.", type=int)
    parser.add_argument("-p", "--plot", default=True, help="Draw plot of generated function. Default set to true",
                        type=bool)
    parser.add_argument("-c", default=16, help="Count of sounds in one riff. Default set to 16.", type=int)
    parser.add_argument("--octaves", default=3, help="Number of octaves used. Default set to 3.", choices=[1, 3, 5],
                        type=int)
    key_choices = ["C", "C#", "D", "Eb", "E", "F", "F#", "G", "G#", "A", "Bb", "B"]
    parser.add_argument("-k", "--key", default="C", help="Main note of main scale", choices=key_choices)
    parser.add_argument("--kind", default="minor", help="Kind of scale.", choices=["major", "minor"])
    parser.add_argument("-r", "--riffs", help="Number of riffs in file", default=8, type=int)
    parser.add_argument("-i", "--iterations", help="Number of mutation iterations", default=2, type=int)
    args = parser.parse_args()
    global a, b, draw, count, octaves, key, kind, riffs_num, iterations
    a = args.a
    b = args.b
    draw = args.plot
    count = args.c
    octaves = args.octaves
    key = args.key
    kind = args.kind
    riffs_num = args.riffs
    iterations = args.iterations


# def main():
print("hello")
parse()
pre_data = draw_function(a, b, draw, count)
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
    n.time = 1.5 * i
    n.duration += n.elongation

generate_midi(sounds)



# if __name__ == '__main__':
#    main()
