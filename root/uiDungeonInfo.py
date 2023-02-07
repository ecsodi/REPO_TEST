import thenewui as ui
import item
import net
import constInfo
import localeInfo
import uiCommon
import wndMgr
import app
import grp
import chat
import CacheEffect as player
import skill
import shop
import chr
import uiScriptLocale
import math
from _weakref import proxy
import cfg
import uiToolTip
import ime
import renderTarget
import wikipedia
import mouseModule
RENDER_TARGET_INDEX = 23

DUNGEON_DICT = {
	0 : {
		"ICON"		: "d:/ymir work/ui/game/questtimer/icons/ape_dungeon.png",
		"NAME"		: localeInfo.DUNGEON_TEXT_01,
		"LEVEL_MIN"	: 30,
		"LEVEL_MAX"	: 50,
		"ELEMENT" 	: localeInfo.TARGET_INFO_RACE_WIND,
		"COOLDOWN"	: 1800,
		"BOSS_VNUM" : 5163,
		"TICKET"	: 4373,
	},
	1 : {
		"ICON"		: "d:/ymir work/ui/game/questtimer/icons/zodiac.png",
		"NAME"		: localeInfo.DUNGEON_TEXT_02,
		"LEVEL_MIN"	: 40,
		"LEVEL_MAX"	: 60,
		"ELEMENT" 	: localeInfo.TARGET_INFO_RACE_WIND,
		"COOLDOWN"	: 1800,
		"BOSS_VNUM" : 692,
		"TICKET"	: 4371,
	},
	2 : {
		"ICON"		: "d:/ymir work/ui/game/questtimer/icons/sd3_new.png",
		"NAME"		: localeInfo.DUNGEON_TEXT_03,
		"LEVEL_MIN"	: 60,
		"LEVEL_MAX"	: 80,
		"ELEMENT" 	: localeInfo.TARGET_INFO_RACE_WIND,
		"COOLDOWN"	: 1800,
		"BOSS_VNUM" : 2092,
		"TICKET"	: 4374,
	},
	3 : {
		"ICON"		: "d:/ymir work/ui/game/questtimer/icons/deviltower_new.png",
		"NAME"		: localeInfo.DUNGEON_TEXT_04,
		"LEVEL_MIN"	: 40,
		"LEVEL_MAX"	: 90,
		"ELEMENT" 	: localeInfo.TARGET_INFO_RACE_EARTH,
		"COOLDOWN"	: 1800,
		"BOSS_VNUM" : 1093,
		"TICKET"	: 4372,
	},
	4 : {
		"ICON"		: "d:/ymir work/ui/game/questtimer/icons/devilcatacomb_new.png",
		"NAME"		: localeInfo.DUNGEON_TEXT_05,
		"LEVEL_MIN"	: 75,
		"LEVEL_MAX"	: 105,
		"ELEMENT" 	: localeInfo.TARGET_INFO_RACE_DARK,
		"COOLDOWN"	: 2700,
		"BOSS_VNUM" : 2598,
		"TICKET"	: 30319,
	},
	5 : {
		"ICON"		: "d:/ymir work/ui/game/questtimer/icons/dragon_lair.png",
		"NAME"		: localeInfo.DUNGEON_TEXT_06,
		"LEVEL_MIN"	: 75,
		"LEVEL_MAX"	: 105,
		"ELEMENT" 	: localeInfo.TARGET_INFO_RACE_ELEC,
		"COOLDOWN"	: 2700,
		"BOSS_VNUM" : 2493,
		"TICKET"	: 30179,
	},
	6 : {
		"ICON"		: "d:/ymir work/ui/game/questtimer/icons/flame_dungeon.png",
		"NAME"		: localeInfo.DUNGEON_TEXT_07,
		"LEVEL_MIN"	: 95,
		"LEVEL_MAX"	: 105,
		"ELEMENT" 	: localeInfo.TARGET_INFO_RACE_FIRE,
		"COOLDOWN"	: 3600,
		"BOSS_VNUM" : 6091,
		"TICKET"	: 8665,
	},
	7 : {
		"ICON"		: "d:/ymir work/ui/game/questtimer/icons/snow_dungeon.png",
		"NAME"		: localeInfo.DUNGEON_TEXT_08,
		"LEVEL_MIN"	: 95,
		"LEVEL_MAX"	: 105,
		"ELEMENT" 	: localeInfo.TARGET_INFO_RACE_ICE,
		"COOLDOWN"	: 3600,
		"BOSS_VNUM" : 6191,
		"TICKET"	: 8666,
	},
}
# Dungeons

