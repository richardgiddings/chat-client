import requests
import threading
import argparse
import os
from decouple import config


BASE_URL = config("BASE_URL")


def connect(url, username):
    s = requests.Session()

    print(f"Connected to {url} as {username}")
    print("Type a message and press return to send it.")
    print("Type 'exit' and press return to exit the chat.\n")

    with s.get(url, headers=None, stream=True) as resp:
        for line in resp.iter_lines():
            if line:
                parsed = line.decode('ascii')[2:-1]
                if f"[{username}]" not in parsed:
                    print(parsed)


def chat(user, channel):
    while True:
        text = input()
        if text == "exit":
            os._exit(1)
        requests.post(f"{BASE_URL}/post", data={"message": text, "user": user, "channel": channel})


if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument("username")
    parser.add_argument("channel")
    args = parser.parse_args()

    thread1 = threading.Thread(target=connect, args=(f"{BASE_URL}/stream",args.username))
    thread1.start()

    thread2 = threading.Thread(target=chat, args=(args.username,args.channel,))
    thread2.start()