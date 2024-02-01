# Importe
import json
import time
import requests
import tls_client

# Konstantendefinitionen
REQUEST_DELAY = 10
bot_token = "6602448853:AAFVqBmsIes9h0cC3YINOVIGxWiBrLBjDmo"
chat_id = "-4153744196"
product_id = 20123412
event_id = 1977  # Bayern Spiel

blocks = [
    848, 849, 850, 851, 854, 855, 856, 857, 861, 862, 864, 865, 866, 867, 868, 869,
    870, 871, 872, 873, 874, 875, 876, 877, 880, 881, 882, 883, 884, 885, 886, 887,
    888, 889, 890, 891, 893, 894, 895, 896, 897, 898, 899, 900, 901, 902, 903, 904,
    905, 906, 907, 908, 909, 910, 911, 912, 913, 914, 915, 916, 917, 918, 919, 931,
    932, 933, 934, 935, 936, 938, 939, 940, 941, 942, 943, 944, 945, 946, 947, 948,
    953, 954, 955, 956, 957, 958, 959, 960, 961, 962, 963, 964, 965, 966
]

headers = {
    'auth-apf': 'eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJpc3MiOiJCYXllcjA0IiwiZXhwIjoxNzA2ODE4MjI1LCJpYXQiOjE3MDY3ODIyMjUsImN1c3RvbWVyX2dyb3VwcyI6IlNPTkRFUjIsU09OREVSMSxDTFVCLERLLU0yIiwic2NvcGUiOiIiLCJjb250YWN0X2lkIjoiMTk3YzBmZWEtY2UyMC00N2YxLTkwYTctOTg1MWEwMDI5YmVhIn0.vmCZVVGgle5nalO6kRoEuCULWldGU9qCJrbCtE_6k2xjM59_pg4B4GQGu08iG38C46dWTObVNfDEaQVlZz6_jdI0094cR1_pEpNIkzNJJKnztMat3zgJFTeSeLvzDOBeXtICu7u9HuFzKhUyFxOEAvSO8uzH7P0NV5gmDx327VS42zRhj12fpP_qYuLT3NeHw-ubjxy7TmdopgPVptvm_kUROTaz4Syazljn1dkdmRQp7OxcGVjoEyxMeKCmcJTqPYBv7qHElJg8O4JgohDrGjzzS6kVKBAAJkNsFdEKzSpA13JKIR4DErMAWL3HsQK_SI-WGZswE1DyIo-Est-55XyHBW3S6PmZNqimEl7TPCJteieVHue5cRObGgyq6DQ_YiBu8BhKW-iGPfA5gqfRrvYof_1mTF6G5E-qJqWY9djrIWaOPRLq_trA1mRocsyS1s5dEIX9aDvd-zUoIBsd7cVwlE_MCdjGLywWO3JxnToy6SHDk7gnywYdmIQPubEs5AoK5VNdR0jnkxc7wVYQ1EG9MBLAEbtSzyKc0OEVt82WTAVQGcmYNyELckWxDNYhGEvAxkDqoRQUpJyPjqkkZrbDgPqQXJsy_dnwq1CYWV-y-H1UX0l3mslPhIsXlG41wcUtSSHtrFOWbciKrVLa_lVJjUAEWnMd9BclPXbuqlU',
    'auth-tws': 'eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJpc3MiOiJ0d3MiLCJhdWQiOiJ1cm46Y3VzdG9tZXIiLCJpYXQiOjE3MDY3ODkwNTMsImV4cCI6MTcwNjc5MjY1Mywic2Vzc2lvbl9pZCI6ImNkMDAyNTY4Zjk4OGY1MTM4MWFhNzc3N2YxMWE1NyJ9.nynO2mdv0m5yF-pbUrPRP6awitLwoImPKKNj-ZYg4JP-WL8g9YhqOHE4n1l7JABoA7yFPLj0Xu_KEdfG86H6Qx4cCV_8TV_-WrdOxOSN_JlpRUEMeeifq4rgVrw9cguDlzi7jMqXcs9LVgJkO_5SubuxN-6Hz9yJx1btS3lNQ9Hva7nVvhFD2t_lkK5wtJRl4CU9-Hla-Owk0b7jOf6FeIG8Ifnzlx159SLDncCzSze2FqjuGWArp_H98NNRzL7BMWIOena9Q5_MDL4gUqD2IEwGaBXGeJ7Yxgtk0pKQnI41fnTlzUp1U3UAF6VpikQXHnOEphYmBLudDHazyNReBg',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36'
}

cookie = {
    "domain": "www.bayer04.de",
    "name": "QueueITAccepted-SDFrts345E-V3_b04tickets20240131",
    "path": "/",
    "secure": False,
    "value": "EventId%3Db04tickets20240131%26QueueId%3D889acef0-cebc-4d6b-aab7-478ba44b4912%26RedirectType%3Dsafetynet%26IssueTime%3D1706793748%26Hash%3D3b6916767a2e0074f8972a10e34f707f1316be1b5c50ad08c5c2f192c6c22747",
}

# Session-Initialisierung
session = tls_client.Session(
    client_identifier="chrome_112",
    random_tls_extension_order=True,
)

session.cookies.set(**cookie)

print(session.cookies.values())



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

    while True:
        try:
            for block in blocks:
                response = session.get(f'https://tss-al.bayer04.de/api/private/seats/{event_id}/{block}', headers=headers)
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
                    pass
                else:
                    print(f"Unexpected status code: {status_code}")
                    print(response.text)
                    send_telegram_message(bot_token, chat_id, f"Unexpected status code: {status_code}. Laurenz kontaktieren", 'Markdown')
                    time.sleep(6000)
                time.sleep(0.1)
            print("Request delay..")
            time.sleep(REQUEST_DELAY)
        except:
            time.sleep(1)
            continue


# Hauptfunktionaufruf
check_seats()
