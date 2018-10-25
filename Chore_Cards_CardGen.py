import traceback
from collections import namedtuple

import PIL_Helper

CardData = namedtuple("CardData", "name, cr, str, dex, con, hp, ac, speed, fly, swim, climb, burrow, darkvision, "
                                  "tremorsense, blindsight, size, actions, abilities, skills, page")
DIRECTORY = "Druid"
ARTIST = "Pixel Prism"

VERSION = "1.0"


BUILD_PAGES = False
PAGE_WIDTH = 3
PAGE_HEIGHT = 3
TOTAL_CARDS = PAGE_WIDTH*PAGE_HEIGHT
BUILD_VASSAL = False


ResourcePath = DIRECTORY+"/resources/"


base_w = 820
base_h = 1122
base_w_center = base_w/2
base_h_center = base_h/2
w_marg = 31
h_marg = 36
baserect=[(w_marg,h_marg),(base_w-w_marg,base_h-h_marg)]
textmaxwidth = 650
skillsmaxwidth = 500

croprect=(50,63,788+50,1088+63)

TextHeightThresholds = [363, 378, 600]
BarTextThreshold = [500]

fonts = {
    "Name": PIL_Helper.BuildFont(ResourcePath + "LemonMilk.otf", 50),
    "CR": PIL_Helper.BuildFont(ResourcePath + "LemonMilk.otf", 60),
    "CRsmall": PIL_Helper.BuildFont(ResourcePath + "LemonMilk.otf", 45),
    "Stat": PIL_Helper.BuildFont(ResourcePath + "LemonMilk.otf", 50),
    "Text": PIL_Helper.BuildFont(ResourcePath + "FuturaExtended.ttf", 35),
    "TextMedium": PIL_Helper.BuildFont(ResourcePath + "FuturaExtended.ttf", 32),
    "TextSmall": PIL_Helper.BuildFont(ResourcePath + "FuturaExtended.ttf", 28),
    "TextTiny": PIL_Helper.BuildFont(ResourcePath + "FuturaExtended.ttf", 25), 
    "Skills": PIL_Helper.BuildFont(ResourcePath + "FuturaExtended.ttf", 45),
    "Speeds": PIL_Helper.BuildFont(ResourcePath + "LemonMilk.otf", 40)
}

Anchors = {
    "Name": (80, 170),
    "CR": (-120, 143),
    "Str": (228, 370),
    "Dex": (228, 443),
    "Con": (230, 519),
    "HP": (231, 296),
    "AC": (231, 220),
    "Speed": (365, 240),
    "Size": (80, 120),
    "Actions": (90, 620), 
    "QuickRef": (base_w_center, 975),
    "CircleLVL": (120, 965),
    "MoonLVL": (-127, 965),
    "Abilities": (90,220),
    "Skills": (502,543),
    "Page": (-200, 120),
    "Version": (-85, 1058)
}

Frames = {
    "BEAST": PIL_Helper.LoadImage(ResourcePath+"/TEMPLATE_front.png"),
    "BACK": PIL_Helper.LoadImage(ResourcePath+"/TEMPLATE_back.png")
}

Symbols = {
    "speed": PIL_Helper.LoadImage(ResourcePath+"/spd.png"),
    "fly": PIL_Helper.LoadImage(ResourcePath+"/fly.png"),
    "swim": PIL_Helper.LoadImage(ResourcePath+"/swim.png"),
    "burrow": PIL_Helper.LoadImage(ResourcePath+"/burrow.png"),
    "blindsight": PIL_Helper.LoadImage(ResourcePath+"/blindsight.png"),
    "tremorsense": PIL_Helper.LoadImage(ResourcePath+"/tremorsense.png"),
    "darkvision": PIL_Helper.LoadImage(ResourcePath+"/darkvision.png"),
    "climb": PIL_Helper.LoadImage(ResourcePath+"/climb.png")
}

ColorDict={
    "White": (255, 255, 255),
    "Black": (0, 0, 0)
}

def FixFileName(tagin):
    FileName = tagin.replace("\n", "")
    invalid_chars = [",", "?", '"', ":"]
    for c in invalid_chars:
        FileName = FileName.replace(c,"")
    FileName = u"{}.png".format(FileName)
    #print FileName
    return FileName

def FixUnicode(text):
    return text.replace(r'\n','\n')

def build_card(tags):
    tags = CardData(*tags)
    try:
        im = MakeBeastCard(tags)
        filename = FixFileName(tags.name)
    except Exception as e:
        print "Warning, Bad Card: {0}".format(tags)
        traceback.print_exc()
        im = MakeBlankCard()
        filename = ""
    try:
        imback = MakeBeastBack(tags)
        filenameback = FixFileName("Back_"+tags.name)
    except Exception as e:
        print "Warning, Bad Card: {0}".format(tags)
        traceback.print_exc()
        imback = MakeBlankCard()
        filenameback = ""
    #im.show()  # TEST
    return im, filename, imback, filenameback

