# -*- coding: cp949 -*-
#-1219400332
import CacheEffect as player
import exchange
import net
import localeInfo
import chat
import item
import thenewui as ui
import mouseModule
import uiPickMoney
import wndMgr
import app
import playerSettingModule
import uiCommon
import time
import constInfo
import cfg

FACE_IMAGE_DICT = {
	playerSettingModule.RACE_WARRIOR_M	: "icon/face/warrior_m.tga",
	playerSettingModule.RACE_WARRIOR_W	: "icon/face/warrior_w.tga",
	playerSettingModule.RACE_ASSASSIN_M	: "icon/face/assassin_m.tga",
	playerSettingModule.RACE_ASSASSIN_W	: "icon/face/assassin_w.tga",
	playerSettingModule.RACE_SURA_M		: "icon/face/sura_m.tga",
	playerSettingModule.RACE_SURA_W		: "icon/face/sura_w.tga",
	playerSettingModule.RACE_SHAMAN_M	: "icon/face/shaman_m.tga",
	playerSettingModule.RACE_SHAMAN_W	: "icon/face/shaman_w.tga",
}
if app.ENABLE_WOLFMAN_CHARACTER:
	FACE_IMAGE_DICT.update({playerSettingModule.RACE_WOLFMAN_M  : "icon/face/wolfman_m.tga",})

