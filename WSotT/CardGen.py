from PIL import Image, ImageFont, ImageDraw
import os, glob
from math import ceil
import ConfigParser

import PIL_Helper

class DeckConfiguration:
	def __init__(self, configfilename="deck.cfg"):
		Config = ConfigParser.ConfigParser()
		Config.read(configfilename)

		self.cardnum=0

		#Global Deck Settings
		settings = {}
		for option in Config.options("Deck"):
			settings[option]=Config.get("Deck", option)

		self.cardpath = settings["cardpath"]
		self.ResourcePath = settings["resourcepath"]

		self.bleed_w = int(settings["cardwidth"])
		self.bleed_h = int(settings["cardheight"])

		self.w_marg = int(settings["marginw"])
		self.h_marg = int(settings["marginh"])

		self.bleedrect=[(self.w_marg,self.h_marg),(self.bleed_w-self.w_marg,self.bleed_h-self.h_marg)]
		self.fullrect=[(0,0),(self.bleed_w,self.bleed_h)]

		self.textmaxwidth = int(settings["textmaxwidth"])
		self.chartextmaxwidth = int(settings["chartextmaxwidth"])

		self.TitleFont = ImageFont.truetype(settings["titlefont"],int(settings["titlefontsize"]))
		self.TypeFont = ImageFont.truetype(settings["typefont"],int(settings["typefontsize"]))
		self.CopyFont = ImageFont.truetype(settings["copyfont"],int(settings["copyfontsize"]))

		#Anchor Coordinates
		anchorsettings = {}
		for option in Config.options("Anchors"):
			anchorsettings[option]=Config.get("Anchors", option)
		self.TitleAnchor = (self.bleed_w/2,int(anchorsettings["titleanchory"]))
		self.FlavorTextAnchor = (self.bleed_w/2,int(anchorsettings["flavortextanchory"]))
		self.CopyTextAnchor = (self.bleed_w/2,int(anchorsettings["copytextanchory"]))

		self.Anchor1 = (int(anchorsettings["anchor1_x"]),int(anchorsettings["anchor1_y"]))
		self.Anchor2 = (int(anchorsettings["anchor2_x"]),int(anchorsettings["anchor2_y"]))
		self.Anchor3 = (int(anchorsettings["anchor3_x"]),int(anchorsettings["anchor3_y"]))
		self.Anchor4 = (int(anchorsettings["anchor4_x"]),int(anchorsettings["anchor4_y"]))

		self.ArtAnchor = (int(anchorsettings["artanchorx"]),int(anchorsettings["artanchory"]))

def SubAnchor(anchor=(0,0), offset=20):
	return (anchor[0],anchor[1]+offset)

def MakeBadCard(config, tags):
	image = Image.new("RGBA", (config.bleed_w, config.bleed_h))
	draw = ImageDraw.Draw(image)	

	draw.rectangle(config.fullrect,(255,255,255,255))
	PIL_Helper.AddText(image = image,
		text = "This Card Intentionally Left Blank",
		font = config.TitleFont,
		fill = (200,200,200),
		anchor = config.TitleAnchor,
		max_width = config.textmaxwidth)	

	return image

def MakeTableCard(config, tags):
	image = Image.new("RGBA", (config.bleed_w, config.bleed_h))
	draw = ImageDraw.Draw(image)

	bg_im = Image.open(config.ResourcePath + "tableclean_frontbg.png")
	image.paste(bg_im,(0,0))

	
	draw.rectangle(config.bleedrect,
		outline=(0,0,0,255))
	PIL_Helper.AddText(image = image,
		text = "TABLE",
		font = config.TitleFont,
		fill = (0,0,0),
		anchor = config.TitleAnchor,
		max_width = config.textmaxwidth)
	PIL_Helper.AddText(image = image,
		text = "(clean)",
		font = config.TypeFont,
		fill = (0,0,0),
		anchor = SubAnchor(config.TitleAnchor,70),
		max_width = config.textmaxwidth)
	return image



def MakeFoodCard(config, tags):
	image = Image.new("RGBA", (config.bleed_w, config.bleed_h))
	draw = ImageDraw.Draw(image)
	
	bg_im = Image.open(config.ResourcePath + "food_frontbg.png")
	image.paste(bg_im,(0,0))

	draw.rectangle(config.bleedrect,
		outline=(0,0,0,255))

	PIL_Helper.AddText(image = image,
		text = tags[1],
		font = config.TitleFont,
		fill = (0,0,0),
		anchor = config.TitleAnchor,
		max_width = config.textmaxwidth)
	PIL_Helper.AddText(image = image,
		text = "Food",
		font = config.TypeFont,
		fill = (0,0,0),
		anchor = SubAnchor(config.TitleAnchor,-35),
		max_width = config.textmaxwidth)
	PIL_Helper.AddText(image = image,
		text = "Filling:",
		font = config.TypeFont,
		fill = (0,0,0),
		anchor = config.Anchor3,
		max_width = 200)
	PIL_Helper.AddText(image = image,
		text = tags[2],
		font = config.TitleFont,
		fill = (0,0,0),
		anchor = SubAnchor(config.Anchor3,40),
		max_width = 200)
	PIL_Helper.AddText(image = image,
		text = tags[3].replace(r'\n', '\n'),
		font = config.TypeFont,
		fill = (0,0,0),
		anchor = config.FlavorTextAnchor,
		max_width = config.textmaxwidth)
	return image



