import os

class Term:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


def display_information(url_objects, INTERVAL):
    def format_status(status):
        if status == 200:
            return Term.OKGREEN + "OK" + Term.ENDC
        elif status > 200:
            # TODO: yellow doesn't seam to work. But why?
            return Term.WARNING + str(status) + Term.ENDC
        else:
            return Term.FAIL + "FAILED" + Term.ENDC

    os.system("clear")

    print(f"URL-Checker\n"
          f"Interval: {INTERVAL}\n")

    for url_object in url_objects.objects:
        print(f"{url_object.url:35}  AVERAGE_RUNTIME: {url_object.average_runtime:<8.3f} \
                    STATUS_NOW: {format_status(url_object.status):>5}")

        for event in url_object.status_history[-3:]:
            print(f"{event[0]:>25}  RUNTIME: {event[2]:8.4f} STATUS: {format_status(event[1]):>5}")
        print()