from Initialization import *
import re





usernames = ["peeti.1k"]
driver = getFirefoxDriver()

POSTS_CSS = 'html.js.logged-in.client-root.js-focus-visible.sDN5V body div#react-root section._9eogI.E3X2T ' \
            'main.SCxLW.o64aR div.v9tJq.AAaSh.VfzDr div._2z6nI article.ySN3v div div div.Nnq7C.weEfm ' \
            'div.v1Nh3.kIKUG._bz0w a '
for username in usernames:
    link = f'https://www.instagram.com/{username}/'
    driver.get(link)
    driver.implicitly_wait(5)
    maxPosts = int(driver.find_elements_by_class_name('g47SY ')[0].text)
    followers = driver.find_elements_by_class_name('g47SY ')[1].text
    postElements = []
    postLinks = []
    index = 1

    while len(postLinks) < 500:
        if index < 4 :
            postLinks = driver.find_elements_by_css_selector(POSTS_CSS)
            index += 1
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            print(len(postLinks))
            sleep(2)

            continue
        if index == 4:
            postLinks = postLinks + (driver.find_elements_by_css_selector(POSTS_CSS)[36:])
            index += 1
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            print(len(postLinks))
            sleep(2)
            continue
        if index > 4:
            postLinks = postLinks + (driver.find_elements_by_css_selector(POSTS_CSS)[30:])
            index +=1
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            print(len(postLinks))
            sleep(2)


    print(len(postLinks))

