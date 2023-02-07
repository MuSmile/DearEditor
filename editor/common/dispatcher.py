from PySide6.QtCore import QObject, Signal
from editor.common.logger import warn

class _Dispatcher(QObject):
	sig = Signal(str, object, object)
	
	def __init__(self):
		super().__init__()
		self.listenerTable = {}
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
		if msg in self.listenerTable:
			listenerList = self.listenerTable[msg]
			if listener not in listenerList:
				listenerList.append(listener)
			else:
				warn(f'connect skiped, already connected on signal \'{msg}\'')
		else:
			self.listenerTable[msg] = [listener]

	def disconnectSignal(self, msg, listener):
		if msg in self.listenerTable:
			listenerList = self.listenerTable[msg]
			if listener in listenerList:
				listenerList.remove(listener)
				if len(listenerList) == 0:
					del self.listenerTable[msg]
				return
		warn(f'disconnect skiped, never connected on signal \'{msg}\'')

	def emitSignal(self, msg, data = None, sender = None):
		self.sig.emit(msg, data, sender)

	def clear(self):
		self.listenerTable = {}

dispatcher = _Dispatcher()


if __name__ == '__main__':
	listener = lambda data, sender: print(data, sender)
	dispatcher.disconnectSignal('test', listener)
	dispatcher.connectSignal('test', listener)
	dispatcher.connectSignal('test', listener)
	dispatcher.disconnectSignal('test', listener)
	dispatcher.connectSignal('test', listener)
	dispatcher.emitSignal('foo', 'data', 1)
	dispatcher.emitSignal('test', 'data', 1)
