"""
Master Game Gen
1.1
@TODO Rework TSSSF/BABOC/etc to work with updated GameGen
"""
import argparse
import csv
import os
import sys

from OS_Helper import clean_directory, build_page, build_back

COMMENT_CHARS = ('#', ';', '/')
DELIMITER = ','


def save_card(filepath, image_to_save):
    """
    If the filepath already exists, insert _001 just before the
    extension. If that exists, increment the number until we get to
    a filepath that doesn't exist yet.
    """
    if os.path.exists(filepath):
        basepath, extension = os.path.splitext(filepath)
        i = 0
        while os.path.exists(filepath):
            i += 1
            filepath = "{}_{:>03}{}".format(basepath, i, extension)
    image_to_save.save(filepath, dpi=(300, 300))


def split_line(line):
    """
    Splits cards file lines. Will skip if the line is empty, or starts with a comment character.
    Leading/trailing whitespace is ignored and removed.
    Note: Comments after valid text will not be removed.
    :param line: string
    :return: List of strings, split based on DELIMITER. If the line should be skipped, will return None.
    """
    # Skip empty lists, strings, and None
    if not line:
        return

    if isinstance(line, str):
        line = line.strip('\r\n').strip()
        # Skip empty lines
        if not line:
            return
        # Skip comments
        if line and line[0] in COMMENT_CHARS:
            return
        line = line.replace(r'\n', '\n').split(DELIMITER)
    elif isinstance(line, list):
        # Skip empty lines
        if not line or line == ['']:
            return
        # Skip comments
        if line[0][0] in COMMENT_CHARS:
            return
    else:
        raise ValueError("line must be a list or a string")

    return [item.strip() for item in line]


def main(folder, filepath="cards.txt"):
    path = os.path.join(folder, filepath)
    if not os.path.exists(path):
        raise LookupError("'{}' does not exist".format(path))

    # Load card module
    try:
        folder, card_set = folder.split("/")
    except ValueError:
        raise ValueError("Folder must reference a folder and subfolder. e.g. Druid/Level 9")

    module_name = folder
    sys.path.append(module_name)
    try:
        import_name = folder.replace(' ', '_') + "_CardGen"
        module = __import__(import_name)
    except (ValueError, ImportError) as e:
        raise ValueError("Failed to load module: {}".format(e))

    # Create workspace for card images
    workspace_path = clean_directory(path=folder, mkdir="workspace", rm_string="*.*")

    # Create output directory
    output_folder = clean_directory(path=folder, mkdir=card_set, rm_string="*.pdf")
    
    # Create image directories
    bleed_path = clean_directory(path=os.path.join(folder, card_set), mkdir="bleed-images", rm_string="*.*")

    # Read in card lines
    f = open(path)
    card_lines = csv.reader(f) if path.endswith(".csv") else f.readlines()

    if module.BUILD_PAGES:
        page_num = 0
        card_list = []
        back_list = []

    # Make cards
    for i, line in enumerate(card_lines):
        # Skip header
        if i == 0 and module.FILE_HAS_HEADER:
            continue

        line = split_line(line)
        if line is None:
            continue

        card_image, filename, back_image, filename_back = module.build_card(line)
        # card_image.show()
        # back_image.show()
        # Save images of cards
        if filename:
            save_card(os.path.join(bleed_path, filename), card_image)
        if filename_back:
            save_card(os.path.join(bleed_path, filename_back), back_image)

        if module.BUILD_PAGES:
            card_list.append(card_image)
            back_list.append(back_image)
            if len(card_list) >= module.TOTAL_CARDS:
                page_num += 1
                print("Building Page {}...".format(page_num))
                build_page(card_list, page_num, module.PAGE_WIDTH, module.PAGE_HEIGHT, workspace_path)
                build_back(back_list, page_num, module.PAGE_WIDTH, module.PAGE_HEIGHT, workspace_path)
                card_list = []
                back_list = []

    if module.BUILD_PAGES:
        # If there are leftover cards, fill in the remaining
        # card slots with blanks and gen the last page
        if len(card_list) > 0:
            # Fill in the missing slots with blanks
            while len(card_list) < module.TOTAL_CARDS:
                card_list.append(module.build_blank())
                back_list.append(module.build_blank())
            page_num += 1
            print("Building Page {}...".format(page_num))
            build_page(card_list, page_num, module.PAGE_WIDTH, module.PAGE_HEIGHT, workspace_path)
            build_page(back_list, page_num, module.PAGE_WIDTH, module.PAGE_HEIGHT, workspace_path)

        # Build PDF
        print("\nCreating PDF...")
        os.system(r'convert "{}/page_*.png" "{}/{}.pdf"'.format(workspace_path, output_folder, card_set))
        print("\nCreating PDF of backs...")
        os.system(r'convert "{}/backs_*.png" "{}/backs_{}.pdf"'.format(workspace_path, output_folder, card_set))
        print("Done!")

    if module.BUILD_VASSAL:
        module.CompileVassalModule()

    f.close()


if __name__ == '__main__':
    # To run this script, you have two options:
    # 1) Run it from the command line with arguments. E.g.:
    #       python GameGen -b "Druid/Level 8" -f cards.txt
    # 2) Edit run_gamegen.py as appropriate
    # See the main() docstring for more info on the use of the arguments
    default_dir, default_file = "Chore Cards/1.0", "cards.csv"
    
    parser = argparse.ArgumentParser(prog="GameGen")
    parser.add_argument('-f', '--set-file',
                        help="Location of set file to be parsed",
                        default=default_file)
    parser.add_argument('-b', '--basedir',
                        help="Workspace base directory with resources output directory",
                        default=default_dir)
    args = parser.parse_args()
    main(args.basedir, args.set_file)
