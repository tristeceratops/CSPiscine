import argparse
from PIL import Image, PngImagePlugin
from PIL.ExifTags import TAGS
import tkinter as tk
from tkinter import ttk

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
metadata_dict.update({tag_name: None for tag_name in TAGS.values()})

# EXIF metadata
exifdata = image.getexif()

for tag_id, value in exifdata.items():
    tag_name = TAGS.get(tag_id, tag_id)
    if isinstance(value, bytes):
        try:
            value = value.decode()
        except UnicodeDecodeError:
            value = str(value)
    metadata_dict[tag_name] = value

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

# Scrollbar
scrollbar = ttk.Scrollbar(screen, orient="vertical", command=tree.yview)
tree.configure(yscrollcommand=scrollbar.set)
tree.pack(side="left", fill="both", expand=True)
scrollbar.pack(side="right", fill="y")

# Insert data into table
for field, value in metadata_dict.items():
    tree.insert("", "end", values=(field, value))

screen.mainloop()
