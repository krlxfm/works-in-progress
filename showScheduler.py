import csv
import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

with open('show_credentials.csv', newline='') as f:
    reader = csv.reader(f)
    data = list(reader)
//set user name and password here
user = ""
pass = ""
driver = webdriver.Chrome()
driver.get("http://stream.krlx.org/login")
username = driver.find_element_by_id("username")
password = driver.find_element_by_id("password")

username.send_keys(user)
password.send_keys(pass)

driver.find_element_by_name("submit").click()
driver.get("http://stream.krlx.org/schedule")
for x in data:
    driver.find_element_by_xpath("//button[@onclick=\"showForm()\"]").click()
    showName = driver.find_element_by_id("add_show_name")
    showName.send_keys(x[0])
    driver.find_element_by_id("add_show_start_now-future").click()
    startDate = driver.find_element_by_id("add_show_start_date")
    startDate.clear()
    startDate.send_keys(x[1])
    startTime = driver.find_element_by_id("add_show_start_time")
    startTime.clear()
    startTime.send_keys(x[2])
    endDate = driver.find_element_by_id("add_show_end_date_no_repeat")
    endDate.clear()
    endDate.send_keys(x[3])
    endTime = driver.find_element_by_id("add_show_end_time")
    endTime.clear()
    endTime.send_keys(x[4])
    driver.find_element_by_id("add_show_repeats").click()
    driver.find_element_by_xpath("//*[text()='Live Stream Input']").click()
    driver.find_element_by_id("cb_custom_auth").click()
    showUsername = driver.find_element_by_id("custom_username")
    showUsername.send_keys(x[5])
    showPassword = driver.find_element_by_id("custom_password")
    showPassword.send_keys(x[6])
    driver.find_element_by_xpath("//*[text()='Add this show']").click()
    time.sleep(3)
