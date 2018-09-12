# Test2.py
# Charles McPherson, Jr.

# This is a dumping ground for random test code to test elements of the program.
# For later projects, I will probably name this something less shit.

import tweepy
import urllib.request

consumer_key = "vsRQBAfBv3tn4RTvdNSGlS8sa"
consumer_secret = "8l2mhX3RMYl73OFWFitwnJ6yH7vVPq4ibevTptgkDkILCYKOvm"
access_key = "1039252782048526337-AvoHPzZa745r6G2EjWKDakNaMU7hK5"
access_secret = "pP5wZBibgb9P3kbJpNf9zTyodO1i0BBQMhOCHbAMkDlM3"

# Create auth object, and set its access token for API use.
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_key, access_secret)

# Initialize the API object.
api = tweepy.API(auth)

# Grab exactly one tweet.
tw = api.user_timeline(screen_name = "@Charles32752654",count=1)

# Grab and save the images in the tweet.
nImages = 0;
for mediaObj in tw[0].entities['media']:
    if(mediaObj['type'] == 'photo'):
        url = mediaObj['media_url']
        ext = url.rpartition('.')[2]
        r = urllib.request.urlopen(mediaObj['media_url'])
        f = open('TwImage_' + str(nImages) + '.' + ext,'wb')
        f.write(r.read())
        f.close()

