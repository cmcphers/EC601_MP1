# MP01.py
# Charles A. McPherson, Jr.
# EC601 A1 - Fall 2018
# Mini-Project 1
#########################################################

import random

supportedTypes = ['png', 'jpg', 'jpeg', 'tiff'];
t_wordList = ['apple', 'orange', 'saxophone', 'armchair', 'Nikola Tesla', 
    'Steve McQueen', 'carptentry', 'nature', 'picture', 'ennui', 'failure',
    'nothing', 'something', 'wood', 'steel', 'fire', 'water', 'air', 'the void'];

def GetTwImages(handle):
    # For sprint 1, simply read the images from a local file with that name.
    f = open(handle,'r') # Open file for reading..
    tweets = [];
    for line in f:
        tweets.append(line.rstrip());
    f.close() # Close it so as not to be a dick.

    # Filter out non-images.
    images = [];
    for obj in tweets:
        if(IsImage(obj)):
            images.append(obj) # If the attached file is an image, append.

    return images # Return images

def ConstructVideo(images, maxRate, minDuration):
    if(minDuration < 0):
        return -1
    elif(maxRate < 0):
        return -1
    nImages= len(images)
    dur = minDuration/nImages
    if(dur < 1.0/maxRate):
        dur = 1.0/maxRate
    f = open('output.txt','w+') # Open output file for writing.
    for im in images:
        f.write(im + ' ' + str(dur) + '\n');
    f.close()
    return 0


def CaptionImage(im):
    c = GVIdentify(im);
    captioned = im;
    for word in c:
        captioned += ', '
        captioned += word
    return captioned
    

def GVIdentify(im):
    random.seed(); # Seed the random number generator.
    nChoices = random.randint(0,3); # Random number of choices.
    content = []
    for i in range(nChoices): # Construct list of random words from the list.
        content.append(random.choice(t_wordList));
    return content

def IsImage(im):
    p = im.rpartition('.')
    ext = p[2] # Get the filename extension.
    r = False # By default, the result is false.
    for t in supportedTypes:
        if(t == ext):
            r = True
            break
    return r
