from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from bs4 import BeautifulSoup
from time import sleep

#getting the account name from the user
account_name = 'elon musk'
driver = webdriver.Chrome('C:/Users/user/chromedriver.exe')
driver.maximize_window()
driver.get('https://twitter.com/login')
sleep(4)

#log in to twitter
email = driver.find_element_by_xpath('//*[@id="layers"]/div/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div/div/div/div[5]/label/div/div[2]/div/input')
email.send_keys('twitter email', Keys.ENTER)
sleep(1)
username = driver.find_element_by_xpath('//*[@id="layers"]/div/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div[1]/div/div[2]/label/div/div[2]/div/input')
username.send_keys('username', Keys.ENTER)
sleep(1)
password = driver.find_element_by_xpath('//*[@id="layers"]/div/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div[1]/div/div/div[3]/div/label/div/div[2]/div[1]/input')
password.send_keys('password', Keys.ENTER)

#waiting for the search box to show up
WebDriverWait(driver, 5).until(
    EC.presence_of_element_located((By.XPATH, '//*[@id="react-root"]/div/div/div[2]/main/div/div/div/div[2]/div/div[2]/div/div/div/div[1]/div/div/div/form/div[1]/div/div/div/label/div[2]/div/input')))

#searching for the target
search_box = driver.find_element_by_xpath('//*[@id="react-root"]/div/div/div[2]/main/div/div/div/div[2]/div/div[2]/div/div/div/div[1]/div/div/div/form/div[1]/div/div/div/label/div[2]/div/input')
search_box.send_keys(account_name, Keys.ENTER)
sleep(1)

#clicking on people tab and selecting the first account
people_tab = driver.find_element_by_xpath('//*[@id="react-root"]/div/div/div[2]/main/div/div/div/div/div/div[1]/div[1]/div[2]/nav/div/div[2]/div/div[3]/a/div')
people_tab.click()
sleep(2)
first_account = driver.find_element_by_xpath('//*[@id="react-root"]/div/div/div[2]/main/div/div/div/div/div/div[3]/div/section/div/div/div[1]/div/div/div')
first_account.click()
sleep(2)

# scraping data
soup = BeautifulSoup(driver.page_source, 'lxml')
unfiltered_tweets = []
scroller = 0
content = soup.find_all('div', class_ = 'css-901oao r-18jsvk2 r-37j5jr r-a023e6 r-16dba41 r-rjixqe r-bcqeeo r-bnwqim r-qvutc0')
while True:
    scroller += 2000
    for tweet in content:
        unfiltered_tweets.append(tweet.text)
    driver.execute_script(f'window.scrollTo(0, {scroller})')
    sleep(2)
    soup = BeautifulSoup(driver.page_source, 'lxml')
    content = soup.find_all('div', class_ = 'css-901oao r-18jsvk2 r-37j5jr r-a023e6 r-16dba41 r-rjixqe r-bcqeeo r-bnwqim r-qvutc0')
    tweets = list(set(unfiltered_tweets))
    if len(tweets) >= 300: #put any num here as long as it doesn't exceed the num of tweets
        break
    
#informing the user that scraping has finished and closing the browser
print('process finished successfully')
driver.close()