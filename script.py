from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common import exceptions

import time

# Creates a dictionary that pairs the name of the skill with the corresponding number of stars
def parseSkills(html):
    html = html.split("\n")
    skills = []
    stars = []

    for line in html:
        # Find the skill name
        if(line.find("h5") != -1):
            skill = line[line.find(">") + 1:line.rfind("<")]
            skills.append(skill)
        # Count the number of stars
        if(line.find("/i") != -1):
            num_stars = line.count("fill")
            stars.append(num_stars)

    return dict(zip(skills, stars))



# Configuring browser options
options = Options()
options.add_experimental_option("detach", True)

driver = webdriver.Chrome(options=options)

# Read all necessary info from file
f = open("info", "r")
info = f.readlines()

# Visiting site
url = "https://onlinejobs.ph/login"
driver.get(url)

# Enter username
login_username = driver.find_element(By.ID, "login_username")

email = info[0]
login_username.send_keys(email + Keys.RETURN)

time.sleep(0.5)

# Enter password
login_password = driver.find_element(By.ID, "login_password")

password = info[1]
login_password.send_keys(password + Keys.RETURN)

time.sleep(1)

# Search for position
search = driver.find_element(By.NAME, "keyword")

position = info[2]
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

    try:
        warning = driver.find_element(By.CLASS_NAME, "text-warning")
    except exceptions.NoSuchElementException:
        # Read in desired qualifications
        desired_skills = info[3].split(",")
        desired_skill_level = info[4].split(",")

        # Remove trailing newlines from desired_skills and desired_skill_level
        desired_skills[-1] = desired_skills[-1][:-1]
        desired_skill_level[-1] = desired_skill_level[-1][:-1]

        # Pull full page source to analyze skills from
        page_source = driver.page_source
        # Narrow down search space
        skills_source = page_source[page_source.find("Top Skills"):page_source.find("Basic Information")]
        
        # Analyze skills
        skills_dict = parseSkills(skills_source)

        # Check to see if the number of skills they have is greater than or equal to the number of desired skills
        if(len(skills_dict) >= len(desired_skills)):
            skill_found = True
            index = 0
            # Verify if the candidate possesses the necessary skills
            # print(skills_dict)
            while(skill_found and index < len(desired_skills)):
                # print("desired: " + desired_skills[index])
                # print("stars: " + desired_skill_level[index])
                skill_found = desired_skills[index] in skills_dict and skills_dict[desired_skills[index]] >= int(desired_skill_level[index])
                # print(skill_found)
                index += 1

            # Contact the candidate if they possess the necessary skills
            if(skill_found):
                # Click contact button
                contact_button = driver.find_element(By.CLASS_NAME, "contact-js-btn")
                contact_button.click()

                time.sleep(0.2)

                # Enter subject
                info_subject = driver.find_element(By.ID, "info_subject")
                subject = info[5]
                info_subject.send_keys(subject)

                time.sleep(0.2)

                # Enter message
                info_message = driver.find_element(By.ID, "info_message")
                message = ''
                for line in info[6:]:
                    message += line

                info_message.send_keys(message)

                # # Click send message button
                # submit_button = driver.find_element(By.CLASS_NAME, "submit-msg")
                # submit_button.click()



    time.sleep(5)

driver.close()

# driver.quit()



# f = open("htmldump", "r")
# dump = f.read()

# print(parseSkills(dump))