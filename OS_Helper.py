'''
OS Helpers
'''
import os, glob
import PIL_Helper


def delete(filename):
    file_list = glob.glob(filename)
    for f in file_list:
        os.remove(f)


def clean_directory(path=".", mkdir="workspace", rm_string="*.*"):
    dir_path = os.path.join(path, mkdir)
    if not os.path.exists(dir_path):
        os.mkdir(dir_path)
    else:
        delete(os.path.join(dir_path, rm_string))
    return dir_path


def build_page(card_list, page_num, page_width, page_height, workspace_path):
    PIL_Helper.BuildPage(card_list, page_width, page_height,
                         os.path.join(workspace_path, "page_{0:>03}.png".format(page_num)))


def build_back(card_list, page_num, page_width, page_height,
               workspace_path):
    # Flip back list vertically, so cards go right to left, top to bottom
    back_list = []
    for i in range(0, page_height):
        for j in range(1, page_width+1):
            back_list.append(card_list[(i + 1) * page_width - j])

    PIL_Helper.BuildPage(back_list, page_width, page_height,
                         os.path.join(workspace_path, "backs_{0:>03}.png".format(page_num)))
