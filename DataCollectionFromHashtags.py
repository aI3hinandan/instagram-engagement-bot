from Initialization import *
import re
from datetime import datetime
import pandas as pd

#DEFINITIONS######################################################################################################

def attribfElements(linkElements: list,attribute) -> list:
    linksList = []
    for i in linkElements:
        linksList.append(i.get_attribute(attribute))
    return linksList



def datetimepTime(timeString: str) -> float:
    utcTime = datetime.utcnow()
    postTime = datetime.strptime(timeString, "%Y-%m-%dT%H:%M:%S.000Z")
    difference = utcTime - postTime
    activeTime = (difference.total_seconds()/3600.00)  #active time in hours
    return (activeTime)

###################################################################################################################
def collectHashtagData(hashtag, driver: webdriver.Firefox):
    dataDict = {
        'username':[],
        'hashtag': [],
        'followers': [],
        'likes': [],
        'comments': [],
        'time':[],
        'link':[]
    }



    POSTS_CSS = 'html.js.logged-in.client-root.js-focus-visible.sDN5V body div#react-root section._9eogI.E3X2T main.SCxLW.o64aR article.KC1QD div div div.Nnq7C.weEfm div.v1Nh3.kIKUG._bz0w a'

    driver.get(f'https://www.instagram.com/explore/tags/{hashtag}/')
    sleep(2)
    postLinks = []
    index = 1
    while len(postLinks) < 500:
        if index < 3:
            postLinks = attribfElements(driver.find_elements_by_css_selector(POSTS_CSS), attribute='href')
            index += 1
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            print(len(postLinks))
            sleep(2)

            continue
        if index == 3:
            items = attribfElements(driver.find_elements_by_css_selector(POSTS_CSS)[36:], attribute='href')
            postLinks = postLinks + items
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            print(len(postLinks))
            sleep(2)
            continue
        if index > 3:
            items = attribfElements(driver.find_elements_by_css_selector(POSTS_CSS)[39:], attribute='href')
            postLinks = postLinks + items
            index += 1
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            print(len(postLinks))
            sleep(2)
    # we have the links ########################################################################################

    for i in postLinks:
        driver.get(i)
        try:
            while True:
                driver.find_element_by_class_name('glyphsSpriteCircle_add__outline__24__grey_9 u-__7').click()
        except:
            print("no more comments")

        try:
            timeString = driver.find_element_by_xpath('/html/body/div[1]/section/main/div/div[1]/article/div[2]/div[2]/a/time').get_attribute('datetime')
        except:
            continue
        time = datetimepTime(timeString)
        likes = 0
        try:
            likes = driver.find_element_by_xpath(
                '/html/body/div[1]/section/main/div/div[1]/article/div[2]/section[2]/div/div/button/span').text.replace(',','')
            if 'k' in likes:
                likes.replace('k', '')
                likes = float(likes) * 1000
            else:
                likes = int(likes)

        except:
            print('overflow likes')

        comments = -1
        try:
            comments = len(driver.find_elements_by_class_name('_8-yf5 ')) - 1
        except:

            print("overflow comments")
        try:
             username = driver.find_element_by_xpath('/html/body/div[1]/section/main/div/div[1]/article/header/div[2]/div[1]/div[1]/a').text
        except:
             username = "Not Found"

        driver.find_element_by_xpath('/html/body/div[1]/section/main/div/div[1]/article/header/div[2]/div[1]/div[1]/a').click()
        followers = -1
        try:
            followers = (driver.find_elements_by_class_name('g47SY ')[1].text).replace(',', '')
            if 'k' in followers:
                followers.replace('k', '')
                followers = float(followers) * 1000
            else:
                followers = int(followers)
        except:
            print('overflow followers')

        print((followers,likes,comments,time))
        dataDict['link'].append(i)
        dataDict['username'].append(username)
        dataDict['followers'].append(followers)
        dataDict['comments'].append(comments)
        dataDict['likes'].append(likes)
        dataDict['time'].append(time)
        dataDict['hashtag'].append(hashtag)

    return dataDict
#MAIN SCRIPT#######################################################################################################


driver = getFirefoxDriver()
driver.implicitly_wait(5)


hashtags = ['indianmen']
DataDicts = []
dataDict : dict
for hashtag in hashtags:
    dataDict = collectHashtagData(hashtag,driver)

path = r'D:\CollectedData.xlsx'
writer = pd.ExcelWriter(path)
df = pd.DataFrame(dataDict)
df.to_excel(writer,"Data")
writer.save()














