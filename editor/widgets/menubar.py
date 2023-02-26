import sys, os
from PySide6.QtCore import Qt, QCoreApplication
from PySide6.QtGui import QAction
from PySide6.QtWidgets import QMenuBar
from editor.common.logger import warn
from editor.widgets.menu.menu_tree import MenuTree

class MenuBarModel:
	def __init__(self):
		self.menuTreeTable = {}
		self.menuPriorityTable = {}
		self.defaultPriority = 20
		self.menubar = None

	def registerMenu(self, name, priority):
		if name in self.menuPriorityTable: warn(f'menu \'{name}\' has registered, priority will be overrided.')
		self.menuPriorityTable[ name ] = priority

	def affirmMenuTree(self, name):
		if name not in self.menuTreeTable: self.menuTreeTable[ name ] = MenuTree(name)
		return self.menuTreeTable[ name ]

	def registerMenuItem(self, path, callback, shortcut = None, priority = None, **data):
		idx = path.find('/')
		assert(idx != -1)
		name = path[:idx]
		path = path[idx+1:]
		tree = self.affirmMenuTree(name)
		if 'shortcutContext' not in data: data['shortcutContext'] = Qt.ApplicationShortcut
		tree.addItem(path, callback, shortcut, priority, **data)

	def registerMenuSeparator(self, groupPath, priority = None, **data):
		idx = groupPath.find('/')
		if idx == -1: idx = len(groupPath)
		name = groupPath[:idx]
		groupPath = groupPath[idx+1:]
		tree = self.affirmMenuTree(name)
		tree.addSeparator(groupPath, priority, **data)

	def menuPriority(self, name):
		if name in self.menuPriorityTable: return self.menuPriorityTable[ name ]
		return self.defaultPriority

	def createMenuBar(self, parent):
		self.menubar = QMenuBar(parent)
		self.menubar.setContextMenuPolicy(Qt.PreventContextMenu)
		sortedMenus = sorted(self.menuTreeTable.keys(), key = lambda n: self.menuPriority(n))
		for name in sortedMenus:
			tree = self.menuTreeTable[ name ]
			widget = tree.createWidget(parent)
			self.menubar.addMenu(widget)
		# self.menubar.setNativeMenuBar(False)
		return self.menubar

	def updateMenuBar(self):
		assert(self.menubar)
		pass


#####################  INIT  #####################
_model = MenuBarModel()

_model.registerMenu('File'      ,     1)
_model.registerMenu('Edit'      ,     2)
_model.registerMenu('Asset'     ,     3)
_model.registerMenu('Entity'    ,     4)
_model.registerMenu('Component' ,     5)

_model.registerMenu('Window'    , 10000)
_model.registerMenu('Help'      , 10001)


_model.registerMenuItem('Tools/__placeholder__', None)


#####################  MENU - FILE  #####################
_model.registerMenuItem('File/New Scene', None, 'Ctrl+N')
_model.registerMenuItem('File/Open Scene', None, 'Ctrl+O')

_model.registerMenuSeparator('File')
_model.registerMenuItem('File/Save', None, 'Ctrl+S')
_model.registerMenuItem('File/Save As...', None, 'Ctrl+Shift+S')

_model.registerMenuSeparator('File')
_model.registerMenuItem('File/New Project...', None)
_model.registerMenuItem('File/Open Project...', None)
_model.registerMenuItem('File/Save Project', None)

_model.registerMenuSeparator('File')
_model.registerMenuItem('File/Build Settings...', None, 'Ctrl+Shift+B')
_model.registerMenuItem('File/Build And Run', None, 'Ctrl+B')

_model.registerMenuItem('File/Restart Dear', lambda: os.execl(sys.executable, sys.executable, *sys.argv), 'Ctrl+R', priority = 10000, menuRole = QAction.ApplicationSpecificRole)
_model.registerMenuItem('File/Quit Dear', QCoreApplication.quit, 'Ctrl+Q', priority = 10001)


