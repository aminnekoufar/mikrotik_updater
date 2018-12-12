#!/usr/pkg/bin/python

#Importing modules
import paramiko
import sys
import time
import ftplib
import os
import glob
 

#setting parameters like host IP, username, passwd and number of iterations to gather cmds
HOST = "172.19.2.209"
USER = "admin"
PASS = "M@dar123456"
ITERATION = 1
filename="a.txt"


def upload(HOST, USER, PASS, filename):
    ftp = ftplib.FTP(HOST)
    ftp.login(USER, PASS)
    ftp.storbinary('STOR '+filename, open(filename, 'rb'))
    ftp.quit()


def fn(command):
  client1=paramiko.SSHClient()
  #Add missing client key
  client1.set_missing_host_key_policy(paramiko.AutoAddPolicy())
  #connect to switch
  client1.connect(HOST,username=USER,password=PASS)
  print "SSH connection to %s established" %HOST
  #Gather commands and read the output from stdout
  stdin, stdout, stderr = client1.exec_command(command)
  # print stdout.read()
  out = stdout.read()
  chek(out)
  print "Logged out of device %s" %HOST
  client1.close()
def chek(out):
  if "mipsbe" in out:
    aname="mipsbe"
  elif "smips" in out:
    aname="smips"
  elif "tile" in out:
    aname="tile"
  elif "ppc" in out:
    aname="ppc"
  elif "arm" in out:
    aname="arm"
  elif "x86" in out:
    aname="x86"
  elif "mmips" in out:
    aname="mmips"
  elif "general" in out:
    aname="geenral"
  else:
    print "not in range!!!!"
  print "mikrotik architecutre-name : " + aname
  filefund(aname)

def filefund(anme):
  os.chdir("file")
  for file in glob.glob("*.npk"):
    if file.split("-")[1] == "tile":
         print file
#for loop to call above fn x times. Here x is set to 3
for x in xrange(ITERATION):
  # upload(HOST, USER, PASS, filename)
  chekcommand = '/system resource print\n'
  reboot = "/system reboot \n"
  fn(chekcommand)
  print "%s Iteration/s completed" %(x+1)
  print "********"





