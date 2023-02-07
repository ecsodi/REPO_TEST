import gc
from threading import Timer


class LoopTimer:
	__timer = None
	
	def __init__(self, interval, runnable, *args):
		self.__timer = LoopTimer.__LoopTimer(interval, runnable, *args)
	
	def __del__(self):
		LoopTimer.__LoopTimer.__del__(self.__timer)
	
	def Start(self):
		if not self.IsRunning():
			self.__timer.Start()
	
	def Stop(self):
		if self.IsRunning():
			self.__timer.Stop()
	
	def IsRunning(self):
		return self.__timer.IsRunning()
	
	
	class __LoopTimer:
		__interval = None
		__runnable = None
		__args = None
		
		__timer = None
		__isAlive = None
		
		def __init__(self, interval, runnable, *args):
			self.__interval = interval
			self.__runnable = runnable
			self.__args = args
			
			self.Stop()
		
		def __del__(self):
			self.Stop()
		
		def __Run(self):
			if self.__isAlive:
				self.__runnable(*self.__args)
				self.__StartNewTimer()
		
		def __StartNewTimer(self):
			self.__ClearTimer()
			
			self.__timer = Timer(self.__interval, self.__Run)
			self.__timer.setDaemon(True)
			self.__timer.start()
		
		def __ClearTimer(self):
			if self.__timer:
				self.__timer.cancel()
				self.__timer = None
				gc.collect()
		
		def Start(self):
			if not self.IsRunning():
				self.__isAlive = True
				self.__StartNewTimer()
		
		def Stop(self):
			if self.IsRunning():
				self.__isAlive = False
			
			self.__ClearTimer()
		
		def IsRunning(self):
			return self.__isAlive