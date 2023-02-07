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
import item
from _weakref import proxy

PATH_ROOT = "d:/ymir work/ui/game/bio/"

class BiologWindow(ui.ScriptWindow):
	BIOLOG_ADDITIONAL_ITEMS = (8604, 31113)

	def __init__(self):
		self.tooltipItem = None
		self.bLoadedInfo = False	
		ui.ScriptWindow.__init__(self)
		self.RewardItemVnum = 0
		self.isLoaded = 0
		self.lastUpdate = 0
		self.vnumGlobal = 0
		self.timeMax = 0
		self.percentActual = 0
		self.percentTotal = 0
		self.interface = None
		self.AdditionalCheckbox = {}

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
		self.Board.SetSize(335,312)
		self.Board.AddFlag("not_pick")
		self.Board.SetTitleName("Biolog")
		self.Board.SetCloseEvent(ui.__mem_func__(self.Close))
		self.Board.Show()
		
		self.boardAfter = ui.MakeImageBox(self.Board, PATH_ROOT + "bg.png", 8, 32)
		self.MissionName = ui.MakeImageBox(self.boardAfter, PATH_ROOT + "header.png", 3, 4)
		self.MissionTitle = ui.MakeImageBox(self.boardAfter, PATH_ROOT + "title.png", 1, 53)
		self.RewardTitle = ui.MakeImageBox(self.boardAfter, PATH_ROOT + "title.png", 1, 184)
		self.MissionTime = ui.MakeImageBox(self.boardAfter, PATH_ROOT + "deliver_bg.png", 0, 147)
		self.MissionTimeClock = ui.MakeImageBox(self.MissionTime, PATH_ROOT + "clock.png", 250, 8)
		self.MissionTime.SetWindowHorizontalAlignCenter()

		self.BonusBoard = ui.MakeBrownBoard(self.boardAfter, 75, 210, 237, 50, False)
		self.MissionSlotBoard = ui.MakeBrownBoard(self.boardAfter, 5, 80, 70, 65, False)
		self.MissionSlotReward = ui.MakeBrownBoard(self.boardAfter, 5, 210, 70, 50, False)
		self.MissionReinforce = ui.MakeBrownBoard(self.boardAfter, 75, 80, 237, 32, False)
		self.MissionButtonBoard = ui.MakeBrownBoard(self.boardAfter, 75, 113, 237, 32, False)

		self.AdditionalCheckbox = {}

		for i in xrange(3):
			self.AdditionalCheckbox[i] = ui.CheckBox_Biolog()
			self.AdditionalCheckbox[i].SetParent(self.MissionReinforce)
			self.AdditionalCheckbox[i].SetPosition(140 + (67*i), 7)
			self.AdditionalCheckbox[i].Enable()
			self.AdditionalCheckbox[i].Show()
			
		self.AdditionalCheckbox[2].SetParent(self.MissionTime)
		self.AdditionalCheckbox[2].SetPosition(230, 7)

		self.AdditionalCheckbox[0].SetEvent(self.SelectNoCooldown)
		self.AdditionalCheckbox[1].SetEvent(self.SelectNoFail)
		self.AdditionalCheckbox[2].SetEvent(self.SetNotification)

		self.listGauge = []
		
		bgGauge = ui.ExpandedImageBox()
		bgGauge.SetParent(self.MissionTitle)
		bgGauge.LoadImage(PATH_ROOT + "gauge_thing.png")
		bgGauge.SetPosition(198, 5)
		bgGauge.AddFlag("not_pick")
		bgGauge.Show()			

		bgGaugeFull = ui.ExpandedImageBox()
		bgGaugeFull.SetParent(bgGauge)
		bgGaugeFull.LoadImage(PATH_ROOT + "gauge_green.png")
		bgGaugeFull.SetPosition(0, 0)
		bgGaugeFull.AddFlag("not_pick")
		bgGaugeFull.Show()

		bgGaugeFull.SetWindowName("GaugeBar")
		
		self.listGauge.append(bgGauge)
		self.listGauge.append(bgGaugeFull)

		self.btnSend = ui.Button()
		self.btnSend.SetParent(self.MissionButtonBoard)
		self.btnSend.SetUpVisual(PATH_ROOT + "deliver_norm.png")
		self.btnSend.SetOverVisual(PATH_ROOT + "deliver_over.png")
		self.btnSend.SetDownVisual(PATH_ROOT + "deliver_down.png")
		self.btnSend.SetPosition(40, 7)
		self.btnSend.SetWindowHorizontalAlignCenter()
		self.btnSend.SetText(uiScriptLocale.SEND_ITEMS_BIOLOG)
		self.btnSend.SetEvent(ui.__mem_func__(self.SendBiologItem))
		self.btnSend.Show()	
		
		self.MissionText = ui.MakeText(self.MissionTitle, "Material:", 5, 5)
		self.MissionChance = ui.MakeText(self.MissionButtonBoard, localeInfo.BIO_CHANCE, 5, 9)
		self.MissionReinforceText = ui.MakeText(self.MissionReinforce, localeInfo.BIO_REINFORCE, 5, 9)
		
		self.MissionInfos = ui.MakeText(self.MissionName, "Misiunile Biologului", -20, 17)
		self.MissionInfos.SetWindowHorizontalAlignCenter()
		
		self.MissionReward = ui.MakeText(self.RewardTitle, uiScriptLocale.REWARD_BIOLOG, 0, 5)
		self.MissionReward.SetWindowHorizontalAlignCenter()
		self.MissionReward.SetHorizontalAlignCenter()
		
		self.MissionTimeText = ui.MakeText(self.MissionTime, False, 0, 9)
		self.MissionTimeText.SetHorizontalAlignCenter()
		self.MissionTimeText.SetWindowHorizontalAlignCenter()

		self.leftItemsText = ui.MakeText(bgGauge, False, 55, 5)
		self.leftItemsText.SetVerticalAlignCenter()
		self.leftItemsText.SetHorizontalAlignCenter()
		self.leftItemsText.SetText("1/69")
		self.leftItemsText.Show()

		self.dictRewardBonuses = {}

		for i in xrange(2):
			self.dictRewardBonuses[i] = ui.MakeText(self.BonusBoard, False, 0, 8 + (20*i))
			self.dictRewardBonuses[i].SetWindowHorizontalAlignCenter()
			self.dictRewardBonuses[i].SetHorizontalAlignCenter()
			self.dictRewardBonuses[i].SetPackedFontColor(0xff8c8c8c)
			self.dictRewardBonuses[i].SetText("---")
			
		self.itemSlot = ui.GridSlotWindow()
		self.itemSlot.SetParent(self.MissionSlotBoard)
		self.itemSlot.SetPosition(0, 15)
		self.itemSlot.ArrangeSlot(0, 1, 1, 32, 32, 0, 0)
		self.itemSlot.SetSlotBaseImage("d:/ymir work/ui/game/comp/storage/slot.png", 1.0, 1.0, 1.0, 1.0)
		self.itemSlot.SetOverInItemEvent(ui.__mem_func__(self.OnOverInItem))
		self.itemSlot.SetOverOutItemEvent(ui.__mem_func__(self.OnOverOutItem))
		self.itemSlot.SetWindowHorizontalAlignCenter()
		self.itemSlot.Show()
		
		self.itemSlotReward = ui.GridSlotWindow()
		self.itemSlotReward.SetParent(self.MissionSlotReward)
		self.itemSlotReward.SetPosition(0, 10)
		self.itemSlotReward.ArrangeSlot(0, 1, 1, 32, 32, 0, 0)
		self.itemSlotReward.SetSlotBaseImage("d:/ymir work/ui/game/comp/storage/slot.png", 1.0, 1.0, 1.0, 1.0)
		self.itemSlotReward.SetOverInItemEvent(ui.__mem_func__(self.OnOverInItemReward))
		self.itemSlotReward.SetOverOutItemEvent(ui.__mem_func__(self.OnOverOutItem))
		self.itemSlotReward.SetWindowHorizontalAlignCenter()
		self.itemSlotReward.Show()
		
		self.itemSlotReset = ui.GridSlotWindow()
		self.itemSlotReset.SetParent(self.MissionReinforce)
		self.itemSlotReset.SetPosition(65, 1)
		self.itemSlotReset.ArrangeSlot(0, 1, 1, 32, 32, 0, 0)
		self.itemSlotReset.SetSlotBaseImage("d:/ymir work/ui/game/comp/storage/slot.png", 1.0, 1.0, 1.0, 1.0)
		self.itemSlotReset.SetItemSlot(0, self.BIOLOG_ADDITIONAL_ITEMS[0], 0)
		self.itemSlotReset.SetOverInItemEvent(ui.__mem_func__(self.OnOverInItemReset))
		self.itemSlotReset.SetOverOutItemEvent(ui.__mem_func__(self.OnOverOutItem))
		self.itemSlotReset.SetWindowHorizontalAlignCenter()
		self.itemSlotReset.Show()
		
		self.itemSlotChance = ui.GridSlotWindow()
		self.itemSlotChance.SetParent(self.MissionReinforce)
		self.itemSlotChance.SetPosition(0, 1)
		self.itemSlotChance.ArrangeSlot(0, 1, 1, 32, 32, 0, 0)
		self.itemSlotChance.SetSlotBaseImage("d:/ymir work/ui/game/comp/storage/slot.png", 1.0, 1.0, 1.0, 1.0)
		self.itemSlotChance.SetItemSlot(0, self.BIOLOG_ADDITIONAL_ITEMS[1], 0)
		self.itemSlotChance.SetOverInItemEvent(ui.__mem_func__(self.OnOverInItemChance))
		self.itemSlotChance.SetOverOutItemEvent(ui.__mem_func__(self.OnOverOutItem))
		self.itemSlotChance.SetWindowHorizontalAlignCenter()
		self.itemSlotChance.Show()

		self.btnShop = ui.Button()
		self.btnShop.SetParent(self.boardAfter)
		self.btnShop.SetUpVisual(PATH_ROOT + "shop-btn-1.png")
		self.btnShop.SetOverVisual(PATH_ROOT + "shop-btn-2.png")
		self.btnShop.SetDownVisual(PATH_ROOT + "shop-btn-3.png")
		self.btnShop.SetPosition(130, 155)
		self.btnShop.SetWindowHorizontalAlignCenter()
		self.btnShop.SetToolTipText("Magazin biolog")
		self.btnShop.SetEvent(ui.__mem_func__(self.RequestShop))
		self.btnShop.Show()	
		

		self.SetSize(self.Board.GetWidth(), self.Board.GetHeight())
		
	def BindInterface(self, interface):
		self.interface = proxy(interface)
		
	def ResetBiologTime(self):
		net.SendChatPacket("/reset_time_biolog")

	def RequestShop(self):
		net.SendRemoteShopPacket(6)
		
	def SelectNoCooldown(self):
		self.itemRequired = player.GetItemCountByVnum(self.BIOLOG_ADDITIONAL_ITEMS[1])
		if self.itemRequired == 0:
			chat.AppendChat(1, localeInfo.DONT_HAVE_NECESARY_ITEM)
			self.AdditionalCheckbox[0].SetChecked(0)
			return
			
		if self.AdditionalCheckbox[0].IsChecked() and self.itemRequired > 0:
			chat.AppendChat(1, localeInfo.NOT_HAVE_COOLDOWN)
		elif self.itemRequired == 0:
			chat.AppendChat(1, localeInfo.DONT_HAVE_NECESARY_ITEM)
		
	def SetNotification(self):
		if self.AdditionalCheckbox[2].IsChecked():
			constInfo.ENABLE_BIO_NOTIF = 1
		else:
			constInfo.ENABLE_BIO_NOTIF = 0

	def SelectNoFail(self):
		self.itemChance = player.GetItemCountByVnum(self.BIOLOG_ADDITIONAL_ITEMS[0])
		if self.itemChance == 0:
			chat.AppendChat(1, localeInfo.DONT_HAVE_NECESARY_ITEM)
			self.AdditionalCheckbox[1].SetChecked(0)
			return
			
		if self.AdditionalCheckbox[1].IsChecked() and self.itemChance > 0:
			chat.AppendChat(1, localeInfo.HAVE_100_CHANCE)
		elif self.itemChance == 0:
			chat.AppendChat(1, localeInfo.DONT_HAVE_NECESARY_ITEM)

	def OneHundreadPercent(self):
		Baits = [8604]
		Baitcount = 0
		for bait in Baits:
			Baitcount += player.GetItemCountByVnum(bait)
		if Baitcount <= 0:
			return 0
		else:
			for InventorySlot in xrange(player.INVENTORY_PAGE_SIZE*4):
				ItemValue = player.GetItemIndex(InventorySlot)
				try:
					Baits.index(ItemValue)
					net.SendItemUsePacket(InventorySlot)
					return 1
				except:
					pass

	def SendBiologItem(self):
		if self.AdditionalCheckbox[0].IsChecked() and constInfo.END_TIME_BIO > 1:
			self.ResetBiologTime()
		if self.AdditionalCheckbox[1].IsChecked() and constInfo.END_TIME_BIO > 1:
			self.OneHundreadPercent()
	
		net.SendChatPacket("/delivery_biolog")

	def SetItemToolTip(self, itemTooltip):
		self.tooltipItem = itemTooltip

	def Destroy(self):
		self.ClearDictionary()	
		self.tooltipItem = None
		self.bLoadedInfo = False
		self.boardAfter = False
		self.AdditionalCheckbox = False
		
	def Close(self):
		if self.tooltipItem:
			self.tooltipItem.HideToolTip()
			
		self.Hide()
		
	def Show(self):
		if self.bLoadedInfo == False:
			net.SendChatPacket("/open_biolog")
	
		self.SetTop()
		self.SetCenterPosition()
		ui.ScriptWindow.Show(self)

	def OnPressEscapeKey(self):
		self.Close()
		return True
		
	def OnOverInItem(self):
		if self.tooltipItem:
			if self.vnumGlobal:
				self.tooltipItem.ClearToolTip()
				self.tooltipItem.AddItemData(self.vnumGlobal, [0, 0, 0], [(0, 0), (0, 0), (0, 0), (0, 0), (0, 0), (0, 0), (0, 0)])

	def OnOverInItemReward(self, slotIndex):
		if self.tooltipItem:
			if self.vnumGlobal:
				self.tooltipItem.ClearToolTip()
				if self.RewardItemVnum:
					self.tooltipItem.SetItemToolTip(self.RewardItemVnum)
				
	def OnOverOutItem(self):
		if self.tooltipItem:
			self.tooltipItem.HideToolTip()
	
	def OnOverInItemReset(self):
		item = self.BIOLOG_ADDITIONAL_ITEMS[0]
		if self.tooltipItem:
			self.tooltipItem.ClearToolTip()
			self.tooltipItem.SetItemToolTip(item, 0)
		
	def OnOverInItemChance(self):
		item = self.BIOLOG_ADDITIONAL_ITEMS[1]
		if self.tooltipItem:
			self.tooltipItem.ClearToolTip()
			self.tooltipItem.SetItemToolTip(item, 0)
	
	def SecondToDHMS(self, time):
		second = int(time % 60)
		minute = int((time / 60) % 60)
		hour = int((time / 60) / 60) % 24
		day = int(int((time / 60) / 60) / 24)

		text = ""

		if day > 0:
			text += str(day) + "Zile"
			text += " "

		if hour > 0:
			text += str(hour) + "Ore"
			text += " "

		if minute > 0:
			text += str(minute) + "Minute"
			text += " "

		if second > 0:
			text += str(second) + "Secunde"

		return text
	
	def SplitStringBonus(self, text, IsGetVal):
		txtNr = ""
		for index in xrange(len(text)):
			txt = text[index]
			
			if txt.isdigit():
				if IsGetVal:
					txtNr += txt
				else:
					return text[:index]
		
		if IsGetVal:
			return txtNr
			
		return text
	
	def SetInfoBonus(self, Index, Type, Value):
		if Type == 0 or Value == 0:
			return

		StringBonus = ""
		try:
			StringBonus = uiToolTip.AFFECT_DICT[Type](Value)
		except Exception:
			return

		if StringBonus == None:
			return
		
		if Index == 0:		
			self.dictRewardBonuses[0].SetText(self.SplitStringBonus(StringBonus, 0) + self.SplitStringBonus(StringBonus, 1) + "%")
		elif Index == 1:		
			self.dictRewardBonuses[1].SetText(self.SplitStringBonus(StringBonus, 0) + self.SplitStringBonus(StringBonus, 1) + "%")
	
	def SetInfoTime(self, leftTime, timeMax):
		leftTimeR = max(0, leftTime)
		
		self.timeMax = timeMax
		self.lastUpdate = app.GetGlobalTimeStamp() + int(leftTimeR)
		constInfo.END_TIME_BIO = self.lastUpdate

	def SetInfoMission(self, iRewardVnum, vnum, actualCount, needCount):
		if vnum == 0:
			return
		
		item.SelectItem(vnum)
	
		self.MissionText.SetText("Misiune : Adu %i |cff8dad80%s" % (int(needCount), item.GetItemName()))
		self.leftItemsText.SetText("%i/%i" % (int(actualCount), int(needCount)))
		self.itemSlot.SetItemSlot(0, vnum)

		self.vnumGlobal = int(vnum)
		self.RewardItemVnum = iRewardVnum
		
		self.percentActual = actualCount
		self.percentTotal = needCount
		
		if iRewardVnum:
			self.itemSlotReward.SetItemSlot(0, iRewardVnum)

	def OnUpdate(self):
		leftTime = max(0, self.lastUpdate - app.GetGlobalTimeStamp())
		if leftTime > 0:
			self.MissionTimeText.SetText(uiScriptLocale.REMAINING_TIME_BIOLOG % (self.SecondToDHMS(int(self.lastUpdate - app.GetGlobalTimeStamp()))))
			self.MissionTime.LoadImage(PATH_ROOT + "deliver_bg_red.png")
		else:
			self.MissionTimeText.SetText(uiScriptLocale.CAN_DELIVER_BIOLOG)
			self.MissionTime.LoadImage(PATH_ROOT + "deliver_bg.png")
			
		xList, yList = self.MissionTitle.GetGlobalPosition()
		
		for item in self.listGauge:
			if item.GetWindowName() == "GaugeBar":
				if self.percentTotal == 0:
					self.percentTotal = 1
				item.SetClipRect(0.0, yList, -1.0 + float(self.percentActual) / float(self.percentTotal), yList + self.MissionTitle.GetHeight(), True)
			else:
				item.SetClipRect(xList, yList, xList + self.MissionTitle.GetWidth(), yList + self.MissionTitle.GetHeight())
