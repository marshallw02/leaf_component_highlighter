import os
import re
import xml.etree.ElementTree as ET
from PIL import Image, ImageDraw

# This method takes the list of leaf component bounds as strings and returns a list of the leaf component bounds as tuples
def normalize_coords(coords_list):
    normalized = []
    for area in coords_list:
        # Regex is used to split the string coordinates into just the raw numbers
        temp = re.split("\[|,|\]", area)

        # This loop attempts to remove every blank cell left over from the re.split() until there are none left
        while True:
            try:
                temp.remove('')
            except:
                break
        
        # List comprehension for casting all numbers from str to int
        temp = [int(x) for x in temp]

        # Appends the whole tuple as a single item in list
        normalized.append(tuple(temp))
    return normalized

# Creating the directory for the fully highlighted screenshots
if not os.path.isdir(".\output"): os.makedirs(".\output")

# This checks to make sure the output directory is clear
for file in os.scandir(".\output"):
    os.remove(file)

DATA_DIR_PATH = ".\Programming-Assignment-Data\\"

# Scan through each file in the dir alphabetically.  If a png is found, then set it as the current png and continue. 
# If the xml file for that png is found, parse through the xml to highlight all of the leaf components.  Then saves highlighted
# png to output directory.
for file in os.scandir(DATA_DIR_PATH):

    filename = file.path.split(DATA_DIR_PATH)[1]
    
    # For each png/xml pair, the png will always be found first by os.scandir(). If this if statement is entered then
    # we know we are on a new png/xml pair, so it will change the current png and advance to the for loop to the next file.
    if ".png" in file.path:
        cur_png = Image.open(file.path)
        draw = ImageDraw.Draw(cur_png)
        continue
    
    # Try catch is used in case there are errors in the xml file that prevent parsing. There was an error in com.apalon.ringtones.xml
    # but I have manually fixed the error so that the corresponding screenshot can be annotated.
    try:
        if ".xml" in file.path:
            tree = ET.parse(file.path)
            root = tree.getroot()
            all_bounds = []

            # For every node in the tree, if they have no children then it is a leaf node, so we append
            # the bounds of this component to the list of bounds as a string
            for node in root.iter():
                if list(node) == []:
                    all_bounds.append(node.attrib.get("bounds"))

            # normalize_coords() will convert all_bounds from a list of string coordinates to a list of tuple coordinates, 
            # since draw.rectangle requires the coordinates to be in tuple format.
            all_bounds = normalize_coords(all_bounds)

            # Iterate through each set of leaf component coordinates and highlight
            for area in all_bounds:
                draw.rectangle( xy = area,
                                fill = None, #clear fill
                                outline = (255,255,0), #yellow outline
                                width = 8)
                
            # Save the file to output directory
            cur_png.save(".\output\\" + filename[:-3] + "png")
    except:
        print("Error in " + filename)
        