class ListBox(ui.Window):
	class NewItem(ui.Window):
		def __init__(self, index):
			ui.Window.__init__(self)
			self.background = None
			self.bSelected = False
			self.OnResetThings()
			self.Index = index

			self.background = ui.ExpandedImageBox()
			self.background.SetParent(self)
			self.background.LoadImage("dungeon/button_norm.png")
			self.background.OnMouseLeftButtonDown = ui.__mem_func__(self.OnMouseLeftButtonDownImage)
			self.background.OnMouseOverIn = ui.__mem_func__(self.OnMouseOverImage)
			self.background.OnMouseOverOut = ui.__mem_func__(self.OnMouseOverOutImage)
			self.background.Show()
			
			self.icon = ui.ExpandedImageBox()
			self.icon.SetParent(self)
			self.icon.LoadImage(DUNGEON_DICT[index]["ICON"])
			self.icon.SetPosition(6, 6)
			self.icon.SetScale(0.82, 0.83)
			self.icon.Show()			

			self.wndName = ui.TextLine()
			self.wndName.SetParent(self.background)
			self.wndName.SetText(DUNGEON_DICT[index]["NAME"])
			self.wndName.SetPosition(65, 18)
			self.wndName.SetOutline()
			self.wndName.Show()
			self.wndName.SetPackedFontColor(0xffd3c29f)

			self.wndAds = ui.TextLine()
			self.wndAds.SetParent(self.background)
			self.wndAds.SetHorizontalAlignCenter()
			self.wndAds.SetText("Disponibil")
			self.wndAds.SetPosition(317, 18)
			self.wndAds.SetPackedFontColor(0xff69e742)
			self.wndAds.SetOutline()
			self.wndAds.Show()
	
			self.SetSize(self.background.GetWidth(), self.background.GetHeight())
		
		def CheckAdvertise(self):
			if player.GetStatus(player.LEVEL) < DUNGEON_DICT[self.Index]["LEVEL_MIN"]:
				self.wndAds.SetPackedFontColor(0xffce3434)
				self.wndAds.SetText("Lv. prea mic!")
				self.isRedBG = 1
				return
			
			if player.GetStatus(player.LEVEL) > DUNGEON_DICT[self.Index]["LEVEL_MAX"]:
				self.wndAds.SetPackedFontColor(0xffce3434)
				self.wndAds.SetText("Lv. prea mare!")
				self.isRedBG = 1
				return
			
			self.wndAds.SetText("Disponibil")
			self.wndAds.SetPackedFontColor(0xff69e742)			

		def OnMouseLeftButtonDownImage(self):
			if self.bSelected:
				return
		
			if self.isRedBG == 1:
				self.background.LoadImage("dungeon/button_red_down.png")
			else:
				self.background.LoadImage("dungeon/button_green_down.png")

			self.bSelected = True
			if self.clickEvent:
				self.clickEvent(self.Index)
				
		def OnMouseOverImage(self):
			if self.bSelected:
				return

			if self.isRedBG == 1:
				self.background.LoadImage("dungeon/button_red_over.png")
			else:
				self.background.LoadImage("dungeon/button_green_over.png")

		def OnMouseOverOutImage(self):
			if self.bSelected:
				return
		
			if self.isRedBG == 1:
				self.background.LoadImage("dungeon/button_red.png")
			else:
				self.background.LoadImage("dungeon/button_green.png")
				
		def __del__(self):
			ui.Window.__del__(self)
			self.OnResetThings()

		def OnResetThings(self):
			self.IsSelected = False
			self.bIsBlocked = False
			self.vnum = 0
			self.xBase = 0
			self.yBase = 0
			self.wndTimeLeft = 0
			self.isRedBG = 0

			self.clickEvent = None
			if self.background != None:
				self.background.Hide()
			self.background = None

		def SetParent(self, parent):
			ui.Window.SetParent(self, parent)
			self.parent = proxy(parent)

		def SetBasePosition(self, x, y):
			self.xBase = x
			self.yBase = y
			
		def GetBasePosition(self):
			return (self.xBase, self.yBase)
			
		def SetClickEvent(self, event):
			self.clickEvent = event

		def OnRender(self):
			xList, yList = self.parent.GetGlobalPosition()
			widthList, heightList = self.parent.GetWidth(), self.parent.GetHeight()	

			images = [self.background, self.icon]
			for img in images:
				if img:
					img.SetClipRect(xList, yList, xList + widthList, yList + heightList)

			textList = [self.wndName, self.wndAds]
			for text in textList:
				if text:
					xText, yText = text.GetGlobalPosition()

					if yText < yList or yText + text.GetTextSize()[1] > yList + heightList:
						text.Hide()
					else:
						text.Show()
			
			if self.wndAds.IsShow():
				self.CheckAdvertise()
				
			if self.wndTimeLeft > 0 and self.wndTimeLeft - app.GetGlobalTimeStamp() > 0:
				m, s = divmod(self.wndTimeLeft - app.GetGlobalTimeStamp(), 60)
				h, m = divmod(m, 60)
				self.wndAds.SetText("%02d:%02d:%02d" % (h, m, s))
				self.wndAds.SetPackedFontColor(0xffce3434)
				self.isRedBG = 1

	def __init__(self):
		ui.Window.__init__(self)
		self.OnResetThings()
		# self.SelectItemForce(0)
		
	def __del__(self):
		ui.Window.__del__(self)
		self.OnResetThings()
		
	def Destroy(self):
		self.OnResetThings()
		
	def OnResetThings(self):
		self.SetFuncDown = None
		self.SelectIndexFunc = None
		self.itemList = []
		self.scrollBar = None
		self.isRedBG = 0

		self.selectEvent = None
		self.selectedItemVnum = 0
	
	def SetEventSelect(self, event):
		self.SelectIndexFunc = event
	
	def SetParent(self, parent):
		ui.Window.SetParent(self, parent)
		
		self.SetPosition(5, 5)
		self.SetSize(parent.GetWidth() - 10, parent.GetHeight() - 10)
		
	def SetScrollBar(self, scrollBar):
		scrollBar.SetScrollEvent(ui.__mem_func__(self.__OnScroll))
		scrollBar.SetScrollStep(0.2)
		self.scrollBar=scrollBar

	def SetSelectEvent(self, event):
		self.selectEvent = event
		
	def __OnScroll(self):
		self.RefreshItemPosition(True)
			
	def GetTotalHeightItems(self):
		totalHeight = 0
		
		if self.itemList:
			for itemH in self.itemList:
				totalHeight += itemH.GetHeight() + 2
			
		return totalHeight

	def GetItemCount(self):
		return len(self.itemList)

	def AppendItem(self, index):
		item = self.NewItem(index)
		item.SetParent(self)

		if len(self.itemList) == 0:
			item.SetBasePosition(0, 0)
		else:
			x, y = self.itemList[-1].GetLocalPosition()
			y += 2
			item.SetBasePosition(0, y + self.itemList[-1].GetHeight())

		item.SetClickEvent(ui.__mem_func__(self.SelectItem))
		item.Show()
		self.itemList.append(item)

		self.ResetPosScrollBar()
		self.ResizeScrollBar()	
		self.RefreshItemPosition()

	def SelectItem(self, index):
		for item in self.itemList:
			if item.Index == index:
				continue
			
			item.bSelected = False
			item.OnMouseOverOutImage()
			
		if self.SelectIndexFunc:
			self.SelectIndexFunc(index)

	def SelectItemForce(self, index):
		for item in self.itemList:
			if item.Index == index:
				if self.isRedBG == 1:
					item.background.LoadImage("dungeon/button_red.png")
				else:
					item.background.LoadImage("dungeon/button_green.png")

				item.bSelected = True
				continue
			
			item.bSelected = False
			item.OnMouseOverOutImage()

	def SendInfos(self, index, time):
		for item in self.itemList:
			if item.Index == index:
				item.wndTimeLeft = time + app.GetGlobalTimeStamp()
				break

	def ResizeScrollBar(self):
		totalHeight = float(self.GetTotalHeightItems())
		if totalHeight:
			scrollBarHeight = min(float(self.GetHeight() - 10) / totalHeight, 1.0)
		else:
			scrollBarHeight = 1.0
			
		self.scrollBar.SetMiddleBarSize(scrollBarHeight)
	
	def ResetPosScrollBar(self):
		self.scrollBar.SetPos(0)

	def RefreshItemPosition(self, bScroll = False):		
		scrollPos = self.scrollBar.GetPos()
		totalHeight = self.GetTotalHeightItems() - self.GetHeight()

		idx, CurIdx, yAccumulate = 0, 0, 0
		for item in self.itemList[idx:]:
			if bScroll:
				setPos = yAccumulate - int(scrollPos * totalHeight)
				item.SetPosition(0, setPos)
			else:
				item.SetPosition(0, yAccumulate)
				
			item.SetBasePosition(0, yAccumulate)

			CurIdx += 1
			yAccumulate += item.GetHeight() + 2

	def Clear(self):
		range = len(self.itemList)
		
		if range > 0:
			for item in self.itemList:
				item.OnResetThings()
				item.Hide()
				del item
		
		# del self.itemList[:]
		self.itemList = []

