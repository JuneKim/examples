'''
IDLE > READY > WAIT > SHUFFLE
'''

import threading, time

class State(object):

	def __init__(self, timeout = 0):
		print('Processing current state' + str(self))
		self.timeout = timeout
		if timeout is not 0:
			self.timer = threading.Timer(timeout, self.on_event, args = ('timeout',))

	def on_event(self, event):
		if event is not 'timeout':
			self.timer.cancel()

	def run(self):
		print (self.timeout)
		if self.timeout is not 0:
			print ('timer started')
			self.timer.start()

	def __repr__(self):
		return self.__str__()
	
	def __str__(self):
		return self.__class__.__name__

class LockState(State):
	def on_event(self, event):
		if event == 'pin_matched':
			return UnlockedState(timeout = 3)

		return self

	def run(self):
		State.run(self)
		print ('lock run')

class UnlockedState(State):
	def on_event(self, event):
		State.on_event(self, event)
		if event == 'lock':
			return LockState()
		elif event == 'timeout':
			print ('timeout: it is automatically locked')
			return LockState()

		return self
	
	def run(self):
		State.run(self)
		print ('unlock run')


class SimpleDevice(object):
	def __init__(self):
		self.state = LockState(0)

	def on_event(self, event):
		self.state = self.state.on_event(event)
		self.state.run()

# for test
myDevice = SimpleDevice()
print (myDevice.state)
myDevice.on_event('pin_matched')
while True:
	time.sleep(5)
	myDevice.on_event('lock')
	time.sleep(1)
	myDevice.on_event('pin_matched')
