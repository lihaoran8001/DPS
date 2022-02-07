import random
import time
import _thread

# author: Haoran
class Process:
	pid = 0  # process id
	lclock = dict()  # local clock, use dictonary as vector
	enum = 0  # event number
	stat = 0  # process status

	def __init__(self, pid, enum):
		self.pid = pid
		self.enum = enum
		self.lclock = {self.pid:0}
		self.stat = 1  # activate process

	def run(self):
		event_counter = 0
		while event_counter < self.enum:
			self.execute_event()
			time.sleep(random.randint(0,5))
			event_counter += 1
		self.stat = 0  # deactivate process
		print('Process', self.pid, 'over')

	def execute_event(self):
		event_list = [self.execute_local_event, self.send]
		random.choice(event_list)()

	def execute_local_event(self):
		self.lclock[self.pid] += 1
		c1 = self.lclock.get(1, 0)
		c2 = self.lclock.get(2, 0)
		print('Process',self.pid, '(', c1, c2, ') executed a local event')
		

	def send(self):
		global p_list
		while len(p_list) > 1:
			target = random.choice(p_list)
			if target != self:
				break
		if target.stat == 0:
			self.execute_event()
		else:
			self.lclock[self.pid] += 1
			msg = 'sending...'
			c1 = self.lclock.get(1, 0)
			c2 = self.lclock.get(2, 0)
			print('Process', self.pid, '(', c1, c2, '): send to', target.pid)
			target.receive(msg, self.lclock[self.pid], self.pid)  # call the target's receive func to simulate sending

	def receive(self, msg, clock, s_pid):
		self.lclock[self.pid] += 1
		self.lclock[s_pid] = clock
		c1 = self.lclock.get(1, 0)
		c2 = self.lclock.get(2, 0)
		print('Process', self.pid, '(', c1, c2, '): recive from', s_pid)
		
def run_process(p):
	p.run()

p1 = Process(1, 5)
p2 = Process(2, 6)
p_list = [p1, p2]

try:
   _thread.start_new_thread(run_process, (p1, ))
   _thread.start_new_thread(run_process, (p2, ))
except e:
   print(e)
 
while True:
   pass