def MakeCharacterCard(config, tags):
	image = Image.new("RGBA", (config.bleed_w, config.bleed_h))
	draw = ImageDraw.Draw(image)

	bg_im = Image.open(config.ResourcePath + "char_frontbg.png")
	image.paste(bg_im,(0,0))
	
	draw.rectangle(config.bleedrect,
		outline=(0,0,0,255))

	PIL_Helper.AddText(image = image,
		text = tags[1],
		font = config.TitleFont,
		fill = (0,0,0),
		anchor = config.TitleAnchor,
		max_width = config.chartextmaxwidth)
	PIL_Helper.AddText(image = image,
		text = "Character",
		font = config.TypeFont,
		fill = (0,0,0),
		anchor = SubAnchor(config.TitleAnchor,-35),
		max_width = config.textmaxwidth)
	PIL_Helper.AddText(image = image,
		text = "Base Tip:",
		font = config.TypeFont,
		fill = (0,0,0),
		anchor = config.Anchor1,
		max_width = 200)
	PIL_Helper.AddText(image = image,
		text = tags[2],
		font = config.TitleFont,
		fill = (0,0,0),
		anchor = SubAnchor(config.Anchor1,25),
		max_width = 200)
	PIL_Helper.AddText(image = image,
		text = "Apetite:",
		font = config.TypeFont,
		fill = (0,0,0),
		anchor = config.Anchor2,
		max_width = 200)
	PIL_Helper.AddText(image = image,
		text = tags[3],
		font = config.TitleFont,
		fill = (0,0,0),
		anchor = SubAnchor(config.Anchor2,25),
		max_width = 200)
	PIL_Helper.AddText(image = image,
		text = "Wrath:",
		font = config.TypeFont,
		fill = (0,0,0),
		anchor = config.Anchor3,
		max_width = 200)
	PIL_Helper.AddText(image = image,
		text = tags[4],
		font = config.TitleFont,
		fill = (0,0,0),
		anchor = SubAnchor(config.Anchor3,40),
		max_width = 200)
	PIL_Helper.AddText(image = image,
		text = tags[5].replace(r'\n', '\n'),
		font = config.TypeFont,
		fill = (0,0,0),
		anchor = config.FlavorTextAnchor,
		max_width = config.textmaxwidth)

	return image


def MakeEatCard(config, tags):
	image = Image.new("RGBA", (config.bleed_w, config.bleed_h))
	draw = ImageDraw.Draw(image)

	bg_im = Image.open(config.ResourcePath + "eat_frontbg.png")
	image.paste(bg_im,(0,0))

	
	draw.rectangle(config.bleedrect,
		outline=(0,0,0,255))

	PIL_Helper.AddText(image = image,
		text = tags[1],
		font = config.TitleFont,
		fill = (0,0,0),
		anchor = config.TitleAnchor,
		max_width = config.textmaxwidth)
	PIL_Helper.AddText(image = image,
		text = "Eating:",
		font = config.TypeFont,
		fill = (0,0,0),
		anchor = SubAnchor(config.TitleAnchor,-35),
		max_width = config.textmaxwidth)
	PIL_Helper.AddText(image = image,
		text = "Eaten:",
		font = config.TypeFont,
		fill = (0,0,0),
		anchor = config.Anchor3,
		max_width = 200)
	PIL_Helper.AddText(image = image,
		text = tags[2],
		font = config.TitleFont,
		fill = (0,0,0),
		anchor = SubAnchor(config.Anchor3,40),
		max_width = 200)
	PIL_Helper.AddText(image = image,
		text = tags[3].replace(r'\n', '\n'),
		font = config.TypeFont,
		fill = (0,0,0),
		anchor = config.FlavorTextAnchor,
		max_width = config.textmaxwidth)
	return image

def MakeWrathCard(config, tags):
	image = Image.new("RGBA", (config.bleed_w, config.bleed_h))
	draw = ImageDraw.Draw(image)

	bg_im = Image.open(config.ResourcePath + "eat_frontbg.png")
	image.paste(bg_im,(0,0))

	
	draw.rectangle(config.bleedrect,
		outline=(0,0,0,255))

	PIL_Helper.AddText(image = image,
		text = tags[1],
		font = config.TitleFont,
		fill = (0,0,0),
		anchor = config.TitleAnchor,
		max_width = config.textmaxwidth)
	PIL_Helper.AddText(image = image,
		text = "Wrath:",
		font = config.TypeFont,
		fill = (0,0,0),
		anchor = SubAnchor(config.TitleAnchor,-35),
		max_width = config.textmaxwidth)
	PIL_Helper.AddText(image = image,
		text = "Magnitude:",
		font = config.TypeFont,
		fill = (0,0,0),
		anchor = config.Anchor3,
		max_width = 200)
	PIL_Helper.AddText(image = image,
		text = tags[2],
		font = config.TitleFont,
		fill = (0,0,0),
		anchor = SubAnchor(config.Anchor3,40),
		max_width = 200)
	PIL_Helper.AddText(image = image,
		text = tags[3].replace(r'\n', '\n'),
		font = config.TypeFont,
		fill = (0,0,0),
		anchor = config.FlavorTextAnchor,
		max_width = config.textmaxwidth)
	return image

