from PySide6.QtCore import QThread, Signal


class Pipeline(QThread):
	progressChanged = Signal(str, float)
	completed = Signal()

	def __init__(self):
		super().__init__()
		self.taskTable = {}
		self.targetTable = {}
		self.context = {}

	def registerTask(self, callback, phase, priority = None, progress = 1, description = None):
		if phase not in self.taskTable: self.taskTable[ phase ] = []
		phaseList = self.taskTable[ phase ]
		if priority == None:
			if len(phaseList) == 0:
				priority = 0
			else:
				priority = max([t['priority'] for t in phaseList]) + 1
		if description == None: description = callback.__code__.co_name
		phaseList.append({
			'callback'    : callback,
			'priority'    : priority,
			'progress'    : progress,
			'description' : description,
		})

	def registerTarget(self, target, phases):
		assert(phases)
		self.targetTable[ target ] = phases

	def listTargets(self):
		return [b for b in self.targetTable.keys()]

	def dumpTarget(self, target):
		assert(target in self.targetTable)
		phases = self.targetTable[ target ]
		print(f'<{target}>: {phases}')
		print('----------------------------------')
		for phase in phases:
			print(f'phase_{phase}:')
			if phase not in self.taskTable:
				print('\t\t<NONE>')
			else:
				phaseList = self.taskTable[ phase ]
				phaseList.sort(key = lambda t: t['priority'])
				for task in phaseList: print('\t\t{:<12} : {}'.format(task["description"], task['priority']))
			print('----------------------------------')

	def setTaskProgress(self, progress):
		phaseProgress  = self.context['phaseProgress']
		passedProgress = self.context['passedProgress']
		taskProgress   = self.context['taskProgress']
		globalProgress = (passedProgress + taskProgress * progress) / phaseProgress
		self.progressChanged.emit(self.phase, globalProgress)

	def run(self):
		for self.phase in self.context['phases']:
			if self.phase not in self.taskTable: continue
			phaseList = self.taskTable[ self.phase ]
			phaseList.sort(key = lambda t: t['priority'])
			self.context['phaseProgress'] = sum([t['progress'] for t in phaseList])
			self.context['passedProgress'] = 0
			self.progressChanged.emit(self.phase, 0)
			for task in phaseList:
				callback = task['callback']
				argcount = callback.__code__.co_argcount
				assert(argcount <= 2)
				self.context['taskProgress'] = task['progress']
				if argcount == 0:
					callback()
				elif argcount == 1:
					callback(self)
				elif argcount == 2:
					callback(self, self.context['data'])
				self.context['passedProgress'] += self.context['taskProgress']
				self.progressChanged.emit(self.phase, self.context['passedProgress'] / self.context['phaseProgress'])
		self.context.clear()
		self.completed.emit()

	def start(self, target, **kwargs):
		assert(target in self.targetTable)
		self.context['phases'] = self.targetTable[ target ]
		self.context['data'] = kwargs
		super().start()



#####################  TEST  #####################
if __name__ == '__main__':
	import sys, time
	from PySide6.QtWidgets import *
	
	app = QApplication(sys.argv)
	win = QWidget()
	win.show()

	label = QLabel(win)
	label.setGeometry(200, 180, 400, 20)
	label.show()

	pgb = QProgressBar(win)
	pgb.setMinimum(0)
	pgb.setMaximum(1000)
	pgb.move(200, 200)
	pgb.show()


	def task1(pipeline):
		for x in range(20):
			print(x)
			pipeline.setTaskProgress(x / 20)
			time.sleep(0.02)
	def task2(pipeline, data):
		for x in range(20):
			print(f'{data["a"]} {x}')
			pipeline.setTaskProgress(x / 20)
			time.sleep(0.01)

	p = Pipeline()

	def progressChanged(phase, progress):
		label.setText(phase)
		pgb.setValue(progress * 1000)
	p.progressChanged.connect(progressChanged)

	p.registerTask(task1, 'pre', 1)
	p.registerTask(task1, 'pre', 2)
	p.registerTask(task2, 'pre', 0)
	p.registerTask(task2, 'pre')
	p.registerTask(task1, 'pre')
	p.registerTask(task2, 'pre')
	p.registerTask(task2, 'pre')
	p.registerTask(task2, 'pre')
	p.registerTask(task2, 'pre')
	p.registerTask(task2, 'main', 1, 20)
	p.registerTask(task1, 'main', 1, 80)
	p.registerTarget('test', ['pre', 'main', 'post'])
	p.dumpTarget('test')
	p.start('test', a = 'hello')

	sys.exit(app.exec())
