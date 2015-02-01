import os, glob, shutil, traceback
import PIL_Helper

TYPE, TITLE, COLOR, VALUE, FLAVOR = range(5)
DIRECTORY = "BaBOC"

PAGE_WIDTH = 3
PAGE_HEIGHT = 3
TOTAL_CARDS = PAGE_WIDTH*PAGE_HEIGHT

workspace_path = os.path.dirname("workspace")
card_set = os.path.dirname("deck.cards")


CardPath = "BaBOC/cards/"
ResourcePath = "BaBOC/resources/"
VassalTemplatesPath = DIRECTORY+"/vassal templates"
VassalWorkspacePath = DIRECTORY+"/vassal workspace"
VassalImagesPath = os.path.join(VassalWorkspacePath, "images")
VassalCard = [0]

bleed_w = 788
bleed_h = 1088
w_marg = 31
h_marg = 36
bleedrect=[(w_marg,h_marg),(bleed_w-w_marg,bleed_h-h_marg)]
textmaxwidth = 580
LineM=PIL_Helper.Image.open(ResourcePath+"line_M.png")
LineH=PIL_Helper.Image.open(ResourcePath+"line_H.png")
LineG=PIL_Helper.Image.open(ResourcePath+"line_G.png")
LineS=PIL_Helper.Image.open(ResourcePath+"line_S.png")
titlefont = ResourcePath+"ComicNeue-Regular.ttf"
titleboldfont = ResourcePath+"ComicNeue-Bold.ttf"
symbolfont = ResourcePath+"Eligible-Regular.ttf"
TitleFont = PIL_Helper.BuildFont(titleboldfont, 60)
SymbolFont = PIL_Helper.BuildFont(symbolfont, 150)
BigSymbolFont = PIL_Helper.BuildFont(symbolfont, 200)
ValueFont = PIL_Helper.BuildFont(symbolfont, 90)
RulesFont = PIL_Helper.BuildFont(titlefont, 50)
TypeFont = PIL_Helper.BuildFont(titleboldfont, 70)
GenreFont = PIL_Helper.BuildFont(titleboldfont,50)
FlavorFont = PIL_Helper.BuildFont("BaBOC/resources/KlinicSlabBookIt.otf", 40)
CopyFont = PIL_Helper.BuildFont("BaBOC/resources/Barth_Regular.ttf", 10)
TypeAnchor = (bleed_w/2+70, 50)
TitleAnchor = (80, 60)
FormTitleAnchor = (80, -60)
SymbolAnchor = (80, -100)
RulesAnchor = (bleed_w/2+70, 650)
OneLineAnchor = (bleed_w/2+70, 160)
TwoLineAnchor = (bleed_w/2+70, 220)
FlavorAnchor = (bleed_w/2+70, -30)
ColDict={
    "G": (225,200,225),
    "S": (225,255,225),
    "H": (255,225,225),
    "M": (225,225,255),
    "+": (225,225,225),
    "-": (225,225,225)
    }
ColDictDark={
    "G": (100,0,100),
    "S": (25,150,25),
    "H": (255,25,25),
    "M": (25,25,255),
    "+": (225,225,225),
    "-": (125,125,125)
    }
GenreDict={
    "G": "Grimdark",
    "S": "Sci-Fi",
    "H": "Hardcore",
    "M": "Magick"
    }
RulesDict={
    "FORM": "Counts as a Feature.\n+1 for every card matching your genre.",
    "FEATURE": "Play this card to your play area. You may attach Modifiers to this card.",
    "MODIFIER": "Play this card on your Form or any Features in your play area.",
    "FORM MODIFIER": "Counts as a Modifier but can be played ONLY on your own Form.",
    "SWITCH": "Change the sign of a card in your play area to {0}. Can be used as an Interrupt.",
    "GENRE CHANGE": "Change the genre of any card in your play area (even your Form). Can be used as an Interrupt."
    }



def BuildCard( linein):
    tags = linein.strip('\n').replace(r'\n', '\n').split('`')
    try:
        im = PickCardFunc(tags[TYPE], tags)
        MakeVassalCard(im)
    except Exception as e:
        im = MakeBlankCard()
        print "Warning, Bad Card: {0}".format(tags)
        traceback.print_exc()
    return im
def PickCardFunc( card_type, tags):
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
    elif tags[TYPE] == "GENRE CHANGE":
        return MakeGenreChangeCard(tags)
    elif tags[TYPE] == "BLANK":
        return MakeBlankCard()
    else:
        raise Exception("No card of type {0}".format(tags[TYPE]))
def DrawSidebar( image, color):
    PIL_Helper.DrawRect(image, 0, 0, 160, 1088, color)
def DrawLines(image,genres):
    for c in genres:
        if c=="G":
            image.paste(LineG,(0,660),LineG)
        if c=="S":
            image.paste(LineS,(0,720),LineS)
        if c=="M":
            image.paste(LineM,(0,800),LineM)
        if c=="H":
            image.paste(LineH,(0,880),LineH)
def TypeText( image, text):
    PIL_Helper.AddText(
        image = image,
        text = text,
        font = TypeFont,
        anchor = TypeAnchor
        )
def GenreText( image, text, color):
    PIL_Helper.AddText(
        image = image,
        text = text,
        font = GenreFont,
        fill = color,
        anchor = OneLineAnchor,
        valign = "top",
        halign = "center",
        )
def TitleText( image, text, color=(0, 0, 0)):
    print text
    PIL_Helper.AddText(
        image = image,
        text = text,
        font = TitleFont,
        fill = color,
        anchor = TitleAnchor,
        max_width = bleed_h-150,
        leading_offset = 0,
        rotate = 90
        )

