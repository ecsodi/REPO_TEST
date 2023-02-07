## Development @ Grimmjock

import thenewui as ui
import app
import net
import grp 
import wndMgr
import mouseModule
import chat
import ui
import item
import nonplayer
import localeInfo
import uiToolTip
import cfg

from _weakref import proxy

PATH_ROOT = "d:/ymir work/ui/game/battle_pass/"
PATH_ROOT_NORM = "d:/ymir work/ui/game/normal_interface/battle_pass/"

INFO_TAB = [ localeInfo.BATTLEPASS_TEXT_1, localeInfo.BATTLEPASS_TEXT_2, localeInfo.BATTLEPASS_TEXT_3,
localeInfo.BATTLEPASS_TEXT_4, localeInfo.BATTLEPASS_TEXT_5, localeInfo.BATTLEPASS_TEXT_6, localeInfo.BATTLEPASS_TEXT_7
]

MISSION_DESC_DICT = {}

class ListBox(ui.Window):
	class NewItem(ui.Window):
		def __init__(self, type, vnum, count, max_count, func, parent):
			ui.Window.__init__(self)
			self.Type = type
			self.Vnum = vnum
			self.Rewards = 0
			self.select = False

			self.percentActual = count
			self.percentTotal = max_count
			
			self.Reinitialize()
			self.tooltipItem = uiToolTip.ItemToolTip()
			self.tooltipItem.Hide()

			self.DoChange = ui.__mem_func__(func)

			self.background = ui.ExpandedImageBox()
			self.background.SetParent(self, parent.hWnd)
			self.background.LoadImage(PATH_ROOT_NORM + "mission_bg_normal.tga")

			self.background.OnMouseLeftButtonDown = ui.__mem_func__(self.OnMouseLeftButtonDownImage)
			self.background.OnMouseOverIn = ui.__mem_func__(self.OnMouseOverImage)
			self.background.OnMouseOverOut = ui.__mem_func__(self.OnMouseOverOutImage)
			self.background.Show()
			
			self.iconBehind = ui.ExpandedImageBox()
			self.iconBehind.SetParent(self, parent.hWnd)
			self.iconBehind.LoadImage(PATH_ROOT_NORM + "mission_small_clean.tga")
			self.iconBehind.SetPosition(1, 1)
			self.iconBehind.Show()
			
			self.icon = ui.ExpandedImageBox()
			self.icon.SetParent(self, parent.hWnd)
			self.icon.SetPosition(1, 1)
			self.icon.Show()

			self.wndName = ui.TextLine()
			self.wndName.SetParent(self.background, parent.hWnd)
			self.wndName.SetPosition(47, 6)

			self.wndName.SetOutline()
			self.wndName.Show()

			if type == 0:
				if vnum == 0:
					vnum = 50258 # cor
				item.SelectItem(vnum)
				self.icon.LoadImage(item.GetIconImageFileName())
				self.wndName.SetText(item.GetItemName())
			elif type == 1:
				self.icon.LoadImage(MISSION_DESC_DICT[type][vnum][1])
				self.wndName.SetText(MISSION_DESC_DICT[type][vnum][0])

			else:
				self.icon.LoadImage(MISSION_DESC_DICT[type][vnum][1])
				self.wndName.SetText(MISSION_DESC_DICT[type][vnum][0])
				
			self.listGauge = []
			
			bgGauge = ui.ExpandedImageBox()
			bgGauge.SetParent(self)
			bgGauge.LoadImage(PATH_ROOT_NORM + "mission_progress_empty.tga")
			bgGauge.SetPosition(45, 25)
			bgGauge.AddFlag("not_pick")
			bgGauge.Show()			

			bgGaugeFull = ui.ExpandedImageBox()
			bgGaugeFull.SetParent(bgGauge)
			bgGaugeFull.LoadImage(PATH_ROOT_NORM + "mission_progress_full.tga")
			bgGaugeFull.SetPosition(8, 2)
				
			bgGaugeFull.AddFlag("not_pick")
			bgGaugeFull.Show()

			bgGaugeFull.SetWindowName("GaugeBar")
			
			self.listGauge.append(bgGauge)
			self.listGauge.append(bgGaugeFull)
			
			self.dictSlotBase = []
			self.dictRewards = []

			for x in xrange(3):
				SlotBase = ui.ExpandedImageBox()
				SlotBase.SetParent(self, parent.hWnd)
				SlotBase.SetPosition(187 + x * 32, 6)
				SlotBase.LoadImage("d:/ymir work/ui/public/Slot_Base.sub")

				SlotBase.SetScale(0.9, 0.9)
				SlotBase.Show()
				
				self.dictSlotBase.append(SlotBase)

			self.SetSize(self.background.GetWidth(), self.background.GetHeight())		
		
		def AddReward(self, vnum, count):
			if self.Rewards >= 3:
				self.Rewards = 0
		
			item.SelectItem(vnum)
		
			Image = ui.ExpandedImageBox()
			Image.SetParent(self.dictSlotBase[self.Rewards], self.parent.hWnd)
			Image.LoadImage(item.GetIconImageFileName())
			Image.SetEvent(ui.__mem_func__(self.IconOnMouseOverIn), "MOUSE_OVER_IN", vnum)
			Image.SetEvent(ui.__mem_func__(self.IconOnMouseOverOut), "MOUSE_OVER_OUT")
			
			Image.SetPosition(0, 0)
			Image.Show()
			
			self.dictRewards.append(Image)

			tmpDropText = ui.TextLine()
			tmpDropText.SetParent(Image, self.parent.hWnd)
			tmpDropText.AddFlag("attach")
			tmpDropText.AddFlag("not_pick")
			tmpDropText.SetText(str(count))
			tmpDropText.SetOutline()

			tmpDropText.SetPosition(Image.GetWidth() - tmpDropText.GetTextSize()[0],\
										Image.GetHeight() - tmpDropText.GetTextSize()[1])
			tmpDropText.Show()
			
			self.dictRewards.append(tmpDropText)
			
			self.Rewards += 1
		
		def IconOnMouseOverIn(self, type, vnum):
			if self.tooltipItem and vnum:
				self.tooltipItem.SetItemToolTip(vnum)

		def IconOnMouseOverOut(self, type):
			if self.tooltipItem:
				self.tooltipItem.HideToolTip()
	
		def OnRender(self):
			xList, yList = self.parent.GetGlobalPosition()
			
			for item in self.listGauge:
				if item.GetWindowName() == "GaugeBar":
					if self.percentTotal == 0:
						self.percentTotal = 1
					item.SetClipRect(0.0, yList, -1.0 + float(self.percentActual) / float(self.percentTotal), yList + self.parent.GetHeight(), True)
				else:
					item.SetClipRect(xList, yList, xList + self.parent.GetWidth(), yList + self.parent.GetHeight())
		
		
		def OnMouseLeftButtonDownImage(self):
			if self.select:
				return

			self.background.LoadImage(PATH_ROOT_NORM + "mission_bg_selected.tga")

			if self.DoChange:
				self.DoChange(self.Type, self.Vnum)
			
			if self.clickEvent:
				self.clickEvent(self.Type, self.Vnum)
			
			self.select = True
		
		def GetSelected(self):
			return self.select
		
		def OnMouseOverImage(self):
			if self.select:
				return

			self.background.LoadImage(PATH_ROOT_NORM + "mission_bg_normal.tga")

		def OnMouseOverOutImage(self):
			if self.select:
				return

			self.background.LoadImage(PATH_ROOT_NORM + "mission_bg_normal.tga")

		def OverOutForce(self):
			self.select = False

			self.background.LoadImage(PATH_ROOT_NORM + "mission_bg_normal.tga")

		def __del__(self):
			ui.Window.__del__(self)
			self.Reinitialize()
			
		def Reinitialize(self):
			self.selected = False
			self.xBase = 0
			self.yBase = 0

			self.overInEvent = None
			self.overOutEvent = None
			self.clickEvent = None
			self.background = None
			self.tooltipItem = None
			self.dictSlotBase = []
			self.dictRewards = []
			self.listGauge = []

		def SetParent(self, parent):
			ui.Window.SetParent(self, parent)
			self.parent = proxy(parent)

		def SetBasePosition(self, x, y):
			self.xBase = x
			self.yBase = y
			
		def GetBasePosition(self):
			return (self.xBase, self.yBase)
			
		def SetOverInEvent(self, event):
			self.overInEvent = event
			
		def SetOverOutEvent(self, event):
			self.overOutEvent = event
			
		def SetClickEvent(self, event):
			self.clickEvent = event
			
		# def OnMouseOverIn(self):
			# if self.overInEvent:
				# self.overInEvent()
			
		# def OnMouseOverOut(self):
			# if self.overOutEvent:
				# self.overOutEvent()

	def __init__(self):
		ui.Window.__init__(self)
		self.Reinitialize()

	def __del__(self):
		ui.Window.__del__(self)
		self.Reinitialize()
		
	def Destroy(self):
		self.Reinitialize()
		
	def Reinitialize(self):
		self.itemList = []
		self.scrollBar = None
		self.tooltipItem = None
		
		self.selectEvent = None

	def SetParent(self, parent):
		ui.Window.SetParent(self, parent)
		
		self.SetPosition(5, 5)
		self.SetSize(parent.GetWidth() - 10, parent.GetHeight() - 10)
		
	def SetScrollBar(self, scrollBar):
		scrollBar.SetScrollEvent(ui.__mem_func__(self.__OnScroll))
		scrollBar.SetScrollStep(0.2)
		self.scrollBar = scrollBar

	def SetItemToolTip(self, tooltipItem):
		self.tooltipItem = tooltipItem
		
	def SetSelectEvent(self, event):
		self.selectEvent = event
		
	def __OnScroll(self):
		self.AdjustItemPositions(True)
			
	def GetTotalItemHeight(self):
		totalHeight = 0
		
		if self.itemList:
			for itemH in self.itemList:
				totalHeight += itemH.GetHeight() + 2
			
		return totalHeight
			
	def OnMouseWheel(self, nLen):
		if self.scrollBar:
			self.scrollBar.OnMouseWheel(nLen)
			
	def GetItemCount(self):
		return len(self.itemList)
			
	def OverOutAll(self, y):
		for x in xrange(len(self.itemList)):
			self.itemList[x].OverOutForce()
			
		self.itemList[y].SetSelect()
	
	def GetCount(self, type, vnum):
		if len(self.itemList) == 0:
			return 0
			
		for item in self.itemList:
			if item.Type == type and item.Vnum == vnum:
				return item.percentActual

		return 0

	def GetMaxCount(self, type, vnum):
		if len(self.itemList) == 0:
			return 0
			
		for item in self.itemList:
			if item.Type == type and item.Vnum == vnum:
				return item.percentTotal

		return 0

	def IsFinished(self, type, vnum):
		if len(self.itemList) == 0:
			return localeInfo.BATTLEPASS_TEXT_8
			
		for item in self.itemList:
			if item.Type == type and item.Vnum == vnum:
				if item.percentActual >= item.percentTotal:
					return localeInfo.BATTLEPASS_TEXT_9
				else:
					return localeInfo.BATTLEPASS_TEXT_8

		return localeInfo.BATTLEPASS_TEXT_8
	
	def BattlePassFinished(self):
		if len(self.itemList) == 0:
			return False		

		for item in self.itemList:
			if item.percentActual < item.percentTotal:
				return False

		return True
	
	def SetProgressMission(self, type, vnum, count, max_count):
		if len(self.itemList) == 0:
			return False
			
		for item in self.itemList:
			if item.Type == type and item.Vnum == vnum:
				item.percentActual = count
				if item.GetSelected() == True:
					item.DoChange(type, vnum) # Refresh in real time
				return True

		return False

	def AddRewardToMission(self, Type, TargetVnum, VnumReward, CountReward):
		if len(self.itemList) == 0:
			return
			
		for item in self.itemList:
			if item.Type == Type and item.Vnum == TargetVnum:
				item.AddReward(VnumReward, CountReward)
				return
	
	def AppendItem(self, type, vnum, count, max_count, func):
		if self.SetProgressMission(type, vnum, count, max_count):
			return
	
		item = self.NewItem(type, vnum, count, max_count, func, self)
		item.SetParent(self)
		
		if len(self.itemList) == 0:
			item.SetBasePosition(0, 0)
		else:
			x, y = self.itemList[-1].GetLocalPosition()
			y += 2
			item.SetBasePosition(0, y + self.itemList[-1].GetHeight())

		item.SetOverInEvent(ui.__mem_func__(self.OverInImage))
		item.SetOverOutEvent(ui.__mem_func__(self.OverOutImage))
		item.SetClickEvent(ui.__mem_func__(self.SelectItem))
			
		item.Show()
		self.itemList.append(item)
		
		self.AdjustScrollBar()
		self.AdjustItemPositions()
	
	def OverInImage(self, vnum):
		pass

	def OverOutImage(self):
		pass

	def AdjustScrollBar(self):
		totalHeight = float(self.GetTotalItemHeight())
		if totalHeight:
			scrollBarHeight = min(float(self.GetHeight() - 10) / totalHeight, 1.0)
		else:
			scrollBarHeight = 1.0
			
		self.scrollBar.SetMiddleBarSize(scrollBarHeight)
		
	def ResetScrollbar(self):
		self.scrollBar.SetPos(0)
				
	def AdjustItemPositions(self, scrolling = False, startIndex = -1):		
		scrollPos = self.scrollBar.GetPos()
		totalHeight = self.GetTotalItemHeight() - self.GetHeight()

		idx = 0
		if startIndex >= 0:
			idx = startIndex

		for item in self.itemList[idx:]:
			xB, yB = item.GetBasePosition()
			
			if startIndex >= 0:
				yB -= ITEM_HEIGHT + 2
			
			if scrolling:
				setPos = yB - int(scrollPos * totalHeight)
				item.SetPosition(xB, setPos)
			else:
				item.SetPosition(xB, yB)
				
			item.SetBasePosition(xB, yB)

	def SelectItem(self, type, vnum):
		if len(self.itemList) == 0:
			return
	
		for item in self.itemList:
			if item.Type == type and item.Vnum == vnum:
				continue
		
			item.OverOutForce()

	def Clear(self):
		if len(self.itemList) == 0:
			return
	
		for item in self.itemList:
			item.Reinitialize()
			item.Hide()
			del item

		self.itemList = []