#####################  MENU - EDIT  #####################
_model.registerMenuItem('Edit/Undo', None, 'Ctrl+Z')
_model.registerMenuItem('Edit/Redo', None, 'Ctrl+Y')

_model.registerMenuSeparator('Edit')
_model.registerMenuItem('Edit/Select All', None, 'Ctrl+A')
_model.registerMenuItem('Edit/Deselect All', None, 'Shift+D')
_model.registerMenuItem('Edit/Select Children', None, 'Shift+C')
_model.registerMenuItem('Edit/Select Prefab Root', None, 'Ctrl+Shift+R')
_model.registerMenuItem('Edit/Invert Selection', None, 'Ctrl+Y')

_model.registerMenuSeparator('Edit')
_model.registerMenuItem('Edit/Cut', None, 'Ctrl+X')
_model.registerMenuItem('Edit/Copy', None, 'Ctrl+C')
_model.registerMenuItem('Edit/Paste', None, 'Ctrl+V')

_model.registerMenuSeparator('Edit')
_model.registerMenuItem('Edit/Duplicate', None, 'Ctrl+D')
_model.registerMenuItem('Edit/Rename', None)
_model.registerMenuItem('Edit/Delete', None)

_model.registerMenuSeparator('Edit')
_model.registerMenuItem('Edit/Frame Selected', None, 'F')
_model.registerMenuItem('Edit/Lock View to Selected', None, 'Shift+F')
_model.registerMenuItem('Edit/Find', None, 'Ctrl+F')

_model.registerMenuSeparator('Edit')
_model.registerMenuItem('Edit/Play', None, 'Ctrl+P')
_model.registerMenuItem('Edit/Pause', None, 'Ctrl+Shift+P')
_model.registerMenuItem('Edit/Step', None, 'Ctrl+Alt+P')

_model.registerMenuSeparator('Edit')
_model.registerMenuItem('Edit/Project Settings...', None)
_model.registerMenuItem('Edit/Preferences...', None)
_model.registerMenuItem('Edit/Shortcuts...', None)


#####################  MENU - ASSET  #####################
_model.registerMenuItem('Asset/Create/Folder', None)
_model.registerMenuSeparator('Asset/Create')
_model.registerMenuItem('Asset/Create/Script', None)
_model.registerMenuItem('Asset/Create/Shader', None)
_model.registerMenuSeparator('Asset/Create')
_model.registerMenuItem('Asset/Create/Scene', None)
_model.registerMenuItem('Asset/Create/Post-processing Profile', None)
_model.registerMenuItem('Asset/Create/Prefab Variant', None)
_model.registerMenuSeparator('Asset/Create')
_model.registerMenuItem('Asset/Create/Material', None)
_model.registerMenuItem('Asset/Create/Lens Flare', None)
_model.registerMenuItem('Asset/Create/Render Texture', None)
_model.registerMenuItem('Asset/Create/Lightmap Parameters', None)
_model.registerMenuItem('Asset/Create/Custom Render Texture', None)
_model.registerMenuSeparator('Asset/Create')
_model.registerMenuItem('Asset/Create/Sprite Atlas', None)
_model.registerMenuItem('Asset/Create/Sprites', None)
_model.registerMenuSeparator('Asset/Create')
_model.registerMenuItem('Asset/Create/Animation', None)
_model.registerMenuItem('Asset/Create/Timeline', None)

import platform
if platform.system() == 'Darwin':
	_model.registerMenuItem('Asset/Rereal in Finder', None)
else:
	_model.registerMenuItem('Asset/Show in Explorer', None)

_model.registerMenuItem('Asset/Open', None)
_model.registerMenuItem('Asset/Delete', None)
_model.registerMenuItem('Asset/Rename', None)
_model.registerMenuItem('Asset/Copy Path', None, 'Ctrl+Shift+C')

_model.registerMenuSeparator('Asset')
_model.registerMenuItem('Asset/Import New Asset...', None)
_model.registerMenuItem('Asset/Import Package', None)
_model.registerMenuItem('Asset/Export Package...', None)
_model.registerMenuItem('Asset/Find References In Scene', None)
_model.registerMenuItem('Asset/Select Dependencies', None)

