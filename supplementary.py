import os
import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

op = webdriver.ChromeOptions()
# https://youtu.be/kiYmBvv94RY
# https://youtu.be/rfdNIOYGYVI
# https://youtu.be/U6gbGk5WPws
# https://youtu.be/b5jt2bhSeXs
# op.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
op.binary_location = "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe"
op.add_argument("--headless")
op.add_argument("--no-sandbox")
op.add_argument("--disable-dev-sh-usage")
op.add_experimental_option('excludeSwitches', ['enable-logging'])


# driver = webdriver.Chrome(executable_path=os.environ.get("CHROMEDRIVER_PATH"), chrome_options=op)
driver = webdriver.Chrome(executable_path=r"C:\Program Files (x86)\chromedriver_win32\chromedriver.exe", chrome_options=op)

# PATH = r"C:\Program Files (x86)\chromedriver_win32\chromedriver.exe"
# options = webdriver.ChromeOptions() 
# options.add_argument("start-maximized")
# # to supress the error messages/logs
# options.add_experimental_option('excludeSwitches', ['enable-logging'])
# driver = webdriver.Chrome(options=options, executable_path=PATH)

def get_disease(img_path):
    driver.get("https://plant-disease-detection-ai.herokuapp.com/index")
    upload_element = driver.find_element(By.XPATH, '//*[@id="actual-btn"]')
    upload_element.send_keys(img_path)
    submit_element = driver.find_element(By.XPATH, "/html/body/div[2]/div/div[2]/div[2]/div/form/center/a/button")
    submit_element.click()
    try:
        title_element = WebDriverWait(driver, 60).until(
            EC.presence_of_all_elements_located((By.XPATH, "/html/body/div[3]/div/div[1]/div/h1/b"))
        )[0].text
        #  /html/body/div[3]/div/div[2]/div/div/p
        des = WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.XPATH, "/html/body/div[3]/div/div[2]/div/div/p"))
        )[0].text
        treat = WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.XPATH, "/html/body/div[3]/div/div[3]/div[1]/div/p"))
        )[0].text
        return (title_element, des, treat)
    finally:
        driver.quit()
y = get_disease("C:\\Users\\Admin\\Desktop\\farmly\\AppleScab2.JPG")
print(y)
