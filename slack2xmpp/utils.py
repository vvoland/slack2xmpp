#!/usr/bin/env python3
import time

from threading import Thread


def main_loop(clients):
    try:
        threads = []
        for client in clients:
            thread = Thread(target=client.connect)
            threads.append(thread)
            thread.start()

        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        for client in clients:
            client.close()
