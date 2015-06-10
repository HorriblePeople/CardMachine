#!/usr/bin/python
'''
Generate a single card
'''
import argparse
import base64
import traceback
import sys

def make_single_card(base_dir, card_line, output_file, module_name, set_name):
    try:
        module = __import__(module_name)
    except ValueError:
        print "Failed to load module: " + str(ValueError)
        return
    module.CardSet = base64.b64decode(set_name)

    try:
        decoded_cardline = base64.b64decode(card_line)
        print("Attempting to build card '%s' to %s" % (decoded_cardline, output_file))
        module.BuildSingleCard(base64.b64decode(card_line).decode('utf-8'), output_file)
    except Exception as e:
        print("Failed to build single card '%s'" % decoded_cardline)
        print(traceback.format_exc())
        sys.exit(1)
    print("Success!")
    sys.exit(0)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(prog="GameGen")

    parser.add_argument('-b', '--basedir',
                        help="Workspace base directory with resources output directory",
                        default="TSSSF")
    parser.add_argument('-c', '--card_line', \
                        help="Base64 encoded single-line card definition",
                        required=True)
    parser.add_argument('-o', '--output',
                        help="File to write card to",
                        required=True)
    parser.add_argument('-m', '--module',
                        help="Module to use",
                        default="TSSSF_CardGen")
    parser.add_argument('-s', '--setname',
                        help="Set name to use",
                        default="TEST CARD")

    args = parser.parse_args()

    make_single_card(args.basedir, args.card_line,
                     args.output, args.module, args.setname)