def GetFrame(card_type):
    return Frames[card_type].copy()

def TitleText(image, text, color=ColorDict["White"]):
    font = fonts["Name"]
    anchor = Anchors["Name"]
    print repr(text)
    PIL_Helper.AddText(
        image = image,
        text = text,
        font = font,
        fill = color,
        anchor = anchor,
        valign = "center",
        halign = "left"
    )
    
def CrText(image, text, color=ColorDict["White"]):
    
    font = fonts["CR"]
    width,height = PIL_Helper.GetTextBlockSize(text, font)
    if width > 40:
        font = fonts["CRsmall"]
    anchor = Anchors["CR"]
    PIL_Helper.AddText(
        image = image,
        text = text,
        font = font,
        fill = color,
        anchor = anchor,
        valign = "center",
        halign = "center"
    )

def StatText(image, tags, color=ColorDict["Black"]):
    font = fonts["Stat"]
    # Str
    PIL_Helper.AddText(
        image = image,
        text = tags.str,
        font = font,
        fill = color,
        anchor = Anchors["Str"]
    )
    # Dex
    PIL_Helper.AddText(
        image = image,
        text = tags.dex,
        font = font,
        fill = color,
        anchor = Anchors["Dex"]
    )
    # Con
    PIL_Helper.AddText(
        image = image,
        text = tags.con,
        font = font,
        fill = color,
        anchor = Anchors["Con"]
    )
    # HP
    PIL_Helper.AddText(
        image = image,
        text = tags.hp,
        font = font,
        fill = color,
        anchor = Anchors["HP"]
    )
    # AC
    PIL_Helper.AddText(
        image = image,
        text = tags.ac,
        font = font,
        fill = color,
        anchor = Anchors["AC"]
    )
    
def SpeedText(image, tags, color=ColorDict["Black"]):
    speeds = ["speed", "fly", "swim", "climb", "burrow", "darkvision", "tremorsense", "blindsight"]
    imageheight = 71
    offsetx = 0
    offsety = 0
    textoffset = 90
    anchorx, anchory = Anchors["Speed"]
    
    for speed in speeds:
        if not getattr(tags,speed) == "-":
            text = getattr(tags,speed)
            image.paste(Symbols[speed], (anchorx+offsetx, anchory+offsety), Symbols[speed])
            PIL_Helper.AddText(
                image = image,
                text = text,
                font = fonts["Speeds"],
                fill = color,
                anchor = (anchorx+textoffset+offsetx, anchory+offsety+(imageheight/2)),
                valign = "center",
                halign = "left"
            )
            offsety += 80
            if offsety >= 80*2:
                offsety = 0
                offsetx = 180

            
    PIL_Helper.AddText(
        image = image,
        text = "Size: {}".format(tags.size),
        font = fonts["TextSmall"],
        fill = "white",
        anchor = Anchors["Size"],
        valign = "center",
        halign = "left"
    )

def ActionsText(image, tags, color=ColorDict["Black"]):
    # Replacement of keywords with symbols
    font = fonts["Text"]
    width,height = PIL_Helper.GetTextBlockSize(tags.actions, font, max_width = textmaxwidth)
    if height > 300:
        font = fonts["TextMedium"]
    if height > 300:
        font = fonts["TextSmall"]
    anchor = Anchors["Actions"]
    text = tags.actions
    text = text.format(name=tags.name)
    text = FixUnicode(text)
    # # Get the size of the body text as (w,h)
    # body_text_size = PIL_Helper.GetTextBlockSize(
    #     text, fonts["Text"], textmaxwidth
    # )
    # # If the height of the body text plus the height of the flavor text
    # # doesn't fit in on the card in the normal position, move the body text up
    # if body_text_size[1] + flavor_text_size[1] > TextHeightThresholds[0]:
    #     anchor = Anchors["BodyShiftedUp"]
    # # If they still don't fit, makes the body text smaller
    # if body_text_size[1] + flavor_text_size[1] > TextHeightThresholds[1]:
    #     font = fonts["BodySmall"]
    #     body_text_size = PIL_Helper.GetTextBlockSize(
    #         text, font, textmaxwidth
    #         )
    #     # If they still don't fit, make it smaller again. They're probably
    #     # the changeling cards
    #     if body_text_size[1] + flavor_text_size[1] > TextHeightThresholds[1]:
    #         font = fonts["BodyChangeling"]
    #         leading = -3
    PIL_Helper.AddText(
        image = image,
        text = text,
        font = font,
        fill = color,
        anchor = anchor,
        halign = "left",
        max_width = textmaxwidth
    )
    
