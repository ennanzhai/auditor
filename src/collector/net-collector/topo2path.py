#!/usr/bin/python

import xml.dom.minidom as minidom
import os, sys

class Node:
	def __init__(self, id, ip, type):
		self.id = id
		self.ip = ip
		self.type = type
		self.neighbors = []
	
	def connect(self, other_side):
		self.neighbors.append(other_side)

	def toString(self):
		nbs = ""
		for nb in self.neighbors:
			nbs = nbs + nb.id + ","
		#print "id=", self.id, "ip=", self.ip, "type=", self.type, "<-->", nbs
			

class Topo:
	def __init__(self, topo_file):
		self.nodes = {}
		self.max_path_len = 0

		doc = minidom.parse(topo_file)
		node = doc.documentElement
		nodes = doc.getElementsByTagName("Node")
		links = doc.getElementsByTagName("Link")

		for nd in nodes:
			id = nd.attributes.get("id").value
			ip = nd.attributes.get("ip").value
			type = nd.attributes.get("type").value
			new_node = Node(id, ip, type)
			self.nodes[id] = new_node

		for ln in links:
			src = ln.attributes.get("src").value
			dst = ln.attributes.get("dst").value
			src_node = self.nodes[src]
			dst_node = self.nodes[dst]
			src_node.connect(dst_node)
			dst_node.connect(src_node)

		for key in self.nodes.keys():
			self.nodes[key].toString()

	def findPaths(self, src_id, dst_id):
		self.max_path_len = 1000
		path_list = self.searchPath([src_id], dst_id)	
		return path_list

	def searchPath(self, prefix, dst_id):
		if len(prefix) > self.max_path_len:
			return []

		if len(prefix) > 0 and prefix[-1] == dst_id:
			self.max_path_len = len(prefix)
			path_list = []
			path_list.append(prefix)
			return path_list
		
		path_list = []
		for nb in self.nodes[prefix[-1]].neighbors:
			if nb.id in prefix:
				continue
			new_prefix = []
			new_prefix += prefix
			new_prefix.append(nb.id)
			paths = self.searchPath(new_prefix, dst_id)
			if len(paths) > 0:
				for path in paths:
					if len(path) <= self.max_path_len:
						path_list.append(path)
		return path_list

	def findServicePaths(self, src_dst_pairs):
		path_list = []
		for src, dst in src_dst_pairs:
			path_list += self.findPaths(src, dst)
		return path_list

def PathsToXML(path_list):
	xml = ""
	for path in path_list:
		route = ""
		if len(path) > 2:
			route = path[1]
		for nd in path[2:-1]:
			route += "," + nd
		xml += "<path src=\"%s\" dst=\"%s\" route=\"%s\"/>\n" % (path[0], path[-1], route)
	return xml

if __name__ == "__main__":
	topo = Topo("./topo.xml")
	path_list = topo.findServicePaths([('7', '10'), ('8', '9')])

	print PathsToXML(path_list)

