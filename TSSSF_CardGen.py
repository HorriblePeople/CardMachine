import os, glob, shutil, traceback, random
import PIL_Helper

TYPE, PICTURE, SYMBOLS, TITLE, KEYWORDS, BODY, FLAVOR, EXPANSION, CLIENT = range(9)
DIRECTORY = "TSSSF"
ARTIST = "Pixel Prism"

Expansion_Icon = None

LegacySymbolMode = False
PAGE_WIDTH = 3
PAGE_HEIGHT = 3
TOTAL_CARDS = PAGE_WIDTH * PAGE_HEIGHT

workspace_path = os.path.dirname("workspace")
card_set = os.path.dirname("deck.cards")
CardSet = os.path.dirname("deck.cards")
CardPath = DIRECTORY + "/Card Art/"
ResourcePath = DIRECTORY + "/resources/"
BleedsPath = DIRECTORY + "/bleed-images/"
CropPath = DIRECTORY + "/cropped-images/"
VassalPath = DIRECTORY + "/vassal-images/"

BleedTemplatesPath = ResourcePath + "/bleed templates/"
SymbolsPath = ResourcePath + "/symbols/"
ExpansionIconsPath = ResourcePath + "/expansion icons/"
CardBacksPath = ResourcePath + "/card backs/"
FontsPath = ResourcePath + "/fonts/"

VassalTemplatesPath = DIRECTORY + "/vassal templates/"
VassalWorkspacePath = DIRECTORY + "/vassal workspace/"
VassalImagesPath = os.path.join(VassalWorkspacePath, "images")
VASSAL_SCALE = (260, 359)

VassalCard = [0]
ART_WIDTH = 600
base_w = 889
base_h = 1215
base_w_center = base_w / 2
base_h_center = base_h / 2
w_marg = 31
h_marg = 36
baserect = [(w_marg, h_marg), (base_w - w_marg, base_h - h_marg)]
textmaxwidth = 689

croprect = (50, 63, 788 + 50, 1088 + 63)

TextHeightThresholds = [363, 378, 600]
TitleWidthThresholds = [50]  # This is in #characters, fix later plox
BarTextThreshold = [500]

fonts = {
    "Title": PIL_Helper.BuildFont(FontsPath + "TSSSFBartholomew-Bold.otf", 55),
    "TitleSmall": PIL_Helper.BuildFont(FontsPath + "TSSSFBartholomew-Bold.otf", 45),
    "Body": PIL_Helper.BuildFont(FontsPath + "TSSSFCabin-Medium.ttf", 35),
    "BodySmall": PIL_Helper.BuildFont(FontsPath + "TSSSFCabin-Medium.ttf", 35),
    "BodyChangeling": PIL_Helper.BuildFont(FontsPath + "TSSSFCabin-Medium.ttf", 31),
    "Bar": PIL_Helper.BuildFont(FontsPath + "TSSSFCabin-Medium.ttf", 38),
    "BarSmall": PIL_Helper.BuildFont(FontsPath + "TSSSFCabin-Medium.ttf", 35),
    "Flavortext": PIL_Helper.BuildFont(FontsPath + "KlinicSlabBookIt.otf", 28),
    "Copyright": PIL_Helper.BuildFont(FontsPath + "TSSSFCabin-Medium.ttf", 18)
}

Anchors = {
    "Blank": (base_w_center, 300),
    "PonyArt": (173, 225),
    "ShipArt": (173, 226),
    "GoalArt": (174, 224),
    "Symbol1": (58 + 50, 56 + 63),
    "Symbol2": (58 + 50, 160 + 63),
    "LoneSymbol": (108, 153),
    "TimelineSymbol": (58 + 50, 535 + 63),
    "GoalSymbol2": (108, 613),
    "Title": (-65 - 50, 160),
    "TitleTwoLine": (-65 - 50, 159),
    "TitleSmall": (-65 - 50, 157),
    "Bar": (-68 - 50, 598 + 67),
    "Body": (base_w_center, 735),
    "BodyShiftedUp": (base_w_center, 730),
    "Flavor": (base_w_center, -110),
    "Expansion": (640 + 50, 525 + 63),
    "Copyright": (-38 - 50, -13 - 61)
}

