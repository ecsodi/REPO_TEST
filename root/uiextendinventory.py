import thenewui as ui
import CacheEffect as player
import mouseModule
import net
import app
import item
import chat
import uiPickMoney
import uiCommon
import uiPrivateShopBuilder
import localeInfo
import constInfo
import ime
import cfg
import grp
import wndMgr
import uiScriptLocale
import background
import shop
import safebox
import uiToolTip
import exchange

ITEM_FLAG_APPLICABLE = 1 << 14

class CustomInventoryWindow(ui.ScriptWindow):
	USE_TYPE_TUPLE = (
		"USE_CLEAN_SOCKET", 
		"USE_CHANGE_ATTRIBUTE", 
		"USE_ADD_ATTRIBUTE", 
		"USE_ADD_ATTRIBUTE2", 
		"USE_ADD_ACCESSORY_SOCKET", 
		"USE_PUT_INTO_ACCESSORY_SOCKET", 
		"USE_PUT_INTO_BELT_SOCKET", 
		"USE_PUT_INTO_RING_SOCKET",
		"USE_COSTUME_CHANGE_ATTRIBUTE", 
		"USE_COSTUME_ADD_ATTRIBUTE", 
		"USE_ADD_ATTRIBUTE_COSTUME", 
		"USE_CHANGE_ATTRIBUTE_COSTUME", 
		"USE_BIND", 
		"USE_UNBIND"
	)
	
	questionDialog = None
	tooltipItem = None
	dlgPickItem = None
	wndInterface = None
	SafeBoxSize = 1

	sellingSlotNumber = -1
	isLoaded = 0
	btnCategoryes = []
	liHighlightedItems = []

	def __init__(self):
		ui.ScriptWindow.__init__(self)
		self.interface = None
		self.__LoadWindow()

	def __del__(self):
		ui.ScriptWindow.__del__(self)
		self.interface = None

	def Show(self):
		self.__LoadWindow()

		self.SelectCategory(0)
		self.SetInventoryPage(0)
		self.RefreshItemSlot()
		
		ui.ScriptWindow.Show(self)

	def BindInterfaceClass(self, interface):
		self.wndInterface = interface

	def RefreshMarkSlots(self, localIndex=None):
		if not self.wndInterface:
			return
		
		onTopWnd = self.wndInterface.GetOnTopWindow()
		if localIndex:
			slotNumber = self.__InventoryLocalSlotPosToGlobalSlotPos(localIndex)
			if onTopWnd == player.ON_TOP_WND_NONE:
				self.wndItem.SetUsableSlotOnTopWnd(localIndex)

			elif onTopWnd == player.ON_TOP_WND_SHOP:
				if player.IsAntiFlagBySlot(slotNumber, item.ANTIFLAG_SELL):
					self.wndItem.SetUnusableSlotOnTopWnd(localIndex)
				else:
					self.wndItem.SetUsableSlotOnTopWnd(localIndex)

			elif onTopWnd == player.ON_TOP_WND_EXCHANGE:
				if player.IsAntiFlagBySlot(slotNumber, item.ANTIFLAG_GIVE):
					self.wndItem.SetUnusableSlotOnTopWnd(localIndex)
				else:
					self.wndItem.SetUsableSlotOnTopWnd(localIndex)

			elif onTopWnd == player.ON_TOP_WND_PRIVATE_SHOP:
				if player.IsAntiFlagBySlot(slotNumber, item.ITEM_ANTIFLAG_MYSHOP):
					self.wndItem.SetUnusableSlotOnTopWnd(localIndex)
				else:
					self.wndItem.SetUsableSlotOnTopWnd(localIndex)

			elif onTopWnd == player.ON_TOP_WND_SAFEBOX:
				if player.IsAntiFlagBySlot(slotNumber, item.ANTIFLAG_SAFEBOX):
					self.wndItem.SetUnusableSlotOnTopWnd(localIndex)
				else:
					self.wndItem.SetUsableSlotOnTopWnd(localIndex)

			return

		for i in xrange(45):
			slotNumber = self.__InventoryLocalSlotPosToGlobalSlotPos(i)

			if onTopWnd == player.ON_TOP_WND_NONE:
				self.wndItem.SetUsableSlotOnTopWnd(i)

			elif onTopWnd == player.ON_TOP_WND_SHOP:
				if player.IsAntiFlagBySlot(slotNumber, item.ANTIFLAG_SELL):
					self.wndItem.SetUnusableSlotOnTopWnd(i)
				else:
					self.wndItem.SetUsableSlotOnTopWnd(i)

			elif onTopWnd == player.ON_TOP_WND_EXCHANGE:
				if player.IsAntiFlagBySlot(slotNumber, item.ANTIFLAG_GIVE):
					self.wndItem.SetUnusableSlotOnTopWnd(i)
				else:
					self.wndItem.SetUsableSlotOnTopWnd(i)

			elif onTopWnd == player.ON_TOP_WND_PRIVATE_SHOP:
				if player.IsAntiFlagBySlot(slotNumber, item.ITEM_ANTIFLAG_MYSHOP):
					self.wndItem.SetUnusableSlotOnTopWnd(i)
				else:
					self.wndItem.SetUsableSlotOnTopWnd(i)

			elif onTopWnd == player.ON_TOP_WND_SAFEBOX:
				if player.IsAntiFlagBySlot(slotNumber, item.ANTIFLAG_SAFEBOX):
					self.wndItem.SetUnusableSlotOnTopWnd(i)
				else:
					self.wndItem.SetUsableSlotOnTopWnd(i)

	def __LoadWindow(self):
		if self.isLoaded == 1:
			return

		self.isLoaded = 1

		try:
			pyScrLoader = ui.PythonScriptLoader()
			pyScrLoader.LoadScriptFile(self, "uiscript/CustomInventoryWindow_norm.py")
		except:
			import exception
			exception.Abort("custominventorywindow.LoadWindow.LoadObject")

		try:
			self.GetChild("TitleBar").SetCloseEvent(ui.__mem_func__(self.CloseFromTitleBar))
			
			wndItem = self.GetChild("ItemSlot")

			self.inventoryTab = []
			self.inventoryTab.append(self.GetChild("Inventory_Page_01"))
			self.inventoryTab.append(self.GetChild("Inventory_Page_02"))
			self.inventoryTab.append(self.GetChild("Inventory_Page_03"))
			self.inventoryTab.append(self.GetChild("Inventory_Page_04"))
			self.inventoryTab.append(self.GetChild("Inventory_Page_05"))
			
			self.categoryTab = []
			self.categoryTab.append(self.GetChild("SkillBookButton"))
			self.categoryTab.append(self.GetChild("StoneButton"))
			self.categoryTab.append(self.GetChild("UpgradeItemsButton"))
			self.categoryTab.append(self.GetChild("BoxButton"))
			
			self.sortButton = self.GetChild("SortInventoryBtn")
			self.wndAnim = self.GetChild("AnimWareHouse")
		except:
			import exception
			exception.Abort("custominventorywindow.LoadWindow.BindObject")

		## Item
		wndItem.SetSelectEmptySlotEvent(ui.__mem_func__(self.SelectEmptySlot))
		wndItem.SetSelectItemSlotEvent(ui.__mem_func__(self.SelectItemSlot))
		wndItem.SetUnselectItemSlotEvent(ui.__mem_func__(self.UseItemSlot))
		wndItem.SetUseSlotEvent(ui.__mem_func__(self.UseItemSlot))
		wndItem.SetOverInItemEvent(ui.__mem_func__(self.OverInItem))
		wndItem.SetOverOutItemEvent(ui.__mem_func__(self.OverOutItem))
		
		self.sortButton.SetEvent(ui.__mem_func__(self.ClickSortButton))

		# self.wndAnim.SetEndFrameEvent(ui.__mem_func__(self.OnFinishAnim))
		# self.wndAnim.Hide()
		# self.wndAnim.SetDelay(1)

		# for i in xrange(39):
			# self.wndAnim.AppendImageScale("d:/ymir work/ui/anim_new/frame_delay_%d.png" % int(i), 0.4, 0.4)

		## PickMoneyDialog
		dlgPickItem = uiPickMoney.PickMoneyDialog()
		dlgPickItem.LoadDialog()
		dlgPickItem.Hide()

		self.inventoryTab[0].SetEvent(lambda arg = 0 : self.SetInventoryPage(arg))
		self.inventoryTab[1].SetEvent(lambda arg = 1 : self.SetInventoryPage(arg))
		self.inventoryTab[2].SetEvent(lambda arg = 2 : self.SetInventoryPage(arg))
		self.inventoryTab[3].SetEvent(lambda arg = 3 : self.SetInventoryPage(arg))
		self.inventoryTab[4].SetEvent(lambda arg = 4 : self.SetInventoryPage(arg))
		self.inventoryTab[0].Down()
		
		self.categoryTab[0].SetEvent(lambda arg = 0 : self.SelectCategory(arg))
		self.categoryTab[1].SetEvent(lambda arg = 1 : self.SelectCategory(arg))
		self.categoryTab[2].SetEvent(lambda arg = 2 : self.SelectCategory(arg))
		self.categoryTab[3].SetEvent(lambda arg = 3 : self.SelectCategory(arg))
		self.inventoryTab[0].Down()
		
		self.inventoryPageIndex = [0] * 5

		self.wndItem = wndItem
		self.dlgPickItem = dlgPickItem

		self.categoryIndex = 0
		self.SelectCategory(0)

		## Refresh
		self.SetInventoryPage(0)
		self.RefreshItemSlot()
		
	def ClickSortButton(self):
		net.SendChatPacket("/sort_custom_inventory %d" % int(self.categoryIndex))

	def Destroy(self):
		self.ClearDictionary()

		self.dlgPickItem.Destroy()
		self.dlgPickItem = 0

		self.tooltipItem = None
		self.wndItem = 0
		self.questionDialog = None
		self.wndInterface = None
		self.sortButton = None
		
		if self.inventoryTab:
			del self.inventoryTab[:]
		
		if self.btnCategoryes:
			del self.btnCategoryes[:]
		
	def Hide(self):
		if constInfo.GET_ITEM_QUESTION_DIALOG_STATUS():
			self.OnCloseQuestionDialog()
			return
			
		if self.tooltipItem:
			self.tooltipItem.HideToolTip()
			
		if self.dlgPickItem:
			self.dlgPickItem.Close()

		wndMgr.Hide(self.hWnd)

	def Close(self):
		self.Hide()
		
	def CloseFromTitleBar(self):
		self.Hide()
			
	def SelectCategory(self, catIndex):
		# if self.wndAnim.IsShow() or catIndex == self.categoryIndex:
			# self.categoryTab[self.categoryIndex].Down()
			# return
	
		if self.categoryTab[catIndex].IsShow() == FALSE: # @ Fix Mouse Wheel
			return
			
		# self.wndAnim.SetPosition(75, 160)
		# self.wndAnim.ResetFrame()
		# self.wndItem.Hide()
		# self.wndAnim.Show()
		
		for x in xrange(0, len(self.inventoryTab)):
			self.inventoryTab[x].Show()

		for x in xrange(3, len(self.inventoryTab)):
			if catIndex == 0:
				self.inventoryTab[x].Hide()
			else:
				self.inventoryTab[x].Show()
		
		self.categoryTab[self.categoryIndex].SetUp()
		self.categoryIndex = catIndex
		self.categoryTab[self.categoryIndex].Down()

		self.RefreshInventoryPage()
		self.ResetItemSize()
		
		self.RefreshItemSlot()
	
	# def OnFinishAnim(self):
		# self.wndItem.Show()
		# self.wndAnim.Hide()

	def RefreshInventoryPage(self):
		for page in self.inventoryTab:
			page.SetUp()
			
		self.SetInventoryPage(self.inventoryPageIndex[self.categoryIndex])

	def SetInventoryPage(self, page):
		if self.wndAnim.IsShow():
			return
	
		if self.inventoryTab[page].IsShow() == FALSE: # @ Fix Mouse Wheel
			return
	
		self.inventoryTab[self.inventoryPageIndex[self.categoryIndex]].SetUp()
		self.inventoryPageIndex[self.categoryIndex] = page
		self.inventoryTab[self.inventoryPageIndex[self.categoryIndex]].Down()
		self.RefreshItemSlot()
		
	def OnRunMouseWheel(self, nLen):
		x, y = self.GetMouseLocalPosition()
		if y <= 325:	
			if nLen > 0:
				if self.inventoryPageIndex[self.categoryIndex] > 0:
					self.SetInventoryPage(self.inventoryPageIndex[self.categoryIndex] - 1)
			else:
				if self.inventoryPageIndex[self.categoryIndex] < 4:
					self.SetInventoryPage(self.inventoryPageIndex[self.categoryIndex] + 1)
		else:
			# if self.wndAnim.IsShow():
				# return

			if nLen > 0:
				if self.categoryIndex > 0:
					self.SelectCategory(self.categoryIndex - 1)
			else:
				if self.categoryIndex < 3:
					self.SelectCategory(self.categoryIndex + 1)


	def OnPickItem(self, count):
		itemSlotIndex = self.dlgPickItem.itemGlobalSlotIndex

		mouseModule.mouseController.AttachObject(self, player.SLOT_TYPE_INVENTORY, itemSlotIndex, player.GetItemIndex(itemSlotIndex), count)

	def __InventoryLocalSlotPosToGlobalSlotPos(self, local):
		# BOOK_RESTRICTION
		if self.categoryIndex == 0:
			return player.INVENTORY_BOOK_START + (self.categoryIndex * 135) + (self.inventoryPageIndex[self.categoryIndex] * 45 + local)
		elif self.categoryIndex == 1:
			return player.INVENTORY_STONE_START + (self.inventoryPageIndex[self.categoryIndex] * 45 + local)
		elif self.categoryIndex == 2:
			return player.INVENTORY_UPGRADE_START + (self.inventoryPageIndex[self.categoryIndex] * 45 + local)
		elif self.categoryIndex == 3:
			return player.INVENTORY_CHEST_START + (self.inventoryPageIndex[self.categoryIndex] * 45 + local)

		return player.INVENTORY_BOOK_START + (self.categoryIndex * 135) + (self.inventoryPageIndex[self.categoryIndex] * 45 + local) # book default, return somethin'

	def GetInventoryPageIndex(self):
		return self.inventoryPageIndex[self.categoryIndex]

	def RefreshItemSlot(self):
		dictPoints = [player.POINT_BOOK_INV_NUM, player.POINT_STONE_INV_NUM, player.POINT_UPGRADE_INV_NUM, player.POINT_CHEST_INV_NUM, 0]
		SlotNum = player.GetStatus(dictPoints[self.categoryIndex])
		
		imgLocked = "d:/ymir work/ui/game/normal_interface/offlineshop_locked_normal.png"
		imgLockedOver = "d:/ymir work/ui/game/normal_interface/offlineshop_locked_hover.png"
			
		for i in xrange(45):
			slotNumber = self.__InventoryLocalSlotPosToGlobalSlotPos(i)
			
			self.wndItem.DeleteCoverButton(i)

			if self.inventoryPageIndex[self.categoryIndex] * 45 + i > SlotNum:
				self.wndItem.SetItemSlot(i, 0, 0)
				self.wndItem.EnableCoverButton(i)
				self.wndItem.SetAlwaysRenderCoverButton(i)
				self.wndItem.SetCoverButton(i, imgLocked, imgLockedOver, imgLockedOver)
				continue
			
			itemCount = player.GetItemCount(slotNumber)
			if 0 == itemCount:
				self.wndItem.ClearSlot(i)
				continue
			elif 1 == itemCount:
				itemCount = 0

			itemVnum = player.GetItemIndex(slotNumber)
			self.wndItem.SetItemSlot(i, itemVnum, itemCount)

			if constInfo.IS_AUTO_POTION(itemVnum) == False and constInfo.IS_BLEND_ITEM(itemVnum) == False and constInfo.COMPANION_ACTIVE_POS != slotNumber:
				if not slotNumber in self.liHighlightedItems:
					self.wndItem.DeactivateSlotInventory(i)

			if app.WJ_ENABLE_TRADABLE_ICON:
				self.RefreshMarkSlots(i)

		self.wndItem.RefreshSlot()
		self.__RefreshHighlights()

	def HighlightSlot(self, slot):
		if not slot in self.liHighlightedItems:
			self.liHighlightedItems.append(slot)

	def __RefreshHighlights(self):
		for i in xrange(player.INVENTORY_PAGE_SIZE):
			slotNumber = self.__InventoryLocalSlotPosToGlobalSlotPos(i)
			if slotNumber in self.liHighlightedItems:
				self.wndItem.ActivateSlotInventory(i)

	def SetItemToolTip(self, tooltipItem):
		self.tooltipItem = tooltipItem
		
	def __SellItem(self, itemSlotPos):
		if not player.IsEquipmentSlot(itemSlotPos):
			itemIndex = player.GetItemIndex(itemSlotPos)
			itemCount = player.GetItemCount(itemSlotPos)
			
			self.sellingSlotNumber = itemSlotPos
			self.sellingSlotitemIndex = itemIndex
			self.sellingSlotitemCount = itemCount

			item.SelectItem(itemIndex)
			itemPrice = item.GetISellItemPrice()
			itemName = item.GetItemName()

			self.questionDialog = uiCommon.QuestionDialog()
			self.questionDialog.SetText(localeInfo.DO_YOU_SELL_ITEM(itemName, itemCount, itemPrice))
			self.questionDialog.SetAcceptEvent(ui.__mem_func__(self.SellItem))
			self.questionDialog.SetCancelEvent(ui.__mem_func__(self.OnCloseQuestionDialog))
			self.questionDialog.Open()
			self.questionDialog.count = itemCount
		
			constInfo.SET_ITEM_QUESTION_DIALOG_STATUS(1)

	def SellItem(self):
		if self.sellingSlotitemIndex == player.GetItemIndex(self.sellingSlotNumber):
			if self.sellingSlotitemCount == player.GetItemCount(self.sellingSlotNumber):
				net.SendShopSellPacketNew(self.sellingSlotNumber, self.questionDialog.count, player.INVENTORY)
				
		self.OnCloseQuestionDialog()

	def OnCloseQuestionDialog(self):
		if not self.questionDialog:
			return

		self.questionDialog.Close()
		self.questionDialog = None
		constInfo.SET_ITEM_QUESTION_DIALOG_STATUS(0)

	## Slot Event
	def SelectEmptySlot(self, selectedSlotPos):
		if constInfo.GET_ITEM_QUESTION_DIALOG_STATUS() == 1:
			return
	
		selectedSlotPos = self.__InventoryLocalSlotPosToGlobalSlotPos(selectedSlotPos)

		if mouseModule.mouseController.isAttached():

			attachedSlotType = mouseModule.mouseController.GetAttachedType()
			attachedSlotPos = mouseModule.mouseController.GetAttachedSlotNumber()
			attachedItemCount = mouseModule.mouseController.GetAttachedItemCount()
			attachedItemIndex = mouseModule.mouseController.GetAttachedItemIndex()

			if player.SLOT_TYPE_INVENTORY == attachedSlotType:
				itemCount = player.GetItemCount(attachedSlotPos)
				attachedCount = mouseModule.mouseController.GetAttachedItemCount()
				self.__SendMoveItemPacket(attachedSlotPos, selectedSlotPos, attachedCount)

				if item.IsRefineScroll(attachedItemIndex):
					self.wndItem.SetUseMode(False)

			elif player.SLOT_TYPE_PRIVATE_SHOP == attachedSlotType:
				mouseModule.mouseController.RunCallBack("INVENTORY")

			elif player.SLOT_TYPE_SHOP == attachedSlotType:
				net.SendShopBuyPacket(attachedSlotPos)

			elif player.SLOT_TYPE_SAFEBOX == attachedSlotType:
				net.SendSafeboxCheckoutPacket(attachedSlotPos, selectedSlotPos)

			elif player.SLOT_TYPE_MALL == attachedSlotType:
				net.SendMallCheckoutPacket(attachedSlotPos, selectedSlotPos)
				
			elif player.SLOT_TYPE_MYSHOP == attachedSlotType:
				mouseModule.mouseController.RunCallBack("INVENTORY", player.SLOT_TYPE_INVENTORY, selectedSlotPos)

			mouseModule.mouseController.DeattachObject()

	def SelectItemSlot(self, itemSlotIndex):
		if constInfo.GET_ITEM_QUESTION_DIALOG_STATUS() == 1:
			return

		itemSlotIndex = self.__InventoryLocalSlotPosToGlobalSlotPos(itemSlotIndex)

		if mouseModule.mouseController.isAttached():
			attachedSlotType = mouseModule.mouseController.GetAttachedType()
			attachedSlotPos = mouseModule.mouseController.GetAttachedSlotNumber()
			attachedItemVID = mouseModule.mouseController.GetAttachedItemIndex()

			if player.SLOT_TYPE_INVENTORY == attachedSlotType:
				self.__DropSrcItemToDestItemInInventory(attachedItemVID, attachedSlotPos, itemSlotIndex)

			mouseModule.mouseController.DeattachObject()

		else:
			curCursorNum = app.GetCursor()
			if app.SELL == curCursorNum:
				self.__SellItem(itemSlotIndex)

			elif app.BUY == curCursorNum:
				chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.SHOP_BUY_INFO)

			elif app.IsPressed(app.DIK_LALT):
				link = player.GetItemLink(itemSlotIndex)
				ime.PasteString(link)

			elif app.IsPressed(app.DIK_LSHIFT):
				itemCount = player.GetItemCount(itemSlotIndex)
				
				if itemCount > 1:
					self.dlgPickItem.SetTitleName(localeInfo.PICK_ITEM_TITLE)
					self.dlgPickItem.SetAcceptEvent(ui.__mem_func__(self.OnPickItem))
					self.dlgPickItem.Open(itemCount)
					self.dlgPickItem.itemGlobalSlotIndex = itemSlotIndex
					
			elif app.IsPressed(app.DIK_LCONTROL):
				itemIndex = player.GetItemIndex(itemSlotIndex)
				
				if True == item.CanAddToQuickSlotItem(itemIndex):
					player.RequestAddToEmptyLocalQuickSlot(player.SLOT_TYPE_INVENTORY, itemSlotIndex)
				else:
					chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.QUICKSLOT_REGISTER_DISABLE_ITEM)
			else:
				selectedItemVNum = player.GetItemIndex(itemSlotIndex)
				itemCount = player.GetItemCount(itemSlotIndex)
				
				mouseModule.mouseController.AttachObject(self, player.SLOT_TYPE_INVENTORY, itemSlotIndex, selectedItemVNum, itemCount)

				if self.__IsUsableItemToItem(selectedItemVNum, itemSlotIndex):
					self.wndItem.SetUseMode(True)
				else:
					self.wndItem.SetUseMode(False)
				
	def __DropSrcItemToDestItemInInventory(self, srcItemVID, srcItemSlotPos, dstItemSlotPos):
		if srcItemSlotPos == dstItemSlotPos:
			return
		vnumDest = player.GetItemIndex(dstItemSlotPos)

		if srcItemVID == player.GetItemIndex(dstItemSlotPos):
			self.__SendMoveItemPacket(srcItemSlotPos, dstItemSlotPos, 0)

		elif item.IsRefineScroll(srcItemVID):
			self.RefineItem(srcItemSlotPos, dstItemSlotPos)
			self.wndItem.SetUseMode(False)
			
		elif item.IsRefineScroll(srcItemVID) and srcItemVID == vnumDest: # Grimm BugFix stack items same VNUM
			self.__SendMoveItemPacket(srcItemSlotPos, dstItemSlotPos, 0)
			return
			
		elif item.IsKey(srcItemVID):
			self.__SendUseItemToItemPacket(srcItemSlotPos, dstItemSlotPos)

		elif (player.GetItemFlags(srcItemSlotPos) & ITEM_FLAG_APPLICABLE) == ITEM_FLAG_APPLICABLE:
			self.__SendUseItemToItemPacket(srcItemSlotPos, dstItemSlotPos)
			
		elif item.GetUseType(srcItemVID) in self.USE_TYPE_TUPLE:
			self.__SendUseItemToItemPacket(srcItemSlotPos, dstItemSlotPos)
		elif item.GetItemSubType() == item.USE_ADD_ATTRIBUTE_COSTUME or item.GetItemSubType() == item.USE_CHANGE_ATTRIBUTE_COSTUME:
			self.__SendUseItemToItemPacket(srcItemSlotPos, dstItemSlotPos)
		else:
			if player.IsEquipmentSlot(dstItemSlotPos):
				if item.IsEquipmentVID(srcItemVID):
					self.__UseItem(srcItemSlotPos)
			else:
				self.__SendMoveItemPacket(srcItemSlotPos, dstItemSlotPos, 0)

	def RefineItem(self, scrollSlotPos, targetSlotPos):
		scrollIndex = player.GetItemIndex(scrollSlotPos)
		targetIndex = player.GetItemIndex(targetSlotPos)

		if player.REFINE_OK != player.CanRefine(scrollIndex, targetSlotPos):
			return

		# if app.ENABLE_REFINE_RENEWAL:
		constInfo.AUTO_REFINE_TYPE = 1
		constInfo.AUTO_REFINE_DATA["ITEM"][0] = scrollSlotPos
		constInfo.AUTO_REFINE_DATA["ITEM"][1] = targetSlotPos
	
		self.__SendUseItemToItemPacket(scrollSlotPos, targetSlotPos)

	def OverOutItem(self):
		self.wndItem.SetUsableItem(False)
		if self.tooltipItem:
			self.tooltipItem.HideToolTip()

	def OverInItem(self, overSlotPos):
		Index = overSlotPos
		overSlotPos = self.__InventoryLocalSlotPosToGlobalSlotPos(overSlotPos)
		self.wndItem.SetUsableItem(False)

		if overSlotPos in self.liHighlightedItems:
			self.liHighlightedItems.remove(overSlotPos)
			self.wndItem.DeactivateSlotInventory(Index)

		if mouseModule.mouseController.isAttached() and self.categoryIndex != 4:
			attachedItemType = mouseModule.mouseController.GetAttachedType()
			if player.SLOT_TYPE_INVENTORY == attachedItemType:
				attachedSlotPos = mouseModule.mouseController.GetAttachedSlotNumber()
				attachedItemVnum = mouseModule.mouseController.GetAttachedItemIndex()

				if self.__CanUseSrcItemToDstItem(attachedItemVnum, attachedSlotPos, overSlotPos):
					self.wndItem.SetUsableItem(True)
					self.ShowToolTip(overSlotPos, False, Index)
					return
		
		IsWareHouse = False
		if self.categoryIndex == 4: # WAREHOUSE
			self.wndItem.SetUsableItem(False)
			IsWareHouse = True

		self.ShowToolTip(overSlotPos, IsWareHouse, Index)

	def __IsUsableItemToItem(self, srcItemVNum, srcSlotPos):
		if item.IsRefineScroll(srcItemVNum):
			return True
		elif item.IsKey(srcItemVNum):
			return True
		elif (player.GetItemFlags(srcSlotPos) & ITEM_FLAG_APPLICABLE) == ITEM_FLAG_APPLICABLE:
			return True
		else:
			if item.GetUseType(srcItemVNum) in self.USE_TYPE_TUPLE:
				return True

		return False

	def __CanUseSrcItemToDstItem(self, srcItemVnum, srcSlotPos, dstSlotPos):
		if srcSlotPos == dstSlotPos:
			return False

		if item.IsRefineScroll(srcItemVnum):
			if player.REFINE_OK == player.CanRefine(srcItemVnum, dstSlotPos):
				return True
				
		elif item.IsKey(srcItemVnum):
			if player.CanUnlock(srcItemVnum, dstSlotPos):
				return True

		elif (player.GetItemFlags(srcSlotPos) & ITEM_FLAG_APPLICABLE) == ITEM_FLAG_APPLICABLE:
			return True
			
		else:
			useType=item.GetUseType(srcItemVnum)

			if "USE_CHANGE_ATTRIBUTE" == useType:
				if self.__CanChangeItemAttrList(dstSlotPos):
					return True
			elif "USE_ADD_ATTRIBUTE" == useType:
				if self.__CanAddItemAttr(dstSlotPos):
					return True
			elif "USE_ADD_ATTRIBUTE2" == useType:
				if self.__CanAddItemAttr(dstSlotPos):
					return True

		return False

	def __CanChangeItemAttrList(self, dstSlotPos):
		dstItemVNum = player.GetItemIndex(dstSlotPos)
		if dstItemVNum == 0:
			return False

		item.SelectItem(dstItemVNum)

		if not item.GetItemType() in (item.ITEM_TYPE_WEAPON, item.ITEM_TYPE_ARMOR):
			return False

		for i in xrange(player.METIN_SOCKET_MAX_NUM):
			if player.GetItemAttribute(dstSlotPos, i) != 0:
				return True

		return False

	def __CanAddItemAttr(self, dstSlotPos):
		dstItemVNum = player.GetItemIndex(dstSlotPos)
		if dstItemVNum == 0:
			return False

		item.SelectItem(dstItemVNum)

		if not item.GetItemType() in (item.ITEM_TYPE_WEAPON, item.ITEM_TYPE_ARMOR):
			return False

		attrCount = 0
		for i in xrange(player.METIN_SOCKET_MAX_NUM):
			if player.GetItemAttribute(dstSlotPos, i) != 0:
				attrCount += 1

		if attrCount<4:
			return True

		return False

	def ShowToolTip(self, slotIndex, IsWareHouse = False, Index = -1):
		if self.tooltipItem:
			self.tooltipItem.SetInventoryItem(slotIndex, player.INVENTORY, self.wndInterface, True)
			
			itemVnum = player.GetItemIndex(player.INVENTORY, slotIndex)
			if app.IsPressed(app.DIK_LALT) and itemVnum > 0:
				item.SelectItem(itemVnum)
				if self.wndInterface.dlgChestDrop and item.GetItemType() == 23 or itemVnum in [ 50011, 50012 ]:
					if not self.wndInterface.dlgChestDrop.IsShow():
						self.wndInterface.dlgChestDrop.Open(slotIndex)
						net.SendChestDropInfo(slotIndex)
						
	def OnTop(self):
		if self.tooltipItem:
			self.tooltipItem.SetTop()
			
		self.RefreshMarkSlots()
			
	def OnPressEscapeKey(self):
		self.CloseFromTitleBar()
		return True

	if constInfo.FAST_INTERACTION_TRADE == True:
		def GetExchangeEmptyGridSlot(self, size):        
			SIZE_X = constInfo.FAST_INTERACTION_TRADE_X
			RET_SLOT = -1        
					
			mtrx = {i : False for i in xrange(exchange.EXCHANGE_ITEM_MAX_NUM)}        
			for i in xrange(exchange.EXCHANGE_ITEM_MAX_NUM):        
				if exchange.GetItemCountFromSelf(i)  != 0 and mtrx[i] == False:                        
					item.SelectItem(exchange.GetItemVnumFromSelf(i))        
					(trash, size_y) = item.GetItemSize()                            
					for x in xrange(size_y):        
						mtrx[i+(SIZE_X*x)] = True                                
					
			for i in xrange(exchange.EXCHANGE_ITEM_MAX_NUM):        
				RET_SLOT = i        
				for a in xrange(size):        
					if i+(SIZE_X*a) >= exchange.EXCHANGE_ITEM_MAX_NUM:        
						RET_SLOT = -1        
						break        
					if mtrx[i+(SIZE_X*a)] != False:        
						RET_SLOT = -1        
						break        
				if RET_SLOT != -1:        
					break        
			return RET_SLOT

	def UseItemSlot(self, slotIndex):
		if constInfo.FAST_INTERACTION_TRADE == True:
			if exchange.isTrading() and app.IsPressed(app.DIK_LCONTROL):		
				if mouseModule.mouseController.isAttached():        
					mouseModule.mouseController.DeattachObject()        
							
				SrcSlotNumber = self.__InventoryLocalSlotPosToGlobalSlotPos(slotIndex)        
				ItemVNum = player.GetItemIndex(SrcSlotNumber)        
				item.SelectItem(ItemVNum)        
				(w, h) = item.GetItemSize()        
							
				DstSlotNumber = self.GetExchangeEmptyGridSlot(h)        
				if DstSlotNumber == -1:        
					return        
							
				if item.IsAntiFlag(item.ANTIFLAG_GIVE):        
					chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.EXCHANGE_CANNOT_GIVE)        
					return                
							
				net.SendExchangeItemAddPacket(player.INVENTORY, SrcSlotNumber, DstSlotNumber)        
				return
				
		curCursorNum = app.GetCursor()
		if app.SELL == curCursorNum:
			return

		if constInfo.GET_ITEM_QUESTION_DIALOG_STATUS():
			return
			
		SlotPos = slotIndex
		slotIndex = self.__InventoryLocalSlotPosToGlobalSlotPos(slotIndex)


		if app.IsPressed(app.DIK_LSHIFT):
			if shop.IsOpen():
				if not shop.IsPrivateShop():
					net.SendShopSellPacketNew(slotIndex, player.GetItemCount(slotIndex), player.INVENTORY)
		
		if app.IsPressed(app.DIK_LCONTROL):
			self.MoveToInventory(slotIndex, SlotPos)
		else:
			self.__UseItem(slotIndex)

		mouseModule.mouseController.DeattachObject()
		
		self.OverOutItem()

	def MoveToInventory(self, slotIndex, SlotPos):
		ExceptArray = []

		if app.IsPressed(app.DIK_LCONTROL):
			ItemVnum = player.GetItemIndex(slotIndex)
			item.SelectItem(ItemVnum)
			_, ItemSizeMovable = item.GetItemSize()				

			for x in xrange(180):
				if player.GetItemIndex(x) > 0:
					item.SelectItem(player.GetItemIndex(x))
					_, ItemSize = item.GetItemSize()
					
					for size in xrange(ItemSize):
						xPos = x + (size * 5)
						ExceptArray.append(xPos)

				if player.GetItemIndex(x) == 0:		
					bCanPass = True
					for size in xrange(ItemSizeMovable):
						if player.GetItemIndex(x + (size * 5)) != 0:
							bCanPass = False

					if x in ExceptArray or not bCanPass:
						continue
					
					self.__SendMoveItemPacket(slotIndex, x, player.GetItemCount(slotIndex))	
					break		

	def __UseItem(self, slotIndex):
		ItemVnum = player.GetItemIndex(slotIndex)
		item.SelectItem(ItemVnum)
		
		if constInfo.FAST_INTERACTION_DELETE == True:
			if app.IsPressed(app.DIK_DELETE):
				if player.IsEquipmentSlot(slotIndex):
					chat.AppendChat(chat.CHAT_TYPE_INFO, "[!] Nu poti sterge obiectele echipate!")
					return

				net.SendItemDestroyPacket(slotIndex)
				return
				
		if app.ENABLE_SELL_ITEM:
			if app.IsPressed(app.DIK_LALT) and app.IsPressed(app.DIK_LSHIFT) and constInfo.IsSellItems(ItemVnum):
				self.__SendSellItemPacket(slotIndex)
				return
				
		if item.IsFlag(item.ITEM_FLAG_CONFIRM_WHEN_USE):
			self.questionDialog = uiCommon.QuestionDialog()
			self.questionDialog.SetText(localeInfo.INVENTORY_REALLY_USE_ITEM)
			self.questionDialog.SetAcceptEvent(ui.__mem_func__(self.__UseItemQuestionDialog_OnAccept))
			self.questionDialog.SetCancelEvent(ui.__mem_func__(self.__UseItemQuestionDialog_OnCancel))
			self.questionDialog.slotIndex = slotIndex
			self.questionDialog.Open()
			constInfo.SET_ITEM_QUESTION_DIALOG_STATUS(1)

		self.__SendUseItemPacket(slotIndex)
	
	def IsDlgQuestionShow(self):
		if self.dlgQuestion.IsShow():
			return True
		else:
			return False
	
	def __UseItemQuestionDialog_OnCancel(self):
		self.OnCloseQuestionDialog()

	def __UseItemQuestionDialog_OnAccept(self):
		self.__SendUseItemPacket(self.questionDialog.slotIndex)
		self.OnCloseQuestionDialog()

	def __SendUseItemToItemPacket(self, srcSlotPos, dstSlotPos):
		if uiPrivateShopBuilder.IsBuildingPrivateShop():
			chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.USE_ITEM_FAILURE_PRIVATE_SHOP)
			return

		net.SendItemUseToItemPacket(srcSlotPos, dstSlotPos)

	def __SendUseItemPacket(self, slotPos):
		if uiPrivateShopBuilder.IsBuildingPrivateShop():
			chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.USE_ITEM_FAILURE_PRIVATE_SHOP)
			return

		net.SendItemUsePacket(slotPos)

	def __SendMoveItemPacket(self, srcSlotPos, dstSlotPos, srcItemCount):
		if uiPrivateShopBuilder.IsBuildingPrivateShop():
			chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.MOVE_ITEM_FAILURE_PRIVATE_SHOP)
			return

		net.SendItemMovePacket(srcSlotPos, dstSlotPos, srcItemCount)
		
	if app.ENABLE_SELL_ITEM:
		def __SendSellItemPacket(self, itemVNum):
			if uiPrivateShopBuilder.IsBuildingPrivateShop():
				chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.USE_ITEM_FAILURE_PRIVATE_SHOP)
				return
				
			net.SendItemSellPacket(itemVNum)
			
	def OverOutItem(self):
		self.wndItem.SetUsableItem(False)
		if self.tooltipItem:
			self.tooltipItem.HideToolTip()
	
	def ResetItemSize(self):
		self.wndItem.ArrangeSlot(0, 5, 9, 34, 34, 0, 0)
		self.wndItem.RefreshSlot()
		self.wndItem.SetSlotBaseImage("d:/ymir work/ui/public/Slot_Base.sub", 1.0, 1.0, 1.0, 1.0)	