_model.registerMenuSeparator('Asset')
_model.registerMenuItem('Asset/Refresh', None, 'Shift+R')
_model.registerMenuItem('Asset/Reimport', None)
_model.registerMenuSeparator('Asset')
_model.registerMenuItem('Asset/Reimport All', None)
_model.registerMenuSeparator('Asset')
_model.registerMenuItem('Asset/Open Script Project', None)


#####################  MENU - EDIT  #####################
_model.registerMenuItem('Entity/Create Empty', None, 'Ctrl+Shift+N')
_model.registerMenuItem('Entity/Create Empty Child', None, 'Alt+Shift+N')

_model.registerMenuItem('Entity/3D Entity/Cube', None)
_model.registerMenuItem('Entity/3D Entity/Sphere', None)
_model.registerMenuItem('Entity/3D Entity/Capsule', None)
_model.registerMenuItem('Entity/3D Entity/Cylinder', None)
_model.registerMenuItem('Entity/3D Entity/Plane', None)
_model.registerMenuItem('Entity/3D Entity/Quad', None)
_model.registerMenuSeparator('Entity/3D Entity')
_model.registerMenuItem('Asset/Create/Post-processing Volume', None)
_model.registerMenuSeparator('Entity/3D Entity')
_model.registerMenuItem('Asset/Create/Terrain', None)
_model.registerMenuItem('Asset/Create/Tree', None)
_model.registerMenuItem('Asset/Create/Wind Zone', None)
_model.registerMenuSeparator('Entity/3D Entity')
_model.registerMenuItem('Asset/Create/3D Text', None)


#####################  MENU - ENTITY  #####################
_model.registerMenuItem('Entity/2D Entity/Sprite', None)
_model.registerMenuSeparator('Entity/2D Entity')
_model.registerMenuItem('Entity/2D Entity/Sprite Mask', None)
_model.registerMenuItem('Entity/2D Entity/Tilemap', None)

_model.registerMenuItem('Entity/Effects/Particle System', None)
_model.registerMenuItem('Entity/Effects/Particle System Force Field', None)
_model.registerMenuItem('Entity/Effects/Trail', None)
_model.registerMenuItem('Entity/Effects/Line', None)

_model.registerMenuItem('Entity/Light/Directional Light', None)
_model.registerMenuItem('Entity/Light/Point Light', None)
_model.registerMenuItem('Entity/Light/Spotlight', None)
_model.registerMenuItem('Entity/Light/Area Light', None)
_model.registerMenuSeparator('Entity/Light')
_model.registerMenuItem('Entity/Light/Reflection Probe', None)
_model.registerMenuItem('Entity/Light/Light Probe Group', None)

_model.registerMenuItem('Entity/Audio/Audio Source', None)
_model.registerMenuItem('Entity/Audio/Audio Reverb Zone', None)
_model.registerMenuItem('Entity/Video/Video Player', None)

_model.registerMenuItem('Entity/UI/Text', None)
_model.registerMenuItem('Entity/UI/Image', None)
_model.registerMenuItem('Entity/UI/Raw Image', None)
_model.registerMenuSeparator('Entity/UI')
_model.registerMenuItem('Entity/UI/Button', None)
_model.registerMenuItem('Entity/UI/Toggle', None)
_model.registerMenuItem('Entity/UI/Slider', None)
_model.registerMenuItem('Entity/UI/Scrollbar', None)
_model.registerMenuItem('Entity/UI/Dropdown', None)
_model.registerMenuItem('Entity/UI/Input Field', None)
_model.registerMenuSeparator('Entity/UI')
_model.registerMenuItem('Entity/UI/Canvas', None)
_model.registerMenuItem('Entity/UI/Panel', None)
_model.registerMenuItem('Entity/UI/Scroll View', None)
_model.registerMenuSeparator('Entity/UI')
_model.registerMenuItem('Entity/UI/Event System', None)