def MakePartyCard(config, tags):
	image = Image.new("RGBA", (config.bleed_w, config.bleed_h))
	draw = ImageDraw.Draw(image)
	
	bg_im = Image.open(config.ResourcePath + "party_frontbg.png")
	image.paste(bg_im,(0,0))

	draw.rectangle(config.bleedrect,
		outline=(0,0,0,255))

	PIL_Helper.AddText(image = image,
		text = tags[1],
		font = config.TitleFont,
		fill = (0,0,0),
		anchor = config.TitleAnchor,
		max_width = config.textmaxwidth)
	PIL_Helper.AddText(image = image,
		text = "Party",
		font = config.TypeFont,
		fill = (0,0,0),
		anchor = SubAnchor(config.TitleAnchor,-35),
		max_width = config.textmaxwidth)
	PIL_Helper.AddText(image = image,
		text = "Party Of:",
		font = config.TypeFont,
		fill = (0,0,0),
		anchor = config.Anchor3,
		max_width = 200)
	PIL_Helper.AddText(image = image,
		text = tags[2],
		font = config.TitleFont,
		fill = (0,0,0),
		anchor = SubAnchor(config.Anchor3,40),
		max_width = 200)
	PIL_Helper.AddText(image = image,
		text = tags[3].replace(r'\n', '\n'),
		font = config.TypeFont,
		fill = (0,0,0),
		anchor = config.FlavorTextAnchor,
		max_width = config.textmaxwidth)
	return image

def MakeCleanCard(config, tags):
	image = Image.new("RGBA", (config.bleed_w, config.bleed_h))
	draw = ImageDraw.Draw(image)
	
	bg_im = Image.open(config.ResourcePath + "tableclean_frontbg.png")
	image.paste(bg_im,(0,0))

	draw.rectangle(config.bleedrect,
		outline=(0,0,0,255))

	PIL_Helper.AddText(image = image,
		text = "Table Cleaned!",
		font = config.TitleFont,
		fill = (0,0,0),
		anchor = config.TitleAnchor,
		max_width = config.textmaxwidth)
	return image


def MakeTipCard(config, tags):
	image = Image.new("RGBA", (config.bleed_w, config.bleed_h))
	draw = ImageDraw.Draw(image)
	
	bg_im = Image.open(config.ResourcePath + "food_frontbg.png")
	image.paste(bg_im,(0,0))

	draw.rectangle(config.bleedrect,
		outline=(0,0,0,255))

	PIL_Helper.AddText(image = image,
		text = tags[1],
		font = config.TitleFont,
		fill = (0,0,0),
		anchor = config.TitleAnchor,
		max_width = config.textmaxwidth)
	PIL_Helper.AddText(image = image,
		text = "Tip!",
		font = config.TypeFont,
		fill = (0,0,0),
		anchor = SubAnchor(config.TitleAnchor,-35),
		max_width = config.textmaxwidth)
	PIL_Helper.AddText(image = image,
		text = tags[2],
		font = config.TypeFont,
		fill = (0,0,0),
		anchor = config.FlavorTextAnchor,
		max_width = config.textmaxwidth)
	PIL_Helper.AddText(image = image,
		text = "Value on eBay:",
		font = config.TypeFont,
		fill = (0,0,0),
		anchor = SubAnchor(config.Anchor3,-10),
		max_width = 200)
	PIL_Helper.AddText(image = image,
		text = tags[3],
		font = config.TitleFont,
		fill = (0,0,0),
		anchor = SubAnchor(config.Anchor3,80),
		max_width = 200)
	return image

MakerDict={
    "TABLE": MakeTableCard,
    "FOOD": MakeFoodCard,
    "CHAR": MakeCharacterCard,
    "EAT": MakeEatCard,
    "PARTY": MakePartyCard,
    "CLEAN": MakeCleanCard,
    "TIP" : MakeTipCard,
    "WRATH" : MakeWrathCard
}


def main(linein, configset):
 	configset.cardnum+=1
 	tags = linein.split('`')	
 	try:
 		im = MakerDict[tags[0]](configset,tags)
 		im.paste(Image.open(configset.ResourcePath + "artmissing.png"),configset.ArtAnchor)
 	except:
 		im = MakeBadCard(configset,tags)
 		print "Warning: Bad Card"
 	return im

if __name__ == '__main__':
	configset = DeckConfiguration("deck.cfg")
	main("CHAR`Test Card`-2`3`4`",configset)