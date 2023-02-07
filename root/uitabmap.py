import chat
import net
import player
import ui
import exception
import wndMgr
import uiToolTip
import uiScriptLocale
import localeInfo
import uiCommon
import item
import nonplayer
from _weakref import proxy

ROOT = 'd:/ymir work/ui/game/comp/map/'

TELEPORT_DICT = {
	0 : {
		"ICON"		: ROOT + "bg/1.png",
		"NAME"		: "Mape principale",
		
		"HASBOSS"		: 191,
		"MIN_LEVEL"		: 1,
		"MAX_LEVEL"		: 105,
		"REQUIRESITEM"		: 0,
		
		"HOWMANYWARPS"		: 3,
		"MAP1"		: "|cfffff000Satul 1 Chunjo",
		"MAP1INDEX"		: 1,
		"MAP2"		: "|cff0039ffSatul 1 Jinno",
		"MAP2INDEX"		: 2,
		"MAP3"		: "|cffff0000Satul 1 Shinsoo",
		"MAP3INDEX"		: 3,
		
		
		# "HOWMANYWARPSFARM"		: 5,
		# "MAP1BLUEFARM"		: "|cff0039ffOras",
		# "MAP1BLUEINDEXFARM"		: 29,
		# "MAP2BLUEFARM"		: "Zona Farm 1",
		# "MAP2BLUEINDEXFARM"		: 30,
		# "MAP3BLUEFARM"		: "Zona Farm 2",
		# "MAP3BLUEINDEXFARM"		: 31,
		# "MAP4BLUEFARM"		: "Zona Farm 3",
		# "MAP4BLUEINDEXFARM"		: 32,
		# "MAP5BLUEFARM"		: "Zona Farm 4",
		# "MAP5BLUEINDEXFARM"		: 33,

		# "MAP1YELLFARM"		: "|cfffff000Oras",
		# "MAP1YELLINDEXFARM"		: 29,
		# "MAP2YELLFARM"		: "Zona Farm 1",
		# "MAP2YELLINDEXFARM"		: 34,
		# "MAP3YELLFARM"		: "Zona Farm 2",
		# "MAP3YELLINDEXFARM"		: 35,
		# "MAP4YELLFARM"		: "Zona Farm 3",
		# "MAP4YELLINDEXFARM"		: 36,
		# "MAP5YELLFARM"		: "Zona Farm 4",
		# "MAP5YELLINDEXFARM"		: 37,
		
		# "MAP1REDFARM"		: "|cffff0000Oras",
		# "MAP1REDINDEXFARM"		: 38,
		# "MAP2REDFARM"		: "Zona Farm 1",
		# "MAP2REDINDEXFARM"		: 39,
		# "MAP3REDFARM"		: "Zona Farm 2",
		# "MAP3REDINDEXFARM"		: 40,
		# "MAP4REDFARM"		: "Zona Farm 3",
		# "MAP4REDINDEXFARM"		: 41,
		# "MAP5REDFARM"		: "Zona Farm 4",
		# "MAP5REDINDEXFARM"		: 42,
		
	},
	1 : {
		"ICON"		: ROOT + "bg/2.png",
		"NAME"		: "Mape secundare",
		
		
		"HASBOSS"		: 591,
		"MIN_LEVEL"		: 1,
		"MAX_LEVEL"		: 105,
		"REQUIRESITEM"		: 0,
		
		"HOWMANYWARPS"		: 3,
		"MAP1"		: "|cfffff000Satul 2 Chunjo",
		"MAP1INDEX"		: 4,
		"MAP2"		: "|cff0039ffSatul 2 Jinno",
		"MAP2INDEX"		: 5,
		"MAP3"		: "|cffff0000Satul 2 Shinsoo",
		"MAP3INDEX"		: 6,
	},
	2 : {
		"ICON"		: ROOT + "bg/9.png",
		"NAME"		: localeInfo.MAP_TEMPLE,
		
		"HASBOSS"		: 1304,
		"MIN_LEVEL"		: 40,
		"MAX_LEVEL"		: 105,
		"REQUIRESITEM"		: 0,
		
		"HOWMANYWARPS"		: 3,
		"MAP1"		: uiScriptLocale.MAP_BEGGINING,
		"MAP1INDEX"		: 7,
		"MAP2"		: "Turnul demonilor",
		"MAP2INDEX"		: 8,
		"MAP3"		: "Catacomba diavolului",
		"MAP3INDEX"		: 9,
	},
	3 : {
		"ICON"		: ROOT + "bg/8.png",
		"NAME"		: localeInfo.MAP_A2,
		
		"HASBOSS"		: 691,
		"MIN_LEVEL"		: 30,
		"MAX_LEVEL"		: 105,
		"REQUIRESITEM"		: 0,
		
		"HOWMANYWARPS"		: 3,
		"MAP1"		: "Mijloc",
		"MAP1INDEX"		: 10,
		"MAP2"		: "Zona metinelor 1",
		"MAP2INDEX"		: 11,
		"MAP3"		: "Zona metinelor 2",
		"MAP3INDEX"		: 12,
	},
	4 : {
		"ICON"		: ROOT + "bg/7.png",
		"NAME"		: localeInfo.MAP_DESERT,
		
		"HASBOSS"		: 2191,
		"MIN_LEVEL"		: 40,
		"MAX_LEVEL"		: 105,
		"REQUIRESITEM"		: 0,
		
		"HOWMANYWARPS"		: 2,
		"MAP1"		: uiScriptLocale.MAP_BEGGINING,
		"MAP1INDEX"		: 13,
		"MAP2"		: "Mijloc",
		"MAP2INDEX"		: 14,
	},
	5 : {
		"ICON"		: ROOT + "bg/10.png",
		"NAME"		: localeInfo.MAP_SNOW,

		"HASBOSS"		: 1901,
		"MIN_LEVEL"		: 45,
		"MAX_LEVEL"		: 105,
		"REQUIRESITEM"		: 0,
		
		"HOWMANYWARPS"		: 3,
		"MAP1"		: "Mijloc",
		"MAP1INDEX"		: 15,
		"MAP2"		: "Zona metinelor 1",
		"MAP2INDEX"		: 16,
		"MAP3"		: "Zona metinelor 2",
		"MAP3INDEX"		: 17,
	},
	6 : {
		"ICON"		: ROOT + "bg/11.png",
		"NAME"		: localeInfo.MAP_FLAME,
		
		"HASBOSS"		: 2206,
		"MIN_LEVEL"		: 50,
		"MAX_LEVEL"		: 105,
		"REQUIRESITEM"		: 0,
		
		"HOWMANYWARPS"		: 3,
		"MAP1"		: "Mijloc",
		"MAP1INDEX"		: 18,
		"MAP2"		: "Zona metinelor 1",
		"MAP2INDEX"		: 19,
		"MAP3"		: "Zona metinelor 2",
		"MAP3INDEX"		: 20,
	},
	7 : {
		"ICON"		: ROOT + "bg/12.png",
		"NAME"		: localeInfo.MAP_TRENT02,
		
		"HASBOSS"		: 2307,
		"MIN_LEVEL"		: 65,
		"MAX_LEVEL"		: 105,
		"REQUIRESITEM"	: 0,
		
		"HOWMANYWARPS"	: 2,
		"MAP1"			: uiScriptLocale.MAP_BEGGINING,
		"MAP1INDEX"		: 32,
		"MAP2"			: uiScriptLocale.EMPIRE_EXIT,
		"MAP2INDEX"		: 33,
	},
	8 : {
		"ICON"		: ROOT + "bg/13.png",
		"NAME"		: localeInfo.MAP_SPIDER,
		
		"HASBOSS"		: 2091,
		"MIN_LEVEL"		: 60,
		"MAX_LEVEL"		: 105,
		"REQUIRESITEM"		: 71095,
		
		"HOWMANYWARPS"		: 3,
		"MAP1"		: uiScriptLocale.SPIDERZONE + " 1",
		"MAP1INDEX"		: 21,
		"MAP2"		: uiScriptLocale.SPIDERZONE + " 2",
		"MAP2INDEX"		: 22,
		"MAP3"		: uiScriptLocale.SPIDERZONE + " 3",
		"MAP3INDEX"		: 23,
	},
	9 : {
		"ICON"		: ROOT + "bg/14.png",
		"NAME"		: "Grota Exilului",
		
		"HASBOSS"		: 2491,
		"MIN_LEVEL"		: 75,
		"MAX_LEVEL"		: 105,
		"REQUIRESITEM"		: 30190,
		
		"HOWMANYWARPS"		: 2,
		"MAP1"		: "Grota exilului 2",
		"MAP1INDEX"		: 24,
		"MAP2"		: "Camera dragonului",
		"MAP2INDEX"		: 25,
	},
	10 : {
		"ICON"		: ROOT + "bg/cape.png",
		"NAME"		: localeInfo.MAP_CAPE,
		
		"HASBOSS"		: 3291,
		"MIN_LEVEL"		: 90,
		"MAX_LEVEL"		: 105,
		"REQUIRESITEM"		: 0,
		
		"HOWMANYWARPS"		: 3,
		"MAP1"		: uiScriptLocale.MAP_BEGGINING,
		"MAP1INDEX"		: 26,
		"MAP2"		: "Zona metinelor 1",
		"MAP2INDEX"		: 27,
		"MAP3"		: "Zona metinelor 2",
		"MAP3INDEX"		: 28,
	},
	11 : {
		"ICON"		: ROOT + "bg/bay.png",
		"NAME"		: localeInfo.MAP_BAY,
		
		"HASBOSS"		: 3491,
		"MIN_LEVEL"		: 90,
		"MAX_LEVEL"		: 105,
		"REQUIRESITEM"		: 0,
		
		"HOWMANYWARPS"		: 3,
		"MAP1"		: uiScriptLocale.MAP_BEGGINING,
		"MAP1INDEX"		: 29,
		"MAP2"		: "Zona metinelor 1",
		"MAP2INDEX"		: 30,
		"MAP3"		: "Zona metinelor 2",
		"MAP3INDEX"		: 31,
	},
	12 : {
		"ICON"		: ROOT + "bg/thunder.png",
		"NAME"		: localeInfo.MAP_THUNDER,
		
		"HASBOSS"		: 3791,
		"MIN_LEVEL"		: 90,
		"MAX_LEVEL"		: 105,
		"REQUIRESITEM"		: 0,
		
		"HOWMANYWARPS"		: 3,
		"MAP1"		: uiScriptLocale.MAP_BEGGINING,
		"MAP1INDEX"		: 34,
		"MAP2"		: "Zona metinelor 1",
		"MAP2INDEX"		: 35,
		"MAP3"		: "Zona metinelor 2",
		"MAP3INDEX"		: 36,
	},
	13 : {
		"ICON"		: ROOT + "bg/gautama.png",
		"NAME"		: localeInfo.MAP_DAWN,
		
		"HASBOSS"		: 3390,
		"MIN_LEVEL"		: 90,
		"MAX_LEVEL"		: 105,
		"REQUIRESITEM"		: 0,
		
		"HOWMANYWARPS"		: 3,
		"MAP1"		: uiScriptLocale.MAP_BEGGINING,
		"MAP1INDEX"		: 37,
		"MAP2"		: "Zona metinelor 1",
		"MAP2INDEX"		: 38,
		"MAP3"		: "Zona metinelor 2",
		"MAP3INDEX"		: 39,
	},
	14 : {
		"ICON"		: ROOT + "bg/mining.png",
		"NAME"		: uiScriptLocale.MINING_MAP,
		
		"HASBOSS"		: 0,
		"MIN_LEVEL"		: 1,
		"MAX_LEVEL"		: 105,
		"REQUIRESITEM"		: 0,
		
		"HOWMANYWARPS"		: 1,
		"MAP1"		: uiScriptLocale.MAP_BEGGINING,
		"MAP1INDEX"		: 40,
		# "MAP2"		: "Zona metinelor 1",
		# "MAP2INDEX"		: 38,
		# "MAP3"		: "Zona metinelor 2",
		# "MAP3INDEX"		: 39,
	},

}

