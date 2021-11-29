import sys
from concurrent import futures
from time import sleep
import threading
import queue

from mymodules.config import read_config, MyConfig
from mymodules.classes import AllObjects
from mymodules.views import display_information
from mymodules.controls import my_controls, read_kbd_input

if __name__ == '__main__':
    read_config()
    url_objects = AllObjects(MyConfig.URL_LIST)
    input_queue = queue.Queue()

    # define threads
    control_thread = threading.Thread(target=my_controls, args=(input_queue, ), daemon=True)
    read_kbd_thread = threading.Thread(target=read_kbd_input, args=(input_queue, ), daemon=True)

    # start controls, keyboard once
    read_kbd_thread.start()
    control_thread.start()

    # loop other threads
    while True:
        update_urls_thread = threading.Thread(target=url_objects.update_all, daemon=True)
        update_urls_thread.start()

        display_thread = threading.Thread(target=display_information, args=(url_objects,), daemon=True)
        display_thread.start()

        sleep(MyConfig.INTERVAL)


    sys.exit()
    with futures.ThreadPoolExecutor(max_workers=5) as e:
        e.submit(my_controls, input_queue)
        e.submit(read_kbd_input, input_queue)

        while True:
            e.submit(url_objects.update_all)
            e.submit(display_information, url_objects)
            sleep(MyConfig.INTERVAL)







