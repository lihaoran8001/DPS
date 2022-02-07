import random
import time
import _thread

class Process:
	pid = 0  # process id
	lclock = 0  # local clock
	enum = 0  # event number
	stat = 0  # process status

	def __init__(self, pid, enum):
		self.pid = pid
		self.enum = enum
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
		self.lclock += 1
		print('Process',self.pid, '(', self.lclock, ') executed a local event')
		

	def send(self):
		global p_list
		while len(p_list) > 1:
			target = random.choice(p_list)
			if target != self:
				break
		if target.stat == 0:
			self.execute_event()
		else:
			self.lclock += 1
			msg = 'sending...'
			print('Process', self.pid, '(', self.lclock, '): send to', target.pid)
			target.receive(msg, self.lclock, self.pid)  # call the target's receive func to simulate sending

	def receive(self, msg, clock, s_pid):
		self.lclock = max(self.lclock, clock) + 1
		print('Process', self.pid, '(', self.lclock, '): recive from', s_pid)
		
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
