############################################################################
# Name: Kevin Hou
# Date: May 4, 2017
#
# Project Name: VSCO Image Grabber
#
# Description:
#   Grabs VSCO images from the .webarchive's of a user
#   To get .webarchive's, go to each page of the user's VSCO
#       and save the page as a Web Archive (Command + S in Safari)
#   Store those .webarchive files in a subdirectory named 'vscoPages'
#   Prints the URLs of all the VSCO images found in the files
#
# Usage:
#   python vscoImageGrabber.py
############################################################################

################   User Settings   ################
# Ignore the profile picture
outputFileName = "vscoImages.js"
profilePictures = [
    "im.vsco.co/1/5596ee97bbcb95169892/575bb69d8c303b81438b456d/vsco_061016.jpg?w=100&amp;h=100&amp;fit=crop&amp;dpr=1",
    "im.vsco.co/1/5596ee97bbcb95169892/575bb69d8c303b81438b456d/vsco_061016.jpg?w=100&amp;h=100&amp;fit=crop&amp;dpr=2"
]
desiredWidth = "1200" # VSCO serves uses 300px width on the user's page

################   Imports   ################
from bs4 import BeautifulSoup # Module to sort through the html
import lxml # Module to parse through the html for BeautifulSoup
import urllib2 # Gets html
import webbrowser # This module can control the browser
import fileinput # To read files from input
import glob # Grabbing files with extensions
import os # Searching through computer directory
import io
from datetime import datetime # For timestamps

################   Find all VSCO pages   ################
files = [] # Valid files
os.chdir("./vscoPages/") # Search directory
for file in glob.glob("*.webarchive"): # Filter
    files.append(file) # Add file

################   Get image urls from webarchive files   ################
images = [] # URLs to all images

# Tag IDs
tagID = "<img alt=\"\" src=\"//"
endTagID = "\" width=\""

# Cycle through each file
for fileName in files:
    file = open(fileName, "r") # Open the file

    for line in file.readlines(): # Cycle through each line of the file
        if tagID in line: # If it contains a link
            startIndex = line.index(tagID) + len(tagID) # Get position of img
            endIndex = line.index(endTagID) # Get end position of link
            imgTag = line[startIndex:endIndex] # Cut the front of the line

            if imgTag not in profilePictures: # If not the profile picture
                if imgTag not in images: # Make sure don't add duplicates
                    largeImg = imgTag.replace("300", desiredWidth) # Change to 1200 resolution
                    images.append(largeImg) # Add to master array
    
    file.close()

################   Output to JS File   ################
print "{0} images found".format(images.count)
try:
    with io.FileIO(outputFileName, 'w') as outputFile: # Writing file and creating file if it doesn't exist
        print "// Last updated: " + datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        print "const vscoImages = ["
        outputFile.write("// Last updated: " + datetime.now().strftime('%Y-%m-%d %H:%M:%S')) # Timestamp
        outputFile.write("const vscoImages = [") # Open array
        for image in images:
            outputFile.write("  \"" + image + "\",") # Print
            print "  \"" + image + "\","
        outputFile.write("];") # Open array
        print "];"
        outputFile.close()
except IOError as (errno, strerror):
    print "I/O error({0}): {1}".format(errno, strerror)
