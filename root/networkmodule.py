import app
import Collision as chr
import dbg
import net
import ShapeSkin as chrmgr
import background
import CacheEffect as player
import playersettingmodule
import thenewui as ui
import uiPhaseCurtain

import localeInfo
import constInfo

class PopupDialog(ui.ScriptWindow):

	def __init__(self):
		ui.ScriptWindow.__init__(self)
		self.CloseEvent = 0
		self.WaitTime = 0
		self.bCanExit = True
		self.AcceptButton = None
		self.wndTime = None

	def __del__(self):
		ui.ScriptWindow.__del__(self)

	def LoadDialog(self):
		PythonScriptLoader = ui.PythonScriptLoader()
		PythonScriptLoader.LoadScriptFile(self, "UIScript/PopupDialog.py")
	
	def SetWait(self, time):
		self.WaitTime = time
		self.bCanExit = False
	
	def Open(self, Message, event = 0, ButtonName = localeInfo.UI_CANCEL):

		if True == self.IsShow():
			self.Close()

		self.Lock()
		self.SetTop()
		self.CloseEvent = event

		AcceptButton = self.GetChild("accept")
		AcceptButton.SetText(ButtonName)
		AcceptButton.SetEvent(ui.__mem_func__(self.Close))
		self.AcceptButton = AcceptButton

		self.GetChild("message").SetText(Message)
		self.wndTime = self.GetChild("Time")
		self.wndTime.Hide()
		
		self.Show()
	
	def OnRender(self):
		if self.bCanExit:
			return

		if app.GetGlobalTimeStamp() > self.WaitTime:
			if self.AcceptButton and self.wndTime:
				self.AcceptButton.Show()
				self.wndTime.Hide()
				self.bCanExit = True
			
		else:
			if self.AcceptButton and self.wndTime:
				self.AcceptButton.Hide()
				
				timeTxt = localeInfo.SecondToDHM(self.WaitTime - app.GetGlobalTimeStamp() + 1)
				self.wndTime.SetText(str(timeTxt))
				self.wndTime.Show()

	def Close(self):

		if False == self.IsShow():
			self.CloseEvent = 0
			return

		self.Unlock()
		self.Hide()

		if 0 != self.CloseEvent:
			try: # @ Grimm pass TYPE ERROR : 'str' object is not callable
				self.CloseEvent()
			except Exception:
				self.CloseEvent = 0

			self.CloseEvent = 0

	def Destroy(self):
		self.Close()
		self.ClearDictionary()

	def OnPressEscapeKey(self):
		if self.bCanExit:
			self.Close()
		return True

	def OnIMEReturn(self):
		if self.bCanExit:
			self.Close()
		return True

