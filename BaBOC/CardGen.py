import os, glob, shutil, traceback
import random
import PIL_Helper

TYPE, TITLE, COLOR, VALUE, FLAVOR, ARTWORK = range(6)
DIRECTORY = "BaBOC"

PAGE_WIDTH = 3
PAGE_HEIGHT = 3
TOTAL_CARDS = PAGE_WIDTH*PAGE_HEIGHT

workspace_path = os.path.dirname("workspace")
card_set = os.path.dirname("deck.cards")


CardPath = "BaBOC/cards/"
CardArtPath = "BaBOC/cardart/"
ResourcePath = "BaBOC/resources/"
VassalTemplatesPath = DIRECTORY+"/vassal templates"
VassalWorkspacePath = DIRECTORY+"/vassal workspace"
VassalImagesPath = os.path.join(VassalWorkspacePath, "images")
VassalCard = [0]

width = 788
height = 1088
width_center = width/2
height_center = height/2
w_marg = 31
h_marg = 36
bleedrect=[(w_marg,h_marg),(width-w_marg,height-h_marg)]
textmaxwidth = 580
#LineM=PIL_Helper.Image.open(ResourcePath+"line_M.png")
#LineH=PIL_Helper.Image.open(ResourcePath+"line_H.png")
#LineG=PIL_Helper.Image.open(ResourcePath+"line_G.png")
#LineS=PIL_Helper.Image.open(ResourcePath+"line_S.png")
titlefont = ResourcePath+"Eligible-Regular.ttf"
titleboldfont = ResourcePath+"Eligible-Bold.ttf"
symbolfont = ResourcePath+"Eligible-Regular.ttf"
TitleFont = PIL_Helper.BuildFont(titleboldfont, 55)
TitleFontSnug = PIL_Helper.BuildFont(titleboldfont, 50)
SymbolFont = PIL_Helper.BuildFont(symbolfont, 150)
BigSymbolFont = PIL_Helper.BuildFont(symbolfont, 200)
BigFont = PIL_Helper.BuildFont(symbolfont, 200)
BiggishFont = PIL_Helper.BuildFont(symbolfont, 80)
ValueFont = PIL_Helper.BuildFont(symbolfont, 90)
RulesFont = PIL_Helper.BuildFont(titlefont, 30)
TypeFont = PIL_Helper.BuildFont(titleboldfont, 70)
GenreFont = PIL_Helper.BuildFont(titleboldfont,50)
FlavorFont = PIL_Helper.BuildFont("BaBOC/resources/KlinicSlabBookIt.otf", 40)
CopyFont = PIL_Helper.BuildFont("BaBOC/resources/Barth_Regular.ttf", 10)
TypeAnchor = (50, 520)
TitleAnchor = (120, 40)
FormTitleAnchor = (40, -60)
SymbolAnchor = (80, -100)
RulesAnchor = (width_center+70, 950)
OneLineAnchor = (width_center+70, 160)
TwoLineAnchor = (width_center+70, 220)
FlavorAnchor = (width_center+70, -30)

ColDict={
    "G": (225,200,225),
    "S": (225,255,225),
    "H": (255,225,225),
    "M": (225,225,255),
    "A": (225,225,225),
    "": (225,225,225),
    "+": (225,225,225),
    "-": (225,225,225)
    }

ColDictDark={
    "G": (100,0,100),
    "S": (25,150,25),
    "H": (255,25,25),
    "M": (25,25,255),
    "A": (100,100,100),
    "": (225,225,225),
    "+": (225,225,225),
    "-": (125,125,125)
    }

GenreDict={
    "G": "Grimdark",
    "S": "Sci-Fi",
    "H": "Hardcore",
    "A": "None",
    "": "None",
    "M": "Magick"
    }

GenreImages={
     "G": "Frame_GrimdarkY.png",
    "S": "Frame_SciFiY.png",
    "H": "Frame_HardcoreY.png",
    "A": "Frame_NoneY.png",
    "": "Frame_NoneY.png",
    "M": "Frame_MagicY.png"   
}

GenreIcons={
     "G": "Symbol_Grimdark.png",
    "S": "Symbol_SciFi.png",
    "H": "Symbol_Hardcore.png",
    "A": "Symbol_None.png",
    "": "Symbol_None.png",
    "M": "Symbol_Magic.png"   
}

