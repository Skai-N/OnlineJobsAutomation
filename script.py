from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
# from selenium.common import exceptions

import time

# Configuring browser options
options = Options()
options.add_experimental_option("detach", True)

driver = webdriver.Chrome(options=options)

# Visiting site
url = "https://onlinejobs.ph/login"
driver.get(url)

# Enter username
login_username = driver.find_element(By.ID, "login_username")

f = open("credentials", "r")

email = f.readline()
login_username.send_keys(email + Keys.RETURN)

# Enter password
login_password = driver.find_element(By.ID, "login_password")

password = f.readline()
login_password.send_keys(password + Keys.RETURN)

time.sleep(1)

# Search for position
search = driver.find_element(By.NAME, "keyword")

position = f.readline()
search.send_keys(position + Keys.RETURN)

time.sleep(1)

# Find all worker profiles
profiles = driver.find_elements(By.TAG_NAME, "a")

print(profiles)

# driver.quit()