ArtMissing = [
    PIL_Helper.LoadImage(CardPath + "artmissing01.png"),
    PIL_Helper.LoadImage(CardPath + "artmissing02.png"),
    PIL_Helper.LoadImage(CardPath + "artmissing03.png"),
    PIL_Helper.LoadImage(CardPath + "artmissing04.png"),
    PIL_Helper.LoadImage(CardPath + "artmissing05.png"),
    PIL_Helper.LoadImage(CardPath + "artmissing06.png"),
    PIL_Helper.LoadImage(CardPath + "artmissing07.png"),
]

Frames = {
    "START": PIL_Helper.LoadImage(BleedTemplatesPath + "BLEED-Blank-Start-bleed.png"),
    "Warning": PIL_Helper.LoadImage(CardPath + "BLEED_Card - Warning.png"),
    "Pony": PIL_Helper.LoadImage(BleedTemplatesPath + "BLEED-Blank-Pony-bleed.png"),
    "Ship": PIL_Helper.LoadImage(BleedTemplatesPath + "BLEED-Blank-Ship-bleed.png"),
    "Rules1": PIL_Helper.LoadImage(CardPath + "BLEED_Rules1.png"),
    "Rules3": PIL_Helper.LoadImage(CardPath + "BLEED_Rules3.png"),
    "Rules5": PIL_Helper.LoadImage(CardPath + "BLEED_Rules5.png"),
    "Goal": PIL_Helper.LoadImage(BleedTemplatesPath + "BLEED-Blank-Goal-bleed.png"),
    "Derpy": PIL_Helper.LoadImage(CardPath + "BLEED_Card - Derpy Hooves.png"),
    "TestSubject": PIL_Helper.LoadImage(CardPath + "BLEED_Card - OverlayTest Subject Cheerilee.png")
}

Symbols = {
    "male": PIL_Helper.LoadImage(SymbolsPath + "Symbol-male.png"),
    "female": PIL_Helper.LoadImage(SymbolsPath + "Symbol-Female.png"),
    "malefemale": PIL_Helper.LoadImage(SymbolsPath + "Symbol-MaleFemale.png"),
    "earth pony": PIL_Helper.LoadImage(SymbolsPath + "Symbol-Earth-Pony.png"),
    "unicorn": PIL_Helper.LoadImage(SymbolsPath + "Symbol-Unicorn.png"),
    "uniearth": PIL_Helper.LoadImage(SymbolsPath + "symbol-uniearth.png"),
    "pegasus": PIL_Helper.LoadImage(SymbolsPath + "Symbol-Pegasus.png"),
    "alicorn": PIL_Helper.LoadImage(SymbolsPath + "Symbol-Alicorn.png"),
    "changelingearthpony": PIL_Helper.LoadImage(SymbolsPath + "Symbol-ChangelingEarthPony.png"),
    "changelingunicorn": PIL_Helper.LoadImage(SymbolsPath + "Symbol-ChangelingUnicorn.png"),
    "changelingpegasus": PIL_Helper.LoadImage(SymbolsPath + "Symbol-ChangelingPegasus.png"),
    "changelingalicorn": PIL_Helper.LoadImage(SymbolsPath + "Symbol-ChangelingAlicorn.png"),
    "dystopian": PIL_Helper.LoadImage(SymbolsPath + "symbol-dystopian-future.png"),
    "ship": PIL_Helper.LoadImage(SymbolsPath + "Symbol-Ship.png"),
    "goal": PIL_Helper.LoadImage(SymbolsPath + "Symbol-Goal.png"),
    "0": PIL_Helper.LoadImage(SymbolsPath + "symbol-0.png"),
    "1": PIL_Helper.LoadImage(SymbolsPath + "symbol-1.png"),
    "2": PIL_Helper.LoadImage(SymbolsPath + "symbol-2.png"),
    "3": PIL_Helper.LoadImage(SymbolsPath + "symbol-3.png"),
    "4": PIL_Helper.LoadImage(SymbolsPath + "symbol-4.png"),
    "3-4": PIL_Helper.LoadImage(SymbolsPath + "symbol-34.png"),
    "2-3": PIL_Helper.LoadImage(SymbolsPath + "symbol-23.png")
}
TIMELINE_SYMBOL_LIST = ["Dystopian"]

