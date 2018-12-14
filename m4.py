#!/usr/pkg/bin/python

#Importing modules
import paramiko
import sys
import time
import ftplib
import os
import glob
 
def upload(HOST, USER, PASS, fileaddres):
  try:
      ftp = ftplib.FTP(HOST)
      ftp.login(USER, PASS)
      ftp.storbinary('STOR '+fileaddres, open(fileaddres, 'rb'))
      ftp.quit()
      print "file : " + fileaddres + "  uploaded to " + HOST
      return "0"
  except:
      print "==========>>>>> ERROR ftp conntion refused <<<<<========"
      print "\n------------------------------------------------"

def fn(HOST, USER, PASS, command):
  client1=paramiko.SSHClient()
  #Add missing client key
  client1.set_missing_host_key_policy(paramiko.AutoAddPolicy())
  #connect to switch
  try:
    client1.connect(HOST,username=USER,password=PASS)
    print "SSH connection to %s established" %HOST
    #Gather commands and read the output from stdout
    stdin, stdout, stderr = client1.exec_command(command)
    out = stdout.read()
    return out
    client1.close()
  except:
    return "es"

def chek(out):
  if out == "es":
    return "es"
  elif "mipsbe" in out:
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
    return "en"

  print "mikrotik architecutre-name : " + aname
  return filefund(aname)

def filefund(aname):
  os.chdir("file")
  for file in glob.glob("*.npk"):
    if file.split("-")[1] == aname:
      return file
    else:
      return "ef"


f = open('ip.txt','r')
message = f.read()
mel=message.split("\n")
count = len(mel)
for x in xrange(count):
  try:
    mela = mel[x].split('/')
    HOST = str(mela[0])
    USER = str(mela[1])
    PASS = str(mela[2])
    
    print " \n++++++++++++++"+ HOST + "++++++++++++++\n"
    fileaddres = chek(fn(HOST, USER, PASS, '/system resource print\n'))
    if fileaddres == "es":
      print "==========>>>>> ERROR ssh to %s <<<<<==========" % HOST
      print "\n------------------------------------------------"
    elif fileaddres == "en":
      print "==========>>>>> ERROR architecutre not find <<<<<========="
      print "\n------------------------------------------------"
    elif fileaddres == "ef":
      print "==========>>>>> ERROR file for %s not find <<<<<=========" % HOST
      print "\n------------------------------------------------"
    else:
      ftp = upload(HOST, USER, PASS, fileaddres)
      if ftp == "0":
        # fn(HOST, USER, PASS, '/system reboot \n')
        os.chdir("..")
        print "%s Rebooted for Update" % HOST
        print "**Complated**"
        print "\n------------------------------------------------"
  except:
     print "error in : " + HOST
f.close()

