from Initialization import *

def checkAndGetUser(username):
        result = [0,0]
        driver.get()  #get link of user
        if len(driver.find_elements_by_class_name('QlxVY')) != 0 and len(driver.find_elements_by_class_name('QlxVY').find_element_by_class_name('rkEop')) != 0:
                return 0
        followers = str(driver.find_elements_by_class_name('g47SY ')[1].text).lower()
        followers.replace(',', '')
        if 'k' in followers:
                followers.replace('k', '')
                followers = int(float(followers) * 1000)
        else:
                followers = int(followers)

        if followers > 500:
                return 0
        postLink = driver.find_elements_by_class_name('v1Nh3 kIKUG  _bz0w')[0].find_element_by_tag_name('a').get_attribute('href')
        return postLink

driver = getFirefoxDriver()
print("Enter Username to follow from:\n")
#username = input()
username = 'fashionwear.men'
driver.get(f'https://www.instagram.com/{username}')
driver.find_elements_by_class_name('-nal3 ')[1].click()
driver.implicitly_wait(5)
items = []
for i in (1,10):
        items =driver.find_elements_by_class_name('FPmhX notranslate  _0imsa ')
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        sleep(2)
        print(len(items))