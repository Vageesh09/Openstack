

import sys, getopt
import configReader
import LogDump
from novaclient import client
import novaclient.exceptions

class status:

	def __init__(self):
		authDict = {}
		KEY_FILE = "key.conf"
		try:
			authDict = configReader.readConfigFile(KEY_FILE,"KeystoneAuth")
			self.nova=client.Client(authDict['versionnumber'], authDict['username'], authDict['password'], authDict['tennantname'], authDict['authurl'])
			print "initialized nova object "
		except:
			print "ERROR Occured while initializing nova object"
	
	def getStatus(self):

		statusDict={}
		statusDict['error'] = "GOOD"
		
		try:
			
			instance = self.nova.servers.list()
			names=[]
			statuses=[]
			console_url=[]

			count=0
			for each in instance:
				names.append(str(each.name));
				statuses.append(str(each.status));
				if statuses[count] == "ACTIVE":
					console_url.append(str(each.get_vnc_console('novnc')['console']['url']));
				else :
					console_url.append("");
				count=count+1;

			statusDict["count"] = count;
			statusDict["names"] = names;
			statusDict["status"] = statuses;
			statusDict["url"] = console_url;

		except :
			statusDict['error']="error"

		print statusDict
		return str(statusDict);

if __name__ == '__main__':
	x=status()
	x.getStatus();