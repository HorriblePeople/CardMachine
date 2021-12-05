'''
Master Game Gen
1.1
'''
import os, glob
import PIL_Helper
import argparse
from OS_Helper import Delete, CleanDirectory, BuildPage, BuildBack
from sys import exit
import json


def main(folder="TSSSF", filepath="Core Deck/cards.json"):
    '''
    @param folder: The base game folder where we'll be working.
        E.g. TSSSF, BaBOC
    @param filepath: The filepath (relative to the base folder) where the
        file that defines the different cards in the game are stored.
    '''

    CardFile = open(os.path.join(folder, filepath))

    # Read first line of file to determine format and/or module
    first_line = CardFile.readline()
    if first_line == "{\n":
        file_type = 'json'
        # Load Card File
        CardFile.seek(0)
        data = json.load(CardFile)
        CardFile.close()
        module_name = data['deck']['module']
        cards = data['cards']
    else:
        file_type = 'pon'
        if first_line == "TSSSF_CardGen":
            print('Warning: .pon files are DEPRECATED for TSSSF. Support for this format may be removed soon. Please use the pontojson.py converter to convert this file to JSON format.')
        module_name = first_line
        # Load Card File and strip out comments
        cards = [line for line in CardFile if not line[0] in ('#', ';', '/')]
        CardFile.close()

    try:
        module = __import__(module_name.strip())
    except ValueError:
        print("Failed to load module: " + str(ValueError))
        return
    card_set = os.path.dirname(filepath)
    if file_type == 'json':
        if data['deck'].get('version', '') != '':
            card_set_text = '{} {}'.format(data['deck']['name'], data['deck']['version'])
        else:
            card_set_text = data['deck']['name']
        module.CardSet = card_set_text
        module.ARTIST = data['deck'].get('defaultArtist', module.ARTIST)
        if 'symbol' in data['deck']:
            module.Expansion_Icon = module.GetExpansionIcon(data['deck']['symbol'])

    else:
        module.CardSet = card_set

    module.card_set = module.CardSet

    # Create workspace for card images
    workspace_path = CleanDirectory(path=folder, mkdir="workspace", rmstring="*.*")

    # Create image directories
    bleed_path = CleanDirectory(path=folder + "/" + card_set, mkdir="bleed-images", rmstring="*.*")
    module.BleedsPath = bleed_path
    cropped_path = CleanDirectory(path=folder + "/" + card_set, mkdir="cropped-images", rmstring="*.*")
    module.CropPath = cropped_path
    vassal_path = CleanDirectory(path=folder + "/" + card_set, mkdir="vassal-images", rmstring="*.*")
    module.VassalPath = vassal_path
    TGC_path = CleanDirectory(path=folder+"/"+card_set, mkdir="TGC-images",rmstring="*.*")
    module.TGCPath = TGC_path
	
	
    # Create output directory
    output_folder = CleanDirectory(path=folder, mkdir=card_set, rmstring="*.pdf")

    # Make pages
    card_list = []
    back_list = []
    page_num = 0
    for line in cards:
        card_list.append(module.BuildCard(line))
        back_list.append(module.BuildBack(line))
        # If the card_list is big enough to make a page
        # do that now, and set the card list to empty again
        if len(card_list) >= module.TOTAL_CARDS:
            page_num += 1
            print("Building Page {}...".format(page_num))
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
        print("Building Page {}...".format(page_num))
        BuildPage(card_list, page_num, module.PAGE_WIDTH, module.PAGE_HEIGHT, workspace_path)
        BuildBack(back_list, page_num, module.PAGE_WIDTH, module.PAGE_HEIGHT, workspace_path)

    # Build Vassal
    module.CompileVassalModule()

    print("\nCreating PDF...")
    print('"{}\page_*.png" "{}\{}.pdf"'.format(workspace_path, output_folder, card_set))
    os.system(r'convert "{}\page_*.png" "{}\{}.pdf"'.format(workspace_path, output_folder, card_set))
    print("\nCreating PDF of backs...")
    print('"{}\backs_*.png" "{}\backs_{}.pdf"'.format(workspace_path, output_folder, card_set))
    os.system(r'convert "{}\backs_*.png" "{}\backs_{}.pdf"'.format(workspace_path, output_folder, card_set))
    print("Done!")


if __name__ == '__main__':
    # To run this script, you have two options:
    # 1) Run it from the command line with arguments. E.g.:
    #       python GameGen -b TSSSF -f "Core 1.0.3/cards.pon"
    # 2) Comment out "main(args.basedir, args.set_file)" in this file
    #       and add a new line with the proper folder and card set
    #       in the arguments.
    # See the main() docstring for more info on the use of the arguments
    parser = argparse.ArgumentParser(prog="GameGen")

    parser.add_argument('-f', '--set-file', \
                        help="Location of set file to be parsed",
                        default="cards.json")
    parser.add_argument('-b', '--basedir',
                        help="Workspace base directory with resources output directory",
                        default="TSSSF")

    args = parser.parse_args()

    #main(args.basedir, args.set_file)
    #main('TSSSF', 'Core Deck/cards.pon')
    #main('TSSSF', 'Mini Expansions\Multiplicity 0.0.1a\cards.json')
    #main('TSSSF', '1.1.0 Patch/cards.pon')
    #main('TSSSF', '2014 Con Exclusives/cards.pon')
    #main('TSSSF', 'BABScon 2015/cards.pon')
    #main('TSSSF', 'Core 1.0.5/cards.pon')
    #main('TSSSF', 'Core 1.0.5 Delta/cards.pon')
    #main('TSSSF', 'Core 1.1.0/cards.pon')
    #main('TSSSF', 'Core 1.1.0 Test/cards.pon')
    #main('TSSSF', 'Custom Card for/cards.pon')
    #main('TSSSF', 'Extra Credit 0.10.4/cards.pon')
    #main('TSSSF', 'Indiegogo/cards.pon')
    #main('TSSSF', 'Patreon Expansion 1/cards.pon')
    #main('TSSSF', 'Ponycon Panel 2015/cards.pon')
    #main('TSSSF', 'Ponyville University 1.0.1/cards.pon')
    #main('TSSSF', 'Ponyville University 0.0.2/cards.pon')
    #main('TSSSF', 'Ponyville University 1.0.2/cards.pon')
    #main('TSSSF', 'Thank You/cards.pon')
