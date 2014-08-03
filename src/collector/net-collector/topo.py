#!/usr/bin/python

import os, sys

CMD = "./snmpwalk -v 2c -c public"

SYS_DESCR = "SNMPv2-MIB::sysDescr.0"

IF_DESCR = "IF-MIB::ifDescr"
IF_MAC = "IF-MIB::ifPhysAddress"
IF_STATUS = "IF-MIB::ifOperStatus"

LLDP_REMOTE = "1.0.8802.1.1.2.1.4.1.1"
LLDP_NEIGHBOR = "iso.0.8802.1.1.2.1.4.1.1.9.0"
LLDP_IF = "iso.0.8802.1.1.2.1.4.1.1.8.0"
LLDP_MAC = "iso.0.8802.1.1.2.1.4.1.1.5.0"
ARP = "ipNetToPhysicalPhysAddress"

IP_ROUTE_TABLE = "IP-MIB::ipAddrTable"
IP_ROUTE_DST = "IP-MIB::ipAdEntAddr"
IP_ROUTE_MASK = "IP-MIB::ipAdEntNetMask"
IP_ROUTE_NEXTHOP = "IP-MIB::ipAdEntIfIndex"

class Interface:
	def __init__(self, name, mac, home_switch):
		self.name = name
		self.mac = mac
		self.home_switch = home_switch
		self.other_side = None

	def connect(self, intf):
		if self.other_side != None:
			print "[Warning] interface has more than one connections"
		self.other_side = intf

class Switch:
	def __init__(self, topo, hostname, address):
		self.topo = topo
		self.hostname = hostname
		self.address = address
		self.interfaces = {}
		self.intf_indexes = {}
		self.neighbors = []
		self.servers = []
		self.routes = []
		self.sys_descr = ""

	def getSysDescr(self):
		fr = os.popen(CMD + " " + self.address + " " + SYS_DESCR)
		data = fr.read()
		try:
			self.sys_descr = data.split("\n")[0].split(" = ")[1].split(": ")[1]
		except:
			self.sys_descr = "NA"

	def addInterface(self, intf_name, intf_mac):
		if self.interfaces.has_key(intf_name):
			return
		intf = Interface(intf_name, intf_mac, self.hostname)
		self.interfaces[intf_name] = intf

	def getInterface(self, intf_name):
		if self.interfaces.has_key(intf_name):
			return self.interfaces[intf_name]
		else:
			return None

	def walkIntfMIB(self, oid):
		fr = os.popen(CMD + " " + self.address + " " + oid)
		data = fr.read();
		fr.close()
		result = {}
		for line in data.split("\n"):
			if not line:
				continue
			items = line.split(" = ")
			key = items[0].split(".")[1]
			val = items[1].split(": ")[1]
			result[key] = val
		return result

	def walkLLDPMIB(self, oid):
		fr = os.popen(CMD + " " + self.address + " " + oid)
		data = fr.read();
		fr.close()
		result = {}
		for line in data.split("\n"):
			if not line:
				continue
			items = line.split(" = ")
			key = items[0].split(".")[-2]
			if items[1].find(":") < 0:
				result[key] = "Unknown"
			else:
				t, val = items[1].split(": ")
				if t == "STRING":
					result[key] = val.split("\"")[1]
				else:
					result[key] = val.split(" ")[0]
					for part in val.split(" ")[1:-1]:
						result[key] += ":" + part
					result[key] = result[key].lower()
		return result

	def walkRoutingTableMIB(self, oid):
		fr = os.popen(CMD + " " + self.address + " " + oid)
		data = fr.read();
		fr.close()
		result = {}
		for line in data.split("\n"):
			if not line:
				continue
			items = line.split(" = ")
			first_parts = items[0].split(".")
			key = first_parts[-4] + "." + first_parts[-3] + "." + first_parts[-2] + "." + first_parts[-1]
			result[key] = items[1].split(": ")[1]
		return result


	def getInterfaces(self):
		intf_num_name = self.walkIntfMIB(IF_DESCR)
		intf_num_mac = self.walkIntfMIB(IF_MAC)
		for num in intf_num_name.keys():
			self.addInterface(intf_num_name[num], intf_num_mac[num])
			self.intf_indexes[num] = intf_num_name[num]

	def getNeighbors(self):
		neighbors = self.walkLLDPMIB(LLDP_NEIGHBOR)
		interfaces = self.walkLLDPMIB(LLDP_IF)
		mac_addresses = self.walkLLDPMIB(LLDP_MAC)
		for key in neighbors.keys():
			hostname = neighbors[key]
			intf = interfaces[key]
			mac = mac_addresses[key]
			switch = self.topo.getSwitch(hostname, hostname)
			switch.addInterface(intf, mac)

			# connecting switches
			self.neighbors.append(hostname)
			switch.neighbors.append(self.hostname)

			# connecting interfaces
			local_intf = self.getInterface(self.intf_indexes[key])
			remote_intf = switch.getInterface(intf)
			local_intf.connect(remote_intf)
			#remote_intf.connect(local_intf)
	
	def getServers(self):
		fr = os.popen(CMD + " " + self.address + " " + ARP)
		data = fr.read()
		for line in data.split("\n")[0:-1]:
			self.servers.append(line.split("\"")[1])

	def getRoutingTable(self):
		dst = self.walkRoutingTableMIB(IP_ROUTE_DST)
		mask = self.walkRoutingTableMIB(IP_ROUTE_MASK)
		nexthop = self.walkRoutingTableMIB(IP_ROUTE_NEXTHOP)
		for key in dst.keys():
			self.routes.append(dst[key] + "/" + mask[key] + "-->" + self.intf_indexes[nexthop[key]])

	def printConnections(self):
		print "Switch Hostname: ", self.hostname
		print "System Descr: ", self.sys_descr
		for intf_name in self.interfaces.keys():
			interface = self.interfaces[intf_name]
			if interface.other_side != None:
				print "\t %s(%s) <--> %s(%s) @ %s" % (interface.name, interface.mac, interface.other_side.name, interface.other_side.mac, interface.other_side.home_switch)	
		print "Server Pool"
		for server in self.servers:
			print "\t ", server
		print "Routing Table"
		for route in self.routes:
			print "\t ", route
		print "---------------------------------------"

