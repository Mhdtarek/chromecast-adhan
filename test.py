import schedule
import time
import os
 
stream = os.popen('echo Returned output')
output = stream.read()
output
def func():
    print("Geeksforgeeks")
  
schedule.every(1).minutes.do(func)
  
while True:
    schedule.run_pending()
    time.sleep(1)