PlotTwistImages={
     "G": "Frame_PlotTwist_GrimdarkY.png",
    "S": "Frame_PlotTwist_SciFiY.png",
    "H": "Frame_PlotTwist_HardcoreY.png",
    "A": "Frame_PlotTwist_NoneY.png",
    "": "Frame_PlotTwist_NoneY.png",
    "M": "Frame_PlotTwist_MagicY.png"     
}

FandomBackdrops={
    "GH": "Fandom_GrimdarkHardcore.png",
    "GM": "Fandom_GrimdarkMagic.png",
    "GS": "Fandom_GrimdarkSci.png",
    "HG": "Fandom_HardcoreGrimdark.png",
    "HM": "Fandom_HardcoreMagic.png",
    "HS": "Fandom_HardcoreSci.png",
    "MG": "Fandom_MagicGrimdark.png",
    "MH": "Fandom_MagicHardcore.png",
    "MS": "Fandom_MagicSci.png",
    "SG": "Fandom_SciGrimdark.png",
    "SH": "Fandom_SciHardcore.png",
    "SM": "Fandom_SciMagic.png"
}

SnowflakeIcons={
    "": "Symbol_None.png",
    "0": "Symbol_None.png",
    "1": "1-Point.png",
    "2": "2-Points.png",
    "3": "3-Points.png",
    "4": "4-Points.png" 
}

BacksImages={
    "FANDOM": "bleed_backA2.png",
    "FORM": "bleed_backA1.png",
    "FEATURE": "bleed_back.png",
    "MODIFIER": "bleed_back.png",
    "FORM MODIFIER": "bleed_back.png",
    "SWITCH": "bleed_back.png",
    "GENRE CHANGE": "bleed_back.png"
}

ArtMissing=["artmissing00.png","artmissing01.png","artmissing02.png"]

RulesDict={
    "FORM": "Counts as a Feature.\n+1 for every card matching your genre.",
    "FEATURE": "Play this card to your play area. You may attach Modifiers to this card.",
    "MODIFIER": "Play this card on your Form or any Features in your play area.",
    "FORM MODIFIER": "Counts as a Modifier but can be played ONLY on your own Form.",
    "SWITCH": "Change the sign of a card to {0}. Can be used as an Interrupt.",
    "GENRE CHANGE": "You may use this card to initiate an Argument for a Trait on top of any stack."
    }

def BuildCard(linein,filename=None):
    tags = linein.strip('\n').replace(r'\n', '\n').split('`')
    try:
        im = PickCardFunc(tags[TYPE], tags)
        MakeVassalCard(im)
    except Exception as e:
        im = MakeBlankCard()
        print "Warning, Bad Card: {0}".format(tags)
        traceback.print_exc()
    return im

def BuildBack(linein):
    #image = PIL_Helper.LoadImage(ResourcePath + "bleed_back.png")
    tags = linein.strip('\n').replace(r'\n', '\n').split('`')
    image = PIL_Helper.LoadImage(ResourcePath + BacksImages[tags[TYPE]])
    #image = PIL_Helper.BlankImage(width, height)
    return image

def PickCardFunc(card_type, tags):
    if tags[TYPE] == "FORM":
        return MakeFormCard(tags)
    elif tags[TYPE] == "FEATURE":
        return MakeFeatureCard(tags)
    elif tags[TYPE] == "MODIFIER":
        return MakeModifierCard(tags)
    elif tags[TYPE] == "FORM MODIFIER":
        return MakeFormModifierCard(tags)
    elif tags[TYPE] == "SWITCH":
        return MakeSwitchCard(tags)
    elif tags[TYPE] == "FANDOM":
        return MakeFandomCard(tags)
    elif tags[TYPE] == "GENRE CHANGE":
        return MakeGenreChangeCard(tags)
    elif tags[TYPE] == "BLANK":
        return MakeBlankCard()
    else:
        raise Exception("No card of type '{0}'".format(tags[TYPE]))

def DrawSidebar(image, color):
    PIL_Helper.DrawRect(image, 0, 0, 160, 1088, color)
