#import threading
import queue
import sys
import time
from threading import Lock
from .views import ViewSate


def read_kbd_input(input_queue):
    """ must be startet from main module"""
    while True:
        input_str = input()
        input_queue.put(input_str)


def my_controls(input_queue):
    """ with e as ThreadPoolExecutor"""
    EXIT = "q"
    MAIN_VIEW = "m"
    SINGLE_VIEW = "s"
    SELECT_URL = "0123456789"

    lock = Lock()

    while True:
        if input_queue.qsize() > 0:
            input_str = input_queue.get()

            if input_str == EXIT:
                print("Exiting serial terminal.")
                return -1
            elif input_str == MAIN_VIEW:
                with lock:
                    ViewSate.VIEW = 0
            elif input_str == SINGLE_VIEW:
                with lock:
                    ViewSate.VIEW = 1
            elif input_str in SELECT_URL:
                with lock:
                    ViewSate.ACTIVE_URL = input_str

        time.sleep(0.1)