_model.registerMenuItem('Entity/Camera', None)
_model.registerMenuSeparator('Entity')
_model.registerMenuItem('Entity/Center on Children', None)

_model.registerMenuSeparator('Entity')
_model.registerMenuItem('Entity/Make Parent', None)
_model.registerMenuItem('Entity/Clear Parent', None)

_model.registerMenuSeparator('Entity')
_model.registerMenuItem('Entity/Lock Selection', None)
_model.registerMenuItem('Entity/Unlock Selection', None, 'Ctrl+Alt+L')
_model.registerMenuItem('Entity/Move Selection Up', None, 'Shift+W')
_model.registerMenuItem('Entity/Move Selection Down', None, 'Shift+S')

_model.registerMenuSeparator('Entity')
_model.registerMenuItem('Entity/Set as first sibling', None, 'Ctrl+=')
_model.registerMenuItem('Entity/Set as last sibling', None, 'Ctrl+-')
_model.registerMenuItem('Entity/Move To View', None, 'Ctrl+Alt+F')
_model.registerMenuItem('Entity/Align With View', None, 'Ctrl+Shift+F')
_model.registerMenuItem('Entity/Align View To Selected', None)
_model.registerMenuItem('Entity/Toggle Active State', None, 'Alt+Shift+A')


#####################  MENU - COMPONENT  #####################
_model.registerMenuItem('Component/Create...', None, 'Ctrl+Shift+A')

_model.registerMenuItem('Component/Mesh/Mesh Filter', None)
_model.registerMenuItem('Component/Mesh/Text Mesh', None)
_model.registerMenuSeparator('Component/Mesh')
_model.registerMenuItem('Component/Mesh/Mesh Renderer', None)
_model.registerMenuItem('Component/Mesh/Skinned Mesh Renderer', None)

_model.registerMenuItem('Component/Effects/Particle System', None)
_model.registerMenuItem('Component/Effects/Trail Renderer', None)
_model.registerMenuItem('Component/Effects/Line Renderer', None)
_model.registerMenuItem('Component/Effects/Lens Flare', None)
_model.registerMenuItem('Component/Effects/Halo', None)
_model.registerMenuItem('Component/Effects/Projector', None)
_model.registerMenuItem('Component/Effects/Visual Effect', None)

_model.registerMenuItem('Component/Physics/Rigidbody', None)
_model.registerMenuSeparator('Component/Physics')
_model.registerMenuItem('Component/Physics/Box Collider', None)
_model.registerMenuItem('Component/Physics/Sphere Collider', None)
_model.registerMenuItem('Component/Physics/Capsule Collider', None)
_model.registerMenuItem('Component/Physics/Mesh Collider', None)
_model.registerMenuItem('Component/Physics/Terrain Collider', None)
_model.registerMenuSeparator('Component/Physics')
_model.registerMenuItem('Component/Physics/Cloth', None)
_model.registerMenuSeparator('Component/Physics')
_model.registerMenuItem('Component/Physics/Hinge Joint', None)
_model.registerMenuItem('Component/Physics/Fixed Joint', None)
_model.registerMenuItem('Component/Physics/Spring Joint', None)
_model.registerMenuItem('Component/Physics/Configurable Joint', None)
_model.registerMenuSeparator('Component/Physics')
_model.registerMenuItem('Component/Physics/Constant Force', None)

