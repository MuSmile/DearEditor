from PySide6.QtCore import QThread, Signal


class Pipeline(QThread):
	progressChanged = Signal(str, float)

	def __init__(self, *phases):
		super().__init__()
		self.phases = phases
		self.taskTable = {}

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

	def dumpPipeline(self):
		print(f'phases: {self.phases}')
		print('----------------------------------')
		for phase in self.phases:
			print(f'phase_{phase}:')
			if phase not in self.taskTable:
				print('\t\t<NONE>')
			else:
				phaseList = self.taskTable[ phase ]
				phaseList.sort(key = lambda t: t['priority'])
				for task in phaseList: print('\t\t{:<12} : {}'.format(task["description"], task['priority']))
			print('----------------------------------')

	def setTaskProgress(self, progress):
		globalProgress = (self.passedProgress + self.taskProgress * progress) / self.phasProgress
		self.progressChanged.emit(self.phase, globalProgress)

	def run(self):
		for self.phase in self.phases:
			if self.phase not in self.taskTable: continue
			phaseList = self.taskTable[ self.phase ]
			phaseList.sort(key = lambda t: t['priority'])
			self.phasProgress = sum([t['progress'] for t in phaseList])
			self.progressChanged.emit(self.phase, 0)
			self.passedProgress = 0
			for task in phaseList:
				callback = task['callback']
				argcount = callback.__code__.co_argcount
				assert(argcount <= 2)
				self.taskProgress = task['progress']
				if argcount == 0:
					callback()
				elif argcount == 1:
					callback(self)
				elif argcount == 2:
					callback(self, self.data)
				self.passedProgress += self.taskProgress
				self.progressChanged.emit(self.phase, self.passedProgress / self.phasProgress)

	def start(self, **kwargs):
		self.data = kwargs
		super().start()



#####################  TEST  #####################
if __name__ == '__main__':
	import sys, time
	from PySide6.QtWidgets import *
	
	app = QApplication(sys.argv)
	win = QWidget()
	win.show()

	label = QLabel('foobar', win)
	label.move(200, 180)
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
			time.sleep(0.04)
	def task2(pipeline, data):
		for x in range(20):
			print(f'{data["a"]} {x}')
			pipeline.setTaskProgress(x / 20)
			time.sleep(0.02)


	p = Pipeline('pre', 'main', 'post')
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
	p.dumpPipeline()
	p.start(a = 'hello')

	sys.exit(app.exec())
