import os
import sqlite3
import sys
from concurrent import futures
import validators
import requests
from datetime import datetime
from time import sleep

# version 0.2
# still working with sqlite3

# basic parameters, may get overridden by config.conf
_interval = 2
_url_list = [
    "https://www.jura.uni-bonn.de",
    "httpass://cloud.jura.uni-bonn.de",
]


class AllObjects:
    def __init__(self, url_list):
        self.urls = url_list
        self.objects = []
        self.get_objects()

    def get_objects(self):
        for _ in self.urls:
            self.objects.append(UrlObject(_))

    def update_all(self):
        for _ in self.objects:
            _.update()

    def print_all(self):
        print("Last three checks of each url:")
        for _ in self.objects:
            print([print(f"{event}") for event in _.status_history[-3:]])
            print()

    def __repr__(self):
        return f"contains a list of {len(self.objects)} UrlObjects"


class UrlObject:
    def __init__(self, url):
        self.url = url
        self.status = -1
        self.runtime = 0
        self.average_runtime = 0
        self.status_history = []

    def update(self):
        now_string = datetime.now().strftime("%d/%m/%Y %H:%M:%S")

        try:
            r = requests.get(self.url)
            status = r.status_code
            runtime = r.elapsed.total_seconds()

        except Exception:  # request fails completely
            status = -1
            runtime = -1

        self.status = status
        self.runtime = runtime
        self.status_history.append((now_string, status, runtime))
        self.calculate_average_runtime()

    def calculate_average_runtime(self):
        if self.status == -1:
            self.average_runtime = -1
        else:
            # TODO: -1 gets counted here... needs a change
            self.average_runtime = sum([(float(event[2])) for event in self.status_history]) \
                                   / len(self.status_history)

    def reset(self):
        self.status = -1
        self.status_history = []

    def __repr__(self):
        return f"{self.url} is {self.status}"


def read_config():
    if os.path.isfile("config.conf"):
        import configparser
        config = configparser.ConfigParser()

        try:
            config.read('config.conf')
            seconds = int(config['config']['interval'])
            urls = config['config']['urls'].strip().splitlines()
        except Exception:
            print("could not parse config.conf. Using hardcoded parameters")
            return

        else:
            if 1 < seconds < 15:
                _interval = seconds

            urllist_temp = []
            for url in urls:
                if validators.url(url):
                    urllist_temp.append(url)
                else:
                    print(f"config_error: given url {url} is not a valid url. use https://domain.com")
                    print("skipped url {url}.")

            if len(urllist_temp) > 0:
                _url_list = urllist_temp

    else:
        with open("config.conf", "w") as config_file:
            sample_config = """[config]
            interval=2
            urls=
                https://google.de
                https://anyothersite.com
            """
            config_file.write(sample_config)



def display_information():
    os.system("clear")
    for object in url_objects.objects:
        print(f"{object.url}        right now: {object.status}      average runtime: {object.average_runtime:.3f}")
        for event in object.status_history[-3:]:
            print(f"            {event[0]}:     STATUS: {event[1]}      runtime: {event[2]:.4f}")
        print()


if __name__ == '__main__':
    read_config()
    url_objects = AllObjects(_url_list)

    o = url_objects.objects[0]
    pass
    for i in range(10):
        url_objects.update_all()
        display_information()
        sleep(2)


    print("eins vor ende")
    print("ende")




