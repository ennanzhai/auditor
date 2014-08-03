[Install]
(1) Download NetSNMP-v5.7.2 and compile it.
(2) Copy the two executables "snmpget" and "snmpwalk" into "python".

[Usage]
In topo.py, class Topology offers two utility interfaces:
	-- Topology.construct(switch_list) which builds up the topology
	from the entrance switches from the parameter "switch_list"

	-- Topology.writeToXML(filename) which outputs the topology 
	information to a XML file.

In topo2path.py, class Topo offers two utility interfaces:
	-- Topo.Topo(filename) which reads the network topology from
	a XML file.
	-- Topo.findServices(switch_pair_list) which returns the pathes
	between the two switches in each element (tuple) in switch_pair_list.

Additionally, PathsToXML(path_list) converts the pathes to XML format.
