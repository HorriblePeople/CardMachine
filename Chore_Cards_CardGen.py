import traceback
from collections import namedtuple

import PIL_Helper

CardData = namedtuple("CardData", "title1, subtitle1, category1, stars1, title2, subtitle2, stars2")
DIRECTORY = "Chore Cards"

VERSION = "1.0"

FILE_HAS_HEADER = True

BUILD_PAGES = False
PAGE_WIDTH = 3
PAGE_HEIGHT = 3
TOTAL_CARDS = PAGE_WIDTH * PAGE_HEIGHT
BUILD_VASSAL = False

resource_path = DIRECTORY + "/resources/"

frames = {
    "monthly": PIL_Helper.LoadImage(resource_path + "/Border_Monthly_1task.png"),
    "weekly": PIL_Helper.LoadImage(resource_path + "/Border_Weekly_1task.png"),
    "monthly_bonus": PIL_Helper.LoadImage(resource_path + "/Border_2task_monthly.png"),
    "weekly_bonus": PIL_Helper.LoadImage(resource_path + "/Border_2task_weekly.png"),
    "back": PIL_Helper.LoadImage(resource_path + "/Border_back.png")
}

base_w, base_h = frames["monthly"].size
base_w_center = base_w / 2
base_h_center = base_h / 2
max_text_width = 600

second_half_offset = base_h_center - 60
anchors = {
    "category1": (110, 130),
    "title1": (base_w_center, 330),
    "subtitle1": (base_w_center, 430),
    "stars1": (base_w - 175, 100),
    "category2": (110, second_half_offset + 130),
    "title2": (base_w_center, second_half_offset + 330),
    "subtitle2": (base_w_center, second_half_offset + 430),
    "stars2": (base_w - 175, second_half_offset + 100)
}

fonts = {
    "category": PIL_Helper.BuildFont(resource_path + "CenturyGothicPro-Bold.otf", 50),
    "title": PIL_Helper.BuildFont(resource_path + "CenturyGothicPro-Bold.otf", 120),
    "title_small": PIL_Helper.BuildFont(resource_path + "CenturyGothicPro-Bold.otf", 110),
    "title_smaller": PIL_Helper.BuildFont(resource_path + "CenturyGothicPro-Bold.otf", 90),
    "subtitle": PIL_Helper.BuildFont(resource_path + "CenturyGothicPro.otf", 70),
    "subtitle_small": PIL_Helper.BuildFont(resource_path + "CenturyGothicPro.otf", 60),
    "subtitle_smaller": PIL_Helper.BuildFont(resource_path + "CenturyGothicPro.otf", 50)
}

symbols = {
    "blue_star": PIL_Helper.LoadImage(resource_path + "/Blue_Star.png"),
    "orange_star": PIL_Helper.LoadImage(resource_path + "/Orange_Star.png"),
    "purple_star": PIL_Helper.LoadImage(resource_path + "/Purple_Star.png")
}

color_dict = {
    "orange": (247, 146, 29),
    "blue": (0, 174, 239),
    "purple": (102, 45, 145)
}


def fix_file_name(filename):
    filename = filename.replace("\n", "")
    invalid_chars = [",", "?", '"', ":"]
    for c in invalid_chars:
        filename = filename.replace(c, "")
    filename = u"{}.png".format(filename)
    # print filename
    return filename


def build_card(tags):
    tags = CardData(*tags)
    try:
        card_image = make_card_front(tags)
        filename = fix_file_name("card")
    except Exception:
        print("Warning, Bad Card: {}".format(tags))
        traceback.print_exc()
        card_image = None
        filename = None
    try:
        back_image = make_card_back(tags)
        filename_back = fix_file_name("back")
    except Exception:
        print("Warning, Bad Card: {}".format(tags))
        traceback.print_exc()
        back_image = None
        filename_back = None
    # card_image.show()  # TEST
    return card_image, filename, back_image, filename_back