class BattlePass(ui.ScriptWindow):
	def __init__(self):
		self.bLoaded = False
		self.bLoadedInfo = False
		ui.ScriptWindow.__init__(self)
		self.FinalRewards = 0
		self.dictRewards = {}
		self.tooltipItem = uiToolTip.ItemToolTip()
		self.tooltipItem.Hide()
		
		self.LoadWindow()
		self.LoadMissionDesc()
		
	def __del__(self):
		ui.ScriptWindow.__del__(self)
		self.tooltipItem = None
		self.dictRewards = {}

	def Destroy(self):
		self.ClearDictionary()
		if self.ListBoxItem:
			self.ListBoxItem.Clear()

		self.ListBoxItem = None
		self.dictWhiteSpace = []
		self.dictInfoText = []
		self.tooltipItem = None
		self.dictRewards = {}
		MISSION_DESC_DICT = {}
	
	def Show(self):
		self.LoadWindow()
		self.SetCenterPosition()
		ui.ScriptWindow.Show(self)
		if self.bLoadedInfo == False:
			net.SendChatPacket("/battle_pass r")

	def LoadMissionDesc(self):
		try:
			lines = open(app.GetLocalePath() + "/battle_pass.txt", "r").readlines()
		except:
			import exception
			exception.Abort("LoadMissionDesc")

		for line in lines:
			tokens = line[:-1].split("\t")
			if len(tokens) == 0 or not tokens[0]:
				continue
				
			if tokens[0] == "#":
				continue
			
			if not int(tokens[0]) in MISSION_DESC_DICT:
				MISSION_DESC_DICT[int(tokens[0])] = {}

			MISSION_DESC_DICT[int(tokens[0])][int(tokens[1])] = [ tokens[2], tokens[3], tokens[4] ]
			
	def LoadWindow(self):
		if self.bLoaded == True:
			return
			
		self.bLoaded = True

		self.AddFlag("movable")

		self.Board = ui.BoardWithTitleBar()
		self.Board.SetParent(self)
		self.Board.AddFlag("attach")
		self.Board.SetSize(537, 297)

		self.Board.SetTitleName("BattlePass")
		self.Board.SetCloseEvent(ui.__mem_func__(self.Close))
		self.Board.Show()

		self.ThinBoard = ui.BorderA()
		self.ThinBoard.SetParent(self)
		self.ThinBoard.SetSize(298,255)
		self.ThinBoard.SetPosition(8,32)
		self.ThinBoard.Show()
		
		self.InformationBoard = ui.BorderA()
		self.InformationBoard.SetParent(self)
		self.InformationBoard.SetSize(207,255)
		self.InformationBoard.SetPosition(320,32)
		self.InformationBoard.Show()
		
		self.missionBG = self.MakeImageBoxNorm(self.InformationBoard, 3, 22, "mission_big_clean.tga")
		self.missionTitle = self.MakeImageBoxNorm(self.InformationBoard, 3, 3, "title_bar_special.tga")
		
		self.textMission = ui.MakeTextV3(self.missionTitle, "", 0, 3, False)
		self.textMission.SetOutline()
		self.textMission.SetPackedFontColor(0xffffeea6)
		self.textMission.SetWindowHorizontalAlignCenter()
		self.textMission.SetHorizontalAlignCenter()
		self.textMission.Show()
		
		self.missionBar1 = self.MakeImageBoxNorm(self.InformationBoard, 0, 22, "info_bar_title.tga")
		self.missionText1 = ui.MakeTextV3(self.missionBar1, localeInfo.BATTLEPASS_TEXT_5, 5, 2, False)
		self.missionText1.SetPackedFontColor(0xFFFEE3AE)
		self.missionText2 = ui.MakeTextV3(self.missionBar1, "", 5, 22, False) 
		
		self.missionBar2 = self.MakeImageBoxNorm(self.InformationBoard, 0, 62, "info_bar_title.tga")
		self.missionText3 = ui.MakeTextV3(self.missionBar2, localeInfo.BATTLEPASS_TEXT_10, 5, 2, False)
		self.missionText3.SetPackedFontColor(0xFFFEE3AE)
		self.missionText4 = ui.MakeTextV3(self.missionBar2, "", 5, 22, False) 
		
		self.missionBar3 = self.MakeImageBoxNorm(self.InformationBoard, 0, 102, "info_bar_even.tga")
		self.missionText5 = ui.MakeTextV3(self.missionBar3, "", 5, 2, False)
		self.missionText6 = ui.MakeTextV3(self.missionBar3, "", 5, 22, False) 
		
		self.missionBar4 = self.MakeImageBoxNorm(self.InformationBoard, 0, 142, "info_bar_title.tga")
		self.missionText7 = ui.MakeTextV3(self.missionBar4, localeInfo.BATTLEPASS_TEXT_6, 5, 2, False)
		self.missionText7.SetPackedFontColor(0xFFFEE3AE)
		self.missionText8 = ui.MakeTextV3(self.missionBar4, "", 5, 22, False) 
		
		self.missionBar5 = self.MakeImageBoxNorm(self.InformationBoard, 0, 182, "info_bar_title.tga")
		self.missionText9 = ui.MakeTextV3(self.missionBar5, localeInfo.BATTLEPASS_TEXT_11, 5, 2, False)
		self.missionText9.SetPackedFontColor(0xFFFEE3AE)
			
		self.ListBoxItem = ListBox()
		self.ListBoxItem.SetParent(self.ThinBoard)
		self.ListBoxItem.SetSize(310, 248)
		self.ListBoxItem.SetPosition(4, 4)
		self.ListBoxItem.Show()

		self.ScrollBar = ui.ScrollBar()
		self.ScrollBar.SetParent(self)
		self.ScrollBar.SetScrollBarSize(253)
		self.ScrollBar.SetPosition(306, 33)

			
		self.ListBoxItem.SetScrollBar(self.ScrollBar)
		self.ScrollBar.Show()
		
		self.SetSize(self.Board.GetWidth(), self.Board.GetHeight())
		
		self.MakeBoardInfo()
		
		self.BoardTip = ui.Bar()
		self.BoardTip.SetParent(self)
		self.BoardTip.SetPosition(50 - 40, 75 - 40)
		self.BoardTip.SetSize(537 - 20, 297 - 45)
		self.BoardTip.SetColor(grp.GenerateColor(0.0, 0.0, 0.0, 0.6))
		self.BoardTip.Hide()
		
		self.MakeTip()
		
	def BattlePassMission(self, Type, TargetVnum, Count, MaxCount):
		self.ListBoxItem.AppendItem(Type, TargetVnum, Count, MaxCount, self.SelectMission)
		
		if self.ListBoxItem.BattlePassFinished():
			self.GetRewardFinal.Enable()
			
		self.bLoadedInfo = True
		
	def BattlePassMissionReward(self, Type, TargetVnum, VnumReward, CountReward):
		self.ListBoxItem.AddRewardToMission(Type, TargetVnum, VnumReward, CountReward)

	def MakeBoardInfo(self):
		self.GetRewardFinal = ui.MakeButton(self.missionBG, 110, 180, False, PATH_ROOT_NORM, "reward_normal.tga", "reward_over.tga", "reward_down.tga")
		self.GetRewardFinal.SetDisableVisual(PATH_ROOT_NORM + "reward_down.tga")
		self.GetRewardFinal.Disable()
		self.ShopBtn = ui.MakeButton(self.missionBG, 110, 205, False, PATH_ROOT_NORM, "btn_shop_normal.png", "btn_shop_hover.png", "btn_shop_down.png")
		self.GetRewardFinal.SetEvent(ui.__mem_func__(self.TakeFinalReward))
		self.ShopBtn.SetEvent(ui.__mem_func__(self.OpenShop))

		wndItem = ui.GridSlotWindow()
		wndItem.SetParent(self.missionBG)
		wndItem.SetPosition(1, 188)
			
		wndItem.SetSlotStyle(wndMgr.SLOT_STYLE_NONE)
		wndItem.SetOverInItemEvent(ui.__mem_func__(self.OverInItem))
		wndItem.SetOverOutItemEvent(ui.__mem_func__(self.OverOutItem))
		wndItem.ArrangeSlot(0, 3, 1, 34, 32, 0, 0)
		wndItem.SetSlotBaseImage("d:/ymir work/ui/public/Slot_Base.sub", 1.0, 1.0, 1.0, 1.0)

		wndItem.RefreshSlot()
		wndItem.Show()
		self.wndItem = wndItem
	
	def OpenShop(self):
		net.SendRemoteShopPacket(8)

	def ToggleTip(self):
		if self.BoardTip.IsShow():
			pass
			
		self.BoardTip.Show()
	
	def CloseTip(self):
		self.BoardTip.Hide()
	
	def MakeTip(self):
		self.textTip = ui.MakeTextV3(self.BoardTip, localeInfo.BATTLEPASS_TEXT_13, 5, 5, False)
		self.textTip.SetOutline()
		self.textTip.Show()
		
		wndItem = ui.GridSlotWindow()
		wndItem.SetParent(self.BoardTip)
		wndItem.SetPosition(350, 0)
		wndItem.SetSlotStyle(wndMgr.SLOT_STYLE_NONE)
		wndItem.ArrangeSlot(0, 1, 1, 51, 32, 0, 0)
		wndItem.RefreshSlot()
		wndItem.SetItemSlot(0, 50027, 1)
		wndItem.Show()

		self.wndItem2 = wndItem
		
		understood = ui.Button()
		understood.SetParent(self.BoardTip)
		understood.SetPosition(5, 25)
		understood.SetUpVisual("d:/ymir work/ui/public/middle_button_01.sub")
		understood.SetOverVisual("d:/ymir work/ui/public/middle_button_02.sub")
		understood.SetDownVisual("d:/ymir work/ui/public/middle_button_03.sub")
		understood.SetText("Ok")
		understood.SetEvent(ui.__mem_func__(self.CloseTip))
		understood.Show()
		self.understood = understood

	def BattlePassFinal(self, vnum, count):
		if self.FinalRewards >= 3:
			self.FinalRewards = 0
		
		self.dictRewards[self.FinalRewards] = vnum
		self.wndItem.SetItemSlot(self.FinalRewards, vnum, count)
		self.FinalRewards += 1
	
	def OverInItem(self, Index):
		if self.tooltipItem and Index < len(self.dictRewards):
			self.tooltipItem.SetItemToolTip(self.dictRewards[Index])

	def OverOutItem(self):
		if self.tooltipItem:
			self.tooltipItem.HideToolTip()
	
	def TakeFinalReward(self):
		net.SendChatPacket("/battle_pass final")
	
	def MakeImageBox(self, parent, x, y, img):
		image = ui.ImageBox()
		image.SetParent(parent)
		image.SetPosition(x, y)
		image.LoadImage(PATH_ROOT + img)
		image.Show()
		return image	
		
	def MakeImageBoxNorm(self, parent, x, y, img):
		image = ui.ImageBox()
		image.SetParent(parent)
		image.SetPosition(x, y)
		image.LoadImage(PATH_ROOT_NORM + img)
		image.Show()
		return image
	
	def SelectMission(self, type, vnum):
		self.textMission.SetText(MISSION_DESC_DICT[type][vnum][0])
		self.missionText2.SetText("Status: " + str(self.ListBoxItem.IsFinished(type, vnum)))
		self.missionText4.SetText("Nume: " + MISSION_DESC_DICT[type][vnum][0])
		self.missionText5.SetText(localeInfo.BATTLEPASS_TEXT_4 + ": " + localeInfo.AddPointToNumberString(str(self.ListBoxItem.GetMaxCount(type, vnum) - self.ListBoxItem.GetCount(type, vnum))))
		self.missionText6.SetText("Procentaj: %.1f" % (float(self.ListBoxItem.GetCount(type, vnum) * 100) / float(self.ListBoxItem.GetMaxCount(type, vnum))) + "%")
		self.missionText8.SetText(MISSION_DESC_DICT[type][vnum][2])
		
	def OnRunMouseWheel(self, nLen):
		if nLen > 0:
			self.ScrollBar.OnUp()
		else:
			self.ScrollBar.OnDown()
			
	def OnPressEscapeKey(self):
		self.Close()
		return True
		
	def Close(self):
		self.OverOutItem()
		self.Hide()
