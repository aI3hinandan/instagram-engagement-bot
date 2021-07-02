from Initialization import *
driver = getFirefoxDriver()

hashtag = 'indianmen'
driver.get(f'https://www.instagram.com/explore/tags/{hashtag}/')
sleep(2)
postLinks = []
index = 1
while len(postLinks) < 500:
    if index < 3:
        postLinks = driver.find_elements_by_class_name('_9AhH0')
        index += 1
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        print(len(postLinks))
        sleep(2)

        continue
    if index == 3:
        items = driver.find_elements_by_class_name('_9AhH0')[36:]
        postLinks = postLinks + items
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        print(len(postLinks))
        sleep(2)
        continue
    if index > 3:
        items = driver.find_elements_by_class_name('_9AhH0')[39:]
        postLinks = postLinks + items
        index += 1
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        print(len(postLinks))
        sleep(2)


