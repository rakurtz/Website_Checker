import os
import configparser
import validators


class MyConfig:
    INTERVAL = 2,
    URL_LIST = [
        "https://www.jura.uni-bonn.de",
        "https://cloud.jura.uni-bonn.de",
        "httpss://haserror.jura.uni-bonn.de",
    ]


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
                MyConfig.INTERVAL = seconds

            for url in urls:
                if validators.url(url):
                    MyConfig.URL_LIST.append(url)
                else:
                    print(f"config_error: given url {url} is not a valid url. use https://domain.com")
                    print("skipped url {url}.")

    else:
        with open("config.conf", "w") as config_file:
            sample_config = """[config]
            #interval=2
            #urls=
            #    https://google.de
            #    https://anyothersite.com
            """
            config_file.write(sample_config)
