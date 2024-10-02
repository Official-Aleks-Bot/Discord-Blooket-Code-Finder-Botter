import requests
import random
from concurrent.futures import ThreadPoolExecutor
import argparse
import time
import os
import subprocess

Threads = 40
bsid = None

def get_bsid():
    global bsid

    url = "https://play.blooket.com/play"
    response = requests.get(url)
    set_cookie = response.headers.get('Set-Cookie')
    if set_cookie:
        for cookie in set_cookie.split(';'):
            if cookie.strip().startswith('bsid='):
                bsid = cookie.split('=')[1]
                break
        else:
            print("bsid not found in Set-Cookie.")
    else:
        print("Set-Cookie header not found.")

def generate_code():
    return str(random.randint(1000000, 9999999))
    #return "4323135" Set code here for testing

def check_code(code, webhook_url):
    url = "https://fb.blooket.com/c/firebase/id?id=" + code

    headers = {
        "Host": "fb.blooket.com",
        "Cookie": f"bsid={bsid}=;",
    }

    message = {
        #'content': '@here Working code found: ' + code No more pings pls
        'content': 'Working code found, beginning to bot...: ' + code
    }

    response = requests.get(url, headers=headers)
    if "true" in response.text:
        requests.post(webhook_url, json=message)
        print("Working code found, beginning to bot...: " + code)
        #subprocess.run(["python3", "obuscatedbotter.py", code], check=True, capture_output=True, text=True)
    #else:
        #print("Failed: " + code) 
        # Your not even gonna look at this use for debug only

def main(webhook_url):
    start_time = time.time()  # sets the current time for later use
    run_duration = 5 * 60 * 60  # 5 hours in seconds...
    #startmessage = {'content': 'New Bot started! Scanning...'}
    #requests.post(webhook_url, json=startmessage)
    get_bsid()
    print("Started!")

    with ThreadPoolExecutor(max_workers=Threads) as executor:
        while True:
            code = generate_code()
            executor.submit(check_code, code, webhook_url)

            # Check if 5 hours have passed
            if time.time() - start_time > run_duration:
                print("5 hours have passed. Stopping the process.")
                os._exit(0)  # Forcefully exit the program

            time.sleep(0.01)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Webhook URL for Discord notifications.')
    parser.add_argument('webhook_url', type=str, help='The Discord webhook URL')
    args = parser.parse_args()
    main(args.webhook_url)
