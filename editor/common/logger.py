import logging, traceback

###################################
class StdFilter(logging.Filter):
	def filter(self, record):
		if record.levelname == 'DEBUG': record.levelname = 'STATUS'
		elif record.levelname == 'WARNING': record.levelname = 'WARN'
		return True

def stdLogger():
	logfmt = "[%(levelname)s: %(created)d]  %(message)s"
	fmtter = logging.Formatter(fmt = logfmt)

	handler = logging.StreamHandler()
	handler.setLevel(logging.DEBUG)
	handler.setFormatter(fmtter)
	handler.addFilter(StdFilter())

	logger = logging.getLogger('std')
	logger.addHandler(handler)
	logger.setLevel(logging.DEBUG)
	return logger


###################################
class IdeLogHandler(logging.Handler):
	def emit(self, record):
		# print(record.levelname, record.msg, record.filename, record.funcName, record.lineno)
		__std__.log(record.levelno, record.msg)
		# print(traceback.extract_stack()[0:-6])

def ideLogger():
	handler = IdeLogHandler()
	handler.setLevel(logging.DEBUG)

	logger = logging.getLogger('ide')
	logger.addHandler(handler)
	logger.setLevel(logging.DEBUG)
	return logger


###################################
__std__ = stdLogger()
__ide__ = ideLogger()

log    = __std__.debug
warn   = __std__.warning
error  = __std__.error
ilog   = __ide__.debug
iwarn  = __ide__.warning
ierror = __ide__.error


if __name__ == '__main__':
	log  ("This is a debug log.")
	log  ("This is a debug log.")
	log  ("This is a debug log.")
	warn ("This is a warning log.")
	warn ("This is a warning log.")
	warn ("This is a warning log.")
	error("This is a error log.")
	error("This is a error log.")
	error("This is a error log.")
