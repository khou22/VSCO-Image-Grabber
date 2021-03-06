# Name: Kevin Hou
# Date (of MVP): May 4, 2017
# Project Name: VSCO Image Grabber

# Description:
Grabs VSCO images from the .webarchive's of a user
To get .webarchive's, go to each page of the user's VSCO and save the page as a Web Archive (Command + S in Safari)
Store those .webarchive files in a subdirectory named 'vscoPages'
Prints the URLs of all the VSCO images found in the files

# Selenium Web Scrape
Because of complications with load times after clicking to the next image, the while loop will only terminate if there is an old file that contains the ID of an image the script is currently scraping. Therefore, it is imperitive that you keep `vscoDataSelenium-0000000000.js` in the directory to gaurentee a termination.

# Usage:
``` bash
$ python vscoImageGrabber.py
```
Requires downloading all pages of VSCO profile by going to the page on Chrome, opening the Inspector (Right click on anything -> Inspect) and navigating to the top of the document tree (`html`). Right click on `html` and click on `Copy->Copy outerHTML`. Paste this into a file named `SOME_NUMBER.html` in the same directory as `vscoImageGrabber.py`. Now you can run the script to grab all images.
