#!/usr/bin/python
#makesutre u use
#sudo apt-get install python-daemon
import time,sys
import datetime
#import LogDump
import configReader
from novaclient import client
import novaclient.exceptions
from daemon import runner


class App():
    def __init__(self):
        self.stdin_path = '/dev/null'
        self.stdout_path = '/dev/tty'
        self.stderr_path = '/dev/tty'
        self.pidfile_path =  '/tmp/foo.pid'
        self.pidfile_timeout = 5
        self.vmCreated={}

        #logDict = configReader.readConfigFile("logdetails")
        #LOG_FILENAME = logDict['deamonlog']
        
        #take the filename of info from key.conf
        deamDict = configReader.readConfigFile("key.conf","infod")
        self.paramDict = configReader.readConfigFile(deamDict["file"],deamDict["package"])
        print self.paramDict
        try :
       		authDict = configReader.readConfigFile("key.conf","KeystoneAuth")
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
		print "Please check the key.conf file for "+ deamDict["file"] + " and "+ deamDict["package"] +"section for osname or flavor. Terminating deamon..."
        	#print paramDict
		sys.exit(1)

	try :
		self.hourInput = int(self.paramDict['start-hour']);
		if self.hourInput > 23:
			print "hours should less than 23. Terminating Deamon..."
			sys.exit(1)

		self.minuteInput = int(self.paramDict['start-minute']);
		if self.minuteInput > 59:
			print "minutes should less than 60. Terminating Deamon..."
			sys.exit(1)

		self.intsanceCount = int(self.paramDict['intsancecount']);
		if self.intsanceCount > 35 | self.intsanceCount < 1:
			print "Instance count should less than 35. Terminating Deamon..."
			sys.exit(1)

	except : 
		print "please enter hour and minute in integers. Terminating Deamon..."
		sys.exit(1)
	try : 	#validation needed
		self.vmname = self.paramDict['vmname'];
		if len(self.vmname) == 0:
			self.vmname = deamDict["package"]
			print "vmname is explicitly empty. taking section name by default : "+self.vmname
	except : 
		print "vmname not found. Terminating Deamon..."
		sys.exit(1)

    def todayAt(self,hr,mins=0,sec=0,microsec=0):
    	now = datetime.datetime.now()
    	return now.replace(hour=hr,minute=mins,second=sec,microsecond=microsec)

    def maskNow(self):
    	now = datetime.datetime.now()
    	return now.replace(second=0,microsecond=0)

    def run(self):
	print("deamon loop started. waiting for time")
	now = self.maskNow()
	startTime = self.todayAt(self.hourInput,self.minuteInput)

	#wait for the time given
	while self.maskNow() < startTime :
		print "now : "+str(now)
		print "now : "+str(startTime)
		time.sleep(10)

	#time elapsed start n VM's now
	try:
		for i in range(0,self.intsanceCount):
			vm=self.nova.servers.create(name=self.vmname+str(i),image=self.image,flavor=self.flavor)
			print "creating VM named : "+self.vmname+str(i)
			if vm.status == "BUILD" :
				#print vm.networks['private'][0]
				print "ID : "+ vm.id
				print "Build Success !!"
				self.vmCreated[self.vmname+str(i)] = vm.id
				#LogDump.dumpLog("createvm : "+self.vmname+str(i)+"ID : "+ vm.id+ "Build Success !!")
			else:
				print self.vmname+str(i) + " : Buid Failed .. "
				#LogDump.dumpLog("createvm : "+self.vmname+str(i)+ " Buid Failed ..")

		print "demon creation sucess"
	except : 
		print "some error while creating... deamon terminating itself"
		sys.exit(1);

	def __del__(self):
		print "desctructor called"
app = App()
daemon_runner = runner.DaemonRunner(app)
daemon_runner.do_action()

#Then just start it with ./howdy.py start, and stop it with ./howdy.py stop.
