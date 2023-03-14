"""This module provide file watcher toolkit.

Whole module is built on a python package named `watchdog <https://github.com/gorakhargosh/watchdog>`_.
"""

from PySide6.QtCore import QObject, Signal

from watchdog.observers import Observer
from watchdog.events import FileSystemEvent, PatternMatchingEventHandler, RegexMatchingEventHandler, LoggingEventHandler

_observer = Observer()

class PatternWatcher(QObject):
	"""Watch files match given patterns.
	"""
	sigCreated  = Signal(FileSystemEvent)
	"""PySide6.QtCore.Signal(FileSystemEvent): Signal when a file or directory is created."""
	sigDeleted  = Signal(FileSystemEvent)
	"""PySide6.QtCore.Signal(FileSystemEvent): Signal when a file or directory is deleted."""
	sigModified = Signal(FileSystemEvent)
	"""PySide6.QtCore.Signal(FileSystemEvent): Signal when a file or directory is modified."""
	sigMoved    = Signal(FileSystemEvent)
	"""PySide6.QtCore.Signal(FileSystemEvent): Signal when a file or directory is moved or renamed."""

	def __init__(self,
		patterns = None, ignorePatterns = None,
		ignoreDirectories = True, caseSensitive = True,
	 	onCreated = None, onDeleted = None, onModified = None, onMoved = None):
		"""
		Args:
			list[str] patterns: Patterns to allow matching event paths.
			list[str] ignorePatterns: Patterns to ignore matching event paths.
			bool ignoreDirectories: ``True`` if directories should be ignored; ``False`` otherwise.
			bool caseSensitive: ``True`` if path names should be matched sensitive to case; ``False`` otherwise.
			function onCreated: Called when a file or directory is created.
			function onDeleted: Called when a file or directory is deleted.
			function onModified: Called when a file or directory is modified.
			function onMoved: Called when a file or directory is moved or renamed.
		"""

		super().__init__()
		self.handler = PatternMatchingEventHandler(
			patterns           = patterns,
			ignore_patterns    = ignorePatterns,
			ignore_directories = ignoreDirectories,
			case_sensitive     = caseSensitive
		)
		"""PatternMatchingEventHandler: Internal ``PatternMatchingEventHandler`` instance."""
		
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
		"""Schedules watching a path and calls appropriate methods specified in the given event handler in response to file system events.
		
		Args:
			str path: Directory path that will be monitored.
			bool recursive: ``True`` if events will be emitted for sub-directories traversed recursively; ``False`` otherwise.
		"""
		_observer.schedule(self.handler, path, recursive)
		_observer.start()

	def stop(self):
		"""Unschedules this watch.
		"""
		_observer.unschedule(self.handler)


class RegexWatcher(QObject):
	"""Watch files match given regexes.
	"""

	sigCreated  = Signal(FileSystemEvent)
	"""PySide6.QtCore.Signal(FileSystemEvent): Signal when a file or directory is created."""
	sigDeleted  = Signal(FileSystemEvent)
	"""PySide6.QtCore.Signal(FileSystemEvent): Signal when a file or directory is deleted."""
	sigModified = Signal(FileSystemEvent)
	"""PySide6.QtCore.Signal(FileSystemEvent): Signal when a file or directory is modified."""
	sigMoved    = Signal(FileSystemEvent)
	"""PySide6.QtCore.Signal(FileSystemEvent): Signal when a file or directory is moved or renamed."""

	def __init__(self,
		regexes = ['.*'], ignoreRegexes = [],
		ignoreDirectories = True, caseSensitive = True,
	 	onCreated = None, onDeleted = None, onModified = None, onMoved = None):
		"""
		Args:
			list[str] regexes: Regexes to allow matching event paths.
			list[str] ignoreRegexes: Regexes to ignore matching event paths.
			bool ignoreDirectories: ``True`` if directories should be ignored; ``False`` otherwise.
			bool caseSensitive: ``True`` if path names should be matched sensitive to case; ``False`` otherwise.
			function onCreated: Called when a file or directory is created.
			function onDeleted: Called when a file or directory is deleted.
			function onModified: Called when a file or directory is modified.
			function onMoved: Called when a file or directory is moved or renamed.
		"""

		super().__init__()
		self.handler = RegexMatchingEventHandler(
			regexes            = regexes,
			ignore_regexes     = ignoreRegexes,
			ignore_directories = ignoreDirectories,
			case_sensitive     = caseSensitive
		)
		"""RegexMatchingEventHandler: Internal ``RegexMatchingEventHandler`` instance."""

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
		"""Schedules watching a path and calls appropriate methods specified in the given event handler in response to file system events.
		
		Args:
			str path: Directory path that will be monitored.
			bool recursive: ``True`` if events will be emitted for sub-directories traversed recursively; ``False`` otherwise.
		"""
		self.watch = _observer.schedule(self.handler, path, recursive)
		_observer.start()

	def stop(self):
		"""Unschedules this watch.
		"""
		_observer.unschedule(self.watch)
		self.watch = None

def stopAllWatches():
	"""Unschedules all watches and detaches all associated event handlers.
	"""
	_observer.unschedule_all()
	_observer.stop()
