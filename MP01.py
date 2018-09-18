# MP01.py
# Charles A. McPherson, Jr.
# EC601 A1 - Fall 2018
# Mini-Project 1
#########################################################

import random
import tweepy
import urllib.request
from ffmpy import FFmpeg

MAX_IMAGES = 100 # Limit to 10 images at this point to prevent filling up the folder.
PER_REQUEST = 10 # Retreive 10 tweets at a time.
MAX_QUERY = 100 # Limit to 10 querys
SIZE = [640,260] # Frame size.
BORDERSIZE = [640,360] # Border size.

t_wordList = ['apple', 'orange', 'saxophone', 'armchair', 'Nikola Tesla', 
    'Steve McQueen', 'carptentry', 'nature', 'picture', 'ennui', 'failure',
    'nothing', 'something', 'wood', 'steel', 'fire', 'water', 'air', 'the void']

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
    if(minDuration < 0):
        return -1
    elif(maxRate < 0):
        return -1
    if(imData['count'] < 1):
        return -1
    fr = imData['count']/maxRate
    if(fr > maxRate):
        fr = maxRate
    # Setup FFMPEG command to concatentate the images.
    ff = FFmpeg(
        inputs = {imData['fSpec'] + '.jpg':'-loglevel quiet -y -framerate 1'},
        outputs = {'out.mp4':'-r 1'}
    )
    print(ff.cmd)
    ff.run() # Invoke FFMPEG
    return 0 # Indicate success


def CaptionImage(im):
    c = GVIdentify(im);
    caption = '';
    for word in c: # Make a list of random words (sprint 1)
        caption += ', '
        caption += word
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
            ')/2",drawtext="fontfile=/Library/Fonts/Arial.ttf:text=\'' + caption + '\':x=(' + 
            str(BORDERSIZE[0]) + '-text_w)/2:y=' + str(round((SIZE[1]+BORDERSIZE[1])/2)) + 
            ':fontsize=20:fontcolor=white@1.0"'}
    )
    ff.run() # Invoke FFMPEG
    return baseFileName + '.jpg'
    

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
