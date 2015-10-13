import sys, getopt
import configReader
import LogDump
from novaclient import client
import novaclient.exceptions

class Status
	def getStatus(self):
		
		authDict = {}
		KEY_FILE = "key.conf"
		statusDict={}
		statusDict['error'] = "NULL"
		
		try:
			authDict = configReader.readConfigFile(KEY_FILE,"KeystoneAuth")
			#get the nova object
			nova=client.Client(authDict['versionnumber'], authDict['username'], authDict['password'], authDict['tennantname'], authDict['authurl'])
			instance = nova.servers.list()
			statusDict["count"] = instance.length();
			for each in instance:
				statusDict["count"] = 
				print each.get_vnc_console('novnc')['console']['url']


		expect :
			statusDict['error']="error"
		
		return statusDict;
