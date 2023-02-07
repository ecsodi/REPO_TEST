import thenewui as ui
import CacheEffect as player
import app
import item
import ShapeSkin as chrmgr
import Collision as chr
import wndMgr

WEAR_MAX_NUM = 32
COSTUME_START_INDEX = 19
COSTUME_MAX_NUM = 5

class CostumeWindow(ui.ScriptWindow):
	def __init__(self, wndInventory):
		import exception

		if not wndInventory:
			exception.Abort("wndInventory parameter must be set to InventoryWindow")
			return

		ui.ScriptWindow.__init__(self)

		self.isLoaded = 0
		self.wndInventory = wndInventory;

		self.__LoadWindow()

	def __del__(self):
		ui.ScriptWindow.__del__(self)

	def Show(self):
		self.__LoadWindow()
		self.RefreshCostumeSlot()
		ui.ScriptWindow.Show(self)

		self.AdjustPositionAndSize()

	def Close(self):
		self.Hide()

		self.AdjustPositionAndSize()

	def GetBasePosition(self):
		x, y = self.wndInventory.GetGlobalPosition()
		return x - 140, y

	def AdjustPositionAndSize(self):
		bx, by = self.GetBasePosition()

		self.SetPosition(bx, by);

	def __LoadWindow(self):
		if self.isLoaded == 1:
			return

		self.isLoaded = 1

		try:
			pyScrLoader = ui.PythonScriptLoader()
			pyScrLoader.LoadScriptFile(self, "UIScript/InventoryView/costumewindow_effect_slot.py")
		except:
			import exception
			exception.Abort("CostumeWindow.LoadWindow.LoadObject")

		try:
			wndEquip = self.GetChild("CostumeSlot")
			self.GetChild("TitleBar").SetCloseEvent(ui.__mem_func__(self.Close))
		except:
			import exception
			exception.Abort("CostumeWindow.LoadWindow.BindObject")

		wndEquip.SetOverInItemEvent(ui.__mem_func__(self.wndInventory.OverInItemEquipment))
		wndEquip.SetOverOutItemEvent(ui.__mem_func__(self.wndInventory.OverOutItem))
		self.wndEquip = wndEquip

	def RefreshCostumeSlot(self):
		for i in xrange(COSTUME_MAX_NUM):
			slotNumber = COSTUME_START_INDEX + i

			if not self.wndInventory.equipmentItems.has_key(slotNumber):
				continue

			self.wndEquip.SetItemSlot(slotNumber, self.wndInventory.equipmentItems[slotNumber]["vnum"], 0)

			if app.ENABLE_CHANGELOOK_SYSTEM:
				itemTransmutedVnum = self.wndInventory.equipmentItems[slotNumber]["transmutation"]
				if itemTransmutedVnum:
					self.wndEquip.DisableCoverButton(slotNumber)
				else:
					self.wndEquip.EnableCoverButton(slotNumber)

		self.wndEquip.RefreshSlot()

