import os
import sys
from concurrent import futures
import validators
import requests
from datetime import datetime
from time import sleep
import configparser

# version 0.2
# still working with sqlite3

# basic parameters, may get overridden by config.conf

my_config = {
    "INTERVAL": 2,
    "URL_LIST": [
        "https://www.jura.uni-bonn.de",
        "httpass://cloud.jura.uni-bonn.de",
    ]
}

class Term():
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


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
                my_config["INTERVAL"] = seconds

            urllist_temp = []
            for url in urls:
                if validators.url(url):
                    urllist_temp.append(url)
                else:
                    print(f"config_error: given url {url} is not a valid url. use https://domain.com")
                    print("skipped url {url}.")

            if len(urllist_temp) > 0:
                my_config['URL_LIST'] = urllist_temp

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
    def format_status(status):
        if status == 200:
            return Term.OKGREEN + "OK" + Term.ENDC
        elif status > 200:
            # TODO: yellow doesn's seam to work. But why?
            return Term.WARNING + status + Term.ENDC
        else:
            return Term.FAIL + "FAILED" + Term.ENDC

    os.system("clear")

    print(f"URL-Checker\n"
          f"Interval: {my_config['INTERVAL']}\n")

    for object in url_objects.objects:
        print(f"{object.url:35}  AVERAGE_RUNTIME: {object.average_runtime:<8.3f} \
                    STATUS_NOW: {format_status(object.status):>5}")

        for event in object.status_history[-3:]:
            print(f"{event[0]:>25}  RUNTIME: {event[2]:8.4f} STATUS: {format_status(event[1]):>5}")
        print()


if __name__ == '__main__':
    read_config()
    url_objects = AllObjects(my_config['URL_LIST'])

    with futures.ThreadPoolExecutor(max_workers=3) as e:
        while True:
            e.submit(url_objects.update_all)
            e.submit(display_information)
            sleep(my_config["INTERVAL"])


    print("eins vor ende")
    print("ende")




