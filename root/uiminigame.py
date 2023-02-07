import thenewui as ui
import uiScriptLocale
import wndMgr
import CacheEffect as player
import localeInfo
import net
import app
import constInfo

class MiniGameWindow(ui.Window):
	def __init__(self):
		ui.Window.__init__(self)
		self.wndInterface = None
		self.InitializeWindow()
		
	def __del__(self):
		ui.Window.__del__(self)
	
	def Close(self):
		self.Hide()
	
	def Destroy(self):
		self.wndInterface = None

	def InitializeWindow(self):
		self.SetPosition(wndMgr.GetScreenWidth() - 155, 100)
		self.SetSize(58, 38)
		self.Show()

		self.eventBennerButton = ui.Button()
		self.eventBennerButton.SetParent(self)
		self.eventBennerButton.SetPosition(0, 0)
		self.eventBennerButton.SetUpVisual("d:/ymir work/ui/game/battle_pass/event_button_normal.png")
		self.eventBennerButton.SetOverVisual("d:/ymir work/ui/game/battle_pass/event_button_hover.png")
		self.eventBennerButton.SetDownVisual("d:/ymir work/ui/game/battle_pass/event_button_down.png")
		self.eventBennerButton.SetEvent(ui.__mem_func__(self.OpenBattlePass))
		self.eventBennerButton.Show()
		
	def BindInterface(self, interface):
		self.wndInterface = interface
		
	def ShowMiniGameDialog(self):
		if self.eventBennerButton:
			self.eventBennerButton.Show()

	def HideMiniGameDialog(self):
		if self.eventBennerButton.IsShow():
			self.eventBennerButton.Hide()
		
	def OpenBattlePass(self):
		if self.wndInterface:
			self.wndInterface.OpenBattlePass()
			net.SendChatPacket("/battle_pass r")

