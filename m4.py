#!/usr/pkg/bin/python

#Importing modules
import paramiko
import sys
import time
import ftplib
import os
import glob
 

#setting parameters like host IP, username, passwd and number of iterations to gather cmds






def upload(HOST, USER, PASS, fileaddres):
    ftp = ftplib.FTP(HOST)
    ftp.login(USER, PASS)
    ftp.storbinary('STOR '+fileaddres, open(fileaddres, 'rb'))
    ftp.quit()
    print "file :" + fileaddres + "  uploaded to " + HOST


def fn(HOST, USER, PASS, command):
  client1=paramiko.SSHClient()
  #Add missing client key
  client1.set_missing_host_key_policy(paramiko.AutoAddPolicy())
  #connect to switch
  client1.connect(HOST,username=USER,password=PASS)
  print "SSH connection to %s established" %HOST
  #Gather commands and read the output from stdout
  stdin, stdout, stderr = client1.exec_command(command)
  out = stdout.read()
  print "Logged out of device %s" %HOST
  return out
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
    else:
      return "error"


f = open('ip.txt','r')
message = f.read()
mel=message.split("\n")
count = len(mel)
for x in xrange(count-1):
  try:
    mela = mel[x].split('/')
    HOST = str(mela[0])
    USER = str(mela[1])
    PASS = str(mela[2])
    fileaddres = chek(fn(HOST, USER, PASS, '/system resource print\n'))
    upload(HOST, USER, PASS, fileaddres)
    fn(HOST, USER, PASS, '/system reboot \n')
    os.chdir("..")
    print "%s completed" % HOST
    print "****************************************"
  except:
    print "error in : " + HOST
f.close()


# HOST = "172.19.2.209"
# USER = "admin"
# PASS = "M@dar123456"
# ITERATION = 1
# fileaddres = ""



# #for loop to call above fn x times. Here x is set to 3
# for x in xrange(ITERATION):






