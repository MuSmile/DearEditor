"""This module provides standard log toolkit.

Typical usage example:

.. code-block:: python
   :linenos:

   from editor.common.logger import log, warn, error
   log  ("This is a debug log.")
   warn ("This is a warn  log.")
   error("This is a error log.")

   ####################################################
   from editor.common.logger import ilog, iwarn, ierror
   ilog  ("This is a debug log to ide.")
   iwarn ("This is a warn  log to ide.")
   ierror("This is a error log to ide.")
"""

import logging, traceback

###################################
class _StdFilter(logging.Filter):
	def filter(self, record):
		if record.levelname == 'DEBUG': record.levelname = 'STATUS'
		elif record.levelname == 'WARNING': record.levelname = 'WARN'
		return True

def _stdLogger():
	logfmt = "[%(levelname)s: %(created)d]  %(message)s"
	fmtter = logging.Formatter(fmt = logfmt)

	handler = logging.StreamHandler()
	handler.setLevel(logging.DEBUG)
	handler.setFormatter(fmtter)
	handler.addFilter(_StdFilter())

	logger = logging.getLogger('std')
	logger.addHandler(handler)
	logger.setLevel(logging.DEBUG)
	return logger


###################################
class _IdeLogHandler(logging.Handler):
	def emit(self, record):
		# print(record.levelname, record.msg, record.filename, record.funcName, record.lineno)
		__std__.log(record.levelno, record.msg)
		# print(traceback.extract_stack()[0:-6])

def _ideLogger():
	handler = _IdeLogHandler()
	handler.setLevel(logging.DEBUG)

	logger = logging.getLogger('ide')
	logger.addHandler(handler)
	logger.setLevel(logging.DEBUG)
	return logger


###################################
__std__ = _stdLogger()
__ide__ = _ideLogger()


log    = __std__.debug
"""Emit debug log via std logger"""
warn   = __std__.warning
"""Emit warning log via std logger"""
error  = __std__.error
"""Emit error log via std logger"""
ilog   = __ide__.debug
"""Emit debug log via ide logger"""
iwarn  = __ide__.warning
"""Emit warning log via ide logger"""
ierror = __ide__.error
"""Emit error log via ide logger"""


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
