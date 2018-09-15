# MP01.py
# Charles A. McPherson, Jr.
# EC601 A1 - Fall 2018
# Mini-Project 1
#########################################################

import random
import tweepy
import urllib.request

MAX_IMAGES = 4 # Limit to 10 images at this point to prevent filling up the folder.
PER_REQUEST = 10 # Retreive 10 tweets at a time.
MAX_QUERY = 20 # Limit to 10 querys

consumer_key = "vsRQBAfBv3tn4RTvdNSGlS8sa"
consumer_secret = "8l2mhX3RMYl73OFWFitwnJ6yH7vVPq4ibevTptgkDkILCYKOvm"
access_key = "1039252782048526337-AvoHPzZa745r6G2EjWKDakNaMU7hK5"
access_secret = "pP5wZBibgb9P3kbJpNf9zTyodO1i0BBQMhOCHbAMkDlM3"

t_wordList = ['apple', 'orange', 'saxophone', 'armchair', 'Nikola Tesla', 
    'Steve McQueen', 'carptentry', 'nature', 'picture', 'ennui', 'failure',
    'nothing', 'something', 'wood', 'steel', 'fire', 'water', 'air', 'the void']

def GetTwImages(handle):
    # For sprint 2, extract the images from the tweets, extract file names,
    # and save the actual files to disk.

    # Initialize the TweePy API
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_key, access_secret)
    api = tweepy.API(auth)

    # Grab newest tweets.
    try:
        tw = api.user_timeline(screen_name = handle, count = PER_REQUEST)
    except tweepy.TweepyError as e:
        print(e.message)
        return []
    
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
                        f = open('TwImage_' + str(image_counter) + '.' + ext,'wb')
                        f.write(r.read())
                        f.close()
                        # Append the file URL to the list.
                        images.append(url)
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
            return []
        if(query_counter > MAX_QUERY or len(tw) == 0):
            break

    return images

def ConstructVideo(images, maxRate, minDuration):
    if(minDuration < 0):
        return -1
    elif(maxRate < 0):
        return -1
    nImages= len(images)
    if(nImages < 0):
        return -1
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
