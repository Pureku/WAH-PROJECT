from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.edge.options import Options
from selenium.webdriver import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import ElementClickInterceptedException, ElementNotInteractableException,  ElementNotSelectableException, ElementNotVisibleException
# from tenacity import time
import pandas as pd
from pytesseract import pytesseract
from PIL import Image
from io import BytesIO
import base64
import asyncio


class setup():

    PATH_ = 'C:\PATH\edgedriver_win64\msedgedriver.exe'  # Call path web-driver
    driver = webdriver.Edge(PATH_)


class getTime():

    driver = setup.driver
    driver = driver
    # driver.get("https://www.timeanddate.com/")
    # wait = WebDriverWait(driver, 20, poll_frequency=1, ignored_exceptions=[
    #                              ElementNotVisibleException, ElementNotSelectableException])

    # hm = wait.until(EC.element_to_be_clickable((By.ID, "clk_hm")))
    # sc = wait.until(EC.element_to_be_clickable((By.ID, "ij0")))

    # hmText = [hm.text]          #Get HH:mm from https://www.timeanddate.com/
    # scText = [sc.text]          #Get sec from https://www.timeanddate.com/


async def runTime():

    # facebook
    dv = setup.driver
    url = "https://www.dcy.go.th/"  # Link ดย

    # newUrl = url.replace("www")
    dv.get(url)
    waitLoad = WebDriverWait(dv, 20, poll_frequency=1, ignored_exceptions=[
        ElementNotVisibleException, ElementNotSelectableException])

    setup.driver.find_element_by_link_text('เข้าสู่ระบบ').click()
    waitLoad.until(EC.element_to_be_clickable(
        (By.ID, "username"))).send_keys("1679900365499")   #Input your id card 
    waitLoad.until(EC.element_to_be_clickable(
        (By.ID, "password"))).send_keys("S.somphot!@#499")   #Input your password

    await capture()
    captcha = await ocr()

    setup.driver.find_element_by_class_name('MuiInputBase-input MuiInput-input').send_key(captcha)
    setup.driver.find_element_by_class_name('MuiButtonBase-root MuiButton-root MuiButton-contained MuiButton-containedPrimary').click()

    setup.driver.find_element_by_link_text('หน้าหลัก').click()


    # waitLoad.until(EC.element_to_be_clickable((By.ID,"m_login_email"))).send_keys("Your Email")           #Input your email for login facebook
    # waitLoad.until(EC.element_to_be_clickable((By.ID,"m_login_password"))).send_keys("Your Pass")          #Input your passwork for login facebook
    # waitLoad.until(EC.element_to_be_clickable((By.ID,"login_password_step_element"))).click()
    # waitLoad.until(EC.element_to_be_clickable((By.ID, "composerInput"))).send_keys("Data") #Input data

    # while True:
    #     hmText = getTime.hmText
    #     scText = getTime.scText

    #     hmStart = '19:00'       #Start time
    #     hmStop = '20:00'        #Stop time

    #     if (str(hmText) == "['" + hmStart + "']"):
    #         if (str(scText) == "['00']"):
    #             waitLoad.until(EC.element_to_be_clickable((By.NAME, "submit"))).click()
    #             waitLoad.until(EC.element_to_be_clickable((By.ID, "composerInput"))).send_keys("data")

    #     if (str(hmText) == "['" + hmStop + "']"):
    #         break

    #     else:
    #         print(str(hmText) + ":" + str(scText))


def capture():
    dv = setup.driver
    url = "https://www.dcy.go.th/login"
    dv.get(url)

    el = dv.find_element_by_class_name('style_captchaContainer__LdFYB')
    location = el.location
    size = el.size
    png = dv.get_screenshot_as_png()
    dv.quit()

    img = Image.open(BytesIO(png))

    left = location['x']
    top = location['y']
    right = location['x'] + size['width']
    bottom = location['y'] + size['height']

    img = img.crop((left, top, right, bottom))  # defines crop points
    img.save('image/myphoto.png', 'png')  # saves new cropped image


def ocr():
    path_pytes = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
    path_img = "image/myphoto.png"
    pytesseract.tesseract_cmd = path_pytes
    img = Image.open(path_img)
    text = pytesseract.image_to_string(img)
    text_split = text.split()
    return (text_split[0])


capture()
ocr()
# runTime()
