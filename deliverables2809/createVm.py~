import sys, getopt
import configReader
import LogDump
from novaclient import client
import novaclient.exceptions

def createVm(argv):
	LogDump.dumpLog("createvm :  called...")
	
	osname = ""
	flavor = ""
	vmname = ""
	authDict = {}
	numberOfVms = 1
	vmCreated={}
	#vmCreated['createVmStat'] = 'error'
	# get the options from cammand line
	try:
		opts, args = getopt.getopt(argv, "ho:f:n:c:", ["help", "osname=", "flavor=", "vmname=","count="])
	except getopt.GetoptError:
		print 'please use the bellow syntax'
		print 'createVM.py -o <os_name> -f <flavour> -n <vm_name> -c <number_of_instance>'
		print 'createVM.py --osname=<os_name> --flavor=<flavour> --vmname=<vm_name> --count=<number_of_instance>'
		LogDump.dumpLog("createVm : option exception throwed") 
		return vmCreated
	
	if len(opts) < 3:
		print 'please use the bellow syntax'
		print 'createVM.py -o <os_name> -f <flavour> -n <vm_name> -c <number_of_instance>'
		print 'createVM.py --osname=<os_name> --flavor=<flavour> --vmname=<vm_name> --count=<number_of_instance>'
		LogDump.dumpLog("createVm : missed syntax")
		return vmCreated
	# iterate the otion object and get each option and its value
	for opt,arg in opts:
		if opt == '-h':
			print 'please use the bellow syntax'
			print 'createVM.py -o <os_name> -f <flavour> -n <vm_name> -c <number_of_instance>'
			print 'createVM.py --osname=<os_name> --flavor=<flavour> --vmname=<vm_name> --count=<number_of_instance>'
			LogDump.dumpLog("createVm : asked help ")
			return vmCreated
		elif opt in ("-o","--osname"):
			osname = arg
		elif opt in ("-f","--flavor"):
			flavor = arg
		elif opt in ("-n","--vmname"):
			vmname = arg
		elif opt in ("-c","--count"):
			try:			
				if int(arg) > 0 :
					numberOfVms = int(arg)
			except: 
				print 'please use the bellow syntax'
				print 'createVM.py -o <os_name> -f <flavour> -n <vm_name> -c <number_of_instance>'
				print 'createVM.py --osname=<os_name> --flavor=<flavour> --vmname=<vm_name> --count=<number_of_instance>'
				print '-c & --count arguement should be INTEGERS'
				LogDump.dumpLog("createVm : accepted arguements is iteger but ecieved string "+opt + " "+ arg)
				return vmCreated	
	
	authDict = configReader.readConfigFile("KeystoneAuth")
	#get the nova object
	nova=client.Client(authDict['versionnumber'],authDict['username'],authDict['password'],authDict['tennantname'],authDict['authurl'])
	# create a vm after getting the inputs
	#find the image object
	image=nova.images.find(name=osname)
	#find te flavor
	flavor=nova.flavors.find(name=flavor)
	#iterate --count/-c times to create --count/-c number of VMs ;each VM's name suffixed with i
	for i in range(0,numberOfVms):
		vm=nova.servers.create(name=vmname+str(i),image=image,flavor=flavor)
		print "creating VM named : "+vmname+str(i)
		if vm.status == "BUILD" :
			#print vm.networks['private'][0]
			print "ID : "+ vm.id
			print "Build Success !!"
			vmCreated[vmname+str(i)] = vm.id
			LogDump.dumpLog("createvm : "+vmname+str(i)+"ID : "+ vm.id+ "Build Success !!")
		else:
			print vmname+str(i) + " : Buid Failed .. "
			LogDump.dumpLog("createvm : "+vmname+str(i)+ " Buid Failed ..")

	# return the dictionary {('vmname':'ID')}
	return vmCreated

if __name__ == "__main__":
    createVm(sys.argv[1:])
