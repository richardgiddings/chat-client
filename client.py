import requests
import threading
import argparse
import os
from decouple import config


BASE_URL = config("BASE_URL")


def get_active_channels():
    
    channels = requests.Session().get(f"{BASE_URL}/active_channels")

    if channels.content:
        print("Active channels:")
        print(channels.content.decode('ascii'))
    else:
        print("There are currently no active channels.")


def connect(url, username, channel):

    try:
        s = requests.Session()

        print(f"Connected to chat {channel} as {username}")
        print("Type a message and press return to send it.")
        print("Type 'exit' and press return to exit the chat.\n")

        with s.get(url+"?channel="+channel, headers=None, stream=True) as resp:
            for line in resp.iter_lines():
                if line:
                    parsed = line.decode('ascii')[2:-1]
                    if f"[{username}]" not in parsed:
                        print(parsed)
    except ConnectionError:
        print("Connection dropped. The server might not be running.")
        os._exit(1)
    except:
        print("An unknown error occurred.")
        os._exit(1)


def chat(user, channel):
    while True:
        text = input()
        if text == "exit":
            os._exit(1)
        requests.post(f"{BASE_URL}/post", data={"message": text, "user": user, "channel": channel})


if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument('-list', action='store_true')
    parser.add_argument('-join', nargs=2)
    args = parser.parse_args()

    if args.list:
        get_active_channels()
    
    if args.join:
        args_list = args.join
        username = args_list[0]
        channel = args_list[1]

        thread1 = threading.Thread(target=connect, args=(f"{BASE_URL}/stream", username, channel,))
        thread1.start()

        thread2 = threading.Thread(target=chat, args=(username,channel,))
        thread2.start()