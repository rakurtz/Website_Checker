import requests
from datetime import datetime
from time import sleep
from threading import Lock



class AllObjects:
    def __init__(self, url_list):
        self.urls = url_list
        self.url_objects = []
        self.get_url_objects()

    def get_url_objects(self):
        for url in self.urls:
            self.url_objects.append(UrlObject(url))

    def update_all(self, loop=True):
        # TODO: parallelize io here...
        if loop:
            while True:
                for url_object in self.url_objects:
                    url_object.update()
                    sleep(0.2)
        else:
            for url_object in self.url_objects:
                url_object.update()

    def print_all(self):
        print("Last three checks of each url:")
        for _ in self.url_objects:
            print([print(f"{event}") for event in _.status_history[-3:]])
            print()

    def __repr__(self):
        return f"contains a list of {len(self.url_objects)} UrlObjects"

class UrlObject:
    def __init__(self, url):
        self.lock = Lock()
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

        with self.lock:
            self.status = status
            self.runtime = runtime
            self.status_history.append((now_string, status, runtime))

        self.calculate_average_runtime()

    def calculate_average_runtime(self):
        if self.status == -1:
            with self.lock:
                self.average_runtime = -1
        else:
            # TODO: -1 gets counted here... needs a change
            with self.lock:
                self.average_runtime = sum([(float(event[2])) for event in self.status_history]) \
                                       / len(self.status_history)

    def reset(self):
        self.status = -1
        self.status_history = []

    def __repr__(self):
        return f"{self.url} is {self.status}"