Expansions = {
    "Everfree14": PIL_Helper.LoadImage(ExpansionIconsPath + "symbol-Everfree14.png"),
    "Indiegogo": PIL_Helper.LoadImage(ExpansionIconsPath + "symbol-Indiegogo.png"),
    "Birthday": PIL_Helper.LoadImage(ExpansionIconsPath + "symbol-birthday.png"),
    "Bronycon": PIL_Helper.LoadImage(ExpansionIconsPath + "symbol-Bronycon14.png"),
    "Summer": PIL_Helper.LoadImage(ExpansionIconsPath + "symbol-summer-lovin.png"),
    "Apricity": PIL_Helper.LoadImage(ExpansionIconsPath + "symbol-apricity.png"),
    "BronyCAN": PIL_Helper.LoadImage(ExpansionIconsPath + "symbol-Bronycan14.png"),
    "Xtra": PIL_Helper.LoadImage(ExpansionIconsPath + "symbol-extracredit.png"),
    "Xtra-dark": PIL_Helper.LoadImage(ExpansionIconsPath + "symbol-extracredit-black.png"),
    "NMND": PIL_Helper.LoadImage(ExpansionIconsPath + "symbol-nightmarenights.png"),
    "Ciderfest": PIL_Helper.LoadImage(ExpansionIconsPath + "symbol-ponyvilleciderfest.png"),
    "Adventure": PIL_Helper.LoadImage(ExpansionIconsPath + "symbol-adventure.png"),
    "Custom": PIL_Helper.LoadImage(ExpansionIconsPath + "symbol-custom.png"),
    "Power": PIL_Helper.LoadImage(ExpansionIconsPath + "symbol-power.png"),
    "Multiplicity": PIL_Helper.LoadImage(ExpansionIconsPath + "symbol-multiplicity.png"),
    "Canon": PIL_Helper.LoadImage(ExpansionIconsPath + "symbol-canon.png"),
    "Dungeon": PIL_Helper.LoadImage(ExpansionIconsPath + "symbol-dungeon.png"),
    "50": PIL_Helper.LoadImage(ExpansionIconsPath + "symbol-50.png"),
    "2014": PIL_Helper.LoadImage(ExpansionIconsPath + "symbol-2014.png"),
    "Hearthswarming": PIL_Helper.LoadImage(ExpansionIconsPath + "symbol-hearthswarming.png"),
    "Ponycon 2015": PIL_Helper.LoadImage(ExpansionIconsPath + "symbol-ponynyc.png"),
    "Patreon": PIL_Helper.LoadImage(ExpansionIconsPath + "symbol-Patreon.png"),
    "Gameshow": PIL_Helper.LoadImage(ExpansionIconsPath + "symbol-gameshow.png"),
    "BABScon": PIL_Helper.LoadImage(ExpansionIconsPath + "symbol-BABScon.png")
}

ColorDict = {
    "START": (58, 50, 53),
    "START bar text": (237, 239, 239),
    "START flavor": (28, 20, 23),
    "Pony": (70, 44, 137),
    "Pony bar text": (234, 220, 236),
    "Pony flavor": (25, 2, 51),
    "Goal": (18, 57, 98),
    "Goal flavor": (7, 34, 62),
    "Shipwrecker": (8, 57, 98),
    "Shipwrecker flavor": (0, 34, 62),
    "Ship": (206, 27, 105),
    "Ship bar text": (234, 220, 236),
    "Ship flavor": (137, 22, 47),
    "Copyright": (255, 255, 255),
    "Blankfill": (200, 200, 200)
}

