from uuid import uuid4
from selenium import webdriver
import os
from selenium.webdriver.common.by import By
import time
from datetime import datetime
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import uuid
from selenium.webdriver.chrome.service import Service
from django.db import transaction


opts = Options()
# Runs Chrome in headless mode.
opts.add_argument("--headless=new")  # or "--headless" if your Chromium is older
opts.add_argument("--no-sandbox")
opts.add_argument("--disable-dev-shm-usage")
# unique temp profile
profile_dir = f"/tmp/selenium_profile_{uuid.uuid4()}"
print("Using profile:", profile_dir)
opts.add_argument(f"--user-data-dir={profile_dir}")
opts.add_argument("--verbose")  # get more internal logging

service = Service("/usr/bin/chromedriver")  # adjust if chromedriver is elsewhere
driver = webdriver.Chrome(service=service, options=opts)

driver = None

def start_bot():
    global driver, options, service
    # getting the phone number which is being used as the bot in eitaa
    # phone_number = input("Enter phone number without first zero (example: 9110000000): ")
    phone_number = os.environ.get("PHONE_NUMBER")

    print("[BOT] received phone_number from .env: ", phone_number)

    driver = webdriver.Chrome(service=service,options=options)
    print('Starting eitaa bot...')

    # wait until the page loads
    driver.get('https://web.eitaa.com/')
    while True:
        try:
            wait = WebDriverWait(driver, 10)
            element = wait.until(EC.presence_of_element_located((By.XPATH, "//*[@id='auth-pages']/div/div[2]/div[1]/div/div[3]/div[2]/div[1]")))
            break
        except Exception as e:
            print('ERROR: The page did not open. Retrying...')
            time.sleep(5)

    # entering the phone number and go to otp tab
    # time.sleep(5)
    element = driver.find_element(By.XPATH, "//*[@id='auth-pages']/div/div[2]/div[1]/div/div[3]/div[2]/div[1]")
    element.clear()
    element.send_keys(phone_number)
    time.sleep(3)
    element = driver.find_element(By.XPATH, "//*[@id='auth-pages']/div/div[2]/div[1]/div/div[3]/button")
    element.click()

    # entering the validation code from user and login
    from .models import EitaaOTP
    otp = ''
    with transaction.atomic():
        while True:
            object = EitaaOTP.objects.first()
            if object:
                otp = object.otp
                object.delete()
                break
    
    # otp = input('enter the validation code: ')
    time.sleep(3)
    element = driver.find_element(By.XPATH, "//*[@id='auth-pages']/div/div[2]/div[3]/div/div[3]/div/input")
    element.send_keys(otp)
    # time.sleep(3)

# global user variable(phone number)
user = ''

# searching for the user in the search bar of eitaa
def find_user(x, number=None):
    time.sleep(1)
    obj = driver.find_element(By.XPATH, "//*[@id='new-menu']")
    obj.click()
    time.sleep(1)
    print("**************************")
    obj = driver.find_element(By.XPATH, "//*[@id='new-menu']/div[3]/div[3]/div")
    obj.click()
    time.sleep(1)
    global user
    if x == 1:
        # user = input("Enter the user number which u want to chat (like 98902902000): ")
        user = number
    obj = driver.find_element(By.XPATH, "//*[@id='contacts-container']/div[1]/div/input")
    obj.send_keys(user)
    time.sleep(1)


def send_message(code):
    element = driver.find_element(By.XPATH, "//*[@id='column-center']/div/div/div[4]/div/div[1]/div[7]/div[1]/div[1]")
    element.send_keys(f'کد اشتراک شما: {code}')
    element = driver.find_element(By.XPATH, "//*[@id='column-center']/div/div/div[4]/div/div[4]/button")
    element.click()
    # time.sleep(5)


def message(user_number, sub_code):
    while True:
        # refreshing the page for the cases that returning to the main page is needed.
        driver.refresh()
        wait = WebDriverWait(driver, 10)
        try:
            element = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="column-left"]/div/div/div[1]/div[1]/span')))
        except Exception as e:
            print('ERROR: The page did not open after 10 seconds. Retrying...')
            continue
        # time.sleep(5)
        # calling find_user with 1 (the case that the destination number should be gotten from API)
        find_user(1, user_number)
        # checking if the user is existing in the contacts or not
        elements = driver.find_elements(By.XPATH, "//*[@id='contacts']/li/div[1]")
        if elements:
            elements[0].click()
            print(user, '#############')
            # sending the desired message to the user
            send_message(sub_code)
            return {'success': True, 'detail': 'پیام ارسال شد'}
        # in most cases the user is new and is not in the contacts of the bot
        else:
            print("\033[31m++++++++++++++++++++\033[0m")
            time.sleep(1)
            # pushing the button of adding new contact
            obj = driver.find_element(By.XPATH, "//*[@id='contacts-container']/div[2]/button")
            obj.click()
            time.sleep(2)

            # entering the phonenumber
            obj = driver.find_element(By.XPATH, '/html/body/div[5]/div/div[3]')
            obj.click()
            obj = driver.find_element(By.XPATH, '/html/body/div[5]/div/div[3]/div[1]')
            obj.clear()
            obj.send_keys(user)
            # driver.execute_script("arguments[0].innerText = arguments[1];", obj, user)
            time.sleep(1)
            
            # entering the name
            obj = driver.find_element(By.XPATH, '/html/body/div[5]/div/div[2]/div[1]')
            obj.click()
            name = driver.find_element(By.XPATH, '/html/body/div[5]/div/div[2]/div[1]/div[1]')
            # a default name which varies by the time of creating the contact (in this bot only the phone number is important)
            name.send_keys(f"contact {datetime.now()}")
            # driver.execute_script("arguments[0].innerText = arguments[1];", name, f"contact {datetime.now()}")
            time.sleep(1)

            # clicking the confirm button
            obj = driver.find_element(By.XPATH, '/html/body/div[5]/div/div[1]/button')
            obj.click()
            time.sleep(1)
            
            # check if the user with the numer has eitaa or not
            toast_err = driver.find_elements(By.XPATH, '/html/body/div[6]')
            if toast_err:
                print('The given number does not have Eitaa.')
                # returns to the first of the while loop to take a new number
                # continue
                return {'success': False, 'detail': 'شماره داده شده ایتا ندارد.'}
            
            # returning to the main page
            driver.refresh()
            try:
                thing = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="column-left"]/div/div/div[1]/div[1]/span')))
            except Exception as e:
                print('ERROR: The page did not respond after 10 seconds. Retrying...')
                continue
            # time.sleep(5)

            # calling find_user with 0 (the case that the last saved new user number is used for searching and no need to enter any number again)
            find_user(0)
            obj = driver.find_element(By.XPATH, "//*[@id='contacts']/li/div[1]")
            obj.click()
            # sending the desired message to the NEW user
            send_message(sub_code)
            return {'success': True, 'detail': 'پیام ارسال شد'}
