import os
import sys
import time
from novaclient import client
import novaclient.exceptions

Keystone_AuthUrl="http://controller:35357/v2.0"
Keystone_VersionNumber=2
Keystone_UserName="admin"
Keystone_Password="ADMIN_PASS"
Keystone_TennantName="admin"
ImageName="cirros-0.3.3-x86_64"
vm_id=["vm1","vm2"]

def create_vm(i):
	global vm_id
	image=nova.images.find(name=ImageName)
	flavor=nova.flavors.find(name="m1.tiny")
	name = vm_id[i]
	vm=nova.servers.create(name=name,image=image,flavor=flavor)
	print "creating " + vm_id[i] ;
	print "waiting for status ..." 
	if vm.status == "BUILD" :
		#print vm.networks['private'][0]
		
		print "ID : "+ vm.id
		print "Build Success !!"
	else:
		print name + " : Buid Failed .. "
	while vm.status == "BUILD":
		print vm.status
	print vm.networks

	return;

def delete_vm():
	global vm_id
	i=len(vm_id)-1
	name=vm_id[i]
	dvm = nova.servers.find(name=name)
	dvm.delete()
	del vm_id[i]

	return;


nova=client.Client(Keystone_VersionNumber,Keystone_UserName,Keystone_Password,Keystone_TennantName,Keystone_AuthUrl)
while 1 == 1 :
	print "Enter 1 for Creating virtual machines"
	print "Enter 2 for Deleting all the virtual machines"
	print "Enter 3 for Exiting the program"
	usr_input=input("please enter the input  ")
	if usr_input == 1:
		print "Enter the number of virtual machines to be created"
		num_of_vm=input("Please enter the input ")
		i=0
		while i != num_of_vm:
			create_vm(i)
			i+=1
		flag=0
	elif usr_input == 2:
		global vm_id
		while len(vm_id) != 0:
			delete_vm()
		flag=1
	elif usr_input == 3:
		if flag == 1:
			sys.exit()
		else :
			while len(vm_id) != 0 :
				delete_vm()
		sys.exit()
	else :
		print "I just told to Enter 1,2 or 3"

