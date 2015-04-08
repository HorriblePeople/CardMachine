from PIL import Image, ImageFont, ImageDraw, ImageOps
import os, glob
from math import ceil

def BuildFont(fontname, fontsize):
    return ImageFont.truetype(fontname, fontsize)

def WrapText(text, font, max_width):
    '''
    Wraps text properly, so that each line does not exceed
    a maximum width in pixels. It does this by adding words
    in the string to the line, one by one, until the next
    word would make the line longer than the maximum width.
    It then start a new line with that word instead.
    New lines get special treatment. It's kind of funky.
    "Words" are split around spaces.
    '''
    temp = ""
    wrapped_text = ""

    for w in text.split(' '):
        # Add words to empty string until the next word would make the line too long
        # If next word contains a newline, check only first word before newline for width match
        if "\n" in w:
            wrapped_text += temp.strip(' ')
            width, height = font.getsize(u"{0} {1}".format(temp, w.partition('\n')[0]))
            # If adding one last word before the line break will exceed max width
            # Add in a line break before last word.
            if width > max_width:
                wrapped_text += "\n"
            else:
                wrapped_text += " "
            par = w.rpartition('\n')
            wrapped_text += par[0] + "\n"
            temp = par[2] + " "
        else:
            width, height = font.getsize(u"{0} {1}".format(temp, w))
            if width > max_width:
                wrapped_text += temp.strip(' ') + "\n"
                temp = ""
            temp += w + " "
    return wrapped_text + temp.strip(' ')

def GetTextBlockSize(text, font, max_width=-1, leading_offset=0):
    if max_width > -1:
        wrapped_text = WrapText(text, font, max_width)
    else:
        wrapped_text = text
    lines = wrapped_text.split('\n')
    
    # Set leading
    leading = font.font.ascent + font.font.descent + leading_offset

    # Get max line width
    max_line_width = 0
    for line in lines:
        line_width, line_height = font.getsize(line)
        # Keep track of the longest line width
        max_line_width = max(max_line_width, line_width)

    return (max_line_width, len(lines)*leading)

def AddText(image, text, font, fill=(0,0,0), anchor=(0,0),
            max_width=-1, halign="center", valign="top", leading_offset=0,
            rotate=0):
    '''
    First, attempt to wrap the text if max_width is set,
    and creates a list of each line.
    Then paste each individual line onto a transparent
    layer one line at a time, taking into account halign.
    Then rotate the layer, and paste on the image according
    to the anchor point, halign, and valign.

    @return (int, int): Total width and height of the text block
        added, in pixels.
    '''
    if max_width > -1:
        wrapped_text = WrapText(text, font, max_width)
    else:
        wrapped_text = text
    lines = wrapped_text.split('\n')

    # Initiliaze layer and draw object
    layer = Image.new('L', (5000,5000))
    draw = ImageDraw.Draw(layer)
    start_y = 500
    if halign == "left":
        start_x = 500
    elif halign == "center":
        start_x = 2500
    elif halign == "right":
        start_x = 4500
    
    # Set leading
    leading = font.font.ascent + font.font.descent + leading_offset

    sw = font.getsize("   ")[0]

    # Begin laying down the lines, top to bottom
    y = start_y
    max_line_width = 0
    for line in lines:
        # If current line is blank, just change y and skip to next
        if not line == "":
            line = "   " + line + "   "  # dirty fix
            line_width, line_height = font.getsize(line)
            if halign == "left":
                x_pos = start_x-sw
            elif halign == "center":
                x_pos = start_x-(line_width/2)
            elif halign == "right":
                x_pos = start_x-line_width+sw
            # Keep track of the longest line width
            max_line_width = max(max_line_width, line_width)
            draw.text((x_pos, y), line, font=font, fill=255)
        y += leading

    total_text_size = (max_line_width, len(lines)*leading)

    # Now that the text is added to the image, find the crop points
    top = start_y
    bottom = y - leading_offset
    if halign == "left":
        left = start_x
        right = start_x + max_line_width
    elif halign == "center":
        left = start_x - max_line_width/2
        right = start_x + max_line_width/2
    elif halign == "right":
        left = start_x - max_line_width
        right = start_x
    layer = layer.crop((left, top, right, bottom))
    # Now that the image is cropped down to just the text, rotate
    if rotate != 0:
        layer = layer.rotate(rotate, expand=True)

    # Find the absolute anchor point on the original image
    # Negative anchor values refer from the right/bottom of the image
    x, y = image.size
    anchor_x = anchor[0]+x if anchor[0] < 0 else anchor[0]
    anchor_y = anchor[1]+y if anchor[1] < 0 else anchor[1]
        
    # Determine the anchor point for the new layer
    width, height = layer.size
    if halign == "left":
        coords_x = anchor_x
    elif halign == "center":
        coords_x = anchor_x - width/2
    elif halign == "right":
        coords_x = anchor_x - width
    if valign == "top":
        coords_y = anchor_y
    elif valign == "center":
        coords_y = anchor_y - height/2
    elif valign == "bottom":
        coords_y = anchor_y - height
    
    image.paste(ImageOps.colorize(layer, (255,255,255), fill),
                (coords_x, coords_y), layer)

    return total_text_size

