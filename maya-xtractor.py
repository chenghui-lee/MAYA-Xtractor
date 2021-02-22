# MAYA Xtractor
# https://github.com/chenghui-lee/maya-xtractor

import os
import time
import random
import datetime
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
import pandas as pd
from bs4 import BeautifulSoup
import env

options = Options()
if os.environ.get("HEADLESS") == 'True' :
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')
driver = webdriver.Chrome(executable_path= os.environ.get("PATH"),options=options)
listOfFaculty = ["FACULTY OF ARTS AND SOCIAL SCIENCES","FACULTY OF BUILT ENVIRONMENT","FACULTY OF BUSINESS AND ACCOUNTANCY","FACULTY OF DENTISTRY","FACULTY OF ECONOMICS AND ADMINISTRATION","CENTRE FOR FOUNDATION STUDIES IN SCIENCE","UNIVERSITY","INSTITUTE FOR ADVANCED STUDIES","ACADEMY OF ISLAMIC STUDIES","ACADEMY OF MALAY STUDIES","FACULTY OF ENGINEERING","FACULTY OF LAW","FACULTY OF MEDICINE","FACULTY OF PHARMACY","FACULTY OF EDUCATION","ASIA EUROPE INSTITUTE","CULTURAL CENTRE","FACULTY OF SCIENCE","FACULTY OF LANGUAGES AND LINGUISTICS","LIBRARY","CENTRE FOR SPORT & EXERCISE SCIENCES","FACULTY OF COMPUTER SCIENCE AND INFORMATION TECHNOLOGY","INTERNATIONAL INSTITUTE OF PUBLIC POLICY AND MANAGEMENT"]


def login(username, password):	
    driver.get("https://maya.um.edu.my/sitsvision/wrd/siw_lgn")
    driver.find_element_by_id("MUA_CODE.DUMMY.MENSYS").send_keys(username)
    driver.find_element_by_id("PASSWORD.DUMMY.MENSYS").send_keys(password)
    driver.find_element_by_name("BP101.DUMMY_B.MENSYS").click()
    driver.implicitly_wait(5)
    
    curURL = driver.current_url
    if "portal" in curURL :
        now = datetime.datetime.now()
        print("Successfully login. Time:", now.strftime("%Y-%m-%d %H:%M:%S"))
        return True
    else:
        return False  

def scrape(index):
    try:
        driver.find_elements_by_xpath("//li")[0].click() # Home
        driver.implicitly_wait(5)
        driver.find_element_by_xpath("//div/div/div/div/div/div/div/a/div/div[1]").click() # Timetable
        driver.implicitly_wait(1)
        driver.find_element_by_xpath("//body/div[2]/div[2]/center/div/div/div[3]/a").click() # Search Timetable
        driver.implicitly_wait(3)
        # Select year
        driver.find_elements_by_xpath("//div[contains(@tabindex, '-1')]")[0].click()
        driver.find_element_by_xpath("//div/input[contains(@aria-label,'Year')]").send_keys("2020/2021")
        driver.find_element_by_xpath("//div/input[contains(@aria-label,'Year')]").send_keys(Keys.ENTER)
        
        # Select Semester
        driver.find_elements_by_xpath("//div[contains(@tabindex, '-1')]")[1].click()
        driver.find_element_by_xpath("//div/input[contains(@aria-label,'Slot')]").send_keys("SEMESTER 2")
        for i in range (8):
            driver.find_element_by_xpath("//div/input[contains(@aria-label,'Slot')]").send_keys(Keys.ARROW_DOWN)
        driver.find_element_by_xpath("//div/input[contains(@aria-label,'Slot')]").send_keys(Keys.ENTER)

        # Select Faculty
        driver.find_elements_by_xpath("//div[contains(@tabindex, '-1')]")[2].click()
        driver.find_element_by_xpath("//div/input[contains(@aria-label,'Faculty')]").send_keys(listOfFaculty[index])
        driver.find_element_by_xpath("//div/input[contains(@aria-label,'Faculty')]").send_keys(Keys.ENTER)

        # Press Search Button
        searchBut = driver.find_element_by_name("BP103.DUMMY_B.MENSYS.1")
        driver.execute_script("arguments[0].scrollIntoView(true);", searchBut)
        searchBut.click()

        # Wait for database to load
        hasFirstPage = False
        driver.find_element_by_xpath("//h1")
        time.sleep(3)
        
        # Capture the first page of the table
        soup = BeautifulSoup(driver.page_source, 'lxml')
        tables = soup.find_all('table')
        dfs = pd.read_html(str(tables))
        df = pd.DataFrame(dfs[1])
        hasFirstPage = True

        # For every pages
        button = driver.find_element_by_link_text("Next")
        WebDriverWait(driver, 10).until(expected_conditions.visibility_of_element_located((By.LINK_TEXT, "Next")))
        elem = driver.find_element_by_xpath("//*[@id='DataTables_Table_0_info']")
        driver.execute_script("arguments[0].scrollIntoView(true);", elem)  
        button.click()

        try: 
            while driver.find_element_by_xpath("//li[@class='paginate_button next']") :
                        soup = BeautifulSoup(driver.page_source, 'lxml')
                        tables = soup.find_all('table')
                        dfs = pd.read_html(str(tables))
                        new_df = pd.DataFrame(dfs[1])
                        df = df.append(new_df, ignore_index=True, sort=False)

                        button = driver.find_element_by_link_text("Next")
                        WebDriverWait(driver, 5).until(expected_conditions.visibility_of_element_located((By.LINK_TEXT, "Next")))
                        elem = driver.find_element_by_xpath("//*[@id='DataTables_Table_0_info']")
                        driver.execute_script("arguments[0].scrollIntoView(true);", elem)  
                        button.click()
        except:
            soup = BeautifulSoup(driver.page_source, 'lxml')
            tables = soup.find_all('table')
            dfs = pd.read_html(str(tables))
            new_df = pd.DataFrame(dfs[1])
            df = df.append(new_df, ignore_index=True, sort=False)

        df.to_csv(listOfFaculty[index] + '.csv')
        print("ok!")
    except Exception as e:
        if hasFirstPage:
            df.to_csv(listOfFaculty[index] + '.csv')
            print("ok!")
        print(e)


loggedIn = False
while not loggedIn:
    username = os.environ.get("USERNAME")
    password = os.environ.get("PASSWORD")
    loggedIn = login(username, password)

print("Scrapping will begin shortly. This might take a long time depending on the load of Maya server.")
time.sleep(3)
before = datetime.datetime.now()
for index in range(len(listOfFaculty)):
    print("Scrapping {}-th faculty: {}".format(index+1, listOfFaculty[index]))
    print("Ctrl+C to cancel.")
    scrape(index)
    time.sleep(3)
    
after = datetime.datetime.now()
driver.close()
print("Done Scrapped {} faculties.".format(len(listOfFaculty)))
print("Time used: {}".format(after - before))

