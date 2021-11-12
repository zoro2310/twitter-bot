from funt.covidsos import coviddmfunt
from funt.checkmentions import check_mentions
from threading import *
import time
import gbv

class f1t(Thread):
        
    def run(self):
        while True:
            check_mentions()
            coviddmfunt()
            if gbv.stopthread:
                print("Background task killed")
                break
            time.sleep(90)

t1=f1t()


def start_scan():
    if gbv.stopthread:
        gbv.stopthread=False
        print("Starting DM Scan and Tweet Scan in background")
        t1.start()
    else:
        print("Already running")


def stop_scan():
    if gbv.stopthread:
        print("Already stoped")
    else:
        gbv.stopthread=True
        print("Removing DM Scan and Tweet Scan from background [may take upto 90 sec]")
        t1.join()