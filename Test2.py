# Test2.py
# Charles McPherson, Jr.

# This is a dumping ground for random test code to test elements of the program.
# For later projects, I will probably name this something less shit.

import tweepy
import urllib.request
import os
import time
#consumer_key = "vsRQBAfBv3tn4RTvdNSGlS8sa"
#consumer_secret = "8l2mhX3RMYl73OFWFitwnJ6yH7vVPq4ibevTptgkDkILCYKOvm"
#access_key = "1039252782048526337-AvoHPzZa745r6G2EjWKDakNaMU7hK5"
#access_secret = "pP5wZBibgb9P3kbJpNf9zTyodO1i0BBQMhOCHbAMkDlM3"

# Create auth object, and set its access token for API use.
#auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
#auth.set_access_token(access_key, access_secret)

# Initialize the API object.
#api = tweepy.API(auth)

# Grab exactly one tweet.
#tw = api.user_timeline(screen_name = "@MBTA",count=1,max_id = 1040165140384161792)

#print(tw)
# Grab and save the images in the tweet.
#nImages = 0;
#for mediaObj in tw[0].entities['media']:
#    if(mediaObj['type'] == 'photo'):
#        url = mediaObj['media_url']
#        ext = url.rpartition('.')[2]
#        r = urllib.request.urlopen(mediaObj['media_url'])
#        f = open('TwImage_' + str(nImages) + '.' + ext,'wb')
#        f.write(r.read())
#        f.close()
#
#(ffmpeg.input('./TwImage_*.jpg',pattern_type='glob',framerate=1)
#.filter('scale=iw*min(1920/iw,1080/ih):ih*min(1920/iw,1080/ih)')
#.filter('pad=1920:1080:(1920-iw*min(1920/iw,1080/ih))/2:(1080-ih*min(1920/iw,1080/ih))/2')
#.output('./TwMovie.mp4')
#.run()
#)
for i in range(3):
    os.system('ffmpeg -i TwImage_' + str(i) + '.jpg -y -filter:v \"scale=iw*min(1920/iw\\,1080/ih):ih*min(1920/iw\\,1080/ih), pad=1920:1080:(1920-min(1920/iw\\,1080/ih))/2:(1080-min(1920/iw\\,1080/ih))/2\" TwImage_' + str(i) + '.jpg')
time.sleep(1)
os.system('ffmpeg -f image2 -r 0.5 -i TwImage_%d.jpg -s 1920x1080 output.mp4');
# ffmpeg -i in.mp4 -filter:v "scale=iw*min($width/iw\,$height/ih):ih*min($width/iw\,$height/ih), pad=$width:$height:($width-iw*min($width/iw\,$height/ih))/2:($height-ih*min($width/iw\,$height/ih))/2" out.mp4
