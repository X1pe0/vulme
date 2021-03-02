import time 
import sys
import os
import subprocess
from netaddr import iter_iprange
from threading import Thread
import threading
from signal import signal, SIGINT
from sys import exit
def clear():
    if os.name =="nt":
        os.system("cls")
    else:
        os.system("clear")
def prompt_sudo():
    ret = 0
    if os.geteuid() != 0:
        msg = "[sudo] password for %u:"
        ret = subprocess.check_call("sudo -v -p '%s'" % msg, shell=True)
    return ret
user = os.getenv("SUDO_USER")
if user is None:
    print ("This program need 'sudo'")
    prompt_sudo()
##Thread limit##
thread_limit = 5
## Set A mode to True if you would like hosts that only respond to ICMP ##
a_mode = False
## Don't overwrite reports? ##
os_path_mode = False
def logo():
    print ('''
 __   __    _ __  __     
 \ \ / /  _| |  \/  |___ 
  \ V / || | | |\/| / -_)
   \_/ \_,_|_|_|  |_\___|
                     v1.0                    
    ''')
try:
    IP_range_Start = sys.argv[1]
    IP_range_Stop = sys.argv[2]
    port_range_start = sys.argv[3]
    port_range_stop = sys.argv[4]
except:
    logo()
    print ('vulme <IP-Range-Start> <IP-Range-Stop> <Port-Range-Start> <Port-Range-Stop>')
    print ('Ex: vulme 127.0.0.1 127.0.1.1 0 1000')
    exit(0)
threadLock = threading.Lock()
with threadLock:
    generator = iter_iprange(IP_range_Start, IP_range_Stop, step=1)
def scanit(num):
    for ips in generator:
        logo()
        print ('Worker: %s Scanning - %s'%(num,ips))
        if a_mode == False:
            if os_path_mode == True:
                if not os.path.exists((str(ips))+".html"):
                    stdout = subprocess.getoutput("nmap --max-rtt-timeout 2 --max-scan-delay 1 --max-retries 1 --version-intensity 0 -sV --script=banner,vuln -sU -sT -p%s-%s --min-rate 100000 -oX - "%(port_range_start,port_range_stop) + str(ips))
                    with open(str(ips)+".scan",'w') as f: f.write(stdout)
                    stdout = subprocess.getoutput("xsltproc %s.scan -o %s.html"%(ips,ips))
                    os.system("cp %s.scan ./raw/%s.scan_raw.txt"%(ips,ips))
                    os.system("rm %s.scan"%(ips))
                else:
                    pass
            else:
                stdout = subprocess.getoutput("nmap --max-rtt-timeout 2 --max-scan-delay 1 --max-retries 1 --version-intensity 0 -sV --script=banner,vuln -sU -sT -p%s-%s --min-rate 100000 -oX - "%(port_range_start,port_range_stop) + str(ips))
                with open(str(ips)+".scan",'w') as f: f.write(stdout)
                stdout = subprocess.getoutput("xsltproc %s.scan -o %s.html"%(ips,ips))
                os.system("cp %s.scan ./raw/%s.scan_raw.txt"%(ips,ips))
                os.system("rm %s.scan"%(ips))
        else:
            response = os.system("ping -w 1 -c 1 " + str(ips) + " > scan.log")
            if response == 0:
                if os_path_mode == True:
                    if not os.path.exists((str(ips))+".html"):
                        stdout = subprocess.getoutput("nmap --max-rtt-timeout 2 --max-scan-delay 1 --max-retries 1 --version-intensity 0 -sV --script=banner,vuln -sU -sT -p%s-%s --min-rate 100000 -oX - "%(port_range_start,port_range_stop) + str(ips))
                        with open(str(ips)+".scan",'w') as f: f.write(stdout)
                        stdout = subprocess.getoutput("xsltproc %s.scan -o %s.html"%(ips,ips))
                        os.system("cp %s.scan ./raw/%s.scan_raw.txt"%(ips,ips))
                        os.system("rm %s.scan"%(ips))
                    else:
                        pass
                else:
                    stdout = subprocess.getoutput("nmap --max-rtt-timeout 2 --max-scan-delay 1 --max-retries 1 --version-intensity 0 -sV --script=banner,vuln -sU -sT -p%s-%s --min-rate 100000 -oX - "%(port_range_start,port_range_stop) + str(ips))
                    with open(str(ips)+".scan",'w') as f: f.write(stdout)
                    stdout = subprocess.getoutput("xsltproc %s.scan -o %s.html"%(ips,ips))
                    os.system("cp %s.scan ./raw/%s.scan_raw.txt"%(ips,ips))
                    os.system("rm %s.scan"%(ips))
            else:
                pass
threads = []
for i in range(thread_limit):
    #clear()
    t = threading.Thread(target=scanit, args=(i,))
    threads.append(t)
    t.start()
