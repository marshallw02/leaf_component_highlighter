# leaf_component_highlighter

This is a python program that is used to highlight all of the leaf-level components of an Android application screenshot using a corresponding 
xml file.  To run this program, the screenshot and xml pairs should have the same filenames in the format: <app.package>-<screen#>.ext, where 
the extension is either .xml or .png.  To run this program, place all of the screenshots into a directory named 
"Programming-Assignment-Data" and place leaf_component_highlighter.py and Programming-Assignment-Data into the same directory.  A 
sample batch of data is included in this repository. Once ran, leaf_component_highlighter.py will create a directory named "output" if one does 
not already exist, and will highlight the leaf-level components in the screenshots and store them into the output directory.

Note: The output directory of this repository contains the screenshots that I was able to generate when running this program on the data in the 
Programming-Assignment-Data directory

## How it works
This program highlights the lefa-level components by parsing through the xml files using the ElementTree XML Python module.  This method 
was chosen for this project because it represents all of the components of the xml file as a tree, making it easy to identify which components 
were leaf-level and which were not.  One of the xml files in the data had an error, so in this case manual parsing is used.  The file is split up by all 
node delimiters and each node with a class tag that is not a layout or viewgroup of some sort is highlighted.  The layouts and viewgroups do 
not need to be highlighted because these components traditionally group other components together so we know they shouldn't be a leaf-
level component themselves.  Once all of the leaf-level components are found, their bounds are stored into a list which converts the bounds to 
sets of tuples which are used by the Pillow library to draw yellow boxes using these bounds. After all of the important bounds have been 
highlighted, the new annotated image is saved into the output directory with the same filename as the original unannotated image.
