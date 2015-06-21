#!/usr/bin/python
'''
Generate a single card
'''
import argparse
import base64
import traceback
import sys
import urllib
import requests
import TSSSF_CardGen
import json
import imgur_auth
from StringIO import StringIO


def SaveCardToFile(image_object, location):
    image_object.save(location, format="PNG", dpi=(300, 300))
    return location


def SaveCardToURL(image_object):
    fileobj = StringIO()
    image_object.save(fileobj, format="PNG", dpi=(300, 300))
    encoded_image = fileobj.getvalue().encode("base64")
    return("data:image/png;base64," + urllib.quote(encoded_image))


def GetImgurCredits():
    credits = requests.get(
        'https://api.imgur.com/3/credits.json',
        headers={'Authorization': 'Client-ID %s' % imgur_auth.CLIENT_ID},
        data={'key': imgur_auth.CLIENT_SECRET}
    )
    return json.loads(credits.text)["data"]["ClientRemaining"]


def SaveCardToImgur(image_object):
    #Make sure we have the budget to do this
    if GetImgurCredits() < 10:
        raise ValueError("Insufficient imgur credits remaining")
    fileobj = StringIO()
    image_object.save(fileobj, format="PNG", dpi=(300, 300))

    img_json = requests.post(
        'https://api.imgur.com/3/upload.json',
        headers={'Authorization': 'Client-ID %s' % imgur_auth.CLIENT_ID},
        data={
            'key': imgur_auth.CLIENT_SECRET,
            'title': 'Card generated with TSSSF Card Generator',
            'type': 'base64',
            'image': fileobj.getvalue().encode("base64")
        }
    )
    #return img_json.text
    return json.loads(img_json.text)["data"]["id"]


def SaveCard(image, save_type, location=None):
    if save_type == "file":
        retval = SaveCardToFile(image, location)
    elif save_type == "encoded_url":
        retval = SaveCardToURL(image)
    elif save_type == "imgur":
        retval = SaveCardToImgur(image)
    else:
        raise ValueError("save type not recognized")
    return retval


def make_single_card(encoded_line, output_file, image_type, save_type,
                     imgurtitle, imgurdesc):
    im = {}

    try:
        card_line = base64.b64decode(encoded_line).decode('utf-8')
        print("Attempting to build card '%s'" % (card_line))
        (im["bleed"],
         im["cropped"],
         im["vassal"]) = TSSSF_CardGen.BuildSingleCard(card_line)

        outstr = SaveCard(im[image_type], save_type, output_file)
        print >> ACTUAL_STDOUT, outstr
    except Exception:
        print("Failed to build single card '%s'" % card_line)
        print(traceback.format_exc())
        sys.exit(1)
    print("Success!")
    sys.exit(0)

if __name__ == '__main__':
    ACTUAL_STDOUT = sys.stdout
    sys.stdout = sys.stderr
    parser = argparse.ArgumentParser(prog="single_card.py")

    parser.add_argument('-c', '--card_line',
                        help="Base64-encoded single-line card definition",
                        required=True)
    parser.add_argument('-o', '--output',
                        help="File to write card to",
                        default=None)
    parser.add_argument('-i', '--imagetype',
                        help="Set image type to output",
                        choices=("bleed", "cropped", "vassal"),
                        default="cropped")
    parser.add_argument('-r', '--returntype',
                        help="Output format",
                        choices=("file", "encoded_url", "imgur"),
                        default="cropped")
    parser.add_argument('-t', '--imgurtitle',
                        help="Base64-encoded alternate imgur title",
                        default=None)
    parser.add_argument('-d', '--imgurdesc',
                        help="Base64-encoded alternate imgur description",
                        default=None)

    args = parser.parse_args()

    if args.returntype == "file" and args.output is None:
        parser.error("--output must be defined if --returntype is set to file")

    make_single_card(args.card_line, args.output, args.imagetype,
                     args.returntype, args.imgurtitle, args.imgurdesc)
