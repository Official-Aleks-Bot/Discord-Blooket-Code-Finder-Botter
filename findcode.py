import requests
import random
from concurrent.futures import ThreadPoolExecutor
import argparse
import time

def generate_code():
    return str(random.randint(1000000, 9999999))

def check_code(code, webhook_url):
    url = "https://fb.blooket.com/c/firebase/id?id=" + code

    headers = {
        "Host": "fb.blooket.com",
        "Cookie": "_ga=GA1.1.652304743.1727505434; bsid=MTcyNzUwNTQzNXxMSEQ5Q1JkRlgzeDkxX0I2SGNJZDZEQ0t0WHBPMkJlcVlOQ3d3X0dpalNVM2NwR2FWUFZmbjRka0FMaz18RlST7EjNbxOqVQTBtlJf5RIAWrRpredKRzwCDEEHC70=; _ga_XPTRQH7XY5=GS1.1.1727505433.1.0.1727505435.0.0.0",
    }

    message = {
        'content': 'Working code found: ' + code
    }

    response = requests.get(url, headers=headers)
    if "true" in response.text:
        requests.post(webhook_url, json=message)
        print("Working code found: " + code)
    else:
        print("Failed: " + code)

def main(webhook_url):
    start_time = time.time()  # Record the start time
    run_duration = 5 * 60 * 60  # 5 hours in seconds

    with ThreadPoolExecutor(max_workers=6) as executor:
        while True:
            code = generate_code()
            executor.submit(check_code, code, webhook_url)

            # Check if 5 hours have passed
            if time.time() - start_time > run_duration:
                print("5 hours have passed. Stopping the process.")
                break

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Webhook URL for Discord notifications.')
    parser.add_argument('webhook_url', type=str, help='The Discord webhook URL')
    args = parser.parse_args()
    main(args.webhook_url)
