'''
Author: yeffky
Date: 2025-02-16 17:17:20
LastEditTime: 2025-02-17 11:52:00
'''
from selenium import webdriver
import os
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
import time

driver = webdriver.Chrome()
driver_wait = WebDriverWait(driver, 10)
driver.get('http://localhost:8080/#/')
time.sleep(5)
pwd_input = driver.find_element(By.CSS_SELECTOR, 'input')
pwd_input.send_keys('123456')
time.sleep(1)
login_btn = driver.find_element(By.CSS_SELECTOR, 'button')
login_btn.click()
time.sleep(5)

upload = driver.find_element(By.CSS_SELECTOR, 'input[type="file"]')
images = os.listdir('./pictures')
images = list(map(lambda x: os.path.join(r"D:\Project\UUCrawl\Code\pictures", x), images))
img_str = ""
print('\n'.join(images))
upload.send_keys('\n'.join(images))
driver.close()
