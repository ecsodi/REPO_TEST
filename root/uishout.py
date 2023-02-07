import ui
import chat
import net
import constInfo
import localeInfo
from _weakref import proxy
from itertools import islice

class ShoutManager(ui.ScriptWindow):

	def __init__(self):
		ui.ScriptWindow.__init__(self)
		self.board = None

		self.LoadWindow()
		
	def __del__(self):
		self.Destroy()
		ui.ScriptWindow.__del__(self)

	def LoadWindow(self):
		try:
			pyScrLoader = ui.PythonScriptLoader()
			pyScrLoader.LoadScriptFile(self, "uiscript/shout.py")
		except:
			import exception
			exception.Abort("ShoutManager.LoadDialog.LoadScript")

		try:
			GetObject=self.GetChild
			self.board = GetObject("board")
			self.startButton = GetObject("start")
			self.stopButton = GetObject("stop")
			self.clearButton = GetObject("clear")
			self.infoText = GetObject("infotext")
			self.textLine = GetObject("CommentValue")
			
			self.startButton.SetEvent(ui.__mem_func__(self.StartFunction))
			self.stopButton.SetEvent(ui.__mem_func__(self.StopFunction))
			self.clearButton.SetEvent(ui.__mem_func__(self.ClearFunction))
			
			self.board.SetCloseEvent(ui.__mem_func__(self.Close))
			
		except:
			import exception
			exception.Abort("ShoutManager.LoadDialog.BindObject")
			
	def Destroy(self):
		self.ClearDictionary()
		self.titleBar = None

	def Open(self):	
		if constInfo.auto_shout_status == 1:
			self.infoText.SetText(localeInfo.MOD_ACTIVE_MESSAGE)
		else:
			self.infoText.SetText(localeInfo.MOD_OFF_MESSAGE)
			
		self.Show()
		self.SetCenterPosition()
		
	def OnUpdate(self):
		if constInfo.auto_shout_status == 1:
			self.infoText.SetText(localeInfo.MOD_ACTIVE_MESSAGE)
		else:
			self.infoText.SetText(localeInfo.MOD_OFF_MESSAGE)
			
	def ClearFunction(self):
		self.textLine.SetText("")
		
	def StartFunction(self):
		if self.textLine.GetText() == "":
			chat.AppendChat(1, localeInfo.AUTO_MESSAGE_EMPTY)
			return
			
		constInfo.auto_shout_text = self.textLine.GetText()
		constInfo.auto_shout_status = 1
		self.startButton.Disable()
		self.clearButton.Disable()

	def StopFunction(self):
		constInfo.auto_shout_text = ""
		constInfo.auto_shout_status = 0
		self.startButton.Enable()
		self.clearButton.Enable()

	def Close(self):
		self.Hide()

	def OnPressEscapeKey(self):
		self.Close()

