#!/usr/bin/python

from pyVim.connect import SmartConnect
from pyVmomi import vim
import ssl
import paramiko
import sys


def getChoice():
	print("\nMenu\n(CHECK-IN) New VM\n(CHECK-OUT) Used VM\n(CLEAN-UP) VM\n(Q)uit")
    	choose=raw_input(">>> ")
    	choice=choose.lower()
    	return choice


def connect_esx():
	s=ssl.SSLContext(ssl.PROTOCOL_TLSv1)
	s.verify_mode=ssl.CERT_NONE
	si= SmartConnect(host="192.16.10.10", user="Administrator@vsphere.local", pwd="xyz",sslContext=s)
	content=si.content
 
# Method that populates objects of type vimtype
	def get_all_objs(content, vimtype):
        	obj = {}
        	container = content.viewManager.CreateContainerView(content.rootFolder, vimtype, True)
        	for managed_object_ref in container.view:
                	obj.update({managed_object_ref: managed_object_ref.name})
        	return obj
 
#Calling above method
	connect_esx.getAllVms=get_all_objs(content, [vim.ClusterComputeResource])

def login_VM(VM_Ip,commmand):   
        try:
                ssh = paramiko.SSHClient()
                ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                ssh.connect(VM_Ip, port=22, username="admin", password="admin")
#Cleaning /tmp directory
                stdin, stdout, stderr = p.exec_command(command)
                login_VM.opt = stdout.readlines()
                login-VM.opt = "".join(opt)
                print(opt)
                
        except paramiko.AuthenticationException:
                print("Authentication failed when connecting to %s" % host_ip)
                sys.exit(1)
 
def new_VM():
#Iterating each cluster object and printing its name
	getAllVms=connect_esx.getAllVms
	for vm in getAllVms:
		if vm.runtime.powerState == vim.VirtualMachinePowerState.poweredOn:
        		new_VM.vm_name=vm.name
			new_VM.available_ip=vm.guest.ipAddress
			useable_vm=vm_name+:+available_ip
#Checking If the useable_vm has already an active ssh connection
			cmd="last -a | grep -i still | wc -l"
			login_VM(available_ip,cmd)
			if login_VM.opt == 0:		
				print "Ssh into the VM with IP:",useable_vm," using username and pswd as admin"
				sys.exit(0)
		else 	
			print ("No VMs are available to use now. Please try again later")
	

def main():
	
    	print "**\n ESXi Administration. Please Make Your Choice to Proceed** \n"

def cleanup():
	
	connect_ESX()
	new_VM()
        VM_To_Clean=new_VM.vm_name
	VM_Ip=new_VM.available_ip
	cmd="rm -rf /tmp/*"
#ssh to vm and execure cleanup command
	login_VM(VM_Ip,cmd)

#normal reset
	try:
    		VM_To_Clean.RebootGuest()
	except:
# forceably shutoff/on (need to do if vmware guestadditions isn't running)
    		VM_To_Clean.ResetVM_Task()
		print "Successful"


choice = getChoice()

while choice!="q" or choice!="Q":
    	if choice=="CHECK-IN":
		main()
		connect_ESX()
        	login_VM()
    	elif choice=="CHECK-OUT":
		main()
        	cleanup()
	elif choice=="Clean-Up":
                main()
                cleanup()
        
	else:
        	print("Invalid choice, please choose again")
        	print("\n")

	choice = getChoice()

print("Exiting Panel, Bye!!")