class MainStream(object):
	isChrData=0

	def __init__(self):
		net.SetHandler(self)
		net.SetTCPRecvBufferSize(128*1024)
		net.SetTCPSendBufferSize(4096)
		net.SetUDPRecvBufferSize(4096)

		self.id=""
		self.pwd=""
		self.addr=""
		self.port=0
		self.account_addr=0
		self.account_port=0
		self.slot=0
		self.isAutoSelect=0
		self.isAutoLogin=0

		self.curtain = 0
		self.curPhaseWindow = 0
		self.newPhaseWindow = 0

	def __del__(self):
		import uiQuest
		if uiQuest.QuestDialog:
			if uiQuest.QuestDialog.__dict__.has_key("QuestCurtain"):
				del uiQuest.QuestDialog.QuestCurtain

	def Destroy(self):
		if self.curPhaseWindow:
			self.curPhaseWindow.Close()
			self.curPhaseWindow = 0

		if self.newPhaseWindow:
			self.newPhaseWindow.Close()
			self.newPhaseWindow = 0

		self.popupWindow.Destroy()
		self.popupWindow = 0

		self.curtain = 0

	def Create(self):
		self.CreatePopupDialog()

		self.curtain = uiPhaseCurtain.PhaseCurtain()

	def SetPhaseWindow(self, newPhaseWindow):
		if self.newPhaseWindow:
			self.__ChangePhaseWindow()

		self.newPhaseWindow=newPhaseWindow

		if self.curPhaseWindow:
			self.curtain.FadeOut(self.__ChangePhaseWindow)
		else:
			self.__ChangePhaseWindow()

	def __ChangePhaseWindow(self):
		oldPhaseWindow=self.curPhaseWindow
		newPhaseWindow=self.newPhaseWindow
		self.curPhaseWindow=0
		self.newPhaseWindow=0

		if constInfo.DETECT_LEAKING_WINDOWS:
			#dbg.LogBox("total window obj count: "+ str(constInfo.WINDOW_TOTAL_OBJ_COUNT))
			import game, gc, os
			if isinstance(newPhaseWindow, game.GameWindow): #going from something else (introloading) to gameWindow
				constInfo.WINDOW_COUNT_OBJ = False # stop object counting while we removing the old phase window
				if oldPhaseWindow:
					oldPhaseWindow.Close() 
				del oldPhaseWindow # try to remove the old phasewindow
				gc.collect() # force garbage collector to remove 0 referenced object
				constInfo.WINDOW_COUNT_OBJ = True # start counting window objects

			elif isinstance(oldPhaseWindow, game.GameWindow): # from gamewindow to something else (intrologin, introselect, introloading)
				constInfo.WINDOW_COUNT_OBJ = True # start counting window objects
				if oldPhaseWindow:
					oldPhaseWindow.Close()
				del oldPhaseWindow # try to remove old gamewindow
				gc.collect() # force garbage collector to collect 0 referenced objects
				constInfo.WINDOW_COUNT_OBJ = False # stop counting window objects
				if constInfo.WINDOW_OBJ_COUNT > 3: # there are static classes, whose are allocated only once on the first login, like the candidatewindow
					# file saving stuff
					dbg.LogBox("!ATTENTION! WINDOW_MEMORY_LEAK DETECTED\n LEAKING WINDOW COUNT: "+ str(constInfo.WINDOW_OBJ_COUNT))
					if not os.path.isdir("memory_leak"):
						os.mkdir("memory_leak")
					leakReport = 0
					while os.path.isfile("memory_leak/window_memory_leak%i.txt" % leakReport):
						leakReport += 1
					opFile = open("memory_leak/window_memory_leak%i.txt"%leakReport, "w+")
					opRootFile = open("memory_leak/window_memory_leak_root%i.txt"%leakReport, "w+")
					for i, v in constInfo.WINDOW_OBJ_LIST.iteritems():
						opFile.write(v.typeStr + " parent type: " + v.strParent + "\n")
						for j in v.traceBack:
							opFile.write("\t" + j + "\n")
						if v.strParent == "":
							opRootFile.write(v.typeStr + "\n")
					opRootFile.flush()
					opRootFile.close()
					opFile.flush()
					opFile.close()

			else:
				if oldPhaseWindow:
					oldPhaseWindow.Close()

		else:
			if oldPhaseWindow:
				oldPhaseWindow.Close()

		# if oldPhaseWindow:
			# oldPhaseWindow.Close()

		if newPhaseWindow:
			newPhaseWindow.Open()

		self.curPhaseWindow=newPhaseWindow

		if self.curPhaseWindow:
			self.curtain.FadeIn()
		else:
			app.Exit()

	def CreatePopupDialog(self):
		self.popupWindow = PopupDialog()
		self.popupWindow.LoadDialog()
		self.popupWindow.SetCenterPosition()
		self.popupWindow.Hide()

	def SetLogoPhase(self):
		net.Disconnect()

		import introLogo
		self.SetPhaseWindow(introLogo.LogoWindow(self))

	def SetLoginPhase(self):
		net.Disconnect()

		import introLogin
		self.SetPhaseWindow(introLogin.LoginWindow(self))

	def SetSelectEmpirePhase(self):
		try:
			import introEmpire
			self.SetPhaseWindow(introEmpire.SelectEmpireWindow(self))
		except:
			import exception
			exception.Abort("networkModule.SetSelectEmpirePhase")


	def SetReselectEmpirePhase(self):
		try:
			import introEmpire
			self.SetPhaseWindow(introEmpire.ReselectEmpireWindow(self))
		except:
			import exception
			exception.Abort("networkModule.SetReselectEmpirePhase")

	def SetSelectCharacterPhase(self):
		try:
			localeInfo.LoadLocaleData()
			import introSelect
			self.popupWindow.Close()
			self.SetPhaseWindow(introSelect.SelectCharacterWindow(self))
		except:
			import exception
			exception.Abort("networkModule.SetSelectCharacterPhase")

	def SetCreateCharacterPhase(self):
		try:
			import introCreate
			self.SetPhaseWindow(introCreate.CreateCharacterWindow(self))
		except:
			import exception
			exception.Abort("networkModule.SetCreateCharacterPhase")

	def SetLoadingPhase(self):
		try:
			import introLoading
			self.SetPhaseWindow(introLoading.LoadingWindow(self))
		except:
			import exception
			exception.Abort("networkModule.SetLoadingPhase")

	def SetGamePhase(self):
		try:
			import game
			self.popupWindow.Close()

			if constInfo.DETECT_LEAKING_WINDOWS: # reset leaking window list since the last teleport
				constInfo.WINDOW_COUNT_OBJ = True
				constInfo.WINDOW_OBJ_COUNT = 0
				constInfo.WINDOW_OBJ_LIST = {}
			
			self.SetPhaseWindow(game.GameWindow(self))
		except:
			raise
			import exception
			exception.Abort("networkModule.SetGamePhase")

		if constInfo.DETECT_LEAKING_WINDOWS:
			constInfo.WINDOW_COUNT_OBJ = False

	def Connect(self):
		import constInfo
		if constInfo.KEEP_ACCOUNT_CONNETION_ENABLE:
			net.ConnectToAccountServer(self.addr, self.port, self.account_addr, self.account_port)
		else:
			net.ConnectTCP(self.addr, self.port)

	def SetConnectInfo(self, addr, port, account_addr=0, account_port=0):
		self.addr = addr
		self.port = port
		self.account_addr = account_addr
		self.account_port = account_port

	def GetConnectAddr(self):
		return self.addr

	def SetLoginInfo(self, id, pwd):
		self.id = id
		self.pwd = pwd
		net.SetLoginInfo(id, pwd)

	def CancelEnterGame(self):
		pass

	def SetCharacterSlot(self, slot):
		self.slot=slot

	def GetCharacterSlot(self):
		return self.slot

	def EmptyFunction(self):
		pass