def DrawDoubleSidebar(image, color):
    PIL_Helper.DrawRect(image, width-160, 0, 160, 1088, color)
    PIL_Helper.DrawRect(image, width-160, 0, 160, 1088, color)

def DrawLines(image, genres):
    for c in genres:
        if c=="G":
            image.paste(LineG,(0,660),LineG)
        if c=="S":
            image.paste(LineS,(0,720),LineS)
        if c=="M":
            image.paste(LineM,(0,800),LineM)
        if c=="H":
            image.paste(LineH,(0,880),LineH)

def AddArt(image, filename, anchor, center=False):
    if filename == "NOART":
        return
    if os.path.isfile(filename):
        art = PIL_Helper.LoadImage(filename)
    else:
        art = PIL_Helper.LoadImage(CardArtPath+random.choice(ArtMissing))
    # Find desired height of image based on width of 600 px
    w, h = art.size
    if center:
        anchor=(anchor[0]-w/2,anchor[1])
    #h = int((float(ART_WIDTH)/w)*h)
    # Resize image to fit in frame
    art = PIL_Helper.ResizeImage(art, (w,h))
    image.paste(art, anchor,art)

def TypeText(image, text, nudge=0):
    PIL_Helper.AddText(
        image = image,
        text = text,
        font = BiggishFont,
        fill = (0,0,0),
        anchor = (width_center+100, 140+nudge),
        max_width = width/2,
        leading_offset = -60,
        valign = "center",
        rotate = 0
        )
# def TypeTextC(image, text):
#     PIL_Helper.AddText(
#         image = image,
#         text = text,
#         font = BiggishFont,
#         fill = (0,0,0),
#         anchor = (width_center, 160),
#         max_width = width-150,
#         leading_offset = -60,
#         valign = "center",
#         rotate = 0
#         )
def GenreText(image, text, color, nudge=0):
    PIL_Helper.AddText(
        image = image,
        text = text,
        font = GenreFont,
        fill = color,
        anchor = (width_center+100, 180+nudge),
        valign = "top",
        halign = "center",
        )

def TitleText(image, text, color=(0, 0, 0), nudge=0):
    print text
    PIL_Helper.AddText(
        image = image,
        text = text,
        font = TitleFont,
        fill = (255,255,255),
        anchor = (150,height-80),
        max_width = height-400,
        leading_offset = -37,
        valign = "bottom",
        halign = "center",
        justification = "left",
        rotate = 90
    )

def ValueText(image, text):
    PIL_Helper.AddText(
        image = image,
        text = text,
        font = ValueFont,
        anchor = (70,920)
        )

def SymbolText(image, text):
    font = BigSymbolFont if text == "-" else SymbolFont
    PIL_Helper.AddText(
        image = image,
        text = text,
        font = font,
        anchor = SymbolAnchor,
        valign = "center"
        )

def RulesText(image, text):
    '''Adds rules  text to the card'''
    PIL_Helper.AddText(
        image = image,
        text = text,
        font = RulesFont,
        anchor = (width/2+100, height*4/5),
        max_width = width*0.6,
        leading_offset = -20
        )


def RulesTextC(image, text):
    '''Adds rules  text to the card'''
    PIL_Helper.AddText(
        image = image,
        text = text,
        font = RulesFont,
        anchor = (width_center, 650),
        max_width = textmaxwidth,
        leading_offset = 0
        )


def FlavorText(image, text):
    '''Adds flavor text to the card'''
    PIL_Helper.AddText(
        image = image,
        text = text,
        font = FlavorFont,
        anchor = FlavorAnchor,
        max_width = textmaxwidth,
        valign = "bottom"
        )

def MakeBlankCard():
    image = PIL_Helper.BlankImage(width, height)
    print("Blank Card")
    PIL_Helper.AddText(
        image = image,
        text = "This Card Intentionally Left Blank",
        font = TitleFont,
        fill = (200,200,200),
        anchor = TypeAnchor,
        max_width = textmaxwidth
        )    
    return image

