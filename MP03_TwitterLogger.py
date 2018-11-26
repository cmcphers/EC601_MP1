# MP01_TwitterLogger.py
# Charles A. McPherson, Jr.

# This script executes the functions in the MP01 API to
# generate an annotated video from a Twitter library.

import MP01
import sqlite3
import time

sessionID = time.time() # Get UNIX time. 
# Obtain twitter handle.
handle = input("Enter Twitter handle: ")
# Append '@' character if necessary.
if(handle[0] != '@'):
    handle = '@' + handle

# Open a connection to the SQL database.
conn = sqlite3.connect('MP01_SQL.db')
c = conn.cursor()

# Retrieve images from Twitter handle.
fileList = MP01.GetTwImages(handle)

# Caption images.
n = 0
L = len(fileList['files'])
for f in fileList['files']:
    print('\rAnalyzing: %d/%d' % (n,L),end='',flush=True)
    wordList = MP01.CaptionImage(f)
    c.execute("SELECT * FROM descriptors ORDER BY id DESC LIMIT 1")
    rows = c.fetchall()
    if(len(rows) == 0):
        rowID = 0
    else:
        rowID = rows[0][0]+1
    for word in wordList:
        c.execute("INSERT INTO descriptors VALUES (?, ?, ?, ?)",(rowID, sessionID, n+1, word))
        rowID = rowID + 1
    n = n + 1
print('\rAnalyzing: %d/%d Done' % (n,L))


# Construct the video.
a = MP01.ConstructVideo(fileList,2,30)
if(a == -1):
    print("Failure in ConstructVideo()")
else:
    # Log the session information.
    c.execute("SELECT * FROM sessions ORDER BY id DESC LIMIT 1")
    rows = c.fetchall()
    if(len(rows) == 0):
        c.execute("INSERT INTO sessions VALUES (?, ?, ?, ?)",(0, sessionID, handle, L))
    else:
        c.execute("INSERT INTO sessions VALUES (?, ?, ?, ?)",(row[0][0]+1, sessionID, handle, L))
    conn.commit() # Since all execution completed successfully, commit the database changes.
    print('Video created.')

conn.close() # Close the SQL connection.
