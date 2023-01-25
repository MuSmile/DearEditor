import sys, os
from editor.ide import Ide
from editor.tools import argparse

def hello():
	# generated from:
	# http://patorjk.com/software/taag
	print('''
	    ____                     ______    ___ __            
	   / __ \___  ____ ______   / ____/___/ (_) /_____  _____
	  / / / / _ \/ __ `/ ___/  / __/ / __  / / __/ __ \/ ___/
	 / /_/ /  __/ /_/ / /     / /___/ /_/ / / /_/ /_/ / /    
	/_____/\___/\__,_/_/     /_____/\__,_/_/\__/\____/_/     
	---------------------------------------------------------

	usage: hna {ide, run, build} [-p PRJ] [-t TAR] [--theme THEME] ...

	commands:
	   ide             start with Hna editor
	   run             run game without editor
	   build           build binaries
	   -----           -----------------------
	   install         check/install required py pkgs
	   python          exec python script with ide env

	ide:
	  -p, --prj        specify working prject path
	  --theme          specify ide theme to open with

	run:
	  -p, --prj        specify prject path to run
	  -t, --tar        specify run target {release, debug}

	build:
	  -p, --prj        specify prject path to build
	  -t, --tar        specify build target {release, debug}
		''')

def startIde(prj):
	ide = Ide(sys.argv)
	ide.raiseWindow(prj)

def runGame():
	pass

def buildBin():
	pass

if __name__ == '__main__':
	if len(sys.argv) == 1:
		hello()
		os._exit(0)

	# process args
	parser = argparse.ArgumentParser(prog = 'hna')
	# Required positional argument
	parser.add_argument('command', choices=['ide','run','build','python'], help='select hna command')
	parser.add_argument('-p', '--prj', help='specify working prject path')
	parser.add_argument('-t', '--tar', help='specify runtime target {release, debug}', default='debug')

	groupIde = parser.add_argument_group('ide')
	groupIde.add_argument('--theme', help='specify ide theme')
	groupIde.add_argument('--host', action='store_true', help='start with host mode', default=False)
	
	groupRun = parser.add_argument_group('run')
	groupRun.add_argument('--dev', action='store_true', help='specify run with dev mode', default=True)

	groupBuild = parser.add_argument_group('build')
	
	groupPython = parser.add_argument_group('python')
	groupPython.add_argument('--script', help='specify script file to exec')

	args = parser.parse_args()

	if args.command == 'ide':
		# print(args.cur)
		startIde(args.prj)
	elif args.command == 'run':
		runGame()
	elif args.command == 'build':
		buildBin()
	elif args.command == 'python':
		# can't call in local scope like func
		exec(open(args.script).read())
