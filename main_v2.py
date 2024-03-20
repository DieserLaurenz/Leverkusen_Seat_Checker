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
product_id = 20123417
event_id = 1983  # Bayern Spiel
username = "alexhintz111@gmail.com"
password = "%VxyS#noa8hxb9o"
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

def fetch_new_headers_v2():
    while True:
        try:
            driver = Driver(uc=True)
            driver.implicitly_wait(10)
            while True:
                driver.get('https://www.bayer04.de/de-de/shop/tickets')
                time.sleep(2)
                captcha_elements = driver.find_elements(By.CLASS_NAME, 'captcha-code')
                if captcha_elements:
                    print("Elements found")
                    captcha_url = captcha_elements[0].get_attribute('src')

                    # Open captcha URL in a new tab
                    driver.execute_script("window.open('');")
                    # Switch to the new tab
                    driver.switch_to.window(driver.window_handles[1])
                    driver.get(captcha_url)
                    
                    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, 'img')))
                    image_data = driver.find_element(By.TAG_NAME, 'img').get_attribute('src')
                    image_bytes = base64.b64decode(image_data.split(',')[1])
                    image = Image.open(BytesIO(image_bytes))
                    pytesseract.pytesseract.tesseract_cmd = 'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'
                    text = pytesseract.image_to_string(image).strip()

                    # Close the current tab
                    driver.close()
                    # Switch back to the original tab
                    driver.switch_to.window(driver.window_handles[0])

                    if text:
                        print("Found text in Captcha:", text)
                        input_field = WebDriverWait(driver, 10).until(
                            EC.presence_of_element_located((By.ID, "solution")))
                        for char in text:
                            input_field.send_keys(char)
                            time.sleep(1)
                        input_field.send_keys(Keys.RETURN)
                        time.sleep(5)
                        if driver.current_url == "https://www.bayer04.de/de-de/shop/tickets":
                            break
                        else:
                            print("Didn't solve captcha")
                            continue
                else:
                    break  # If no captcha, exit loop

            driver.get('https://login.bayer04.de/login')
            username_input = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "input-username")))

            print("Reached login page")

            for char in username:
                username_input.send_keys(char)
                time.sleep(0.2)
            password_input = driver.find_element(By.ID, "input-password")
            for char in password:
                password_input.send_keys(char)
                time.sleep(0.2)
            login_button = driver.find_element(By.ID, "signin-form-submit")
            time.sleep(2)
            login_button.click()

            driver.get('https://www.bayer04.de/de-de/shop/customer/login/')

            time.sleep(1)

            print("Logged in")

            previous_auth_apf = None
            previous_auth_tws = None
            while True:
                print("Fetching new headers")
                driver.get('https://www.bayer04.de/de-de/shop/user/')
                time.sleep(2)
                pre_element = driver.find_element(By.TAG_NAME, "pre")
                text = json.loads(pre_element.text)
                auth_apf = text["accessToken"]
                auth_tws = text["jwt"]
                if auth_apf == previous_auth_apf and auth_tws == previous_auth_tws:
                    print("Same headers")
                    time.sleep(60)
                    continue
                else:
                    print("New Headers")
                headers = {
                    'auth-apf': auth_apf,
                    'auth-tws': auth_tws,
                    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36'
                }
                with open('headers.json', 'w') as file:
                    portalocker.lock(file, portalocker.LOCK_EX)
                    json.dump(headers, file)
                with open('cookies.json', 'w') as file:
                    json.dump(driver.get_cookies(), file, indent=2)
                previous_auth_apf = auth_apf
                previous_auth_tws = auth_tws  
                print("Sleeping for 60s")  
                time.sleep(60)
        except Exception as e:
            print(f"An error occured: {e}")
            driver.quit()
            continue

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
                time.sleep(0.001)
            print("Request delay..")
            time.sleep(REQUEST_DELAY)
        except Exception as e:
            print(e)
            time.sleep(1)
            continue


def main():
    # Create threads
    t1 = threading.Thread(target=check_seats)
    t2 = threading.Thread(target=fetch_new_headers_v2)

    # Start threads
    t1.start()
    t2.start()

    # Wait for threads to complete
    t1.join()
    t2.join()

main()

