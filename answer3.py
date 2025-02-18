# Q3. Uptime Monitoring and Alert System
# Write a Python script that checks the uptime of provided URLs and notifies the user if any of the URLs return
# 4xx or 5xx HTTP status codes (indicating client or server errors). For demonstration purposes, you can use
# the following URLs as inputs:

import requests;
import time;

def checkURLS(urls):
    
    for url in urls:
        
        try:
            res=requests.get(url,timeout=10)
            resStatusCode=res.status_code
            resReason=res.reason
            
            print(f"{url}->{resStatusCode} : {resReason}")
            
            if 400 <= resStatusCode < 600:
                print(f"Alert error code {resStatusCode}!")

        except requests.exceptions.RequestException as e:
            print(f"e")
            
            
            
def monitor(urls):
    while True:
        checkURLS(urls)
        time.sleep(10)
        
        
urls = ["http://www.example.com/nonexistentpage",  
    "http://httpstat.us/404",                   
    "http://httpstat.us/500",                  
    "https://www.google.com/" ]

monitor(urls)
    