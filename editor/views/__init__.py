import os, importlib


basepath = os.environ[ 'DEAR_BASE_PATH' ]
for f in os.scandir(basepath + '/editor/views'):
	if f.is_file(): continue
	module = 'editor.views.' + f.name
	importlib.import_module(module)
