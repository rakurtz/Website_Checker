import sys
import threading
import queue

from mymodules.config import read_config, MyConfig
from mymodules.classes import AllObjects
from mymodules.views import display_information
from mymodules.controls import my_controls, read_kbd_input


def start_threads(url_objects, key_control_queue, data_queue):
    threads = []

    # threads in deamon mode to end them automatically with end of main thread
    read_kbd_thread = threading.Thread(target=read_kbd_input, args=(key_control_queue,), daemon=True)
    update_urls_thread = threading.Thread(target=url_objects.update_all, daemon=True)
    display_thread = threading.Thread(target=display_information, args=(url_objects,), daemon=True)

    read_kbd_thread.start()
    threads.append(read_kbd_thread)

    update_urls_thread.start()
    threads.append(update_urls_thread)

    display_thread.start()
    threads.append(display_thread)

    return threads


if __name__ == '__main__':
    read_config()
    key_control_queue = queue.Queue()

    # TODO: Use queue to transport data from url_objects to views.
    data_queue = queue.Queue()

    url_objects = AllObjects(MyConfig.URL_LIST)

    # start background threads
    my_threads = start_threads(url_objects, key_control_queue, data_queue)

    # controls remains in main thread
    controls_exit = my_controls(key_control_queue)

    if controls_exit == -1:
        sys.exit()







