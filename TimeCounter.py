import threading
import time
Limit = 30       #phut
def timeCounter():
    while True:
        time.sleep(60 * Limit)
        #updateData()
t = threading.Thread(target = timeCounter)
t.start()