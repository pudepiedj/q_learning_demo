import threading
import time
import json as js
import urllib
import numpy as np
import requests

def counter(i):
        print("starting counting\n")
        print("time for a nap!\n")
        time.sleep(i)
        print("finishing counting\n")
	
def getbtc():
	print("starting data pull")
	#dataLink = https://spreadsheets.google.com/feeds/list/=/1/public/basic
	data = requests.get('https://spreadsheets.google.com/feeds/list/0AhySzEddwIC1dEtpWF9hQUhCWURZNEViUmpUeVgwdGc/1/public/basic?alt=json').json()
	#	data = data.read().decode("utf-8")
	#read_data = requests.get(data).js()
	#data = data.split("}], ")
	print(data)
	
if __name__ == "__main__":
	print("Main thread started\n")
	time.sleep(1)
	t = threading.Thread(target = counter, args = (1, ))
	tbtc = threading.Thread(target = getbtc)
	tbtc.start()
	time.sleep(1)
	print("Main thread finished\n")
