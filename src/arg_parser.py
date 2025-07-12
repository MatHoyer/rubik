import argparse


def arg_parser():
    parser = argparse.ArgumentParser(
        prog="Rubik",
        description="Rubik solver",
    )

    mix_group = parser.add_mutually_exclusive_group(required=True)
    mix_group.add_argument(
        "-r", "--random",
        action="store_true",  # Always true if provided
        help="generate a random mix"
    )
    mix_group.add_argument(
        "-m", "--mix",
        type=str,
        help="provide mix sequence"
    )

    random_group = parser.add_argument_group("options for --random")
    random_group.add_argument(
        "--range",
        type=int,
        help="choose the number of action in the random mix sequence (default 20)"
    )

    return parser
