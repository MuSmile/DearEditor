from enum import Enum

class PropertyType(Enum):
	Unknown    = 0
	Int        = 1
	Float      = 2
	Boolean    = 3
	String     = 4
	Enum       = 5
	Flag       = 6
	Color      = 7
	Object     = 8
	Action     = 9

	Vec2       = 10
	Vec3       = 11
	Vec4       = 12

	List       = 20
	Dict       = 21

class GroupType(Enum):
	Unknown       = 0
	SimpleGroup   = 1
	TitleGroup    = 2
	BoxGroup      = 3
	FoldoutGroup  = 4
	TabGroup      = 5


##############################################
class Property:
	def __init__(self, name, type, **metas):
		self.name = name
		self.type = type
		self.metas = metas

	def meta(self, key, defvalue = None):
		return self.metas[key] if key in self.metas else defvalue

	def label   (self): return self.meta('label', self.name)
	def value   (self): return self.meta('value')
	def tooltip (self): return self.meta('tooltip')
	def readonly(self): return self.meta('readonly', False)
	def priority(self): return self.meta('priority', 'auto')

	def setter  (self): return self.meta('setter')
	def getter  (self): return self.meta('getter')

	def spaceAfter (self): return self.meta('space')
	def spaceBefore(self): return self.meta('space_before')

	def min (self): return self.meta('min')
	def max (self): return self.meta('max')
	def step(self): return self.meta('step')

	def items(self): return self.meta('items') # for enum/flag

	def keyType  (self): return self.meta('key_type')
	def valueType(self): return self.meta('value_type') # for item type

	def group    (self): return self.meta('group')
	def groupType(self): return self.meta('group_type')

class PropertyGroup:
	def __init__(self, name, type, **metas):
		self.name = name
		self.type = type
		self.metas = metas
		self.properties = []

	def append(self, property):
		self.properties.append(property)

	def insert(self, index, property):
		self.properties.insert(index, property)

	def meta(self, key, defvalue = None):
		return self.metas[key] if key in self.metas else defvalue

	def priority(self): return self.meta('priority', 'auto')


##############################################
class PropertyModel:
	def __init__(self):
		self.properties = []

	def append(self, name, type, **metas):
		p = Property(name, type, **metas)
		self.properties.append(p)

	def commit(self):
		# todo: nesting group, priority sorting
		if not self.properties: return
		groupTable = {}
		for p in self.properties:
			if not p.group(): continue
			groupId = p.group() + '::' + str(p.groupType())[10:]
			if groupId in groupTable: groupTable[ groupId ].append(p)
			else: groupTable[ groupId ] = [ p ]

		if not groupTable: return

		for groupId in groupTable:
			groupName, groupType = groupId.split('::')
			group = PropertyGroup(groupName, GroupType[ groupType ])
			beginPos = self.properties.index(groupTable[groupId][0])
			self.properties.insert(beginPos, group)
			for p in groupTable[ groupId ]:
				group.append(p)
				self.properties.remove(p)


##############################################
if __name__ == '__main__':
	import jsonpickle
	model = PropertyModel()
	model.append('var0', PropertyType.Int)
	model.append('var1', PropertyType.Int, group = 'group1', group_type = GroupType.BoxGroup )
	model.append('var2', PropertyType.Int, group = 'group1', group_type = GroupType.TitleGroup )
	model.append('var3', PropertyType.Int, group = 'group1', group_type = GroupType.BoxGroup )
	model.append('var4', PropertyType.Int, group = 'group2', group_type = GroupType.TitleGroup )
	model.append('var5', PropertyType.Int)
	model.commit()
	print(jsonpickle.encode(model, indent = '\t'))

