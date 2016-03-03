#!/usr/bin/env python
"""
pontojson.py: Convert Horrible People Games' cards.pon files to .json format
For use with the TSSSF Card Generator module
"""
__author__ = "Jouva Moufette"
__copyright__ = "Copyright 2016, Children of Kefentse"
__license__ = "CC-BY-SA"
__version__ = "1.0.0"
__maintainer__ = "Jouva Moufette"
__email__ = "jouva@childrenofkefentse.com"

import sys
import json
import os
import distutils.version
from collections import OrderedDict

TYPE, PICTURE, SYMBOLS, TITLE, KEYWORDS, BODY, FLAVOR, EXPANSION, CLIENT = range(9)
DEFAULT_ARTIST = "Pixel Prism"

Expansion_Icons = {
    "Indiegogo": "symbol-Indiegogo.png",
    "Summer": "symbol-summer-lovin.png",
    "Xtra": "symbol-extracredit.png",
    "Adventure": "symbol-adventure.png",
    "Custom": "symbol-custom.png",
    "Power": "symbol-power.png",
    "Multiplicity": "symbol-multiplicity.png",
    "Canon": "symbol-canon.png",
    "Dungeon": "symbol-dungeon.png",
    "2014": "symbol-2014.png",
    "2015": "symbol-2015.png",
    "Workshop": "symbol-workshop.png",
    "Hearthswarming": "symbol-hearthswarming.png",
    "Patreon": "symbol-Patreon.png",
    "anime": "symbol-weeaboo.png",
}


def convert_files(pon_file_path, json_file_path, artist):
    # Initialize and setup important data
    meta_key_order = ['name', 'version', 'module', 'symbol', 'defaultArtist', 'copyright']
    card_key_order = ['type', 'title', 'picture', 'artist', 'symbols', 'keywords', 'body', 'flavor', 'client']
    pack_key_order = ['deck', 'cards']
    special_card_types = ['Rules1', 'Rules3', 'Rules5', 'Warning', 'Card']
    cards = []
    expansions = []

    # Grab module name from first line and rest of file and close it
    pon_file = open(pon_file_path)
    module_name = pon_file.readline()
    cardlines = [line for line in pon_file if not line[0] in ('#', ';', '/')]
    pon_file.close()

    # Use the directory that holds the cards.pon file as the pack name and version
    pack_directory = os.path.basename(os.path.dirname(os.path.abspath(pon_file_path)))
    pack_directory_words = pack_directory.split(' ')
    pack_version_string = pack_directory_words.pop()
    try:
        pack_name = ' '.join(pack_directory_words)
        pack_version = distutils.version.StrictVersion(pack_version_string)
    except Exception:
        pack_name = pack_directory
        pack_version = distutils.version.StrictVersion("1.0.0")

    pack_metadata = {
        'name': pack_name,
        'version': str(pack_version),
        'module': module_name.strip(),
        'defaultArtist': artist,
        'copyright': "TSSSF by Horrible People Games."
    }

    for line in cardlines:
        card = {}
        row_data = line.strip('\n').strip('\r').replace(r'\n', '\n').split('`')

        card['type'] = row_data[TYPE]
        card['picture'] = row_data[PICTURE]

        # Special cards only have 2 columns of data; add the data we have, ignore the rest and move on
        if card['type'] in special_card_types:
            cards.append(card)
            continue

        card['title'] = row_data[TITLE]
        card['artist'] = artist

        # Clean up symbols: Ignore goal/ship as a symbol and don't make a list of them if there are none
        if row_data[SYMBOLS] != '':
            symbols = row_data[SYMBOLS].split('!')
            if row_data[TYPE].lower() != 'pony' and row_data[TYPE] in symbols:
                symbols.remove(row_data[TYPE])
            if len(symbols) > 0:
                card['symbols'] = symbols

        # Don't make a list of keywords if there are none
        if row_data[KEYWORDS] != "":
            card['keywords'] = [keywords.strip() for keywords in row_data[KEYWORDS].split(',')]

        if row_data[BODY] != "":
            card['body'] = row_data[BODY]
        card['flavor'] = row_data[FLAVOR]

        # Custom cards sometimes have a "client" attached to it (e.g. "for Horsefamous Pone")
        if len(row_data) - 1 >= CLIENT:
            card['client'] = row_data[CLIENT]

        # Handle expansion icons: Not all cards have expansions, but keep track to warn user of multiple expansions referenced
        if len(row_data) - 1 >= EXPANSION:
            if row_data[EXPANSION] not in expansions and row_data[EXPANSION] != '':
                expansions.append(row_data[EXPANSION])

        cards.append(card)

    # Keep the JSON of each card sorted in the order we want
    cards_ordered = [OrderedDict(sorted(item.iteritems(), key=lambda (k, v): card_key_order.index(k)))
                     for item in cards]

    # Core deck doesn't have an expansion so don't run this. Warn user of multiple expansions referenced
    if len(expansions) > 0:
        if len(expansions) > 1:
            print "Warning: Found more than one expansion referenced! Using the first entry of {0}".format(
                expansions[0])
        pack_metadata['symbol'] = Expansion_Icons.get(expansions[0])

    meta_ordered = OrderedDict(sorted(pack_metadata.iteritems(), key=lambda (k, v): meta_key_order.index(k)))

    # Put together cards and deck info and make sure deck is at the top of the JSON
    unordered_pack_data = {
        'deck': meta_ordered,
        'cards': cards_ordered
    }
    pack_data = OrderedDict(sorted(unordered_pack_data.items(), key=lambda (k, v): pack_key_order.index(k)))

    json_file = open(json_file_path, mode='w')
    json.dump(pack_data, json_file, indent=4)

    return True


if len(sys.argv) < 3:
    print "{} pon_file json_file [artist]".format(sys.argv[0])
    print "Example: {} \"Core Deck 1.1.6\"/cards.pon \"Core Deck 1.1.6\"/cards.json".format(sys.argv[0])
    print "Example: {} \"Core Deck 1.1.6\"/cards.pon \"Core Deck 1.1.6\"/cards.json \"Your Name\"".format(sys.argv[0])
    exit(1)

pon_file_path = sys.argv[1]
json_file_path = sys.argv[2]

artist = DEFAULT_ARTIST
if len(sys.argv) > 3:
    artist = sys.argv[3]

success = convert_files(pon_file_path, json_file_path, artist)
if success:
    print "Done converting"
