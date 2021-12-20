import data_analysis
import time
import os

data_analysis.main()
time.sleep(5)
os.system('wireviz data.yml')
os.rename('data.html','index.html') 