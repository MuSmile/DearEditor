import os, argparse

ignoreFolder = [
	'__pycache__',
	'__qsscache__',
	'img',
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
	'engine',
	'data/themes',
]

lineCounter = {
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
	global lineCounter
	if ext == '.py':
		lineCounter['pyLines'] += countFileLines( path )
	elif ext == '.qss':
		lineCounter['qssLines'] += countFileLines( path )
	elif ext == '.h' or ext == '.cpp':
		lineCounter['nativeLines'] += countFileLines( path )


def description():
	return 'report statistics of code lines'

def main( argv ):
	parser = argparse.ArgumentParser(prog = 'dear report', description = description())
	args = parser.parse_args(argv)

	basepath = os.environ[ 'DEAR_BASE_PATH' ] + '/'
	for target in scanTarget: processDir( basepath + target )

	print( 'report results:' )
	print( '  - editor script lines: {:>8}'.format( lineCounter['pyLines'] ) )
	print( '  - editor themes lines: {:>8}'.format( lineCounter['qssLines'] ) )
	print( '  - native code   lines: {:>8}'.format( lineCounter['nativeLines'] ) )
	total = lineCounter['pyLines'] + lineCounter['qssLines'] + lineCounter['nativeLines']
	print( 'total lines: {0}, keep going...'.format( total ) )
