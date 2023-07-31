from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
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
profiles = driver.find_elements(By.CLASS_NAME, "card-worker")

# Consolidate list of profile links
profile_links = []

for profile in profiles:
    profile_links.append(profile.get_attribute("href"))

time.sleep(1)

# Visit worker profiles
for i,link in enumerate(profile_links[:3]):
    if(i == 0):
        driver.execute_script(f"window.open('{link}','_blank');")
        driver.switch_to.window(driver.window_handles[1])
    else:
        driver.get(link)

    time.sleep(1)

    button = driver.find_element(By.CLASS_NAME, "contact-js-btn")
    button.click()

    time.sleep(2)

driver.close()

# driver.quit()