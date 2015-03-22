#!/usr/bin/env python2
# -*- coding: utf-8 -*-
'''
Master Game Gen 
1.0b
'''
import os, glob, json
import PIL_Helper
from OS_Helper import *
import sys

#TSSSF Migration TODO:
#automagickally create vassal module :D
#individual artist naming
#.pon files have symbols like {ALICORN} and so on.

def main(folder=".", filepath="deck.cards"):
    if isinstance(folder, str):
        folder = folder.decode('utf-8', 'replace')
    if isinstance(filepath, str):
        filepath = filepath.decode('utf-8', 'replace')

    CardFile = open(os.path.join(folder, filepath), 'rb')
    card_set = os.path.dirname(filepath)

    # Read first line of file to determine module
    first_line = CardFile.readline().decode('utf-8', 'replace').strip()
    try:
        module = __import__(first_line)
    except ValueError:
        print "Failed to load module: " + str(ValueError)
        return
    module.CardSet = card_set

    # Custom translations: using translation.json file from card set folder and from game folder
    for tpath in (os.path.join(folder, 'translation.json'), os.path.join(folder, card_set, 'translation.json')):
        if not os.path.isfile(tpath):
            continue

        with open(tpath, 'rb') as fp:
            translation = json.loads(fp.read().decode('utf-8', 'replace'))

        if 'RulesDict' in translation:
            module.RulesDict.update(translation['RulesDict'])

        if first_line == "TSSSF_CardGen":
            if 'CopyrightString' in translation:
                module.CopyrightString = translation['CopyrightString']
            if 'ArtArtist' in translation:
                module.ARTIST = translation['ArtArtist']

    # Create workspace for card images
    workspace_path = CleanDirectory(path=folder, mkdir="workspace", rmstring="*.*")

    # Create image directories
    bleed_path = CleanDirectory(path=folder+"/"+card_set, mkdir="bleed-images",rmstring="*.*")
    module.BleedsPath = bleed_path
    cropped_path = CleanDirectory(path=folder+"/"+card_set, mkdir="cropped-images",rmstring="*.*")
    module.CropPath = cropped_path
    vassal_path = CleanDirectory(path=folder+"/"+card_set, mkdir="vassal-images",rmstring="*.*")
    module.VassalPath = vassal_path

    # Create output directory
    output_folder = CleanDirectory(path=folder, mkdir=card_set,rmstring="*.pdf")

    # Load Card File and strip out comments
    cardlines = [line.decode('utf-8', 'replace') for line in CardFile if not line[0] in ('#', ';', '/')]
    CardFile.close()

##    # Make a list of lists of cards, each one page in scale
##    cardpages = []
##    cardlines += ["BLANK" for i in range(1, module.TOTAL_CARDS)]
##    cardlines.reverse()
##    while len(cardlines) > module.TOTAL_CARDS:
##        cardpages.append([cardlines.pop() for i in range(0,module.TOTAL_CARDS)])

    # Make pages
    card_list = []
    back_list = []
    page_num = 0
    for line in cardlines:
        card_list.append(module.BuildCard(line))
        back_list.append(module.BuildBack(line))
        # If the card_list is big enough to make a page
        # do that now, and set the card list to empty again
        if len(card_list) >= module.TOTAL_CARDS:
            page_num += 1
            print "Building Page {}...".format(page_num)
            BuildPage(card_list, page_num, module.PAGE_WIDTH, module.PAGE_HEIGHT, workspace_path)
            BuildBack(back_list, page_num, module.PAGE_WIDTH, module.PAGE_HEIGHT, workspace_path)
            card_list = []
            back_list = []

    # If there are leftover cards, fill in the remaining
    # card slots with blanks and gen the last page
    if len(card_list) > 0:
        # Fill in the missing slots with blanks
        while len(card_list) < module.TOTAL_CARDS:
            card_list.append(module.BuildCard("BLANK"))
            back_list.append(module.BuildCard("BLANK"))
        page_num += 1
        print "Building Page {}...".format(page_num)
        BuildPage(card_list, page_num, module.PAGE_WIDTH, module.PAGE_HEIGHT, workspace_path)
        BuildBack(back_list, page_num, module.PAGE_WIDTH, module.PAGE_HEIGHT, workspace_path)

    #Build Vassal
    module.CompileVassalModule()

    if sys.platform == 'win32':
        print "\nCreating PDF (Windows)..."
        if os.path.isfile(r'imagemagick\convert.exe'):
            # on windows it working only with ascii path
            os.system(ur'imagemagick\convert.exe "{}/page_*.png" "{}/{}.pdf"'.format(
                workspace_path.decode('utf-8'),
                output_folder,
                card_set
                ))
            print "\nCreating PDF of backs..."
            os.system(ur'imagemagick\convert.exe "{}/backs_*.png" "{}/backs_{}.pdf"'.format(
                workspace_path.decode('utf-8'),
                output_folder,
                card_set
                ))
            print "Done!"
        else:
            print "Please download and unpack ImageMagick for Windows into imagemagick directory"
            print "PDF was not created"

    else:
        print "\nCreating PDF (*nix)..."
        os.system(ur'convert "{}/page_*.png" "{}/{}.pdf"'.format(
            workspace_path.decode('utf-8'),
            output_folder,
            card_set
            ).encode('utf-8'))
        print "\nCreating PDF of backs..."
        os.system(ur'convert "{}/backs_*.png" "{}/backs_{}.pdf"'.format(
            workspace_path.decode('utf-8'),
            output_folder,
            card_set
            ).encode('utf-8'))
        print "Done!"

if __name__ == '__main__':
    #main('TSSSF', '1.1.0 Patch/cards.pon')
    #main('TSSSF', '2014 Con Exclusives/cards.pon')
    #main('TSSSF', 'BABScon 2015/cards.pon')
    #main('TSSSF', 'Core 1.0.5/cards.pon')
    #main('TSSSF', 'Core 1.0.5 Delta/cards.pon')
    #main('TSSSF', 'Core 1.1.0/cards.pon')
    #main('TSSSF', 'Core 1.1.0 Test/cards.pon')
    #main('TSSSF', 'Custom Card for/cards.pon')
    #main('TSSSF', 'Extra Credit 0.10.4/cards.pon')
    main('TSSSF', 'Indiegogo/cards.pon')
    #main('TSSSF', 'Patreon Expansion 1/cards.pon')
    #main('TSSSF', 'Ponycon Panel 2015/cards.pon')
    #main('TSSSF', 'Ponyville University 0.0.2/cards.pon')
    #main('TSSSF', 'Ponyville University 1.0.1/cards.pon')
    #main('TSSSF', 'Ponyville University 1.0.2/cards.pon')
    #main('TSSSF', 'Thank You/cards.pon')
    #main('BaBOC', 'BaBOC 0.1.0/deck.cards')
