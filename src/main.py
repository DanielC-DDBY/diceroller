import argparse
import json
import re
from pathlib import Path
from .roll import Dice, Roll

#
# GLOBALS
#
DATA_PATH = Path(__file__).resolve().parent / "saved_ids.json"
print(DATA_PATH)

#HELPER. Loads a roll from a specific id.
def load(id=int):
    with DATA_PATH.open("r", encoding="utf-8") as f:
        data = json.load(f)
    return data[id]


#Saves an argument to saved_rolls.json
#Arguments:
#   roll - the roll that needs to be saved (e.g 8d8 + 5)
def save(args):
    with open("data.txt"):
        pass
    print(f"Saved {args.roll}")

#Deletes the roll attached to the specified id in saved_rolls.json
#Arguments:
#   id - the id of the roll in saved_rolls.json to be deleted
#   -a - clear the entire file if true
def delete(args):
    print(f"Deleted {args.id}")

#Lists the roll attached to the specified id in saved_rolls.json
#Arguments:
#   id - the id of the roll in saved_rolls.json to be listed
#   -a - list the entire file if true
def list(args):
    print(f"Listing {args.id}")

#rolls a roll
#Arguments:

def roll(args):
    
    roll_string = ""

    if (args.name is None) == (args.id is None):
        args.parser.error("Provide either a name OR an -id")
        return

    if args.id is not None:
        roll_string = load(args.id)
        print(f"Rolling saved entry {roll_string} from id {args.id}")
    elif args.roll is not None:
        roll_string = args.roll
        print(f"Rolling {roll_string}")
    
    # One term: optional sign, then either dice (NdM) or a flat number
    TERM = re.compile(r"\s*([+-]?)\s*(?:(\d*)d(\d+)|(\d+))", re.IGNORECASE)

    VALID = re.compile(
    r"\s*[+-]?\s*(?:\d*d\d+|\d+)(?:\s*[+-]\s*(?:\d*d\d+|\d+))*\s*",
    re.IGNORECASE,)

    input = []

    if not VALID.fullmatch(roll_string):
        args.parser.error(f"Invalid dice expression: {roll_string}")
        return
    for m in TERM.finditer(roll_string):
        sign, count, size, flat = m.groups()
        sign = -1 if sign == "-" else 1

        if size: #if size is true, then create a Dice object and add to terms
            da = count or 1 #dice amount is equal to the count provided or one
            for i in range(da):
                d = Dice(size, sign, da)
                input.append(d)
        else:
            input.append(flat * sign)

    rl = Roll(input)
    rl.roll
    rl.form_output

    print(f"{rl.form_output()}")
    
def repeat_roll(args):
    print(f"Rolling {args.reps} iterations...")
    for _ in range(args.reps):
        roll(args)



#builds the parser
def build_parser():
    parser = argparse.ArgumentParser(prog="dr")
    subparsers = parser.add_subparsers(dest="command", required=True)

    save_par = subparsers.add_parser("save", aliases=["s"], help="")
    save_par.add_argument("roll", type=str)
    save_par.set_defaults(func=save)

    delete_par = subparsers.add_parser("delete", aliases=["clear", "d"], help="")
    delete_par.add_argument("id", type=int)
    delete_par.add_argument("-a", "--all", action="store_true", help="")
    delete_par.set_defaults(func=delete)

    list_par = subparsers.add_parser("list", aliases=["ls"], help="")
    list_par.add_argument("id", type=int)
    list_par.add_argument("-a", "--all", action="store_true", help="")
    list_par.set_defaults(func=list)

    roll_par = subparsers.add_parser("roll", aliases=["r"], help="Roll a dice expression")
    roll_par.add_argument("roll", type=str, help="Dice expression (e.g. 2d6 + 3 + 1d4)")
    roll_par.add_argument("-i", "--id", nargs="?", type=int, help="ID of a saved roll")
    roll_par.set_defaults(func=roll)

    repeat_par = subparsers.add_parser("repeat", aliases=["rr"], help="Roll multiple iterations of an expression")
    repeat_par.add_argument("roll", type=str, help="Dice expression (e.g. 2d6 + 3 + 1d4)")
    repeat_par.add_argument("-i", "--id", nargs="?", type=int, help="ID of a saved roll")
    repeat_par.add_argument("-n", "--times", type=int, help="Number of repetitions")
    repeat_par.set_defaults(func=repeat_roll)


    return parser

#defines the "read-eval-print-loop", which keeps the program running 
#and recieving commands until it exits
def repl(parser):
    print("Welcome to DiceRoller")
    print("Type --help for commands, or exit to quit")
    while True:
        try:
            line = input("dr> ").strip()
        except (EOFError, KeyboardInterrupt): #ends program on ctrl+c
            print()
            break

        if not line:
            continue
        if line in ("exit, quit", "q"):
            break

        try:
            args = parser.parse_args(line.split)
        except SystemExit:
            continue

        if hasattr(args, "func"):
            args.func(args)


def main():
    parser = build_parser
    repl(parser)


main()