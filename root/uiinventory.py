import thenewui as ui
import CacheEffect as player
import mouseModule
import net
import app
import item
import chat
import grp
import uiScriptLocale
import uiRefine
import uiAttachMetin
import uiPickMoney
import uiCommon
import uiPrivateShopBuilder
import localeInfo
import constInfo
import ime
import wndMgr
import exchange
import uiToolTip
import shop
if app.ENABLE_CHANGELOOK_SYSTEM:
	import changelook
import cfg
if app.ENABLE_SASH_SYSTEM:
	import sash
if app.ENABLE_COSTUME_SYSTEM: #ENABLE_RENDER_TARGET_SYSTEM
	import renderTargetExtension
if app.ENABLE_OFFLINE_SHOP:
	import shop
if app.ENABLE_PREMIUM_SYSTEM_EXTRA:
	import uiPremium
	
import safebox
ENABLE_DEBUG_SLOTS = False
ITEM_FLAG_APPLICABLE = 1 << 14
class CostumeWindow(ui.ScriptWindow):

	def __init__(self, wndInventory):
		import exception

		if not app.ENABLE_COSTUME_SYSTEM:
			exception.Abort("What do you do?")
			return

		if not wndInventory:
			exception.Abort("wndInventory parameter must be set to InventoryWindow")
			return

		ui.ScriptWindow.__init__(self)

		self.isLoaded = 0
		self.wndInventory = wndInventory;

		self.keyHideCostumeStatus = {}
		for x in xrange(5):
			self.keyHideCostumeStatus[x] = 0

		self.__LoadWindow()
		self.CreateHideCostume()
		self.CreateHideCostumeImages()

	def __del__(self):
		self.keyHideCostumeStatus = {}
		self.dictHideCostumeButton = []
		self.dictHideCostumeImages = []
		ui.ScriptWindow.__del__(self)

	def Show(self):
		self.__LoadWindow()
		self.RefreshCostumeSlot()
		ui.ScriptWindow.Show(self)

	def Close(self):
		self.Hide()
		
	def __LoadWindow(self):
		if self.isLoaded == 1:
			return

		self.isLoaded = 1

		try:
			pyScrLoader = ui.PythonScriptLoader()
			pyScrLoader.LoadScriptFile(self, "UIScript/costumewindow.py")
		except:
			import exception
			exception.Abort("CostumeWindow.LoadWindow.LoadObject")

		try:
			wndEquip = self.GetChild("CostumeSlot")
			wndBuffi = self.GetChild("BuffiSlot")
			self.GetChild("TitleBar").SetCloseEvent(ui.__mem_func__(self.Close))
			costumePage = self.GetChild("Costume_Base")
			buffiPage = self.GetChild("Buffi_Base")
			board = self.GetChild("board")

			self.inventoryTab = []
			self.inventoryTab.append(self.GetChild("CostumeButton"))
			self.inventoryTab.append(self.GetChild("BuffiButton"))

		except:
			import exception
			exception.Abort("CostumeWindow.LoadWindow.BindObject")
			
		costumePage.LoadImage("d:/ymir work/ui/game/normal_interface/normal_costume.png")
		buffiPage.LoadImage("d:/ymir work/ui/game/normal_interface/buffi_costume.png")
			
		## Equipment
		wndEquip.SetOverInItemEvent(ui.__mem_func__(self.wndInventory.OverInItem))
		wndEquip.SetOverOutItemEvent(ui.__mem_func__(self.wndInventory.OverOutItem))
		wndEquip.SetUnselectItemSlotEvent(ui.__mem_func__(self.wndInventory.UseItemSlot))
		wndEquip.SetUseSlotEvent(ui.__mem_func__(self.wndInventory.UseItemSlot))
		wndEquip.SetSelectEmptySlotEvent(ui.__mem_func__(self.wndInventory.SelectEmptySlot))
		wndEquip.SetSelectItemSlotEvent(ui.__mem_func__(self.wndInventory.SelectItemSlot))
		
		wndBuffi.SetOverInItemEvent(ui.__mem_func__(self.wndInventory.OverInItem))
		wndBuffi.SetOverOutItemEvent(ui.__mem_func__(self.wndInventory.OverOutItem))
		wndBuffi.SetUnselectItemSlotEvent(ui.__mem_func__(self.wndInventory.UseItemSlot))
		wndBuffi.SetUseSlotEvent(ui.__mem_func__(self.wndInventory.UseItemSlot))
		wndBuffi.SetSelectEmptySlotEvent(ui.__mem_func__(self.TestFunc))
		wndBuffi.SetSelectItemSlotEvent(ui.__mem_func__(self.wndInventory.SelectItemSlot))
		
		self.inventoryTab[0].SetEvent(lambda arg=0: self.SetInventoryPage(arg))
		self.inventoryTab[1].SetEvent(lambda arg=1: self.SetInventoryPage(arg))
		self.inventoryTab[0].Down()
		self.inventoryPageIndex = 0
		
		self.wndEquip = wndEquip
		self.wndBuffi = wndBuffi
		self.board = board

		self.costumePage = costumePage
		self.costumePage.Show()
		self.buffiPage = buffiPage
		self.buffiPage.Hide()

	def TestFunc(self):
		chat.AppendChat(1, "To equip, place the item on the buffi npc.")
		return

	def SetInventoryPage(self, page):
		if self.inventoryTab[page].IsShow() == FALSE: # @ Fix Mouse Wheel
			return
	
		self.inventoryTab[self.inventoryPageIndex].SetUp()
		self.inventoryPageIndex = page
		self.inventoryTab[self.inventoryPageIndex].Down()
		
		if page == 0:
			self.buffiPage.Hide()
			self.costumePage.Show()
			self.board.SetSize(192, 230)
			self.SetSize(192, 230)
			self.CreateHideCostume(True)
		elif page == 1:
			self.costumePage.Hide()
			self.buffiPage.Show()
			self.board.SetSize(192, 193)
			self.SetSize(192, 193)
			self.CreateHideCostume(False)
			
		self.RefreshCostumeSlot()
		
	def CreateHideCostumeImages(self, isShown = True):
		self.dictHideCostumeImages = []
		
		xPos = [65, 65, 115, 17, 115]
		yPos = [45, 9, 45, 13, 9]
		images = ["d:/ymir work/ui/costume/hideslot_02.tga", "d:/ymir work/ui/costume/hideslot_01.tga", "d:/ymir work/ui/costume/hideslot_01.tga", "d:/ymir work/ui/costume/hideslot_03.tga", "d:/ymir work/ui/costume/hideslot_01.tga"]
		for x in xrange(5):
			imageBox = ui.ImageBox()
			imageBox.SetParent(self.costumePage)
			imageBox.LoadImage(images[x])
			imageBox.SetPosition(xPos[x] + 2, yPos[x] + 3)
			self.dictHideCostumeImages.append(imageBox)

	def SetHideCostumePart(self, index, status):
		self.keyHideCostumeStatus[index] = status
		
		try:
			if status:
				self.dictHideCostumeButton[index].SetUpVisual("d:/ymir work/ui/costume/eye_closed_01.tga")
				self.dictHideCostumeButton[index].SetOverVisual("d:/ymir work/ui/costume/eye_closed_02.tga")
				self.dictHideCostumeImages[index].Show()
			else:
				self.dictHideCostumeButton[index].SetUpVisual("d:/ymir work/ui/costume/eye_normal_01.tga")
				self.dictHideCostumeButton[index].SetOverVisual("d:/ymir work/ui/costume/eye_normal_02.tga")
				self.dictHideCostumeImages[index].Hide()
		except Exception:
			pass

	def CreateHideCostume(self, isShown = True):
		self.dictHideCostumeButton = []
		
		xPos = [61, 61, 115, 12, 115]
		yPos = [45, 8, 45, 11, 8]
		for x in xrange(5):
			button = ui.Button()
			button.SetParent(self)
			button.SetUpVisual("d:/ymir work/ui/costume/eye_normal_01.tga")
			button.SetOverVisual("d:/ymir work/ui/costume/eye_normal_02.tga")
			button.SetDownVisual("d:/ymir work/ui/costume/eye_closed_02.tga")
			button.SetPosition(40 + xPos[x], 55 + yPos[x])
			button.SetEvent(ui.__mem_func__(self.SendHideCostume), x)
			
			if isShown == False:
				button.Hide()
			else:
				button.Show()
			
			self.dictHideCostumeButton.append(button)

	def SendHideCostume(self, index):
		net.SendChatPacket("/hide_costume %d %d" % (1 + index, not self.keyHideCostumeStatus[index]))
	
	def RefreshCostumeSlot(self):
		getItemVNum=player.GetItemIndex

		for i in xrange(item.COSTUME_SLOT_COUNT + 30):
			slotNumber = item.COSTUME_SLOT_START + i
			self.wndEquip.SetItemSlot(slotNumber, getItemVNum(slotNumber), 0)
			self.wndBuffi.SetItemSlot(slotNumber, getItemVNum(slotNumber), 0)
			
			# if getItemVNum(slotNumber):
				# chat.AppendChat(1, "COSTUME: ItemVnum: %d, Slot: %d" % (getItemVNum(slotNumber), slotNumber))

			if app.ENABLE_CHANGELOOK_SYSTEM:
				itemTransmutedVnum = player.GetItemTransmutation(slotNumber)
				if itemTransmutedVnum:
					self.wndEquip.DisableCoverButton(slotNumber)
				else:
					self.wndEquip.EnableCoverButton(slotNumber)
		
		EQUIPMENT_START_INDEX = 180 + 810

		v_slot = [item.COSTUME_SLOT_WEAPON, item.COSTUME_SLOT_START,\
				item.COSTUME_SLOT_START+1, EQUIPMENT_START_INDEX+29,\
				item.COSTUME_SLOT_START+2, EQUIPMENT_START_INDEX+30]
		
		for slotNumber in v_slot:
			self.wndEquip.SetItemSlot(slotNumber, getItemVNum(slotNumber), 0)
			if app.ENABLE_CHANGELOOK_SYSTEM:
				changelookvnum = player.GetItemTransmutation(slotNumber)
				if changelookvnum:
					self.wndEquip.DisableCoverButton(slotNumber)
				else:
					self.wndEquip.EnableCoverButton(slotNumber)
		
		slotNumber = item.EQUIPMENT_BELT + 1
		self.wndEquip.SetItemSlot(slotNumber, getItemVNum(slotNumber), 0)
		self.wndBuffi.SetItemSlot(slotNumber, getItemVNum(slotNumber), 0)

		if app.ENABLE_CHANGELOOK_SYSTEM:
			itemTransmutedVnum = player.GetItemTransmutation(slotNumber)
			if itemTransmutedVnum:
				self.wndEquip.DisableCoverButton(slotNumber)
			else:
				self.wndEquip.EnableCoverButton(slotNumber)
		
		self.wndEquip.RefreshSlot()	
		self.wndBuffi.RefreshSlot()	

