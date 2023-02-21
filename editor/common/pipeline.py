

class Pipeline:
	def __init__(self, *stages):
		self.stages = stages
		self.taskTable = {}
		for s in stages: self.taskTable[ s ] = {}

	def registerTask(self, task, stage, priority = None):
		pass

	def run(self, **kwargs):
		pass

