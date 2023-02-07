import app
import thenewui as ui
import localeInfo
import wndMgr

class MaintenanceBoard(ui.ScriptWindow):

	def __init__(self):
		ui.ScriptWindow.__init__(self)

		self.timeEnd = 0
		self.duration = 0

		self.LoadWindow()
		
		# if app.ENABLE_WINDOW_SLIDE_EFFECT:
			# self.EnableSlidingEffect()

	def __del__(self):
		ui.ScriptWindow.__del__(self)

	def Destroy(self):
		self.Close()

	def LoadWindow(self):
		try:
			pyScrLoader = ui.PythonScriptLoader()
			pyScrLoader.LoadScriptFile(self, "UIScript/MaintenanceWindow.py")
		except:
			import exception
			exception.Abort("MaintenanceBoard.LoadDialog.LoadScript")

		try:
			GetObject=self.GetChild
			self.board = GetObject("board")
			self.desc = GetObject("desc")

		except:
			import exception
			exception.Abort("MaintenanceBoard.LoadDialog.BindObject")

		# self.board.HideCorners(ui.ThinBoard.LT)
		# self.board.HideCorners(ui.ThinBoard.RT)
		# self.board.HideLine(ui.ThinBoard.T)

	def Open(self, timeLeft, duration):
		self.timeEnd = app.GetTime() + timeLeft
		self.duration = duration
		self.Refresh(TRUE)
		self.Show()

	def Close(self):
		self.Hide()

	def Refresh(self, new_size = FALSE):
		self.desc.SetText(localeInfo.MAINTENANCE_DESCRIPTION % (localeInfo.NewFormatTime(max(0, int(self.timeEnd - app.GetTime())), True, True, True, True, True), localeInfo.NewFormatTime(self.duration, True, True, True, True, True)))

		if new_size == TRUE or self.desc.GetWidth() + 30 > self.GetWidth():
			self.SetSize(self.desc.GetWidth() + 30, self.GetHeight())
			self.board.SetSize(self.GetWidth(), self.GetHeight())
			self.SetPosition((wndMgr.GetScreenWidth() - self.GetWidth()) / 2, 75)
			self.desc.UpdateRect()

	def OnUpdate(self):
		self.Refresh()