class BeltInventoryWindow(ui.ScriptWindow):
	def __init__(self, wndInventory):
		import exception

		if not wndInventory:
			exception.Abort("wndInventory parameter must be set to InventoryWindow")
			return

		ui.ScriptWindow.__init__(self)

		self.isLoaded = 0
		self.wndInventory = wndInventory;

		self.wndBeltInventoryLayer = None
		self.wndBeltInventorySlot = None
		self.expandBtn = None
		self.minBtn = None

		self.__LoadWindow()

	def __del__(self):
		ui.ScriptWindow.__del__(self)

	def Show(self, openBeltSlot = False):
		self.__LoadWindow()
		self.RefreshSlot()

		ui.ScriptWindow.Show(self)

		if openBeltSlot:
			self.OpenInventory()
		else:
			self.CloseInventory()

	def Close(self):
		self.Hide()

	def IsOpeningInventory(self):
		return self.wndBeltInventoryLayer.IsShow()

	def OpenInventory(self):
		self.wndBeltInventoryLayer.Show()
		self.expandBtn.Hide()
		self.AdjustPositionAndSize()

	def CloseInventory(self):
		self.wndBeltInventoryLayer.Hide()
		self.expandBtn.Show()
		self.AdjustPositionAndSize()

	def GetBasePosition(self):
		x, y = self.wndInventory.GetGlobalPosition()
		return x - 148, y + 241

	def AdjustPositionAndSize(self):
		bx, by = self.GetBasePosition()

		if self.IsOpeningInventory():
			self.SetPosition(bx, by)
			self.SetSize(self.ORIGINAL_WIDTH, self.GetHeight())
		else:
			self.SetPosition(bx + 138, by);
			self.SetSize(10, self.GetHeight())

	def __LoadWindow(self):
		if self.isLoaded == 1:
			return

		self.isLoaded = 1

		try:
			pyScrLoader = ui.PythonScriptLoader()
			pyScrLoader.LoadScriptFile(self, "UIScript/InventoryView/BeltInventoryWindow.py")
		except:
			import exception
			exception.Abort("CostumeWindow.LoadWindow.LoadObject")

		try:
			self.ORIGINAL_WIDTH = self.GetWidth()
			wndBeltInventorySlot = self.GetChild("BeltInventorySlot")
			self.wndBeltInventoryLayer = self.GetChild("BeltInventoryLayer")
			self.expandBtn = self.GetChild("ExpandBtn")
			self.minBtn = self.GetChild("MinimizeBtn")

			self.expandBtn.SetEvent(ui.__mem_func__(self.OpenInventory))
			self.minBtn.SetEvent(ui.__mem_func__(self.CloseInventory))
		except:
			import exception
			exception.Abort("CostumeWindow.LoadWindow.BindObject")

		## Equipment
		wndBeltInventorySlot.SetOverInItemEvent(ui.__mem_func__(self.wndInventory.OverInItemBelt))
		wndBeltInventorySlot.SetOverOutItemEvent(ui.__mem_func__(self.wndInventory.OverOutItem))
		
		self.wndBeltInventorySlot = wndBeltInventorySlot

	def RefreshSlot(self):
		for slotNumber in xrange(item.BELT_INVENTORY_SLOT_COUNT):
			if not self.wndInventory.beltInventoryItems.has_key(slotNumber):
				continue
		
			beltInventory = self.wndInventory.beltInventoryItems[slotNumber]

			self.wndBeltInventorySlot.SetItemSlot(slotNumber, beltInventory["vnum"], beltInventory["count"])

		self.wndBeltInventorySlot.RefreshSlot()