class BeltInventoryWindow(ui.ScriptWindow):

	def __init__(self, wndInventory):
		import exception

		if not app.ENABLE_NEW_EQUIPMENT_SYSTEM:
			exception.Abort("What do you do?")
			return

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

	def CloseInventory(self):
		self.wndBeltInventoryLayer.Hide()
		self.expandBtn.Show()

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
			pyScrLoader.LoadScriptFile(self, "UIScript/BeltInventoryWindow.py")
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

			for i in xrange(item.BELT_INVENTORY_SLOT_COUNT):
				slotNumber = item.BELT_INVENTORY_SLOT_START + i
				wndBeltInventorySlot.SetCoverButton(slotNumber,	"d:/ymir work/ui/game/quest/slot_button_01.sub",\
												"d:/ymir work/ui/game/quest/slot_button_01.sub",\
												"d:/ymir work/ui/game/quest/slot_button_01.sub",\
												"d:/ymir work/ui/game/belt_inventory/slot_disabled.tga", False, False)

		except:
			import exception
			exception.Abort("CostumeWindow.LoadWindow.BindObject")

		## Equipment
		wndBeltInventorySlot.SetOverInItemEvent(ui.__mem_func__(self.wndInventory.OverInItem))
		wndBeltInventorySlot.SetOverOutItemEvent(ui.__mem_func__(self.wndInventory.OverOutItem))
		wndBeltInventorySlot.SetUnselectItemSlotEvent(ui.__mem_func__(self.wndInventory.UseItemSlot))
		wndBeltInventorySlot.SetUseSlotEvent(ui.__mem_func__(self.wndInventory.UseItemSlot))
		wndBeltInventorySlot.SetSelectEmptySlotEvent(ui.__mem_func__(self.wndInventory.SelectEmptySlot))
		wndBeltInventorySlot.SetSelectItemSlotEvent(ui.__mem_func__(self.wndInventory.SelectItemSlot))

		self.wndBeltInventorySlot = wndBeltInventorySlot

	def RefreshSlot(self):

		getItemVNum=player.GetItemIndex

		for i in xrange(item.BELT_INVENTORY_SLOT_COUNT):
			slotNumber = item.BELT_INVENTORY_SLOT_START + i
			self.wndBeltInventorySlot.SetItemSlot(slotNumber, getItemVNum(slotNumber), player.GetItemCount(slotNumber))
			self.wndBeltInventorySlot.SetAlwaysRenderCoverButton(slotNumber, True)

			avail = "0"

			if player.IsAvailableBeltInventoryCell(slotNumber):
				self.wndBeltInventorySlot.EnableCoverButton(slotNumber)
			else:
				self.wndBeltInventorySlot.DisableCoverButton(slotNumber)

		self.wndBeltInventorySlot.RefreshSlot()

