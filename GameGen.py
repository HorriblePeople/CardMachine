'''
Master Game Gen
1.0b
'''
import os, glob, importlib
import PIL_Helper
import OS_Helper
import config_helper
import sys
from sys import exit

#TSSSF Migration TODO:
#automagickally create vassal module :D
#individual artist naming
#.pon files have symbols like {ALICORN} and so on.

CARDGEN_NAME = "CardGen"
pjoin = os.path.join
        
def LoadModule(folder):
    """
    Loads the CardGen.py file from the given folder as a new module. 
    """
    print "Loading module {}...".format(folder)
    try:
        return importlib.import_module("{}.{}".format(folder, CARDGEN_NAME))
    except ValueError:
        print "Failed to load module: {}".format(folder)
        raise

def main(folder, card_set, filename='cards.pon',
         config_filename="config.ini"):
    config_helper.LoadConfig(folder, card_set, config_filename)
    config_helper.print_config()
    return

    
    LoadPaths(config, folder, card_set)
    module = LoadModule(folder)
    module.config = config

    print "Creating {} from file {}".format(folder, filename)

    CardFile = open(os.path.join(folder, card_set, filename))

    # Load Card File and strip out comments
    cardlines = [line for line in CardFile if not line[0] in ('#', ';', '/')]
    CardFile.close()

    # Make pages
    card_list = []
    back_list = []
    item_num = 0
    page_num = 0
    for line in cardlines:
        item_num += 1
        card_list.append(module.BuildCard(line, filename="{:>03}.png".format(item_num)))
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
        OS_Helper.BuildPage(card_list, page_num, module.PAGE_WIDTH, module.PAGE_HEIGHT, workspace_path)
        OS_Helper.BuildBack(back_list, page_num, module.PAGE_WIDTH, module.PAGE_HEIGHT, workspace_path)

    #Build Vassal
    module.CompileVassalModule()

    print "\nCreating PDF..."
    os.system(r'convert "{}/page_*.png" "{}/{}.pdf"'.format(workspace_path, output_path, card_set))
    print "\nCreating PDF of backs..."
    os.system(r'convert "{}/backs_*.png" "{}/backs_{}.pdf"'.format(workspace_path, output_path, card_set))
    print "Done!"

if __name__ == '__main__':
    main('TSSSF', 'Test')
