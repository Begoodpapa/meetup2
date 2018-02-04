import os, subprocess, datetime, signal, time, threading
from random import choice

cat_mac_tbl  = ' "cat /proc/dmxmsg/mac_addr_tbl | grep local | awk \'{print \$(NF-1)}\'"'

def TIMEOUT_COMMAND(command, timeout):
    """call shell-command and either return its output or kill it
    if it doesn't normally exit within timeout seconds and return None"""
    cmd     = command.split(" ")
    start   = datetime.datetime.now()
    process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    while process.poll() is None:
        time.sleep(0.2)
        now = datetime.datetime.now()
        if (now - start).seconds> timeout:
            os.kill(process.pid, signal.SIGKILL)
            os.waitpid(-1, os.WNOHANG)
            return None
    return process.stdout.readlines()

class node:
	""" A node is an addin card in BCN
    Attributes:
        box 	: 	The addin card id, eg CFPU-0 locates on the first box, box=0
        name 	: 	'EIPU-0', 'CFPU-0' ...
        wind 	: 	If there are 6wind modules embeded, wind=1, else, wind=0
        has_se 	: 	If there is a IL SE running on the addin card, has_se=1, else has_se=0
    """
	def __init__(self, node_name, addin_card):
		"""For each node, has member: box id, node name, is_wind, is_has_se, stub pids for in linux and se"""
		self.box  = int(addin_card.split('-')[1])
		self.name = node_name
		self.has_wind()
		self.has_se()
		self.set_stub()
	def has_wind(self):
		"""EIPU and CFPU nodes have 6wind modules"""
		if((self.name.split('-')[0] == 'EIPU') or (self.name.split('-')[0] == 'CFPU')):
			self.wind = 1
		else:
			self.wind = 0 
	def has_se(self):
		"""Except for CFPU node, all other nodes has both linux and se"""
		if(self.name.split('-')[0] != 'CFPU'):
			self.has_se = 1;
		else:
			self.has_se = 0;
	def set_stub(self):
		cmd = 'ssh -o StrictHostKeyChecking=no ' + self.name + cat_mac_tbl
		f = os.popen(cmd)
		self.linux_pid = '1' + f.readline().strip()[-2:] +':ad9c:0'
		if(self.has_se == 1):
			self.se_pid    = f.readline().strip() + ':450:0'
        
class Cluster:
	""" A cluster compsed of several boxes, each box contains several addin_card, they can be 
	grouped in 6wind nodes, no6wind nodes, boxes
	Attributes:
		node_count 	:	How many nodes are in the cluster
		nodes 		: 	A list to chain all nodes in the cluster
		box 		: 	A dic grouped nodes into different boxes, box id starts from 0
		wind 		: 	A list to chain all 6wind nodes
		nwnd 		: 	A list to chain all no 6wind nodes
	"""
	def __init__(self):
		"""Collecting and store the cluster information"""
		self.node_count = 0
		self.nodes 	    = []
		self.box 		= {} 
		self.wind 		= []
		self.nwnd 		= []
		self.probe()
		self.setup()
	def probe(self):
		print 'Dectecing the cluster env'
		f = os.popen("hwcli -o off | egrep 'CFPU|EIPU|CSPU|USPU'")
		for line in f.readlines():
			name  = line.strip().split(':')[0].strip()
			card = line.strip().split(':')[1].split('/')[2].strip()
			self.node_count += 1
			self.nodes.append(node(name, card))
	def setup(self):
		for i in range(self.node_count/8):
			self.box[i] = [] 
		for node in self.nodes:
			self.box[node.box - 1].append(node)
			if(node.wind == 0):
				self.nwnd.append(node)
			else:
				self.wind.append(node)
	def select_node_by_type(self, node_type):
		if(node_type == '6wind'):
			return choice(self.wind)
		else:
			return choice(self.nwnd)
	def find_node_by_name(self, name):
		for node in self.nodes:
			if(node.name == name):
				return node

