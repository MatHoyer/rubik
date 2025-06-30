import logging
import argparse
from classes.Rubik import Rubik
from classes.Color import Color
from classes.Position import Position

logging.basicConfig(
    level=logging.INFO,
    format='%(levelname)s: %(message)s ---- %(asctime)s'
)
parser = argparse.ArgumentParser(
    prog='Rubik',
    description="Rubik solver",
)
mix_group = parser.add_mutually_exclusive_group(required=True)
mix_group.add_argument(
    '-r', '--random',
    action='store_true',  # Always true if provided
    help="generate a random mix"
)
mix_group.add_argument(
    '-m', '--mix',
    type=str,
    help='provide mix senquence'
)
random_group = parser.add_argument_group("options for --random")
random_group.add_argument(
    '--range',
    type=int,
    help='choose the number of action in the random mix sequence (default 20)'
)

if __name__ == "__main__":
    args = parser.parse_args()
    random_range = 20
    if args.random:
        if args.range:
            random_range = args.range
    else:
        if args.range is not None:
            parser.error("Option --range can\'t be used without --random")

    cube = Rubik(mix=args.mix if args.mix else random_range)
    print(cube)
