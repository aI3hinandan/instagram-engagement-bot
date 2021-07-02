from selenium import webdriver
from time import sleep, strftime
from selenium.webdriver.common.keys import Keys
def getFirefoxDriver(
        profileDir = 'C:/Users/abhin/AppData/Roaming/Mozilla/Firefox/Profiles/ozrlh87n.SelDriver'
):
    profile = webdriver.FirefoxProfile(profileDir)
    driver = webdriver.Firefox(profile)

    return driver