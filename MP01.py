# MP01.py
# Charles A. McPherson, Jr.
# EC601 A1 - Fall 2018
# Mini-Project 1
#########################################################

def GetTwImages(handle):
    # For sprint 1, simply read the images from a local file with that name.
    f = open(handle,'r') # Open file for reading.
    tweets = f.read() # Read the entire file.
    f.close() # Close it so as not to be a dick.

    # Filter out non-images.
    images = [];
    for obj in tweets:
        if(IsImage(obj)):
            images.extend(obj) # If the attached file is an image, append.

    return images # Return images
