# Importe
import base64
import json
import time
from io import BytesIO

import pytesseract
import requests
import tls_client
from PIL import Image
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from seleniumbase import Driver

# Konstantendefinitionen
REQUEST_DELAY = 10
bot_token = "6602448853:AAFVqBmsIes9h0cC3YINOVIGxWiBrLBjDmo"
chat_id = "-4153744196"
product_id = 20123412
event_id = 1977  # Bayern Spiel
username = "freimut51371"
password = "Nujbop-raxsor-8nyxqa"

# Es geht auch einfach nur nach event_id fetchen ohne block

blocks = [
    848, 849, 850, 851, 854, 855, 856, 857, 861, 862, 864, 865, 866, 867, 868, 869,
    870, 871, 872, 873, 874, 875, 876, 877, 880, 881, 882, 883, 884, 885, 886, 887,
    888, 889, 890, 891, 893, 894, 895, 896, 897, 898, 899, 900, 901, 902, 903, 904,
    905, 906, 907, 908, 909, 910, 911, 912, 913, 914, 915, 916, 917, 918, 919, 931,
    932, 933, 934, 935, 936, 938, 939, 940, 941, 942, 943, 944, 945, 946, 947, 948,
    953, 954, 955, 956, 957, 958, 959, 960, 961, 962, 963, 964, 965, 966
]



# Session-Initialisierung
session = tls_client.Session(
    client_identifier="chrome_112",
    random_tls_extension_order=True,
)


def fetch_new_headers():
    # Konfiguriere Selenium WebDriver (Beispiel mit Chrome)
    original_driver = Driver(uc=True)

    try:

        original_driver.get('https://www.bayer04.de/de-de/shop/tickets')

        # Wait for the page to load (you can use better waiting strategies)
        original_driver.implicitly_wait(10)

        # Check if an element with the class 'captcha-code' exists
        captcha_elements = original_driver.find_elements(By.CLASS_NAME, 'captcha-code')
        if captcha_elements:
            # Extract the URL of the Captcha image
            captcha_url = captcha_elements[0].get_attribute('src')

            time.sleep(2)

            # Open a new WebDriver instance for fetching the image
            image_driver = webdriver.Chrome()

            try:
                # Go to the Captcha URL using the new WebDriver instance
                image_driver.get(captcha_url)

                time.sleep(1)

                # Fetch the Captcha image using the new WebDriver
                image_data = image_driver.find_element(By.TAG_NAME, 'img').get_attribute('src')

                image_bytes = base64.b64decode(image_data.split(',')[1])

                image = Image.open(BytesIO(image_bytes))

                # Use pytesseract to extract text from the image
                pytesseract.pytesseract.tesseract_cmd = 'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'

                text = pytesseract.image_to_string(image).strip()

                if text:
                    print("Found text in Captcha:", text)
                else:
                    print("No captcha code found")
                    return

                # Close the new WebDriver instance
                image_driver.quit()

                # Explicitly wait for the input field to become available
                input_field = WebDriverWait(original_driver, 10).until(
                    EC.presence_of_element_located((By.ID, "solution"))
                )

                # Send the characters one by one with a delay
                for char in text:
                    input_field.send_keys(char)
                    time.sleep(1)  # Adjust the delay as needed

                input_field.send_keys(Keys.RETURN)  # You can use Keys.RETURN to submit the input

                time.sleep(5)

                current_url = original_driver.current_url

                if current_url != "https://www.bayer04.de/de-de/shop/tickets":
                    print("Didn't solve captcha")
                    original_driver.quit()
                    return

                # Now, navigate to the login URL
                original_driver.get(
                    'https://login.bayer04.de/login/?next=/authorize/%3Fclient_id%3Dq1pJ20GomJ6fjKxXee5HelQB4jhgKcAWjl9xHOH0%26response_type%3Dcode%26redirect_uri%3Dhttps%253A%252F%252Fwww.bayer04.de%252Fde-de%252Fshop%252Fcustomer%252Flogin%252Fprofile%253Ftarget%253Dhome%26state%3DeyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpYXQiOjE3MDY3OTcwNDIsIm5iZiI6MTcwNjc5NzA0MiwiZXhwIjoxNzA2Nzk3OTQyfQ.qU5F5oNFw4a8eY8xwam0oOB44pwEZUKzKLfgpDjBizc')

                # Find and enter the username slowly
                username_input = WebDriverWait(original_driver, 10).until(
                    EC.presence_of_element_located((By.ID, "input-username"))
                )

                for char in username:  # Replace 'your_username' with your actual username
                    username_input.send_keys(char)
                    time.sleep(0.5)  # Adjust the delay as needed

                # Find and enter the password
                password_input = original_driver.find_element(By.ID, "input-password")

                for char in password:  # Replace 'your_username' with your actual username
                    password_input.send_keys(char)
                    time.sleep(0.5)  # Adjust the delay as needed

                # Find and click the login button
                login_button = original_driver.find_element(By.ID, "signin-form-submit")
                time.sleep(2)
                login_button.click()

                original_driver.get('https://www.bayer04.de/de-de/shop/customer/login/?target=product_20123412')

                time.sleep(2)

                original_driver.get('https://www.bayer04.de/de-de/shop/user/')

                time.sleep(2)

                pre_element = original_driver.find_element(By.TAG_NAME, "pre")
                text = json.loads(pre_element.text)
                auth_apf = text["accessToken"]
                auth_tws = text["jwt"]

                headers = {
                    'auth-apf': auth_apf,
                    'auth-tws': auth_tws,
                    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36'
                }

                return headers

            finally:
                # Close the new WebDriver instance even in case of exceptions
                image_driver.quit()
        else:
            print("No Captcha code found.")
    finally:
        # Close the original WebDriver
        original_driver.quit()


