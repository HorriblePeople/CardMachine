#!/usr/bin/python
'''
Generate a single card
'''
import argparse
import base64
import traceback
import sys
import urllib
import TSSSF_CardGen
from StringIO import StringIO


def SaveCardToFile(image_object, location):
    image_object.save(location, format="PNG", dpi=(300, 300))
    return location


def SaveCardToURL(image_object):
    fileobj = StringIO()
    image_object.save(fileobj, format="PNG", dpi=(300, 300))
    encoded_image = fileobj.getvalue().encode("base64")
    return("data:image/png;base64," + urllib.quote(encoded_image))


def SaveCard(image, save_type, location=None):
    if save_type == "file":
        retval = SaveCardToFile(image, location)
    elif save_type == "encoded_url":
        retval = SaveCardToURL(image)
    elif save_type == "imgur":
        raise ValueError("imgur save not yet implemented")
    else:
        raise ValueError("save type not recognized")
    return retval


def make_single_card(base_dir, encoded_line, output_file,
                     image_type, set_name, save_type):
    my_stdout = sys.stdout
    sys.stdout = sys.stderr

    TSSSF_CardGen.CardSet = base64.b64decode(set_name)

    im = {}

    try:
        card_line = base64.b64decode(encoded_line).decode('utf-8')
        print("Attempting to build card '%s'" % (card_line))
        (im["bleed"],
         im["cropped"],
         im["vassal"]) = TSSSF_CardGen.BuildSingleCard(card_line)

        outstr = SaveCard(im[image_type], save_type, output_file)
        print >> my_stdout, outstr
    except Exception:
        print("Failed to build single card '%s'" % card_line)
        print(traceback.format_exc())
        sys.exit(1)
    print("Success!")
    sys.exit(0)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(prog="GameGen")

    parser.add_argument('-b', '--basedir',
                        help="Workspace base directory with resources output directory",
                        default="TSSSF")
    parser.add_argument('-c', '--card_line',
                        help="Base64 encoded single-line card definition",
                        required=True)
    parser.add_argument('-o', '--output',
                        help="File to write card to",
                        default=None)
    parser.add_argument('-s', '--setname',
                        help="Set name to use",
                        default="TEST CARD")
    parser.add_argument('-i', '--imagetype',
                        help="Set image type to output",
                        choices=("bleed", "cropped", "vassal"),
                        default="cropped")
    parser.add_argument('-r', '--returntype',
                        help="Output format",
                        choices=("file", "encoded_url", "imgur"),
                        default="cropped")

    args = parser.parse_args()

    if args.returntype == "file" and args.output is None:
        parser.error("--output must be defined if --returntype is set to file")

    make_single_card(args.basedir, args.card_line, args.output,
                     args.imagetype, args.setname, args.returntype)
