# Test.py
# Charles A. McPherson, Jr.

# This file contains test code for elements of the MP01 library.

import MP01

# Test code for GetTwImages()

fileList = MP01.GetTwImages('FrankReynolds.txt')
print(fileList)

# Test code for CaptionImage()

for f in fileList:
    t = MP01.CaptionImage(f)
    print(t)
