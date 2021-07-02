import time

def getPostLinks(link, driver):
    #INITIALIZE
    driver.get(link)
    driver.implicitly_wait(10)
    driver.maximize_window()
    posts = []
    following = driver.find_element_by_class_name('g47SY ').text.replace(',','')
    if 'k' in following:
        following.replace('k', '')
        following = int(float(following) * 1000)
    else:
        following = int(following)


    SCROLL_PAUSE_TIME = 5
    lastHeight = driver.execute_script("return document.body.scrollHeight")
    #GET LINKS
    while ((len(posts)) < 30) :
       driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
       time.sleep(SCROLL_PAUSE_TIME)
       posts = [None]
       posts = driver.find_elements_by_css_selector("div.v1Nh3.kIKUG._bz0w a")
       newHeight = driver.execute_script("return document.body.scrollHeight")
       lastHeight = newHeight
       if newHeight == lastHeight:
           break
       print(len(posts))

    #GMAKE LINK LIST
    links = []
    for i in posts:
        links.append(i.get_attribute("href"))

    return [links, following]


#-----------------------------------------------------------------
#-----------------------------------------------------------------
#-----------------------------------------------------------------
#-----------------------------------------------------------------
#-----------------------------------------------------------------
def getValues(driver):
    try:
        likes = driver.find_element_by_css_selector('button._8A5w5 > span').text.replace(',', '')
    except:
        return 0
    if 'k' in likes:
        likes.replace('k', '')
        likes = float(likes) * 1000
    else:
        likes = int(likes)

    return likes


def instaScrape(link, driver):
    data = getPostLinks(link, driver)
    links = data[0]
    folowing = data[1]
    eData = []
    for i in links:
        driver.get(i)
        eData.append(getValues(driver))
    if 0 in eData:
        eData.remove(0)
    average = 0
    if len(eData) != 0:
        average = sum( eData)/len(eData)
    return [average, folowing]


