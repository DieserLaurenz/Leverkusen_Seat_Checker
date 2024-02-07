# Importe
import base64
import json
import time
from io import BytesIO
from zoneinfo import available_timezones
import portalocker
import threading

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
REQUEST_DELAY = 5
bot_token = "6602448853:AAFVqBmsIes9h0cC3YINOVIGxWiBrLBjDmo"
chat_id = "-4153744196"
product_id = 20123412
event_id = 1977  # Bayern Spiel
username = "freimut51371"
password = "Nujbop-raxsor-8nyxqa"
headers_path = "headers.json"

# Es geht auch einfach nur nach event_id fetchen ohne block

blocks = [
    848, 849, 850, 851, 854, 855, 856, 857, 861, 862, 864, 865, 866, 867, 868, 869,
    870, 871, 872, 873, 874, 875, 876, 877, 880, 881, 882, 883, 884, 885, 886, 887,
    888, 889, 890, 891, 893, 894, 895, 896, 897, 898, 899, 900, 901, 902, 903, 904,
    905, 906, 907, 908, 909, 910, 911, 912, 913, 914, 915, 916, 917, 918, 919, 931,
    932, 933, 934, 935, 936, 938, 939, 940, 941, 942, 943, 944, 945, 946, 947, 948,
    953, 954, 955, 956, 957, 958, 959, 960, 961, 962, 963, 964, 965, 966
]

avilable_seats = {}

# Session-Initialisierung
session = tls_client.Session(
    client_identifier="chrome_112",
    random_tls_extension_order=True,
)


def fetch_new_headers():

    while True:
        # Konfiguriere Selenium WebDriver (Beispiel mit Chrome)
        original_driver = Driver(uc=True)

        try:

            original_driver.get('https://www.bayer04.de/de-de/shop/tickets')


            """
            print("Loading cookies...")

            try:
                # Open the JSON file using a 'with' statement
                with open("cookies.json", 'r') as json_file:
                    # Read the contents of the JSON file
                    json_data = json_file.read()

                    # Check if the JSON data is not empty
                    if json_data.strip():
                        # Parse the JSON data
                        cookies = json.loads(json_data)

                        # Add each cookie to your driver
                        for cookie in cookies:
                            original_driver.add_cookie(cookie)

                    else:
                        print("The JSON file is empty.")
            except FileNotFoundError:
                print("The JSON file does not exist.")

            print(f"Cookies: {original_driver.get_cookies()}")
            """

            original_driver.get('https://www.bayer04.de/de-de/shop/tickets')

            # Wait for the page to load (you can use better waiting strategies)
            original_driver.implicitly_wait(10)

            # Check if an element with the class 'captcha-code' exists
            captcha_elements = original_driver.find_elements(By.CLASS_NAME, 'captcha-code')

            if captcha_elements:

                try:
                    # Extract the URL of the Captcha image
                    captcha_url = captcha_elements[0].get_attribute('src')

                    time.sleep(2)

                    # Open a new WebDriver instance for fetching the image
                    image_driver = webdriver.Chrome()

                    # Go to the Captcha URL using the new WebDriver instance
                    image_driver.get(captcha_url)

                    time.sleep(5) # Ändern dass der auf Captcha image wartet

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
                        original_driver.quit()
                        image_driver.quit()
                        continue

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
                        continue
                
                finally:
                    # Close the new WebDriver instance even in case of exceptions
                    image_driver.quit()

            # Now, navigate to the login URL
            original_driver.get(
                'https://login.bayer04.de/login/?next=/authorize/%3Fclient_id%3Dq1pJ20GomJ6fjKxXee5HelQB4jhgKcAWjl9xHOH0%26response_type%3Dcode%26redirect_uri%3Dhttps%253A%252F%252Fwww.bayer04.de%252Fde-de%252Fshop%252Fcustomer%252Flogin%252Fprofile%253Ftarget%253Dhome%26state%3DeyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpYXQiOjE3MDY3OTcwNDIsIm5iZiI6MTcwNjc5NzA0MiwiZXhwIjoxNzA2Nzk3OTQyfQ.qU5F5oNFw4a8eY8xwam0oOB44pwEZUKzKLfgpDjBizc')

            # Find and enter the username slowly
            username_input = WebDriverWait(original_driver, 10).until(
                EC.presence_of_element_located((By.ID, "input-username"))
            )

            for char in username:
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

            original_driver.get('https://www.bayer04.de/de-de/shop/customer/login/')

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

            with open(headers_path, 'w') as file:
                # Lock the file for writing
                portalocker.lock(file, portalocker.LOCK_EX)
                
                # Write headers to the file in JSON format
                json.dump(headers, file)

            with open('cookies.json', 'w') as file:
                json.dump(original_driver.get_cookies(), file, indent=2)  # Use json.dump() to write JSON data to the file

            original_driver.quit()

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

