import argparse

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

	usage: dear {ide, run, build, list, ...} [-h] [--help] ...

	commands:
	   ide             start Dear Editor ide
	   run             run game without ide
	   build           build game binaries
	   -----           ------------------------
	   install         install required py pkgs
	   list            list all available commands

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


def description():
	return 'display hello page'

def main( argv ):
	parser = argparse.ArgumentParser(prog = 'dear hello', description = description())
	args = parser.parse_args(argv)
	hello()
