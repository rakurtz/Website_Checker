import requests
from datetime import datetime


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
