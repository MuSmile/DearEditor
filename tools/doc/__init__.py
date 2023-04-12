import os, platform, argparse

def testRequirements(path):
	import pkg_resources
	from pkg_resources import DistributionNotFound, VersionConflict

	try:
		dependencies = None
		with open(path, 'r') as file:
			dependencies = file.read()
			file.close()
		pkg_resources.require(dependencies)
		return True

	except Exception as e:
		print('----------------------------------------------------------------')
		print('[Error] generate fail! check python pkg requirements state first')
		print('----------------------------------------------------------------')

		if isinstance(e, DistributionNotFound):
			print(f'pkg_resources.DistributionNotFound: The \'{e.req}\' distribution was not found and is required by the application')
		elif isinstance(e, VersionConflict):
			print(f'pkg_resources.VersionConflict: The \'{e.req}\' distribution version conflicted and is required by the application')
		else:
			print(e)
		return False


###################################################
def description():
	return 'editor doc toolkit'

def main( argv ):
	parser = argparse.ArgumentParser(prog = 'dear doc', description = description())
	parser.add_argument('command', choices=['clean','gen','open'], default='open', nargs='?', help='select command to perform')
	groupGen = parser.add_argument_group('gen')
	groupGen.add_argument('-j', '--job', metavar='N', type=int, default=12, help='distribute over N processes in parallel')
	args = parser.parse_args(argv)

	docFolder = os.environ[ 'DEAR_BASE_PATH' ] + '/docs'
	buildFolder = docFolder + '/_build'
	cmd = args.command

	if cmd == 'open':
		import webbrowser
		index = buildFolder + '/index.html'
		if os.path.exists(index):
			webbrowser.open_new_tab('file:///' + index)
		else:
			print('local doc not found, try open online doc...')
			url = 'https://MuSmile.github.io/DearDoc'
			webbrowser.open_new_tab(url)
		return

	if cmd == 'clean':
		if os.path.exists(buildFolder):
			import shutil
			for f in os.scandir(buildFolder):
				if f.name == '.git': continue
				if f.name == '.gitignore': continue
				if f.name == '.nojekyll': continue
				if f.name == 'readme.md': continue
				if f.is_dir(): shutil.rmtree(f)
				else: os.remove(f)
			print('doc clean completed.')
		else:
			print('doc cleaned already.')
		return

	if cmd == 'gen':
		reqPath = docFolder + '/requirements.txt'
		if not testRequirements(reqPath): return

		binFolder = os.environ[ 'DEAR_BASE_PATH' ]
		if platform.system() == 'Windows':
			binFolder += '/py/Scripts'
		else:
			binFolder += '/py/bin'

		cwd = os.getcwd()
		os.chdir(docFolder)
		os.system(f'{binFolder}/sphinx-build -b html . _build -j {args.job}')
		os.chdir(cwd)
		return