def ValueText( image, text):
    PIL_Helper.AddText(
        image = image,
        text = text,
        font = ValueFont,
        anchor = (70,920)
        )
def SymbolText( image, text):
    font = BigSymbolFont if text == "-" else SymbolFont
    PIL_Helper.AddText(
        image = image,
        text = text,
        font = font,
        anchor = SymbolAnchor,
        valign = "center"
        )
def RulesText( image, text):
    PIL_Helper.AddText(
        image = image,
        text = text,
        font = RulesFont,
        anchor = RulesAnchor,
        max_width = textmaxwidth,
        leading_offset = 0
        )
def FlavorText( image, text):
    PIL_Helper.AddText(
        image = image,
        text = text,
        font = FlavorFont,
        anchor = FlavorAnchor,
        max_width = textmaxwidth,
        valign = "bottom"
        )
def MakeBlankCard():
    image = PIL_Helper.BlankImage(bleed_w, bleed_h)
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
    image = PIL_Helper.BlankImage(bleed_w, bleed_h,
                                  color=ColDict[tags[COLOR][0]]
                                  )
    TypeText(image, "Form")
    GenreText(image,
                   GenreDict[tags[COLOR][0]],
                   ColDictDark[tags[COLOR][0]]
                   )
    # Form sidebar type
    TitleText(image, "Form")
    
    # Form Title
    PIL_Helper.AddText(
        image = image,
        text = tags[TITLE],
        font = TitleFont,
        fill = (0,0,0),
        anchor = FormTitleAnchor,
        max_width = bleed_h,
        valign = "bottom",
        rotate = 90
        )
    
    RulesText(image, RulesDict["FORM"])
    if len(tags) > FLAVOR:
        FlavorText(image, tags[FLAVOR])
    #DrawLines(image,tags[COLOR])
    return image
def MakeFeatureCard( tags):
    image = PIL_Helper.BlankImage(bleed_w, bleed_h)
    DrawSidebar(image, ColDict[tags[COLOR][0]])
    DrawLines(image,tags[COLOR])
    TypeText(image, "Feature")
    GenreText(image,
                   GenreDict[tags[COLOR][0]],
                   ColDictDark[tags[COLOR][0]]
                   )
    TitleText(image, tags[TITLE])
    ValueText(image, tags[VALUE])
    RulesText(image, RulesDict["FEATURE"])
    if len(tags) > FLAVOR:
        FlavorText(image, tags[FLAVOR])
    return image
def MakeModifierCard( tags):
    image = PIL_Helper.BlankImage(bleed_w, bleed_h)
    DrawSidebar(image, ColDict[tags[COLOR][0]])
    DrawLines(image,tags[COLOR])
    TypeText(image, "Modifier")
    GenreText(image,
                   GenreDict[tags[COLOR][0]],
                   ColDictDark[tags[COLOR][0]]
                   )
    TitleText(image, tags[TITLE])
    ValueText(image, tags[VALUE])
    RulesText(image, RulesDict["MODIFIER"])
    if len(tags) > FLAVOR:
        FlavorText(image, tags[FLAVOR])
        
    return image
def MakeFormModifierCard( tags):
    image = PIL_Helper.BlankImage(bleed_w, bleed_h)
    DrawSidebar(image, ColDict[tags[COLOR][0]])
    DrawLines(image,tags[COLOR])
    TypeText(image, "Form Modifier")
    GenreText(image,
                   GenreDict[tags[COLOR][0]],
                   ColDictDark[tags[COLOR][0]]
                   )
    TitleText(image, tags[TITLE])
    ValueText(image, tags[VALUE])
    RulesText(image, RulesDict["FORM MODIFIER"])
    if len(tags) > FLAVOR:
        FlavorText(image, tags[FLAVOR])
    return image
def MakeSwitchCard( tags):
    image = PIL_Helper.BlankImage(bleed_w, bleed_h)
    DrawSidebar(image, ColDict[tags[COLOR][0]])
    DrawLines(image,tags[COLOR])
    TypeText(image, "Switch")
    TitleText(image, tags[TITLE])
    SymbolText(image, tags[COLOR][0])
    RulesText(image, RulesDict["SWITCH"].format(tags[COLOR][0]))
    if len(tags) > FLAVOR:
        FlavorText(image, tags[FLAVOR])
    return image
def MakeGenreChangeCard( tags):
    image = PIL_Helper.BlankImage(bleed_w, bleed_h)
    DrawLines(image,tags[COLOR])
    TypeText(image, "Genre Change")
    GenreText(image,
                   GenreDict[tags[COLOR][0]],
                   ColDictDark[tags[COLOR][0]]
                   )
    TitleText(image, tags[TITLE],
                   color=ColDictDark[tags[COLOR][0]]
                   )
    SymbolText(image, "<")
    RulesText(image, RulesDict["GENRE CHANGE"])
    if len(tags) > FLAVOR:
        FlavorText(image, tags[FLAVOR])
    return image

def BuildPage(card_list, page_num, page_width=PAGE_WIDTH, page_height=PAGE_HEIGHT):
    PIL_Helper.BuildPage(card_list, page_width, page_height,r"page_{0:>03}.png".format(page_num))

def InitVassalModule(): pass
def MakeVassalCard(im):
    VassalCard[0]+=1
    #BuildCard(line).save(VassalImagesPath + "/" + str(VassalCard) + ".png")
    im.save(VassalImagesPath + "\\" + str(VassalCard[0]) + ".png")
def CompileVassalModule(): pass

if __name__ == "__main__":
    print "Not a main module. Run GameGen.py"