class Tester:
	""" Run test cases and summaries test results
	Attributes:
		cluster 	:	The cluster, should be a instance of class Cluster
		failed 		:	Totally failed cases during the testing.
		successed	:	Totally successed cases during the testing
		failed_cmd	:	A list of all failed commands
	"""
	def __init__(self, cluster):
		self.cluster    = cluster
		self.failed     = 0
		self.successed  = 0
		self.failed_cmd = []
	def run_cmd_set(self, cmdset):
		"""A warpper to run all the commands listed in the cmd set, 
		if a command failed or didn't finish for 5 seconds, it will 
		be considered as failed. A result 'OK' or 'FAILED' returned
		"""
		result = 'OK'
		for command in cmdset:
			if TIMEOUT_COMMAND(command, 5):
				self.successed += 1
			else:
				self.failed += 1
				self.failed_cmd.append(command)
				result = 'FAILED'
		return result
	def intra_node(self, node):
		"""one round of test intra a given node, covers following cases:
			1. linux-linux
			2. linux-se
		all case include a sending and a receiving.
		"""
		cmd = []
		command = 'dmxcli -s %s -r %s -m 1 | grep successful'
		cmd.append(command % (node.linux_pid, node.linux_pid))
		if(node.has_se == 1):
			cmd.append(command % (node.se_pid, node.linux_pid))
		result = self.run_cmd_set(cmd)
		print '\t%s\t\t<=========>\t%s\t\t\t[%s]' % (node.name, node.name, result)
	def inter_node(self, sender, receiver):
		"""one round of test inter two node, covers following cases: 
			1. linux-linux; 
			2. linux-se; 
			3. se-linux; 
			4. se-se
		all case include a sending and a receiving.
		"""
		cmd = []
		command = 'dmxcli -s %s -r %s -m 1 | grep successful'
		cmd.append(command % (sender.linux_pid, receiver.linux_pid))
		if(sender.has_se == 1):
			cmd.append(command % (sender.se_pid, receiver.linux_pid))
			if(receiver.has_se == 1):
				cmd.append(command % (sender.se_pid, receiver.se_pid))
		if(receiver.has_se == 1):
			cmd.append(command % (sender.linux_pid, receiver.se_pid))
		result = self.run_cmd_set(cmd)
		print '\t%s\t\t<=========>\t%s\t\t\t[%s]' % (receiver.name, sender.name, result)
	def run_with_all_other_nodes(self, sender):
		"""A set of tests between node self and all other nodes int the cluster """
		for node in self.cluster.nodes:
			if(node.name != sender.name):
				self.inter_node(node, sender)
	def report(self):
		"""Summaries the current test result"""
		print 'Case finish, totally %d case ran, successed %d, failed %s' % (self.successed + self.failed, self.successed, self.failed)
		if(self.failed):
			print 'Failed cases:\n'
			for i in self.failed_cmd:
				print i
			print 'Run the failed case again: %s' % self.run_cmd_set(self.failed_cmd)


def full_cover_test():
	cluster = Cluster()
	test    = Tester(cluster)
	print '\nSet 1 : CFPU node could send/receive dmxmsg message with all other nodes'
	test.run_with_all_other_nodes(cluster.find_node_by_name('CFPU-0'))
	if cluster.find_node_by_name('CFPU-1'):
		test.run_with_all_other_nodes(cluster.find_node_by_name('CFPU-1'))

	print '\nSet 2 : Intra node dmxmsg should work'
	test.intra_node(cluster.select_node_by_type('6wind'))
	test.intra_node(cluster.select_node_by_type('no6wind'))

	print '\nSet 3 : Any 6wind node could send/receive dmxmsg with other nodes in the cluster'
	test.run_with_all_other_nodes(cluster.select_node_by_type('6wind'))

	print '\nSet 4 : Any no6wind node could send/receive dmxmsg message with all other nodes'
	test.run_with_all_other_nodes(cluster.select_node_by_type('no6wind'))

	print '\n Test Done'	
	test.report()

if __name__ == '__main__':
	full_cover_test()
