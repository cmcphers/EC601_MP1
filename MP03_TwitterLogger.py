# MP01_TwitterLogger.py
# Charles A. McPherson, Jr.

# This script executes the functions in the MP01 API to
# generate an annotated video from a Twitter library.

import MP01
import pymongo
import time

sessionID = time.time() # Get UNIX time. 
# Obtain twitter handle.
handle = input("Enter Twitter handle: ")
# Append '@' character if necessary.
if(handle[0] != '@'):
    handle = '@' + handle

# Open a connection to the MongoDB database (assuming localhost, port 27017)
client = pymongo.MongoClient()
try:
    # Use dummy command to check if db is available.
    client.admin.command('ismaster')
except pymongo.errors.ConnectionFailure:
    print("Database connection failed.  Ensure that 'mongod' is running")
    print("and listening on localhost at port 27017")
    quit()
# Open the database
db = client.MP03_TwitterDB_cmcphers
# Open the two collections.
sess = db.sessions
desc = db.descriptors

# Retrieve images from Twitter handle.
fileList = MP01.GetTwImages(handle)

# Caption images.
n = 0
L = len(fileList['files'])
for f in fileList['files']:
    print('\rAnalyzing: %d/%d' % (n,L),end='',flush=True)
    wordList = MP01.CaptionImage(f)
    if(len(wordList) > 0):
        # Insert entries into descriptors collection.
        desc.insert_many([{'session':sessionID,'image':n+1,'word':w} for w in wordList])
    n = n + 1
print('\rAnalyzing: %d/%d Done' % (n,L))

# Construct the video.
a = MP01.ConstructVideo(fileList,2,30)
if(a == -1):
    print("Failure in ConstructVideo()")
else:
    # Log the session information.
    sess.insert_one({'session':sessionID,'channel':handle,'images':L})
    print('Video created.')

client.close() # Close the MongoDB connection.
