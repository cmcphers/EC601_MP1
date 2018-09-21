# MP01.py
# Charles A. McPherson, Jr.
# EC601 A1 - Fall 2018
# Mini-Project 1
#########################################################

import random
import tweepy
import urllib.request
import os
from ffmpy import FFmpeg
from google.cloud import vision
from google.cloud.vision import types

MAX_IMAGES = 100 # Limit to 100 images at this point to prevent filling up the folder.
PER_REQUEST = 10 # Retreive 10 tweets at a time.
MAX_QUERY = 100 # Limit to 100 querys
SIZE = [640,260] # Frame size.
BORDERSIZE = [640,360] # Border size.
MAX_ANNOTATIONS = 3 # Maximum of three words per image.

def __ReadKeys__():
    keys = []
    with open('Keys.txt','r') as f:
        for line in f:
            keys.append(line.strip())
    return keys

def GetTwImages(handle):
    # For sprint 2, extract the images from the tweets, extract file names,
    # and save the actual files to disk.

    # New change - Read keys from file.
    keys = __ReadKeys__()

    # Initialize the TweePy API
    auth = tweepy.OAuthHandler(keys[0], keys[1])
    auth.set_access_token(keys[2], keys[3])
    api = tweepy.API(auth)

    # Grab newest tweets.
    try:
        tw = api.user_timeline(screen_name = handle, count = PER_REQUEST)
    except tweepy.TweepyError as e:
        print(e.message)
        return {'error':e.message}
    
    # Keep track of number of images downloaded.
    image_counter = 0
    query_counter = 1
    images = []
    # Keep collecting images until you have the maximum. 
    while image_counter < MAX_IMAGES:
        # Loop through the tweets from the query.
        for tweet in tw:
            if('media' in tweet.entities): # If there is attached media, scan through it.
                for obj in tweet.entities['media']:
                    if(obj['type'] == 'photo'): # If the item is a photo, 
                        url = obj['media_url'] # Get the URL,
                        ext = url.rpartition('.')[2] # Determine the file extension.
                        r = urllib.request.urlopen(obj['media_url']) # Get the HTML request.
                        # Write the image data to a file.
                        fspec = "TwImage_%03d"
                        fileName = (fspec + '.' + ext) % image_counter
                        f = open(fileName,'wb')
                        f.write(r.read())
                        f.close()
                        # Append the file URL to the list.
                        images.append(fileName)
                        # Increment the counter.
                        image_counter = image_counter + 1
                        # If we've grabbed enough images, break.
                        if(image_counter >= MAX_IMAGES):
                            break
            if(image_counter >= MAX_IMAGES):
                break
        if(image_counter >= MAX_IMAGES):
            break
        oldest = tw[-1].id -1 # Get id of oldest tweet in the list, and subtract one.
        try:
            # Get PER_REQUEST more tweets starting just before the oldest one in the last
            # query.
            tw = api.user_timeline(screen_name = handle, count = PER_REQUEST, max_id = oldest)
            query_counter = query_counter + 1
        except tweepy.TweepyError as e:
            print(e.message)
            return {'error':e.message}
        if(query_counter > MAX_QUERY or len(tw) == 0):
            break

    return {'files':images,'fSpec':fspec,'count':image_counter}

def ConstructVideo(imData, maxRate, minDuration):
    if(minDuration <= 0):
        print('ConstructVideo() parameter error: \'minDuration\' must be a positive non-zero value') 
        return -2
    elif(maxRate <= 0):
        print('ConstructVideo() parameter error: \'maxRate\' must be a positive non-zero value')
        return -3
    if(imData['count'] < 1):
        print('ConstructVideo() parameter error: field \'count\' in \'imData\' is less than 1, indicating no images present')
        return -1
    fr = imData['count']/maxRate
    if(fr > maxRate):
        fr = maxRate
    # Setup FFMPEG command to concatentate the images.
    ff = FFmpeg(
        inputs = {imData['fSpec'] + '.jpg':'-loglevel quiet -y -framerate ' + fr},
        outputs = {'out.mp4':'-r ' + fr}
    )
    #print(ff.cmd)
    ff.run() # Invoke FFMPEG

    # Delete the files (jpeg and otherwise)
    for f in imData['files']:
        splt = f.rpartition('.')
        ext = splt[2]
        base = splt[0]
        # If the file was not a jpeg to begin with,
        # remove its original as well.
        if(ext != 'jpg'):
            os.remove(f)
        # Delete the jpeg.
        os.remove(base + '.jpg')

    return 0 # Indicate success


def CaptionImage(im):
    c = GVIdentify(im);
    caption = '';
    for word in c: # Make a list of random words (sprint 1)
        caption += word
        caption += '  '
    baseFileName = im.rpartition('.')[0] # Get the base file name.
    outName = baseFileName + '.jpg' # Convert to JPEG.
    # Expression to calculate the scale fatcor.
    scalexpr = '\'min('+str(SIZE[0])+'/iw,'+str(SIZE[1])+'/ih)\''
    # Setup FFMPEG command to scale the images, pad them, and add the caption.
    ff = FFmpeg(
        inputs = {im:'-loglevel quiet -y'},
        outputs = {outName:'-filter:v scale="iw*' + scalexpr + ':ih*' + scalexpr + 
            '",pad="' + str(BORDERSIZE[0]) + ':' + str(BORDERSIZE[1]) + ':(' + str(SIZE[0]) + 
            '- iw*' + scalexpr + ')/2:(' + str(SIZE[1]) + '- ih*' + scalexpr + 
            ')/2",drawtext="fontfile=./Butler_Regular.otf:text=\'' + caption + '\':x=(' + 
            str(BORDERSIZE[0]) + '-text_w)/2:y=' + str(round((SIZE[1]+BORDERSIZE[1])/2)) + 
            ':fontsize=20:fontcolor=white@1.0"'}
    )
    ff.run() # Invoke FFMPEG
    return baseFileName + '.jpg'
    

def GVIdentify(im):
    # Ininitiate the image annotator client.
    client = vision.ImageAnnotatorClient()
    # Open the image.
    with open(im,'rb') as f:
        imData = f.read()
    image = types.Image(content=imData)
    # Perform the detection
    det = client.label_detection(image=image)
    # Get the annotations
    annot = det.label_annotations
    # Retrieve just the descriptions from the labels
    content = []
    i = 0
    for label in annot:
        content.append(label.description)
        i += 1
        if(i >= MAX_ANNOTATIONS):
            break

    return content

