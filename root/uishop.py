import net
import CacheEffect as player
import item
import shop
import net
import wndMgr
import app
import chat
import thenewui as ui
import uiCommon
import mouseModule
import localeInfo
import uiScriptLocale
import cfg
import constInfo
import uiPickItem
if app.ENABLE_OFFLINE_SHOP:
	import uiPickMoney
	import time
	import background
	import itemprices

class ShopDialog(ui.ScriptWindow):
	BOX_WIDTH = 368 - 23

	def __init__(self):
		ui.ScriptWindow.__init__(self)
		self.tooltipItem = 0
		self.questionDialog = None
		self.popup = None
		self.isOfflineShop = None
		self.itemBuyQuestionDialog = None
		self.dlgPickItem = None
		self.itemlockQuestionDialog = None
		self.oldNameLine = None
		self.isEditing = 0
		if app.WJ_ENABLE_TRADABLE_ICON:
			self.interface = None
		if app.ENABLE_OFFLINE_SHOP:
			self.priceInputBoard = None
		self.temporaryItems = {}	

	def __del__(self):
		ui.ScriptWindow.__del__(self)

	def __GetRealIndex(self, i):
		return self.tabIdx * shop.SHOP_SLOT_COUNT + i

	def GetEmptySlots(self):
		emptyLines = 8
		for i in xrange(10):
			empty = 8
			for j in xrange(8):
				itemIndex = shop.GetItemID(10 * j + i)
				if itemIndex > 0:
					item.SelectItem(itemIndex)
					(w, h) = item.GetItemSize()
					empty -= h
			emptyLines = min(emptyLines, empty)
		return emptyLines

	def Refresh(self):
		getItemID=shop.GetItemID
		getItemCount=shop.GetItemCount
		setItemID=self.itemSlotWindow.SetItemSlot
		for i in xrange(shop.SHOP_SLOT_COUNT):
			idx = self.__GetRealIndex(i)
			itemCount = getItemCount(idx)

			if itemCount <= 1:
				itemCount = 0
			setItemID(i, getItemID(idx), itemCount)

			if app.ENABLE_CHANGELOOK_SYSTEM:
				itemTransmutedVnum = shop.GetItemTransmutation(i)
				if itemTransmutedVnum == 0 and i in self.temporaryItems:
					itemTransmutedVnum = self.temporaryItems[i]
				if itemTransmutedVnum:
					self.itemSlotWindow.DisableCoverButton(i)
				else:
					self.itemSlotWindow.EnableCoverButton(i)

		wndMgr.RefreshSlot(self.itemSlotWindow.GetWindowHandle())

	def SetItemData(self, pos, itemID, itemCount, itemPrice):
		shop.SetItemData(pos, itemID, itemCount, itemPrice)
		
	def LoadDialog(self):
		try:
			PythonScriptLoader = ui.PythonScriptLoader()
			if app.ENABLE_OFFLINE_SHOP:
				PythonScriptLoader.LoadScriptFile(self, "UIScript/shopdialognew_norm.py")
			else:
				PythonScriptLoader.LoadScriptFile(self, "UIScript/shopdialog.py")
		except:
			import exception
			exception.Abort("ShopDialog.LoadDialog.LoadObject")

		try:
			GetObject = self.GetChild
			self.itemSlotWindow = GetObject("ItemSlot")
			self.Board = GetObject("board")
			self.titleBar = GetObject("TitleBar")
			self.titleName = GetObject("TitleName")
			self.btnClose = GetObject("CloseButton")
			if app.ENABLE_OFFLINE_SHOP:
				self.offShopPanel = GetObject("OffShopPanel")
				self.locationText = GetObject("LocationText")
				self.totalNetworth = GetObject("TotalNetworth")
				self.closeOffshop = GetObject("CloseOffshop")
				self.lockButton = GetObject("LockButton")
				self.timeText = GetObject("TimeText")
				self.searchShop = GetObject("SearchShop")
				self.goldButton = GetObject("MoneySlot")
				self.goldText = GetObject("Money")
				self.goldAmount = 0
				self.expireTime = 0
		except:
			import exception
			exception.Abort("ShopDialog.LoadDialog.BindObject")

		self.itemSlotWindow.SetSlotStyle(wndMgr.SLOT_STYLE_NONE)
		self.itemSlotWindow.SAFE_SetButtonEvent("LEFT", "EMPTY", self.SelectEmptySlot)
		self.itemSlotWindow.SAFE_SetButtonEvent("LEFT", "EXIST", self.SelectItemSlot)
		self.itemSlotWindow.SAFE_SetButtonEvent("RIGHT", "EXIST", self.UnselectItemSlot)

		self.itemSlotWindow.SetOverInItemEvent(ui.__mem_func__(self.OverInItem))
		self.itemSlotWindow.SetOverOutItemEvent(ui.__mem_func__(self.OverOutItem))

		self.btnClose.SetEvent(ui.__mem_func__(self.AskClosePrivateShop))
		
		self.titleBar.SetCloseEvent(ui.__mem_func__(self.Close))
		if app.ENABLE_OFFLINE_SHOP:
			self.goldButton.SetEvent(ui.__mem_func__(self.OpenPickMoneyDialog))
			self.lockButton.SetEvent(ui.__mem_func__(self.SetLock))
			self.closeOffshop.SetEvent(ui.__mem_func__(self.CloseShop))
			self.searchShop.SetEvent(ui.__mem_func__(self.OpenSearch))

			self.dlgPickMoney = uiPickMoney.PickMoneyDialog()
			self.dlgPickMoney.SetAcceptEvent(ui.__mem_func__(self.OnPickMoney))
			self.dlgPickMoney.LoadDialog()
			self.dlgPickMoney.SetMax(16)
			self.dlgPickMoney.Hide()
			
			self.NameSlotBar = ui.ImageBox()
			self.NameSlotBar.SetParent(self.offShopPanel)
			self.NameSlotBar.SetPosition(2, 1)
			self.NameSlotBar.LoadImage("d:/ymir work/ui/shop/namefield.png")
			self.NameSlotBar.Show()

			self.nameLine = ui.EditLine()
			self.nameLine.SetParent(self.NameSlotBar)
			self.nameLine.SetPosition(5, 5)
			self.nameLine.SetSize(167, 18)
			self.nameLine.SetMax(30)
			self.nameLine.Show()
			
			self.searchShop.SetToolTipText(localeInfo.SEARCH_OBJECT)
			self.closeOffshop.SetToolTipText(uiScriptLocale.PRIVATE_SHOP_CLOSE_BUTTON)
	
			self.nameLine.SetReturnEvent(ui.__mem_func__(self.OnChangeShopName))
			self.nameLine.OnIMEUpdate = ui.__mem_func__(self.OnNameUpdate)
			
		self.tabIdx = 0
		self.coinType = shop.SHOP_COIN_TYPE_GOLD
		
		dlgPickItem = uiPickItem.PickItemDialog()
		dlgPickItem.LoadDialog()
		dlgPickItem.Hide()
		self.dlgPickItem = dlgPickItem
		
		self.Refresh()

	def Destroy(self):
		if app.WJ_ENABLE_TRADABLE_ICON:
			self.Close(True)
			self.interface = None
		else:
			self.Close()
		self.ClearDictionary()

		self.tooltipItem = 0
		self.itemSlotWindow = 0
		self.titleBar = 0
		self.btnClose = 0
		self.questionDialog = None
		self.popup = None
		self.dlgPickItem.Destroy()
		self.dlgPickItem = 0
		if app.ENABLE_OFFLINE_SHOP:
			self.goldButton = None
			self.goldText = None
			self.dlgPickMoney.Destroy()
			self.dlgPickMoney = None
			self.priceInputBoard = None
			
	def Open(self, vid, extraInfo = False):

		isPrivateShop = False
		isMainPlayerPrivateShop = False

		import Collision as chr
		if chr.IsNPC(vid):
			isPrivateShop = False
			# self.isOfflineShop = True

		else:
			isPrivateShop = True
			# self.isOfflineShop = True

		self.NPCList = [30000, 30001, 30002, 30003, 30004, 30005, 30006, 30007, 30008]
		wnd_height = 380
		wnd_width = 348
		self.tabIdx = 0
		
		if chr.GetVirtualNumber(vid) in self.NPCList:
			self.isOfflineShop = True
		else:
			self.isOfflineShop = False

		
		if app.ENABLE_OFFLINE_SHOP:
			if shop.IsOwner():
				self.Board.SetSize(wnd_width, wnd_height)
				self.SetSize(wnd_width, wnd_height)
				self.itemSlotWindow.SetPosition(13, 85)
				self.itemSlotWindow.ArrangeSlot(0, 10, 8, 32, 32, 0, 0)
				self.titleName.SetText(uiScriptLocale.HOME_PAGE_OFFSHOP)
				self.offShopPanel.Show()
				self.goldAmount = shop.GetGoldAmount()
				self.goldText.SetText(localeInfo.NumberToMoneyString(self.goldAmount))
			else:
				self.offShopPanel.Hide()
				self.itemSlotWindow.SetSlotStyle(wndMgr.SLOT_STYLE_NONE)
				wnd_height = 145 + 32 * 5
				self.Board.SetSize(self.BOX_WIDTH, wnd_height)
				self.SetSize(self.BOX_WIDTH, wnd_height)
				self.itemSlotWindow.SetPosition(12, 34)
				self.itemSlotWindow.ArrangeSlot(0, 10, 8, 32, 32, 0, 0)
				self.titleName.SetText(uiScriptLocale.SHOP_TITLE)
				
		if player.IsMainCharacterIndex(vid):
			isMainPlayerPrivateShop = True
			self.btnClose.Show()
		else:
			if not chr.GetVirtualNumber(vid) in self.NPCList and extraInfo == False:
				EMPTY_SLOTS = 32 * self.GetEmptySlots()
				self.SetSize(self.BOX_WIDTH, wnd_height - EMPTY_SLOTS)
				self.Board.SetSize(self.BOX_WIDTH, wnd_height - EMPTY_SLOTS)
				self.itemSlotWindow.ArrangeSlot(0, 10, 8 - EMPTY_SLOTS / 32, 32, 32, 0, 0)
			elif extraInfo == True or chr.GetVirtualNumber(vid) in self.NPCList:
				self.Board.SetSize(self.BOX_WIDTH, wnd_height)
				self.SetSize(self.BOX_WIDTH, wnd_height)
				self.itemSlotWindow.ArrangeSlot(0, 10, 8, 32, 32, 0, 0)

			isMainPlayerPrivateShop = False
			self.btnClose.Hide()

		self.itemSlotWindow.SetSlotBaseImage("d:/ymir work/ui/public/Slot_Base.sub", 1.0, 1.0, 1.0, 1.0)

		self.itemSlotWindow.RefreshSlot()

		shop.Open(isPrivateShop, isMainPlayerPrivateShop)

		self.Refresh()
		self.SetTop()
		self.Show()

		if app.WJ_ENABLE_TRADABLE_ICON:
			if not isPrivateShop:
				self.interface.SetOnTopWindow(player.ON_TOP_WND_SHOP)
				self.interface.RefreshMarkInventoryBag()

	def Close(self, isDestroy = False):
		if self.interface:
			self.interface.SetOnTopWindow(player.ON_TOP_WND_NONE)
			
			if not isDestroy:
				self.interface.RefreshMarkInventoryBag()

		if self.itemBuyQuestionDialog:
			self.itemBuyQuestionDialog.Close()
			self.itemBuyQuestionDialog = None
		if self.itemlockQuestionDialog:
			self.itemlockQuestionDialog.Close()
			self.itemlockQuestionDialog = None
			constInfo.SET_ITEM_QUESTION_DIALOG_STATUS(0)

		self.OnCloseQuestionDialog()
		self.OnCloseQuestionLockDialog()
		shop.Close()
		if app.ENABLE_OFFLINE_SHOP:
			self.dlgPickMoney.Close()
		net.SendShopEndPacket()
		self.CancelShopping()
		self.tooltipItem.HideToolTip()
		self.Hide()

	def GetIndexFromSlotPos(self, slotPos):
		return self.tabIdx * shop.SHOP_SLOT_COUNT + slotPos

	def AskClosePrivateShop(self):
		questionDialog = uiCommon.QuestionDialog()
		questionDialog.SetText(localeInfo.PRIVATE_SHOP_CLOSE_QUESTION)
		questionDialog.SetAcceptEvent(ui.__mem_func__(self.OnClosePrivateShop))
		questionDialog.SetCancelEvent(ui.__mem_func__(self.OnCloseQuestionDialog))
		questionDialog.Open()
		self.questionDialog = questionDialog

		constInfo.SET_ITEM_QUESTION_DIALOG_STATUS(1)

		return True

	def OnClosePrivateShop(self):
		net.SendChatPacket("/close_shop")
		self.OnCloseQuestionDialog()
		return True

	def OnPressEscapeKey(self):
		self.Close()
		return True

	def OnPressExitKey(self):
		self.Close()
		return True

	def CancelShopping(self):
		app.SetCursor(app.NORMAL)

	def __OnClosePopupDialog(self):
		self.pop = None
		constInfo.SET_ITEM_QUESTION_DIALOG_STATUS(0)

	def SellAttachedItem(self):

		if shop.IsPrivateShop():
			mouseModule.mouseController.DeattachObject()
			return

		attachedSlotType = mouseModule.mouseController.GetAttachedType()
		attachedSlotPos = mouseModule.mouseController.GetAttachedSlotNumber()
		attachedCount = mouseModule.mouseController.GetAttachedItemCount()
		attachedItemIndex = mouseModule.mouseController.GetAttachedItemIndex()

		if player.SLOT_TYPE_INVENTORY == attachedSlotType or\
			player.SLOT_TYPE_DRAGON_SOUL_INVENTORY == attachedSlotType:

			item.SelectItem(attachedItemIndex)

			if item.IsAntiFlag(item.ANTIFLAG_SELL):
				popup = uiCommon.PopupDialog()
				popup.SetText(localeInfo.SHOP_CANNOT_SELL_ITEM)
				popup.SetAcceptEvent(self.__OnClosePopupDialog)
				popup.Open()
				self.popup = popup
				return

			itemtype = player.INVENTORY

			if player.IsValuableItem(itemtype, attachedSlotPos):

				itemPrice = item.GetISellItemPrice()

				itemPrice = itemPrice * max(1, attachedCount)

				itemName = item.GetItemName()

				questionDialog = uiCommon.QuestionDialog()
				questionDialog.SetText(localeInfo.DO_YOU_SELL_ITEM(itemName, attachedCount, itemPrice))

				questionDialog.SetAcceptEvent(lambda arg1=attachedSlotPos, arg2=attachedCount, arg3 = itemtype: self.OnSellItem(arg1, arg2, arg3))
				questionDialog.SetCancelEvent(ui.__mem_func__(self.OnCloseQuestionDialog))
				questionDialog.Open()
				self.questionDialog = questionDialog

				constInfo.SET_ITEM_QUESTION_DIALOG_STATUS(1)

			else:
				self.OnSellItem(attachedSlotPos, attachedCount, itemtype)

		mouseModule.mouseController.DeattachObject()

	def OnSellItem(self, slotPos, count, itemtype):
		net.SendShopSellPacketNew(slotPos, count, itemtype)
		self.OnCloseQuestionDialog()

	def OnCloseQuestionDialog(self):
		if not self.questionDialog:
			return

		self.questionDialog.Close()
		self.questionDialog = None
		constInfo.SET_ITEM_QUESTION_DIALOG_STATUS(0)

	def SelectEmptySlot(self, selectedSlotPos):
		isAttached = mouseModule.mouseController.isAttached()
		if isAttached:
			if app.ENABLE_OFFLINE_SHOP:
				if shop.IsOwner():
					attachedSlotType = mouseModule.mouseController.GetAttachedType()
					attachedSlotPos = mouseModule.mouseController.GetAttachedSlotNumber()
					mouseModule.mouseController.DeattachObject()
					
					if player.SLOT_TYPE_INVENTORY != attachedSlotType and player.SLOT_TYPE_DRAGON_SOUL_INVENTORY != attachedSlotType:
						return
					
					attachedInvenType = player.SlotTypeToInvenType(attachedSlotType)

					itemVNum = player.GetItemIndex(attachedInvenType, attachedSlotPos)
					item.SelectItem(itemVNum)

					if item.IsAntiFlag(item.ANTIFLAG_GIVE) or item.IsAntiFlag(item.ANTIFLAG_MYSHOP):
						chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.PRIVATE_SHOP_CANNOT_SELL_ITEM)
						return

					priceInputBoard = uiCommon.MoneyInputDialog()
					priceInputBoard.SetTitle(localeInfo.PRIVATE_SHOP_INPUT_PRICE_DIALOG_TITLE)
					priceInputBoard.SetAcceptEvent(ui.__mem_func__(self.AcceptInputPrice))
					priceInputBoard.SetCancelEvent(ui.__mem_func__(self.CancelInputPrice))
					priceInputBoard.Open()
					
					if itemVNum in itemprices.PRICE_DICT:
						priceInputBoard.SetValue(itemprices.PRICE_DICT[itemVNum])
					
					self.priceInputBoard = priceInputBoard
					self.priceInputBoard.itemVNum = itemVNum
					self.priceInputBoard.sourceWindowType = attachedInvenType
					self.priceInputBoard.sourceSlotPos = attachedSlotPos
					self.priceInputBoard.targetSlotPos = selectedSlotPos
				else:
					self.SellAttachedItem()
			else:
				self.SellAttachedItem()

	def UnselectItemSlot(self, selectedSlotPos):
		if constInfo.GET_ITEM_QUESTION_DIALOG_STATUS() == 1:
			return
			
		if self.isOfflineShop:
			if app.IsPressed(app.DIK_LSHIFT):
				itemVnum = shop.GetItemID(selectedSlotPos)
				self.tooltipItem.ModelPreviewFull(itemVnum)
			else:
				self.AskBuyItem(selectedSlotPos)
		else:
			if app.IsPressed(app.DIK_LSHIFT):
				itemVnum = shop.GetItemID(selectedSlotPos)
				self.tooltipItem.ModelPreviewFull(itemVnum)
			elif app.IsPressed(app.DIK_LCONTROL):
				itemIndex = shop.GetItemID(selectedSlotPos)
				item.SelectItem(itemIndex)
				itemName = item.GetItemName()
				itemPrice = shop.GetItemPrice(selectedSlotPos)
				itemCount = shop.GetItemCount(selectedSlotPos)
				self.dlgPickItem.SetTitleName(itemName)
				self.dlgPickItem.SetAcceptEvent(ui.__mem_func__(self.OnPickItem))
				self.dlgPickItem.SetItem(itemIndex, itemCount, itemPrice)
				self.dlgPickItem.Open(100)
				self.dlgPickItem.SetMax(3)
				self.dlgPickItem.itemGlobalSlotIndex = selectedSlotPos
			else:
				if app.ENABLE_OFFLINE_SHOP and shop.IsOwner():
					if app.IsPressed(app.DIK_LSHIFT):
						itemVnum = shop.GetItemID(selectedSlotPos)
						self.tooltipItem.ModelPreviewFull(itemVnum)
					else:
						net.SendShopWithdrawItemPacket(self.__GetRealIndex(selectedSlotPos))
				else:
					if app.IsPressed(app.DIK_LSHIFT):
						itemVnum = shop.GetItemID(selectedSlotPos)
						self.tooltipItem.ModelPreviewFull(itemVnum)
					else:
						net.SendShopBuyPacket(self.__GetRealIndex(selectedSlotPos))

		# if not shop.IsPrivateShop():
			# if app.IsPressed(app.DIK_LSHIFT):
				# itemVnum = shop.GetItemID(selectedSlotPos)
				# self.tooltipItem.ModelPreviewFull(itemVnum)
			# elif app.IsPressed(app.DIK_LCONTROL):
				# itemIndex = shop.GetItemID(selectedSlotPos)
				# item.SelectItem(itemIndex)
				# itemName = item.GetItemName()
				# itemPrice = shop.GetItemPrice(selectedSlotPos)
				# itemCount = shop.GetItemCount(selectedSlotPos)
				# self.dlgPickItem.SetTitleName(itemName)
				# self.dlgPickItem.SetAcceptEvent(ui.__mem_func__(self.OnPickItem))
				# self.dlgPickItem.SetItem(itemIndex, itemCount, itemPrice)
				# self.dlgPickItem.Open(100)
				# self.dlgPickItem.SetMax(3)
				# self.dlgPickItem.itemGlobalSlotIndex = selectedSlotPos
			# else:
				# if app.ENABLE_OFFLINE_SHOP and shop.IsOwner():
					# if app.IsPressed(app.DIK_LSHIFT):
						# itemVnum = shop.GetItemID(selectedSlotPos)
						# self.tooltipItem.ModelPreviewFull(itemVnum)
					# else:
						# net.SendShopWithdrawItemPacket(self.__GetRealIndex(selectedSlotPos))
				# else:
					# if app.IsPressed(app.DIK_LSHIFT):
						# itemVnum = shop.GetItemID(selectedSlotPos)
						# self.tooltipItem.ModelPreviewFull(itemVnum)
					# else:
						# net.SendShopBuyPacket(self.__GetRealIndex(selectedSlotPos))

		# elif shop.IsPrivateShop():
			# if app.IsPressed(app.DIK_LSHIFT):
				# itemVnum = shop.GetItemID(selectedSlotPos)
				# self.tooltipItem.ModelPreviewFull(itemVnum)
			# else:
				# self.AskBuyItem(selectedSlotPos)
		# else:
			# if app.ENABLE_OFFLINE_SHOP and shop.IsOwner():
				# if app.IsPressed(app.DIK_LSHIFT):
					# itemVnum = shop.GetItemID(selectedSlotPos)
					# self.tooltipItem.ModelPreviewFull(itemVnum)
				# else:
					# net.SendShopWithdrawItemPacket(self.__GetRealIndex(selectedSlotPos))
			# else:
				# if app.IsPressed(app.DIK_LSHIFT):
					# itemVnum = shop.GetItemID(selectedSlotPos)
					# self.tooltipItem.ModelPreviewFull(itemVnum)
				# else:
					# self.AskBuyItem(selectedSlotPos)

	def SelectItemSlot(self, selectedSlotPos):
		if constInfo.GET_ITEM_QUESTION_DIALOG_STATUS() == 1:
			return

		isAttached = mouseModule.mouseController.isAttached()
		selectedSlotPos = self.__GetRealIndex(selectedSlotPos)
		if isAttached:
			self.SellAttachedItem()

		else:

			if True == shop.IsMainPlayerPrivateShop():
				return

			curCursorNum = app.GetCursor()
			if app.BUY == curCursorNum:
				self.AskBuyItem(selectedSlotPos)

			elif app.SELL == curCursorNum:
				chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.SHOP_SELL_INFO)

			else:
				selectedItemID = shop.GetItemID(selectedSlotPos)
				itemCount = shop.GetItemCount(selectedSlotPos)

				type = player.SLOT_TYPE_SHOP
				if shop.IsPrivateShop():
					type = player.SLOT_TYPE_PRIVATE_SHOP

				mouseModule.mouseController.AttachObject(self, type, selectedSlotPos, selectedItemID, itemCount)
				mouseModule.mouseController.SetCallBack("INVENTORY", ui.__mem_func__(self.DropToInventory))

	def DropToInventory(self):
		attachedSlotPos = mouseModule.mouseController.GetAttachedSlotNumber()
		self.AskBuyItem(attachedSlotPos)
		
	def OnPickItem(self, count):
		itemSlotIndex = self.dlgPickItem.itemGlobalSlotIndex
		n = 0

		while n < count:
			net.SendShopBuyPacket(self.__GetRealIndex(itemSlotIndex))
			n = n + 1

	def AskBuyItem(self, slotPos):
		if app.ENABLE_OFFLINE_SHOP and shop.IsOwner():
			net.SendShopWithdrawItemPacket(self.__GetRealIndex(slotPos))
			return

		slotPos = self.__GetRealIndex(slotPos)
		
		itemIndex = shop.GetItemID(slotPos)
		itemPrice = shop.GetItemPrice(slotPos)
		itemCount = shop.GetItemCount(slotPos)

		itemPrice2 = shop.GetItemPrice2(slotPos)
		itemPrice3 = shop.GetItemPrice3(slotPos)
		itemPriceType = shop.GetItemPriceType(slotPos)
		itemPriceVnum = shop.GetItemPriceVnum(slotPos)
		itemPriceVnum2 = shop.GetItemPriceVnum2(slotPos)
		itemPriceVnum3 = shop.GetItemPriceVnum3(slotPos)

		item.SelectItem(itemIndex)
		itemName = item.GetItemName()
		
		if itemPriceType == shop.PRICE_TYPE_OBJECT:
			if itemPriceVnum > 1:
				itemBuyQuestionDialog = uiCommon.BuyItemPopupDialog()
				itemBuyQuestionDialog.SetItem(itemPriceVnum)
				itemBuyQuestionDialog.SetText(uiScriptLocale.FIRST_BUY_ITEM % (itemName, itemCount, itemPrice))
				itemBuyQuestionDialog.SetAcceptEvent(lambda arg=True: self.AnswerBuyItem(arg))
				itemBuyQuestionDialog.SetCancelEvent(lambda arg=False: self.AnswerBuyItem(arg))
				itemBuyQuestionDialog.AutoResize(45, False)
				itemBuyQuestionDialog.ScaleIcons(0.8, 0.8)
				itemBuyQuestionDialog.Open()
				itemBuyQuestionDialog.pos = slotPos
				self.itemBuyQuestionDialog = itemBuyQuestionDialog
				constInfo.SET_ITEM_QUESTION_DIALOG_STATUS(1)

			if itemPriceVnum2 > 1:
				itemBuyQuestionDialog = uiCommon.BuyItemPopupDialog()
				itemBuyQuestionDialog.SetItem(itemPriceVnum)
				itemBuyQuestionDialog.SetItem2(itemPriceVnum2)
				itemBuyQuestionDialog.SetText(uiScriptLocale.SECOND_BUY_ITEM % (itemName, itemCount, itemPrice, itemPrice2))
				itemBuyQuestionDialog.SetAcceptEvent(lambda arg=True: self.AnswerBuyItem(arg))
				itemBuyQuestionDialog.SetCancelEvent(lambda arg=False: self.AnswerBuyItem(arg))
				itemBuyQuestionDialog.AutoResize(45, True)
				itemBuyQuestionDialog.ScaleIcons(0.8, 0.8)
				itemBuyQuestionDialog.Open()
				itemBuyQuestionDialog.pos = slotPos
				self.itemBuyQuestionDialog = itemBuyQuestionDialog
				constInfo.SET_ITEM_QUESTION_DIALOG_STATUS(1)
		else:
			itemBuyQuestionDialog = uiCommon.QuestionDialog()
			itemBuyQuestionDialog.SetText(localeInfo.DO_YOU_BUY_ITEM(itemName, itemCount, localeInfo.NumberToMoneyString(itemPrice)))
			itemBuyQuestionDialog.SetAcceptEvent(lambda arg=True: self.AnswerBuyItem(arg))
			itemBuyQuestionDialog.SetCancelEvent(lambda arg=False: self.AnswerBuyItem(arg))
			itemBuyQuestionDialog.Open()
			itemBuyQuestionDialog.pos = slotPos
			self.itemBuyQuestionDialog = itemBuyQuestionDialog
		
			constInfo.SET_ITEM_QUESTION_DIALOG_STATUS(1)
		
	def AnswerBuyItem(self, flag):

		if flag:
			pos = self.itemBuyQuestionDialog.pos
			net.SendShopBuyPacket(pos)

		self.itemBuyQuestionDialog.Close()
		self.itemBuyQuestionDialog = None

		constInfo.SET_ITEM_QUESTION_DIALOG_STATUS(0)

	def SetItemToolTip(self, tooltipItem):
		self.tooltipItem = tooltipItem

	def OverInItem(self, slotIndex):
		slotIndex = self.__GetRealIndex(slotIndex)
		if mouseModule.mouseController.isAttached():
			return

		if 0 != self.tooltipItem:
			if shop.SHOP_COIN_TYPE_GOLD == shop.GetTabCoinType(self.tabIdx):
				self.tooltipItem.SetShopItem(slotIndex, self.temporaryItems)
			else:
				self.tooltipItem.SetShopItemBySecondaryCoin(slotIndex)
	
	def OverOutItem(self):
		if 0 != self.tooltipItem:
			self.tooltipItem.HideToolTip()
			
	if app.WJ_ENABLE_TRADABLE_ICON:
		def BindInterface(self, interface):
			self.interface = interface

		def OnTop(self):
			if not shop.IsPrivateShop():
				self.interface.SetOnTopWindow(player.ON_TOP_WND_SHOP)
				self.interface.RefreshMarkInventoryBag()
				
	if app.ENABLE_OFFLINE_SHOP:
		def OpenPickMoneyDialog(self):
			if self.goldAmount < 1:
				return

			self.dlgPickMoney.SetTitleName(localeInfo.PICK_MONEY_TITLE)
			self.dlgPickMoney.Open(self.goldAmount)
			
		def UpdateGold(self, gold):
			self.goldAmount = gold
			self.goldText.SetText(localeInfo.NumberToMoneyString(gold))
			
		def UpdateLock(self, lock):
			self.isLocked = lock
			
			if self.expireTime <= time.clock():
				self.lockButton.SetToolTipText(uiScriptLocale.OFFLINE_SHOP_BUTTON_RENEW)
				self.lockButton.SetUpVisual("d:/ymir work/ui/shop/btn_locked_normal.png")
				self.lockButton.SetOverVisual("d:/ymir work/ui/shop/btn_locked_over.png")
				self.lockButton.SetDownVisual("d:/ymir work/ui/shop/btn_locked_down.png")
			else:
				self.lockButton.SetToolTipText(uiScriptLocale.OFFLINE_SHOP_BUTTON_UNLOCK if self.isLocked else uiScriptLocale.OFFLINE_SHOP_BUTTON_LOCK)
				if self.isLocked:
					self.lockButton.SetUpVisual("d:/ymir work/ui/shop/btn_locked_normal.png")
					self.lockButton.SetOverVisual("d:/ymir work/ui/shop/btn_locked_over.png")
					self.lockButton.SetDownVisual("d:/ymir work/ui/shop/btn_locked_down.png")
				else:
					self.lockButton.SetUpVisual("d:/ymir work/ui/shop/btn_lock_normal.png")
					self.lockButton.SetOverVisual("d:/ymir work/ui/shop/btn_lock_over.png")
					self.lockButton.SetDownVisual("d:/ymir work/ui/shop/btn_lock_down.png")
				
		def UpdateTime(self, timeLeft):
			self.expireTime = time.clock() + timeLeft

		def UpdateTimeFunc(self):
			expired = self.expireTime <= time.clock()
			
			m, s = divmod(self.expireTime - time.clock(), 60)
			h, m = divmod(m, 60)
			d, h = divmod(h, 24)
			
			self.timeText.SetFontColor(0.5411, 0.7254, 0.5568)
			self.timeText.SetText(uiScriptLocale.OFFLINE_SHOP_TIME_LEFT % ((d, h, m) if not expired else (0, 0, 0)))

			if expired:
				self.timeText.SetFontColor(0.9, 0.4745, 0.4627)
				self.lockButton.SetToolTipText(uiScriptLocale.OFFLINE_SHOP_BUTTON_RENEW)
			
		def CloseShop(self):
			net.SendCloseShopPacket()

		def OpenSearch(self):
			self.interface.OpenSearchShop()

		def SetLock(self, arg = True):
			if self.expireTime <= time.clock() and arg:
				itemlockQuestionDialog = uiCommon.QuestionDialog()
				itemlockQuestionDialog.SetText(uiScriptLocale.OFFLINE_SHOP_RENEW_CONFIRM)
				itemlockQuestionDialog.SetAcceptEvent(lambda arg = False: self.SetLock(arg))
				itemlockQuestionDialog.SetCancelEvent(ui.__mem_func__(self.OnCloseQuestionDialog))
				itemlockQuestionDialog.Open()
				self.itemlockQuestionDialog = itemlockQuestionDialog
				
				constInfo.SET_ITEM_QUESTION_DIALOG_STATUS(1)
			else:
				net.SendShopLockPacket(not self.isLocked)
				self.OnCloseQuestionLockDialog()
				
		def OpenOfflineShop(self, sign, channel, index, x, y, time, update):
			if self.IsShow() and not update:
				self.Close()
				return
				
			self.isLocked = shop.IsLocked()
			self.lockButton.SetToolTipText(uiScriptLocale.OFFLINE_SHOP_BUTTON_UNLOCK if self.isLocked else uiScriptLocale.OFFLINE_SHOP_BUTTON_LOCK)
			
			if self.isLocked:
				self.lockButton.SetUpVisual("d:/ymir work/ui/shop/btn_locked_normal.png")
				self.lockButton.SetOverVisual("d:/ymir work/ui/shop/btn_locked_over.png")
				self.lockButton.SetDownVisual("d:/ymir work/ui/shop/btn_locked_down.png")
			else:
				self.lockButton.SetUpVisual("d:/ymir work/ui/shop/btn_lock_normal.png")
				self.lockButton.SetOverVisual("d:/ymir work/ui/shop/btn_lock_over.png")
				self.lockButton.SetDownVisual("d:/ymir work/ui/shop/btn_lock_down.png")
				
			(mapName, xBase, yBase) = background.GlobalPositionToMapInfo(x, y)
			localeMapName = localeInfo.MINIMAP_ZONE_NAME_DICT.get(mapName, "")
			self.locationText.SetText("CH %d, %s (%d, %d)" % (channel, localeMapName, int(x - xBase) / 100, int(y - yBase) / 100))

			if update and self.IsShow():
				self.Open(0, True)
			elif not update:
				self.Open(0, True)
		
			if not self.isEditing:
				self.nameLine.SetText(sign)
			
			self.UpdateTime(time)

		def OnPickMoney(self, gold):
			net.SendShopWithdrawGoldPacket(gold)
			
		def OnChangeShopName(self):
			if self.nameLine.GetText() != str(self.oldNameLine):
				self.oldNameLine = self.nameLine.GetText()
				net.SendShopChangeSignPacket(self.nameLine.GetText())
				self.nameLine.SetFontColor(0.8549, 0.8549, 0.8549)
				self.isEditing = 0
		
		def OnNameUpdate(self):
			ui.EditLine.OnIMEUpdate(self.nameLine)
			self.nameLine.SetPackedFontColor(0xfffc670c)
			self.isEditing = 1
		
		def AcceptInputPrice(self):
			if not self.priceInputBoard:
				return True

			text = self.priceInputBoard.GetText()

			if not text:
				return True

			if not text.isdigit():
				return True

			if int(text) <= 0:
				return True

			attachedInvenType = self.priceInputBoard.sourceWindowType
			sourceSlotPos = self.priceInputBoard.sourceSlotPos
			targetSlotPos = self.priceInputBoard.targetSlotPos

			price = int(self.priceInputBoard.GetText())

			self.temporaryItems[targetSlotPos] = player.GetItemTransmutation(sourceSlotPos)

			net.SendShopAddItemPacket(attachedInvenType, sourceSlotPos, targetSlotPos, price)
			
			itemprices.PRICE_DICT[self.priceInputBoard.itemVNum] = price
			
			self.priceInputBoard = None
			
			return True

		def CancelInputPrice(self):
			self.priceInputBoard = None
			return True
			
		def OnCloseQuestionLockDialog(self):
			if not self.itemlockQuestionDialog:
				return

			self.itemlockQuestionDialog.Close()
			self.itemlockQuestionDialog = None
			constInfo.SET_ITEM_QUESTION_DIALOG_STATUS(0)
			
	def OnUpdate(self):
		self.UpdateTimeFunc()

class MallPageDialog(ui.ScriptWindow):
	def __init__(self):
		ui.ScriptWindow.__init__(self)

	def __del__(self):
		ui.ScriptWindow.__del__(self)

	def Destroy(self):
		self.ClearDictionary()

	def Open(self):
		scriptLoader = ui.PythonScriptLoader()
		scriptLoader.LoadScriptFile(self, "uiscript/mallpagedialog.py")

		self.GetChild("titlebar").SetCloseEvent(ui.__mem_func__(self.Close))

		(x, y)=self.GetGlobalPosition()
		x+=10
		y+=30

		MALL_PAGE_WIDTH = 600
		MALL_PAGE_HEIGHT = 480

		self.Lock()
		self.Show()

	def Close(self):
		self.Unlock()
		self.Hide()

	def OnPressEscapeKey(self):
		self.Close()
		return True