class InventoryWindow(ui.ScriptWindow):
	tooltipItem = None
	wndCostume = None
	wndBelt = None
	interface = None

	isLoaded = 0
	isOpenedCostumeWindowWhenClosingInventory = 0
	isOpenedBeltWindowWhenClosingInventory = 0

	def __init__(self):
		ui.ScriptWindow.__init__(self)

		self.isOpenedBeltWindowWhenClosingInventory = 0

		self.equipmentItems = { }
		self.inventoryItems = { }
		self.beltInventoryItems = { }

		self.__LoadWindow()

	def __del__(self):
		ui.ScriptWindow.__del__(self)

	def Show(self):
		self.__LoadWindow()

		ui.ScriptWindow.Show(self)

		self.equipmentItems = { }
		self.inventoryItems = { }
		self.beltInventoryItems = { }

		if self.isOpenedCostumeWindowWhenClosingInventory and self.wndCostume:
			self.wndCostume.Show()

		if self.wndBelt:
			self.wndBelt.Show(self.isOpenedBeltWindowWhenClosingInventory)

	def BindInterfaceClass(self, interface):
		self.interface = interface

	def __LoadWindow(self):
		if self.isLoaded == 1:
			return

		self.isLoaded = 1

		try:
			pyScrLoader = ui.PythonScriptLoader()
			pyScrLoader.LoadScriptFile(self, "UIScript/InventoryView/InventoryWindow.py")
		except:
			import exception
			exception.Abort("InventoryWindow.LoadWindow.LoadObject")

		try:
			wndItem = self.GetChild("ItemSlot")
			wndEquip = self.GetChild("EquipmentSlot")

			self.GetChild("TitleBar").SetCloseEvent(ui.__mem_func__(self.Close))

			self.costumeButton = self.GetChild2("CostumeButton")
			self.titleName = self.GetChild2("TitleName")

			self.inventoryTab = []
			self.inventoryTab.append(self.GetChild("Inventory_Tab_01"))
			self.inventoryTab.append(self.GetChild("Inventory_Tab_02"))
			self.inventoryTab.append(self.GetChild("Inventory_Tab_03"))
			self.inventoryTab.append(self.GetChild("Inventory_Tab_04"))

			self.wndBelt = BeltInventoryWindow(self)
		except:
			import exception
			exception.Abort("InventoryWindow.LoadWindow.BindObject")

		wndItem.SetOverInItemEvent(ui.__mem_func__(self.OverInItem))
		wndItem.SetOverOutItemEvent(ui.__mem_func__(self.OverOutItem))
		wndEquip.SetOverInItemEvent(ui.__mem_func__(self.OverInItemEquipment))
		wndEquip.SetOverOutItemEvent(ui.__mem_func__(self.OverOutItem))

		self.inventoryTab[0].SetEvent(lambda arg=0: self.SetInventoryPage(arg))
		self.inventoryTab[1].SetEvent(lambda arg=1: self.SetInventoryPage(arg))
		self.inventoryTab[2].SetEvent(lambda arg=2: self.SetInventoryPage(arg))
		self.inventoryTab[3].SetEvent(lambda arg=3: self.SetInventoryPage(arg))
		self.inventoryTab[0].Down()
		self.inventoryPageIndex = 0

		self.wndItem = wndItem
		self.wndEquip = wndEquip

		if self.costumeButton:
			self.costumeButton.SetEvent(ui.__mem_func__(self.ClickCostumeButton))

		self.wndCostume = None

		self.SetInventoryPage(0)
		self.RefreshEquipSlotWindow()
		self.RefreshItemSlot()

	def Destroy(self):
		self.ClearDictionary()

		self.tooltipItem = None
		self.wndItem = 0
		self.wndEquip = 0
		self.interface = None

		if self.wndCostume:
			self.wndCostume.Destroy()
			self.wndCostume = 0

		if self.wndBelt:
			self.wndBelt.Destroy()
			self.wndBelt = None

		self.inventoryTab = []

		self.equipmentItems = { }
		self.inventoryItems = { }
		self.beltInventoryItems = { }

	def Hide(self):
		if None != self.tooltipItem:
			self.tooltipItem.HideToolTip()

		if self.wndCostume:
			self.isOpenedCostumeWindowWhenClosingInventory = self.wndCostume.IsShow()
			self.wndCostume.Close()

		if self.wndBelt:
			self.isOpenedBeltWindowWhenClosingInventory = self.wndBelt.IsOpeningInventory()
			self.wndBelt.Close()

		wndMgr.Hide(self.hWnd)

	def Close(self):
		self.Hide()

	def Open(self, chrVid):
		self.Show()
		self.SetTop()
		self.SetCenterPosition()

		if self.wndBelt:
			self.wndBelt.AdjustPositionAndSize()

		if self.wndCostume:
			self.wndCostume.AdjustPositionAndSize()

		self.titleName.SetText("Inventar %s" % chr.GetNameByVID(chrVid))

	def SetInventoryPage(self, page):
		self.inventoryTab[self.inventoryPageIndex].SetUp()
		self.inventoryPageIndex = page
		self.inventoryTab[self.inventoryPageIndex].Down()
		self.RefreshBagSlotWindow()

	def ClickCostumeButton(self):
		if self.wndCostume:
			if self.wndCostume.IsShow():
				self.wndCostume.Hide()
			else:
				self.wndCostume.Show()
		else:
			self.wndCostume = CostumeWindow(self)
			self.wndCostume.Show()

	def AddItemInInventory(self, pageIndex, slotIndex, itemVnum, itemCount):
		tempDict = { 
			"vnum" : itemVnum,
			"count" : itemCount,
			"socket" : { 0 : 0, 1 : 0, 2 : 0 },
			"attr" : { 0 : [0, 0], 1 : [0, 0], 2 : [0, 0], 3 : [0, 0], 4 : [0, 0], 5 : [0, 0], 5 : [0, 0], 6 : [0, 0] },
			"transmutation" : 0,
			"bind" : 0,
		}

		if pageIndex == 1:
			self.equipmentItems[slotIndex] = tempDict
		elif pageIndex == 2:
			self.inventoryItems[slotIndex] = tempDict
		elif pageIndex == 3:
			self.beltInventoryItems[slotIndex] = tempDict

		self.RefreshEquipSlotWindow()
		self.RefreshItemSlot()

	def InventoryItemAddSocket(self, pageIndex, slotIndex, socketIndex, socketValue):
		if pageIndex == 1:
			self.equipmentItems[slotIndex]["socket"][socketIndex] = socketValue
		elif pageIndex == 2:
			self.inventoryItems[slotIndex]["socket"][socketIndex] = socketValue
		elif pageIndex == 3:
			self.beltInventoryItems[slotIndex]["socket"][socketIndex] = socketValue

	def InventoryItemAddAttr(self, pageIndex, slotIndex, attrIndex, attrType, attrValue):
		if pageIndex == 1:
			self.equipmentItems[slotIndex]["attr"][attrIndex][0] = attrType
			self.equipmentItems[slotIndex]["attr"][attrIndex][1] = attrValue
		elif pageIndex == 2:
			self.inventoryItems[slotIndex]["attr"][attrIndex][0] = attrType
			self.inventoryItems[slotIndex]["attr"][attrIndex][1] = attrValue
		elif pageIndex == 3:
			self.beltInventoryItems[slotIndex]["attr"][attrIndex][0] = attrType
			self.beltInventoryItems[slotIndex]["attr"][attrIndex][1] = attrValue

	if app.ENABLE_CHANGELOOK_SYSTEM:
		def InventoryItemAddTransmutation(self, pageIndex, slotIndex, transmutation):
			if pageIndex == 1:
				self.equipmentItems[slotIndex]["transmutation"] = transmutation
			elif pageIndex == 2:
				self.inventoryItems[slotIndex]["transmutation"] = transmutation
			elif pageIndex == 3:
				self.beltInventoryItems[slotIndex]["transmutation"] = transmutation

	def __InventoryLocalSlotPosToGlobalSlotPos(self, local):
		return self.inventoryPageIndex * player.INVENTORY_PAGE_SIZE + local

	def __InventoryGlobalSlotPosToLocalSlotPos(self, globalPos):
		return globalPos - self.inventoryPageIndex * player.INVENTORY_PAGE_SIZE

	def GetInventoryPageIndex(self):
		return self.inventoryPageIndex

	def RefreshBagSlotWindow(self):
		for i in xrange(player.INVENTORY_PAGE_SIZE):
			slotNumber = self.__InventoryLocalSlotPosToGlobalSlotPos(i)

			if not self.inventoryItems.has_key(slotNumber):
				continue

			itemCount = self.inventoryItems[slotNumber]["count"]

			if 0 == itemCount:
				self.wndItem.ClearSlot(i)
				continue
			elif 1 == itemCount:
				itemCount = 0

			self.wndItem.SetItemSlot(i, self.inventoryItems[slotNumber]["vnum"], itemCount)

			if app.ENABLE_CHANGELOOK_SYSTEM:
				itemTransmutedVnum = self.inventoryItems[slotNumber]["transmutation"]
				if itemTransmutedVnum:
					self.wndItem.DisableCoverButton(i)
				else:
					self.wndItem.EnableCoverButton(i)

		self.wndItem.RefreshSlot()

		if self.wndBelt:
			self.wndBelt.RefreshSlot()

	def RefreshEquipSlotWindow(self):
		for slotNumber in xrange(WEAR_MAX_NUM):
			if not self.equipmentItems.has_key(slotNumber):
				continue

			itemCount = self.equipmentItems[slotNumber]["count"]

			if itemCount <= 1:
				itemCount = 0

			self.wndEquip.SetItemSlot(slotNumber, self.equipmentItems[slotNumber]["vnum"], itemCount)

			if app.ENABLE_CHANGELOOK_SYSTEM:
				itemTransmutedVnum = self.equipmentItems[slotNumber]["transmutation"]
				if itemTransmutedVnum:
					self.wndEquip.DisableCoverButton(slotNumber)
				else:
					self.wndEquip.EnableCoverButton(slotNumber)

		self.wndEquip.RefreshSlot()

		if self.wndCostume:
			self.wndCostume.RefreshCostumeSlot()

	def RefreshItemSlot(self):
		self.RefreshBagSlotWindow()
		self.RefreshEquipSlotWindow()

	def SetItemToolTip(self, tooltipItem):
		self.tooltipItem = tooltipItem

	def OverOutItem(self):
		if None != self.tooltipItem:
			self.tooltipItem.HideToolTip()

	def OverInItem(self, slotIndex):
		slotIndex = self.__InventoryLocalSlotPosToGlobalSlotPos(slotIndex)

		metinSlot = []
		for i in xrange(player.METIN_SOCKET_MAX_NUM):
			metinSlot.append(self.inventoryItems[slotIndex]["socket"][i])

		attrSlot = []
		for j in xrange(player.ATTRIBUTE_SLOT_MAX_NUM):
			attrSlot.append((self.inventoryItems[slotIndex]["attr"][j][0], self.inventoryItems[slotIndex]["attr"][j][1]))

		if None != self.tooltipItem:
			self.tooltipItem.ClearToolTip()

			if app.ENABLE_CHANGELOOK_SYSTEM:
				transmutation = self.inventoryItems[slotIndex]["transmutation"]
				if not transmutation:
					self.tooltipItem.AddItemData(self.inventoryItems[slotIndex]["vnum"], metinSlot, attrSlot)
				else:
					self.tooltipItem.AddItemData(self.inventoryItems[slotIndex]["vnum"], metinSlot, attrSlot, 0, player.INVENTORY, -1, transmutation)
			else:
				self.tooltipItem.AddItemData(self.inventoryItems[slotIndex]["vnum"], metinSlot, attrSlot)

	def OverInItemEquipment(self, slotIndex):
		if not self.equipmentItems.has_key(slotIndex):
			return

		metinSlot = []
		for i in xrange(player.METIN_SOCKET_MAX_NUM):
			metinSlot.append(self.equipmentItems[slotIndex]["socket"][i])

		attrSlot = []
		for j in xrange(player.ATTRIBUTE_SLOT_MAX_NUM):
			attrSlot.append((self.equipmentItems[slotIndex]["attr"][j][0], self.equipmentItems[slotIndex]["attr"][j][1]))

		if None != self.tooltipItem:
			self.tooltipItem.ClearToolTip()

			if app.ENABLE_CHANGELOOK_SYSTEM:
				transmutation = self.equipmentItems[slotIndex]["transmutation"]
				if not transmutation:
					self.tooltipItem.AddItemData(self.equipmentItems[slotIndex]["vnum"], metinSlot, attrSlot)
				else:
					self.tooltipItem.AddItemData(self.equipmentItems[slotIndex]["vnum"], metinSlot, attrSlot, 0, player.INVENTORY, -1, transmutation)
			else:
				self.tooltipItem.AddItemData(self.equipmentItems[slotIndex]["vnum"], metinSlot, attrSlot)

	def OverInItemBelt(self, slotIndex):
		if not self.beltInventoryItems.has_key(slotIndex):
			return

		metinSlot = []
		for i in xrange(player.METIN_SOCKET_MAX_NUM):
			metinSlot.append(self.beltInventoryItems[slotIndex]["socket"][i])

		attrSlot = []
		for j in xrange(player.ATTRIBUTE_SLOT_MAX_NUM):
			attrSlot.append((self.beltInventoryItems[slotIndex]["attr"][j][0], self.beltInventoryItems[slotIndex]["attr"][j][1]))

		if None != self.tooltipItem:
			self.tooltipItem.ClearToolTip()

			if app.ENABLE_CHANGELOOK_SYSTEM:
				transmutation = self.beltInventoryItems[slotIndex]["transmutation"]
				if not transmutation:
					self.tooltipItem.AddItemData(self.beltInventoryItems[slotIndex]["vnum"], metinSlot, attrSlot)
				else:
					self.tooltipItem.AddItemData(self.beltInventoryItems[slotIndex]["vnum"], metinSlot, attrSlot, 0, player.INVENTORY, -1, transmutation)
			else:
				self.tooltipItem.AddItemData(self.beltInventoryItems[slotIndex]["vnum"], metinSlot, attrSlot)

	def OnTop(self):
		if None != self.tooltipItem:
			self.tooltipItem.SetTop()

	def OnPressEscapeKey(self):
		self.Close()
		return True

	def OnMoveWindow(self, x, y):
		if self.wndBelt:
			self.wndBelt.AdjustPositionAndSize()

		if self.wndCostume:
			self.wndCostume.AdjustPositionAndSize()