def remove_expired_seat_ids():
    if avilable_seats:
        current_time = time.time()
        expired_seat_ids = [seat_id for seat_id, added_time in avilable_seats.items() if current_time - added_time > 900]  # 900 Sekunden sind 15 Minuten
        for seat_id in expired_seat_ids:
            del avilable_seats[seat_id]

def check_seats():
    """
    Überprüft verfügbare Sitze für ein Event und benachrichtigt über Telegram.
    """

    options_headers = {
        'authority': 'tss-al.bayer04.de',
        'accept': '*/*',
        'accept-language': 'de-DE,de;q=0.9,en-GB;q=0.8,en;q=0.7,en-US;q=0.6,es;q=0.5,it;q=0.4,fr;q=0.3',
        'access-control-request-headers': 'auth-apf,auth-tws',
        'access-control-request-method': 'GET',
        'origin': 'https://www.bayer04.de',
        'referer': 'https://www.bayer04.de/',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-site',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36',
    }

    while True:
        try:
            print(f"Removing seats: {avilable_seats}")
            remove_expired_seat_ids()
            print(f"Removed seats: {avilable_seats}")

            print("Fetching headers")

            with open(headers_path, 'r') as file:
                # Lock the file for reading (shared lock)
                portalocker.lock(file, portalocker.LOCK_SH)
                
                # Read and return the headers from the file
                request_headers = json.load(file)

            print("Fetched headers")

            for block in blocks:
                options_response = session.options(f'https://tss-al.bayer04.de/api/private/seats/{event_id}/{block}', headers=options_headers)
                print(options_response.status_code)
                response = session.get(f'https://tss-al.bayer04.de/api/private/seats/{event_id}/{block}',
                                       headers=request_headers)
                status_code = response.status_code

                if status_code == 404:
                    print(f"No Seats found for event {event_id} and block {block}")
                elif status_code == 200:
                    response_data = json.loads(response.text)
                    seat_ids = [seat["id"] for category in response_data[0]["category"] for seat in category["seats"]]

                    for seat_id in seat_ids:
                        current_time = time.time()
                        avilable_seats[seat_id] = current_time
                        print(f"Seat found for event {event_id} and block {block}. Seat_ID: {seat_id}")
                        message = f"Seat found for event {event_id} and block {block}. Seat\\_ID: {seat_id}\n [Checkout Link](https://www.bayer04.de/de-de/shop/product/{product_id})"
                        send_telegram_message(bot_token, chat_id, message, 'Markdown')
                        time.sleep(2)
                        
                elif status_code == 502:
                    print(f"Status code: {status_code}")
                        
                elif status_code == 403:
                    print(f"Status code: {status_code}")

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


def main():
    # Create threads
    t1 = threading.Thread(target=check_seats)
    t2 = threading.Thread(target=fetch_new_headers)

    # Start threads
    t1.start()
    t2.start()

    # Wait for threads to complete
    t1.join()
    t2.join()

main()