# property_type:
#	unknown
#	action
#	int
#	float
#	boolean
#	string
#	enum
#	flag
#	color
#	vector2
#	vector3
#	vector4
#	reference(assets, objects)
#	list
#	dict
#
# property_group_type:
#	unknown
#	simple_group
#	title_group
#	box_group
#	foldout_group
#	tab_group

class Property:
	def __init__(self, name, type, value = None, **metas):
		self.name = name
		self.type = type
		self.value = value
		self.metas = metas

	def meta(self, key, defvalue = None):
		return self.metas[key] if key in self.metas else defvalue

	def label   (self): return self.meta('label', self.name)
	def tooltip (self): return self.meta('tooltip')
	def readonly(self): return self.meta('readonly', False)
	def setter  (self): return self.meta('setter')
	def getter  (self): return self.meta('getter')

	def spaceAfter (self): return self.meta('space')
	def spaceBefore(self): return self.meta('space_before')

	def min (self): return self.meta('min')
	def max (self): return self.meta('max')
	def step(self): return self.meta('step')

	def enumList(self): return self.meta('enum_list')
	def flagList(self): return self.meta('flag_list')

	def refType(self): return self.meta('ref_type')

	def itemType (self): return self.meta('item_type')
	def keyType  (self): return self.meta('key_type')
	def valueType(self): return self.meta('value_type')

	def group    (self): return self.meta('group')
	def groupType(self): return self.meta('group_type')

class PropertyGroup:
	def __init__(self, name, type):
		self.name = name
		self.type = type
		self.properties = []

	def append(self, property):
		self.properties.append(property)

	def insert(self, index, property):
		self.properties.insert(index, property)

class DataGrid:
	def __init__(self):
		self.properties = []

	def append(self, name, type, **metas):
		p = Property(name, type, **metas)
		self.properties.append(p)

	def buildGroups(self):
		# todo: nesting group
		if not self.properties: return
		groups = {}
		for p in self.properties:
			if not p.group(): continue
			g = f'{p.group()}#{p.groupType()}'
			if g in groups:
				groups[g].append(p)
			else:
				groups[g] = [ p ]

		if not groups: return

		for g in groups:
			gname, gtype = g.split('#')
			pg = PropertyGroup(gname, gtype)
			firstpos = self.properties.index(groups[g][0])
			self.properties.insert(firstpos, pg)
			for p in groups[g]:
				pg.append(p)
				self.properties.remove(p)


if __name__ == '__main__':
	import jsonpickle
	model = DataGrid()
	model.append('var0', 'int')
	model.append('var1', 'int', group = 'group1', group_type = 'box_group' )
	model.append('var2', 'int', group = 'group1', group_type = 'title_group' )
	model.append('var3', 'int', group = 'group1', group_type = 'box_group' )
	model.append('var4', 'int', group = 'group2', group_type = 'title_group' )
	model.append('var5', 'int')
	model.buildGroups()
	print(jsonpickle.encode(model, indent = '\t'))
