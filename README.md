MP01.py

I - Installation Instructions:

1. Reconfigure and Install FFMPEG (if necessary)
For the MP01 library to function as intended, FFMPEG must be installed with the
—enable-libfreetype option.  To do this:

    a. Download FFMPEG https://www.ffmpeg.org/
    b. Navigate to the FFMPEG download folder.
    c. Run ‘./configure —enable-libfreetype’
        If already installed, be sure to include any options previously included (run ffmpeg from the Terminal and look at the ‘configuration:’ line to be sure.
    d. Run ‘make’ to build the application with this new configurationm
    e. Run ‘make install’ to install it.

2. Install ffmpy (if necessary)
    a. Run ‘pip install ffmpy’ from the Terminal

3. Install tweepy (if necessary)
    a. Run ‘pip install tweepy’ from the Terminal

2. Create key file for Twitter API

    a. Open a text new text file called ‘keys.txt’
    b. On each line, enter your consumer key, consumer secret, access key, and access secret.  For example:  If you had the following keys:

        consumer key = 1234567
        consumer secret = 890123456
        access key = 7890123
        access secret = 456789012

        the file would simply contain 4 lines:

        1234567
        890123456
        7890123
        456789012

    c. Save the file and leave it in the directory with ‘MP01.py’

II - Use

The MP01.py library contains 4 functions:
#################################################
imData = GetTwImages( handle )
#################################################
This function searches the 1,000 most recent tweets of the user indicated by ‘handle’ and extracts up to 100 images and saves them.

    handle - A string containing the user’s Twitter handle (Ex. @the_moviebob)

    imData - This is a dictionary containing 3 entries:
        ‘files’ - A list of file names.
        ‘fSpec’ - A string containing the format specifier for the image file naming convention.
        ‘count’ - The number of downloaded images.
#################################################
fName = CaptionImage( im )
#################################################
This function passes an image through the Google Vision API to retrieve a list of appropriate caption words.  The file is then resized, captioned, and saved as a jpeg.

    im - A string containing the name of the image file

    fName - The name of the saved image file (will be the same as ‘im’ unless the original was not in jpeg format.
#################################################
content = GVIdentify( im )
#################################################
This function passes the given image through the Google Cloud Vision API and retrieves up to 3 annotations.

    im - A string containing the name of the image file.

    content - A list of annotation strings (up to 3).
#################################################
res = ConstructVideo( imData, maxRate, minDuration )
#################################################
This function concatenates the frames into an ‘mp4’ video file.

    imData - A dictionary object as returned by ‘GetTwImages()’
    maxRate - A maximum frame rate to cap the video (in frames per second).
    minDuration - A minimum duration for the video (in seconds).

    res - An integer indicating success or failure:
        0 - Success
        -1 - Count of zero images in ‘imData’ dictionary
        -2 - MinDuration is zero or less than zero
        -3 - MaxRate is zero or less than zero
#################################################

III Notes:

Some videos returned by FFMPEG are not properly playable in Apple Quicktime, which supports a limited number of codecs and formats.  However, these videos should play without issue in VLC, which can be obtained from:

    https://www.videolan.org/vlc/