def make_card_front(tags):
    # Get frame, based on category and whether there's a bonus chore
    frame_name = tags.category1.lower()
    if tags.title2:
        frame_name += "_bonus"
    image = get_frame(frame_name)

    title1_text(image, tags)
    subtitle1_text(image, tags)
    category1_text(image, tags)
    stars1_symbol(image, tags)

    if tags.title2:
        title2_text(image, tags)
        subtitle2_text(image, tags)
        category2_text(image, tags)
        stars2_symbol(image, tags)

    return image


def make_card_back(tags):
    return get_frame("back")


def get_frame(card_type):
    return frames[card_type].copy()


def shrink_text(text, font_name, max_width=max_text_width):
    """
    Shrinks the text as needed to fit on a line.
    :param text:
    :param font_name: "title" or "subtitle"
    :return: Font object to use
    """
    font = fonts[font_name]
    if PIL_Helper.GetTextBlockSize(text, font)[0] <= max_text_width:
        return font
    font = fonts[font_name + "_small"]
    if PIL_Helper.GetTextBlockSize(text, font)[0] <= max_text_width:
        return font
    font = fonts[font_name + "_smaller"]
    return font


def title1_text(image, tags):
    text = tags.title1
    font = shrink_text(text, "title")
    anchor = anchors["title1"]
    color = color_dict["orange" if tags.category1.lower() == "weekly" else "blue"]
    print(repr(text))
    PIL_Helper.AddText(
        image=image,
        text=text,
        font=font,
        fill=color,
        anchor=anchor,
        valign="center",
        halign="center"
    )


def subtitle1_text(image, tags):
    text = tags.subtitle1
    font = shrink_text(text, "subtitle")
    anchor = anchors["subtitle1"]
    color = color_dict["orange" if tags.category1.lower() == "weekly" else "blue"]
    PIL_Helper.AddText(
        image=image,
        text=text,
        font=font,
        fill=color,
        anchor=anchor,
        valign="center",
        halign="center"
    )


def category1_text(image, tags):
    text = tags.category1
    font = fonts["category"]
    anchor = anchors["category1"]
    color = color_dict["orange" if tags.category1.lower() == "weekly" else "blue"]
    PIL_Helper.AddText(
        image=image,
        text=text,
        font=font,
        fill=color,
        anchor=anchor,
        valign="top",
        halign="left"
    )


def stars1_symbol(image, tags):
    symbol = symbols[("orange" if tags.category1.lower() == "weekly" else "blue") + "_star"]
    start_x, start_y = anchors["stars1"]
    offset = 100
    for i in range(int(tags.stars1)):
        image.paste(symbol, (start_x - offset * i, start_y), symbol)


def title2_text(image, tags):
    text = tags.title2
    font = shrink_text(text, "title")
    anchor = anchors["title2"]
    color = color_dict["blue" if tags.category1.lower() == "weekly" else "purple"]
    print(repr(text))
    PIL_Helper.AddText(
        image=image,
        text=text,
        font=font,
        fill=color,
        anchor=anchor,
        valign="center",
        halign="center"
    )


def subtitle2_text(image, tags):
    text = tags.subtitle2
    font = shrink_text(text, "subtitle")
    anchor = anchors["subtitle2"]
    color = color_dict["blue" if tags.category1.lower() == "weekly" else "purple"]
    PIL_Helper.AddText(
        image=image,
        text=text,
        font=font,
        fill=color,
        anchor=anchor,
        valign="center",
        halign="center"
    )


def category2_text(image, tags):
    text = "BONUS"
    font = fonts["category"]
    anchor = anchors["category2"]
    color = color_dict["blue" if tags.category1.lower() == "weekly" else "purple"]
    PIL_Helper.AddText(
        image=image,
        text=text,
        font=font,
        fill=color,
        anchor=anchor,
        valign="top",
        halign="left"
    )


def stars2_symbol(image, tags):
    symbol = symbols[("blue" if tags.category1.lower() == "weekly" else "purple") + "_star"]
    start_x, start_y = anchors["stars2"]
    offset = 100
    for i in range(int(tags.stars2)):
        image.paste(symbol, (start_x - offset * i, start_y), symbol)


if __name__ == "__main__":
    text = ["WIPE SWITCHES", "Kitchen", "WEEKLY", "1", "MOP", "Bedroom", "2"]
    image, name, back, back_name = build_card(text)
    image.show()