class InventoryWindow(ui.ScriptWindow):

	USE_TYPE_TUPLE = ("USE_CLEAN_SOCKET", "USE_CHANGE_ATTRIBUTE", "USE_ADD_ATTRIBUTE", "USE_ADD_ATTRIBUTE2", "USE_ADD_ACCESSORY_SOCKET", "USE_PUT_INTO_ACCESSORY_SOCKET", "USE_PUT_INTO_BELT_SOCKET", "USE_PUT_INTO_RING_SOCKET")

	questionDialog = None
	tooltipItem = None
	wndCostume = None
	wndBelt = None

	dlgPickMoney = None
	interface = None
	if app.WJ_ENABLE_TRADABLE_ICON:
		bindWnds = []

	sellingSlotNumber = -1
	isLoaded = 0
	isOpenedCostumeWindowWhenClosingInventory = 0		# 
	isOpenedBeltWindowWhenClosingInventory = 0		# 

	# if app.ENABLE_HIGHLIGHT_NEW_ITEM:
	liHighlightedItems = []

	def __init__(self):
		if constInfo.ENABLE_EXPANDED_MONEY_TASKBAR:
			self.wndExpandedMoneyBar = None
			self.wndMoney = None
			self.wndMoneySlot = None
			
		ui.ScriptWindow.__init__(self)
		
		self.buttonTooltip		= None
		self.showButtonToolTip	= False
		
		self.wndSashCombine = None
		self.wndSashAbsorption = None
		self.wndDragonSoulRefine = None
		self.bSelectedEquip = False
			
		self.isOpenedBeltWindowWhenClosingInventory = 0		#
		self.__LoadWindow()

	def __del__(self):
		ui.ScriptWindow.__del__(self)

		if constInfo.ENABLE_EXPANDED_MONEY_TASKBAR:
			self.wndExpandedMoneyBar = None
			
		# @ Grimm Fix Memory Leaking
		if self.wndSashCombine:
			del self.wndSashCombine
		
		if self.wndSashAbsorption:
			del self.wndSashAbsorption
			
		if self.wndDragonSoulRefine:
			del self.wndDragonSoulRefine
	
	def SetHideCostumePart(self, index, status):
		if self.wndCostume:
			self.wndCostume.SetHideCostumePart(index, status)
	
	def Show(self):
		self.__LoadWindow()
		ui.ScriptWindow.Show(self)
		
		if self.isOpenedCostumeWindowWhenClosingInventory and self.wndCostume:
			self.wndCostume.Show()

		if self.wndBelt:
			self.wndBelt.Hide()

		if constInfo.ENABLE_EXPANDED_MONEY_TASKBAR:
			if self.wndExpandedMoneyBar:
				self.wndExpandedMoneyBar.Show()

		# GRIMM_NINJA_ARROWS
		if not self.bSelectedEquip:
			if player.GetJob() == 1: # NINJA
				self.wndEquip.AppendSlot(180 + 810 + 4, 3, 3, 32, 64)
				self.wndEquip.AppendSlot(180 + 810 + 9, 3, 66, 32, 32)
			else:
				self.wndEquip.AppendSlot(180 + 810 + 4, 3, 3, 32, 96)
				
			self.RefreshItemSlot()
				
		self.bSelectedEquip = True

	def BindInterfaceClass(self, interface):
		self.interface = interface

	if app.WJ_ENABLE_TRADABLE_ICON:
		def BindWindow(self, wnd):
			self.bindWnds.append(wnd)

	def __LoadWindow(self):
		if self.isLoaded == 1:
			return

		self.isLoaded = 1

		try:
			pyScrLoader = ui.PythonScriptLoader()
			pyScrLoader.LoadScriptFile(self, "uiscript/InventoryWindow_norm.py")
		except:
			import exception
			exception.Abort("InventoryWindow.LoadWindow.LoadObject")

		try:
			wndItem = self.GetChild("ItemSlot")
			wndEquip = self.GetChild("EquipmentSlot")
			self.board = self.GetChild("board")
			
			self.btnStorage = self.GetChild2("MallButton")
			self.btnShopSearch = self.GetChild2("ShopSearchButton")
			self.btnSwitch = self.GetChild2("SwitchbotBtn")
			
			self.GetChild("TitleBar").SetCloseEvent(ui.__mem_func__(self.Close))
			self.wndMoney = None
			self.wndMoneySlot = None
			self.mallButton = self.GetChild2("SpecialStorageButton")
			self.costumeButton = self.GetChild2("CostumeButton")

			self.dragonSoulButton = self.GetChild2("DSSButton")
			self.rewardButton = self.GetChild2("RewardButton")

			self.inventoryTab = []
			self.inventoryTab.append(self.GetChild("Inventory_Tab_01"))
			self.inventoryTab.append(self.GetChild("Inventory_Tab_02"))
			self.inventoryTab.append(self.GetChild("Inventory_Tab_03"))
			self.inventoryTab.append(self.GetChild("Inventory_Tab_04"))
			
			if self.costumeButton and not app.ENABLE_COSTUME_SYSTEM:
				self.costumeButton.Hide()
				self.costumeButton.Destroy()
				self.costumeButton = 0
				
			self.buttonTooltip = uiToolTip.ToolTip()
			self.buttonTooltip.ClearToolTip()
			
			# Belt Inventory Window
			self.wndBelt = None

			if app.ENABLE_NEW_EQUIPMENT_SYSTEM:
				self.wndBelt = BeltInventoryWindow(self)

		except:
			import exception
			exception.Abort("InventoryWindow.LoadWindow.BindObject")

		## Item
		wndItem.SetSelectEmptySlotEvent(ui.__mem_func__(self.SelectEmptySlot))
		wndItem.SetSelectItemSlotEvent(ui.__mem_func__(self.SelectItemSlot))
		wndItem.SetUnselectItemSlotEvent(ui.__mem_func__(self.UseItemSlot))
		wndItem.SetUseSlotEvent(ui.__mem_func__(self.UseItemSlot))
		wndItem.SetOverInItemEvent(ui.__mem_func__(self.OverInItem))
		wndItem.SetOverOutItemEvent(ui.__mem_func__(self.OverOutItem))

		## Equipment
		wndEquip.SetSelectEmptySlotEvent(ui.__mem_func__(self.SelectEmptySlot))
		wndEquip.SetSelectItemSlotEvent(ui.__mem_func__(self.SelectItemSlot))
		wndEquip.SetUnselectItemSlotEvent(ui.__mem_func__(self.UseItemSlot))
		wndEquip.SetUseSlotEvent(ui.__mem_func__(self.UseItemSlot))
		wndEquip.SetOverInItemEvent(ui.__mem_func__(self.OverInItem))
		wndEquip.SetOverOutItemEvent(ui.__mem_func__(self.OverOutItem))

		## PickMoneyDialog
		dlgPickMoney = uiPickMoney.PickMoneyDialog()
		dlgPickMoney.LoadDialog()
		dlgPickMoney.Hide()

		## RefineDialog
		self.refineDialog = uiRefine.RefineDialog()
		self.refineDialog.Hide()
	
		## AttachMetinDialog
		self.attachMetinDialog = uiAttachMetin.AttachMetinDialog()
		self.attachMetinDialog.Hide()

		self.inventoryTab[0].SetEvent(lambda arg=0: self.SetInventoryPage(arg))
		self.inventoryTab[1].SetEvent(lambda arg=1: self.SetInventoryPage(arg))
		self.inventoryTab[2].SetEvent(lambda arg=2: self.SetInventoryPage(arg))
		self.inventoryTab[3].SetEvent(lambda arg=3: self.SetInventoryPage(arg))
		self.inventoryTab[0].Down()
		self.inventoryPageIndex = 0

		self.wndItem = wndItem
		self.wndEquip = wndEquip
		self.dlgPickMoney = dlgPickMoney
		
		# MallButton
		if self.mallButton:
			self.mallButton.SetEvent(ui.__mem_func__(self.ClickMallButton))

		# Costume Button
		if self.costumeButton:
			self.costumeButton.SetEvent(ui.__mem_func__(self.ClickCostumeButton))

		if self.btnStorage:
			self.btnStorage.SetEvent(ui.__mem_func__(self.OpenStorage))

		if self.btnSwitch:
			self.btnSwitch.SetEvent(ui.__mem_func__(self.OpenSwitchbot))
			
		if self.dragonSoulButton:
			self.dragonSoulButton.SetEvent(ui.__mem_func__(self.OpenDragonSoul))
			
		if self.btnShopSearch:
			self.btnShopSearch.SetEvent(ui.__mem_func__(self.OpenSearchShop))
			
		if self.rewardButton:
			self.rewardButton.SetEvent(ui.__mem_func__(self.OpenRewardWindow))

		self.btnStorage.SetShowToolTipEvent(ui.__mem_func__(self.OverInToolTipButton), "Inventar Special")
		self.btnStorage.SetHideToolTipEvent(ui.__mem_func__(self.OverOutToolTipButton))
		self.dragonSoulButton.SetShowToolTipEvent(ui.__mem_func__(self.OverInToolTipButton), "Alchimie Dragon")
		self.dragonSoulButton.SetHideToolTipEvent(ui.__mem_func__(self.OverOutToolTipButton))
		self.btnSwitch.SetShowToolTipEvent(ui.__mem_func__(self.OverInToolTipButton), "Switchbot")
		self.btnSwitch.SetHideToolTipEvent(ui.__mem_func__(self.OverOutToolTipButton))
		self.mallButton.SetShowToolTipEvent(ui.__mem_func__(self.OverInToolTipButton), "Depozit Obiecte")
		self.mallButton.SetHideToolTipEvent(ui.__mem_func__(self.OverOutToolTipButton))
		self.btnShopSearch.SetShowToolTipEvent(ui.__mem_func__(self.OverInToolTipButton), localeInfo.PREMIUM_TEXT_10)
		self.btnShopSearch.SetHideToolTipEvent(ui.__mem_func__(self.OverOutToolTipButton))
		self.rewardButton.SetShowToolTipEvent(ui.__mem_func__(self.OverInToolTipButton), "Recompense")
		self.rewardButton.SetHideToolTipEvent(ui.__mem_func__(self.OverOutToolTipButton))
		
		self.wndCostume = None

		if app.ENABLE_SASH_SYSTEM:
			self.listAttachedSashs = []

 		#####
		if app.ENABLE_CHANGELOOK_SYSTEM:
			self.listAttachedCl = []

		## Refresh
		self.SetInventoryPage(0)
		self.RefreshItemSlot()
		self.RefreshStatus()

	def OpenStorage(self):
		if self.interface:
			self.interface.ToggleCustomInventoryWindow()

	def OpenDragonSoul(self):
		if self.interface:
			self.interface.ToggleDragonSoulWindowWithNoInfo()
	
	def OpenSearchShop(self):
		if self.interface:
			self.interface.OpenSearchShop()
	
	def OpenSwitchbot(self):
		net.SBOpen()
			
	def OpenRewardWindow(self):
		if self.interface:
			self.interface.OpenRewardWindow()
		
	def SetEquipPage(self, page):
		for x in xrange(len(self.dictPages)):
			if page == x:
				self.GetChild(self.dictPages[x].SetName).Show()
			else:
				self.GetChild(self.dictPages[x].SetName).Hide()
		
		self.wndEquip = self.GetChild(self.dictPages[page].SetNameChild)
		self.wndEquip.SetSelectEmptySlotEvent(ui.__mem_func__(self.SelectEmptySlot))
		self.wndEquip.SetSelectItemSlotEvent(ui.__mem_func__(self.SelectItemSlot))
		self.wndEquip.SetUnselectItemSlotEvent(ui.__mem_func__(self.UseItemSlot))
		self.wndEquip.SetUseSlotEvent(ui.__mem_func__(self.UseItemSlot))
		self.wndEquip.SetOverInItemEvent(ui.__mem_func__(self.OverInItem))
		self.wndEquip.SetOverOutItemEvent(ui.__mem_func__(self.OverOutItem))
		
		self.RefreshEquipSlotWindow()

	def Destroy(self):
		self.ClearDictionary()

		self.dlgPickMoney.Destroy()
		self.dlgPickMoney = 0

		self.refineDialog.Destroy()
		self.refineDialog = 0

		self.attachMetinDialog.Destroy()
		self.attachMetinDialog = 0
		self.buttonTooltip		= None
		self.showButtonToolTip	= False
		self.tooltipItem = None
		self.wndItem = 0
		self.wndEquip = 0
		self.dlgPickMoney = 0
		self.wndMoney = 0
		self.wndMoneySlot = 0
		self.questionDialog = None
		self.mallButton = None
		self.interface = None
		self.bSelectedEquip = False
		self.DSSEffectRenewal = False
		
		if app.WJ_ENABLE_TRADABLE_ICON:
			self.bindWnds = []

		if self.wndCostume:
			self.wndCostume.Destroy()
			self.wndCostume = 0

		if self.wndBelt:
			self.wndBelt.Destroy()
			self.wndBelt = None
			
		self.inventoryTab = []

		if constInfo.ENABLE_EXPANDED_MONEY_TASKBAR:
			self.wndExpandedMoneyBar = None

	def Hide(self):
		if constInfo.GET_ITEM_QUESTION_DIALOG_STATUS():
			self.OnCloseQuestionDialog()
			return
		if None != self.tooltipItem:
			self.tooltipItem.HideToolTip()

		if self.wndCostume:
			self.isOpenedCostumeWindowWhenClosingInventory = self.wndCostume.IsShow()
			self.wndCostume.Close()

		if self.wndBelt:
			self.isOpenedBeltWindowWhenClosingInventory = self.wndBelt.IsOpeningInventory()
			print "Is Opening Belt Inven?? ", self.isOpenedBeltWindowWhenClosingInventory
			self.wndBelt.Close()

		if self.dlgPickMoney:
			self.dlgPickMoney.Close()

		if constInfo.ENABLE_EXPANDED_MONEY_TASKBAR:
			if self.wndExpandedMoneyBar:
				self.wndExpandedMoneyBar.Close()

		wndMgr.Hide(self.hWnd)

	def OnRunMouseWheel(self, nLen):
		x, y = self.GetMouseLocalPosition()
		if nLen > 0:
			if self.inventoryPageIndex > 0:
				self.SetInventoryPage(self.inventoryPageIndex - 1)
		else:
			if self.inventoryPageIndex < 3:
				self.SetInventoryPage(self.inventoryPageIndex + 1)
						
	def UseDSSButtonEffect(self, enable):
		if self.dragonSoulButton:
			self.DSSEffectRenewal = ui.AniImageBox()
			self.DSSEffectRenewal.AddFlag("attach")
			self.DSSEffectRenewal.SetParent(self.dragonSoulButton)
			self.DSSEffectRenewal.SetDelay(7)
	
			for i in xrange(5):
				self.DSSEffectRenewal.AppendImageScale("d:/ymir work/ui/dragonsoul/efect_alchimie_nou_%d.sub" % int(i), 1.0, 1.0)
				self.DSSEffectRenewal.SetPosition(-3, -5)

			self.DSSEffectRenewal.UpdateRect()

			if enable == True:
				self.DSSEffectRenewal.Show()
				self.dragonSoulButton.SetUpVisual("d:/ymir work/ui/dragonsoul/dss_inventory_button_01_fire.png")
				self.dragonSoulButton.SetOverVisual("d:/ymir work/ui/dragonsoul/dss_inventory_button_02_fire.png")				
				self.dragonSoulButton.SetDownVisual("d:/ymir work/ui/dragonsoul/dss_inventory_button_03_fire.png")				
			else:
				self.DSSEffectRenewal.Hide()
				self.dragonSoulButton.SetUpVisual("d:/ymir work/ui/game/normal_interface/dss_inventory_button_01.tga")
				self.dragonSoulButton.SetOverVisual("d:/ymir work/ui/game/normal_interface/dss_inventory_button_02.tga")				
				self.dragonSoulButton.SetDownVisual("d:/ymir work/ui/game/normal_interface/dss_inventory_button_03.tga")

	def Close(self):
		if None != self.tooltipItem:
			self.tooltipItem.HideToolTip()
		
		if self.buttonTooltip:
			self.buttonTooltip.Hide()
			self.showButtonToolTip = False
			
		if self.wndCostume:
			self.isOpenedCostumeWindowWhenClosingInventory = self.wndCostume.IsShow()
			self.wndCostume.Close()

		if self.wndBelt:
			self.isOpenedBeltWindowWhenClosingInventory = self.wndBelt.IsOpeningInventory()
			self.wndBelt.CloseInventory()
			self.wndBelt.Close()
  
		if self.dlgPickMoney:
			self.dlgPickMoney.Close()

		self.OnCloseQuestionDialog()
		# wndMgr.Hide(self.hWnd)

		self.Hide()
		
	def OverInToolTipButton(self, btnText, text_len = 0):
		if self.buttonTooltip:
			if 0 == text_len:
				arglen = len(str(btnText))
			else:
				arglen = text_len
				
			pos_x, pos_y = wndMgr.GetMousePosition()
			
			self.buttonTooltip.ClearToolTip()
			self.buttonTooltip.SetThinBoardSize(9 * arglen)
			self.buttonTooltip.SetToolTipPosition(pos_x + 50, pos_y + 50)
			self.buttonTooltip.AppendTextLine(btnText, 0xffffffff)
			self.buttonTooltip.Show()
			self.buttonTooltip.SetTop()
			self.showButtonToolTip = True

	def OverOutToolTipButton(self):
		if self.buttonTooltip:
			self.buttonTooltip.Hide()
			self.showButtonToolTip = False

	def ButtonToolTipProgress(self):
		if self.buttonTooltip and self.showButtonToolTip:
			pos_x, pos_y = wndMgr.GetMousePosition()
			self.buttonTooltip.SetToolTipPosition(pos_x + 50, pos_y + 50)
			
	if constInfo.ENABLE_EXPANDED_MONEY_TASKBAR:
		def SetExpandedMoneyBar(self, wndBar):
			self.wndExpandedMoneyBar = wndBar
			if self.wndExpandedMoneyBar:
				self.wndMoney = self.wndExpandedMoneyBar.GetMoney()

	def SetInventoryPage(self, page):
		if self.inventoryTab[page].IsShow() == FALSE: # @ Fix Mouse Wheel
			return
	
		self.inventoryTab[self.inventoryPageIndex].SetUp()
		self.inventoryPageIndex = page
		self.inventoryTab[self.inventoryPageIndex].Down()
		self.RefreshBagSlotWindow()

	def ClickMallButton(self):
		print "click_mall_button"
		net.SendChatPacket("/click_mall")

	def ClickCostumeButton(self):
		print "Click Costume Button"
		if self.wndCostume:
			if self.wndCostume.IsShow():
				self.wndCostume.Hide()
			else:
				self.wndCostume.Show()
		else:
			self.wndCostume = CostumeWindow(self)
			self.wndCostume.Show()

	def OpenPickMoneyDialog(self):

		if mouseModule.mouseController.isAttached():

			attachedSlotPos = mouseModule.mouseController.GetAttachedSlotNumber()
			if player.SLOT_TYPE_SAFEBOX == mouseModule.mouseController.GetAttachedType():

				if player.ITEM_MONEY == mouseModule.mouseController.GetAttachedItemIndex():
					net.SendSafeboxWithdrawMoneyPacket(mouseModule.mouseController.GetAttachedItemCount())

			mouseModule.mouseController.DeattachObject()

		else:
			curMoney = player.GetElk()

			if curMoney <= 0:
				return

			self.dlgPickMoney.SetTitleName(localeInfo.PICK_MONEY_TITLE)
			self.dlgPickMoney.SetAcceptEvent(ui.__mem_func__(self.OnPickMoney))
			self.dlgPickMoney.Open(curMoney)
			self.dlgPickMoney.SetMax(7)

	def OnPickMoney(self, money):
		mouseModule.mouseController.AttachMoney(self, player.SLOT_TYPE_INVENTORY, money)

	def OnPickItem(self, count):
		itemSlotIndex = self.dlgPickMoney.itemGlobalSlotIndex
		selectedItemVNum = player.GetItemIndex(itemSlotIndex)
		mouseModule.mouseController.AttachObject(self, player.SLOT_TYPE_INVENTORY, itemSlotIndex, selectedItemVNum, count)

	def __InventoryLocalSlotPosToGlobalSlotPos(self, local):
		if player.IsEquipmentSlot(local) or player.IsCostumeSlot(local) or (app.ENABLE_NEW_EQUIPMENT_SYSTEM and player.IsBeltInventorySlot(local)):
			return local

		return self.inventoryPageIndex * player.INVENTORY_PAGE_SIZE + local
	
	def GetInventoryPageIndex(self):
		return self.inventoryPageIndex

	if app.WJ_ENABLE_TRADABLE_ICON:
		def RefreshMarkSlots(self, localIndex=None):
			if not self.interface:
				return

			onTopWnd = self.interface.GetOnTopWindow()
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

			for i in xrange(player.INVENTORY_PAGE_SIZE):
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

	def RefreshBagSlotWindow(self):
		getItemVNum=player.GetItemIndex
		getItemCount=player.GetItemCount
		setItemVNum=self.wndItem.SetItemSlot

		for i in xrange(player.INVENTORY_PAGE_SIZE):
			slotNumber = self.__InventoryLocalSlotPosToGlobalSlotPos(i)
			itemCount = getItemCount(slotNumber)
			# itemCount == 
			if 0 == itemCount:
				self.wndItem.ClearSlot(i)
				continue
			elif 1 == itemCount:
				itemCount = 0

			itemVnum = getItemVNum(slotNumber)
			setItemVNum(i, itemVnum, itemCount)

			if app.WJ_ENABLE_TRADABLE_ICON:
				self.RefreshMarkSlots(i)

			# COMPANION_ACTIVE_POS
			if player.GetItemTypeBySlot(slotNumber) == item.ITEM_TYPE_COMPANION:
				if constInfo.COMPANION_ACTIVE_POS == slotNumber:
					self.wndItem.ActivateSlot(i)
				else:
					self.wndItem.DeactivateSlot(i)
			# COMPANION_ACTIVE_POS

			if app.ENABLE_CHANGELOOK_SYSTEM:
				itemTransmutedVnum = player.GetItemTransmutation(slotNumber)
				if itemTransmutedVnum:
					self.wndItem.DisableCoverButton(i)
				else:
					self.wndItem.EnableCoverButton(i)

			if constInfo.IS_AUTO_POTION(itemVnum):
				metinSocket = [player.GetItemMetinSocket(slotNumber, j) for j in xrange(player.METIN_SOCKET_MAX_NUM)]

				isActivated = 0 != metinSocket[0]

				if isActivated:
					self.wndItem.ActivateSlot(i)
					potionType = 0;
					if constInfo.IS_AUTO_POTION_HP(itemVnum):
						potionType = player.AUTO_POTION_TYPE_HP
					elif constInfo.IS_AUTO_POTION_SP(itemVnum):
						potionType = player.AUTO_POTION_TYPE_SP

					usedAmount = int(metinSocket[1])
					totalAmount = int(metinSocket[2])
					player.SetAutoPotionInfo(potionType, isActivated, (totalAmount - usedAmount), totalAmount, self.__InventoryLocalSlotPosToGlobalSlotPos(i))

				else:
					self.wndItem.DeactivateSlot(i)

			if constInfo.IS_BLEND_ITEM(itemVnum):
				metinSocket = [player.GetItemMetinSocket(slotNumber, j) for j in xrange(player.METIN_SOCKET_MAX_NUM)]
				
				if slotNumber >= player.INVENTORY_PAGE_SIZE:
					slotNumber -= player.INVENTORY_PAGE_SIZE
			
				isActivated = 0 != (metinSocket[0] % 10)
				
				if isActivated:
					self.wndItem.ActivateSlot(i)
				else:
					self.wndItem.DeactivateSlot(i)

			if constInfo.IS_AUTO_POTION(itemVnum) == False and constInfo.IS_BLEND_ITEM(itemVnum) == False and constInfo.COMPANION_ACTIVE_POS != slotNumber:
				if not slotNumber in self.liHighlightedItems:
					if not slotNumber in self.listAttachedCl:
						if not slotNumber in self.listAttachedSashs:
							self.wndItem.DeactivateSlotInventory(i)
						if not slotNumber == constInfo.COMPANION_ACTIVE_POS:
							self.wndItem.DeactivateSlotInventory(i)
	
			if app.ENABLE_CHANGELOOK_SYSTEM:
				slotClNumberChecked = 0
			
				for q in xrange(changelook.WINDOW_MAX_MATERIALS):
					(isHere, iCell) = changelook.GetAttachedItem(q)
					if isHere:
						if iCell == slotNumber:
							self.wndItem.ActivateSlot(i, (238.00 / 255.0), (11.00 / 255.0), (11.00 / 255.0), 1.0)
							if not slotNumber in self.listAttachedCl:
								self.listAttachedCl.append(slotNumber)
							
							slotClNumberChecked = 1
					else:
						if slotNumber in self.listAttachedCl and not slotClNumberChecked:
							self.wndItem.DeactivateSlot(i)
							self.listAttachedCl.remove(slotNumber)							

			if app.ENABLE_SASH_SYSTEM:
				slotNumberChecked = 0
	
				for j in xrange(sash.WINDOW_MAX_MATERIALS):
					(isHere, iCell) = sash.GetAttachedItem(j)
					if isHere:
						if iCell == slotNumber:
							self.wndItem.ActivateSlot(i, (36.00 / 255.0), (222.00 / 255.0), (3.00 / 255.0), 1.0)
							if not slotNumber in self.listAttachedSashs:
								self.listAttachedSashs.append(slotNumber)
							
							slotNumberChecked = 1
					else:
						if slotNumber in self.listAttachedSashs and not slotNumberChecked:
							self.wndItem.DeactivateSlot(i)
							self.listAttachedSashs.remove(slotNumber)
			
		self.wndItem.RefreshSlot()
		self.__RefreshHighlights()

		if self.wndBelt:
			self.wndBelt.RefreshSlot()

		if app.WJ_ENABLE_TRADABLE_ICON:
			map(lambda wnd:wnd.RefreshLockedSlot(), self.bindWnds)

	def HighlightSlot(self, slot):
		if not slot in self.liHighlightedItems:
			self.liHighlightedItems.append(slot)

	def __RefreshHighlights(self):
		for i in xrange(player.INVENTORY_PAGE_SIZE):
			slotNumber = self.__InventoryLocalSlotPosToGlobalSlotPos(i)
			if slotNumber in self.liHighlightedItems:
				self.wndItem.ActivateSlotInventory(i)

	def RefreshEquipSlotWindow(self):
		getItemVNum=player.GetItemIndex
		getItemCount=player.GetItemCount
		job = player.GetJob()
		for i in xrange(player.EQUIPMENT_PAGE_COUNT+ 20):
			slotNumber = player.EQUIPMENT_SLOT_START + i
			itemCount = getItemCount(slotNumber)
			if itemCount <= 1:
				itemCount = 0

			self.wndEquip.SetItemSlot(slotNumber, getItemVNum(slotNumber), itemCount)

			if app.ENABLE_CHANGELOOK_SYSTEM:
				itemTransmutedVnum = player.GetItemTransmutation(slotNumber)

				if itemTransmutedVnum:
					self.wndEquip.DisableCoverButton(slotNumber)
				else:
					self.wndEquip.EnableCoverButton(slotNumber)
					
			if ENABLE_DEBUG_SLOTS == True:
				if getItemVNum(slotNumber):
					chat.AppendChat(1, "EQUIP-1: ItemVnum: %d, Slot: %d" % (getItemVNum(slotNumber), slotNumber))

		if app.ENABLE_NEW_EQUIPMENT_SYSTEM:
			for i in xrange(player.NEW_EQUIPMENT_SLOT_COUNT + 20):
				slotNumber = player.NEW_EQUIPMENT_SLOT_START + i
				itemCount = getItemCount(slotNumber)
				if itemCount <= 1:
					itemCount = 0

				self.wndEquip.SetItemSlot(slotNumber, getItemVNum(slotNumber), itemCount)

				if app.ENABLE_CHANGELOOK_SYSTEM:
					itemTransmutedVnum = player.GetItemTransmutation(slotNumber)

					if itemTransmutedVnum:
						self.wndEquip.DisableCoverButton(slotNumber)
					else:
						self.wndEquip.EnableCoverButton(slotNumber)
						
				if ENABLE_DEBUG_SLOTS == True:
					if getItemVNum(slotNumber):
						chat.AppendChat(1, "EQUIP-2: ItemVnum: %d, Slot: %d" % (getItemVNum(slotNumber), slotNumber))

		self.wndEquip.RefreshSlot()

		if self.wndCostume:
			self.wndCostume.RefreshCostumeSlot()

	def RefreshItemSlot(self):
		self.RefreshBagSlotWindow()
		self.RefreshEquipSlotWindow()

	def RefreshStatus(self):
		money = player.GetElk()
		if self.wndMoney:
			self.wndMoney.SetText(localeInfo.DottedNumber(money))

	def SetItemToolTip(self, tooltipItem):
		self.tooltipItem = tooltipItem

	def SellItem(self):
		if self.sellingSlotitemIndex == player.GetItemIndex(self.sellingSlotNumber):
			if self.sellingSlotitemCount == player.GetItemCount(self.sellingSlotNumber):
				net.SendShopSellPacketNew(self.sellingSlotNumber, self.questionDialog.count, player.INVENTORY)

		self.OnCloseQuestionDialog()

	def OnDetachMetinFromItem(self):
		if None == self.questionDialog:
			return

		self.__SendUseItemToItemPacket(self.questionDialog.sourcePos, self.questionDialog.targetPos)
		self.OnCloseQuestionDialog()

	def OnCloseQuestionDialog(self):
		if not self.questionDialog:
			return

		self.questionDialog.Close()
		self.questionDialog = None
		constInfo.SET_ITEM_QUESTION_DIALOG_STATUS(0)

	def OnCloseNewQuestionDialog(self):
		if not self.questionDialog:
			return

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
				
			elif app.ENABLE_SWITCHBOT_WORLDARD and player.SLOT_TYPE_SWITCHBOT == attachedSlotType:
				attachedCount = mouseModule.mouseController.GetAttachedItemCount()
				net.SendItemMovePacket(player.SWITCHBOT, attachedSlotPos, player.INVENTORY, selectedSlotPos, attachedCount)
				
			elif player.SLOT_TYPE_SHOP == attachedSlotType:
				if app.ENABLE_OFFLINE_SHOP and shop.IsOwner():
					net.SendShopWithdrawItemPacket(attachedSlotPos)
				else:
					net.SendShopBuyPacket(attachedSlotPos)

			elif player.SLOT_TYPE_SAFEBOX == attachedSlotType:

				if player.ITEM_MONEY == attachedItemIndex:
					net.SendSafeboxWithdrawMoneyPacket(mouseModule.mouseController.GetAttachedItemCount())

				else:
					net.SendSafeboxCheckoutPacket(attachedSlotPos, selectedSlotPos)

			elif player.SLOT_TYPE_MALL == attachedSlotType:
				net.SendMallCheckoutPacket(attachedSlotPos, selectedSlotPos)

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
					self.dlgPickMoney.SetTitleName(localeInfo.PICK_ITEM_TITLE)
					self.dlgPickMoney.SetAcceptEvent(ui.__mem_func__(self.OnPickItem))
					self.dlgPickMoney.Open(itemCount)
					self.dlgPickMoney.itemGlobalSlotIndex = itemSlotIndex

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
		
		if app.ENABLE_SEALBIND_SYSTEM and item.IsSealScroll(srcItemVID):
			self.__SendUseItemToItemPacket(srcItemSlotPos, dstItemSlotPos)

		elif item.IsRefineScroll(srcItemVID) and srcItemVID == vnumDest: # Grimm BugFix stack items same VNUM
			self.__SendMoveItemPacket(srcItemSlotPos, dstItemSlotPos, 0)
			return

		elif item.IsRefineScroll(srcItemVID):
			self.RefineItem(srcItemSlotPos, dstItemSlotPos)
			self.wndItem.SetUseMode(False)

		elif item.IsMetin(srcItemVID):
			self.AttachMetinToItem(srcItemSlotPos, dstItemSlotPos)

		elif item.IsDetachScroll(srcItemVID):
			self.DetachMetinFromItem(srcItemSlotPos, dstItemSlotPos)

		elif item.IsKey(srcItemVID):
			self.__SendUseItemToItemPacket(srcItemSlotPos, dstItemSlotPos)

		elif (player.GetItemFlags(srcItemSlotPos) & ITEM_FLAG_APPLICABLE) == ITEM_FLAG_APPLICABLE:
			self.__SendUseItemToItemPacket(srcItemSlotPos, dstItemSlotPos)

		elif item.GetUseType(srcItemVID) in self.USE_TYPE_TUPLE:
			self.__SendUseItemToItemPacket(srcItemSlotPos, dstItemSlotPos)
		
		# NEW_COSTUME_BONUS
		elif item.GetItemSubType() == item.USE_ADD_ATTRIBUTE_COSTUME or item.GetItemSubType() == item.USE_CHANGE_ATTRIBUTE_COSTUME:
			self.__SendUseItemToItemPacket(srcItemSlotPos, dstItemSlotPos)
		elif item.GetItemSubType() == item.USE_ADD_PENDANT_ATTRIBUTE or item.GetItemSubType() == item.USE_ADD_PENDANT_FIVE_ATTRIBUTE or item.GetItemSubType() == item.USE_CHANGE_PENDANT_ATTRIBUTE:
			self.__SendUseItemToItemPacket(srcItemSlotPos, dstItemSlotPos)
		else:
			item.SelectItem(srcItemVID)
			if item.GetItemType() == item.ITEM_TYPE_BLEND:
				item.SelectItem(player.GetItemIndex(dstItemSlotPos))
				if item.GetItemType() == item.ITEM_TYPE_BLEND:
					self.__SendUseItemToItemPacket(srcItemSlotPos, dstItemSlotPos)
					return
			
			if srcItemVID == 30187 and player.GetItemTypeBySlot(dstItemSlotPos) == item.ITEM_TYPE_COMPANION:
				self.__SendUseItemToItemPacket(srcItemSlotPos, dstItemSlotPos)
				return
			if player.IsEquipmentSlot(dstItemSlotPos):
				if item.IsEquipmentVID(srcItemVID):
					self.__UseItem(srcItemSlotPos)
			else:
				self.__SendMoveItemPacket(srcItemSlotPos, dstItemSlotPos, 0)

	def __SellItem(self, itemSlotPos):
		if not player.IsEquipmentSlot(itemSlotPos):
			self.sellingSlotNumber = itemSlotPos
			itemIndex = player.GetItemIndex(itemSlotPos)
			itemCount = player.GetItemCount(itemSlotPos)


			self.sellingSlotitemIndex = itemIndex
			self.sellingSlotitemCount = itemCount

			item.SelectItem(itemIndex)
			if item.IsAntiFlag(item.ANTIFLAG_SELL):
				popup = uiCommon.PopupDialog()
				popup.SetText(localeInfo.SHOP_CANNOT_SELL_ITEM)
				popup.SetAcceptEvent(self.__OnClosePopupDialog)
				popup.Open()
				self.popup = popup
				return

			itemPrice = item.GetISellItemPrice()

			if item.Is1GoldItem():
				itemPrice = itemCount / itemPrice / 5
			else:
				itemPrice = itemPrice * itemCount / 5

			item.GetItemName(itemIndex)
			itemName = item.GetItemName()

			self.questionDialog = uiCommon.QuestionDialog()
			self.questionDialog.SetText(localeInfo.DO_YOU_SELL_ITEM(itemName, itemCount, itemPrice))
			self.questionDialog.SetAcceptEvent(ui.__mem_func__(self.SellItem))
			self.questionDialog.SetCancelEvent(ui.__mem_func__(self.OnCloseQuestionDialog))
			self.questionDialog.Open()
			self.questionDialog.count = itemCount

			constInfo.SET_ITEM_QUESTION_DIALOG_STATUS(1)

	def __OnClosePopupDialog(self):
		self.pop = None

	def RefineItem(self, scrollSlotPos, targetSlotPos):
		scrollIndex = player.GetItemIndex(scrollSlotPos)
		targetIndex = player.GetItemIndex(targetSlotPos)

		if player.REFINE_OK != player.CanRefine(scrollIndex, targetSlotPos):
			return

		constInfo.AUTO_REFINE_TYPE = 1
		constInfo.AUTO_REFINE_DATA["ITEM"][0] = scrollSlotPos
		constInfo.AUTO_REFINE_DATA["ITEM"][1] = targetSlotPos

		self.__SendUseItemToItemPacket(scrollSlotPos, targetSlotPos)
		return

		result = player.CanRefine(scrollIndex, targetSlotPos)

		if player.REFINE_ALREADY_MAX_SOCKET_COUNT == result:
			chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.REFINE_FAILURE_NO_MORE_SOCKET)
		elif player.REFINE_NEED_MORE_GOOD_SCROLL == result:
			chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.REFINE_FAILURE_NEED_BETTER_SCROLL)
		elif player.REFINE_CANT_MAKE_SOCKET_ITEM == result:
			chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.REFINE_FAILURE_SOCKET_DISABLE_ITEM)
		elif player.REFINE_NOT_NEXT_GRADE_ITEM == result:
			chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.REFINE_FAILURE_UPGRADE_DISABLE_ITEM)
		elif player.REFINE_CANT_REFINE_METIN_TO_EQUIPMENT == result:
			chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.REFINE_FAILURE_EQUIP_ITEM)

		if player.REFINE_OK != result:
			return

		self.refineDialog.Open(scrollSlotPos, targetSlotPos)

	def DetachMetinFromItem(self, scrollSlotPos, targetSlotPos):
		scrollIndex = player.GetItemIndex(scrollSlotPos)
		targetIndex = player.GetItemIndex(targetSlotPos)
		
		if app.ENABLE_SASH_SYSTEM:
			if not player.CanDetach(scrollIndex, targetSlotPos):
				item.SelectItem(scrollIndex)
				if item.GetValue(0) == sash.CLEAN_ATTR_VALUE0:
					chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.SASH_FAILURE_CLEAN)
				else:
					chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.REFINE_FAILURE_METIN_INSEPARABLE_ITEM)
				
				return
		else:
			if not player.CanDetach(scrollIndex, targetSlotPos):
				chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.REFINE_FAILURE_METIN_INSEPARABLE_ITEM)
				return
		
		if app.ENABLE_CHANGELOOK_SYSTEM:
			if not player.CanDetach(scrollIndex, targetSlotPos):
				item.SelectItem(scrollIndex)
				if item.GetValue(0) == changelook.CLEAN_ATTR_VALUE0:
					chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.CHANGE_LOOK_FAILURE_CLEAN)
				else:
					chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.REFINE_FAILURE_METIN_INSEPARABLE_ITEM)
				
				return
		else:
			if not player.CanDetach(scrollIndex, targetSlotPos):
				chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.REFINE_FAILURE_METIN_INSEPARABLE_ITEM)
				return
		
		self.questionDialog = uiCommon.QuestionDialog()
		self.questionDialog.SetText(localeInfo.REFINE_DO_YOU_SEPARATE_METIN)
		
		if app.ENABLE_CHANGELOOK_SYSTEM:
			item.SelectItem(targetIndex)
			if item.GetItemType() == item.ITEM_TYPE_WEAPON or item.GetItemType() == item.ITEM_TYPE_ARMOR or item.GetItemType() == item.ITEM_TYPE_COSTUME:
				item.SelectItem(scrollIndex)
				if item.GetValue(0) == changelook.CLEAN_ATTR_VALUE0:
					self.questionDialog.SetText(localeInfo.CHANGE_LOOK_DO_YOU_CLEAN)

		if app.ENABLE_SASH_SYSTEM:
			item.SelectItem(targetIndex)
			if item.GetItemType() == item.ITEM_TYPE_COSTUME and item.GetItemSubType() == item.COSTUME_TYPE_SASH:
				item.SelectItem(scrollIndex)
				if item.GetValue(0) == sash.CLEAN_ATTR_VALUE0:
					self.questionDialog.SetText(localeInfo.SASH_DO_YOU_CLEAN)
		
		self.questionDialog.SetAcceptEvent(ui.__mem_func__(self.OnDetachMetinFromItem))
		self.questionDialog.SetCancelEvent(ui.__mem_func__(self.OnCloseQuestionDialog))
		self.questionDialog.Open()
		self.questionDialog.sourcePos = scrollSlotPos
		self.questionDialog.targetPos = targetSlotPos

	def AttachMetinToItem(self, metinSlotPos, targetSlotPos):
		metinIndex = player.GetItemIndex(metinSlotPos)
		targetIndex = player.GetItemIndex(targetSlotPos)

		item.SelectItem(metinIndex)
		itemName = item.GetItemName()

		result = player.CanAttachMetin(metinIndex, targetSlotPos)

		if player.ATTACH_METIN_NOT_MATCHABLE_ITEM == result:
			chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.REFINE_FAILURE_CAN_NOT_ATTACH(itemName))

		if player.ATTACH_METIN_NO_MATCHABLE_SOCKET == result:
			chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.REFINE_FAILURE_NO_SOCKET(itemName))

		elif player.ATTACH_METIN_NOT_EXIST_GOLD_SOCKET == result:
			chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.REFINE_FAILURE_NO_GOLD_SOCKET(itemName))

		elif player.ATTACH_METIN_CANT_ATTACH_TO_EQUIPMENT == result:
			chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.REFINE_FAILURE_EQUIP_ITEM)

		if player.ATTACH_METIN_OK != result:
			return

		self.attachMetinDialog.Open(metinSlotPos, targetSlotPos)

	def OverOutItem(self):
		self.wndItem.SetUsableItem(False)
		if None != self.tooltipItem:
			self.tooltipItem.HideToolTip()

	def OverInItem(self, overSlotPos):
		Index = overSlotPos

		overSlotPos = self.__InventoryLocalSlotPosToGlobalSlotPos(overSlotPos)	
			
		self.wndItem.SetUsableItem(False)

		if overSlotPos in self.liHighlightedItems:
			self.liHighlightedItems.remove(overSlotPos)
			self.wndItem.DeactivateSlotInventory(Index)

		if mouseModule.mouseController.isAttached():
			attachedItemType = mouseModule.mouseController.GetAttachedType()
			if player.SLOT_TYPE_INVENTORY == attachedItemType:

				attachedSlotPos = mouseModule.mouseController.GetAttachedSlotNumber()
				attachedItemVNum = mouseModule.mouseController.GetAttachedItemIndex()

				if self.__CanUseSrcItemToDstItem(attachedItemVNum, attachedSlotPos, overSlotPos):
					self.wndItem.SetUsableItem(True)
					self.wndItem.SetUseMode(True)
					self.ShowToolTip(overSlotPos)
					return

		self.ShowToolTip(overSlotPos)


	def __IsUsableItemToItem(self, srcItemVNum, srcSlotPos):
		if item.IsRefineScroll(srcItemVNum):
			return True
		elif item.IsMetin(srcItemVNum):
			return True
		elif item.IsDetachScroll(srcItemVNum):
			return True
		elif item.IsKey(srcItemVNum):
			return True
		elif (player.GetItemFlags(srcSlotPos) & ITEM_FLAG_APPLICABLE) == ITEM_FLAG_APPLICABLE:
			return True
		else:
			if item.GetUseType(srcItemVNum) in self.USE_TYPE_TUPLE:
				return True
			
			# NEW_COSTUME_BONUS
			item.SelectItem(srcItemVNum)
			if item.GetItemSubType() == item.USE_ADD_ATTRIBUTE_COSTUME or item.GetItemSubType() == item.USE_CHANGE_ATTRIBUTE_COSTUME:
				return True

			if item.GetItemSubType() == item.USE_ADD_PENDANT_ATTRIBUTE or item.GetItemSubType() == item.USE_ADD_PENDANT_FIVE_ATTRIBUTE  or item.GetItemSubType() == item.USE_CHANGE_PENDANT_ATTRIBUTE:
				return True

		return False

	def __CanUseSrcItemToDstItem(self, srcItemVNum, srcSlotPos, dstSlotPos):
		if srcSlotPos == dstSlotPos:
			return False
		
		item.SelectItem(srcItemVNum)
		
		if item.IsRefineScroll(srcItemVNum):
			if player.REFINE_OK == player.CanRefine(srcItemVNum, dstSlotPos):
				return True
		elif item.IsMetin(srcItemVNum):
			if player.ATTACH_METIN_OK == player.CanAttachMetin(srcItemVNum, dstSlotPos):
				return True
		elif item.IsDetachScroll(srcItemVNum):
			if player.DETACH_METIN_OK == player.CanDetach(srcItemVNum, dstSlotPos):
				return True
		elif item.IsKey(srcItemVNum):
			if player.CanUnlock(srcItemVNum, dstSlotPos):
				return True

		elif (player.GetItemFlags(srcSlotPos) & ITEM_FLAG_APPLICABLE) == ITEM_FLAG_APPLICABLE:
			return True

		# BLEND
		elif item.GetItemType() == item.ITEM_TYPE_BLEND:
			item.SelectItem(player.GetItemIndex(dstSlotPos))
			if item.GetItemType() == item.ITEM_TYPE_BLEND:
				return True

		else:
			useType=item.GetUseType(srcItemVNum)

			if "USE_CLEAN_SOCKET" == useType:
				if self.__CanCleanBrokenMetinStone(dstSlotPos):
					return True
			elif "USE_CHANGE_ATTRIBUTE" == useType:
				if self.__CanChangeItemAttrList(dstSlotPos):
					return True
			elif "USE_ADD_ATTRIBUTE" == useType:
				if self.__CanAddItemAttr(dstSlotPos):
					return True
			elif "USE_ADD_ATTRIBUTE2" == useType:
				if self.__CanAddItemAttr(dstSlotPos):
					return True
			elif "USE_ADD_ACCESSORY_SOCKET" == useType:
				if self.__CanAddAccessorySocket(dstSlotPos):
					return True
			elif "USE_PUT_INTO_ACCESSORY_SOCKET" == useType:
				if self.__CanPutAccessorySocket(dstSlotPos, srcItemVNum):
					return True
			elif "USE_PUT_INTO_BELT_SOCKET" == useType:
				dstItemVNum = player.GetItemIndex(dstSlotPos)
				print "USE_PUT_INTO_BELT_SOCKET", srcItemVNum, dstItemVNum

				item.SelectItem(dstItemVNum)

				if item.ITEM_TYPE_BELT == item.GetItemType():
					return True
			#NEW_COSTUME_BONUS
			elif item.GetItemSubType() == item.USE_ADD_ATTRIBUTE_COSTUME or item.GetItemSubType() == item.USE_CHANGE_ATTRIBUTE_COSTUME:
				bForSubType = item.GetValue(0)
				if self.__CanAddItemAttrCostume(bForSubType, dstSlotPos):
					return True

			elif item.GetItemSubType() == item.USE_ADD_PENDANT_ATTRIBUTE or item.GetItemSubType() == item.USE_ADD_PENDANT_FIVE_ATTRIBUTE  or item.GetItemSubType() == item.USE_CHANGE_PENDANT_ATTRIBUTE:
				if self.__CanAddItemAttrTalisman(dstSlotPos):
					return True

		return False

	def __CanCleanBrokenMetinStone(self, dstSlotPos):
		dstItemVNum = player.GetItemIndex(dstSlotPos)
		if dstItemVNum == 0:
			return False

		item.SelectItem(dstItemVNum)

		if item.ITEM_TYPE_WEAPON != item.GetItemType():
			return False

		for i in xrange(player.METIN_SOCKET_MAX_NUM):
			if player.GetItemMetinSocket(dstSlotPos, i) == constInfo.ERROR_METIN_STONE:
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

	def __CanPutAccessorySocket(self, dstSlotPos, mtrlVnum):
		dstItemVNum = player.GetItemIndex(dstSlotPos)
		if dstItemVNum == 0:
			return False

		item.SelectItem(dstItemVNum)

		if item.GetItemType() != item.ITEM_TYPE_ARMOR:
			return False

		if not item.GetItemSubType() in (item.ARMOR_WRIST, item.ARMOR_NECK, item.ARMOR_EAR):
			return False

		curCount = player.GetItemMetinSocket(dstSlotPos, 0)
		maxCount = player.GetItemMetinSocket(dstSlotPos, 1)

		if mtrlVnum != constInfo.GET_ACCESSORY_MATERIAL_VNUM(dstItemVNum, item.GetItemSubType()):
			return False

		if curCount>=maxCount:
			return False

		return True

	def __CanAddAccessorySocket(self, dstSlotPos):
		dstItemVNum = player.GetItemIndex(dstSlotPos)
		if dstItemVNum == 0:
			return False

		item.SelectItem(dstItemVNum)

		if item.GetItemType() != item.ITEM_TYPE_ARMOR:
			return False

		if not item.GetItemSubType() in (item.ARMOR_WRIST, item.ARMOR_NECK, item.ARMOR_EAR):
			return False

		curCount = player.GetItemMetinSocket(dstSlotPos, 0)
		maxCount = player.GetItemMetinSocket(dstSlotPos, 1)

		ACCESSORY_SOCKET_MAX_SIZE = 3
		if maxCount >= ACCESSORY_SOCKET_MAX_SIZE:
			return False

		return True

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

	def __CanAddItemAttrCostume(self, SubType, dstSlotPos):
		dstItemVNum = player.GetItemIndex(dstSlotPos)
		if dstItemVNum == 0:
			return False

		item.SelectItem(dstItemVNum)

		if not item.GetItemType() == item.ITEM_TYPE_COSTUME:
			return False
			
		# if not item.GetItemSubType() == SubType:
			# return False

		return True

	def __CanAddItemAttrTalisman(self, dstSlotPos):
		dstItemVNum = player.GetItemIndex(dstSlotPos)
		if dstItemVNum == 0:
			return False

		item.SelectItem(dstItemVNum)

		if not item.GetItemType() == item.ITEM_TYPE_ARMOR:
			return False

		if not item.GetItemSubType() == item.ARMOR_PENDANT:
			return False

		return True

	def ShowToolTip(self, slotIndex):
		if None != self.tooltipItem:
			self.tooltipItem.SetInventoryItem(slotIndex, player.INVENTORY, self.interface, True)
			
			itemVnum = player.GetItemIndex(player.INVENTORY, slotIndex)
			if app.IsPressed(app.DIK_LALT) and itemVnum > 0:
				item.SelectItem(itemVnum)
				if self.interface.dlgChestDrop and item.GetItemType() == 23 or itemVnum in [ 50011, 50012 ]:
					if not self.interface.dlgChestDrop.IsShow():
						self.interface.dlgChestDrop.Open(slotIndex)
						net.SendChestDropInfo(slotIndex)
						
	def OnTop(self):
		if None != self.tooltipItem:
			self.tooltipItem.SetTop()

		if app.WJ_ENABLE_TRADABLE_ICON:
			map(lambda wnd:wnd.RefreshLockedSlot(), self.bindWnds)
			self.RefreshMarkSlots()

	def OnPressEscapeKey(self):
		self.Close()
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

		slotPos = slotIndex
		slotIndex = self.__InventoryLocalSlotPosToGlobalSlotPos(slotIndex)

		if self.wndDragonSoulRefine.IsShow():
			self.wndDragonSoulRefine.AutoSetItem((player.INVENTORY, slotIndex), 1)
			return

		if app.ENABLE_CHANGELOOK_SYSTEM:
			if self.isShowChangeLookWindow():
				changelook.Add(player.INVENTORY, slotIndex, 255)
				return

		if app.ENABLE_SASH_SYSTEM:
			if self.isShowSashWindow():
				sash.Add(player.INVENTORY, slotIndex, 255)
				return
		
		ItemVnum = player.GetItemIndex(slotIndex)
		
		# if app.IsPressed(app.DIK_LSHIFT):
			# if shop.IsOpen():
				# if not shop.IsPrivateShop():
					# net.SendShopSellPacketNew(slotIndex, player.GetItemCount(slotIndex), player.INVENTORY)
				
		ExceptArray = []
		if app.IsPressed(app.DIK_LCONTROL) and constInfo.IsItemMovable(ItemVnum):
			# chat.AppendChat(1, "TEST ITEMMOVE")
			item.SelectItem(player.GetItemIndex(slotIndex))
			_, ItemSizeMovable = item.GetItemSize()

			xStart = 0
			xEnd = 0
			
			if constInfo.IsItemBook(ItemVnum):
				xStart = player.INVENTORY_BOOK_START
				xEnd = player.INVENTORY_BOOK_END
			elif constInfo.IsItemStone(ItemVnum):
				xStart = player.INVENTORY_STONE_START
				xEnd = player.INVENTORY_STONE_END
			elif constInfo.IsItemUpgrade(ItemVnum):
				xStart = player.INVENTORY_UPGRADE_START
				xEnd = player.INVENTORY_UPGRADE_END
			elif constInfo.IsItemChest(ItemVnum):
				xStart = player.INVENTORY_CHEST_START
				xEnd = player.INVENTORY_CHEST_END

			if xStart > 0 or xEnd > 0:
				for xCell in xrange(xStart, xEnd):
					if player.GetItemIndex(xCell) > 0:
						item.SelectItem(player.GetItemIndex(xCell))
						_, ItemSize = item.GetItemSize()
						
						for size in xrange(ItemSize):
							xPos = xCell + (size * 5)
							ExceptArray.append(xPos)

					if player.GetItemIndex(xCell) == 0:		
						bCanPass = True
						for size in xrange(ItemSizeMovable):
							if player.GetItemIndex(xCell + (size * 5)) != 0:
								bCanPass = False

						if xCell in ExceptArray or not bCanPass:
							continue
						
						self.__SendMoveItemPacket(slotIndex, xCell, player.GetItemCount(slotIndex))
						break
		else:
			self.__UseItem(slotIndex)

		mouseModule.mouseController.DeattachObject()
		self.OverOutItem()
	
	# def MoveToSafeBox(self, slotIndex):
		# ExceptArray = []

		# ItemVnum = player.GetItemIndex(slotIndex)
		# item.SelectItem(ItemVnum)
		# _, ItemSizeMovable = item.GetItemSize()

		# for x in xrange(safebox.SAFEBOX_PAGE_SIZE):
			# if safebox.GetItemID(x) != 0:
				# item.SelectItem(safebox.GetItemID(x))
				# _, ItemSize = item.GetItemSize()
				
				# for size in xrange(ItemSize):
					# xPos = x + (size * 5)
					# ExceptArray.append(xPos)

			# if safebox.GetItemID(x) == 0:		
				# bCanPass = True
				# for size in xrange(ItemSizeMovable):
					# if safebox.GetItemID(x + (size * 5)) != 0:
						# bCanPass = False

				# if x in ExceptArray or not bCanPass:
					# continue
				
				# net.SendSafeboxCheckinPacket(player.INVENTORY, slotIndex, x)
				# break
	
	if constInfo.FAST_INTERACTION_SAFEBOX == True:
		def __GetCurrentItemGrid(self):
			itemGrid = [[False for slot in xrange(player.INVENTORY_PAGE_SIZE)] for page in xrange(player.INVENTORY_PAGE_COUNT)]

			for page in xrange(player.INVENTORY_PAGE_COUNT):
				for slot in xrange(player.INVENTORY_PAGE_SIZE):
					itemVnum = player.GetItemIndex(slot + page * player.INVENTORY_PAGE_SIZE)
					if itemVnum <> 0:
						(w, h) = item.GetItemSize(item.SelectItem(itemVnum))
						for i in xrange(h):
							itemGrid[page][slot + i * 5] = True

			return itemGrid

		def __FindEmptyCellForSize(self, itemGrid, size):
			for page in xrange(player.INVENTORY_PAGE_COUNT):
				for slot in xrange(player.INVENTORY_PAGE_SIZE):
					if itemGrid[page][slot] == False:
						possible = True
						for i in xrange(size):
							p = slot + (i * 5)

							try:
								if itemGrid[page][p] == True:
									possible = False
									break
							except IndexError:
								possible = False
								break

						if possible:
							return slot + page * player.INVENTORY_PAGE_SIZE

			return -1

		def AttachItemFromSafebox(self, slotIndex, itemIndex):
			itemGrid = self.__GetCurrentItemGrid()

			if item.GetItemType(item.SelectItem(itemIndex)) == item.ITEM_TYPE_DS:
				return

			emptySlotIndex = self.__FindEmptyCellForSize(itemGrid, item.GetItemSize()[1])
			if emptySlotIndex <> -1:
				net.SendSafeboxCheckoutPacket(slotIndex, player.INVENTORY, emptySlotIndex)

			return True
	
	def __UseItem(self, slotIndex):
		ItemVNum = player.GetItemIndex(slotIndex)
		item.SelectItem(ItemVNum)
        
		if constInfo.FAST_INTERACTION_DELETE == True:
			if app.IsPressed(app.DIK_DELETE):
				if player.IsEquipmentSlot(slotIndex):
					chat.AppendChat(chat.CHAT_TYPE_INFO, "[!] Nu poti sterge obiectele echipate!")
					return

				net.SendItemDestroyPacket(slotIndex)
				return
				
		if app.ENABLE_PREMIUM_SYSTEM_EXTRA:
			index = player.GetItemIndex(slotIndex)
			if index >= 30526 and index <= 30529:
				self.premium = uiPremium.PremiumSelectAttribute()
				self.premium.Open(slotIndex, index - 30526)
				# chat.AppendChat(1, "OPEN PREMIUM :D")
				return
				
		if app.ENABLE_SELL_ITEM:
			if app.IsPressed(app.DIK_LALT) and app.IsPressed(app.DIK_LSHIFT) and constInfo.IsSellItems(ItemVNum):
				self.__SendSellItemPacket(slotIndex)
				return
				
		if constInfo.FAST_INTERACTION_SAFEBOX == True:
			if app.IsPressed(app.DIK_LCONTROL) and self.interface.AttachInvenItemToOtherWindowSlot(player.INVENTORY, slotIndex):
				return
					
		if player.GetItemTypeBySlot(slotIndex) == item.ITEM_TYPE_COMPANION and player.GetItemMetinSocket(player.INVENTORY, slotIndex, 0) == 0:
			self.questionDialog = uiCommon.CompanionCreate(slotIndex)
			self.questionDialog.SetCancelEvent(ui.__mem_func__(self.OnCloseNewQuestionDialog))
			self.questionDialog.Show()
			constInfo.SET_ITEM_QUESTION_DIALOG_STATUS(1)
							
		elif app.ENABLE_COSTUME_SYSTEM and app.IsPressed(app.DIK_LSHIFT): #ENABLE_RENDER_TARGET_SYSTEM
			itemTransmutedVnum = player.GetItemTransmutation(slotIndex)
			if itemTransmutedVnum:
				self.tooltipItem.ModelPreviewFull(itemTransmutedVnum)
			else:
				self.tooltipItem.ModelPreviewFull(ItemVNum)
		else:
			if app.ENABLE_COSTUME_SYSTEM: #ENABLE_RENDER_TARGET_SYSTEM
				wndTargetRender = renderTargetExtension.RenderTarget.Get()
				if wndTargetRender.IsShow():
					wndTargetRender.DisplayUser(player.GetRace(), True)
			self.__SendUseItemPacket(slotIndex)

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
			
	def SetDragonSoulRefineWindow(self, wndDragonSoulRefine):
		self.wndDragonSoulRefine = wndDragonSoulRefine

	if app.ENABLE_CHANGELOOK_SYSTEM:
		def SetChangeLookWindow(self, wndChangeLook):
			self.wndChangeLook = wndChangeLook

		def isShowChangeLookWindow(self):
			if self.wndChangeLook:
				if self.wndChangeLook.IsShow():
					return 1
			
			return 0

	if app.ENABLE_SASH_SYSTEM:
		def SetSashWindow(self, wndSashCombine, wndSashAbsorption):
			self.wndSashCombine = wndSashCombine
			self.wndSashAbsorption = wndSashAbsorption

		def isShowSashWindow(self):
			if self.wndSashCombine:
				if self.wndSashCombine.IsShow():
					return 1

			if self.wndSashAbsorption:
				if self.wndSashAbsorption.IsShow():
					return 1
			
			return 0
		
	def OnMoveWindow(self, x, y):
		if self.wndBelt:
			self.wndBelt.AdjustPositionAndSize()
