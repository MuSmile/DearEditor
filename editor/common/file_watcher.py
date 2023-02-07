from PySide6.QtCore import QObject, Signal

from watchdog.observers import Observer
from watchdog.events import FileSystemEvent, PatternMatchingEventHandler, RegexMatchingEventHandler, LoggingEventHandler

_observer = Observer()

class PatternWatcher(QObject):
	sigCreated  = Signal(FileSystemEvent)
	sigDeleted  = Signal(FileSystemEvent)
	sigModified = Signal(FileSystemEvent)
	sigMoved    = Signal(FileSystemEvent)

	def __init__(self,
		patterns = None, ignorePatterns = None,
		ignoreDirectories = True, caseSensitive = True,
	 	onCreated = None, onDeleted = None, onModified = None, onMoved = None):

		super().__init__()
		self.handler = PatternMatchingEventHandler(
			patterns           = patterns,
			ignore_patterns    = ignorePatterns,
			ignore_directories = ignoreDirectories,
			case_sensitive     = caseSensitive
		)
		if onCreated:
			self.sigCreated.connect(onCreated)
			self.handler.on_created = self.sigCreated.emit
		if onDeleted:
			self.sigDeleted.connect(onDeleted)
			self.handler.on_deleted = self.sigDeleted.emit
		if onModified:
			self.sigModified.connect(onModified)
			self.handler.on_modified = self.sigModified.emit
		if onMoved:
			self.sigMoved.connect(onMoved)
			self.handler.on_moved = self.sigMoved.emit

	def start(self, path, recursive = True):
		_observer.schedule(self.handler, path, recursive)
		_observer.start()

	def stop(self):
		_observer.unschedule(self.handler)


class RegexWatcher(QObject):
	sigCreated  = Signal(FileSystemEvent)
	sigDeleted  = Signal(FileSystemEvent)
	sigModified = Signal(FileSystemEvent)
	sigMoved    = Signal(FileSystemEvent)

	def __init__(self,
		regexes = ['.*'], ignoreRegexes = [],
		ignoreDirectories = True, caseSensitive = True,
	 	onCreated = None, onDeleted = None, onModified = None, onMoved = None):

		super().__init__()
		self.handler = RegexMatchingEventHandler(
			regexes            = regexes,
			ignore_regexes     = ignoreRegexes,
			ignore_directories = ignoreDirectories,
			case_sensitive     = caseSensitive
		)
		self.handler.on_modified = lambda e: print(e)
		if onCreated:
			self.sigCreated.connect(onCreated)
			self.handler.on_created = self.sigCreated.emit
		if onDeleted:
			self.sigDeleted.connect(onDeleted)
			self.handler.on_deleted = self.sigDeleted.emit
		if onModified:
			self.sigModified.connect(onModified)
			self.handler.on_modified = self.sigModified.emit
		if onMoved:
			self.sigMoved.connect(onMoved)
			self.handler.on_moved = self.sigMoved.emit

	def start(self, path, recursive = True):
		self.watch = _observer.schedule(self.handler, path, recursive)
		_observer.start()

	def stop(self):
		_observer.unschedule(self.watch)
		self.watch = None

def stopAllWatches():
	_observer.unschedule_all()
	_observer.stop()
