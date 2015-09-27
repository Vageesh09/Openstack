#!/usr/bin/env python
#http://www.jejik.com/articles/2007/02/a_simple_unix_linux_daemon_in_python/
import time, sys
import datetime
import logging
import configReader
from novaclient import client
#import novaclient.exceptions
from deamon import Daemon
 
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

	def InitializeDeamon(self):
		self.vmCreated={}
		#take the filename to create log
		logDict = configReader.readConfigFile("key.conf", "logdetails")
		self.LOG_FILENAME = logDict['deamonlog']
		#test the write
		self.dumplogd("createvm :  called initialization")

		deamDict = configReader.readConfigFile("key.conf", "infod")
		self.paramDict = configReader.readConfigFile(deamDict["file"],deamDict["package"])
		print self.paramDict
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

		try : # boundry checking and type checking
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
		try : 	#validation needed
			self.vmname = self.paramDict['vmname'];
			if len(self.vmname) == 0:
				self.vmname = deamDict["package"]
				print "vmname is explicitly empty. taking section name by default : " + self.vmname
		except : 
			print "vmname not found. Terminating Deamon..."
			sys.exit(1)

		self.dumplogd("createvmd : end of initialization ")
		pass

        def run(self):
       		self.dumplogd("createvmd : is now demonized ")
		startTime = self.todayAt(self.startHour,self.startMinute)
		endTime = self.todayAt(self.endHour,self.endMinute)

		#wait for the time given
		while self.maskNow() < startTime :
			time.sleep(10)

		#time elapsed start n VM's now
		try:
			for i in range(0,self.intsanceCount):
				vm=self.nova.servers.create(name=self.vmname+str(i),image=self.image,flavor=self.flavor)
				if vm.status == "BUILD" :
					#print vm.networks['private'][0]
					self.vmCreated[self.vmname+str(i)] = vm.id
					self.dumplogd("createvmd : "+self.vmname+str(i)+"ID : "+ vm.id+ " Build Success !!")
				else:	
					self.vmCreated[self.vmname+str(i)] = vm.id
					self.dumplogd("createvmd : "+self.vmname+str(i)+ " Buid Failed ..")
		except : 
			self.dumplogd("createvmd : some error while creating... deamon terminating itself")

		self.dumplogd("createvmd : dictionary - "+ str(self.vmCreated));
			#sys.exit(1);
		
		# wait till end point
                while self.maskNow() >= endTime:
			time.sleep(10)
			
			
		for instanceName, instanceId in self.vmCreated :
			sever = nova.servers.find(id=instanceId);
		
		# now end time is crossed tome to delete created vms
		
		

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
