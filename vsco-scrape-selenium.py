# Selenium
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

# Date parsing
from datetime import datetime
from dateutil.parser import parse
import calendar
import time

# Other
import glob # Grabbing files with extensions
import io

# Options
outputFileName = "vscoDataSelenium-[date].js"

# Incognito Chrome
option = webdriver.ChromeOptions()
option.add_argument("--incognito")

# Use the Chrome driver
driver = webdriver.Chrome("/usr/local/bin/chromedriver/chromedriver", chrome_options=option)

# Initial URL (first image)
driver.get("https://vsco.co/khou22/media/5c404ce942976801064ed4ac") # Latest image

# Testing
# driver.get("http://vsco.co/khou22/media/5596fc5328331ed9388b4569") # Last image
# driver.get("http://vsco.co/khou22/media/55abea862b331e0f258b456c") # Second to last image

# States
hasNextImage = True

# Master data
data = []

# Get the latest data set if possible
latestFile = None
for currentFile in glob.glob("vscoDataSelenium*.js"): # Filter
    if (latestFile == None):
        latestFile = currentFile
    if (latestFile <= currentFile): # Newer data
        latestFile = currentFile

# Parse in the contents of the file as a long string
latestData = ""
if (latestFile != None):
    print "Latest test file is: " + latestFile
    latestData = file(latestFile).read()

################   Webscrape VSCO   ################
while (hasNextImage):
    # Get the image ID from the URL
    imageID = driver.current_url.split('/')[-1] # Gets the ID of the image

    # If this image is already in the old data set, discontinue webscrape
    if imageID in latestData:
        hasNextImage = False # End while loop
        break # Break out of this iteration

    # Get the next button
    nextImageButton = driver.find_element_by_class_name('MouseAndKeyboardPagination-NextButton')

    if (nextImageButton.is_enabled()):
        # Get the image
        mainBody = driver.find_element_by_class_name("MediaBgColorWrapper--withRatio")
        image = mainBody.find_element_by_xpath(".//img").get_attribute("src")

        # Expose meta data
        driver.find_element_by_class_name("DetailViewMetaCollapsible-button").click()

        # Get meta data container
        metaContainer = driver.find_element_by_class_name("DetailViewMetaCollapsible-meta-container")

        # Get just date
        # date = metaContainer.find_element_by_xpath(".//time/span").text

        # Get date and time and parse
        parsedTime = metaContainer.find_element_by_xpath(".//time").text
        parsedDate = datetime.strptime(parsedTime, '%B %d, %Y %I:%M%p') # Example: July 03, 2015 2:19pm
        isoDate = parsedDate.isoformat()

        # Log to master data set
        data.append({ "id": imageID, "image": image, "date": isoDate })

        # print "Going to next image"
        nextImageButton.click() # Go to next image if exists
        # time.sleep(0.5) # To allow page loads

    # else: # Uncomment if only doing a small number of images
    #     print "No more images"
    #     # If no next image, terminate
    #     hasNextImage = False

driver.close()
print "{0} new image(s) found".format(len(data))

################   Output to JS File   ################
outputFileName = outputFileName.replace("[date]", str(calendar.timegm(time.gmtime()))) # Add epoche timestamp
print "Writing to file " + outputFileName
try:
    with io.FileIO(outputFileName, 'w') as outputFile: # Writing file and creating file if it doesn't exist
        outputFile.write("// Last updated: " + datetime.now().strftime('%Y-%m-%d %H:%M:%S') + "\n") # Timestamp
        outputFile.write("const vscoData = [\n") # Open array

        # Cycle through data
        for image in data:
            outputFile.write("  {\n")
            outputFile.write("    \"id\": \"" + image["id"] + "\",\n")
            outputFile.write("    \"image\": \"" + image["image"] + "\",\n")
            outputFile.write("    \"date\": \"" + image["date"] + "\"\n")
            outputFile.write("  },\n")

        # Append the data from the latest file
        if latestFile is not None:
            fp = open(latestFile)
            for i, line in enumerate(fp):
                if (i >= 2): # Start appending from the third line
                    outputFile.write(line) # Append
            fp.close()
        else:
            outputFile.write("];\n") # Close array
        outputFile.close()
except IOError as (errno, strerror):
    print "I/O error({0}): {1}".format(errno, strerror)
