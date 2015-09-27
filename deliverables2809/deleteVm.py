import sys, getopt
import configReader
import LogDump
from novaclient import client
import novaclient.exceptions

def deleteVm(argv):
	LogDump.dumpLog("deletevm :  called...")
	
	vmname = ""
	authDict = {}
	KEY_FILE = "key.conf"
	option = ""
	vmDeleted={}
	# get the options from cammand line
	try:
		opts, args = getopt.getopt(argv, "han:s:", ["help", "all", "name=", "series="])
	except getopt.GetoptError:
		print 'please use the bellow syntax'
		print 'deletevm.py -a -n <vm_name> -s <series_name>'
		print 'deletevm.py --all --name=<vm_name> --series=<series_name> '
		LogDump.dumpLog("deletevm : option exception throwed") 
		return 0
	
	if len(opts) < 1:
		print 'please use the bellow syntax'
		print 'deletevm.py -a -n <vm_name> -s <series_name>'
		print 'deletevm.py --all --name=<vm_name> --series=<series_name> '
		LogDump.dumpLog("deletevm : missed syntax")
		return 0
	# iterate the otion object and get each option and its value
	for opt,arg in opts:
		if opt in ("-h","--help","help") :
			print 'please use the bellow syntax'
			print 'deletevm.py -a -n <vm_name> -s <series_name>'
			print 'deletevm.py --all --name=<vm_name> --series=<series_name> '
			LogDump.dumpLog("deletevm : asked help ")
			return 0
		elif opt in ("-a","--all"):
			option = "all"
			break
		elif opt in ("-n","--name"):
			vmname = arg
			option = "specific"
			if 0 >= len(vmname):
				print "please enter the specific vm name"
				print 'deletevm.py -a -n <vm_name> -s <series_name>'
				print 'deletevm.py --all --name=<vm_name> --series=<series_name> '
				return 0
			break
		elif opt in ("-s","--series"):
			vmname = arg
			option = "series"
			if 0 >= len(vmname):
				print "please enter the vm series name excluding suffixed index"
				print 'deletevm.py -a -n <vm_name> -s <series_name>'
				print 'deletevm.py --all --name=<vm_name> --series=<series_name> '
				return 0
			break


	authDict = configReader.readConfigFile(KEY_FILE,"KeystoneAuth")
	#get the nova object
	nova=client.Client(authDict['versionnumber'], authDict['username'], authDict['password'], authDict['tennantname'], authDict['authurl'])

	if option == "specific" :
		try:
			instance = nova.servers.find(name=vmname)
			instance.delete()
		except: 
			print "no VM with the name %s" %vmname
			return 0
	if option == "all" :
		try:	
			instances = nova.servers.list()
			for instance in instances :
				instance.delete()
		except: 
			print "no VM present" 
			return 0
		
	if option == "series" :
		i = 0
		try:
			while (1):
				instance = nova.servers.find(name=vmname+str(i))
				instance.delete()
				i = i+1
				
		except :
			if i==0 :
				print "No series found with name "+vmname+str(i)
			else :
				print str(i)+" instance(s) deleted of series - "+vmname
			
	return 0

if __name__ == "__main__":
    deleteVm(sys.argv[1:])