RulesDict = {
    "{replace}": "While this card is in your hand, you may discard a Pony card from the grid and play this card in its place. This power cannot be copied.",
    "{swap}": "You may swap 2 Pony cards on the shipping grid.",
    "{3swap}": "You may swap up to 3 Pony cards on the grid.",
    "{draw}": "You may draw 1 card from the Ship or Pony deck.",
    "{goal}": "You may discard 1 active Goal and draw 1 new Goal to replace it.",
    "{search}": "You may search the Ship or Pony discard pile for 1 card of your choice and put it into your hand. If it's still in your hand at the end of your turn, discard it.",
    "{copy}": "You may copy the power of any Pony card currently on the shipping grid, except for Changelings.",
    "{hermaphrodite}": "May count as either {male} or {female} for all Goals, Ships, and powers.",
    "{double pony}": "This card counts as 2 Ponies.",
    "{love poison}": "Instead of playing this Ship with a Pony card from your hand, or connecting two Pony cards already on the grid, you may take a Pony card from the shipping grid and reattach it elsewhere with this Ship. That card's power activates.",
    "{keyword change}": "When you attach this card to the grid, you may choose one Pony card attached to this Ship. Until the end of your turn, that Pony card gains one keyword of your choice, except for Pony names.",
    "{gender change}": "When you attach this card to the grid, you may choose one Pony card attached to this Ship. Until the end of your turn, that Pony card becomes the opposite gender.",
    "{race change}": "When you attach this card to the grid, you may choose one Pony card attached to this Ship. Until the end of your turn, that Pony card becomes the race of your choice. This cannot affect Changelings.",
    "{timeline change}": "When you attach this card to the grid, you may choose one Pony card attached to this Ship. Until the end of your turn, that Pony card's timeline becomes {postapocalypse}.",
    "{play from discard}": "You may choose to play the top card of the Pony discard pile with this Ship, rather than play a Pony card from your hand.",
    "{clone}": "When you attach this card to the grid, you may choose one Pony card attached to this Ship. Until the end of your turn, that Pony card counts as 2 Ponies.",
}

backs = {
    "START": PIL_Helper.LoadImage(CardBacksPath + "Back-Start.png"),
     "Pony": PIL_Helper.LoadImage(CardBacksPath + "Back-Main.png"),
     "Goal": PIL_Helper.LoadImage(CardBacksPath + "Back-Goals.png"),
     "Ship": PIL_Helper.LoadImage(CardBacksPath + "Back-Ships.png"),
     "Card": PIL_Helper.LoadImage(CardBacksPath + "Back-Main.png"),
     "Shipwrecker": PIL_Helper.LoadImage(CardBacksPath + "Back-Main.png"),
     "BLANK": PIL_Helper.LoadImage(CardBacksPath + "Blank - Intentionally Left Blank.png"),
     "Rules1": PIL_Helper.LoadImage(CardPath + "Rules2.png"),
     "Rules3": PIL_Helper.LoadImage(CardPath + "Rules4.png"),
     "Rules5": PIL_Helper.LoadImage(CardPath + "Rules6.png"),
     "TestSubject": PIL_Helper.LoadImage(CardBacksPath + "Back-Main.png"),
     "Warning": PIL_Helper.LoadImage(CardPath + "Card - Contact.png")
}

special_card_types = ["Rules1", "Rules3", "Rules5", "Warning", "Derpy", "Card"]
special_cards_with_copyright = ["Derpy"]


def FixFileName(tagin):
    FileName = tagin.replace("\n", "")
    invalid_chars = [",", "?", '"', ":"]
    for c in invalid_chars:
        FileName = FileName.replace(c, "")
    FileName = u"{0}.png".format(FileName)
    return FileName


def FixUnicode(text):
    text = text.replace(r'\n', '\n')
    if LegacySymbolMode:
        text = text.replace(';', u"\u2642")
        text = text.replace('*', u"\u2640")
        text = text.replace('>', u"\u26A4")
        text = text.replace('<', u"\u2764")
        text = text.replace('%', u"\uE000")
        text = text.replace('8', u"\uE001")
        text = text.replace('9', u"\uE002")
        text = text.replace('@', u"\uE003")
        text = text.replace('$', u"\uE004")
    else:
        text = text.replace('{male}', u"\u2642")
        text = text.replace('{female}', u"\u2640")
        text = text.replace('{malefemale}', u"\u26A4")
        text = text.replace('{ship}', u"\u2764")
        text = text.replace('{earthpony}', u"\uE000")
        text = text.replace('{unicorn}', u"\uE001")
        text = text.replace('{pegasus}', u"\uE002")
        text = text.replace('{alicorn}', u"\uE003")
        text = text.replace('{postapocalypse}', u"\uE004")
    return text