class ListBox(ui.Window):
	class NewItem(ui.Window):
		def __init__(self, index):
			ui.Window.__init__(self)
			self.background = None
			self.childs_board = None
			self.bSelected = False
			self.OnResetThings()
			self.Index = index
			
			self.childs_board = ui.BorderA()
			self.childs_board.SetParent(self)
			self.childs_board.SetSize(424,98)
			self.childs_board.Show()
			
			self.icon = ui.ExpandedImageBox()
			self.icon.SetParent(self)
			self.icon.LoadImage(TELEPORT_DICT[index]["ICON"])
			self.icon.SetPosition(4, 3)
			self.icon.Show()			
			
			self.nameBar = ui.ExpandedImageBox()
			self.nameBar.SetParent(self)
			self.nameBar.LoadImage(ROOT + "name.png")
			self.nameBar.SetPosition(4, 75)
			self.nameBar.Show()			

			self.background = ui.ExpandedImageBox()
			self.background.SetParent(self.icon)
			self.background.LoadImage(ROOT + "norm.png")
			self.background.OnMouseLeftButtonDown = ui.__mem_func__(self.OnMouseLeftButtonDownImage)
			self.background.OnMouseOverIn = ui.__mem_func__(self.OnMouseOverImage)
			self.background.OnMouseOverOut = ui.__mem_func__(self.OnMouseOverOutImage)
			self.background.Show()
			
			self.wndName = ui.TextLine()
			self.wndName.SetParent(self.nameBar)
			self.wndName.SetText(TELEPORT_DICT[index]["NAME"])
			self.wndName.SetPosition(200, 0)
			self.wndName.SetCenter()
			self.wndName.Show()

			self.SetSize(self.background.GetWidth(), self.background.GetHeight())
			
		def OnMouseLeftButtonDownImage(self):
			if self.bSelected:
				return
		
			self.background.LoadImage(ROOT + "over.png")
			
			self.bSelected = True
			if self.clickEvent:
				self.clickEvent(self.Index)
				
		def OnMouseOverImage(self):
			if self.bSelected:
				return

			self.background.LoadImage(ROOT + "down.png")
			
		def OnMouseOverOutImage(self):
			if self.bSelected:
				return
		
			self.background.LoadImage(ROOT + "norm.png")

		def __del__(self):
			ui.Window.__del__(self)
			self.OnResetThings()

		def OnResetThings(self):
			self.IsSelected = False
			self.bIsBlocked = False
			self.vnum = 0
			self.xBase = 0
			self.yBase = 0

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

			images = [self.background, self.icon, self.nameBar]
			for img in images:
				if img:
					img.SetClipRect(xList, yList, xList + widthList, yList + heightList)

			textList = [self.wndName]
			for text in textList:
				if text:
					xText, yText = text.GetGlobalPosition()

					if yText < yList or yText + text.GetTextSize()[1] > yList + heightList:
						text.Hide()
					else:
						text.Show()

			boardList = [self.childs_board]
			for board in boardList:
				if board:
					xBoard, yBoard = board.GetGlobalPosition()

					if yBoard < yList or yBoard + board.GetHeight() > yList + heightList:
						board.Hide()
					else:
						board.Show()

	def __init__(self):
		ui.Window.__init__(self)
		self.OnResetThings()

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
				totalHeight += itemH.GetHeight() + 10
			
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
			y += 10
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
				item.background.LoadImage(ROOT + "down.png")
				item.bSelected = True
				continue
			
			item.bSelected = False
			item.OnMouseOverOutImage()

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
			yAccumulate += item.GetHeight() + 10

	def Clear(self):
		range = len(self.itemList)
		
		if range > 0:
			for item in self.itemList:
				item.OnResetThings()
				item.Hide()
				del item
		
		# del self.itemList[:]
		self.itemList = []

