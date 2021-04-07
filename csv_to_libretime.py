# Written by Cole Schiffer
# Modified by Oliver Calder

import sys
import os
import csv
import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

from libretime_credentials import USER, PASSWORD

DOMAIN = 'stream.krlx.org'

def get_credentials_filename():
    credentials_filename = 'show_credentials.csv'
    if len(sys.argv) > 1:
        credentials_filename = sys.argv[1]
    assert(os.path.exists(credentials_filename))

def main():
    driver = webdriver.Chrome()
    driver.get(f"http://{DOMAIN}/login")
    username = driver.find_element_by_id("username")
    password = driver.find_element_by_id("password")

    username.send_keys(USER)
    password.send_keys(PASSWORD)

    driver.find_element_by_name("submit").click()
    driver.get(f"http://{DOMAIN}/schedule")

    with open('show_credentials.csv', newline='') as infile:
        reader = csv.reader(infile)
        for row in reader:
            name, start_date, start_time, end_date, end_time, login, password, emails = row
            # camelCase variables are for page elements, snake_case for values

            driver.find_element_by_xpath("//button[@onclick=\"showForm()\"]").click()
            time.sleep(3)
            showName = driver.find_element_by_id("add_show_name")
            showName.send_keys(name)

            driver.find_element_by_id("add_show_start_now-future").click()
            time.sleep(3)
            startDate = driver.find_element_by_id("add_show_start_date")
            startDate.clear()
            startDate.send_keys(start_date)
            startTime = driver.find_element_by_id("add_show_start_time")
            startTime.clear()
            startTime.send_keys(start_time)

            endDate = driver.find_element_by_id("add_show_end_date_no_repeat")
            endDate.clear()
            endDate.send_keys(end_date)
            endTime = driver.find_element_by_id("add_show_end_time")
            endTime.clear()
            endTime.send_keys(end_time)

            driver.find_element_by_id("add_show_repeats").click()
            time.sleep(3)
            driver.find_element_by_xpath("//*[text()='Live Stream Input']").click()
            time.sleep(3)
            driver.find_element_by_id("cb_custom_auth").click()

            time.sleep(3)

            showUsername = driver.find_element_by_id("custom_username")
            showUsername.send_keys(login)

            showPassword = driver.find_element_by_id("custom_password")
            showPassword.send_keys(password)
            driver.find_element_by_xpath("//*[text()='Add this show']").click()

            time.sleep(5)
