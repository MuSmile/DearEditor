import logging

# loggingFmt = "[%(levelname)s\t: %(created)d]\t%(message)s"
# logging.basicConfig(level = logging.DEBUG, format = loggingFmt)

# DEBUG
# INFO
# WARNING
# ERROR
# CRITICAL

class _StdFilter(logging.Filter):
	def filter(self, record):
		# record.levelname = _levelnameTable[record.levelname]
		if record.levelname == 'DEBUG': record.levelname = 'STATUS'
		elif record.levelname == 'WARNING': record.levelname = 'WARN'
		return True

def _getStdLogger():
	logfmt = "[%(levelname)s: %(created)d]  %(message)s"
	fmtter = logging.Formatter(fmt = logfmt)

	handler = logging.StreamHandler()
	handler.setLevel(logging.DEBUG)
	handler.setFormatter(fmtter)
	handler.addFilter(_StdFilter())

	logger = logging.getLogger('log')
	logger.addHandler(handler)
	logger.setLevel(logging.DEBUG)
	return logger

class _IdeFilter(logging.Filter):
	def filter(self, record):
		# filter and send to ide ouput view
		return False

def _getIdeLogger():
	handler = logging.StreamHandler()
	handler.setLevel(logging.DEBUG)
	handler.addFilter(_IdeFilter())

	logger = logging.getLogger('log.ide')
	logger.addHandler(handler)
	logger.setLevel(logging.DEBUG)
	return logger

_logger    = _getStdLogger()
_ideLogger = _getIdeLogger()

log    = _logger.debug
warn   = _logger.warning
error  = _logger.error
ilog   = _ideLogger.debug
iwarn  = _ideLogger.warning
ierror = _ideLogger.error

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
