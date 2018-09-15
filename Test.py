# Test.py
# Charles A. McPherson, Jr.

# This file contains test code for elements of the MP01 library.

import MP01

# Test code for GetTwImages()

fileList = MP01.GetTwImages('@MBTA')
print(fileList)

# Test code for CaptionImage()

t = []
for f in fileList:
    t.append(MP01.CaptionImage(f))

# Test code for ConstructVideo()

a = MP01.ConstructVideo(t,2,30)
if(a == -1):
    print("Failure in construct video")
