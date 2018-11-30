# MP03_TwitterAnalyzer
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

import sqlite3
import time

MAX_ENTRIES = 20

def Global_Stats(conn):
    c = conn.cursor()
    # Get number of sessions
    q = c.execute('SELECT * FROM sessions')
    sessions = q.fetchall()
    # Get average number of images per session
    avg = 0
    for s in sessions:
        avg = avg + s[3]
    avg = avg/len(sessions)
    # Get number of unique channels accessed
    q = c.execute('SELECT DISTINCT channel FROM sessions')
    channels = q.fetchall()
    
    print('')
    print('')
    print('Global Statistics')
    print('Number of sessions: %d' % len(sessions))
    print('Average number of images: %d' % avg)
    print('Number of channels queried: %d' % len(channels))
    print('')
    print('')

def Session_Info(conn):
    c = conn.cursor()
    # Get earliest and latest session timestamps
    q = c.execute('SELECT * FROM sessions ORDER BY session ASC LIMIT 1')
    tOld = time.localtime(q.fetchone()[1])
    q = c.execute('SELECT * FROM sessions ORDER BY session DESC LIMIT 1')
    tNew = time.localtime(q.fetchone()[1])

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
    q = c.execute('SELECT * FROM sessions WHERE session >= ? AND session <= ?',(time.mktime(tStart),time.mktime(tEnd)))
    sessionList = q.fetchall()
    print('{:^8s}{:^23s}{:^30s}{:^8s}'.format('ID','TIME STAMP','CHANNEL','IMAGES'))
    n = len(sessionList)
    if(n > MAX_ENTRIES):
        n = MAX_ENTRIES
    for i in range(n):
        sessionID = str(sessionList[i][0])
        sessionTime = time.strftime('%Y-%m-%d %I:%M:%S %p',time.localtime(sessionList[i][1]))
        sessionChan = sessionList[i][2]
        sessionImages = str(sessionList[i][3])
        print("{0:^8s}{1:^23s}{2:^30s}{3:^8s}".format(sessionID,
            sessionTime, sessionChan, sessionImages))
    print('')
    print('')

def Descriptors(conn):
    c = conn.cursor()
    # Get all unique descriptors
    q = c.execute('SELECT DISTINCT word FROM descriptors')
    words = q.fetchall()
    wordList = [x[0] for x in words] # Get word out of each tuple.
    counts = [0]*len(wordList)
    # Count the number of occurrences of each word
    for i in range(len(wordList)):
        q = c.execute("SELECT * FROM descriptors WHERE word=?",(wordList[i],))
        counts[i] = len(q.fetchall())
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
conn = sqlite3.connect('MP01_SQL.db')
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
            Global_Stats(conn)
            break
        elif(choice == '2'):
            Session_Info(conn)
            break
        elif(choice == '3'):
            Descriptors(conn)
            break
        elif(choice == '4'):
            quit = True
            break
        else:
            print('Invalid entry')
conn.close()
