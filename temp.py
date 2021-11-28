from concurrent import futures
from time import sleep, time


def test(s):
    sleep(s)
    print(f"{time():.0f} I waited {s} seconds.")



print(f"Startzeit: {time():.0f}")

with futures.ThreadPoolExecutor(max_workers=3) as e:
    e.submit(test, 10)
    e.submit(test, 20)

print("Done.")