def MakeFormCard( tags):
    image = PIL_Helper.Image.open(ResourcePath+"Frame_FormY.png")
    TypeText(image, "Form")

    #ADD BACK LATER
    # AddArt(image,
    #     ResourcePath+tags[ARTWORK],
    #     (240,220)
    #     )


    # GenreText(image,
    #                GenreDict[tags[COLOR][0]],
    #                ColDictDark[tags[COLOR][0]]
    #                )
    TitleText(image, tags[TITLE])
#    RulesText(image, RulesDict["FEATURE"])
    if len(tags) > FLAVOR:
        FlavorText(image, tags[FLAVOR])
    return image

def MakeFandomCard( tags):
    image = PIL_Helper.Image.open(ResourcePath+FandomBackdrops[tags[COLOR]])
    #DrawLines(image, ('G','S','M','H'))
    # Add flavor text if it's in the list
    PIL_Helper.AddText(
        image = image,
        text = tags[1].split("/")[0],
        font = TitleFont,
        fill = (255,255,255),
        anchor = (width/2,height*1/5),
        max_width = width*4/5,
        leading_offset = -20,
        valign = "center",
        rotate = 0
        )
    PIL_Helper.AddText(
        image = image,
        text = tags[1].split("/")[1],
        font = TitleFont,
        fill = (255,255,255),
        anchor = (width/2,height*4/5),
        max_width = width*4/5,
        leading_offset = -20,
        valign = "center",
        rotate = 0
        )
    if len(tags) > FLAVOR:
        FlavorText(image, tags[FLAVOR])
    return image

def MakeFeatureCard( tags):
    image = PIL_Helper.Image.open(ResourcePath+GenreImages[tags[COLOR][0]])
    TypeText(image, "Feature")

    if tags[COLOR][0]=="A":
        NonGenreOffset=-130
    else:
        NonGenreOffset=0
    AddArt(image,
        ResourcePath+GenreIcons[tags[COLOR][0]],
        (78,70)
        )
    #ADD BACK LATER
    # AddArt(image,
    #     ResourcePath+tags[ARTWORK],
    #     (240,220)
    #     )
    AddArt(image,
        ResourcePath+SnowflakeIcons[tags[VALUE]],
        (156,230+NonGenreOffset),
        center=True
        )


    GenreText(image,
                   GenreDict[tags[COLOR][0]],
                   ColDictDark[tags[COLOR][0]]
                   )
    TitleText(image, tags[TITLE])
#    RulesText(image, RulesDict["FEATURE"])
    if len(tags) > FLAVOR:
        FlavorText(image, tags[FLAVOR])
    return image

def MakeModifierCard( tags):
    image = PIL_Helper.Image.open(ResourcePath+GenreImages[tags[COLOR][0]])
    TypeText(image, "Modifier")

    if tags[COLOR][0]=="A":
        NonGenreOffset=-130
    else:
        NonGenreOffset=0
    AddArt(image,
        ResourcePath+GenreIcons[tags[COLOR][0]],
        (78,70)
        )
    #ADD BACK LATER
    # AddArt(image,
    #     ResourcePath+tags[ARTWORK],
    #     (240,220)
    #     )
    AddArt(image,
        ResourcePath+SnowflakeIcons[tags[VALUE]],
        (156,230+NonGenreOffset),
        center=True
        )


    GenreText(image,
                   GenreDict[tags[COLOR][0]],
                   ColDictDark[tags[COLOR][0]]
                   )
    TitleText(image, tags[TITLE])
#    RulesText(image, RulesDict["MODIFIER"])
    if len(tags) > FLAVOR:
        FlavorText(image, tags[FLAVOR])
    return image

def MakeFormModifierCard( tags):
    image = PIL_Helper.Image.open(ResourcePath+GenreImages[tags[COLOR][0]])
    TypeText(image, "Form Modifier",nudge=20)
    
    if tags[COLOR][0]=="A":
        NonGenreOffset=-130
    else:
        NonGenreOffset=0
    AddArt(image,
        ResourcePath+GenreIcons[tags[COLOR][0]],
        (78,70)
        )
    #ADD BACK LATER
    # AddArt(image,
    #     ResourcePath+tags[ARTWORK],
    #     (240,220)
    #     )
    AddArt(image,
        ResourcePath+SnowflakeIcons[tags[VALUE]],
        (156,230+NonGenreOffset),
        center=True
        )

    GenreText(image,
                   GenreDict[tags[COLOR][0]],
                   ColDictDark[tags[COLOR][0]],nudge=50
                   )
    TitleText(image, tags[TITLE])
