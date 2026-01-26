import argparse
from PIL import Image, PngImagePlugin
from PIL.ExifTags import TAGS, GPSTAGS, Base, GPS, Interop, LightSource, IFD
import tkinter as tk
from tkinter import ttk

def reverse_enum(enum_cls):
	"""Convert Pillow enum classes into {tag_id: tag_name}"""
	return {value: name for name, value in enum_cls.__dict__.items() if isinstance(value, int)}

BASE_TAGS = reverse_enum(Base)
INTEROP_TAGS = reverse_enum(Interop)
LIGHTSOURCE_TAGS = reverse_enum(LightSource)


def decode_value(value):
	if isinstance(value, bytes):
		try:
			return value.decode("utf-8", errors="replace")
		except Exception:
			return str(value)
	return value


def extract_ifd(exifdata, ifd_id, tag_map):
	"""
	Extracts one IFD and resolves tag names.
	"""
	result = {}
	try:
		ifd = exifdata.get_ifd(ifd_id)
	except KeyError:
		return result

	for tag_id, value in ifd.items():
		tag_name = tag_map.get(tag_id, tag_id)
		result[tag_name] = decode_value(value)

	return result


def extract_all_exif(image):
	exifdata = image.getexif()
	metadata = {}

	# ------------------ IFD0 (primary EXIF) ------------------
	for tag_id, value in exifdata.items():
		tag_name = TAGS.get(tag_id, tag_id)
		metadata[tag_name] = decode_value(value)

	# ------------------ Exif SubIFD ------------------
	base_data = extract_ifd(exifdata, 0x8769, BASE_TAGS)
	for tag_name, value in base_data.items():
		if tag_name == "ComponentsConfiguration":
			COMP_MAP = {0:"Unused", 1:"Y", 2:"Cb", 3:"Cr", 4:"R", 5:"G", 6:"B"}
			readable = tuple(COMP_MAP.get(ord(c) if isinstance(c, str) else c, c) for c in value)
			readable = ",".join(readable)
			base_data[tag_name] = readable
		elif tag_name == "FileSource":
			if value == "\x03":
				base_data[tag_name] = "Image was recorded on a DSC"
		elif tag_name == "SceneType":
			if value == "\x01":
				base_data[tag_name] = "Image was directly photographed"
	metadata.update(base_data)

	# ------------------ GPS IFD ------------------
	gps_data = extract_ifd(exifdata, 0x8825, GPSTAGS)
	for tag_name, value in gps_data.items():
		if tag_name == "GPSVersionID":
			b = ''.join(format(ord(char), 'x') for char in value)
			b = '.'.join(b[i:i+1] for i in range(0, len(b), 1))
			value = b
		elif tag_name == "GPSAltitudeRef":
			b = ''.join(format(ord(char), 'x') for char in value)
			if (b):
				value = "BELOW SEA LEVEL"
			else:
				value = "ABOVE SEA LEVEL"
		metadata[f"GPS_{tag_name}"] = value

	# ------------------ Interop IFD ------------------
	metadata.update(
		extract_ifd(exifdata, 0xA005, INTEROP_TAGS)
	)


	return metadata

# ------------------ argparse ------------------
parser = argparse.ArgumentParser(description="EXIF metadata parser")
parser.add_argument("path", help="Target path of the image file")
args = parser.parse_args()

# ------------------ file parsing ------------------
path = args.path
image = Image.open(path)

# collect metadata into a dictionary
metadata_dict = {}

# basic metadata
info_dict = {
	"Filename": image.filename,
	"Image Size": image.size,
	"Image Height": image.height,
	"Image Width": image.width,
	"Image Format": image.format,
	"Image Mode": image.mode,
	"Image is Animated": getattr(image, "is_animated", False),
	"Frames in Image": getattr(image, "n_frames", 1)
}


metadata_dict.update(info_dict)
metadata_dict.update(extract_all_exif(image))

# ------------------ GUI ------------------
screen = tk.Tk()
screen.title("Image Metadata Editor")
screen.geometry("800x600")

# Treeview (table)
tree = ttk.Treeview(screen, columns=("Field", "Value"), show="headings")
tree.heading("Field", text="Field")
tree.heading("Value", text="Value")
tree.column("Field", width=250, anchor="w")
tree.column("Value", width=520, anchor="w")

# Track rows with None values
none_items = []
none_hidden = False

# Scrollbar
scrollbar = ttk.Scrollbar(screen, orient="vertical", command=tree.yview)
tree.configure(yscrollcommand=scrollbar.set)
tree.pack(side="left", fill="both", expand=True)
scrollbar.pack(side="right", fill="y")


# Insert data into table
for field, value in metadata_dict.items():
	item = tree.insert("", "end", values=(field, value))
	if value is None:
		none_items.append(item)

screen.mainloop()