class DungeonInfoWindow(ui.ScriptWindow):
	class ItemGrid(object):
		def __init__(self, width, height):
			self.grid = {}
			self.gridWidth = width
			self.gridHeight = height
			self.gridSize = width * height
			self.Clear()

		def __del__(self):
			self.grid = {}
			self.gridWidth = 0
			self.gridHeight = 0
			self.gridSize = 0

		def Clear(self):
			for pos in range(self.gridSize):
				self.grid[pos] = False

		def IsEmpty(self, pos, width, height):
			row = pos / self.gridWidth

			if row + height > self.gridHeight:
				return False

			if pos + width > row * self.gridWidth + self.gridWidth:
				return False

			for y in range(height):
				start = pos + (y * self.gridWidth)
				if self.grid[start] == True:
					return False

				x = 1
				while x < width:
					x =+ 1
					if self.grid[start + x] == True:
						return False

			return True

		def FindBlank(self, width, height):
			if width > self.gridWidth or height > self.gridHeight:
				return -1

			for row in range(self.gridHeight):
				for col in range(self.gridWidth):
					index = row * self.gridWidth + col
					if self.IsEmpty(index, width, height):
						return index

			return -1

		def Put(self, pos, width, height):
			if not self.IsEmpty(pos, width, height):
				return False

			for y in range(height):
				start = pos + (y * self.gridWidth)
				self.grid[start] = True

				x = 1
				while x < width:
					x += 1
					self.grid[start + x] = True

			return True
			
	def __init__(self):
		ui.ScriptWindow.__init__(self)
		self.bLoaded = 0
		self.Index = -1
		self.interface = None
		self.dlgTeleportQuestion = None
		self.tooltipItem = None
		self.DictZoom = {}
		self.LoadWindow()
		self.boxItems = {}
		self.boxGrid = self.ItemGrid(11, 3)

	def __del__(self):
		ui.ScriptWindow.__del__(self)

		if self.ModelPreview:
			self.ModelPreview.Hide()
			renderTarget.SetVisibility(RENDER_TARGET_INDEX, False)
			self.ModelPreview = None
			
		self.DictZoom = {}
		if self.ItemList:
			self.ItemList.Clear()

	def Show(self):
		self.SetTop()
		self.SetCenterPosition()
		self.SelectIndex(0, True)
		ui.ScriptWindow.Show(self)
	
	def LoadWindow(self):
		if self.bLoaded == 1:
			return

		self.bLoaded = 1		

		self.AddFlag("float")
		self.AddFlag("movable")
		self.AddFlag("animation")
		
		self.Board = ui.BoardWithTitleBar()
		self.Board.SetParent(self)
		self.Board.SetSize(630, 575)
		self.Board.SetTitleName("Dungeon Info")
		self.Board.AddFlag("not_pick")
		self.Board.SetCloseEvent(ui.__mem_func__(self.Close))
		self.Board.Show()			
		
		self.SetSize(self.Board.GetWidth(), self.Board.GetHeight())

		self.ThinBoard = ui.ImageBox()
		self.ThinBoard.SetParent(self.Board)
		self.ThinBoard.SetPosition(10, 36)
		self.ThinBoard.LoadImage("dungeon/bg_run.png")
		self.ThinBoard.Show()	

		self.PossibleDrops = ui.ImageBox()
		self.PossibleDrops.SetParent(self.Board)
		self.PossibleDrops.SetPosition(10, 434)
		self.PossibleDrops.LoadImage("dungeon/bg_drop.png")
		self.PossibleDrops.Show()
		
		self.PossibleDropsText = ui.MakeText(self.PossibleDrops, "Dungeon Boss Drop", 0, 3)
		self.PossibleDropsText.SetWindowHorizontalAlignCenter()
		self.PossibleDropsText.SetHorizontalAlignCenter()
		
		self.ItemList = ListBox()
		self.ItemList.SetParent(self.ThinBoard)
		self.ItemList.SetSize(370, 380)
		self.ItemList.SetPosition(6, 6)
		self.ItemList.SetEventSelect(ui.__mem_func__(self.SelectIndex))
		self.ItemList.Show()
		
		self.rewardItems = ui.GridSlotWindow()
		self.rewardItems.SetParent(self.PossibleDrops)
		self.rewardItems.SetPosition(6, 26)
		self.rewardItems.SetSlotStyle(wndMgr.SLOT_STYLE_NONE)
		self.rewardItems.SetOverInItemEvent(ui.__mem_func__(self.OverInItem))
		self.rewardItems.SetOverOutItemEvent(ui.__mem_func__(self.OverOutItem))
		self.rewardItems.ArrangeSlot(0, 11, 3, 34, 33, 0, 0)
		self.rewardItems.SetSlotBaseImage("dungeon/slot.png", 1.0, 1.0, 1.0, 1.0)	
		self.rewardItems.RefreshSlot()
		self.rewardItems.Show()

		self.ScrollBar = ui.ScrollBar()
		self.ScrollBar.SetParent(self)
		self.ScrollBar.SetScrollBarSize(393)
		self.ScrollBar.SetPosition(388, 36)
		self.ItemList.SetScrollBar(self.ScrollBar)
		self.ScrollBar.Show()
		
		self.MakeDungeons()
		self.MakeInfoDungeon()
		
		if self.rewardItems:
			self.rewardItems.SetOverInItemEvent(ui.__mem_func__(self.__OnOverInBoxItem))
			self.rewardItems.SetOverOutItemEvent(ui.__mem_func__(self.__OnOverOutBoxItem))

	def __OnOverInBoxItem(self, slotIndex):
		self.__ShowBoxItemToolTip(slotIndex)

	def __OnOverOutBoxItem(self):
		if self.tooltipItem:
			self.tooltipItem.HideToolTip()

	def __ShowBoxItemToolTip(self, slotIndex):
		if self.tooltipItem:
			self.tooltipItem.ClearToolTip()

			metinSlot = []
			for i in xrange(player.METIN_SOCKET_MAX_NUM):
				metinSlot.append(0)

			attrSlot = []
			for i in xrange(player.ATTRIBUTE_SLOT_MAX_NUM):
				attrSlot.append((0, 0))

			self.tooltipItem.AddItemData(self.boxItems[slotIndex][0], metinSlot, attrSlot)

	def MakeDungeons(self):
		for x in xrange(len(DUNGEON_DICT)):
			self.ItemList.AppendItem(x)
			self.DictZoom[x] = 10.0
	
	def MakeInfoDungeon(self):
		self.BarInfo = ui.ExpandedImageBox()
		self.BarInfo.SetParent(self.Board)
		self.BarInfo.LoadImage("dungeon/bg_info.png")
		self.BarInfo.SetPosition(400, 36)
		self.BarInfo.Show()
		self.NameTitle = {}
		self.personalNames = {}
		self.limitNames = {}
		self.wndNames = {}
		
		self.ItemNames = ["", "Statistici Personale","Previzualizare","Interactiuni"]
		for i in xrange(4):
			self.NameTitle[i] = ui.MakeImageBox(self.BarInfo, "dungeon/dungeon_titlename.png", 2, 2 + (140 * i))
			self.wndNames[i] = ui.MakeText(self.NameTitle[i], self.ItemNames[i], 0, 8)
			self.wndNames[i].SetOutline()
			self.wndNames[i].SetPackedFontColor(0xffd3c29f)
			self.wndNames[i].SetWindowHorizontalAlignCenter()	
			self.wndNames[i].SetHorizontalAlignCenter()
			
		self.Separators = {}
		
		for i in xrange(2):
			self.Separators[i] = ui.MakeImageBox(self.BarInfo, "dungeon/little_separator.png", 2, 52 + (20 * i))
			
		self.Necessary = ui.MakeImageBox(self.BarInfo, "dungeon/item_necessary.png", 2, 95)

		self.wndNecessary = ui.MakeText(self.Necessary, "Obiect necesar", 10, 13)
		
		for i in xrange(3):
			self.limitNames[i] = ui.MakeText(self.BarInfo, "", 8, 35 +(20 * i))
			self.limitNames[i].SetOutline()
			self.limitNames[i].SetPackedFontColor(0xffd3c29f)
			
		self.SeparatorsSec = {}
		
		for i in xrange(3):
			self.SeparatorsSec[i] = ui.MakeImageBox(self.BarInfo, "dungeon/little_separator.png", 2, 193 + (20 * i))
			
		self.SeparatorsSec[2].SetPosition(2, 480)
		
		for i in xrange(3):
			self.personalNames[i] = ui.MakeText(self.BarInfo, "Test", 8, 175 +(20 * i))
			self.personalNames[i].SetOutline()
			self.personalNames[i].SetPackedFontColor(0xffd3c29f)

		self.NameTitle[2].SetPosition(2, 235)
		self.NameTitle[3].SetPosition(2, 410)

		self.PossibleDropsText.SetOutline()
		self.wndNecessary.SetOutline()
		self.PossibleDropsText.SetPackedFontColor(0xffd3c29f)
		self.wndNecessary.SetPackedFontColor(0xffd3c29f)

		self.TeleportButton = ui.Button()
		self.TeleportButton.SetParent(self.BarInfo)
		self.TeleportButton.SetUpVisual("dungeon/buttons/button_teleport_1.png")
		self.TeleportButton.SetOverVisual("dungeon/buttons/button_teleport_2.png")
		self.TeleportButton.SetDownVisual("dungeon/buttons/button_teleport_3.png")
		self.TeleportButton.SetPosition(5, 489)
		self.TeleportButton.SetText("Teleportare")
		self.TeleportButton.SetToolTipText("Teleportare")
		self.TeleportButton.SetEvent(ui.__mem_func__(self.AskTeleport))
		self.TeleportButton.Show()

		self.itemSlot = ui.GridSlotWindow()
		self.itemSlot.SetParent(self.Necessary)
		self.itemSlot.ArrangeSlot(0, 1, 1, 32, 32, 0, 0)
		self.itemSlot.SetPosition(180, 7)
		self.itemSlot.SetOverInItemEvent(ui.__mem_func__(self.OverInItem))
		self.itemSlot.SetOverOutItemEvent(ui.__mem_func__(self.OverOutItem))
		self.itemSlot.Show()

		self.ModelPreview = ui.RenderTarget()
		self.ModelPreview.SetParent(self.BarInfo)
		self.ModelPreview.SetSize(215, 138)
		self.ModelPreview.SetPosition(3, 268)
		self.ModelPreview.SetRenderTarget(RENDER_TARGET_INDEX)
		self.ModelPreview.Show()

		renderTarget.SetBackground(RENDER_TARGET_INDEX, "dungeon/bg_run.png")
		renderTarget.SetVisibility(RENDER_TARGET_INDEX, True)
		renderTarget.SelectModel(RENDER_TARGET_INDEX, 691)

		self.ShopButton = ui.Button()
		self.ShopButton.SetParent(self.BarInfo)
		self.ShopButton.SetUpVisual("dungeon/buttons/button_leave_1.png")
		self.ShopButton.SetOverVisual("dungeon/buttons/button_leave_2.png")
		self.ShopButton.SetDownVisual("dungeon/buttons/button_leave_3.png")
		self.ShopButton.SetPosition(148, 489)
		self.ShopButton.SetToolTipText("Magazin")
		self.ShopButton.SetEvent(ui.__mem_func__(self.__OpenShop))
		self.ShopButton.Show()

		self.ResetButton = ui.Button()
		self.ResetButton.SetParent(self.BarInfo)
		self.ResetButton.SetUpVisual("dungeon/buttons/button_refresh_1.png")
		self.ResetButton.SetOverVisual("dungeon/buttons/button_refresh_2.png")
		self.ResetButton.SetDownVisual("dungeon/buttons/button_refresh_3.png")
		self.ResetButton.SetPosition(184, 489)
		self.ResetButton.SetToolTipText("Resetare Cooldown")
		self.ResetButton.SetEvent(ui.__mem_func__(self.RefreshCooldown))
		self.ResetButton.Show()
		
		self.TimeButton = ui.Button()
		self.TimeButton.SetParent(self.BarInfo)
		self.TimeButton.SetUpVisual("dungeon/buttons/button_time_1.png")
		self.TimeButton.SetOverVisual("dungeon/buttons/button_time_2.png")
		self.TimeButton.SetDownVisual("dungeon/buttons/button_time_3.png")
		self.TimeButton.SetPosition(5, 448)
		self.TimeButton.SetToolTipText("Clasament timp")
		self.TimeButton.SetEvent(ui.__mem_func__(self.RefreshCooldown))
		self.TimeButton.Show()

		self.KilledButton = ui.Button()
		self.KilledButton.SetParent(self.BarInfo)
		self.KilledButton.SetUpVisual("dungeon/buttons/button_deaths_1.png")
		self.KilledButton.SetOverVisual("dungeon/buttons/button_deaths_2.png")
		self.KilledButton.SetDownVisual("dungeon/buttons/button_deaths_3.png")
		self.KilledButton.SetPosition(77, 448)
		self.KilledButton.SetToolTipText("Clasament finalizate")
		self.KilledButton.SetEvent(ui.__mem_func__(self.RefreshCooldown))
		self.KilledButton.Show()
		
		self.RankButton = ui.Button()
		self.RankButton.SetParent(self.BarInfo)
		self.RankButton.SetUpVisual("dungeon/buttons/button_rank_1.png")
		self.RankButton.SetOverVisual("dungeon/buttons/button_rank_2.png")
		self.RankButton.SetDownVisual("dungeon/buttons/button_rank_3.png")
		self.RankButton.SetPosition(150, 448)
		self.RankButton.SetToolTipText("Clasament general")
		self.RankButton.SetEvent(ui.__mem_func__(self.RefreshCooldown))
		self.RankButton.Show()

	def __OpenShop(self):
		net.SendRemoteShopPacket(3)
		
	def RefreshCooldown(self):
		chat.AppendChat(1, "to do #")
		
	def SelectIndex(self, index, bSelectFromList = False):
		if self.Index == index:
			return
			
		self.personalNames[0].SetText("Completate:")
		self.personalNames[1].SetText("Cel mai rapid timp:")
		self.personalNames[2].SetText("Max dmg. in boss:")
	
		self.limitNames[0].SetText("Element: " + DUNGEON_DICT[index]["ELEMENT"])
		self.limitNames[1].SetText(uiScriptLocale.DUNGEON_INFO_3 + str(DUNGEON_DICT[index]["LEVEL_MIN"]) + " - " + str(DUNGEON_DICT[index]["LEVEL_MAX"]))
		self.limitNames[2].SetText(uiScriptLocale.DUNGEON_INFO_2 + localeInfo.SecondToDHM(DUNGEON_DICT[index]["COOLDOWN"]))

		self.wndNames[0].SetText(str(DUNGEON_DICT[index]["NAME"]))
	
		self.Index = index
		
		renderTarget.SelectModel(RENDER_TARGET_INDEX, DUNGEON_DICT[self.Index]["BOSS_VNUM"])

		if bSelectFromList: # This it to force select a index, like reset "selected item"
			self.ItemList.SelectItemForce(index)
			
		self.RefreshBoxInventory()

		self.itemSlot.SetItemSlot(0, DUNGEON_DICT[self.Index]["TICKET"], 0)
	
	def ClearBoxInventory(self):
		for slotPos in xrange(self.rewardItems.GetSlotCount()):
			self.rewardItems.ClearSlot(slotPos)
			self.rewardItems.EnableCoverButton(slotPos)

		if self.boxGrid:
			self.boxGrid.Clear()

		if self.boxItems:
			self.boxItems = {}

	def RefreshBoxInventory(self):
		self.ClearBoxInventory()

		for itemDrop in wikipedia.GetMonsterDropByVnum(DUNGEON_DICT[self.Index]["BOSS_VNUM"]):

			if itemDrop != 0:
				itemVnum = itemDrop["item"][0]
				itemCount = itemDrop["item"][1]
				if itemCount <= 1:
					itemCount = 0

				item.SelectItem(itemVnum)
				itemIcon = item.GetIconImage()
				(width, height) = item.GetItemSize()

				pos = self.boxGrid.FindBlank(width, height)
				if pos == -1:
					break

				self.boxGrid.Put(pos, width, height)
				self.boxItems.update({ pos : [ itemVnum, itemCount] })
				self.rewardItems.SetItemSlot(pos, itemVnum, itemCount)

				self.rewardItems.RefreshSlot()
	
	def OverInItem(self, slotIndex):
		if mouseModule.mouseController.isAttached() or self.Index == -1:
			return

		if 0 != self.tooltipItem and DUNGEON_DICT[self.Index]["TICKET"] != 0:
			self.tooltipItem.SetItemToolTip(DUNGEON_DICT[self.Index]["TICKET"])

	def OverOutItem(self):
		if 0 != self.tooltipItem:
			self.tooltipItem.HideToolTip()

	def SetItemToolTip(self, tooltip):
		self.tooltipItem = tooltip

	def AskTeleport(self):
		if self.dlgTeleportQuestion or self.Index == -1:
			return
		
		dlgTeleportQuestion = uiCommon.QuestionDialog()
		dlgTeleportQuestion.SetText(localeInfo.DUNGEON_TELEPORT_ASK)
		dlgTeleportQuestion.SetAcceptEvent(ui.__mem_func__(self.OnTeleportDungeon))
		dlgTeleportQuestion.SetCancelEvent(ui.__mem_func__(self.TeleportQuestionCancel))
		dlgTeleportQuestion.Open()
		self.dlgTeleportQuestion = dlgTeleportQuestion

	def OnTeleportDungeon(self):
		if self.Index != -1:
			net.SendChatPacket("/dungeon_teleport %d" % (self.Index))
		
		if self.dlgTeleportQuestion:
			self.dlgTeleportQuestion.Close()
			self.dlgTeleportQuestion = None

	def TeleportQuestionCancel(self):
		if self.dlgTeleportQuestion:
			self.dlgTeleportQuestion.Close()
			self.dlgTeleportQuestion = None	

	def OnRunMouseWheel(self, nLen):
		if nLen > 0:
			self.ScrollBar.OnUp()
		else:
			self.ScrollBar.OnDown()
		
	def SendInfos(self, index, time):
		if self.ItemList:
			self.ItemList.SendInfos(index, time)
		
	def SetInterface(self, interface):
		self.interface = interface

	def Close(self):
		if self.dlgTeleportQuestion:
			self.dlgTeleportQuestion.Close()
			self.dlgTeleportQuestion = None
			
		if 0 != self.tooltipItem:
			self.tooltipItem.HideToolTip()
		
		self.Hide()
	
	def OnPressEscapeKey(self):		
		self.Close()
		return True	
		