import ui
import dbg
import app
import chr
import net
import wndMgr
import imp
import thread
import time
import grp
import ntpath

class PythonLiveWindow(ui.ScriptWindow):

	def __init__(self):
		ui.ScriptWindow.__init__(self)
		self.file = "C:/Users/Andi-Gabriel/Desktop/minecraft/Client/root/uichestview.py"
		self.module_name ='ChestViewWindow'
		
		self.last_update = app.GetFileDifference(self.file)
		self.window = imp.load_source(self.module_name, self.file)
		self.class_ = getattr(self.window, self.module_name)()
		self.class_.Hide()
		
		self.isLoaded = 0
		self.LoadButtons()

	def __del__(self):
		ui.ScriptWindow.__del__(self)
		
		if self.board:
			del self.board
			
		if self.Button1:
			del self.Button1

	def LoadButtons(self):
		if self.isLoaded == 1:
			return
		self.isLoaded = 1

		self.board = ui.MakeBoardWithTitleBar(None, "", "Python Inject", self.Close, 350, 200)
		self.board.AddFlag('movable')
		self.board.AddFlag('float')
		self.board.Hide()
		
		self.Slot1 = ui.MakeSlotBar(self.board, 15, 35, 280, 15)
		self.Slot2 = ui.MakeSlotBar(self.board, 15, 35+35, 280, 15)

		self.wndNameFile = self.CreateEditLine(190, 280, 15+15, 3, 2, self.Slot1)
		self.wndNameWindow = self.CreateEditLine(190, 280, 15+15, 3, 2, self.Slot2)
		
		self.wndNameFile.SetText("p")
		self.wndNameWindow.SetText("C")

		self.btnReload = ui.MakeButton(self.board, 15, 35+35+45, False, "d:/ymir work/ui/game/battle_pass/buttons/", "button_reward_disabled.png", "button_reward_disabled.png", "button_reward_disabled.png")
		self.btnReload.SetEvent(ui.__mem_func__(self.Reload))
		self.btnReload.SetToolTipText("Reload")

		self.comp = Component()
		img="inject.tga"
		self.Button1 = self.comp.Button(None, "", "", 27, 90, self.OpenPanel, img, img, img)
		self.SetSize(350, 200)
			
	def OpenPanel(self):
		self.board.Show()

	def ClearList(self):
		self.class_.ClearList()
		
	def BattlePassMission(self, iType, iVnum, pCount, iCount):
		self.class_.BattlePassMission(int(iType), int(iVnum), int(pCount), int(iCount))

	def BattlePassReward(self, iType, iVnum, iVnumReward, iCountReward):
		self.class_.BattlePassMissionReward(int(iType), int(iVnum), int(iVnumReward), int(iCountReward))

	def BattlePassFinal(self, iVnum, iCount):
		self.class_.BattlePassFinal(int(iVnum), int(iCount))

	def Reload(self):
		if self.class_:
			self.class_.Destroy()
			del self.class_
			self.class_ = None
	
		self.file = "C:/Users/Andi-Gabriel/Desktop/minecraft/Client/root/" + self.wndNameFile.GetText()
		self.module_name = self.wndNameWindow.GetText()

		self.last_update = app.GetFileDifference(self.file)
		self.window = imp.load_source(self.module_name, self.file)
		self.class_ = getattr(self.window, self.module_name)()
		self.class_.Show()
			
	def Close(self):
		if self.board:
			self.board.Hide()
		if self.Button1:
			self.Button1.Hide()
		self.Hide()
		if self.class_:
			self.class_.Hide()
		
		self.board = None
		self.class_ = None
		self.Button1 = None
		self.wndNameFile = None
		self.wndNameWindow = None
		self.Slot1 = None
		self.Slot2 = None
		self.comp = None

	def CreateEditLine(self, max, size_x, size_y, x, y, parent):
		line = ui.EditLine()
		line.SetParent(parent)
		line.SetPosition(x, y)
		line.SetSize(size_x, size_y)
		line.SetMax(max)
		line.Show()
		return line

class Component:
	def Button(self, parent, buttonName, tooltipText, x, y, func, UpVisual, OverVisual, DownVisual):
		button = ui.Button()
		if parent != None:
			button.SetParent(parent)
		button.SetPosition(x, y)
		button.SetUpVisual(UpVisual)
		button.SetOverVisual(OverVisual)
		button.SetDownVisual(DownVisual)
		button.SetText(buttonName)
		button.SetToolTipText(tooltipText)
		button.Show()
		button.SetEvent(func)
		return button
