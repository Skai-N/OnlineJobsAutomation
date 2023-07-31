from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
# from selenium.common import exceptions

import time

options = Options()
options.add_experimental_option("detach", True)

driver = webdriver.Chrome(options=options)

url = "https://onlinejobs.ph/login"
# url = "https://google.com"
driver.get(url)

login_username = driver.find_element(By.ID, "login_username")

f = open("credentials", "r")

email = f.readline()
login_username.send_keys(email + Keys.RETURN)
login_username.send_keys(Keys.RETURN)

time.sleep(.5)

login_password = driver.find_element(By.ID, "login_password")

password = f.readline()
login_password.send_keys(password + Keys.RETURN)

# time.sleep(2)

# print("sleep")

# body = driver.find_element_by_tag_name("body")
# body.send_keys(Keys.CONTROL + 'r')

# print("bop")

# try:
#     search = WebDriverWait(driver, 5).until(
#         EC.presence_of_element_located((By.NAME, "keyword"))
#     )

#     search = driver.find_element(By.NAME, "keyword")
#     WebDriverWait(driver, 5).until(EC.staleness_of(search))
# except :
#     driver.quit()

# driver.refresh()

# search = driver.find_element(By.ID, "searchform")
# WebDriverWait(driver, 5).until(EC.staleness_of(search))
# search = driver.find_element(By.ID, "searchform")

# position = f.readline()
# search.send_keys(position)
# search.send_keys(Keys.RETURN)

# time.sleep(5)

# driver.quit()