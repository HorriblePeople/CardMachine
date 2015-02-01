from PIL import Image, ImageFont, ImageDraw

filename = "Template.png"

bleed_w = 850
bleed_h = 1161

w = 788
h = 1088

w_marg = (bleed_w-w)/2
h_marg = (bleed_h-h)/2


image = Image.new("RGBA", (bleed_w, bleed_h))
draw = ImageDraw.Draw(image)
points = ((w_marg,h_marg),
	    (w_marg+w,h_marg),
	    (w_marg+w,h_marg+h),
	    (w_marg,h_marg+h),
	    (w_marg,h_marg))

draw.line(points,fill=(0,0,0,255), width=2)

image.save(filename, "PNG")
