from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common import exceptions
from selenium.webdriver.support.ui import Select

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

# Keep track of what info to load from the info array
info_index = 0

# Visiting site
url = "https://onlinejobs.ph/login"
driver.get(url)

# Enter username
login_username = driver.find_element(By.ID, "login_username")

email = info[info_index]
info_index += 1
login_username.send_keys(email + Keys.RETURN)

time.sleep(0.5)

# Enter password
login_password = driver.find_element(By.ID, "login_password")

password = info[info_index]
info_index += 1
login_password.send_keys(password + Keys.RETURN)

time.sleep(1)

# Search for position
search = driver.find_element(By.NAME, "keyword")

position = info[info_index]
info_index += 1
search.send_keys(position + Keys.RETURN)

time.sleep(1)

# Select the employment type
employment_types = ["Any", "Full Time", "Part Time", "Gig"]
employment_type = employment_types.index(info[info_index][:-1])
info_index += 1
select = Select(driver.find_element(By.NAME, "employmenttype"))
select.select_by_index(employment_type)

# Get all sliders
sliders = driver.find_elements(By.XPATH, "//span[@tabindex]")

# Change minimum availability
min_availability = int(info[info_index][:-1])
info_index += 1 
availability = sliders[0]
actions = ActionChains(driver)

match min_availability:
    case 10:
        offset = 110
    case 11:
        offset = 120
    case 12:
        offset = 135
    case _:
        offset = (min_availability - 2) * 15

actions.drag_and_drop_by_offset(availability, offset, 0).perform()

# Change maximum salary
max_salary = int(info[info_index][:-1])
info_index += 1
salary = sliders[3]

match max_salary:
    case 100:
        offset = 2
    case 95:
        offset = -5
    case 90:
        offset = -12
    case 85:
        offset = -19
    case 80:
        offset = -27
    case 75:
        offset = -33
    case 70:
        offset = -40
    case 65:
        offset = -48
    case 60:
        offset = -55
    case 55:
        offset = -62
    case 50:
        offset = -69
    case 45:
        offset = -76
    case 40:
        offset = -83
    case 35:
        offset = -90
    case 30:
        offset = -97
    case 25:
        offset = -104
    case 20:
        offset = -112
    case 15:
        offset = -119
    case 10:
        offset = -126
    case 5:
        offset = -133

actions.drag_and_drop_by_offset(salary, offset, 0).perform()

# Select the minimum ID proof score
min_proof_score = info[info_index][:-1]
info_index += 1
select = Select(driver.find_element(By.NAME, "trust"))
if(int(min_proof_score) != -1):
    select.select_by_value(min_proof_score) # Valid entries: 30 - 70 incremented by 5

# Select the maximum inactivity range
max_inactivity = info[info_index][:-1]
info_index += 1
select = Select(driver.find_element(By.ID, "addate"))
if(int(max_inactivity) != -1):
    select.select_by_value(max_inactivity) # Valid entries: 7, 31, 93, 186, 366

# Select the IQ
IQs = ["Any", "extremely-high", "very-high", "high-average", "average"]
IQ = IQs.index(info[info_index][:-1])
info_index += 1
select = Select(driver.find_element(By.NAME, "testIQ"))
if(IQ > 0):
    select.select_by_index(IQ)

# Select the English score
score = info[info_index][:-1]
info_index += 1
select = Select(driver.find_element(By.NAME, "englishScore"))
if(int(score) != -1):
    select.select_by_value(score) # Valid entries: 14, 12, 10, 8, 6, 4

# Refine the search
searches = driver.find_elements(By.NAME, "keyword")
searches[1].send_keys(Keys.ENTER)

time.sleep(1)

# Load the maximum number of profiles to scrape, used to keep track of how many more profiles should be scraped
max_profiles = int(info[info_index][:-1])
info_index += 1

# Consolidate list of profile links
profile_links = []

while(max_profiles > 0):
    # Find all worker profiles
    profiles = driver.find_elements(By.CLASS_NAME, "card-worker")

    # Modify early to prevent overflow of profile link amount
    max_profiles -= len(profiles)

    if(max_profiles >= 0):
        for profile in profiles:
            profile_links.append(profile.get_attribute("href"))

        # Go to the next page if possible
        shortcuts = driver.find_elements(By.XPATH, "//a[@aria-label]")
        
        labels = []
        for shortcut in shortcuts:
            labels.append(shortcut.get_attribute("aria-label"))

        if("Next" in labels):
            shortcuts[1].click()
        else:
            max_profiles = -1

    else:
        for profile in profiles[:max_profiles + len(profiles)]:
            profile_links.append(profile.get_attribute("href"))

    time.sleep(1)

# Store the current info index so that looping through worker profiles doesn't make unintended changes
original_info_index = info_index

# Visit worker profiles
for i,link in enumerate(profile_links):
    info_index = original_info_index

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
        desired_skills = info[info_index].split(",")
        info_index += 1
        desired_skill_level = info[info_index].split(",")
        info_index += 1

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
                subject = info[info_index]
                info_index += 1
                info_subject.send_keys(subject)

                time.sleep(0.2)

                # Enter message
                info_message = driver.find_element(By.ID, "info_message")
                message = ''
                for line in info[info_index:]:
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