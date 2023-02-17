from editor.common import argparse

def description():
	return 'exec py with ide env'

def main( argv ):
	parser = argparse.ArgumentParser(prog = 'dear python', description = description())
	parser.add_argument('--script', help='specify script file to exec', required=True)
	args = parser.parse_args(argv)
	exec(open(args.script).read())