class Topology:
	def __init__(self):
		self.switches = {}
		self.servers = {}

	def getSwitch(self, hostname, address):
		if self.switches.has_key(hostname):
			return self.switches[hostname]
		else:
			switch = Switch(self, hostname, address)
			self.switches[hostname] = switch
			return self.switches[hostname]

	def construct(self, switch_list):
		visited = []
		to_visit = []
		for s in switch_list:
			to_visit.append(s)	
		while len(to_visit) != 0:
			s_hostname = to_visit.pop()
			switch = self.getSwitch(s_hostname, s_hostname)
			switch.getInterfaces()
			switch.getNeighbors()
			switch.getSysDescr()
			#switch.getServers()
			#switch.getRoutingTable()
			visited.append(switch.hostname)
			for hostname in switch.neighbors:
				if hostname in visited:
					continue
				to_visit.append(hostname)

	def drawToFile(self, filename):
		pass

	def writeToXML(self, filename):
		fw = open(filename, "w")
		fw.write("<?xml version=\"1.0\"?>\n")
		fw.write("<topo>\n")
		id = 1
		for hostname in self.switches.keys():
			fw.write("\t<Node id=\"%d\" ip=\"%s\" type=\"%s\"/>\n" % (id, self.switches[hostname].address, self.switches[hostname].sys_descr))
			id += 1

		links = {}
		for src in self.switches.keys():
			for nb in self.switches[src].neighbors:
				if src >= nb:
					continue
				if links.has_key(src) and links[src].has_key(nb):
					continue
				if not links.has_key(src):
					links[src] = {}
				links[src][nb] = 1
				fw.write("\t<Link src=\"%s\" dst=\"%s\">\n" % (src, nb))

		fw.write("</topo>\n")
		fw.close()

	def printTopo(self):
		for switch in self.switches.values():
			switch.printConnections()
		
if __name__ == "__main__":
	topo = Topology()
	topo.construct(["10.0.0.1"])
	#topo.printTopo()
	topo.writeToXML("simple.xml")
