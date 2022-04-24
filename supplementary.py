import os
import time

import pickle
import pandas as pd
from sklearn.preprocessing import LabelEncoder
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

df = pd.read_csv('./crop.csv')
labelencoder = LabelEncoder()
df['label_cat'] = labelencoder.fit_transform(df['label'])
with open('model_pickle', "rb") as f:
    model = pickle.load(f)

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
driver = webdriver.Chrome(
    executable_path=r"C:\Program Files (x86)\chromedriver_win32\chromedriver.exe", chrome_options=op)

# PATH = r"C:\Program Files (x86)\chromedriver_win32\chromedriver.exe"
# options = webdriver.ChromeOptions()
# options.add_argument("start-maximized")
# # to supress the error messages/logs
# options.add_experimental_option('excludeSwitches', ['enable-logging'])
# driver = webdriver.Chrome(options=options, executable_path=PATH)


def recommend(temp, hum, ph, rain):
    preds = list(model.predict([[temp, hum, ph, rain]])[0])
    npk = preds[1:]
    crop_index = round(preds[0])

    mapper = dict(zip(labelencoder.classes_,
                  range(len(labelencoder.classes_))))
    # The code for mapper is from https://stackoverflow.com/questions/42196589/any-way-to-get-mappings-of-a-label-encoder-in-python-pandas

    crop = list(mapper.keys())[list(mapper.values()).index(int(crop_index))]
    # The code for crop is from https://www.geeksforgeeks.org/python-get-key-from-value-in-dictionary/
    return crop, npk


def get_disease(img_path):
    driver.get(
        "https://plant-disease-detection-ai.herokuapp.com/index")
    upload_element = driver.find_element(
        By.XPATH, '//*[@id="actual-btn"]')
    upload_element.send_keys(img_path)
    submit_element = driver.find_element(
        By.XPATH,
        "/html/body/div[2]/div/div[2]/div[2]/div/form/center/a/button")
    submit_element.click()
    try:
        title_element = extract_values(
            120, "/html/body/div[3]/div/div[1]/div/h1/b")

        meta_des = extract_values(
            10, "/html/body/div[3]/div/div[2]/div/div/h5/b")
        des = extract_values(
            10, "/html/body/div[3]/div/div[2]/div/div/p")
        meta_treat = extract_values(
            10, "/html/body/div[3]/div/div[3]/div/div/h5/b")
        treat = extract_values(
            10, "/html/body/div[3]/div/div[3]/div[1]/div/p")
        os.remove(img_path)
        return {"title": title_element,
                "meta_des": meta_des,
                "des": des,
                "meta_treat": meta_treat,
                "treat": treat}

    finally:
        driver.quit()


def extract_values(t, p):
    return WebDriverWait(driver, t).until(
        EC.presence_of_all_elements_located((By.XPATH, f"{p}"))
    )[0].text
