import os
import sqlite3
import sys
from concurrent import futures
import validators
import requests
from datetime import datetime
from time import sleep

# basic parameters, may get overridden by config.conf
INTERVAL = 2
URLS = [
    "https://www.jura.uni-bonn.de",
    "https://cloud.jura.uni-bonn.de",
    "https://gpil.jura.uni-bonn.de",
    "https://seminar.jura.uni-bonn.de"
]


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
                INTERVAL = seconds

            urllist_temp = []
            for url in urls:
                if validators.url(url):
                    urllist_temp.append(url)
                else:
                    print(f"config_error: given url {url} is not a valid url. use https://domain.com")
                    print("skipped url {url}.")

            if len(urllist_temp) > 0:
                URLS = urllist_temp

    else:
        with open("config.conf", "w") as config_file:
            sample_config = """[config]
            interval=2
            urls=
                https://google.de
                https://anyothersite.com
            """
            config_file.write(sample_config)








# interval in seconds
DATABASE = 'checks.db'

# list of websites to check



def db_connect(database):
    # connect to database
    try:
        conn = sqlite3.connect(database, check_same_thread=False)
    except:
        print("Database error - quitting...")
        sys.exit()
    else:
        return conn


def db_ready_database():
    # table exists?
    sql_check_table = """SELECT name FROM sqlite_master WHERE type='table' AND name='checks'"""

    c.execute(sql_check_table)
    if len(c.fetchall()) != 1:
        sql_create = """CREATE TABLE checks (id INTEGER PRIMARY KEY, site TEXT NOT NULL, date TEXT, result INTEGER, runtime INTEGER)"""
        c.execute(sql_create)
        conn.commit()


def db_write_to_database(result):
    (site, time_str, status_code, runtime) = result
    sql = """INSERT INTO checks (site, date, result, runtime) VALUES (?,?,?,?)"""
    c.execute(sql, (site, time_str, status_code, runtime))
    conn.commit()


def check_all():
    for site in URLS:
        try:
            r = requests.get(site)
            if r.status_code == 200:
                now_string = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
                runtime = r.elapsed.total_seconds()
                result = (site, now_string, 200, runtime)
                db_write_to_database(result)
            else:
                now_string = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
                runtime = r.elapsed.total_seconds()
                result = (site, now_string, r.status_code, runtime)
                db_write_to_database(result)

        except Exception:   # request fails
            now_string = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
            result = (site, now_string, -1, -1)
            db_write_to_database(result)

    sleep(INTERVAL)


def display_information(website_index=-1):
    """
    :param website_index:   -1 returns all results for all websites
                            0 - len(URLS) returns results of specific website
    """

    os.system('clear')

    # generate sql command in list
    sql = []
    if -1 < website_index < len(URLS):
        sql.append(f"""SELECT * FROM checks WHERE site = '{URLS[website_index]}' ORDER BY site, date LIMIT 20""")
    elif website_index == -1:
        for website in URLS:
            sql.append(f"""SELECT * FROM checks WHERE site = '{website}' ORDER BY site, date LIMIT 3""")
    else:
        # TODO: raise exception
        print("display_information() - we are out of index")
        sys.exit()

    for _ in sql:
        c.execute(_)
        result = c.fetchall()
        print(f"Checks for {result[0][1]}:")
        for line in result:
            print(f".................{line[2:]}")
    sleep(INTERVAL)


if __name__ == '__main__':
    read_config()
    conn = db_connect(DATABASE)
    c = conn.cursor()
    db_ready_database()

    # different threads for websites checks and displaying information

    with futures.ThreadPoolExecutor(max_workers=2) as e:
        e.submit(check_all)
        e.submit(display_information)