#    RulesText(image, RulesDict["FORM MODIFIER"])
    if len(tags) > FLAVOR:
        FlavorText(image, tags[FLAVOR])
    return image

def MakeSwitchCard( tags):
    #image = PIL_Helper.BlankImage(width, height)
    image = PIL_Helper.Image.open(ResourcePath+"Frame_BackstoryY.png")
    #DrawDoubleSidebar(image, (230,230,230))
    PIL_Helper.AddText(
        image = image,
        text = tags[1].split("/")[0],
        font = TitleFontSnug,
        fill = (255,255,255),
        anchor = (width-120,80),
        max_width = height-300,
        leading_offset = -30,
        valign = "top",
        halign = "center",
        justification = "left",
        rotate = 270
        )
    PIL_Helper.AddText(
        image = image,
        text = tags[1].split("/")[1],
        font = TitleFontSnug,
        fill = (255,255,255),
        anchor = (150,height-80),
        max_width = height-300,
        leading_offset = -30,
        valign = "bottom",
        halign = "center",
        justification = "left",
        rotate = 90
        )
    PIL_Helper.AddText(
        image = image,
        text = RulesDict["SWITCH"],
        font = RulesFont,
        fill = (0,0,0),
        anchor = (width/2+10,height*5/6),
        max_width = width*0.4,
        leading_offset = -20,
        valign = "center",
        rotate = 0
        )


     #DrawSidebar(image, ColDict[tags[COLOR][0]])
    #DrawLines(image,tags[COLOR])
    #TypeText(image, "Switch")
    #PMText = tags[TITLE].split("\\")
    #RulesText(image, tags[TITLE])
    #SymbolText(image, tags[COLOR][0])
    #RulesText(image, RulesDict["SWITCH"].format(tags[COLOR][0]))
    if len(tags) > FLAVOR:
        FlavorText(image, tags[FLAVOR])
    return image

def MakeGenreChangeCard( tags):
    image = PIL_Helper.Image.open(ResourcePath+PlotTwistImages[tags[COLOR][0]])
    #DrawLines(image,tags[COLOR])
    #TitleText(image, tags[TITLE])
    PIL_Helper.AddText(
        image = image,
        text = tags[TITLE],
        font = TitleFontSnug,
        fill = (255,255,255),
        anchor = (145,height-80),
        max_width = height-380,
        leading_offset = -30,
        valign = "bottom",
        halign = "center",
        justification = "left",
        rotate = 90
        )

    if tags[COLOR][0]=="A":
        NonGenreOffset=-130
    else:
        NonGenreOffset=0
    AddArt(image,
        ResourcePath+GenreIcons[tags[COLOR][0]],
        (78,74)
        )

    # AddArt(image,
    #     ResourcePath+SnowflakeIcons[tags[VALUE]],
    #     (156,230+NonGenreOffset),
    #     center=True
    #     )

    PIL_Helper.AddText(
        image = image,
        text = RulesDict["GENRE CHANGE"],
        font = RulesFont,
        fill = (255,255,255),
        anchor = (width/2+100,height*5/6),
        max_width = width*0.4,
        leading_offset = -20,
        valign = "center",
        rotate = 0
        )
    #RulesText(image, RulesDict["GENRE CHANGE"])
    if len(tags) > FLAVOR:
        FlavorText(image, tags[FLAVOR])
    return image

def BuildPage(card_list, page_num, page_width=PAGE_WIDTH, page_height=PAGE_HEIGHT):
    PIL_Helper.BuildPage(card_list, page_width, page_height,r"page_{0:>03}.png".format(page_num))

def InitVassalModule(): pass

def MakeVassalCard(im):
    VassalCard[0]+=1
    #BuildCard(line).save(VassalImagesPath + "/" + str(VassalCard) + ".png")
    #im.save(VassalImagesPath + "\\" + str(VassalCard[0]) + ".png")

def CompileVassalModule(): pass

if __name__ == "__main__":
    print "Not a main module. Run GameGen.py"
