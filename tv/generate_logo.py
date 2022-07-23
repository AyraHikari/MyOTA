import json, requests
from PIL import Image
from io import BytesIO

data = json.loads(open("Stream.json", "r").read())


def resize(image_pil, width, height, replace_color):
	'''
	Resize PIL image keeping ratio and using white background.
	'''
	ratio_w = width / image_pil.width
	ratio_h = height / image_pil.height
	if ratio_w < ratio_h:
		# It must be fixed by width
		resize_width = width
		resize_height = round(ratio_w * image_pil.height)
	else:
		# Fixed by height
		resize_width = round(ratio_h * image_pil.width)
		resize_height = height
	image_resize = image_pil.resize((resize_width, resize_height), Image.NEAREST)
	background = Image.new('RGBA', (width, height), replace_color)
	offset = (round((width - resize_width) / 2), round((height - resize_height) / 2))
	background.paste(image_resize, offset)
	return background.convert('RGB')


dataCopy = data

count = 0
for station in data:
	count += 1
	try:
		response = requests.get(station['logo'])
		image = Image.open(BytesIO(response.content))
	except:
		print("> [{}/{}] Failed: {}".format(count, len(data), station["id"]))
		continue
	replace_color = (0, 0, 0, 255)

	rgb_im = image.convert('RGB')
	r, g, b = rgb_im.getpixel((1, 1))
	replace_color = (r, g, b, 255)

	e = resize(image, 171, 270, replace_color)
	e.save("logo/{}.jpg".format(station["id"]))

	genStation = station
	genStation["logo"] = "https://raw.githubusercontent.com/AyraHikari/MyOTA/anime/tv/logo/{}.jpg".format(station["id"])
	dataCopy[count-1] = genStation
	print("> [{}/{}] Generated logo: {}".format(count, len(data), station["id"]))

w = open("Stream.json", "w")
w.write(json.dumps(dataCopy))
w.close()
print("\n\n> New Stream.json has been saved")