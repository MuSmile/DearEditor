import os, argparse, pkg_resources
from pkg_resources import DistributionNotFound, VersionConflict

def testRequirements(path):
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
	return 'generate prject docs'

def main( argv ):
	parser = argparse.ArgumentParser(prog = 'dear doc', description = description())
	parser.add_argument('-j', '--job', metavar = 'N', type = int, default = 1, help='distribute over N processes in parallel')
	args = parser.parse_args(argv)
	
	docPrjFoler = os.environ[ 'DEAR_BASE_PATH' ] + '/docs/.project'
	reqPath = docPrjFoler + '/requirements.txt'
	if not testRequirements(reqPath): return

	cwd = os.getcwd()
	os.chdir(docPrjFoler)
	os.system(f'sphinx-build -b html . _build -j {args.job}')
	# move build files
	os.chdir(cwd)