# Funktionsdefinitionen
def send_telegram_message(bot_token, chat_id, message, parse_mode='Markdown'):
    """
    Sendet eine Nachricht an einen Telegram-Chat.
    """
    url = f'https://api.telegram.org/bot{bot_token}/sendMessage'
    data = {'chat_id': chat_id, 'text': message, 'parse_mode': parse_mode}
    response = requests.post(url, data=data)
    print(response.text)
    return response.json()


def check_seats():
    """
    Überprüft verfügbare Sitze für ein Event und benachrichtigt über Telegram.
    """

    headers = {
        'auth-apf': 'eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzJpc3MiOiJCYXllcjA0IiwiZXhwIjoxNzA2ODMzMDE0LCJpYXQiOjE3MDY3OTcwMTQsImN1c3RvbWVyX2dyb3VwcyI6IlNPTkRFUjIsU09OREVSMSxDTFVCLERLLU0yIiwic2NvcGUiOiIiLCJjb250YWN0X2lkIjoiMTk3YzBmZWEtY2UyMC00N2YxLTkwYTctOTg1MWEwMDI5YmVhIn0.ZGYn5VSY_kCvS0Rjl5sfwsVJu8ov5l0qfiYQxup3q_bh8QDuXc2mKIcIJuPBaWwUK7OXs6-wPeKZtaYZSka44eRjinYleB0VU2W7uX6a9WOHDAUNjYuio0DyOUt2LmsTjvBbp-0EH8-FMmQuqyOH7WxjLwioQtgWyh1gQsioX7SRT7YH5yHj0fPDH751AI4wG6G5YJQDo77_j6SzsYdS6nJXj6sbOzbJoHivOuYm-YWjmaN9IcmdkrsetJeNoikSodt6xhh1a4_n7A69hrsi_IKEKTg86YhhJBq8Ab-orJUL_tj6K4InLJYzLpf4ID-V24cRTqmyuR32ADZuZIWS0c_BDG6Kxic6y7hE0tDIMfEJtwNZ0BAlCRiPmHp4lmXl7Gdw9DU-7ksvSjRGw56uD8CZCktYfk_dYT-O2Bi0kmn1QX1ULcLyCAmAw2k3z6-fh9KKinPZZ6_IjUVHypLGCy7mtAd-3iQqv22XoPJ322WoO1an4cHFrcccgYOJiyhHByH-RY3FImbewnGBDVnZMlQrU0nTaiQL1fFs-YFiwMQUOGTqYreTkCSXUF05d9YBIkg-UK7C428IYByIrP60mDbzyt0AoL2Sb7dpnKP0uKJ6CR-D1uqCkFDgMUX-zf4j3NZay4FtI-Abkg2txr36JblQPDAq_90qKAC0ImQnTOs',
        'auth-tws': 'eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJJ0d3MiLCJhdWQiOiJ1cm46Y3VzdG9tZXIiLCJpYXQiOjE3MDY3OTkyNDUsImV4cCI6MTcwNjgwMjg0NSwic2Vzc2lvbl9pZCI6IjE2NDMzMDM4ZTI0MTcyYmM5OGVhYzZhNmJkOTNhNiJ9.HDAUcNT-5ur2v_CKJzQHMY4rQJztNI1U_NrGGDfdEEqx_eSdcW_zHvAs-2lpFrAiGwKhhQ3-dMqhFCeENwgw2FlvJNyDVzqULl4f-C07OzgBSpKMEFwuOUfc5OFpjiILJFCnxHkDm3vcBImGol2OItz31ifLhD5FcWMuxhrEZmf_MOSuHAHecL7LK3S5pp84CgI7VMYa-wtbNKakICC_96erI6AHViaJnxW2LUdb0bQMcjr-5jala7CXpAKnrs2rmukDzpS3j76Nh3y9Mou9oz6wfRfDhJ5WWr5LuGE7-WnlgHIgv9HBwN0GWBU5NFLT9JWpsP-6Z49z-TtwbVzkdQ',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36'
    }

    while True:
        try:
            for block in blocks:
                response = session.get(f'https://tss-al.bayer04.de/api/private/seats/{event_id}/{block}',
                                       headers=headers)
                status_code = response.status_code

                if status_code == 404:
                    print(f"No Seats found for event {event_id} and block {block}")
                elif status_code == 200:
                    response_data = json.loads(response.text)
                    seat_ids = [seat["id"] for category in response_data[0]["category"] for seat in category["seats"]]

                    for seat_id in seat_ids:
                        print(f"Seat found for event {event_id} and block {block}. Seat_ID: {seat_id}")
                        message = f"Seat found for event {event_id} and block {block}. Seat\\_ID: {seat_id}\n [Checkout Link](https://www.bayer04.de/de-de/shop/product/{product_id})"
                        send_telegram_message(bot_token, chat_id, message, 'Markdown')
                        time.sleep(2)
                elif status_code == 502:
                    print(f"Status code: {status_code}")
                    while True:
                        headers = fetch_new_headers()
                        if headers:
                            request_headers = headers
                            break
                        else:
                            continue

                else:
                    print(f"Unexpected status code: {status_code}")
                    print(response.text)
                    send_telegram_message(bot_token, chat_id,
                                          f"Unexpected status code: {status_code}. Laurenz kontaktieren", 'Markdown')
                    time.sleep(6000)
                time.sleep(0.1)
            print("Request delay..")
            time.sleep(REQUEST_DELAY)
        except Exception as e:
            print(e)
            time.sleep(1)
            continue


check_seats()