class ExchangeDialog(ui.ScriptWindow):
	def __init__(self):
		ui.ScriptWindow.__init__(self)
		self.TitleName = 0
		self.tooltipItem = 0
		self.xStart = 0
		self.yStart = 0
		self.usedYang0 = 0
		self.usedYang1 = 0
		self.STOP = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
		self.STOP2 = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
		if app.WJ_ENABLE_TRADABLE_ICON:
			self.interface = 0
			self.wndInventory = 0
			self.lockedItems = {i:(-1,-1) for i in range(exchange.EXCHANGE_ITEM_MAX_NUM)}

	def __del__(self):
		ui.ScriptWindow.__del__(self)

	class Item(ui.ListBoxEx.Item):
		def __init__(self,parent, text, value=0):
			ui.ListBoxEx.Item.__init__(self)
			self.textBox=ui.TextLine()
			self.textBox.SetParent(self)
			self.textBox.SetText(text)
			self.textBox.Show()
			self.value = value

		def GetValue(self):
			return self.value

		def __del__(self):
			ui.ListBoxEx.Item.__del__(self)

	def LoadDialog(self):
		PythonScriptLoader = ui.PythonScriptLoader()
		if app.ENABLE_NEW_EXCHANGE_WINDOW:
			PythonScriptLoader.LoadScriptFile(self, "UIScript/exchangedialog_new.py")
		else:
			PythonScriptLoader.LoadScriptFile(self, "UIScript/exchangedialog.py")

		## Owner
		self.OwnerSlot = self.GetChild("Owner_Slot")
		self.OwnerSlot.SetSelectEmptySlotEvent(ui.__mem_func__(self.SelectOwnerEmptySlot))
		self.OwnerSlot.SetSelectItemSlotEvent(ui.__mem_func__(self.SelectOwnerItemSlot))
		self.OwnerSlot.SetUnselectItemSlotEvent(ui.__mem_func__(self.UnselectItemSlotSelf))
		self.OwnerSlot.SetOverInItemEvent(ui.__mem_func__(self.OverInOwnerItem))
		self.OwnerSlot.SetOverOutItemEvent(ui.__mem_func__(self.OverOutItem))
		self.OwnerSlot.SetSlotBaseImage("d:/ymir work/ui/public/Slot_Base.sub", 1.0, 1.0, 1.0, 1.0)	

		self.OwnerMoney = self.GetChild("Owner_Money_Value")
		self.Owner_Overlay = self.GetChild("Owner_Overlay")
		self.Owner_Overlay.Hide()
		self.OwnerMoneyButton = self.GetChild("Owner_Money")
		self.OwnerMoneyButton.SetEvent(ui.__mem_func__(self.OpenPickMoneyDialog))

		## Target
		self.TargetSlot = self.GetChild("Target_Slot")
		self.TargetSlot.SetOverInItemEvent(ui.__mem_func__(self.OverInTargetItem))
		self.TargetSlot.SetUnselectItemSlotEvent(ui.__mem_func__(self.UnselectItemSlotTarget))
		self.TargetSlot.SetOverOutItemEvent(ui.__mem_func__(self.OverOutItem))
		self.TargetMoney = self.GetChild("Target_Money_Value")
		self.Target_Overlay = self.GetChild("Target_Overlay")
		self.Target_Overlay.Hide()
		self.TargetSlot.SetSlotBaseImage("d:/ymir work/ui/public/Slot_Base.sub", 1.0, 1.0, 1.0, 1.0)	
		## PickMoneyDialog
		dlgPickMoney = uiPickMoney.PickMoneyDialog()
		dlgPickMoney.LoadDialog()
		dlgPickMoney.SetAcceptEvent(ui.__mem_func__(self.OnPickMoney))
		dlgPickMoney.SetTitleName(localeInfo.EXCHANGE_MONEY)
		dlgPickMoney.SetMax(13)
		dlgPickMoney.Hide()
		self.dlgPickMoney = dlgPickMoney

		## Button
		self.TitleName = self.GetChild("TitleName")
		self.GetChild("TitleBar").SetCloseEvent(net.SendExchangeExitPacket)

		self.Middle_Exchange_Button = self.GetChild("Middle_Exchange_Button")
		self.Middle_Exchange_Button.SetUpVisual("d:/ymir work/ui/game/exchange/none_ready_button.tga")
		self.Middle_Exchange_Button.SetOverVisual("d:/ymir work/ui/game/exchange/none_ready_button_over.tga")
		self.Middle_Exchange_Button.SetDownVisual("d:/ymir work/ui/game/exchange/none_ready_button_down.tga")		
		self.Middle_Exchange_Button.SetToggleDownEvent(ui.__mem_func__(self.AcceptExchange))

		self.ExchangeLogs = self.GetChild("ExchangeLogs")
		self.LogsScrollBar = ui.ThinScrollBar()
		self.LogsScrollBar.SetParent(self.ExchangeLogs)
		self.LogsScrollBar.SetPosition(442 - 65, 17)
		self.LogsScrollBar.SetScrollBarSize(70)
		self.LogsScrollBar.Show()
		self.LogsDropList = ui.ListBoxEx()
		self.LogsDropList.SetParent(self.ExchangeLogs)
		self.LogsDropList.itemHeight = 12
		self.LogsDropList.itemStep = 13
		self.LogsDropList.append_left = True
		self.LogsDropList.SetPosition(10, 15)
		self.LogsDropList.SetSize(0, 150)
		self.LogsDropList.SetScrollBar(self.LogsScrollBar)
		self.LogsDropList.SetViewItemCount(5)
		self.LogsDropList.SetBasePos(0)
		self.LogsDropList.Show()

	def Destroy(self):
		self.ClearDictionary()
		self.dlgPickMoney.Destroy()
		self.dlgPickMoney = 0
		self.OwnerSlot = 0
		self.OwnerMoney = 0
		self.Owner_Overlay = 0
		self.OwnerMoneyButton = 0
		self.TargetSlot = 0
		self.TargetMoney = 0
		self.Middle_Exchange_Button = 0
		self.Target_Overlay = 0
		self.TitleName = 0

		self.tooltipItem = 0
		self.LogsDropList.RemoveAllItems()
		self.LogsScrollBar = None
		self.LogsDropList = None
		self.usedYang0 = 0
		self.usedYang1 = 0
		if app.WJ_ENABLE_TRADABLE_ICON:
			self.interface = 0
			self.wndInventory = 0
			self.lockedItems = {i:(-1,-1) for i in range(exchange.EXCHANGE_ITEM_MAX_NUM)}

	def OpenDialog(self):
		self.TitleName.SetText(localeInfo.EXCHANGE_TITLE_LEVEL % (exchange.GetNameFromTarget(), exchange.GetLevelFromTarget()))
		self.Show()
		self.SetTop()

		(self.xStart, self.yStart, z) = player.GetMainCharacterPosition()
		
		self.GetChild("Target_Name").SetText(str(exchange.GetNameFromTarget()))
		self.GetChild("Target_Level").SetText("Lv." + str(exchange.GetLevelFromTarget()))
		self.GetChild("Owner_Name_Value").SetText(str(exchange.GetNameFromSelf()))	
		self.GetChild("Owner_Level_Value").SetText("Lv." + str(exchange.GetLevelFromSelf()))	
		
		if exchange.GetRaceFromSelf() not in FACE_IMAGE_DICT:
			self.GetChild("OwnerFaceImage").LoadImage("icon/face/poly_face.tga")
		else:
			self.GetChild("OwnerFaceImage").LoadImage(FACE_IMAGE_DICT[exchange.GetRaceFromSelf()])
		
		if exchange.GetRaceFromTarget() not in FACE_IMAGE_DICT:
			self.GetChild("TargetFaceImage").LoadImage("icon/face/poly_face.tga")
		else:
			self.GetChild("TargetFaceImage").LoadImage(FACE_IMAGE_DICT[exchange.GetRaceFromTarget()])	
		
		self.LogsDropList.RemoveAllItems()
		# self.LogsDropList.AppendItem(self.Item(self, localeInfo.NEW_EXCHANGE_YOU_READY % (str(time.strftime("[%H:%M:%S]"))), 0))
		self.LogsDropList.AppendItem(self.Item(self, "%s Negotul a inceput." % (str(time.strftime("[%H:%M:%S]"))), 0))	

		if app.WJ_ENABLE_TRADABLE_ICON:
			self.interface.SetOnTopWindow(player.ON_TOP_WND_EXCHANGE)
			self.interface.RefreshMarkInventoryBag()

		# (self.xStart, self.yStart, z) = player.GetMainCharacterPosition()

	def CloseDialog(self):
		wndMgr.OnceIgnoreMouseLeftButtonUpEvent()

		if 0 != self.tooltipItem:
			self.tooltipItem.HideToolTip()

		self.dlgPickMoney.Close()
		self.Hide()
		self.usedYang0 = 0
		self.usedYang1 = 0
		self.STOP = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
		self.STOP2 = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
		if app.WJ_ENABLE_TRADABLE_ICON:
			for exchangePos, (itemInvenPage, itemSlotPos) in self.lockedItems.items():
				if itemInvenPage == self.wndInventory.GetInventoryPageIndex():
					self.wndInventory.wndItem.SetCanMouseEventSlot(itemSlotPos)

			self.lockedItems = {i:(-1,-1) for i in range(exchange.EXCHANGE_ITEM_MAX_NUM)}
			self.interface.SetOnTopWindow(player.ON_TOP_WND_NONE)
			self.interface.RefreshMarkInventoryBag()

	def SetItemToolTip(self, tooltipItem):
		self.tooltipItem = tooltipItem

	def OpenPickMoneyDialog(self):
		if exchange.GetElkFromSelf() > 0:
			chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.EXCHANGE_CANT_EDIT_MONEY)
			return

		self.dlgPickMoney.Open(player.GetElk())

	def OnPickMoney(self, money):
		net.SendExchangeElkAddPacket(money)

	def AcceptExchange(self):
		iCountTarget = 0
		iCountSelf = 0
		for i in xrange(exchange.EXCHANGE_ITEM_MAX_NUM):
			itemIndex = exchange.GetItemVnumFromTarget(i)
			if (itemIndex != 0):
				iCountTarget = iCountTarget + 1
				
		for i in xrange(exchange.EXCHANGE_ITEM_MAX_NUM):
			itemIndex = exchange.GetItemVnumFromSelf(i)
			if (itemIndex != 0):
				iCountSelf = iCountSelf + 1

		if iCountTarget == 0 and iCountSelf != 0:
			acceptQuestionDialog = uiCommon.QuestionDialog2()
			acceptQuestionDialog.SetText1(localeInfo.NEW_EXCHANGE_ALERT1)
			acceptQuestionDialog.SetText2(localeInfo.NEW_EXCHANGE_ALERT2)
			acceptQuestionDialog.SetAcceptEvent(lambda arg=True: self.AcceptNegot(arg))
			acceptQuestionDialog.SetCancelEvent(lambda arg=False: self.AcceptNegot(arg))
			acceptQuestionDialog.Open()
			self.acceptQuestionDialog = acceptQuestionDialog
		else:
			net.SendExchangeAcceptPacket()

	def AcceptNegot(self, flag):
		if (flag):
			net.SendExchangeAcceptPacket()
			
		self.acceptQuestionDialog = None	
		self.Middle_Exchange_Button.SetUpVisual("d:/ymir work/ui/game/exchange/none_ready_button.tga")
		self.Middle_Exchange_Button.SetOverVisual("d:/ymir work/ui/game/exchange/none_ready_button_over.tga")
		self.Middle_Exchange_Button.SetDownVisual("d:/ymir work/ui/game/exchange/none_ready_button_down.tga")
		self.Middle_Exchange_Button.Enable()

	def SelectOwnerEmptySlot(self, SlotIndex):
		if False == mouseModule.mouseController.isAttached():
			return

		if mouseModule.mouseController.IsAttachedMoney():
			net.SendExchangeElkAddPacket(mouseModule.mouseController.GetAttachedMoneyAmount())
		else:
			attachedSlotType = mouseModule.mouseController.GetAttachedType()
			if (player.SLOT_TYPE_INVENTORY == attachedSlotType or player.SLOT_TYPE_DRAGON_SOUL_INVENTORY == attachedSlotType):
				attachedInvenType = player.SlotTypeToInvenType(attachedSlotType)
				SrcSlotNumber = mouseModule.mouseController.GetAttachedSlotNumber()
				DstSlotNumber = SlotIndex

				itemID = player.GetItemIndex(attachedSlotType, SrcSlotNumber)
				item.SelectItem(itemID)

				if item.IsAntiFlag(item.ANTIFLAG_GIVE):
					chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.EXCHANGE_CANNOT_GIVE)
					mouseModule.mouseController.DeattachObject()
					return

				net.SendExchangeItemAddPacket(attachedInvenType, SrcSlotNumber, DstSlotNumber)

		mouseModule.mouseController.DeattachObject()

	def SelectOwnerItemSlot(self, SlotIndex):
		if player.ITEM_MONEY == mouseModule.mouseController.GetAttachedItemIndex():
			money = mouseModule.mouseController.GetAttachedItemCount()
			net.SendExchangeElkAddPacket(money)

	def UnselectItemSlotSelf(self, slotIndex):
		if app.IsPressed(app.DIK_LSHIFT):
			itemVnum =  exchange.GetItemVnumFromSelf(slotIndex)

			self.tooltipItem.ModelPreviewFull(itemVnum)

	def UnselectItemSlotTarget(self, slotIndex):
		if app.IsPressed(app.DIK_LSHIFT):
			itemVnum =  exchange.GetItemVnumFromTarget(slotIndex)
	
			self.tooltipItem.ModelPreviewFull(itemVnum)

	def RefreshOwnerSlot(self):
		for i in xrange(exchange.EXCHANGE_ITEM_MAX_NUM):
			itemIndex = exchange.GetItemVnumFromSelf(i)
			itemCount = exchange.GetItemCountFromSelf(i)
			if 1 == itemCount:
				itemCount = 0

			self.OwnerSlot.SetItemSlot(i, itemIndex, itemCount)

			if app.ENABLE_CHANGELOOK_SYSTEM:
				itemTransmutedVnum = exchange.GetItemTransmutation(i, True)
				if itemTransmutedVnum:
					self.OwnerSlot.DisableCoverButton(i)
				else:
					self.OwnerSlot.EnableCoverButton(i)

			if itemIndex != 0 and self.STOP[i] == 0:
				item.SelectItem(exchange.GetItemVnumFromSelf(i))
				itemName = item.GetItemName(exchange.GetItemVnumFromSelf(i))
				attrSlot = []
				for j in xrange(player.ATTRIBUTE_SLOT_MAX_NUM):
					attrSlot.append(exchange.GetItemAttributeFromSelf(i, j))

				if attrSlot[0][0] != 0:
					if itemCount != 0:
						self.LogsDropList.AppendItem(self.Item(self, "%s Ai adaugat %sx |cffffc700|H|h[%s]|h|r " % (str(time.strftime("[%H:%M:%S]")), str(itemCount), itemName), 0))
					else:
						self.LogsDropList.AppendItem(self.Item(self, "%s Ai adaugat |cffffc700|H|h[%s]|h|r" % (str(time.strftime("[%H:%M:%S]")), itemName), 0))
				else:
					if itemCount != 0:
						self.LogsDropList.AppendItem(self.Item(self, "%s Ai adaugat %sx [%s]" % (str(time.strftime("[%H:%M:%S]")), str(itemCount), itemName), 0))
					else:
						self.LogsDropList.AppendItem(self.Item(self, "%s Ai adaugat [%s]" % (str(time.strftime("[%H:%M:%S]")), itemName), 0))

				self.STOP[i] = 1

		self.RefreshOwnerBonusedItems()
		self.OwnerSlot.RefreshSlot()

	def RefreshOwnerBonusedItems(self):
		for i in xrange(exchange.EXCHANGE_ITEM_MAX_NUM):
			itemIndex = exchange.GetItemVnumFromSelf(i)
			if itemIndex != 0:
				item.SelectItem(exchange.GetItemVnumFromSelf(i))
				itemSize = item.GetItemSize()
				attrSlot = []
				for j in xrange(player.ATTRIBUTE_SLOT_MAX_NUM):
					attrSlot.append(exchange.GetItemAttributeFromSelf(i, j))

				if attrSlot[4][0] != 0:
					if itemSize == 1:
						self.OwnerSlot.HideSlotBaseImage(i)
					elif itemSize == 2:
						self.OwnerSlot.HideSlotBaseImage(i)
						self.OwnerSlot.HideSlotBaseImage(i+6)
					elif itemSize == 3:
						self.OwnerSlot.HideSlotBaseImage(i)
						self.OwnerSlot.HideSlotBaseImage(i+6)
						self.OwnerSlot.HideSlotBaseImage(i+12)

	def RefreshTargetSlot(self):
		for i in xrange(exchange.EXCHANGE_ITEM_MAX_NUM):
			itemIndex = exchange.GetItemVnumFromTarget(i)
			itemCount = exchange.GetItemCountFromTarget(i)
			if 1 == itemCount:
				itemCount = 0

			self.TargetSlot.SetItemSlot(i, itemIndex, itemCount)
			
			if app.ENABLE_CHANGELOOK_SYSTEM:
				itemTransmutedVnum = exchange.GetItemTransmutation(i, False)
				if itemTransmutedVnum:
					self.TargetSlot.DisableCoverButton(i)
				else:
					self.TargetSlot.EnableCoverButton(i)

			if itemIndex != 0 and self.STOP2[i] == 0:
				item.SelectItem(exchange.GetItemVnumFromTarget(i))
				itemName = item.GetItemName(exchange.GetItemVnumFromTarget(i))
				attrSlot = []
				for j in xrange(player.ATTRIBUTE_SLOT_MAX_NUM):
					attrSlot.append(exchange.GetItemAttributeFromTarget(i, j))

				if attrSlot[0][0] != 0:
					if itemCount != 0:
						self.LogsDropList.AppendItem(self.Item(self, "%s %s a adaugat %sx |cffffc700|H|h[%s]|h|r" % (str(time.strftime("[%H:%M:%S]")),exchange.GetNameFromTarget(), str(itemCount), itemName), 0))
					else:
						self.LogsDropList.AppendItem(self.Item(self, "%s %s a adaugat |cffffc700|H|h[%s]|h|r" % (str(time.strftime("[%H:%M:%S]")),exchange.GetNameFromTarget(), itemName), 0))
				else:
					if itemCount != 0:
						self.LogsDropList.AppendItem(self.Item(self, "%s %s a adaugat %sx [%s]" % (str(time.strftime("[%H:%M:%S]")),exchange.GetNameFromTarget(), str(itemCount), itemName), 0))
					else:
						self.LogsDropList.AppendItem(self.Item(self, "%s %s a adaugat [%s]" % (str(time.strftime("[%H:%M:%S]")),exchange.GetNameFromTarget(), itemName), 0))

				self.STOP2[i] = 1

		self.RefreshTargetBonusedItems()
		self.TargetSlot.RefreshSlot()

	def RefreshTargetBonusedItems(self):
		for i in xrange(exchange.EXCHANGE_ITEM_MAX_NUM):
			itemIndex = exchange.GetItemVnumFromTarget(i)
			if itemIndex != 0:
				item.SelectItem(exchange.GetItemVnumFromTarget(i))
				itemSize = item.GetItemSize()
				attrSlot = []
				for j in xrange(player.ATTRIBUTE_SLOT_MAX_NUM):
					attrSlot.append(exchange.GetItemAttributeFromTarget(i, j))

				if attrSlot[4][0] != 0:
					if itemSize == 1:
						self.TargetSlot.HideSlotBaseImage(i)
					elif itemSize == 2:
						self.TargetSlot.HideSlotBaseImage(i)
						self.TargetSlot.HideSlotBaseImage(i+6)
					elif itemSize == 3:
						self.TargetSlot.HideSlotBaseImage(i)
						self.TargetSlot.HideSlotBaseImage(i+6)
						self.TargetSlot.HideSlotBaseImage(i+12)

	def Refresh(self):
		self.RefreshOwnerSlot()
		self.RefreshTargetSlot()
		if app.WJ_ENABLE_TRADABLE_ICON:
			self.RefreshLockedSlot()

		self.OwnerMoney.SetText(str(localeInfo.AddPointToNumberString(exchange.GetElkFromSelf())))
		self.TargetMoney.SetText(str(localeInfo.AddPointToNumberString(exchange.GetElkFromTarget())))

		if True == exchange.GetAcceptFromSelf():
			self.Middle_Exchange_Button.SetUpVisual("d:/ymir work/ui/game/exchange/player_ready_button.tga")
			self.Middle_Exchange_Button.SetOverVisual("d:/ymir work/ui/game/exchange/player_ready_button_over.tga")
			self.Middle_Exchange_Button.SetDownVisual("d:/ymir work/ui/game/exchange/player_ready_button_down.tga")
			self.Middle_Exchange_Button.Disable()
			self.Owner_Overlay.Show()
			# self.LogsDropList.AppendItem(self.Item(self, "%s Ai acceptat negotul." % (str((time.strftime("[%H:%M:%S]")))), 0))
			self.LogsDropList.AppendItem(self.Item(self, localeInfo.NEW_EXCHANGE_YOU_ACCEPT % (str((time.strftime("[%H:%M:%S]")))), 0))
		elif True == exchange.GetAcceptFromTarget():
			self.Target_Overlay.Show()
			self.Middle_Exchange_Button.SetUpVisual("d:/ymir work/ui/game/exchange/target_ready_button.tga")
			self.Middle_Exchange_Button.SetOverVisual("d:/ymir work/ui/game/exchange/target_ready_button_over.tga")
			self.Middle_Exchange_Button.SetDownVisual("d:/ymir work/ui/game/exchange/target_ready_button_down.tga")	
			# self.LogsDropList.AppendItem(self.Item(self, "%s %s a acceptat negotul." % (str((time.strftime("[%H:%M:%S]"))), exchange.GetNameFromTarget()), 0))
			self.LogsDropList.AppendItem(self.Item(self, localeInfo.NEW_EXCHANGE_ACCEPT % (str((time.strftime("[%H:%M:%S]"))), exchange.GetNameFromTarget()), 0))
		else:
			self.Target_Overlay.Hide()
			self.Middle_Exchange_Button.SetUpVisual("d:/ymir work/ui/game/exchange/none_ready_button.tga")
			self.Middle_Exchange_Button.SetOverVisual("d:/ymir work/ui/game/exchange/none_ready_button_over.tga")
			self.Middle_Exchange_Button.SetDownVisual("d:/ymir work/ui/game/exchange/none_ready_button_down.tga")			
			self.Middle_Exchange_Button.Enable()
			self.Owner_Overlay.Hide()

		if exchange.GetElkFromSelf() != 0 and self.usedYang0 == 0:
			self.LogsDropList.AppendItem(self.Item(self, "%s Ai crescut suma de Yang la |cffb8ff00|H|h%s|h|r" % (str(time.strftime("[%H:%M:%S]")), localeInfo.AddPointToNumberString(exchange.GetElkFromSelf())), 0))
			self.usedYang0 = 1
		elif exchange.GetElkFromTarget() != 0 and self.usedYang1 == 0:
			self.LogsDropList.AppendItem(self.Item(self, "%s %s a crescut suma de Yang la |cffb8ff00|H|h%s|h|r" % (str(time.strftime("[%H:%M:%S]")), str(exchange.GetNameFromTarget()), localeInfo.AddPointToNumberString(exchange.GetElkFromTarget())), 0))
			self.usedYang1 = 1

	def OverInOwnerItem(self, slotIndex):
		if 0 != self.tooltipItem:
			self.tooltipItem.SetExchangeOwnerItem(slotIndex)

	def OverInTargetItem(self, slotIndex):
		if 0 != self.tooltipItem:
			self.tooltipItem.SetExchangeTargetItem(slotIndex)

	def OverOutItem(self):
		if 0 != self.tooltipItem:
			self.tooltipItem.HideToolTip()

	def OnTop(self):
		self.tooltipItem.SetTop()
		if app.WJ_ENABLE_TRADABLE_ICON:
			if self.interface:
				self.interface.SetOnTopWindow(player.ON_TOP_WND_EXCHANGE)
				self.interface.RefreshMarkInventoryBag()

	def OnUpdate(self):
		USE_EXCHANGE_LIMIT_RANGE = 1000

		(x, y, z) = player.GetMainCharacterPosition()
		if abs(x - self.xStart) > USE_EXCHANGE_LIMIT_RANGE or abs(y - self.yStart) > USE_EXCHANGE_LIMIT_RANGE:
			(self.xStart, self.yStart, z) = player.GetMainCharacterPosition()
			net.SendExchangeExitPacket()

	if app.WJ_ENABLE_TRADABLE_ICON:
		def CantTradableItem(self, destSlotIndex, srcSlotIndex):
			if True == exchange.GetAcceptFromTarget():
				return

			itemInvenPage = srcSlotIndex / player.INVENTORY_PAGE_SIZE
			localSlotPos = srcSlotIndex - (itemInvenPage * player.INVENTORY_PAGE_SIZE)
			self.lockedItems[destSlotIndex] = (itemInvenPage, localSlotPos)

			if self.wndInventory.GetInventoryPageIndex() == itemInvenPage and self.IsShow():
				self.wndInventory.wndItem.SetCantMouseEventSlot(localSlotPos)

		def RefreshLockedSlot(self):
			if self.wndInventory:
				for exchangePos, (itemInvenPage, itemSlotPos) in self.lockedItems.items():
					if self.wndInventory.GetInventoryPageIndex() == itemInvenPage:
						self.wndInventory.wndItem.SetCantMouseEventSlot(itemSlotPos)

				self.wndInventory.wndItem.RefreshSlot()

		def BindInterface(self, interface):
			self.interface = interface

		def SetInven(self, wndInventory):
			from _weakref import proxy
			self.wndInventory = proxy(wndInventory)