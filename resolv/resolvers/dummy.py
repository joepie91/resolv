from resolv.shared import Task

class DummyTask(Task):
	result_type = "dummy"
	
	def run(self):
		self.results = {'dummy': self.url}
		self.state = "finished"
		return self
