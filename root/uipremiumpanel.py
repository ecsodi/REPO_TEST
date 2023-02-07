import uiCommon
import app
import wndMgr
import net 
import player 
import ui 
import uiToolTip 
import background 
import uiScriptLocale
import constInfo
import localeInfo
import chat
import cfg
import item
import uiAffectShower
import grp
from _weakref import proxy
import Collision as chr

COLOR_BAR_FALSE = grp.GenerateColor(1.0, 0.0, 0.1, 0.2)
COLOR_BAR_TRUE = grp.GenerateColor(0.0, 1.0, 0.1, 0.2)
COLOR_BAR_BROWN = grp.GenerateColor(0.690,0.282,0.157, 0.2)
COLOR_BAR_SILVER = grp.GenerateColor(0.655,0.643,0.643, 0.2)
COLOR_BAR_YELLOW = grp.GenerateColor(0.976,0.863,0.224,0.2)
COLOR_BAR_GREEN = grp.GenerateColor(0.9, 0.4745, 0.4627, 0.2)
COLOR_BAR_RED = grp.GenerateColor(0.5411, 0.7254, 0.5568, 0.2)
BOARD_WIDTH = 265
BOARD_HEIGHT = 255

class PremiumWindow(ui.ScriptWindow):

	def __init__(self):
		self.bLoadedInfo = False	
		ui.ScriptWindow.__init__(self)
		self.isLoaded = 0
		self.interface = None
		self.IsHidden = True
		self.IsHiddenFromButtons = False
		self.arg = 0

		self.__LoadWindow()
		
	def __del__(self):
		ui.ScriptWindow.__del__(self)
		
	def __LoadWindow(self):
		if self.isLoaded == 1:
			return

		self.isLoaded = 1
		
		self.AddFlag("float")
		self.AddFlag("movable")
		self.AddFlag("animation")
		
		self.Board = ui.BoardWithTitleBar()
		self.Board.SetParent(self)
		self.Board.SetPosition(0, 0)
		self.Board.SetSize(BOARD_WIDTH, BOARD_HEIGHT)
		self.Board.AddFlag("not_pick")
		self.Board.SetTitleName("Panou caracter")
		self.Board.SetCloseEvent(ui.__mem_func__(self.Close))
		self.Board.Show()

		self.InfoBorder = ui.BorderA()
		self.InfoBorder.SetParent(self.Board)
		self.InfoBorder.SetSize(BOARD_WIDTH - 20, BOARD_HEIGHT - 40)
		self.InfoBorder.SetPosition(10,30)
		self.InfoBorder.Show()
		
		self.FacilityWindow = ui.Window()
		self.FacilityWindow.SetParent(self.InfoBorder)
		self.FacilityWindow.SetSize(BOARD_WIDTH - 20, BOARD_HEIGHT - 30)
		self.FacilityWindow.SetPosition(0,0)
		self.FacilityWindow.Hide()

		self.ButtonsWindow = ui.Window()
		self.ButtonsWindow.SetParent(self.InfoBorder)
		self.ButtonsWindow.SetSize(BOARD_WIDTH - 20, BOARD_HEIGHT - 30)
		self.ButtonsWindow.SetPosition(0,0)
		self.ButtonsWindow.Show()
		
		self.arg = player.IsPremiumUser()

		self.BuildInterface()
		self.HideFacilityBoard()
		
		self.SetSize(self.Board.GetWidth(), self.Board.GetHeight())
		
	def BuildInterface(self):
		self.ImageSlot = ui.ImageBox()
		self.ImageSlot.SetParent(self.InfoBorder)
		self.ImageSlot.LoadImage("d:/ymir work/ui/public/yang_slot.png")
		self.ImageSlot.SetPosition(115,5)
		self.ImageSlot.SetScale(1.0, 1.2)
		self.ImageSlot.Show()

		self.premiumStatus = ui.MakeTextV3(self.ImageSlot, "", 5, 2, False)

		self.ImageSlotV2 = ui.ImageBox()
		self.ImageSlotV2.SetParent(self.InfoBorder)
		self.ImageSlotV2.LoadImage("d:/ymir work/ui/public/yang_slot.png")
		self.ImageSlotV2.SetPosition(5,28)
		self.ImageSlotV2.SetScale(1.958, 1.2)
		self.ImageSlotV2.Show()
		
		self.CharSlot = ui.ImageBox()
		self.CharSlot.SetParent(self.InfoBorder)
		self.CharSlot.LoadImage("d:/ymir work/ui/public/yang_slot.png")
		self.CharSlot.SetPosition(5,5)
		self.CharSlot.SetScale(0.81, 1.2)
		self.CharSlot.Show()
		
		self.ShowPriv = ui.ToggleButton()
		self.ShowPriv.SetParent(self.ImageSlotV2)
		self.ShowPriv.SetPosition(BOARD_WIDTH - 48, 1)
		self.ShowPriv.SetToggleDownEvent(ui.__mem_func__(self.ShowFacilityBoard))
		self.ShowPriv.SetToggleUpEvent(ui.__mem_func__(self.HideFacilityBoard))
		self.ShowPriv.SetUpVisual("d:/ymir work/ui/public/scrollbar_thin_down_button_01.sub")
		self.ShowPriv.SetOverVisual("d:/ymir work/ui/public/scrollbar_thin_down_button_02.sub")
		self.ShowPriv.SetDownVisual("d:/ymir work/ui/public/scrollbar_thin_down_button_03.sub")
		self.ShowPriv.Show()
		
		self.nameChar = ui.MakeTextV3(self.CharSlot, "%s" % player.GetMainCharacterName(), 0, 2, False)
		self.nameChar.SetOutline()
		self.nameChar.SetWindowHorizontalAlignCenter()
		self.nameChar.SetHorizontalAlignCenter()
		
		self.textMission = ui.MakeTextV3(self.ImageSlotV2, localeInfo.PREMIUM_TEXT_5, 0, 2, False)
		self.textMission.SetOutline()
		self.textMission.SetWindowHorizontalAlignCenter()
		self.textMission.SetHorizontalAlignCenter()
		self.textMission.Show()
		
		self.textPrivV2 = {}
		self.textPriv = {}
		self.ButtonsNormal = {}
		self.statusBar = {}
		self.statusBarV2 = {}
		self.privNames = [localeInfo.PREMIUM_TEXT_6, localeInfo.PREMIUM_TEXT_7, localeInfo.PREMIUM_TEXT_8, localeInfo.PREMIUM_TEXT_9, localeInfo.PREMIUM_TEXT_4, localeInfo.PREMIUM_TEXT_13]

		for x in xrange(6):
			self.statusBar[x] = ui.Bar()
			self.statusBar[x].SetParent(self.FacilityWindow)
			self.statusBar[x].SetSize(BOARD_WIDTH - 24, 12)
			self.statusBar[x].SetPosition(2, 50 + (25 * x))
			self.statusBar[x].Show()
			self.textPriv[x] = ui.MakeTextV3(self.statusBar[x], self.privNames[x], 0, -2, False)
			self.textPriv[x].SetWindowHorizontalAlignCenter()
			self.textPriv[x].SetHorizontalAlignCenter()
			
		# for x in xrange(3):
			# self.statusBarV2[x] = ui.Bar()
			# self.statusBarV2[x].SetParent(self.FacilityWindow)
			# self.statusBarV2[x].SetSize(BOARD_WIDTH - 24, 15)
			# self.statusBarV2[x].SetPosition(2, 125 + (20 * x))
			# self.statusBarV2[x].Show()
			
			
		# values = [
			# [ localeInfo.TOOLTIP_APPLY_ATTBONUS_MONSTER, 10, 15, 25, 63 ],
			# [ localeInfo.TOOLTIP_APPLY_ATTBONUS_METIN, 10, 15, 25, 110 ],
			# [ localeInfo.TOOLTIP_APPLY_ATTBONUS_BOSS, 10, 15, 25, 111 ],
		# ]

		# for x in xrange(3):
			# self.textPrivV2[x] = ui.MakeTextV3(self.statusBarV2[x], "", 0, 0, False)
			# self.textPrivV2[x].SetWindowHorizontalAlignCenter()
			# self.textPrivV2[x].SetHorizontalAlignCenter()
			# self.textPrivV2[x].SetText("%s" % (values[x][0](values[x][self.arg])))
			
			# if values[x][4] in uiAffectShower.CHOSEN_ATTRIBUTES:
				# self.textPrivV2[x].SetFontColor(0.9, 0.4745, 0.4627)
				# self.statusBarV2[x].SetColor(COLOR_BAR_GREEN)
				# global TAKEN
				# TAKEN = x
			# else:
				# self.textPrivV2[x].SetFontColor(0.5411, 0.7254, 0.5568)
				# self.statusBarV2[x].SetColor(COLOR_BAR_RED)
			
		self.NamesButton = ["Switchbot", "Depozit Special", localeInfo.PREMIUM_TEXT_10, "Calendar evenimente", "Top clasament", localeInfo.PREMIUM_TEXT_11, "Biolog", "Wiki"]
		
		for belestipula in xrange(8):
			self.ButtonsNormal[belestipula] = ui.Button()
			self.ButtonsNormal[belestipula].SetParent(self.ButtonsWindow)
			self.ButtonsNormal[belestipula].SetPosition(10, 60 + 40 * (belestipula))
			self.ButtonsNormal[belestipula].SetUpVisual("d:/ymir work/ui/shop/btn_payout_normal.png")
			self.ButtonsNormal[belestipula].SetOverVisual("d:/ymir work/ui/shop/btn_payout_hover.png")
			self.ButtonsNormal[belestipula].SetDownVisual("d:/ymir work/ui/shop/btn_payout_down.png")
			self.ButtonsNormal[belestipula].SetText(self.NamesButton[belestipula])
			self.ButtonsNormal[belestipula].Show()
			if belestipula > 3:
				self.ButtonsNormal[belestipula].SetPosition(133, 60 + 40 * (belestipula) - 160)
				
		self.ButtonsNormal[0].SetEvent(ui.__mem_func__(self.ShowSwitch))
		self.ButtonsNormal[1].SetEvent(ui.__mem_func__(self.ShowStorage))
		self.ButtonsNormal[2].SetEvent(ui.__mem_func__(self.ShowSearch))
		self.ButtonsNormal[3].SetEvent(ui.__mem_func__(self.ShowCalendar))
		self.ButtonsNormal[4].SetEvent(ui.__mem_func__(self.ShowRanking))
		self.ButtonsNormal[5].SetEvent(ui.__mem_func__(self.ShowDungeon))
		self.ButtonsNormal[6].SetEvent(ui.__mem_func__(self.ShowBiolog))
		self.ButtonsNormal[7].SetEvent(ui.__mem_func__(self.ShowWiki))

		self.OpenEmoticonChanger = ui.Button()
		self.OpenEmoticonChanger.SetParent(self.FacilityWindow)
		self.OpenEmoticonChanger.SetPosition(10, 189)
		self.OpenEmoticonChanger.SetUpVisual("d:/ymir work/ui/shop/btn_payout_normal.png")
		self.OpenEmoticonChanger.SetOverVisual("d:/ymir work/ui/shop/btn_payout_hover.png")
		self.OpenEmoticonChanger.SetDownVisual("d:/ymir work/ui/shop/btn_payout_down.png")
		self.OpenEmoticonChanger.SetText(localeInfo.PREMIUM_TEXT_3)
		self.OpenEmoticonChanger.SetEvent(ui.__mem_func__(self.ShowEmoticon))
		self.OpenEmoticonChanger.Show()
		
		self.OpenDistanceShop = ui.Button()
		self.OpenDistanceShop.SetParent(self.FacilityWindow)
		self.OpenDistanceShop.SetPosition(133, 189)
		self.OpenDistanceShop.SetUpVisual("d:/ymir work/ui/shop/btn_payout_normal.png")
		self.OpenDistanceShop.SetOverVisual("d:/ymir work/ui/shop/btn_payout_hover.png")
		self.OpenDistanceShop.SetDownVisual("d:/ymir work/ui/shop/btn_payout_down.png")
		self.OpenDistanceShop.SetText(localeInfo.PREMIUM_TEXT_4)
		self.OpenDistanceShop.SetEvent(ui.__mem_func__(self.ShowShop))
		self.OpenDistanceShop.Show()
		
	def ShowSwitch(self):
		# interface = constInfo.GetInterfaceInstance()
		# if interface:
			# interface.ToggleSwitchbotWindow()
		net.SBOpen()

	def ShowWiki(self):
		interface = constInfo.GetInterfaceInstance()
		if interface:
			interface.ShowWiki()
		
	def ShowStorage(self):
		interface = constInfo.GetInterfaceInstance()
		if interface:
			interface.ToggleCustomInventoryWindow()
		
	def ShowSearch(self):
		interface = constInfo.GetInterfaceInstance()
		if interface:
			interface.OpenSearchShop()
		
	def ShowCalendar(self):
		interface = constInfo.GetInterfaceInstance()
		if interface:
			interface.OpenEventCalendar()
		
	def ShowRanking(self):
		interface = constInfo.GetInterfaceInstance()
		if interface:
			interface.ShowRankInfo()
		
	def ShowDungeon(self):
		interface = constInfo.GetInterfaceInstance()
		if interface:
			interface.ShowDungeonInfo()
		
	def ShowBiolog(self):
		interface = constInfo.GetInterfaceInstance()
		if interface:
			interface.ShowBiolog()
		
	def ShowEmoticon(self):
		interface = constInfo.GetInterfaceInstance()
		if interface:
			interface.OpenChangeEmoticon()

	def ShowShop(self):
		interface = constInfo.GetInterfaceInstance()
		if interface:
			interface.OpenRemoteShop()
		
	def ShowFacilityBoard(self):
		self.FacilityWindow.Show()
		self.ShowPriv.SetUpVisual("d:/ymir work/ui/public/scrollbar_thin_up_button_01.sub")
		self.ShowPriv.SetOverVisual("d:/ymir work/ui/public/scrollbar_thin_up_button_02.sub")
		self.ShowPriv.SetDownVisual("d:/ymir work/ui/public/scrollbar_thin_up_button_03.sub")
		self.IsHidden = False
		self.ButtonsWindow.Hide()
		self.textMission.SetPackedFontColor(0xff82FF7D)

	def HideFacilityBoard(self):
		self.FacilityWindow.Hide()
		self.IsHidden = True
		self.ShowPriv.SetUpVisual("d:/ymir work/ui/public/scrollbar_thin_down_button_01.sub")
		self.ShowPriv.SetOverVisual("d:/ymir work/ui/public/scrollbar_thin_down_button_02.sub")
		self.ShowPriv.SetDownVisual("d:/ymir work/ui/public/scrollbar_thin_down_button_03.sub")
		self.ButtonsWindow.Show()
		self.textMission.SetPackedFontColor(0xffFF9D9D)

	def BindInterface(self, interface):
		self.interface = proxy(interface)
		
	def Destroy(self):
		self.ClearDictionary()	
		self.bLoadedInfo = False
		
	def Close(self):			
		self.Hide()

	def OnUpdate(self):			
		if self.IsHiddenFromButtons == True:
			self.Board.SetSize(BOARD_WIDTH, BOARD_HEIGHT)
			self.InfoBorder.SetSize(BOARD_WIDTH - 20, BOARD_HEIGHT - 40)
			self.SetSize(BOARD_WIDTH, BOARD_HEIGHT)

		if player.IsPremiumUser() == 1:
			self.premiumStatus.SetText(localeInfo.PREMIUM_TEXT_1_V1)
		elif player.IsPremiumUser() == 2:
			self.premiumStatus.SetText(localeInfo.PREMIUM_TEXT_1_V2)
		elif player.IsPremiumUser() == 3:
			self.premiumStatus.SetText(localeInfo.PREMIUM_TEXT_1_V3)
		else:
			self.premiumStatus.SetText(localeInfo.PREMIUM_TEXT_2)
			
		for x in xrange(6):
			if player.IsPremiumUser() == 1:
				self.statusBar[x].SetColor(COLOR_BAR_BROWN)
			elif player.IsPremiumUser() == 2:
				self.statusBar[x].SetColor(COLOR_BAR_SILVER)
			elif player.IsPremiumUser() == 3:
				self.statusBar[x].SetColor(COLOR_BAR_YELLOW)
			else:
				self.statusBar[x].SetColor(COLOR_BAR_FALSE)
			
	def Show(self):
		self.SetTop()
		self.SetCenterPosition()
		ui.ScriptWindow.Show(self)

	def OnPressEscapeKey(self):
		self.Close()
		return True
		