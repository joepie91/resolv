from resolv.shared import Task

class DummyTask(Task):
	result_type = "dummy"
	
	name = "Dummy Resolver"
	author = "Sven Slootweg"
	author_url = "http://cryto.net/~joepie91"
	
	def run(self):
		self.results = {'dummy': self.url}
		self.state = "finished"
		return self
