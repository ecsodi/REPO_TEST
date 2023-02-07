import uiCommon
import chat
import app
import net
import player
import item
import wndMgr
import mouseModule
import localeInfo
import ui
import cfg

class GayaWindow(ui.ScriptWindow):
	
	LIMIT_RANGE = 500
	MAX_ITEMS_PER_PAGE = 12

	def __init__(self):
		ui.ScriptWindow.__init__(self)

		self.xGayaStart = 0
		self.yGayaStart = 0
		self.page = 0
		self.CurrentRace = 0
		self.max_size = 0
		
		self.ListPrice = {}
		self.ListIcon = {}
		self.ListItems = {}
		
		self.questionDialog = None
		self.tooltipItem = None
		self.__LoadWindow()

	def __del__(self):
		ui.ScriptWindow.__del__(self)
		
	def __LoadWindow(self):
		try:
			PythonScriptLoader = ui.PythonScriptLoader()
			PythonScriptLoader.LoadScriptFile(self, "UIScript/gaya.py")
		except:
			import exception
			exception.Abort("GayaWindow.__LoadWindow.LoadObject")

		try:
			self.titleBar = self.GetChild("TitleBar")
			self.itemSlot = self.GetChild("ItemSlot")
			self.btnPagePrev = self.GetChild("PrevButton")
			self.btnPageNext = self.GetChild("NextButton")
			self.wndTextPage = self.GetChild("TextPage")
			
			for i in xrange(self.MAX_ITEMS_PER_PAGE):
				self.ListPrice[i] = self.GetChild("slot_%s_price" % str(i+1))
			
			for i in xrange(self.MAX_ITEMS_PER_PAGE):
				self.ListIcon[i] = self.GetChild("slot_%s_Icon" % str(i+1))
		except:
			import exception
			exception.Abort("GayaWindow.__LoadWindow.BindObject")
			
		self.titleBar.SetCloseEvent(ui.__mem_func__(self.Close))
		
		self.btnPagePrev.SetEvent(ui.__mem_func__(self.OnPagePrev))
		self.btnPageNext.SetEvent(ui.__mem_func__(self.OnPageNext))
		
		self.itemSlot.SetSlotStyle(wndMgr.SLOT_STYLE_NONE)
		self.itemSlot.SetOverInItemEvent(ui.__mem_func__(self.OverInItem))
		self.itemSlot.SetOverOutItemEvent(ui.__mem_func__(self.OverOutItem))
		self.itemSlot.SetSelectItemSlotEvent(ui.__mem_func__(self.UseItemSlot))
		self.itemSlot.SetSlotBaseImage("d:/ymir work/ui/public/Slot_Base.sub", 1.0, 1.0, 1.0, 1.0)

	def OnPagePrev(self):
		if self.questionDialog:
			return

		self.OnPage(self.page - 1)
	
	def OnPageNext(self):
		if self.questionDialog:
			return

		self.OnPage(self.page + 1)
	
	def Close(self):
		self.QuestionDialogClose()
		if 0 != self.tooltipItem:
			self.tooltipItem.HideToolTip()
		self.Hide()
		
	def Destroy(self):
		self.ClearDictionary()
		self.questionDialog = None
		
	def Open(self):
		self.SetTop()
		self.SetCenterPosition()
		self.OnPage(0)
		self.RefreshActivateSlot(-1)
		self.Show()

		(self.xGayaStart, self.yGayaStart, z) = player.GetMainCharacterPosition()
	
	def OnUpdate(self):
		(x, y, z) = player.GetMainCharacterPosition()
		if abs(x - self.xGayaStart) > self.LIMIT_RANGE or abs(y - self.yGayaStart) > self.LIMIT_RANGE:
			self.Close()
			
	def SetItemToolTip(self, tooltip):
		self.tooltipItem = tooltip
			
	def OverInItem(self, slotIndex):
		if mouseModule.mouseController.isAttached():
			return

		if 0 != self.tooltipItem and self.GetItem(self.page*self.MAX_ITEMS_PER_PAGE+slotIndex) != 0:
			self.tooltipItem.SetItemToolTip(self.GetItem(self.page*self.MAX_ITEMS_PER_PAGE+slotIndex))

	def GetItem(self, pos):
		if pos > len(self.ListItems):
			return 0
			
		return self.ListItems[pos]["VnumReward"]

	def OverOutItem(self):
		if 0 != self.tooltipItem:
			self.tooltipItem.HideToolTip()
						
	def UseItemSlot(self, slotIndex):
		if self.questionDialog:
			return

		self.iPosBuyItem = int(self.page*self.MAX_ITEMS_PER_PAGE+slotIndex)
	
		questionDialog = uiCommon.QuestionDialog()
		item.SelectItem(self.GetItem(self.page*self.MAX_ITEMS_PER_PAGE+slotIndex))
		questionDialog.SetText(localeInfo.GAYA_ASK_BUY % (item.GetItemName()))
		questionDialog.SetAcceptEvent(ui.__mem_func__(self.AcceptBuy))
		questionDialog.SetCancelEvent(ui.__mem_func__(self.QuestionDialogClose))
		questionDialog.Open()
		self.questionDialog = questionDialog
		
		self.RefreshActivateSlot(slotIndex)

	def AcceptBuy(self):
		self.QuestionDialogClose()
		net.SendBuyItemGaya(self.iPosBuyItem, self.CurrentRace)
	
	def RefreshActivateSlot(self, index):
		for i in xrange(self.MAX_ITEMS_PER_PAGE):
			if index == i:
				self.itemSlot.ActivateSlot(i)
			else:
				self.itemSlot.DeactivateSlot(i)

	def OnPressEscapeKey(self):
		self.Close()
		return True

	def Clear(self, bClearList = True):
		if bClearList == True:
			self.ListItems = {}

		for i in xrange(self.MAX_ITEMS_PER_PAGE):
			self.ListPrice[i].SetText(" ")
			self.ListIcon[i].Hide()
			self.itemSlot.SetItemSlot(i, 0, 0)

		wndMgr.RefreshSlot(self.itemSlot.GetWindowHandle())

	def Set(self, race):
		self.CurrentRace = race
		self.Open()

	def AddItem(self, pos, dwVnumReward, bCountReward, dwVnumPrice, iCountNeed, bType):
		self.ListItems[pos] = {"VnumReward":dwVnumReward, "CountReward":bCountReward, "VnumPrice":dwVnumPrice, "CountNeed":iCountNeed, "Type":bType}

	def OnPage(self, page):
		if page * self.MAX_ITEMS_PER_PAGE >= len(self.ListItems) or page < 0:
			return
	
		self.Clear(False)
	
		for i in xrange(self.MAX_ITEMS_PER_PAGE):
			if page * self.MAX_ITEMS_PER_PAGE + i >= len(self.ListItems):
				break
			
			self.itemSlot.SetItemSlot(i, self.ListItems[page*self.MAX_ITEMS_PER_PAGE+i]["VnumReward"], self.ListItems[page*self.MAX_ITEMS_PER_PAGE+i]["CountReward"])
			self.ListPrice[i].SetText(self.GetColorNeedCount(self.ListItems[page*self.MAX_ITEMS_PER_PAGE+i]["VnumPrice"], self.ListItems[page*self.MAX_ITEMS_PER_PAGE+i]["CountNeed"]))
			
			if self.ListItems[page*self.MAX_ITEMS_PER_PAGE+i]["Type"] == 0:
				self.ListIcon[i].LoadImage("d:/ymir work/ui/gemshop/gemshop_gemicon.sub")
				self.ListIcon[i].Show()
			elif self.ListItems[page*self.MAX_ITEMS_PER_PAGE+i]["Type"] == 1:
				self.ListIcon[i].LoadImage("d:/ymir work/ui/public/gaya_coin.png")
				self.ListIcon[i].Show()
			
			wndMgr.RefreshSlot(self.itemSlot.GetWindowHandle())
			
		self.page = page
		
		self.wndTextPage.SetText(str(self.GetTextPage()))

	def GetColorNeedCount(self, vnum, price):
		# if player.GetItemCountByVnum(vnum) < price:
			# set color text
			
		return str(price)

	def GetTextPage(self):
		return str(self.page + 1) + " / " + str(int(len(self.ListItems) / self.MAX_ITEMS_PER_PAGE) + 1)

	def QuestionDialogClose(self):
		if self.questionDialog:
			self.questionDialog.Close()

		self.questionDialog = None
		self.RefreshActivateSlot(-1)
