import uiCommon, chat, app, net, item, wndMgr, mouseModule, localeInfo, constInfo
import thenewui as ui
import CacheEffect as player
import uiScriptLocale
# import skill
import renderTarget

import systemSetting
import grp

class ChestDropWindow(ui.ScriptWindow):
	timer = 0
	def __init__(self):
		ui.ScriptWindow.__init__(self, "GAME")

		self.tooltipItem = None
		self.AnimSize = 0.0

		self.currentChest = 0
		self.currentPage = 1
		self.openAmount = 1
		self.invItemPos = -1

		self.chestDrop = { }
		
		# skillIcon = skill.GetIconImage(246)
		# import chat
		# chat.AppendChat(1, "Icon :%s" % str(skillIcon))

		self.__LoadWindow()
		
		self.GetChild("board").SetSize(600, 400)
		self.SetSize(600, 400)
		
		# import uiwiky_ful
		# self.ThinFull = uiwiky_ful.WikiScrollBar()
		# self.ThinFull.SetParent(self)
		# self.ThinFull.SetSize(7, 155)
		# self.ThinFull.SetPosition(25, 45)
		# self.ThinFull.Show()

		# self.ModelPreview = ui.RenderTarget()
		# self.ModelPreview.SetParent(self.ThinFull)
		# self.ModelPreview.SetSize(130, 121)
		# self.ModelPreview.SetPosition(125, 45)
		# self.ModelPreview.SetRenderTarget(44)
		# self.ModelPreview.Show()
	
		# renderTarget.SetBackground(44, "d:/ymir work/ui/shop/decoration/background.png")
		# renderTarget.SetVisibility(44, True)
		# renderTarget.SelectModel(44, 691)
		
		self.scaleTimeStart = app.GetTime()
		# wndMgr.SetScaleWindow(self.hWnd, 0.2, 0.2)

	def __del__(self):
		ui.ScriptWindow.__del__(self)

	def __LoadWindow(self):
		try:
			PythonScriptLoader = ui.PythonScriptLoader()
			PythonScriptLoader.LoadScriptFile(self, "UIScript/chestdropwindow.py")
		except:
			import exception
			exception.Abort("ChestDropWindow.__LoadWindow.LoadObject")

		try:
			self.titleBar = self.GetChild("TitleBar")

			self.openItemSlot = self.GetChild("OpenItemSlot")
			self.openItemSlot.Hide()
			self.openCountController = self.GetChild("OpenCountController")
			self.openChestButtonSingle = self.GetChild("OpenChestButtonSingle")
			self.openChestButtonMultiple = self.GetChild("OpenChestButtonMultiple")

			self.prevButton = self.GetChild("prev_button")
			self.nextButton = self.GetChild("next_button")
			self.currentPageBack = self.GetChild("CurrentPageBack")
			self.currentPageText = self.GetChild("CurrentPage")
		except:
			import exception
			exception.Abort("ChestDropWindow.__LoadWindow.BindObject")

		self.titleBar.SetCloseEvent(ui.__mem_func__(self.Close))
		self.openCountController.SetEvent(ui.__mem_func__(self.OnChangeOpenAmount))

		self.openChestButtonSingle.SetEvent(ui.__mem_func__(self.OnClickOpenChest))
		self.openChestButtonMultiple.SetEvent(ui.__mem_func__(self.OnClickOpenChest))

		self.openChestButtonSingle.SetText(uiScriptLocale.CHEST_OPEN_COUNT % self.openAmount)
		self.openChestButtonMultiple.SetText(uiScriptLocale.CHEST_OPEN_COUNT % self.openAmount)

		self.prevButton.SetEvent(ui.__mem_func__(self.OnClickPrevPage))
		self.nextButton.SetEvent(ui.__mem_func__(self.OnClickNextPage))

		self.currentPageText.SetText(str(self.currentPage))

		wndItem = ui.GridSlotWindow()
		wndItem.SetParent(self)
		wndItem.SetPosition(8, 35)
		wndItem.SetSlotStyle(wndMgr.SLOT_STYLE_NONE)
		wndItem.SetOverInItemEvent(ui.__mem_func__(self.OverInItem))
		wndItem.SetOverOutItemEvent(ui.__mem_func__(self.OverOutItem))
		wndItem.ArrangeSlot(0, 15, 5, 32, 32, 0, 0)
		wndItem.RefreshSlot()
		wndItem.SetSlotBaseImage("d:/ymir work/ui/game/comp/slot.png", 1.0, 1.0, 1.0, 1.0)
		# wndItem.Show()

		self.wndItem = wndItem
		
		self.openCountController.SetSliderPos(float(systemSetting.GetFieldOfView() * 2))

	def Close(self):
		self.invItemPos = -1
		self.Hide()

	def Destroy(self):
		self.ClearDictionary()

		self.tooltipItem = None
		self.wndItem = None

		self.currentChest = 0
		self.currentPage = 1
		self.openAmount = 1
		self.invItemPos = -1
		self.chestDrop = { }
	
	def Show(self):
		ui.ScriptWindow.Show(self)
		self.SetTop()
		self.SetCenterPosition()
	
	def Open(self, invItemPos = -1):
		self.currentChest = 0
		self.currentPage = 1
		self.openAmount = 1
		self.openCountController.SetSliderPos(0.0)
		self.chestDrop = { }
		self.RefreshItemSlot()

		self.SetInvItemSlot(invItemPos)

		self.SetTop()
		self.SetCenterPosition()
		self.Show()

	def SetItemToolTip(self, tooltip):
		self.tooltipItem = tooltip

	def OnChangeOpenAmount(self):
		openTemp = float(self.openCountController.GetSliderPos()) / 2
		# if openTemp == 0:
			# self.openAmount = 1
		# else:
			# self.openAmount = openTemp
		
		chat.AppendChat(1, str(openTemp))
		
		systemSetting.SetFieldOfView(openTemp)
		
		# self.ModelPreview.SetSize(openTemp*10, openTemp*10)
		# renderTarget.SetSizeTest(44, self.ModelPreview.GetWidth()-openTemp, self.ModelPreview.GetHeight()-openTemp)

		# self.openChestButtonSingle.SetText(uiScriptLocale.CHEST_OPEN_COUNT % self.openAmount)
		# self.openChestButtonMultiple.SetText(uiScriptLocale.CHEST_OPEN_COUNT % self.openAmount)

	def AddChestDropItem(self, chestVnum, pageIndex, slotIndex, itemVnum, itemCount):
		if not self.chestDrop.has_key(chestVnum):
			self.chestDrop[chestVnum] = {}

		if not self.chestDrop[chestVnum].has_key(pageIndex):
			self.chestDrop[chestVnum][pageIndex] = {}

		if self.chestDrop[chestVnum].has_key(pageIndex):
			if self.chestDrop[chestVnum][pageIndex].has_key(slotIndex):
				if self.chestDrop[chestVnum][pageIndex][slotIndex][0] == itemVnum and self.chestDrop[chestVnum][pageIndex][slotIndex][1] == itemCount:
					return

		self.chestDrop[chestVnum][pageIndex][slotIndex] = [itemVnum, itemCount]

	def OnClickOpenChest(self):
		if self.invItemPos == -1:
			return

		itemCount = player.GetItemCount(self.invItemPos)

		if app.GetTime() > self.timer:
			if itemCount >= self.openAmount:
				for i in xrange(self.openAmount):
					if itemCount == 1:
						net.SendItemUsePacket(self.invItemPos)
						self.OnPressEscapeKey()
						break

					net.SendItemUsePacket(self.invItemPos)
					itemCount = itemCount - 1
			else:
				for i in xrange(itemCount):
					if itemCount == 1:
						net.SendItemUsePacket(self.invItemPos)
						self.OnPressEscapeKey()
						break

					net.SendItemUsePacket(self.invItemPos)
					itemCount = itemCount - 1

			self.timer = app.GetTime() + 1
		else:
			v = self.timer - app.GetTime()
			chat.AppendChat(chat.CHAT_TYPE_INFO, "Poti deschide in %d secunde." % (v))

	def OnClickPrevPage(self):
		if not self.chestDrop.has_key(self.currentChest):
			return

		if self.chestDrop[self.currentChest].has_key(self.currentPage - 1):
			self.currentPage = self.currentPage - 1
			self.currentPageText.SetText(str(self.currentPage))
			self.RefreshItemSlot()

	def OnClickNextPage(self):
		if not self.chestDrop.has_key(self.currentChest):
			return

		if self.chestDrop[self.currentChest].has_key(self.currentPage + 1):
			self.currentPage = self.currentPage + 1
			self.currentPageText.SetText(str(self.currentPage))
			self.RefreshItemSlot()

	def EnableMultiPage(self):
		self.openChestButtonSingle.Hide()
		self.openChestButtonMultiple.Show()

		self.prevButton.Show()
		self.nextButton.Show()
		self.currentPageBack.Show()

	def EnableSinglePage(self):
		self.openChestButtonSingle.Show()
		self.openChestButtonMultiple.Hide()

		self.prevButton.Hide()
		self.nextButton.Hide()
		self.currentPageBack.Hide()	

	def SetInvItemSlot(self, invItemPos):
		self.invItemPos = invItemPos

		itemVnum = player.GetItemIndex(invItemPos)
		itemCount = player.GetItemCount(invItemPos)
		if itemVnum:
			self.openItemSlot.SetItemSlot(0, itemVnum, itemCount)

	def GetInvItemSlot(self):
		return self.invItemPos

	def RefreshItems(self, chestVnum):
		if chestVnum:
			self.currentChest = chestVnum

		if not self.chestDrop.has_key(self.currentChest):
			chat.AppendChat(chat.CHAT_TYPE_INFO, "Acest cufar nu are drop. Raporteaza probleme unui administrator.")
			self.Close()
			return

		if self.chestDrop[self.currentChest].has_key(2):
			self.EnableMultiPage()
		else:
			self.EnableSinglePage()

		self.RefreshItemSlot()

	def RefreshItemSlot(self):
		for i in xrange(15 * 5):
			self.wndItem.ClearSlot(i)

		if not self.chestDrop.has_key(self.currentChest):
			return

		if not self.chestDrop[self.currentChest].has_key(self.currentPage):
			return

		for key, value in self.chestDrop[self.currentChest][self.currentPage].iteritems():
			itemVnum = value[0]
			itemCount = value[1]

			if itemCount <= 1:
				itemCount = 0

			self.wndItem.SetItemSlot(key, itemVnum, itemCount)

		wndMgr.RefreshSlot(self.wndItem.GetWindowHandle())

	def OverInItem(self, slotIndex):
		if mouseModule.mouseController.isAttached():
			return

		if not self.chestDrop.has_key(self.currentChest):
			return

		if not self.chestDrop[self.currentChest].has_key(self.currentPage):
			return

		if 0 != self.tooltipItem:
			self.tooltipItem.SetItemToolTip(self.chestDrop[self.currentChest][self.currentPage][slotIndex][0])

	def OverOutItem(self):
		if 0 != self.tooltipItem:
			self.tooltipItem.HideToolTip()

	def OnPressEscapeKey(self):
		self.Close()
		return True