import os, sys

ignoreFolder = [
	'__pycache__',
	'__qsscache__',
	'image',
	'imgui',
]

ignoreFile = [
	'__init__',
]

acceptFile = [
	'.py',
	'.qss',
	'.h',
	'.cpp',
]

scanTarget = [
	'editor',
	'native',
]

context = {
	'pyLines'       : 0,
	'qssLines'      : 0,
	'nativeLines'   : 0,
}

def countFileLines(path):
	with open(path, encoding = 'utf-8') as f:
		return len(f.readlines())

def getFileExt( file ):
	return os.path.splitext(file)[-1]

def processDir( path ):
	for name in os.listdir( path ):
		child = f'{path}/{name}'
		if os.path.isdir( child ):
			if name in ignoreFolder: continue
			processDir( child )
		else:
			if name in ignoreFile: continue
			ext = getFileExt( name )
			if ext not in acceptFile: continue
			processFile( child, ext )

def processFile( path, ext ):
	global context
	if ext == '.py':
		context['pyLines'] += countFileLines( path )
	elif ext == '.qss':
		context['qssLines'] += countFileLines( path )
	elif ext == '.h' or ext == '.cpp':
		context['nativeLines'] += countFileLines( path )

if __name__ == '__main__':
	for target in scanTarget: processDir( target )
	print( '------------------------------------------' )
	print( 'prj reports:' )
	print( '------------------------------------------' )
	print( '> editor script lines: {0}'.format( context['pyLines'] ) )
	print( '> editor themes lines: {0}'.format( context['qssLines'] ) )
	print( '> native code   lines: {0}'.format( context['nativeLines'] ) )
	total = context['pyLines'] + context['qssLines'] + context['nativeLines']
	print( '------------------------------------------' )
	print( '> Total text lines: {0}'.format( total ) )
	print( '------------------------------------------' )

	if sys.stdin and sys.stdin.isatty():
		# running interactively
		input()
	else:
		# running in background
		pass