def BuildPage(card_list, grid_width, grid_height, filename,
              cut_line_width=3, page_ratio=8.5/11.0, h_margin=100):
    '''
    Adds cards, in order, to a grid defined by grid_width, grid_height.
    It then adds a border to the grid, making sure to preserve the
    page ratio for later printing, and saves to filename
    Assumes that all the cards are the same size
    '''
    # Create card grid based on size of the first card
    w,h = card_list[0].size
    bg = Image.new("RGB", (w * grid_width + cut_line_width * (grid_width - 1),
                           h * grid_height + cut_line_width * (grid_height - 1)
                           )
                  )
    # Add cards to the grid, top down, left to right
    for y in xrange(grid_height):
        for x in xrange(grid_width):
            card = card_list.pop(0)
            coords = (x*(w+cut_line_width),
                      y*(h+cut_line_width))
            bg.paste(card, coords)
    # If there's a margin defined, add extra whitespace around the page
    # if h_margin > 0:
    #     w,h = bg.size
    #     w_margin = (((h_margin*2)+h)*page_ratio-w)/2.0
    #     w_margin = round(w_margin)
    #     page = Image.new("RGB", (int(w+w_margin*2), int(h+h_margin*2)), (255, 255, 255))
    #     page.paste(bg, (w_margin,h_margin))
    #     page.save(filename)
    # else:
        # bg.save(filename)
    # Create a paper image the exact size of an 8.5x11 paper
    # to paste the card images onto
    paper_width = int(8.5*300)  # 8.5 inches times 300 dpi
    paper_height = int(11*300)  # 11 inches times 300 dpi
    paper_image = Image.new("RGB", (paper_width, paper_height), (255, 255, 255))
    w,h = bg.size
    # TODO Add code that shrinks the bg if it's bigger than any dimension
    # of the Paper image
    paper_image.paste(bg, ((paper_width - w)/2, (paper_height - h)/2))
    paper_image.save(filename, dpi=(300, 300))

def BlankImage(w, h, color=(255,255,255), image_type="RGBA"):
    return Image.new(image_type, (w, h), color=color)

def LoadImage(filepath):
    return Image.open(filepath)

def ResizeImage(image, size, method=Image.ANTIALIAS):
    return image.resize(size, method)

def DrawRect(image, x, y, width, height, color):
    draw = ImageDraw.Draw(image)
    draw.rectangle((x, y, width, height), fill=color)

if __name__ == "__main__":
    image = Image.open("y.png")
    font = ImageFont.truetype("Ubahn_newpony.ttf", 40)
    text = "Boulder\nBoulder Boulder\nBoulder"
    w,h = image.size
    center = w/2
    anchor = (-50, -50)
    AddText(image, text, font, anchor=anchor, halign="right",
            valign="bottom", fill=(200,0,0), rotate=0)
    image.show()
