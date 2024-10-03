import requests
import random
from concurrent.futures import ThreadPoolExecutor
import argparse
import time
import os
import subprocess

Threads = 25
bsid = None

def get_bsid():
    global bsid
    headers = {
    "Host": "play.blooket.com",
    "Sec-Ch-Ua": '"Not;A=Brand";v="24", "Chromium";v="128"',
    "Sec-Ch-Ua-Mobile": "?0",
    "Sec-Ch-Ua-Platform": '"Windows"',
    "Accept-Language": "en-US,en;q=0.9",
    "Upgrade-Insecure-Requests": "1",
    "User-Agent": "Mozilla/5.0 (X11; CrOS x86_64 14541.0.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
    "Sec-Fetch-Site": "none",
    "Sec-Fetch-Mode": "navigate",
    "Sec-Fetch-User": "?1",
    "Sec-Fetch-Dest": "document",
    }
    url = "https://play.blooket.com/play"
    response = requests.get(url, headers=headers)
    set_cookie = response.headers.get('Set-Cookie')
    if set_cookie:
        for cookie in set_cookie.split(';'):
            if cookie.strip().startswith('bsid='):
                bsid = cookie.split('=')[1] + "="
                break
        else:
            print("bsid not found in Set-Cookie.")
    else:
        print("Set-Cookie header not found.")

def generate_code():
    return str(random.randint(1000000, 9999999))
    #return "4948789"


def check_code(code, webhook_url):
    url = "https://fb.blooket.com/c/firebase/id?id=" + code
    get_bsid()
    headers = {
        "Host": "fb.blooket.com",
        'User-Agent': "Mozilla/5.0 (X11; CrOS x86_64 14541.0.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36", # Chrome OS is the best is it not? (jk, who acctually likes this)
        'Referer': 'https://fb.blooket.com',
        "Cookie": f"bsid={bsid}",
    }

    message = {
        #'content': '@here Working code found: ' + code No more pings pls
        'content': 'Working code found: ' + code
    }

    response = requests.get(url, headers=headers)
    if "true" in response.text:
        requests.post(webhook_url, json=message)
        print("Working code found, beginning to bot...: " + code)
        subprocess.run(["python3", "obuscatedbotter.py", code], check=True, capture_output=True, text=True)
    #else:
        #print("Failed: " + code) 
        #print(response.text)
        # Your not even gonna look at this use for debug only

def main(webhook_url):
    start_time = time.time()  # sets the current time for later use
    run_duration = 5 * 60 * 60  # 5 hours in seconds...
    #startmessage = {'content': 'New Bot started! Scanning...'}
    #requests.post(webhook_url, json=startmessage)
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