_model.registerMenuItem('Component/Physics 2D/Rigidbody 2D', None)
_model.registerMenuSeparator('Component/Physics 2D')
_model.registerMenuItem('Component/Physics 2D/Box Collider 2D', None)
_model.registerMenuItem('Component/Physics 2D/Circle Collider 2D', None)
_model.registerMenuItem('Component/Physics 2D/Edge Collider 2D', None)
_model.registerMenuItem('Component/Physics 2D/Polygon Collider 2D', None)
_model.registerMenuItem('Component/Physics 2D/Capsule Collider 2D', None)
_model.registerMenuItem('Component/Physics 2D/Composite Collider 2D', None)
_model.registerMenuSeparator('Component/Physics 2D')
_model.registerMenuItem('Component/Physics 2D/Distance Joint 2D', None)
_model.registerMenuItem('Component/Physics 2D/Fixed Joint 2D', None)
_model.registerMenuItem('Component/Physics 2D/Friction Joint 2D', None)
_model.registerMenuItem('Component/Physics 2D/Hinge Joint 2D', None)
_model.registerMenuItem('Component/Physics 2D/Relative Joint 2D', None)
_model.registerMenuItem('Component/Physics 2D/Slider Joint 2D', None)
_model.registerMenuItem('Component/Physics 2D/Spring Joint 2D', None)
_model.registerMenuItem('Component/Physics 2D/Target Joint 2D', None)
_model.registerMenuSeparator('Component/Physics 2D')
_model.registerMenuItem('Component/Physics 2D/Area Effector 2D', None)
_model.registerMenuItem('Component/Physics 2D/Buoyancy Effector 2D', None)
_model.registerMenuItem('Component/Physics 2D/Point Effector 2D', None)
_model.registerMenuItem('Component/Physics 2D/Platform Effector 2D', None)
_model.registerMenuItem('Component/Physics 2D/Surface Effector 2D', None)
_model.registerMenuSeparator('Component/Physics 2D')
_model.registerMenuItem('Component/Physics 2D/Constant Force 2D', None)

_model.registerMenuItem('Component/Navigation', None)

_model.registerMenuItem('Component/Audio/Audio Listener', None)
_model.registerMenuItem('Component/Audio/Audio Source', None)
_model.registerMenuItem('Component/Audio/Audio Reverb Zone', None)
_model.registerMenuSeparator('Component/Audio')
_model.registerMenuItem('Component/Audio/Audio Low Pass Filter', None)
_model.registerMenuItem('Component/Audio/Audio High Pass Filter', None)
_model.registerMenuItem('Component/Audio/Audio Echo Filter', None)
_model.registerMenuItem('Component/Audio/Audio Distortion Filter', None)
_model.registerMenuItem('Component/Audio/Audio Reverb Filter', None)
_model.registerMenuItem('Component/Audio/Audio Chorus Filter', None)

_model.registerMenuItem('Component/Video/Video Player', None)

_model.registerMenuItem('Component/Rendering/Camera', None)
_model.registerMenuItem('Component/Rendering/Skybox', None)
_model.registerMenuItem('Component/Rendering/Flare Layer', None)
_model.registerMenuSeparator('Component/Rendering')
_model.registerMenuItem('Component/Rendering/Light', None)
_model.registerMenuItem('Component/Rendering/Light Probe Group', None)
_model.registerMenuItem('Component/Rendering/Light Probe Proxy Volume', None)
_model.registerMenuItem('Component/Rendering/Reflection Probe', None)
_model.registerMenuSeparator('Component/Rendering')
_model.registerMenuItem('Component/Rendering/Occlusion Area', None)
_model.registerMenuItem('Component/Rendering/Occlusion Portal', None)
_model.registerMenuItem('Component/Rendering/LOD Group', None)
_model.registerMenuSeparator('Component/Rendering')
_model.registerMenuItem('Component/Rendering/Sprite Renderer', None)
_model.registerMenuItem('Component/Rendering/Sorting Group', None)
_model.registerMenuItem('Component/Rendering/Canvas Renderer', None)
_model.registerMenuSeparator('Component/Rendering')
_model.registerMenuItem('Component/Rendering/Post-process Layer', None)
_model.registerMenuItem('Component/Rendering/Post-process Volume', None)
_model.registerMenuItem('Component/Rendering/Post-process Debug', None)

_model.registerMenuItem('Component/Tilemap/Tilemap', None)
_model.registerMenuItem('Component/Tilemap/Tilemap Renderer', None)
_model.registerMenuItem('Component/Tilemap/Tilemap Collider 2D', None)

