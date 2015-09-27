#!/usr/bin/env python

import time, sys
import datetime
import logging

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from novaclient import client
#import novaclient.exceptions
from deamon import Daemon

import configReader
 
class CreateVmd(Daemon):
	
	#method to write to log file
	def dumplogd(self, logString):
		logging.basicConfig( filename = self.LOG_FILENAME, level = logging.DEBUG )
		logging.debug( str( datetime.datetime.now()) + " " + logString )
		return 0;

	#method to get the time
	def todayAt(self, hr, mins=0, sec=0, microsec=0 ):
		now = datetime.datetime.now()
		return now.replace( hour = hr, minute = mins, second = sec, microsecond = microsec)
	# method to mask the now time seconds and microsecond 
	def maskNow(self):
		now = datetime.datetime.now()
		return now.replace(second = 0, microsecond = 0)
	
	#sendmail module to send the notification of events
	def sendmail(self,content):
		#check if flag , before sending email
		if self.mailFlag :
			msg = MIMEMultipart('alternative')
			me = self.mailFrom
			you = self.paramDict['sendto']
			msg['Subject'] = "Createvm Deamon Notification"
			msg['From'] = me
			msg['To'] = you
			text = "Hi!"
			html = """\
			<html>
			  <head></head>
			  <body>
			    <p>Hi!<br>
			       """+content+"""
			    </p>
			  </body>
			</html>
			"""
			part1 = MIMEText(text, 'plain')
			part2 = MIMEText(html, 'html')
			msg.attach(part1)
			msg.attach(part2)

			mail = smtplib.SMTP('smtp.gmail.com', 587)	#hardcoded...
			mail.ehlo()
			mail.starttls()
			mail.login(me, self.mailPass)
			mail.sendmail(me, you, msg.as_string())
			mail.quit()

		pass
	def InitializeDeamon(self):

		self.vmCreated={}	#holds the key/value pair of vm created
		self.mailFlag=False
		self.mailFrom = ""
		self.mailPass = ""
		#bellow cade will not be demonized

		#take the filename to create log
		logDict = configReader.readConfigFile("key.conf", "logdetails")
		self.LOG_FILENAME = logDict['deamonlog']

		#dump status log
		self.dumplogd("createvm :  called initialization")
		
		#get file from key file
		deamDict = configReader.readConfigFile("key.conf", "infod")
		
		#retrieve the initialization details
		self.paramDict = configReader.readConfigFile(deamDict["file"],deamDict["package"])
		
		#print self.paramDict # this will print in terminal
		#check each pareameter and validate
		try :
	       		authDict = configReader.readConfigFile("key.conf", "KeystoneAuth")
			#get the nova object
			self.nova=client.Client(authDict['versionnumber'],authDict['username'],authDict['password'],authDict['tennantname'],authDict['authurl'])
		except :
			print "Authentication failure, please check the credentials. Terminating Deamon..."
			sys.exit(1)

		try : 
			self.image=self.nova.images.find(name=self.paramDict['osname'])
			#find te flavor
			self.flavor=self.nova.flavors.find(name=self.paramDict['flavorname'])
		except:
			print "Please check the key.conf file for " + deamDict["file"] + " and " + deamDict["package"] + "section for osname or flavor. Terminating deamon..."
			#print paramDict
			sys.exit(1)

		try : # boundry checking and type checking for hour minute and instance count
			self.startHour = int(self.paramDict['start-hour']);
			if self.startHour > 23 | self.startHour < 0 :
				print "hours should less than 23. Terminating Deamon..."
				sys.exit(1)

			self.startMinute = int(self.paramDict['start-minute']);
			if self.startMinute > 59 | self.startMinute < 0 :
				print "minutes should less than 60. Terminating Deamon..."
				sys.exit(1)

			self.endHour = int(self.paramDict['end-hour']);
			if self.endHour > 23 | self.endHour < 0 :
				print "hour should less than 23. Terminating Deamon..."
				sys.exit(1)

			self.endMinute = int(self.paramDict['end-minute']);
			if self.endMinute > 59 | self.endMinute < 0:
				print "minutes should less than 60. Terminating Deamon..."
				sys.exit(1)

			self.intsanceCount = int(self.paramDict['intsancecount']);
			if self.intsanceCount > 35 | self.intsanceCount < 1:
				print "Instance count should less than 35. Terminating Deamon..."
				sys.exit(1)

		except : 
			print "please enter hour, minute, intsace count in integer in integers. Terminating Deamon..."
			sys.exit(1)
			
		try : 
			if len(self.paramDict['sendto']) > 4 :
				self.mailFlag = True
				self.mailFrom = authDict['mailid']
				self.mailPass = authDict['mailpas']
		except :
		 	self.mailFlag=False
		 	print "error here "
		 	print self.paramDict['sendto']
		 	print len(self.paramDict['sendto'])
		 	print authDict['mailid']
		 	print authDict['mailpas']
		 	
			
			
		try : 	#validation needed
			self.vmname = self.paramDict['vmname'];
			if len(self.vmname) == 0:
				self.vmname = deamDict["package"]
				print "vmname is explicitly empty. taking section name by default : " + self.vmname
		except : 
			print "vmname not found. Terminating Deamon..."
			sys.exit(1)
		
		self.dumplogd("createvmd : end of initialization ")
		print "Deamon Initialized and running."
		print "Check "+self.LOG_FILENAME+" for loges dumped by deamon "
		print "to stop use: %s stop|restart" % sys.argv[0]
		pass

        def run(self):
        	#bellow code is run as deamon. use self to adress the class properties
       		self.dumplogd("createvmd : is now demonized ")
		
		#time to start and delete VMs
		startTime = self.todayAt(self.startHour,self.startMinute)
		endTime = self.todayAt(self.endHour,self.endMinute)

		#wait for the time given
		#while (1):
		#while self.maskNow() != startTime :
		while self.maskNow() < startTime :
			time.sleep(10)

		#time elapsed start n VM's now
		try:
			for i in range(0,self.intsanceCount):

				vm=self.nova.servers.create(name=self.vmname+str(i),image=self.image,flavor=self.flavor)

				if vm.status == "BUILD" :
					#print vm.networks['private'][0]
					self.vmCreated[self.vmname+str(i)] = vm.id
					self.dumplogd("createvmd : "+self.vmname+str(i)+" ID : "+ vm.id+ " Build Success !!")
				else:	
					self.vmCreated[self.vmname+str(i)] = vm.id
					self.dumplogd("createvmd : "+self.vmname+str(i)+ " Buid Failed ..")
		except : 
			self.dumplogd("createvmd : some error while creating... deamon terminating itself")

		#dump status logs
		self.sendmail(self.paramDict['intsancecount']+" Virtual machine has been created <br/>status : "+ str(self.vmCreated))
		self.dumplogd("createvmd : dictionary - "+ str(self.vmCreated))
		self.dumplogd("createvmd : waiting for end time ")

		# wait till end point
		#while self.maskNow() != endTime:
        	while self.maskNow() <= endTime:
			time.sleep(10)

		# now end time is crossed; time to delete created vms
		self.dumplogd("createvmd : started deleting vms")
		for instanceName in self.vmCreated.keys():
			#server = self.nova.servers.find(id=self.vmCreated[instanceName])
			server = self.nova.servers.find(name=instanceName)
			server.delete();
			self.dumplogd("createvmd : deleted - "+ instanceName + " status : "+server.status)
		self.sendmail(self.paramDict['intsancecount']+" Virtual machine has been deleted  <br/> series name : "+self.vmname)

if __name__ == "__main__":
        daemon = CreateVmd('/tmp/daemon-createvm.pid')
        if len(sys.argv) == 2:
                if 'start' == sys.argv[1]:
                        daemon.start()
                elif 'stop' == sys.argv[1]:
                        daemon.stop()
                elif 'restart' == sys.argv[1]:
                        daemon.restart()
                else:
                        print "Unknown command"
                        sys.exit(2)
                sys.exit(0)
        else:
                print "usage: %s start|stop|restart" % sys.argv[0]
                sys.exit(2)
