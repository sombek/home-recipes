"""
frame_resizer.py
Nick Flanders

Creates a new directory with all images in the given directory
resized to 800 x 600 for to save space when being displayed in
a digital picture frame
"""

import sys
import os
import math
from PIL import Image


def update_progress(completed, message=None, width=40):
    """
    Display a progress bar for a task that is the given percent completed
    :param completed:   the ratio of the task completed (con the closed interval [0, 1])
    :param message:     the preceding message to display in front of the progress bar
    :param width:       the width of the progress bar
    """
    if message is None:
        message_str = ""
    else:
        message_str = message
    done_width = int(math.ceil(completed * width))
    sys.stdout.write("\r" + message_str + " [{}]".format(" " * (width - 1)) + " " + str(int(completed * 100)) + "%")
    sys.stdout.write("\r" + message_str + " " + '\u2588' * (done_width + 1))


# constants for the max height and width to resize images to
WIDTH = 800
HEIGHT = 600

directory = "./docs"
output_dir = directory + "/resized"

if not os.path.exists(output_dir):
    os.mkdir(output_dir)

print("\nResizing images in", directory, "\n")

# log all errors to be displayed at script termination
error_log = []
img_files = os.listdir(directory)
img_files.remove("resized")
# after finishing delete the old images and move the new ones to the original directory
history = []
for index, infile in enumerate(img_files):
    outfile = output_dir + "/" + infile
    if not os.path.exists(outfile):
        try:
            # check if file is an image
            if infile[-4:] not in [".jpg", ".png", ".jpeg"]:
                error_log.append("'%s' is not an image" % infile)
                continue

            im = Image.open(directory + "/" + infile)
            ratio = min(WIDTH / im.width, HEIGHT / im.height)
            im.thumbnail((im.size[0] * ratio, im.size[1] * ratio), Image.Resampling.LANCZOS)
            # based on the file extension, save the resized image
            format = infile.split(".")[-1]
            if format == "jpg" or format == "jpeg":
                im.save(outfile, "JPEG")
            elif format == "png":
                im.save(outfile, "PNG")
            else:
                im.save(outfile, "JPEG")

            history.append({
                "old": directory + "/" + infile,
                "new": outfile
            })

        except IOError:
            error_log.append("cannot create resized image for '%s'" % infile)
    # display progress bar
    update_progress((index + 1) / len(img_files), message="Resizing")

# remove the old images
for index, img in enumerate(history):
    os.remove(img["old"])
    os.rename(img["new"], img["old"])
    update_progress((index + 1) / len(img_files), message="Moving")

# check if any images failed to be resized
if len(error_log) == 0:
    print("\n\nAll images successfully resized!")
else:
    print("\n\nThe following errors occurred during resizing:")
    for error in error_log:
        print(error)
