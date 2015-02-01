'''
OS Helpers
'''
import os, glob
import PIL_Helper

def Delete(filename):
    filelist = glob.glob(filename)
    for f in filelist:
        os.remove(f)

def CleanDirectory(path=".", mkdir="workspace", rmstring="*.*"):
    dir_path = os.path.join(path, mkdir)
    if not os.path.exists(dir_path):
        os.mkdir(dir_path)
    else:
        Delete(os.path.join(dir_path, rmstring))
    return dir_path

def BuildPage(card_list, page_num, page_width, page_height,
              workspace_path):
    PIL_Helper.BuildPage(card_list, page_width, page_height,
                         os.path.join(
                             workspace_path,
                             "page_{0:>03}.png".format(page_num)
                             )
                         )

def BuildBack(card_list, page_num, page_width, page_height,
              workspace_path):
    back_list=[]
    for i in range(0,page_height):
        for j in range(1,page_width+1):
            back_list.append(card_list[(i+1)*page_width-j])

    PIL_Helper.BuildPage(back_list, page_width, page_height,
                         os.path.join(
                             workspace_path,
                             "backs_{0:>03}.png".format(page_num)
                             )
                         )
