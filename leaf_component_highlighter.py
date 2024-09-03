import os
import re
import xml.etree.ElementTree as ET
from PIL import Image, ImageDraw

# This method takes the list of leaf component bounds as strings and returns a list of the leaf component bounds as tuples
def normalize_coords(coords_list):
    normalized = []
    for area in coords_list:
        # re.split is used to split the string coordinates into just the raw numbers using multiple delimiters
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
if not os.path.isdir("output"): os.makedirs("output")

# This checks to make sure the output directory is clear
for file in os.scandir("output"):
    os.remove(file)

DATA_DIR_PATH = "Programming-Assignment-Data/"

#Scan through each file in the dir and sort them alphabetically
with os.scandir(DATA_DIR_PATH) as files:
    sorted_files = sorted(files, key=lambda entry: entry.name)
    sorted_names = [entry.name for entry in sorted_files]

# Iterate through the files in the data directory using the alphabetically sorted list.  If a png is found, then set it as the 
# current png and continue. If the xml file for that png is found, parse through the xml to highlight all of the leaf components.  
# Then saves highlighted png to output directory.
for file in sorted_names:

    filepath = DATA_DIR_PATH + file
    
    # For each png/xml pair, the png will always be found first because we sorted the files alphabetically. If this if statement 
    # is entered then we know we are on a new png/xml pair, so it will change the current png and advance to the for loop to the 
    # next file.
    if ".png" in file:
        cur_png = Image.open(filepath)
        draw = ImageDraw.Draw(cur_png)
        continue

    if ".xml" in file:
        all_bounds = []

        # Try catch is used in case there are errors in the xml file that prevent parsing. If errors are present, 
        # we will manually parse through the file to find the leaf components
        try:
            tree = ET.parse(filepath)
            root = tree.getroot()

            # For every node in the tree, if they have no children then it is a leaf node, so we append
            # the bounds of this component to the list of bounds as a string
            for node in root.iter():
                if list(node) == []:
                    all_bounds.append(node.attrib.get("bounds"))

        # If there is an error in the xml file prevents automatic parsing, then we manually parse through the file
        # by splitting the xml file up by all node related delimiters, so each item in the list corresponds to a node
        # in the xml file.  If the class of the compoent is a ViewGrup, RecyclerView, or Layout, then we assume that node 
        # does not represent anything on the page and do not record the bounds.  If the class is anything else, then we 
        # assume the component is present in the screenshot visually, and record the bounds of the component for highlighting.
        except:
            with open(filepath, "r") as corrupt_file:
                # Reading the file into a single string and splitting into a list
                split_file = corrupt_file.read()
                split_file = re.split("<node |>|/>|</node>",split_file)

                for node in split_file:
                    # If node does not have a class tag, then it is not important for highlighting and can be skipped
                    try:
                        component_class = node.split("class=\"")[1].split("\"")[0]
                    except:
                        continue
                    # If node does have a class tag, then check if it is an important class or not
                    if "Layout" in component_class or ".ViewGroup" in component_class or "RecyclerView" in component_class:
                        continue
                    # If this line is reached then the current node is important and should be highlighted, so bounds are recorded here
                    leaf_bound = node.split("bounds=\"")[1].split("\"")[0]
                    all_bounds.append(leaf_bound)

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
        cur_png.save("output/" + file[:-3] + "png")

        