def SaveCard(filepath, image_to_save):
    '''
    If the filepath already exists, insert _001 just before the
    extension. If that exists, increment the number until we get to
    a filepath that doesn't exist yet.
    '''
    if os.path.exists(filepath):
        basepath, extension = os.path.splitext(filepath)
        i = 0
        while os.path.exists(filepath):
            i += 1
            filepath = "{}_{:>03}{}".format(basepath, i, extension)
    image_to_save.save(filepath, dpi=(300, 300))


def BuildCard(data):
    picture = None
    title = None

    if type(data).__name__ == 'dict':
        card = data
        card_type = data['type']
        picture = data.get('picture', None)
        title = data.get('title', None)
    else:
        card = data.strip('\n').strip('\r').replace(r'\n', '\n').split('`')
        card_type = card[TYPE]
        if len(card) >= 2:
            picture = card[PICTURE]
        if len(card) > 2:
            title = card[TITLE]

    try:
        im = PickCardFunc(card_type, card)
        if picture is not None:
            if title is not None:
                filename = FixFileName(card_type + "_" + title)
            else:
                filename = FixFileName(card_type + "_" + picture)
            SaveCard(os.path.join(BleedsPath, filename), im)
            im_crop = im.crop(croprect)
            SaveCard(os.path.join(CropPath, filename), im_crop)
            im_vassal = PIL_Helper.ResizeImage(im_crop, VASSAL_SCALE)
            SaveCard(os.path.join(VassalPath, filename), im_vassal)
        else:
            im_crop = im.crop(croprect)

    except Exception as e:
        print "Warning, Bad Card: {0}".format(data)
        traceback.print_exc()
        im_crop = MakeBlankCard().crop(croprect)
    return im_crop


def BuildBack(data):
    if type(data).__name__ == 'dict':
        card_type = data['type']
    else:
        card = data.strip('\n').strip('\r').replace(r'\n', '\n').split('`')
        card_type = card[TYPE]

    return backs[card_type]


def PickCardFunc(card_type, data):
    if card_type == "START":
        return MakeStartCard(data)
    elif card_type == "Pony":
        return MakePonyCard(data)
    elif card_type == "Ship":
        return MakeShipCard(data)
    elif card_type == "Goal":
        return MakeGoalCard(data)
    elif card_type == "BLANK":
        return MakeBlankCard()
    elif card_type == "TestSubject":
        return MakePonyCard(data)
    elif card_type in special_card_types:
        return MakeSpecialCard(data)
    else:
        raise Exception("No card of type {0}".format(card_type))


def GetFrame(card_type):
    return Frames[card_type].copy()


def AddCardArt(image, filename, anchor):
    if filename == "NOART":
        return
    if os.path.exists(os.path.join(CardPath, filename)):
        art = PIL_Helper.LoadImage(os.path.join(CardPath, filename))
    else:
        art = random.choice(ArtMissing)
    # Find desired height of image based on width of 600 px
    w, h = art.size
    h = int((float(ART_WIDTH) / w) * h)
    # Resize image to fit in frame
    art = PIL_Helper.ResizeImage(art, (ART_WIDTH, h))
    image.paste(art, anchor)


def AddSymbols(image, symbols, card_type=""):
    # Remove any timeline symbols from the symbols list
    pruned_symbols = set(symbols) - set(TIMELINE_SYMBOL_LIST)
    if card_type == "Goal":
        positions = [Anchors["LoneSymbol"], Anchors["GoalSymbol2"]]
    else:
        # If there's only one non-timeline symbol in the list,
        # Set it right on the corner of the picture.
        # Otherwise, adjust so the symbols share the space
        if len(pruned_symbols) == 1:
            positions = [Anchors["LoneSymbol"]]
        else:
            positions = [Anchors["Symbol1"], Anchors["Symbol2"]]

    for index, s in enumerate(symbols):
        sym = Symbols.get(s.lower(), None)
        if sym:
            if s in TIMELINE_SYMBOL_LIST:
                image.paste(sym, Anchors["TimelineSymbol"], sym)
            else:
                image.paste(sym, positions[index], sym)


