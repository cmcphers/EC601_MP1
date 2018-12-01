#MP03_TwitterAnalyzer
# Charles McPherson, Jr.

# Top-level Menu options:
# 1. View Global Statistics
# 2. View Session Info
# 3. View Most Common Descriptors
# 4. Quit

# Global Statistics
# Displays:
#   Number of sessions logged
#   Average number of images per session
#   Number of unique channels accessed

# Session Info
# Displays timestamp of first session and most recent session
# Prompts for start timestamp of range
# Prompts for end timestamp of range
# Displays up to 20 session IDs in the time range with all their information

# Most Common Descriptors
# Displays the 20 most common descriptors of all time

import pymongo
import time

MAX_ENTRIES = 20

def Global_Stats(sess):
    # Get list of sessions
    q = sess.find({})
    sessions = [s for s in q]
        
    # Get average number of images per session
    avg = 0
    for s in sessions:
        avg = avg + s['images']
    avg = avg/len(sessions)
    # Get number of unique channels accessed
    channels = sess.distinct('channel')
    
    print('')
    print('')
    print('Global Statistics')
    print('Number of sessions: %d' % len(sessions))
    print('Average number of images: %d' % avg)
    print('Number of channels queried: %d' % len(channels))
    print('')
    print('')

def Session_Info(sess):
    # Get earliest and latest session timestamps
    q = sess.find({}).sort('session',pymongo.ASCENDING)
    q = [s for s in q]
    tOld = time.localtime(q[0]['session'])
    q = sess.find({}).sort('session',pymongo.DESCENDING)
    q = [s for s in q]
    tNew = time.localtime(q[0]['session'])

    print('')
    print('')
    print('First session: %s - Latest session: %s' % 
        (time.strftime('%Y-%m-%d %I:%M:%S %p',tOld),
        time.strftime('%Y-%m-%d %I:%M:%S %p',tNew)))
    while True:
        r = input('Enter start time for search [YYYY-MM-DD HH:mm:ss (AM/PM)]: ')
        try:
            tStart = time.strptime(r,'%Y-%m-%d %I:%M:%S %p')
            break
        except ValueError:
            print('Format error. Ex: 2018-09-25 10:34:04 PM')
    while True:
        r = input('Enter end time for search [YYYY-MM-DD HH:mm:ss (AM/PM)]: ')
        try:
            tEnd = time.strptime(r,'%Y-%m-%d %I:%M:%S %p')
            break
        except ValueError:
            print('Format error. Ex: 2018-09-25 10:34:04 PM')
    q = sess.find({'session':{'$gte':time.mktime(tStart),'$lte':time.mktime(tEnd)}})
    sessionList = [s for s in q]
    print('{:^23s}{:^30s}{:^8s}'.format('TIME STAMP','CHANNEL','IMAGES'))
    n = len(sessionList)
    if(n > MAX_ENTRIES):
        n = MAX_ENTRIES
    for i in range(n):
        sessionTime = time.strftime('%Y-%m-%d %I:%M:%S %p',time.localtime(sessionList[i]['session']))
        sessionChan = sessionList[i]['channel']
        sessionImages = str(sessionList[i]['images'])
        print("{:^23s}{:^30s}{:^8s}".format(
            sessionTime, sessionChan, sessionImages))
    print('')
    print('')

def Descriptors(desc):
    # Get all unique descriptors
    wordList = desc.distinct('word') 
    counts = [0]*len(wordList)
    # Count the number of occurrences of each word
    for i in range(len(wordList)):
        q = desc.find({'word':wordList[i]})
        counts[i] = q.count()
    hist = sorted(zip(counts,wordList),reverse=True)
    sortedWords = [x for _,x in hist]
    sortedCounts = [x for x,_ in hist]

    print('')
    print('')
    print('Top %d Words' % MAX_ENTRIES)
    print('{:^30s}{:^8s}'.format('DESCRIPTOR','COUNT'))
    for i in range(MAX_ENTRIES):
        print('{:^30s}{:^8d}'.format(sortedWords[i],sortedCounts[i]))
    print('')
    print('')

#__main__()
# Open connection to MongoDB database (assuming localhost, port 27017)
client = pymongo.MongoClient()
try:
    # Use dummy command to check if db is available.
    client.admin.command('ismaster')
except pymongo.errors.ConnectionFailure:
    print("Database connection failed.  Ensure that 'mongod' is")
    print("running and listening on localhost at port 27017")
    quit()

# Open the database
db = client.MP03_TwitterDB_cmcphers
# Open the collections
sess = db.sessions
desc = db.descriptors

quit = False
while not quit:
    print('Twitter Analyzer')
    print('1. View Global Statistics')
    print('2. View Session Info')
    print('3. View Top %d Descriptors' % MAX_ENTRIES)
    print('4. Quit')
    while True:
        choice = input('Select an option: ')
        if(choice == '1'):
            Global_Stats(sess)
            break
        elif(choice == '2'):
            Session_Info(sess)
            break
        elif(choice == '3'):
            Descriptors(desc)
            break
        elif(choice == '4'):
            quit = True
            break
        else:
            print('Invalid entry')
client.close() # Close connection
