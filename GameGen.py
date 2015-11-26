'''
Master Game Gen
1.0b
'''
import os, glob, sys
import PIL_Helper
import argparse
from OS_Helper import Delete, CleanDirectory, BuildPage, BuildBack
from sys import exit

#TSSSF Migration TODO:
#automagickally create vassal module :D
#individual artist naming
#.pon files have symbols like {ALICORN} and so on.

def main(folder, filepath="deck.cards"):

    CardFile = open(os.path.join(folder, filepath))
    folder, card_set = folder.split("/")

    # Read first line of file to determine module
    modulename = CardFile.readline().strip()
    sys.path.append(modulename)
    try:
        import_name = folder+"_CardGen"
        module = __import__(import_name)
    except ValueError:
        print "Failed to load module: " + str(ValueError)
        return
    module.CardSet = card_set

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
    cardlines = [line for line in CardFile if not line[0] in ('#', ';', '/')]
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

    print "\nCreating PDF..."
    os.system(r'convert "{}/page_*.png" "{}/{}.pdf"'.format(workspace_path, output_folder, card_set))
    print "\nCreating PDF of backs..."
    os.system(r'convert "{}/backs_*.png" "{}/backs_{}.pdf"'.format(workspace_path, output_folder, card_set))
    print "Done!"

if __name__ == '__main__':
    # To run this script, you have two options:
    # 1) Run it from the command line with arguments. E.g.:
    #       python GameGen -b TSSSF -f "Core 1.0.3/cards.pon"
    # 2) Edit run_gamegen.py as appropriate
    # See the main() docstring for more info on the use of the arguments
	default_dir, default_file = "TSSSF/Core 1.0.5", "cards.pon"
    
    parser = argparse.ArgumentParser(prog="GameGen")
    parser.add_argument('-f', '--set-file', \
                        help="Location of set file to be parsed",
                        default=default_file)
    parser.add_argument('-b', '--basedir',
                        help="Workspace base directory with resources output directory",
                        default=default_dir)
    args = parser.parse_args()
    main(args.basedir, args.set_file)