_model.registerMenuItem('Component/Layout', None)
_model.registerMenuItem('Component/Scripts', None)
_model.registerMenuItem('Component/UI', None)
_model.registerMenuItem('Component/Event', None)
_model.registerMenuItem('Component/Input', None)


#####################  MENU - WINDOW  #####################
_model.registerMenuItem('Window/Next Window', None, 'Ctrl+Tab')
_model.registerMenuItem('Window/Previous Window', None, 'Ctrl+Shift+Tab')

_model.registerMenuSeparator('Window')
_model.registerMenuItem('Window/Layouts/Default', None)
_model.registerMenuSeparator('Window/Layouts')
_model.registerMenuItem('Window/Layouts/Save Layout...', None)
_model.registerMenuItem('Window/Layouts/Load Layout...', None)
_model.registerMenuItem('Window/Layouts/Revert Factory Settings...', None)

_model.registerMenuSeparator('Window')
_model.registerMenuItem('Window/General/Scene', None, 'Ctrl+1')
_model.registerMenuItem('Window/General/Game', None, 'Ctrl+2')
_model.registerMenuItem('Window/General/Inspector', None, 'Ctrl+3')
_model.registerMenuItem('Window/General/Hierarchy', None, 'Ctrl+4')
_model.registerMenuItem('Window/General/Project', None, 'Ctrl+5')
_model.registerMenuItem('Window/General/Console', None, 'Ctrl+Shift+C')
_model.registerMenuItem('Window/General/Test Runner', None)
_model.registerMenuSeparator('Window/General')
_model.registerMenuItem('Window/General/Active Tool', None)

_model.registerMenuItem('Window/Rendering/Lighting Settings', None)
_model.registerMenuItem('Window/Rendering/Light Explorer', None)
_model.registerMenuSeparator('Window/Rendering')
_model.registerMenuItem('Window/Rendering/Occlusion Culling', None)

_model.registerMenuItem('Window/Animation/Animation', None, 'Ctrl+6')
_model.registerMenuItem('Window/Audio/Audio Mixer', None, 'Ctrl+8')
_model.registerMenuItem('Window/Sequencing/Timeline', None)

_model.registerMenuItem('Window/Analysis/Profiler', None, 'Ctrl+7')
_model.registerMenuItem('Window/Analysis/Frame Debugger', None)
_model.registerMenuItem('Window/Analysis/Physics Debugger', None)
_model.registerMenuSeparator('Window/Analysis')
_model.registerMenuItem('Window/Analysis/Input Debugger', None)

_model.registerMenuItem('Window/2D/Sprite Editor', None, 'Ctrl+6')
_model.registerMenuItem('Window/2D/Sprite Packer', None, 'Ctrl+8')


#####################  MENU - HELP  #####################
_model.registerMenuItem('Help/About Dear', None)
_model.registerMenuItem('Help/Documentation', None)
_model.registerMenuSeparator('Help')
_model.registerMenuItem('Help/Release Notes', None)
_model.registerMenuItem('Help/Software Licenses', None)
_model.registerMenuItem('Help/Report a Bug...', None)
_model.registerMenuSeparator('Help')
_model.registerMenuItem('Help/Troubleshoot Issue...', None)
_model.registerMenuSeparator('Help')
_model.registerMenuItem('Help/Quick Search', None, 'Alt+\'')
# _model.registerMenuItem('File/test', None, role = QAction.ApplicationSpecificRole, priority = 1)


#####################  API  ######################
def createMenuBar(parent):
	return _model.createMenuBar(parent)

def updateMenuBar():
	return _model.updateMenuBar()

def registerMenu(name, priority):
	_model.registerMenu(name, priority)

def registerMenuItem(path, callback, shortcut = None, priority = None, **data):
	_model.registerMenuItem(path, callback, shortcut, priority, **data)

def registerMenuSeparator(groupPath, priority = None, **data):
	_model.registerMenuSeparator(groupPath, priority, **data)

def menuItem(path, shortcut = None, priority = None, **data):
	def warpper(func):
		_model.registerMenuItem(path, func, shortcut, priority, **data)
		return func
	return warpper
