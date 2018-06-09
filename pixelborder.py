#!/usr/bin/env python

from gimpfu import *
from array import array
import sys;
import traceback;

def check_neighbour4(src, x, y, w, h, f, any = any):
	return any([
		f(src[x - 1, y]) if x != 0 else False,
		f(src[x, y - 1]) if y != 0 else False,
		f(src[x + 1, y]) if x != w - 1 else False,
		f(src[x, y + 1]) if y != h - 1 else False,
	])			

def make_border(image, layer):
	layerName = "Border";

	col = gimp.get_foreground()
	w = layer.width
	h = layer.height

	dest_drawable = gimp.Layer(image, layerName, layer.width, layer.height,layer.type, layer.opacity, layer.mode)
	image.add_layer(dest_drawable, 0)
	dst_rgn = dest_drawable.get_pixel_rgn(0, 0, w, h, False, True)

	src_rgn = layer.get_pixel_rgn(0, 0, w, h, False, False)
	for y in xrange(0, h):
		for x in xrange(0, w):
			if 0 == ord(src_rgn[x, y][3]) and \
			   check_neighbour4(src_rgn, x, y, w, h, (lambda val: 0 < (map(ord, val)[3]) )):
				dst_rgn[x, y] = array("B", [ col[0], col[1], col[2], 255 ]).tostring()
				
				progress = float(h)/layer.height
				gimp.progress_update(progress)

	dest_drawable.flush()
	dest_drawable.merge_shadow()
	dest_drawable.update(0, 0, w, h)

def plugin_main(image, layer):
#	sys.stdout = open("stdout.txt", 'a')
#	sys.stderr = open("stdout.txt", 'a')
	print "--BEGIN -----------------------------"
	pdb.gimp_image_undo_group_start(image)
	gimp.progress_init("Making a border" + layer.name + "...")

	try:
		make_border(image, layer);
	except:
		traceback.print_exc()
		gimp.message(format(sys.exc_info()[1]));
	finally:
		pdb.gimp_selection_none(image)
		pdb.gimp_image_undo_group_end(image)
		pdb.gimp_progress_end()
		pdb.gimp_displays_flush()

	print "--END   -----------------------------"


register("python_fu_pixel_border", 
	"Pixel Border", 
	"",
	"N/A", 
	"", 
	"2018",
	"Pixiel Border", 
	"RGBA",
	[
		(PF_IMAGE, "image",       "Input image", None),
		(PF_DRAWABLE, "drawable", "Input drawable", None),
	],
	[],
	plugin_main,
	menu = "<Image>/Filters/Edge-Detect")

main()
