import app
import net
import player
import item
import ui
import uiToolTip
import mouseModule
import localeInfo
import uiCommon
import constInfo
import wndMgr
import chat
import uiScriptLocale
import cfg

# REFINE_VNUM = [
	# player.REFINE_VNUM_POTION_LOW,
	# player.REFINE_VNUM_POTION_MEDIUM,
	# player.REFINE_VNUM_POTION_EXTRA
# ]

# REFINE_PERCENTAGE = [
	# player.REFINE_PERCENTAGE_LOW,
	# player.REFINE_PERCENTAGE_MEDIUM,
	# player.REFINE_PERCENTAGE_EXTRA
# ]

# REFINE_MODE = {
	# 0 : 0,
	# 1 : 0,
	# 2 : 0
# }

REFINE_TOTAL_PERCENTAGE = {
	"update" : 0
}

# def IS_UPGRADE_ITEM(itemVnum):
	# for i in xrange(3):
		# if itemVnum == REFINE_VNUM[i]:
			# return TRUE
	# return FALSE

class RefineDialog(ui.ScriptWindow):

	makeSocketSuccessPercentage = ( 100, 33, 20, 15, 10, 5, 0 )
	upgradeStoneSuccessPercentage = ( 30, 29, 28, 27, 26, 25, 24, 23, 22 )
	upgradeArmorSuccessPercentage = ( 99, 66, 33, 33, 33, 33, 33, 33, 33 )
	upgradeAccessorySuccessPercentage = ( 99, 88, 77, 66, 33, 33, 33, 33, 33 )
	upgradeSuccessPercentage = ( 99, 66, 33, 33, 33, 33, 33, 33, 33 )

	def __init__(self):
		ui.ScriptWindow.__init__(self)
		self.__LoadScript()

		self.scrollItemPos = 0
		self.targetItemPos = 0

	def __LoadScript(self):

		self.__LoadQuestionDialog()

		try:
			pyScrLoader = ui.PythonScriptLoader()
			pyScrLoader.LoadScriptFile(self, "uiscript/refinedialog.py")

		except:
			import exception
			exception.Abort("RefineDialog.__LoadScript.LoadObject")

		try:
			self.board = self.GetChild("Board")
			self.titleBar = self.GetChild("TitleBar")
			self.successPercentage = self.GetChild("SuccessPercentage")
			self.GetChild("AcceptButton").SetEvent(self.OpenQuestionDialog)
			self.GetChild("CancelButton").SetEvent(self.Close)
		except:
			import exception
			exception.Abort("RefineDialog.__LoadScript.BindObject")

		if constInfo.ENABLE_REFINE_PCT:
			self.successPercentage.Show()
		else:
			self.successPercentage.Hide()

		toolTip = uiToolTip.ItemToolTip()
		toolTip.SetParent(self)
		toolTip.SetPosition(15, 38)
		toolTip.SetFollow(FALSE)
		toolTip.Show()
		self.toolTip = toolTip

		self.titleBar.SetCloseEvent(ui.__mem_func__(self.Close))

	def __del__(self):
		ui.ScriptWindow.__del__(self)

	def __LoadQuestionDialog(self):
		self.dlgQuestion = ui.ScriptWindow()

		try:
			pyScrLoader = ui.PythonScriptLoader()
			pyScrLoader.LoadScriptFile(self.dlgQuestion, "uiscript/questiondialog2.py")
		except:
			import exception
			exception.Abort("RefineDialog.__LoadQuestionDialog.LoadScript")

		try:
			GetObject=self.dlgQuestion.GetChild
			GetObject("message1").SetText(localeInfo.REFINE_DESTROY_WARNING)
			GetObject("message2").SetText(localeInfo.REFINE_WARNING2)
			GetObject("accept").SetEvent(ui.__mem_func__(self.Accept))
			GetObject("cancel").SetEvent(ui.__mem_func__(self.dlgQuestion.Hide))
		except:
			import exception
			exception.Abort("SelectCharacterWindow.__LoadQuestionDialog.BindObject")

	def Destroy(self):
		self.ClearDictionary()
		self.board = 0
		self.successPercentage = 0
		self.titleBar = 0
		self.toolTip = 0
		self.dlgQuestion = 0

	def GetRefineSuccessPercentage(self, scrollSlotIndex, itemSlotIndex):

		if -1 != scrollSlotIndex:
			if player.IsRefineGradeScroll(scrollSlotIndex):
				curGrade = player.GetItemGrade(itemSlotIndex)
				itemIndex = player.GetItemIndex(itemSlotIndex)

				item.SelectItem(itemIndex)
				itemType = item.GetItemType()
				itemSubType = item.GetItemSubType()

				if item.ITEM_TYPE_METIN == itemType:

					if curGrade >= len(self.upgradeStoneSuccessPercentage):
						return 0
					return self.upgradeStoneSuccessPercentage[curGrade]

				elif item.ITEM_TYPE_ARMOR == itemType:

					if item.ARMOR_BODY == itemSubType:
						if curGrade >= len(self.upgradeArmorSuccessPercentage):
							return 0
						return self.upgradeArmorSuccessPercentage[curGrade]
					else:
						if curGrade >= len(self.upgradeAccessorySuccessPercentage):
							return 0
						return self.upgradeAccessorySuccessPercentage[curGrade]

				else:

					if curGrade >= len(self.upgradeSuccessPercentage):
						return 0
					return self.upgradeSuccessPercentage[curGrade]

		for i in xrange(player.METIN_SOCKET_MAX_NUM+1):
			if 0 == player.GetItemMetinSocket(itemSlotIndex, i):
				break

		return self.makeSocketSuccessPercentage[i]

	def Open(self, scrollItemPos, targetItemPos):
		self.scrollItemPos = scrollItemPos
		self.targetItemPos = targetItemPos

		percentage = self.GetRefineSuccessPercentage(scrollItemPos, targetItemPos)
		if 0 == percentage:
			return
		self.successPercentage.SetText(localeInfo.REFINE_SUCCESS_PROBALITY % (percentage))

		itemIndex = player.GetItemIndex(targetItemPos)


		self.toolTip.ClearToolTip()

		if app.WJ_ENABLE_TRADABLE_ICON:
			self.SetCantMouseEventSlot(targetItemPos)
			
		metinSlot = []
		for i in xrange(player.METIN_SOCKET_MAX_NUM):
			metinSlot.append(player.GetItemMetinSocket(targetItemPos, i))
		self.toolTip.AddItemData(itemIndex, metinSlot)

		self.UpdateDialog()
		self.SetTop()
		self.Show()

	def UpdateDialog(self):
		newWidth = self.toolTip.GetWidth() + 30
		newHeight = self.toolTip.GetHeight() + 98
		# self.board.SetSize(newWidth, newHeight)
		# self.titleBar.SetWidth(newWidth-15)
		self.SetSize(newWidth, newHeight)

		(x, y) = self.GetLocalPosition()
		self.SetPosition(x, y)

	def OpenQuestionDialog(self):
		percentage = self.GetRefineSuccessPercentage(-1, self.targetItemPos)
		if 100 == percentage:
			self.Accept()
			return

		self.dlgQuestion.SetTop()
		self.dlgQuestion.Show()

	def Accept(self):
		net.SendItemUseToItemPacket(self.scrollItemPos, self.targetItemPos)

	def Close(self):
		if self.dlgQuestion:
			self.dlgQuestion.Close()

		self.dlgQuestion = None
		self.Hide()
				
	def OnPressEscapeKey(self):
		self.Close()
		return TRUE

