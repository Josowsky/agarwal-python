import logging # This module is thread safe.
import threading

# LOCK = threading.Lock()

# def run(arg):
#     if LOCK.acquire(False): # Non-blocking -- return whether we got it
#         logging.info('Got the lock! {}'.format(arg))
#         LOCK.release()
#     else:
#         logging.info("Couldn't get the lock. Maybe next time")

# logging.basicConfig(level=logging.INFO)

# threads = []

# for i in range(100):
# 	threads.append(threading.Thread(target=run, args=[i]))

# for thread in threads:
#    thread.start()

NUMBER_OF_HOSTS = 32

tree = []
for i in range(NUMBER_OF_HOSTS):
    tree[i] = {
        'Node': i,
    }

_hosts = []
for i in range(NUMBER_OF_HOSTS):
    _hosts.append(threading.Thread(target=main, args=[i]))

HOSTS = _hosts

for host in HOSTS:
    host.start()