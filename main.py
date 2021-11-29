import sys
from concurrent import futures
from time import sleep

from mymodules.config import read_config, MyConfig
from mymodules.classes import AllObjects
from mymodules.views import display_information


if __name__ == '__main__':
    read_config()
    url_objects = AllObjects(MyConfig.URL_LIST)

    while True:
        url_objects.update_all()
        display_information(url_objects, MyConfig.INTERVAL)
        sleep(MyConfig.INTERVAL)


    sys.exit()
    with futures.ThreadPoolExecutor(max_workers=3) as e:
        while True:
            e.submit(url_objects.update_all)
            e.submit(display_information)
            sleep(MyConfig.INTERVAL)