class RefineDialogNew(ui.ScriptWindow):
	def __init__(self):
		ui.ScriptWindow.__init__(self)
		self.__Initialize()
		self.isLoaded = FALSE
		if app.WJ_ENABLE_TRADABLE_ICON:
			self.wndInventory = None

	def __Initialize(self):
		self.dlgQuestion = None
		self.children = []
		self.vnum = 0
		self.targetItemPos = 0
		self.dialogHeight = 0
		self.percentage = 0
		self.total_percentage = 0
		self.cost = 0
		self.type = 0
		if app.WJ_ENABLE_TRADABLE_ICON:
			self.lockedItem = (-1,-1)

	def __LoadScript(self):
		try:
			pyScrLoader = ui.PythonScriptLoader()
			pyScrLoader.LoadScriptFile(self, "uiscript/refinedialogrenewal_norm.py")
		except:
			import exception
			exception.Abort("RefineDialog.__LoadScript.LoadObject")
		try:
			self.board = self.GetChild("Board")
			self.titleBar = self.GetChild("TitleBar")
			self.probText = self.GetChild("SuccessPercentage")
			self.costText = self.GetChild("Cost")
			self.button_accept = self.GetChild("AcceptButton")

			self.GetChild("AcceptButton").SetEvent(self.OpenQuestionDialog)
			self.GetChild("CancelButton").SetEvent(self.CancelRefine)
		except:
			import exception
			exception.Abort("RefineDialog.__LoadScript.BindObject")

		self.toolTipNext = uiToolTip.ItemToolTip()
		self.toolTipNext.HideToolTip()

		self.toolTipCur = uiToolTip.ItemToolTip()
		self.toolTipCur.HideToolTip()

		self.tooltipMode = uiToolTip.ItemToolTip()
		self.tooltipMode.HideToolTip()

		self.toolTipMaterial = uiToolTip.ItemToolTip()
		self.toolTipMaterial.HideToolTip()

		self.itemImageCur = ui.MakeImageBox(self, False, 45, 89)
		self.itemImageNext = ui.MakeImageBox(self, False, 125 * 3 + 56, 89)
		
		self.materialList = []

		self.titleBar.SetCloseEvent(ui.__mem_func__(self.CancelRefine))
		self.isLoaded = TRUE
		if app.ENABLE_COSTUME_SYSTEM:
			self.checkBox = ui.CheckBox()
			self.checkBox.SetParent(self)
			self.checkBox.SetPosition(40, 12)
			self.checkBox.SetEvent(ui.__mem_func__(self.AutoRefine), "ON_CHECK", True)
			self.checkBox.SetEvent(ui.__mem_func__(self.AutoRefine), "ON_UNCKECK", False)
			self.checkBox.SetCheckStatus(constInfo.IS_AUTO_REFINE)
			self.checkBox.SetTextInfo(uiScriptLocale.UPGRADE)
			self.checkBox.Show()

	def __del__(self):
		ui.ScriptWindow.__del__(self)

	def __MakeItemSlot(self,c):
		itemslot = ui.SlotWindow()
		itemslot.SetParent(self)
		itemslot.SetSize(32, 32)
		itemslot.AppendSlot(c, 0, 0, 32, 32)
		itemslot.SetOverInItemEvent(ui.__mem_func__(self.OverInItem))
		itemslot.SetOverOutItemEvent(ui.__mem_func__(self.OverOutItem))
		itemslot.RefreshSlot()
		itemslot.SetSlotBaseImage("d:/ymir work/ui/public/Slot_Base.sub", 1.0, 1.0, 1.0, 1.0)
		itemslot.Show()
		self.children.append(itemslot)
		return itemslot

	def __MakeThinBoard(self):
		thinBoard = ui.ThinBoard()
		thinBoard.SetParent(self)
		thinBoard.Show()
		self.children.append(thinBoard)
		return thinBoard

	def Destroy(self):
		self.ClearDictionary()
		self.dlgQuestion = None
		self.board = 0
		self.probText = 0
		self.costText = 0
		self.titleBar = 0
		self.toolTipNext = 0
		self.toolTipCur = 0
		self.itemImageCur = 0
		self.itemImageNext = 0
		self.children = []
		self.materialList = []
		self.toolTipMaterial = 0
		self.slotCurrent = None
		self.slotAfter = None
		self.numberSlotImage = None
		self.imgPotion = None
		REFINE_TOTAL_PERCENTAGE["update"] = 0

		if app.WJ_ENABLE_TRADABLE_ICON:
			self.wndInventory = None
			self.lockedItem = (-1,-1)

	if app.ENABLE_COSTUME_SYSTEM:
		def __InitializeOpen(self):
			self.children = []
			self.vnum = 0
			self.targetItemPos = 0
			self.dialogHeight = 0
			self.cost = 0
			self.percentage = 0
			self.type = 0
			self.xRefineStart = 0
			self.yRefineStart = 0	

	def Open(self, targetItemPos, nextGradeItemVnum, cost, prob, type):
		if FALSE == self.isLoaded:
			self.__LoadScript()

		if app.ENABLE_COSTUME_SYSTEM:
			self.__InitializeOpen()
		else:
			self.__Initialize()

		self.targetItemPos = targetItemPos
		self.vnum = nextGradeItemVnum
		self.cost = cost
		self.percentage = prob
		self.type = type
		# self.SetCenterPosition()

		self.Clear()

		if constInfo.ENABLE_REFINE_PCT:
			self.probText.SetText(localeInfo.REFINE_CURRENT_PERCENTAGE % (self.percentage))

		self.costText.SetText(localeInfo.TOOLTIP_BUYPRICE % (localeInfo.NumberToMoneyString(self.cost)))

		self.toolTipNext.ClearToolTip()
		self.toolTipCur.ClearToolTip()

		metinSlot = []
		for i in xrange(player.METIN_SOCKET_MAX_NUM):
			metinSlot.append(player.GetItemMetinSocket(targetItemPos, i))

		attrSlot = []
		for i in xrange(player.ATTRIBUTE_SLOT_MAX_NUM):
			attrSlot.append(player.GetItemAttribute(targetItemPos, i))

		self.toolTipCur.SetInventoryItem(targetItemPos)
		self.toolTipNext.AddRefineItemData(nextGradeItemVnum, metinSlot, attrSlot)

		curItemIndex = player.GetItemIndex(targetItemPos)
		
		if curItemIndex != 0:
			item.SelectItem(curItemIndex)

			try:
				self.itemImageCur.LoadImage(item.GetIconImageFileName())
			except:
				dbg.TraceError("Refine.CurrentItem.LoadImage - Failed to find item data")

		item.SelectItem(nextGradeItemVnum)
		self.itemImageNext.LoadImage(item.GetIconImageFileName())

		self.dialogHeight = 45
		self.UpdateDialog()

		# self.SetTop()
		self.Show()
		
	def Clear(self):
		REFINE_TOTAL_PERCENTAGE["update"] = 0

	def Close(self):
		self.dlgQuestion = None
		self.Clear()
		self.Hide()

	def AppendMaterial(self, vnum, count):
		grid = self.__MakeItemSlot(len(self.materialList))
		grid.SetPosition(128, self.dialogHeight)
		grid.SetItemSlot(len(self.materialList), vnum, 0)

		self.materialList.append(vnum)

		textLine = ui.TextLine()
		textLine.SetParent(grid)
		textLine.SetFontName(localeInfo.UI_DEF_FONT)
		textLine.SetText("%s x%d" % (item.GetItemName(), count))
		textLine.SetOutline()
		textLine.SetFeather(FALSE)
		textLine.SetWindowVerticalAlignCenter()
		textLine.SetVerticalAlignCenter()
		textLine.SetPosition(49, -18)
		textLine.SetPackedFontColor(0xff3dd95a)
		textLine.Show()
		self.children.append(textLine)
		
		textLine2 = ui.TextLine()
		textLine2.SetParent(grid)
		textLine2.SetFontName(localeInfo.UI_DEF_FONT)
		textLine2.SetText("Iteme detinute: |cFFddcb77%d" % (player.GetItemCountByVnum(vnum)))
		textLine2.SetOutline()
		textLine2.SetFeather(FALSE)
		textLine2.SetWindowVerticalAlignCenter()
		textLine2.SetVerticalAlignCenter()
		textLine2.SetPosition(49, 2)
		textLine2.Show()
		self.children.append(textLine2)

		self.dialogHeight += 37
		self.UpdateDialog()

	def UpdateDialog(self):
		(x, y) = self.GetLocalPosition()
		self.SetPosition(x, y)

	def OpenQuestionDialog(self):
		totalPerc = self.percentage + REFINE_TOTAL_PERCENTAGE["update"]

		if 100 == totalPerc:
			self.Accept()
			return

		if 5 == self.type:
			self.Accept()
			return

		dlgQuestion = uiCommon.QuestionDialog2()
		dlgQuestion.SetText2(localeInfo.REFINE_WARNING2)
		dlgQuestion.SetAcceptEvent(ui.__mem_func__(self.Accept))
		dlgQuestion.SetCancelEvent(ui.__mem_func__(dlgQuestion.Close))

		if 3 == self.type:
			dlgQuestion.SetText1(localeInfo.REFINE_DESTROY_WARNING_WITH_BONUS_PERCENT_1)
			dlgQuestion.SetText2(localeInfo.REFINE_DESTROY_WARNING_WITH_BONUS_PERCENT_2)
		elif 2 == self.type:
			dlgQuestion.SetText1(localeInfo.REFINE_DOWN_GRADE_WARNING)
		else:
			dlgQuestion.SetText1(localeInfo.REFINE_DESTROY_WARNING)

		dlgQuestion.Open()
		self.dlgQuestion = dlgQuestion

	def Accept(self):
		totalPerc = self.percentage + REFINE_TOTAL_PERCENTAGE["update"]
		net.SendRefinePacket(self.targetItemPos, self.type)
		if not app.ENABLE_COSTUME_SYSTEM:
			self.Close()

	if app.ENABLE_COSTUME_SYSTEM:	
		def AutoRefine(self, checkType, autoFlag):
			constInfo.IS_AUTO_REFINE = autoFlag
		
		def CheckRefine(self, isFail):
			if constInfo.IS_AUTO_REFINE == True:
				if constInfo.AUTO_REFINE_TYPE == 1:
					if constInfo.AUTO_REFINE_DATA["ITEM"][0] != -1 and constInfo.AUTO_REFINE_DATA["ITEM"][1] != -1:
						scrollIndex = player.GetItemIndex(constInfo.AUTO_REFINE_DATA["ITEM"][0])
						itemIndex = player.GetItemIndex(constInfo.AUTO_REFINE_DATA["ITEM"][1])
						
						if scrollIndex == 0 or (itemIndex % 10 == 8 and not isFail):
							self.Close()
						else:
							net.SendItemUseToItemPacket(constInfo.AUTO_REFINE_DATA["ITEM"][0], constInfo.AUTO_REFINE_DATA["ITEM"][1])
				elif constInfo.AUTO_REFINE_TYPE == 2:
					npcData = constInfo.AUTO_REFINE_DATA["NPC"]
					if npcData[0] != 0 and npcData[1] != -1 and npcData[2] != -1 and npcData[3] != 0:
						itemIndex = player.GetItemIndex(npcData[1], npcData[2])
						if (itemIndex % 10 == 8 and not isFail) or isFail:
							self.Close()
						else:
							net.SendGiveItemPacket(npcData[0], npcData[1], npcData[2], npcData[3])
				else:
					self.Close()
			else:
				self.Close()

	def OnUpdate(self):
		if self.itemImageCur:
			if self.itemImageCur.IsIn():
				self.toolTipCur.ShowToolTip()
			else:
				self.toolTipCur.HideToolTip()

		if self.itemImageNext:
			if self.itemImageNext.IsIn():
				self.toolTipNext.ShowToolTip()
			else:
				self.toolTipNext.HideToolTip()

	def CancelRefine(self):
		net.SendRefinePacket(255, 255)
		self.Close()
		if app.ENABLE_COSTUME_SYSTEM:
			constInfo.AUTO_REFINE_TYPE = 0
			constInfo.AUTO_REFINE_DATA = {
				"ITEM" : [-1, -1],
				"NPC" : [0, -1, -1, 0]
			}

	def OnPressEscapeKey(self):
		self.CancelRefine()
		return TRUE

	if app.WJ_ENABLE_TRADABLE_ICON:
		def SetCanMouseEventSlot(self, slotIndex):
			itemInvenPage = slotIndex / player.INVENTORY_PAGE_SIZE
			localSlotPos = slotIndex - (itemInvenPage * player.INVENTORY_PAGE_SIZE)
			self.lockedItem = (-1, -1)

			if itemInvenPage == self.wndInventory.GetInventoryPageIndex():
				self.wndInventory.wndItem.SetCanMouseEventSlot(localSlotPos)

		def SetCantMouseEventSlot(self, slotIndex):
			itemInvenPage = slotIndex / player.INVENTORY_PAGE_SIZE
			localSlotPos = slotIndex - (itemInvenPage * player.INVENTORY_PAGE_SIZE)
			self.lockedItem = (itemInvenPage, localSlotPos)

			if itemInvenPage == self.wndInventory.GetInventoryPageIndex():
				self.wndInventory.wndItem.SetCantMouseEventSlot(localSlotPos)

		def SetInven(self, wndInventory):
			from _weakref import proxy
			self.wndInventory = proxy(wndInventory)

		def RefreshLockedSlot(self):
			if self.wndInventory:
				itemInvenPage, itemSlotPos = self.lockedItem
				if self.wndInventory.GetInventoryPageIndex() == itemInvenPage:
					self.wndInventory.wndItem.SetCantMouseEventSlot(itemSlotPos)

				self.wndInventory.wndItem.RefreshSlot()

	def OverInItem(self, slot):
		if self.toolTipMaterial:
			self.toolTipMaterial.SetItemToolTip(self.materialList[slot])

	def OverOutItem(self):
		if self.toolTipMaterial:
			self.toolTipMaterial.HideToolTip()
