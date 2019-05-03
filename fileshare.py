#!/usr/bin/env python2

import sys  #for inline input
import subprocess  #for executing terminal command
import os  #for checking if selected item is file or directory and its path
import socket
import commands
import time
import cgi

def sender():
	#  we are looking for UDP (user datagram protocol )
	#              ip_version4,         UDP 
	s=socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
	# defining ip and port below 
	ip="192.168.43.108" 
	port=7890
	name = "samyak"
	#defining functions for windows and linux servers
	def linux():
		pwdraw = subprocess.check_output('pwd',shell=True) #fetching 'present working directory' path from terminal
		pwd = pwdraw[0:-1] #for removing \n from last of pwd path obtained

		while True :

			src_files=raw_input("\nEnter all files to be shared..  \n\n").split()
			for i in src_files :
				
				if os.path.isdir(i):  #checking if source is directory or not
					print "\nERROR: '"+i+"' is a directory , cannot copy a directory "
					exit()
				else:
					if os.path.exists(i) and '/' in i: #checking if specified full path name file exists 
						fsrc = open(i,'r')
						src_data = fsrc.read()
						fsrc.close()
						s.sendto(i,(ip,port))
						s.sendto(src_data,(ip,port))
						print "sending",i,"-->"

					elif os.path.exists(pwd+'/'+i): #checking if direct name file exists in pwd
						fsrc = open(pwd+'/'+i,'r')
						src_data = fsrc.read()
						fsrc.close()
						s.sendto(i,(ip,port))
						s.sendto(src_data,(ip,port))
						print "sending",i,"-->"

					else:
						print "\npycp: cannot stat '"+i+"': No such file or directory"
						exit()

	def windows():
		# defining list for 10 commands counter
		timer=[]
		while  True :
		#  sending  data to  target machine 
			cmd=raw_input("G:\projectpython\server-terminal-python> ")
			s.sendto(cmd,(ip,port))
			if  'exit' in  cmd  or  'close' in cmd:
					print "closing server.."
					exit()
			else :
					timer.append(cmd)
					if  len(timer) > 5 :
							subprocess.call('cls',shell=True)
							for i in  range(len(timer)):
									timer.pop()
					server_data=s.recvfrom(500)
					#   only  server  data is stored and printed
					recv_cmd=server_data[0]
					if "not recognized" in recv_cmd :
							print "\ncommand not found..\nmake sure you are connected to WINDOWS server\n"
					else:
							print "\n",recv_cmd,"\n"  
						   
	#authentication from server
	print "sending request to server........\n\n"
	time.sleep(2)
	s.sendto(name,(ip,port))
	msg = s.recvfrom(40)
	if msg[0] == 'ok' :
			Os = subprocess.check_output('nmap -O -V 192.168.1.37',shell=True)
			if 'windows' in Os:
					window()
			else:
					linux()
	else:
			print "\n",msg[0]
	s.close()

def receiver() :
		#  we are looking for UDP (user datagram protocol )
		#              ip_version4,         UDP 
		s=socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
		# defining ip and port below 
		# ip="192.168.1.37"
		port=7890
		#  binind ip and port with bind function that takes input as tuple
		s.bind(("",port))
		#  authenticating client
		user = s.recvfrom(10)
		print user
		choice = raw_input("Do you want to connect to above user (type y for yes and n for no :")
		if choice == 'y':
				s.sendto("ok",user[1])

				#  rec  data from  client 
				dst_files="/home/samyak/Documents/fileshare/"
				while True:
					filenameraw = s.recvfrom(20)
					filename = filenameraw[0]
					contentraw =s.recvfrom(5000)
					content = contentraw[0]
					fdst = open(dst_files+filename,'a')
					fdst.write(content)
					fdst.close()
					print "-->","receiving",filename
										
		else :
				s.sendto("cannot connect",user[1])
		s.close()


modeselect=raw_input("(type s) if you want to send or (type r) if you want receive: ")

if modeselect == 's':
	sender()
elif modeselect == 'r':
	receiver()
else :
	print "please select from r and s"

