def test_request():
    import requests

    cookies = {
        'PHPSESSID': '3jukomu94bju4q3ae1p80943b0',
        'QueueITAccepted-SDFrts345E-V3_b04tickets20240131': 'EventId%3Db04tickets20240131%26QueueId%3D2a7699c5-e5d4-4ba4-b614-85e824f1e1df%26RedirectType%3Dsafetynet%26IssueTime%3D1707336887%26Hash%3D7330d5c1ab736cc97e73baf91dabbb8876607f493c5c0d8f69387cdf130a618c',
    }

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36',
    }

    response = requests.get('https://www.bayer04.de/de-de/shop/user/', cookies=cookies, headers=headers)

    print(response.text)

def test_request_dortmund():
    import requests
    import re
    import html

    cookies = {
        'OLS_SESSION_ID': '3c7d5ceaa8b8d71ad39ac0da2ff3583c',
        'ols_cookieconsent': 'agree',
        'bm_sz': 'BBE6D7E2B0B9D614EC45541F8133F456~YAAQHWUQAnpQ616NAQAA6ZVAhRYOPIdzEDrjX1tX1bzD0kvoVrId/Ckf3oTica06b4RHCedjm5SI5xE/u18Y5TuP9XBS3sqtk3MmmiHTHAERRYaN0Ui5VFJVZRocNDrMwAuhuHCbzOJNM69zxqcR00pgZYz1Fo1JM+CGXBw12rQ/nnbEoGvny4kqwSFEnhhScorSNOchGJ4Cv05OlhFiW+DlsBYFoIltxfuHTLRK/cbi+5yVFVSZnN5ZlnAcjGVlRIrV2/D2k0q9N4a3nhxIv4WBVoY21Yfis8H3XCNTQ+ZbautPHbP0eew96Qeol7eDV93pRBvoY+e0Xx4qKv+x+VOXOoajLW5o1w==~3553089~4604468',
        'bm_mi': '5D6E8DFEFE806333DC979A7266BE7A39~YAAQHWUQAqtR616NAQAAyLVAhRZ7vim4F0pQeKeQzrL7VYoj2eQTBj++zZw8ppeaX1/xsDtkt95YiduOIGXdhULe5+tMnJC8E+B6QUSB1qm+j4q4Wqr5UQnkLwSkKQW3BpDPbZ+5dS0Q4WhbL24D5NfloFHuOZ3aO0bmgunhm8NFXJIwDo7Tp6dv4SJbw4An2ehA5BHBVd2FkfZ/jIqT25v5kV7SD0hChJIoNkA1P/ErVswnqxIR8SweBFfM6vGNhnNiYjP6D/ApwniRzAY16jBpKswQvKoXoeVwRwmNFk6mAmovTkfcel6TtBCKrXJSNA0sHyJpTsfS/9OtmBvHcaTa8nJFpd49dxheY93/w4qB2+BaMWY0N3iQN49kvFTG/S5hg7vMxFTalkE=~1',
        'ak_bmsc': 'A1E49C96092D159C22843136FECA6D6A~000000000000000000000000000000~YAAQHWUQAtlR616NAQAAIL5AhRZtfUGK5DQda+/yYZolyBS2TNfwzNyDb0/+MDnKI4HLCftBV5N8jnpmH3g4VVJTzXOtg/hOWG2varQEMd8CTCgdfSRDFgTl7JZB103MdMuDYBzd/6MTDqpQKL19PIx9v3QaB7PEDGaevg6jPY7I/VE5nx/ux8JVRppeh3s92cuTGNeruuje8zTE14jY+n5lV3jdn7uqU19OOX7aucwqnwK7FjllCNW99don1WTzIBy3O1LkHXRNJqR7jF4BRXmnUn6GEM9OdiZ420L+8SUezSOk8HNrFU/aNjSpeGFYYW6S26EMVpktC5jtaTxqJCkdrbQ0A/TcfVR+peigVOS1+vcHPqOYQh1XW4okvn3unvbwN/QXhy9oOjtAqfvHAUikuq1dL/R5gEunIazXNakObHP3wdwNAxvDKfvlI0UYwkan3OaFqNGWkq0rVvSNVCv4ek+A0RngJU0E1EdAmAYAsqnV+uOTj/pfGVX/kiGdHWALvwQyP2LyUTEqvu8bSraL4tT4/svncTKxGYZ69QGn6VmPQC4tVW7SJCODikrHmaWZ7Qvl0qHV/mgKK/Wn7vhmUNIsaLLk0dCsEZvnJHw=',
        'QueueITAccepted-SDFrts345E-V3_tixxfetchallv1': 'EventId%3Dtixxfetchallv1%26QueueId%3Dfe54c4df-aecc-4b93-bfa8-37b7b6d74b2b%26RedirectType%3Dsafetynet%26IssueTime%3D1707337875%26Hash%3Db24004aff1abd00218aea76faad229b938444fe461822e1f2cbdaf4f351d2d7b',
        '_gcl_au': '1.1.24844177.1707337890',
        '_gid': 'GA1.2.701222984.1707337890',
        '_abck': '566558D0BB20C45F323C650F586CD4E1~0~YAAQHWUQAmab616NAQAAM2xJhQse9LJPKG/El+RRdAcsSJi+8olQARbejU9JAyul+dPND6RPUGefcjNXqABt9fVkR/uin8ZCfucM7QBpvWXUkqJW/7CwGwsnvoO8Hs13P0B9QoIyZbTIcNyBE1Bi5+zNBLgDerMeTuAsbPPuwY5SqFfSPtz0O6R77GCco2V0S0rINGTHD9uX3ATXA1K1Y7to+9ikdbrejitn5ECwFjZWMZz7JThs5T1E9J4M3XRskUczrleryhhFCYirWx/EcGTyo4Is456xXn3pZm+zgE4Sc33KqlFkMiznoIWr5ooSK2Qkf3JsHOCS4ZWkcQzk2YzBBZY3StadQKIgKDpLus2Dc3JF9cjcQa1F98vL8qbV8clGn/UQJ3w6l/Qu0A3OSu7HsmGWiI2NsRQIkIV/tDssGHw=~-1~-1~1707341255',
        'q_i_t_u_i': 'referrer_https%3A%2F%2Fqueue.ticket-onlineshop.com%2Fsoftblock%2F%3Fc%3Dtixx%26e%3Dtixxbvbv43%26t%3Dhttps%253A%252F%252Fwww.ticket-onlineshop.com%252Fols%252Fbvb%252F%26cid%3Dde-DE%26enqueuetoken%3DeyJ0eXAiOiJRVDEiLCJlbmMiOiJBRVMyNTYiLCJpc3MiOjE3MDczMzk3ODAwNDEsInRpIjoiYTlmYzQwMDctZWE0Zi00MDBmLThiZDUtNGFhMTVlYjE2MGZhIiwiYyI6InRpeHgiLCJlIjoidGl4eGJ2YnY0MyIsImlwIjoiNS4xODAuNjEuMzkifQ.a4KUKijn9XlwuI-FYVxQQQ.qXKU57WVNHvzsrLHs4fIyHgt14SlNjS1Oemz16vWlxE%26rticr%3D3~cookiedomain_ticket-onlineshop.com',
        'QueueITAccepted-SDFrts345E-V3_tixxbvbv43': 'EventId%3Dtixxbvbv43%26QueueId%3Df9b1341b-71ac-43dc-a114-89960e56cc73%26RedirectType%3Dsafetynet%26IssueTime%3D1707339787%26Hash%3D3fc33468fda169b092358867111237c21f3962e3a0dffbf712d2675323339864',
        '_ga_XT2BHDJQNC': 'GS1.1.1707337890.1.1.1707339795.0.0.0',
        '_ga': 'GA1.2.1477844306.1707337890',
        'bm_sv': 'BBCDE96130F6C7C62DEB56406FFCE4CE~YAAQbdbdWK493mCNAQAA2gJjhRYaQSTJLWOIVoUfYVzwXkmB5CM1cB9WskqezODfsFpdWzW5eiq+lX9DOKtG0niFMmoNfREnMiBPAqIuXWr9n0ecEiujHaktRKYYXYebk1ShZt4ZqIzHedmqKW1k+k+xrAmo337tjpMtubDDfkN2c+IQRc6Twm4aWFfZ2EBjiERkP8thxJq+9YOhrPA5tB701e/tNCwVN2mH8Ic4X2xd0/ihEG9IRXR9H+hIOFZH+KYn3YmiCEWOUmyfZw==~1',
    }

    headers = {
        'authority': 'www.ticket-onlineshop.com',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'accept-language': 'de-DE,de;q=0.9,en-GB;q=0.8,en;q=0.7,en-US;q=0.6,es;q=0.5,it;q=0.4,fr;q=0.3',
        # 'cookie': 'OLS_SESSION_ID=3c7d5ceaa8b8d71ad39ac0da2ff3583c; ols_cookieconsent=agree; bm_sz=BBE6D7E2B0B9D614EC45541F8133F456~YAAQHWUQAnpQ616NAQAA6ZVAhRYOPIdzEDrjX1tX1bzD0kvoVrId/Ckf3oTica06b4RHCedjm5SI5xE/u18Y5TuP9XBS3sqtk3MmmiHTHAERRYaN0Ui5VFJVZRocNDrMwAuhuHCbzOJNM69zxqcR00pgZYz1Fo1JM+CGXBw12rQ/nnbEoGvny4kqwSFEnhhScorSNOchGJ4Cv05OlhFiW+DlsBYFoIltxfuHTLRK/cbi+5yVFVSZnN5ZlnAcjGVlRIrV2/D2k0q9N4a3nhxIv4WBVoY21Yfis8H3XCNTQ+ZbautPHbP0eew96Qeol7eDV93pRBvoY+e0Xx4qKv+x+VOXOoajLW5o1w==~3553089~4604468; QueueITAccepted-SDFrts345E-V3_tixxhsvv1=EventId%3Dtixxhsvv1%26QueueId%3D804b3532-a8f6-4ab8-9e36-033677889086%26RedirectType%3Dsafetynet%26IssueTime%3D1707337626%26Hash%3Df63b13eab3c281f225017a8126b9d5d882abcf268897e122096d64304b06d726; bm_mi=5D6E8DFEFE806333DC979A7266BE7A39~YAAQHWUQAqtR616NAQAAyLVAhRZ7vim4F0pQeKeQzrL7VYoj2eQTBj++zZw8ppeaX1/xsDtkt95YiduOIGXdhULe5+tMnJC8E+B6QUSB1qm+j4q4Wqr5UQnkLwSkKQW3BpDPbZ+5dS0Q4WhbL24D5NfloFHuOZ3aO0bmgunhm8NFXJIwDo7Tp6dv4SJbw4An2ehA5BHBVd2FkfZ/jIqT25v5kV7SD0hChJIoNkA1P/ErVswnqxIR8SweBFfM6vGNhnNiYjP6D/ApwniRzAY16jBpKswQvKoXoeVwRwmNFk6mAmovTkfcel6TtBCKrXJSNA0sHyJpTsfS/9OtmBvHcaTa8nJFpd49dxheY93/w4qB2+BaMWY0N3iQN49kvFTG/S5hg7vMxFTalkE=~1; ak_bmsc=A1E49C96092D159C22843136FECA6D6A~000000000000000000000000000000~YAAQHWUQAtlR616NAQAAIL5AhRZtfUGK5DQda+/yYZolyBS2TNfwzNyDb0/+MDnKI4HLCftBV5N8jnpmH3g4VVJTzXOtg/hOWG2varQEMd8CTCgdfSRDFgTl7JZB103MdMuDYBzd/6MTDqpQKL19PIx9v3QaB7PEDGaevg6jPY7I/VE5nx/ux8JVRppeh3s92cuTGNeruuje8zTE14jY+n5lV3jdn7uqU19OOX7aucwqnwK7FjllCNW99don1WTzIBy3O1LkHXRNJqR7jF4BRXmnUn6GEM9OdiZ420L+8SUezSOk8HNrFU/aNjSpeGFYYW6S26EMVpktC5jtaTxqJCkdrbQ0A/TcfVR+peigVOS1+vcHPqOYQh1XW4okvn3unvbwN/QXhy9oOjtAqfvHAUikuq1dL/R5gEunIazXNakObHP3wdwNAxvDKfvlI0UYwkan3OaFqNGWkq0rVvSNVCv4ek+A0RngJU0E1EdAmAYAsqnV+uOTj/pfGVX/kiGdHWALvwQyP2LyUTEqvu8bSraL4tT4/svncTKxGYZ69QGn6VmPQC4tVW7SJCODikrHmaWZ7Qvl0qHV/mgKK/Wn7vhmUNIsaLLk0dCsEZvnJHw=; _abck=566558D0BB20C45F323C650F586CD4E1~0~YAAQHWUQAshg616NAQAAxrpChQtBpAbnmfeGufyLjrSuZGcW7s8q+iJpT1RoMjDkwz4dKmf5SH8sEiD0Wge9Zj7JJNcwQcehq3M9CSvlyJydkTKidgXCAP/BtQ9Rbs+svrTDjdKKD8UWxqBgSQ0sfg/NtVqHmf+4/YnmgAZWTvDW+7L1I1zQT0snne6OtLCi9Ne64ypodHn7apSyUPGE7LhTGYz/Uw/gFUFcEdN6aJBgVROKqXuu9VVtOF9oqb4azzkEVwC+2Y+rnOxuQsETzNZuPvIHtyJuswn9WmL+2sduhaJ5hTdopIFwnjrRCfpeZ+t/gDoM9SrNuZDNa3yr5+9yhF1TLKqh2OiGJH7WR8DYKyBAigG9JbM62xveqf01jT2y016S81G60KdPg/i4n16ReNkuaWaqqj3MTi7Nb1ihJC8=~-1~-1~1707341255; QueueITAccepted-SDFrts345E-V3_tixxfetchallv1=EventId%3Dtixxfetchallv1%26QueueId%3Dfe54c4df-aecc-4b93-bfa8-37b7b6d74b2b%26RedirectType%3Dsafetynet%26IssueTime%3D1707337875%26Hash%3Db24004aff1abd00218aea76faad229b938444fe461822e1f2cbdaf4f351d2d7b; QueueITAccepted-SDFrts345E-V3_tixxbvbv43=EventId%3Dtixxbvbv43%26QueueId%3Df5bf8fbd-c719-4be6-86cc-44916170d25b%26RedirectType%3Dsafetynet%26IssueTime%3D1707337883%26Hash%3D4e54fc69b04ff498716ed4bea4becdf655a713e9bb1bd6e32c1d7d1a7d7a58a3; _gcl_au=1.1.24844177.1707337890; _gid=GA1.2.701222984.1707337890; _gat_UA-137253515-1=1; _ga_XT2BHDJQNC=GS1.1.1707337890.1.1.1707337891.0.0.0; _ga=GA1.2.1477844306.1707337890; bm_sv=BBCDE96130F6C7C62DEB56406FFCE4CE~YAAQHWUQAslv616NAQAASP1EhRbylvBULjjKr8DeEexDutEjso7t7uxYP1kFfIXWKn8slDjVxM3Sprt8v8eKMPErAbcRQkYWzuZ6xkJ9V9XYdGLirdW2VeRU9EAhjTPNYhsKkeCG10Qc7rQ/yHOBUH4zwMRVlFcXizYtADSl1OT/NRIAUh461SnGDvBimTM/+Z+ujI/vNQ4R1yyXXk/7S2FLQzsvpv3XLi5nt1tbzupXF58Rt3C6CBpgZrfIf+WMkx5x0MOut/LRydUQ~1',
        'dnt': '1',
        'referer': 'https://www.ticket-onlineshop.com/ols/bvb/de/profis/channel/shop/index/',
        'sec-ch-ua': '"Not A(Brand";v="99", "Google Chrome";v="121", "Chromium";v="121"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'document',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-user': '?1',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36',
    }

    event_id = int(input("EVENT ID: "))

    response = requests.get(
        f'https://www.ticket-onlineshop.com/ols/bvb/de/profis/channel/shop/areaplan/venue/event/{event_id}',
        cookies=cookies,
        headers=headers,
    )

    html_content = str(response.text)

    match = re.search(r"areaList: (\[.*?\]),\s*eventId:", html_content, re.DOTALL)
    if match:
        area_list_str = match.group(1)
        # Konvertiere den String in ein Python-Objekt
        area_list = json.loads(area_list_str)
        
        # Durchsuche die areaList nach der Nordtribüne und ihren freien Plätzen
        for area in area_list:
            name = html.unescape(area["name"])
            if name == "Alle Tribünen":
                continue
            print(f"Tribüne: {name}\nFreie Plätze: {area['freeSeats']}")
    else:
        print("Bereichsliste nicht gefunden.")
