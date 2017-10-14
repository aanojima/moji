#!/usr/bin/python
# -*- coding: utf-8 -*-
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageChops
import unicode_blocks, unicode_fonts
import os
from fontTools.ttLib import TTFont

'''
Main Definitions
'''
def char_in_font(unicode_char, font):
	for cmap in font['cmap'].tables:
		if cmap.isUnicode():
			if ord(unicode_char) in cmap.cmap:
				return True
	return False

def equal(im1, im2):
	return ImageChops.difference(im1, im2).getbbox() is None

def unicode_to_image(unicode_text, generate_test_file = False):
	# Configuration
	color_scheme = "RGB"
	width = 256
	height = 256
	back_ground_color = (255,255,255)
	font_size = 128
	font_color = (0,0,0)
	blockName = unicode_blocks.get_block_of(unicode_text[0])
	font = unicode_fonts.get_font_of_char(unicode_text[0])
	fontFilename = "/mit/moji/fonts/" + font
	ttfont = TTFont(fontFilename)

	im = Image.new(color_scheme, (width, height), back_ground_color)
	if font != "NotoColorEmoji.ttf":
		draw = ImageDraw.Draw(im)
		unicode_font = ImageFont.truetype(fontFilename, font_size)
		(w, h) = unicode_font.getsize(unicode_text[0])
		# TODO: what if w or h are bigger than image dimensions?
		(x, y) = (float(width - w) / 2, float(height - h) / 2)
		draw.text((x, y), unicode_text[0], font=unicode_font, fill=font_color)
		# Character boundary display
		# draw.rectangle([(x,y), (x+w, y+h)], outline=font_color)
		del draw

	# Save first block characters to view
	if generate_test_file:
		if not blockName:
			blockName = "None"
		else:
			decValue = "{0:#0{1}}".format(ord(unicode_text[0]),7)
			hexValue = "{0:#0{1}x}".format(ord(unicode_text[0]),6)
			filename = "test/" + decValue + '_' + blockName + "_" + hexValue + ".png"
			im.save(filename)
	
	return im

'''
Testing Methods
'''
def record_block_fonts():
	f = open("unicode_fonts.txt", "w")
	f2 = open("unicode_unknown_fonts.txt", "w")
	for firstUChar in unicode_fonts._BLOCK_STARTS:
		a = unicode_to_image(unichr(firstUChar), True)
		hexValue = "{0:#0{1}x}".format(firstUChar,6)
		line = "(" + hexValue.upper() + ", '" + str(a[0]) + "', '" + str(a[1]) + "'),\n"
		if a[0] is None:
			line = "(" + hexValue.upper() + ", " + str(a[0]) + ", '" + str(a[1]) + "'),\n"
		if not a[2]:
			for offset in xrange(1,6):
				# For some blocks, first characters might be undefined or reserved
				a = unicode_to_image(unichr(firstUChar + offset), True)
				if a[2]:
					hexValue = "{0:#0{1}x}".format(firstUChar,6)
					if a[0] is None:
						line = "(" + hexValue.upper() + ", " + str(a[0]) + ", '" + str(a[1]) + "'),\n"
					else:
						line = "(" + hexValue.upper() + ", '" + str(a[0]) + "', '" + str(a[1]) + "'),\n"
					break
			if not a[2]:
				f2.write(line)
		f.write(line)
	f2.close()
	f.close()

def find_font(unicode_text):
	# Configuration
	color_scheme = "RGB"
	width = 256
	height = 256
	back_ground_color = (255,255,255)
	font_size = 128
	font_color = (0,0,0)
	blockName = unicode_blocks.get_block_of(unicode_text[0])
	font = unicode_fonts.get_font_of_char(unicode_text[0])
	fontFilename = "fonts/" + font
	ttfont = TTFont(fontFilename)

	fonts = os.walk(os.getcwd() + '/fonts').next()[2]
	fontIndex = 0
	hasUsableFont = True and blockName is not None
	tempFont = font
	tempFontFilename = fontFilename
	tempTTFont = ttfont
	while blockName is None or not char_in_font(unicode_text[0], tempTTFont):
		if fontIndex >= len(fonts):
			hasUsableFont = False
			break
		tempFont = fonts[fontIndex]
		fontIndex += 1
		if tempFont[-4:] != ".ttf" and tempFont[-4:] != ".otf":
			continue
		tempFontFilename = "fonts/" + tempFont
		tempTTFont = TTFont(tempFontFilename)

	if hasUsableFont:
		ttfont = tempTTFont
		font = tempFont
		fontFilename = tempFontFilename
		print "[INFO] Found font", font, "for Unicode Block", blockName
	else:
		print "[WARNING] Could not find font for Unicode Block", blockName

	# Write to an external file
	return (blockName, font, hasUsableFont)

def generate_block_first_character_images():
	for code in unicode_blocks._BLOCK_STARTS:
		unicode_to_image(unichr(code), True)

# # Main Code
# unicode_text = u'{か'
# unicode_text_image = unicode_to_image(unicode_text)
# output_filename = "test.png"
# unicode_text_image.save(output_filename)

# generate_block_first_character_images()