def QuickRef(image, tags):
    speeds = ["fly", "swim", "climb", "burrow", "darkvision", "tremorsense", "blindsight"]
    symbols = [Symbols[speed] for speed in speeds
               if not getattr(tags, speed) == "-"]
    if len(symbols) == 0:
        return
    padding = 10
    imagewidth = symbols[0].width
    refwidth = len(symbols) * imagewidth + (padding * (len(symbols) - 1))
    quickrefanchorx = Anchors["QuickRef"][0] - (refwidth / 2)
    quickrefanchory = Anchors["QuickRef"][1]
    offsetx = 0
    for symbol in symbols:
        image.paste(symbol, (quickrefanchorx + offsetx, quickrefanchory), symbol)
        offsetx += imagewidth + padding
        
def SpeedLimits(tags, text):
    if not tags.fly == "-" and text in ["2", "4", "6"]:
        return "8"
    if not tags.swim == "-" and text in ["2"]:
        return "4"
    return text
            
def Levels(image, CR, tags):
    Circle = {
        "0": "2",
        "1/8": "2",
        "1/4": "2",
        "1/2": "4",
        "1": "8"
        }
    text = SpeedLimits(tags, Circle.get(CR,"-"))
    PIL_Helper.AddText(
        image = image,
        text = text,
        font = fonts["CR"],
        fill = ColorDict["White"],
        anchor = Anchors["CircleLVL"],
        halign = "center"
    )

    Moon = {
        "0": "2",
        "1/8": "2",
        "1/4": "2",
        "1/2": "2",
        "1": "2",
        "2": "6",
        "3": "9",
        "4": "12",
        "5": "15",
        "6": "18"
        }
    if "Elemental" not in tags.name:
        text = Moon.get(CR,"-")
    else:
        text = "10"
    text = SpeedLimits(tags, text)
    PIL_Helper.AddText(
        image = image,
        text = text,
        font = fonts["CR"],
        fill = ColorDict["White"],
        anchor = Anchors["MoonLVL"],
        halign = "center"
    )
  
def MakeBlankCard():
    image = PIL_Helper.BlankImage(base_w, base_h)
    
    PIL_Helper.AddText(
        image = image,
        text = "This Card Intentionally Left Blank",
        font = fonts["Name"],
        fill = ColorDict["Black"],
        anchor = Anchors["Name"],
        max_width = textmaxwidth
    )
    return image

def SkillsText(image, tags):
    PIL_Helper.AddText(
        image = image,
        text = tags.skills,
        font = fonts["Text"],
        fill = ColorDict["Black"],
        anchor = Anchors["Skills"],
        halign = "center",
        valign = "center",
        max_width = skillsmaxwidth
    )

def PageText(image, tags):
    PIL_Helper.AddText(
        image = image,
        text = tags.page,
        font = fonts["TextSmall"],
        fill = ColorDict["White"],
        anchor = Anchors["Page"],
        halign = "right",
        valign = "center"
    )

def VersionText(image):
    PIL_Helper.AddText(
        image = image,
        text = VERSION,
        font = fonts["TextTiny"],
        fill = ColorDict["White"],
        anchor = Anchors["Version"],
        halign = "right",
    )

def MakeBeastCard(tags):
    image = GetFrame("BEAST")
    TitleText(image, tags.name)
    CrText(image, tags.cr)
    StatText(image, tags)
    SpeedText(image, tags)
    ActionsText(image, tags)
    QuickRef(image, tags)
    Levels(image, tags.cr, tags)
    SkillsText(image, tags)
    PageText(image, tags)
    VersionText(image)
    return image

def MakeBeastBack(tags):
    image = GetFrame("BACK")
    TitleText(image, tags.name)
    Abilities = tags.abilities.replace(r"\n","\n")
    font = fonts["Text"]
    width,height = PIL_Helper.GetTextBlockSize(Abilities, font, max_width = textmaxwidth)
    if height > 600:
        font = fonts["TextMedium"]
    if height > 600:
        font = fonts["TextSmall"]
    PIL_Helper.AddText(
        image = image,
        text = Abilities,
        font = font,
        fill = ColorDict["Black"],
        anchor = Anchors["Abilities"],
        halign = "left",
        max_width = textmaxwidth
    )
    return image

if __name__ == "__main__":
    text = ["Genan Wolf Hound",
            "0",
            "+0",
            "+2",
            "+1",
            "5",
            "12",
            "-",
            "120",
            "-",
            "120",
            "-",
            "-",
            "120",
            "-",
            "Medium",
            "Bite: +3 to hit, 1d6 Piercing\nOn a hit, the target is Poisoned.",
            "Keen Hearing\nThe Genan Wolf Hound gains advantage on Perception checks relating to Smell.",
            "Perception +4"
            ]
    im, filename = BuildCard(text)
    im.save("card.png")
    im.show()