class TabMapWindow(ui.ScriptWindow):
	def __init__(self):
		ui.ScriptWindow.__init__(self)
		
		self.titleBar = None
		self.interface = None
		
		self.AddFlag("animation")

		self.__LoadWindow()

	def __del__(self):
		ui.ScriptWindow.__del__(self)
		if self.ItemList:
			self.ItemList.Clear()

	def __LoadWindow(self):
		try:
			PythonScriptLoader = ui.PythonScriptLoader()
			PythonScriptLoader.LoadScriptFile(self, "UIScript/tabmapwindow.py")
		except:
			exception.Abort("TabMapWindow.__LoadWindow.LoadObject")

		try:
			self.titleBar = self.GetChild("TitleBar")
			self.board = self.GetChild("board")
			
			self.BorderButtons = ui.BorderA()
			self.BorderButtons.SetParent(self.board)
			self.BorderButtons.SetPosition(15,35)
			self.BorderButtons.SetSize(450,405)
			self.BorderButtons.Show()
			
		except:
			exception.Abort("TabMapWindow.__LoadWindow.BindObject")

		try:
			self.titleBar.SetCloseEvent(ui.__mem_func__(self.Close))
		except:
			exception.Abort("TabMapWindow.__LoadWindow.BindEvent")

		self.ButtonsTeleport = {}
		# self.ButtonsTeleportFarm = {}
		self.MakeTexts = {}
		self.MakeSeparators = {}

		self.ScrollBar = ui.ScrollBar()
		self.ScrollBar.SetParent(self.BorderButtons)
		self.ScrollBar.SetScrollBarSize(395)
		self.ScrollBar.SetPosition(436, 5)
		self.ScrollBar.Show()

		self.BoardSecond = ui.BorderA()
		self.BoardSecond.SetParent(self.board)
		self.BoardSecond.SetSize(197,405)
		self.BoardSecond.SetPosition(475, 35)
		self.BoardSecond.Show()
		
		self.BoardThird = ui.BorderA()
		self.BoardThird.SetParent(self.board)
		self.BoardThird.SetSize(197,155)
		self.BoardThird.SetPosition(475, 285)
		self.BoardThird.Show()
		
		self.ImageTitle = ui.ImageBox()
		self.ImageTitle.SetParent(self.BoardSecond)
		self.ImageTitle.SetPosition(3, 3)
		self.ImageTitle.LoadImage("d:/ymir work/ui/game/myshop_deco/model_view_title.sub")
		self.ImageTitle.Show()

		self.ImageTitle2 = ui.ImageBox()
		self.ImageTitle2.SetParent(self.BoardThird)
		self.ImageTitle2.SetPosition(3, 3)
		self.ImageTitle2.LoadImage("d:/ymir work/ui/game/myshop_deco/model_view_title.sub")
		self.ImageTitle2.Show()

		self.ImageBg = ui.ImageBox()
		self.ImageBg.SetParent(self.BoardSecond)
		self.ImageBg.LoadImage("d:/ymir work/ui/game/comp/map/bg_2.png")
		self.ImageBg.SetPosition(3, 25)
		self.ImageBg.SetScale(0.972, 0.989)
		self.ImageBg.Show()	
				
		for i in xrange(4):
			self.MakeSeparators[i] = ui.ImageBox()
			self.MakeSeparators[i].SetParent(self.ImageBg)
			self.MakeSeparators[i].SetPosition(0, 120 + (20 *i))
			self.MakeSeparators[i].LoadImage("d:/ymir work/ui/game/comp/map/separator.png")
			self.MakeSeparators[i].SetScale(0.972, 1.4)
			self.MakeSeparators[i].Show()
			
		for i in xrange(6):
			self.MakeTexts[i] = ui.TextLine()
			self.MakeTexts[i].SetParent(self.ImageBg)
			self.MakeTexts[i].SetPosition(95, 5)
			self.MakeTexts[i].SetPackedFontColor(0xFFFEE3AE)
			self.MakeTexts[i].SetCenter()
			self.MakeTexts[i].SetHorizontalAlignCenter()
			self.MakeTexts[i].Show()

		self.MakeTexts[1].SetText("Descriere")
		self.MakeTexts[0].SetText("Descriere")
		self.MakeTexts[0].SetParent(self.ImageTitle2)
		self.MakeTexts[1].SetParent(self.ImageTitle)

		self.MakeTexts[2].SetPosition(95,120+20)
		self.MakeTexts[3].SetPosition(95,120+40)
		self.MakeTexts[4].SetPosition(95,120)
		self.MakeTexts[5].SetPosition(95,120+60)

		self.ItemList = ListBox()
		self.ItemList.SetParent(self.BorderButtons)
		self.ItemList.SetSize(430, 395)
		self.ItemList.SetPosition(5, 5)
		self.ItemList.SetEventSelect(ui.__mem_func__(self.SelectIndex))
		self.ItemList.SetScrollBar(self.ScrollBar)
		self.ItemList.Show()
		
		for i in xrange(3):
			self.ButtonsTeleport[i] = ui.Button()
			self.ButtonsTeleport[i].SetParent(self.BoardThird)
			self.ButtonsTeleport[i].SetPosition(15, 40+ (33 * i))
			self.ButtonsTeleport[i].SetUpVisual(ROOT + "button_1.png")
			self.ButtonsTeleport[i].SetOverVisual(ROOT + "button_2.png")
			self.ButtonsTeleport[i].SetDownVisual(ROOT + "Untitled-3.png")
			self.ButtonsTeleport[i].SetText("Maps")
			self.ButtonsTeleport[i].Hide()

		# for i in xrange(5):
			# self.ButtonsTeleportFarm[i] = ui.Button()
			# self.ButtonsTeleportFarm[i].SetParent(self.BoardThird)
			# self.ButtonsTeleportFarm[i].SetPosition(15, 27+ (25 * i))
			# self.ButtonsTeleportFarm[i].SetUpVisual(ROOT + "button_1.png")
			# self.ButtonsTeleportFarm[i].SetOverVisual(ROOT + "button_2.png")
			# self.ButtonsTeleportFarm[i].SetDownVisual(ROOT + "Untitled-3.png")
			# self.ButtonsTeleportFarm[i].SetButtonScale(1.0, 0.8)
			# self.ButtonsTeleportFarm[i].SetText("Maps")
			# self.ButtonsTeleportFarm[i].Hide()
			
		self.SelectIndex(0)
		
		self.MakeTeleports()
	
	def BindInterfaceClass(self, interface):
		self.interface = interface
		
	def SelectIndex(self, index):
		self.MakeTexts[0].SetText(TELEPORT_DICT[index]["NAME"])
		self.MakeTexts[2].SetText("Nivel Recomandat:|cff00ff00 %i" % TELEPORT_DICT[index]["MIN_LEVEL"])
		self.MakeTexts[3].SetText("Nivel Maxim:|cff00ff00 %i" % TELEPORT_DICT[index]["MAX_LEVEL"])
		self.MakeTexts[4].SetText(uiScriptLocale.THIS_MAP_HAS_BOSS % nonplayer.GetMonsterName(TELEPORT_DICT[index]["HASBOSS"]))
		item.SelectItem(TELEPORT_DICT[index]["REQUIRESITEM"])
		
		if index == 1:
			self.DICT_NAME = "MAP1BLUEFARM"
		elif index == 2:
			self.DICT_NAME = "MAP1YELLFARM"
		elif index == 3:
			self.DICT_NAME = "MAP1REDFARM"


		if TELEPORT_DICT[index]["REQUIRESITEM"] > 1:
			self.MakeTexts[5].SetText("Ai nevoie de :|cff00ff00 %s" % item.GetItemName())
		else:
			self.MakeTexts[5].SetText(uiScriptLocale.MAP_NOT_REQUIRED_ITEM)
		
		self.ResetButtons()
		
		for x in xrange(TELEPORT_DICT[index]["HOWMANYWARPS"]):
			self.ButtonsTeleport[x].Show()
			if x == 0:
				self.ButtonsTeleport[x].SetText(TELEPORT_DICT[index]["MAP1"])
				self.ButtonsTeleport[x].SetEvent(ui.__mem_func__(self.TeleportMe), TELEPORT_DICT[index]["MAP1INDEX"])

			elif x == 1:
				self.ButtonsTeleport[x].SetText(TELEPORT_DICT[index]["MAP2"])
				self.ButtonsTeleport[x].SetEvent(ui.__mem_func__(self.TeleportMe), TELEPORT_DICT[index]["MAP2INDEX"])

			elif x == 2:
				self.ButtonsTeleport[x].SetText(TELEPORT_DICT[index]["MAP3"])
				self.ButtonsTeleport[x].SetEvent(ui.__mem_func__(self.TeleportMe), TELEPORT_DICT[index]["MAP3INDEX"])
				
		# if TELEPORT_DICT[index]["HOWMANYWARPSFARM"] > 1:
			# for x in xrange(TELEPORT_DICT[index]["HOWMANYWARPSFARM"]):

				# if x == 0:
					# self.ButtonsTeleportFarm[x].SetText(TELEPORT_DICT[index][self.DICT_NAME])
					# self.ButtonsTeleportFarm[x].SetEvent(ui.__mem_func__(self.TeleportMe), TELEPORT_DICT[index]["MAP1INDEXFARM"])

				# elif x == 1:
					# self.ButtonsTeleportFarm[x].SetText(TELEPORT_DICT[index][self.DICT_NAME])
					# self.ButtonsTeleportFarm[x].SetEvent(ui.__mem_func__(self.TeleportMe), TELEPORT_DICT[index]["MAP2INDEXFARM"])

				# elif x == 2:
					# self.ButtonsTeleportFarm[x].SetText(TELEPORT_DICT[index][self.DICT_NAME])
					# self.ButtonsTeleportFarm[x].SetEvent(ui.__mem_func__(self.TeleportMe), TELEPORT_DICT[index]["MAP3INDEXFARM"])
					
				# elif x == 3:
					# self.ButtonsTeleportFarm[x].SetText(TELEPORT_DICT[index][self.DICT_NAME])
					# self.ButtonsTeleportFarm[x].SetEvent(ui.__mem_func__(self.TeleportMe), TELEPORT_DICT[index]["MAP4INDEXFARM"])
					
				# elif x == 4:
					# self.ButtonsTeleportFarm[x].SetText(TELEPORT_DICT[index][self.DICT_NAME])
					# self.ButtonsTeleportFarm[x].SetEvent(ui.__mem_func__(self.TeleportMe), TELEPORT_DICT[index]["MAP5INDEXFARM"])

	def ResetButtons(self):
		for i in xrange(3):
			self.ButtonsTeleport[i].Hide()
			
		# for i in xrange(5):
			# self.ButtonsTeleportFarm[i].Hide()
	
	def OnRunMouseWheel(self, nLen):
		if nLen > 0:
			self.ScrollBar.OnUp()
		else:
			self.ScrollBar.OnDown()

	def MakeTeleports(self):
		for x in xrange(len(TELEPORT_DICT)):
			self.ItemList.AppendItem(x)

	def TeleportMe(self, index):
		# if index == 1 or index == 2 or index == 3:
			# for i in xrange(3):
				# self.ButtonsTeleport[i].Hide()
			# for i in xrange(5):
				# self.ButtonsTeleportFarm[i].Show()
	
		net.SendChatPacket("/maptab_teleport %d" % index)
		# chat.AppendChat(7, "/maptab_teleport %d" % index)
		
		
	def Close(self):
		self.Hide()

	def Destroy(self):
		self.ClearDictionary()
		self.titleBar = None

	def Open(self):
		if self.IsShow():
			return

		self.SetCenterPosition()
		self.Show()

	def OnPressEscapeKey(self):
		self.Close()
		return True