def TitleText(image, text, color):
    font = fonts["Title"]
    anchor = Anchors["Title"]
    leading = -9
    if text.count('\n') > 0:
        anchor = Anchors["TitleTwoLine"]
        leading = -15
    if len(text) > TitleWidthThresholds[0]:
        anchor = Anchors["TitleSmall"]
        font = fonts["TitleSmall"]
    print repr(text)
    PIL_Helper.AddText(
        image=image,
        text=text,
        font=font,
        fill=color,
        anchor=anchor,
        valign="center",
        halign="right",
        leading_offset=leading
    )


def BarText(image, text, color):
    bar_text_size = PIL_Helper.GetTextBlockSize(text, fonts["Bar"], textmaxwidth)
    if bar_text_size[0] > BarTextThreshold[0]:
        font = fonts["BarSmall"]
    else:
        font = fonts["Bar"]
    PIL_Helper.AddText(
        image=image,
        text=text,
        font=font,
        fill=color,
        anchor=Anchors["Bar"],
        halign="right"
    )


def BodyText(image, text, color, flavor_text_size=0, font=None):
    # Replacement of keywords with symbols
    for keyword in RulesDict:
        if keyword in text:
            text = text.replace(keyword, RulesDict[keyword])
    text = FixUnicode(text)
    if font is None:
        font = fonts["Body"]
    anchor = Anchors["Body"]
    leading = -1
    # Get the size of the body text as (w,h)
    body_text_size = PIL_Helper.GetTextBlockSize(
        text, fonts["Body"], textmaxwidth
    )
    # If the height of the body text plus the height of the flavor text
    # doesn't fit in on the card in the normal position, move the body text up
    if body_text_size[1] + flavor_text_size[1] > TextHeightThresholds[0]:
        anchor = Anchors["BodyShiftedUp"]
    # If they still don't fit, makes the body text smaller
    if body_text_size[1] + flavor_text_size[1] > TextHeightThresholds[1]:
        font = fonts["BodySmall"]
        body_text_size = PIL_Helper.GetTextBlockSize(
            text, font, textmaxwidth
        )
        # If they still don't fit, make it smaller again. They're probably
        # the changeling cards
        if body_text_size[1] + flavor_text_size[1] > TextHeightThresholds[1]:
            font = fonts["BodyChangeling"]
            leading = -3
    Anchors["BodyShiftedUp"]
    PIL_Helper.AddText(
        image=image,
        text=text,
        font=font,
        fill=color,
        anchor=anchor,
        halign="center",
        max_width=textmaxwidth,
        leading_offset=leading
    )


def FlavorText(image, text, color):
    return PIL_Helper.AddText(
        image=image,
        text=text,
        font=fonts["Flavortext"],
        fill=color,
        anchor=Anchors["Flavor"],
        valign="bottom",
        halign="center",
        leading_offset=+1,
        max_width=textmaxwidth,
    )


def GetExpansionIcon(expansion):
    return PIL_Helper.LoadImage(ExpansionIconsPath + expansion)


def AddExpansion(image, expansion):
    expansion_symbol = Expansions.get(expansion, None)
    if expansion_symbol:
        image.paste(expansion_symbol, Anchors["Expansion"], expansion_symbol)


def AddExpansionJSON(image, expansion_symbol):
    if expansion_symbol:
        image.paste(expansion_symbol, Anchors["Expansion"], expansion_symbol)


def CopyrightText(card, image, color, artist):
    card_set = CardSet.replace('_', ' ')
    client = None

    if type(card).__name__ == 'dict':
        client = card.get('client')
    else:
        if len(card) - 1 >= CLIENT:
            client = str(card[CLIENT])

    if client is not None:
        card_set += " " + client
    text = "{}; TSSSF by Horrible People Games. Art by {}.".format(
        card_set,
        artist
    )
    PIL_Helper.AddText(
        image=image,
        text=text,
        font=fonts["Copyright"],
        fill=color,
        anchor=Anchors["Copyright"],
        valign="bottom",
        halign="right",
    )


