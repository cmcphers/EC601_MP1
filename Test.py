# Test.py
# Charles A. McPherson, Jr.

# This file contains test code for elements of the MP01 library.

import MP01

# Test code for GetTwImages()
fileList = MP01.GetTwImages('@the_moviebob')
#fileList = MP01.GetTwImages('@Charles32752654')
print(fileList)

# Test code for CaptionImage()
t = []
for f in fileList['files']:
    print(f)
    t.append(MP01.CaptionImage(f))

# Test code for ConstructVideo()

a = MP01.ConstructVideo(fileList,2,30)
if(a == -1):
    print("Failure in construct video")
