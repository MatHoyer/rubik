import logging

from arg_parser import arg_parser

from classes.Rubik import Rubik
from classes.Resolver import Resolver
from classes.Application import Application

logging.basicConfig(
    level=logging.INFO,
    format="%(levelname)s: %(message)-20s ---- %(asctime)s"
)

if __name__ == "__main__":
    parser = arg_parser()
    args = parser.parse_args()
    random_range = 20
    if args.random:
        if args.range:
            random_range = args.range
    else:
        if args.range is not None:
            parser.error("Option --range can\'t be used without --random")

    rubik = Rubik(mix=args.mix if args.mix else random_range)
    print(rubik)
    Resolver(rubik)
    app = Application(rubik)
    app.run()