def MakeBlankCard():
    image = PIL_Helper.BlankImage(base_w, base_h)

    PIL_Helper.AddText(
        image=image,
        text="This Card Intentionally Left Blank",
        font=fonts["Title"],
        fill=ColorDict["Blankfill"],
        anchor=Anchors["Blank"],
        max_width=textmaxwidth
    )
    return image


def MakeStartCard(card):
    if type(card).__name__ == 'dict':
        return MakeStartCardJSON(card)
    else:
        return MakeStartCardPON(card)


def MakeStartCardJSON(data):
    image = GetFrame(data['type'])
    AddCardArt(image, data['picture'], Anchors["PonyArt"])
    TitleText(image, data['title'], ColorDict["START"])
    AddSymbols(image, data.get('symbols', []))
    BarText(image, ', '.join(data.get('keywords', [])), ColorDict["START bar text"])
    text_size = FlavorText(image, data.get('flavor', ''), ColorDict["START flavor"])
    BodyText(image, data.get('body', ''), ColorDict["START"], text_size)
    CopyrightText(data, image, ColorDict["Copyright"], data.get('artist', ARTIST))
    if Expansion_Icon is not None:
        AddExpansionJSON(image, Expansion_Icon)
    return image


def MakeStartCardPON(tags):
    image = GetFrame(tags[TYPE])
    AddCardArt(image, tags[PICTURE], Anchors["PonyArt"])
    TitleText(image, tags[TITLE], ColorDict["START"])
    AddSymbols(image, tags[SYMBOLS].split('!'))
    BarText(image, tags[KEYWORDS], ColorDict["START bar text"])
    text_size = FlavorText(image, tags[FLAVOR], ColorDict["START flavor"])
    BodyText(image, tags[BODY], ColorDict["START"], text_size)
    CopyrightText(tags, image, ColorDict["Copyright"], ARTIST)
    if len(tags) > EXPANSION:
        AddExpansion(image, tags[EXPANSION])
    return image


def MakePonyCard(card):
    if type(card).__name__ == 'dict':
        return MakePonyCardJSON(card)
    else:
        return MakePonyCardPON(card)


def MakePonyCardJSON(data):
    image = GetFrame(data['type'])
    AddCardArt(image, data['picture'], Anchors["PonyArt"])
    TitleText(image, data['title'], ColorDict["Pony"])
    AddSymbols(image, data.get('symbols', []))
    BarText(image, ', '.join(data.get('keywords', [])), ColorDict["Pony bar text"])
    text_size = FlavorText(image, data.get('flavor', ''), ColorDict["Pony flavor"])
    BodyText(image, data.get('body', ''), ColorDict["Pony"], text_size)
    CopyrightText(data, image, ColorDict["Copyright"], data.get('artist', ARTIST))
    if Expansion_Icon is not None:
        AddExpansionJSON(image, Expansion_Icon)
    return image


def MakePonyCardPON(tags):
    image = GetFrame(tags[TYPE])
    AddCardArt(image, tags[PICTURE], Anchors["PonyArt"])
    TitleText(image, tags[TITLE], ColorDict["Pony"])
    AddSymbols(image, tags[SYMBOLS].split('!'))
    BarText(image, tags[KEYWORDS], ColorDict["Pony bar text"])
    text_size = FlavorText(image, tags[FLAVOR], ColorDict["Pony flavor"])
    BodyText(image, tags[BODY], ColorDict["Pony"], text_size)
    CopyrightText(tags, image, ColorDict["Copyright"], ARTIST)
    if len(tags) > EXPANSION:
        AddExpansion(image, tags[EXPANSION])
    return image


def MakeShipCard(card):
    if type(card).__name__ == 'dict':
        return MakeShipCardJSON(card)
    else:
        return MakeShipCardPON(card)


