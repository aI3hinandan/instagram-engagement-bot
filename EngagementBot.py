from Initialization import *
import re
from datetime import datetime
import GenderDetection as gd
import commentsList as cl

import pandas as pd
#PARAMETERS################################################################
NO_HASHTAGS = 1


#FUNCTIONS#################################################################
def getElements(index):
    if index == 1:
        postLinks = driver.find_elements_by_class_name('_9AhH0')
        del postLinks[0:9]
        print(len(postLinks))
        return postLinks
    if index == 2:
        postLinks = driver.find_elements_by_class_name('_9AhH0')[33:]
        print(len(postLinks))
        return postLinks
    if index >= 3:
        postLinks = driver.find_elements_by_class_name('_9AhH0')[45:]
        print(len(postLinks))
        return postLinks


def checkConditions(likesVal, commentsVal, time, url, username: str):
    excludeList = ['men', 'style', 'outfit', 'fitness', 'cloth', 'apparel', 'body', 'shoes', 'fashion', 'trend','design','wear','shop','masculine', 'online', 'collection', 'tee', 'exclusive', 'celeb', 'face']
    for i in excludeList:
        if(i in username.lower()):
            return False
    genderResult = gd.getGender(url)
    if genderResult == -1 or genderResult == 0:
        return False
    time = datetimepTime(time)
    print("time:" + str(time))
    likesPara =  (likesVal/(time*60))
    print(likesPara)
    if time < 0.30 and likesPara > 0.3 and likesPara < 2:
        return True
    if time > 0.30 and time < 1.00 and likesVal> 10 and likesVal < 200  :
        return True
    elif time >1.00 and likesVal > 20 and likesVal < 400 and likesPara < 2:
        return True
    else:
        return False





#############################################################################
def datetimepTime(timeString: str) -> float:
    utcTime = datetime.utcnow()
    postTime = datetime.strptime(timeString, "%Y-%m-%dT%H:%M:%S.000Z")
    difference = utcTime - postTime
    activeTime = (difference.total_seconds()/3600.00)  #active time in hours
    return (activeTime)


############################################################################

############################################################################

#Defining the data Dictionary############################

dataDictBulk = {
    'link': [],
    'username': [],
    'comments': [],
    'likes': [],
    'time': [],
    'hashtag': []
}


pathBulk = r'D:\CollectedData.xlsx'
writerBulk = pd.ExcelWriter(pathBulk)

dataDictComments = {
        'link':[],
        'username': [],
        'comments': [],
        'likes': [],
        'time':[],
        'hashtag':[]
    }

pathComments = r'D:\CommentsData.csv'
##########################################################
def makeComments(postLinks: list):
    commentIndex = 0
    for link in postLinks:
        driver.get(link)
        commentBox = driver.find_element_by_class_name('Ypffh')
        commentBox.click()
        commentBoxEdit = driver.find_element_by_xpath('/html/body/div[1]/section/main/div/div[1]/article/div[2]/section[3]/div/form/textarea')
        comment = cl.commentGenerator(commentIndex)
        commentIndex += 1
        commentBoxEdit.send_keys(comment)
        print(f"1 Comment made: {comment}")
        sleep(200)
#Run######################################################
PREV_USER_LIST = pd.read_csv(r'D:\CommentsData.csv').iloc[:,1]
PREV_USER_LIST = list(PREV_USER_LIST)



driver = getFirefoxDriver()
driver.implicitly_wait(3)
hashtags = []
for i in range(0,NO_HASHTAGS):
    print(f"Enter Hashtag No.{i+1}: ")
    hashtags.append(input())

for hashtag in hashtags:
    driver.get(f'https://www.instagram.com/explore/tags/{hashtag}/')
    sleep(2)
    selectedPosts = []
    usernames = []
    posts= []
    roller = 0
    index = 0
    while len(selectedPosts) < 5:
        exVal = 0
        if (roller != 0) and (roller+1 == (len(posts))):
            roller = 0
            if index >0:
                driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            index +=1
            posts = getElements(index)
        elif (roller == 0) :
            if index >0:
                driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            index +=1
            posts = getElements(index)

        ########################################################
        try:
            posts[roller].click()
            roller += 1
        except Exception:
            print(f"skipped{roller}")
            print(Exception)
            print

            exit(329)
            roller += 1
            continue
        ########################################################
        try:
            username = driver.find_element_by_class_name('e1e1d').find_element_by_tag_name("a").text
        except:
            exVal = -1
            driver.find_element_by_xpath("/html/body/div[4]/div[3]/button").click()
            print("username not found")
            continue

        if username in PREV_USER_LIST:
            driver.find_element_by_xpath("/html/body/div[4]/div[3]/button").click()
            continue
        try:
            while True:
                driver.find_element_by_class_name('glyphsSpriteCircle_add__outline__24__grey_9 u-__7').click()
        except:
            print("no more comments")
        ########################################################
        try:
            time = driver.find_element_by_xpath('/html/body/div[4]/div[2]/div/article/div[2]/div[2]/a/time').get_attribute('datetime')
        except:
            exVal = -1
            print("time not found")
        likes = 0
        try:
            likes = driver.find_element_by_class_name(
                'Nm9Fw').find_element_by_tag_name('span').text.replace(',','')
            if 'k' in likes:
                likes.replace('k', '')
                likes = float(likes) * 1000
            else:
                likes = int(likes)
        except:
            print('overflow likes')



        comments = -1
        try:
            comments = (len(driver.find_elements_by_class_name('_8-yf5 ')) - 9)/2
        except:
            print("overflow comments")

        dataDictBulk['link'].append(driver.current_url)
        dataDictBulk['username'].append(username)
        dataDictBulk['comments'].append(comments)
        dataDictBulk['likes'].append(likes)
        dataDictBulk['time'].append(time)
        dataDictBulk['hashtag'].append(hashtag)


        print(username, comments, likes, time, hashtag)
        result = checkConditions(likesVal= likes, commentsVal= comments, time= time,url= driver.current_url, username= username)
        print(result)
        if result == True:
            selectedPosts.append(driver.current_url)
            print(len(selectedPosts))

            dataDictComments['link'].append(driver.current_url)
            dataDictComments['username'].append(username)
            dataDictComments['comments'].append(comments)
            dataDictComments['likes'].append(likes)
            dataDictComments['time'].append(time)
            dataDictComments['hashtag'].append(hashtag)

        driver.find_element_by_xpath("/html/body/div[4]/div[3]/button").click()



    makeComments(selectedPosts)



dfc = pd.DataFrame(dataDictComments)
dfc.to_csv(pathComments, mode='a')





df = pd.DataFrame(dataDictBulk)
df.to_csv(pathBulk,mode='a')
writerBulk.save()










