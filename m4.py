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
fileaddres = ""

def upload(fileaddres):
    ftp = ftplib.FTP(HOST)
    ftp.login(USER, PASS)
    ftp.storbinary('STOR '+fileaddres, open(fileaddres, 'rb'))
    ftp.quit()
    print "file :" + fileaddres + "  uploaded to " + HOST






def fn(command):
  client1=paramiko.SSHClient()
  #Add missing client key
  client1.set_missing_host_key_policy(paramiko.AutoAddPolicy())
  #connect to switch
  client1.connect(HOST,username=USER,password=PASS)
  print "SSH connection to %s established" %HOST
  #Gather commands and read the output from stdout
  stdin, stdout, stderr = client1.exec_command(command)
  out = stdout.read()
  return out
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
    print "architecutre not fine!!!!"

  print "mikrotik architecutre-name : " + aname
  return filefund(aname)

def filefund(aname):
  os.chdir("file")
  for file in glob.glob("*.npk"):
    if file.split("-")[1] == aname:
      return file



f = open('ip.txt','r')
message = f.read()
mel=message.split("\n")
count = len(mel)
for x in xrange(count-1):
    mela = mel[x].split('/')
    address = mela[0]
    user = mela[1]
    password = mela[2]
f.close()
#for loop to call above fn x times. Here x is set to 3
for x in xrange(ITERATION):
  fileaddres = chek(fn('/system resource print\n'))
  upload(fileaddres)
  fn('/system reboot \n')
  print "%s completed" % HOST
  print "****************************************"





