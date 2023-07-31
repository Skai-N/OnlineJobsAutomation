from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
# from selenium.common import exceptions

options = Options()
options.add_experimental_option("detach", True)

driver = webdriver.Chrome(options=options)

url = "https://onlinejobs.ph/login/"
driver.get(url)

search = driver.find_element(By.ID, "login_username")
print(search)

driver.quit()