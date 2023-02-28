import os, importlib

basepath = os.environ[ 'DEAR_BASE_PATH' ]
for f in os.scandir(basepath + '/extensions'):
	if f.is_file(): continue
	module = 'extensions.' + f.name
	importlib.import_module(module)

# todo: setup modules watcher
