import sys, getopt
import configReader
import LogDump
from novaclient import client
import novaclient.exceptions
import pandas as pd

def getVncUrl(argv):
	write_file_name = "filename.csv";
	LogDump.dumpLog("getVncUrl :  called...")
	
	authDict = {}
	KEY_FILE = "key.conf"
	urlDict={}
	# get the options from cammand line
	try:
		opts, args = getopt.getopt(argv, "h", ["help"])
	except getopt.GetoptError:
		print 'getVncUrl : will create a xls file which shows vnc console url for each instances'
		LogDump.dumpLog("getVncUrl : option exception throwed") 
		return 0
	
	
	# iterate the otion object and get each option and its value
	for opt,arg in opts:
		if opt in ("-h","--help","help") :
			print 'getVncUrl : will create a xls file which shows vnc console url for each instances'
			LogDump.dumpLog("getVncUrl : asked help ")
			return 0
		
	authDict = configReader.readConfigFile(KEY_FILE,"KeystoneAuth")
	#get the nova object
	nova=client.Client(authDict['versionnumber'], authDict['username'], authDict['password'], authDict['tennantname'], authDict['authurl'])
	instance = nova.servers.list()
	target = open(write_file_name, 'w')
	target.write("VM_NAME, STATUS , CONSOLE_URL\n");
	for each in instance:
		print each.get_vnc_console('novnc')['console']['url']
		target.write(each.name+","+each.status+","+each.get_vnc_console('novnc')['console']['url']+"\n")
	target.close()
		
	return 0

if __name__ == "__main__":
    getVncUrl(sys.argv[1:])
