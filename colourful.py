
import random, colorsys, hashlib

def rescale(n, lower, upper):
	return (upper-lower)*n + lower

def string_to_rgb(s="#ffffff"):
	return int(s[1:3], 16), int(s[3:5], 16), int(s[5:7], 16)

def rgb_to_string(r=255, g=255, b=255):
	r, g, b = hex(int(r))[2:], hex(int(g))[2:], hex(int(b))[2:]

	r = '0' + r if len(r) < 2 else r
	g = '0' + g if len(g) < 2 else g
	b = '0' + b if len(b) < 2 else b

	return '#' + r + g + b

def random_pastel(tint="#ffffff"):
	tint_r, tint_g, tint_b = string_to_rgb(tint)

	r = (random.randrange(0, 256) + tint_r) // 2
	g = (random.randrange(0, 256) + tint_g) // 2
	b = (random.randrange(0, 256) + tint_b) // 2

	return rgb_to_string(r, g, b)

def prettify(r, g, b):
	h, s, v = colorsys.rgb_to_hsv(r/255, g/255, b/255)

	# Rescale values into the following ranges:

	# Hue: [0, 360]
	# Saturation: [20, 100]
	# Brightness: [67, 100]

	s = rescale(s, 0.2, 1)
	v = rescale(v, 0.67, 1)

	r, g, b = colorsys.hsv_to_rgb(h, s, v)
	r, g, b = r*255, g*255, b*255

	return r, g, b

def uglify(r, g, b):
	h, s, v = colorsys.rgb_to_hsv(r/255, g/255, b/255)

	# Rescale values into the following ranges:

	# Hue: [0, 360]
	# Saturation: [0, 20]
	# Brightness: [0, 67]

	s = rescale(s, 0, 0.2)
	v = rescale(v, 0, 0.67)

	r, g, b = colorsys.hsv_to_rgb(h, s, v)
	r, g, b = r*255, g*255, b*255

	return r, g, b

def random_rgb():
	r = random.randrange(0, 256)
	g = random.randrange(0, 256)
	b = random.randrange(0, 256)
	return prettify(r, g, b)

def random_colour():
	return rgb_to_string(*random_rgb())

def string_to_colour(s):
	h = int(hashlib.sha1(s.encode('utf-8')).hexdigest(), 16)

	r = h & 0xFF
	g = (h >> 8) & 0xFF
	b = (h >> 16) & 0xFF

	r, g, b = prettify(r, g, b)

	return rgb_to_string(r, g, b)

def string_to_dark_colour(s):
	h = int(hashlib.sha1(s.encode('utf-8')).hexdigest(), 16)

	r = h & 0xFF
	g = (h >> 8) & 0xFF
	b = (h >> 16) & 0xFF

	r, g, b = uglify(r, g, b)

	return rgb_to_string(r, g, b)

GOLDEN_RATIO_CONJUGATE = 0.618033988749895

def cyclic_colours(n, seed):
	h, _, _ = colorsys.rgb_to_hsv(*(random_rgb() if not seed else string_to_rgb(seed)))

	result = []
	for i in range(0, n):
		h = (h + GOLDEN_RATIO_CONJUGATE) % 1
		r, g, b = colorsys.hsv_to_rgb(h, 0.5, 0.95)
		r, g, b = r*255, g*255, b*255
		result.append(rgb_to_string(r, g, b))

	return result
