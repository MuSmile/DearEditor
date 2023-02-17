import sys, os, importlib, warnings
warnings.filterwarnings('ignore')


def addEnvPath( key, entry, prepend = False ):
	if not isinstance( entry, list ): entry = [ entry ]
	processedEntry = entry

	try:
		path0 = os.environ[ key ]
		if prepend:
			processedEntry = processedEntry + [ path0 ]
		else:
			processedEntry = [ path0 ] + processedEntry
	except KeyError as e:
		pass

	path1 = os.pathsep.join( processedEntry )
	os.environ[ key ] = path1
	os.putenv( key, path1 )
	return path1


def setupEnvironment():
	basepath = os.path.dirname(__file__)
	sys.path.insert(0, basepath)

	# addEnvPath( 'PATH', _path, True )
	# addEnvPath( 'DYLD_FRAMEWORK_PATH', _path, True )
	# addEnvPath( 'DYLD_LIBRARY_PATH', _path, True )

	os.environ[ 'DE_ENV_SET'     ] = 'OK'
	os.environ[ 'DE_CWD'         ] = os.getcwd();
	os.environ[ 'DE_BASE_PATH'   ] = basepath
	os.environ[ 'DE_THEME_PATH'  ] = basepath + '/data/themes'
	os.environ[ 'DE_LAYOUT_PATH' ] = basepath + '/data/layouts'
	os.environ[ 'DE_PREFS_PATH'  ] = basepath + '/data/prefs.db'
	# os.environ[ 'DE_SUPPORT_PATH' ] = supportPath
	# os.environ[ 'DE_NATIVE_SUPPORT_PATH' ] = supportPathNative

	# os.execv(sys.executable, [pyname] + sys.argv)


def listEditorTool():
	tooldir = os.environ[ 'DE_BASE_PATH' ] + '/tools'
	return [ f.name for f in os.scandir(tooldir) if f.is_dir() ]

def loadEditorTool(name):
	# log(f'loading tool <{name}>')
	module = 'tools.' + name
	m = importlib.import_module(module)
	if hasattr(m, 'main'): m.main(sys.argv[2:])


def printEditorTools():
	print('available commands:')
	for name in listEditorTool():
		m = importlib.import_module('tools.' + name)
		desc = hasattr(m, 'description') and m.description() or 'none'
		print('  - {:<16}  {}'.format(name, desc))
	print(f'use \'dear <commmand> -h\' for detailed helps')


if __name__ == '__main__':
	setupEnvironment()

	if len(sys.argv) == 1:
		sys.argv.append('hello')

	command = sys.argv[1]
	if command == 'list':
		printEditorTools()

	elif command in listEditorTool():
		loadEditorTool(command)

	else:
		t = command[0] == '-' and 'argument' or 'command'
		print(f'error: unrecognized {t} \'{command}\'')
		print(f'use \'dear list\' to check available commands')

