"""This module provides global signal toolkit.

Typical usage example:

.. code-block:: python
   :linenos:

   from editor.common.dispatcher import dispatcher

   def listener1(): print(f'listener1')
   def listener2(data): print(f'listener2: {data}')
   def listener3(data, sender): print(f'listener3: {data}, {sender}')

   dispatcher.connectSignal('foo', listener1)
   dispatcher.connectSignal('foo', listener2)
   dispatcher.disconnectSignal('foo', listener2)
   dispatcher.connectSignal('bar', listener2)
   dispatcher.connectSignal('bar', listener3)

   sender = 1 # can be any type, sender is just a general identity
   dispatcher.emitSignal('foo', 'test_data', sender)
   dispatcher.emitSignal('bar', 'test_data', sender)
"""

from PySide6.QtCore import QObject, Signal
from editor.common.logger import warn

class Dispatcher(QObject):
	"""Handle general global signal stuff.

	In most situation, this ``Dispatcher`` class do not need be instanced by user.
	The built-in ``dispatcher`` instance is fully meet the needs.
	"""

	sig = Signal(str, object, object)
	"""`PySide6.QtCore.Signal(str, any, any)`_: A qt signal attribute, all functions are built on this.

	.. _PySide6.QtCore.Signal(str, any, any): https://doc.qt.io/qtforpython/PySide6/QtCore/Signal.html"""
	
	def __init__(self):
		super().__init__()
		
		self.listenerTable = {}
		"""dict[str, list[function]]: All connected listerners table."""
		
		self.sig.connect(self._onSignal)

	def _onSignal(self, msg, data, sender):
		if msg in self.listenerTable:
			listenerList = self.listenerTable[ msg ]
			for listener in listenerList:
				argcount = listener.__code__.co_argcount
				if argcount == 0:
					listener()
				elif argcount == 1:
					listener(data)
				elif argcount == 2:
					listener(data, sender)
				else:
					raise Exception('signal listener argument count can not larger than 2')
		else:
			warn(f'signal \'{msg}\' has no listener connected!')

	def connectSignal(self, msg, listener):
		"""Register a listenter of certain message.
		
		Args:
			str msg: Message to listener.
			function listener: Called when listenered message emitted.
		"""
		if msg in self.listenerTable:
			listenerList = self.listenerTable[msg]
			if listener not in listenerList:
				listenerList.append(listener)
			else:
				warn(f'connect skiped, already connected on signal \'{msg}\'')
		else:
			self.listenerTable[msg] = [listener]

	def disconnectSignal(self, msg, listener):
		"""Unregister a listenter of certain message.
		
		Args:
			str msg: Message to remove from.
			function listener: Listener to remove.
		"""
		if msg in self.listenerTable:
			listenerList = self.listenerTable[msg]
			if listener in listenerList:
				listenerList.remove(listener)
				if len(listenerList) == 0:
					del self.listenerTable[msg]
				return
		warn(f'disconnect skiped, never connected on signal \'{msg}\'')

	def emitSignal(self, msg, data = None, sender = None):
		"""Emit a sinal, will trigger all registered listeners.
		
		Args:
			str msg: Message to emit.
			any data: Data to emit with.
			any sender: Indicate emit's sender.
		"""
		self.sig.emit(msg, data, sender)

	def clear(self):
		"""Clear all listeners of all messages."""
		self.listenerTable = {}

dispatcher = Dispatcher()
"""Dispatcher: Built-in ``Dispatcher`` instance."""
