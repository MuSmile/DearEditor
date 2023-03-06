from abc import ABCMeta, abstractmethod


_nameSeparator = '.'
def _parent(id):
	idx = id.rfind(_nameSeparator)
	if idx > -1: return id[:idx]


class Slot:
	def __init__(self, **data): self.data = data
	def type(self): return self.data['type'] if 'type' in self.data else None
	def name(self): return self.data['name'] if 'name' in self.data else None
	
	def parent(self, graph):
		pid = _parent(graph.slotId(self))
		if pid: return graph.nodes[pid]

class Node:
	def __init__(self, **data): self.data = data
	def type(self): return self.data['type'] if 'type' in self.data else None
	def name(self): return self.data['name'] if 'name' in self.data else None

	def slots(self, graph):
		slots = []
		nid = graph.nodeId(self)
		for k, v in graph.slots:
			if k.startswith(nid):
				slots.append(v)
		return slots
	def parent(self, graph):
		pid = _parent(graph.nodeId(self))
		if pid: return graph.groups[pid]

class Group:
	def __init__(self, **data): self.data = data
	def name(self): return self.data['name'] if 'name' in self.data else None

	def nodes(self, graph):
		nodes = []
		gid = graph.gropuId(self)
		for k, v in graph.nodes:
			if k.startswith(gid):
				nodes.append(v)
		return nodes
	def groups(self, graph):
		groups = []
		gid = graph.gropuId(self)
		for k, v in graph.groups:
			if k == gid: continue
			if k.startswith(gid):
				groups.append(v)
		return groups
	def parent(self, graph):
		pid = _parent(graph.groupId(self))
		if pid: return graph.groups[pid]

class Edge:
	def __init__(self, src, dst, **data):
		self.src  = src
		self.dst  = dst
		self.data = data


####################################################
class Graph(metaclass = ABCMeta):
	def __init__(self):
		self.groups = {}
		self.nodes  = {}
		self.slots  = {}
		self.edges  = {}

	def groupId(self, group):
		for k, v in self.groups:
			if v == group:
				return k
	def nodeId(self, node):
		for k, v in self.nodes:
			if v == node:
				return k
	def slotId(self, slot):
		for k, v in self.slots:
			if v == slot:
				return k


	@abstractmethod
	def generateGroupId(self): pass
	@abstractmethod
	def generateNodepId(self): pass
	@abstractmethod
	def generateSlotId(self): pass
	@abstractmethod
	def generateEdgeId(self): pass


	def addGroup(self, **data):
		gid = self.generateGroupId()
		self.groups[gid] = Group(**data)

	def addNode(self, **data):
		nid = self.generateNodeId()
		self.nodes[nid] = Node(**data)

	def addSlot(self, **data):
		sid = self.generateSlotId()
		self.slots[sid] = Slot(**data)

	def addEdge(self, src, dst, **data):
		eid = self.generateEdgeId()
		self.edges[eid] = Edge(src, dst, **data)

