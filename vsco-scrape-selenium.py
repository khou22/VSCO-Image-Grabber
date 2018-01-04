from selenium import webdriver
from selenium.webdriver.common.keys import Keys

# Incognito Chrome
option = webdriver.ChromeOptions()
option.add_argument("--incognito")

# Use the Chrome driver
driver = webdriver.Chrome(chrome_options=option)

# Initial URL (first image)
driver.get("http://vsco.co/khou22/media/5a49a6cc8fb562190c40cab8")

# Get the image
mainBody = driver.find_element_by_class_name("container")
image = mainBody.find_element_by_xpath(".//img").get_attribute("src")
print image

# Expose meta data
driver.find_element_by_class_name("DetailViewMetaCollapsible-button").click()

# Get meta data container
metaContainer = driver.find_element_by_class_name("DetailViewMetaCollapsible-meta-container")

# Get just date
# date = metaContainer.find_element_by_xpath(".//time/span").text

# Get date and time
time = metaContainer.find_element_by_xpath(".//time").text

# print date
print time

nextImageButton = driver.find_element_by_class_name('MouseAndKeyboardPagination-NextButton')
nextImageButton.click() # Go to next image

driver.close()