def MakeShipCardJSON(data):
    image = GetFrame(data['type'])
    AddCardArt(image, data['picture'], Anchors["ShipArt"])
    TitleText(image, data['title'], ColorDict["Ship"])
    AddSymbols(image, data.get('symbols', []), "Ship")
    BarText(image, ', '.join(data.get('keywords', [])), ColorDict["Ship bar text"])
    text_size = FlavorText(image, data.get('flavor', ''), ColorDict["Ship flavor"])
    BodyText(image, data.get('body', ''), ColorDict["Ship"], text_size)
    CopyrightText(data, image, ColorDict["Copyright"], data.get('artist', ARTIST))
    if Expansion_Icon is not None:
        AddExpansionJSON(image, Expansion_Icon)
    return image


def MakeShipCardPON(tags):
    image = GetFrame(tags[TYPE])
    AddCardArt(image, tags[PICTURE], Anchors["ShipArt"])
    TitleText(image, tags[TITLE], ColorDict["Ship"])
    AddSymbols(image, tags[SYMBOLS].split('!'), "Ship")
    BarText(image, tags[KEYWORDS], ColorDict["Ship bar text"])
    text_size = FlavorText(image, tags[FLAVOR], ColorDict["Ship flavor"])
    BodyText(image, tags[BODY], ColorDict["Ship"], text_size)
    CopyrightText(tags, image, ColorDict["Copyright"], ARTIST)
    if len(tags) > EXPANSION:
        AddExpansion(image, tags[EXPANSION])
    return image


def MakeGoalCard(card):
    if type(card).__name__ == 'dict':
        return MakeGoalCardJSON(card)
    else:
        return MakeGoalCardPON(card)


def MakeGoalCardJSON(data):
    image = GetFrame(data['type'])
    AddCardArt(image, data['picture'], Anchors["GoalArt"])
    TitleText(image, data['title'], ColorDict["Goal"])
    AddSymbols(image, data.get('symbols', []), card_type="Goal")
    text_size = FlavorText(image, data.get('flavor', ''), ColorDict["Goal flavor"])
    BodyText(image, data.get('body', ''), ColorDict["Goal"], text_size)
    CopyrightText(data, image, ColorDict["Copyright"], data.get('artist', ARTIST))
    if Expansion_Icon is not None:
        AddExpansionJSON(image, Expansion_Icon)
    return image


def MakeGoalCardPON(tags):
    image = GetFrame(tags[TYPE])
    AddCardArt(image, tags[PICTURE], Anchors["GoalArt"])
    TitleText(image, tags[TITLE], ColorDict["Goal"])
    AddSymbols(image, tags[SYMBOLS].split('!'), card_type="Goal")
    text_size = FlavorText(image, tags[FLAVOR], ColorDict["Goal flavor"])
    BodyText(image, tags[BODY], ColorDict["Goal"], text_size)
    CopyrightText(tags, image, ColorDict["Copyright"], ARTIST)
    if len(tags) > EXPANSION:
        AddExpansion(image, tags[EXPANSION])
    return image


def MakeSpecialCard(card):
    if type(card).__name__ == 'dict':
        return MakeSpecialCardJSON(card)
    else:
        return MakeSpecialCardPON(card)


def MakeSpecialCardJSON(data):
    print repr(data['picture'])
    image = GetFrame(data['picture'])
    if data['picture'] in special_cards_with_copyright:
        CopyrightText(data, image, ColorDict["Copyright"], data.get('artist', ARTIST))
    if Expansion_Icon is not None:
        AddExpansionJSON(image, Expansion_Icon)
    return image


def MakeSpecialCardPON(data):
    print repr(data[PICTURE])
    image = GetFrame(data[PICTURE])
    if data[PICTURE] in special_cards_with_copyright:
        CopyrightText(data, image, ColorDict["Copyright"], ARTIST)
    if len(data) > EXPANSION:
        AddExpansion(image, data[EXPANSION])
    return image


def InitVassalModule():
    pass


def MakeVassalCard(im):
    VassalCard[0] += 1
    im.save(VassalImagesPath + "/" + str(VassalCard[0]) + ".png")


def CompileVassalModule():
    pass


if __name__ == "__main__":
    print "Not a main module. Run GameGen.py"
