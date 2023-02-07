import thenewui as ui
import shop
import mouseModule
import CacheEffect as player
import Collision as chr
import net
import uiCommon
import localeInfo
import chat
import item
import systemSetting
import renderTarget
import app
import constInfo
import itemprices
import uiScriptLocale
import cfg

g_isBuildingPrivateShop = False

g_itemPriceDict={}

g_privateShopAdvertisementBoardDict={}

RENDER_TARGET_INDEX = 1
class OfflineShopDecoration(ui.ScriptWindow):
	def __init__(self):
		self.SelectedDeco = 30000
		ui.ScriptWindow.__init__(self)
		self.__LoadWindow()
		
	def __del__(self):
		ui.ScriptWindow.__del__(self)

	def __LoadWindow(self):
		self.AddFlag("float")
		self.AddFlag("movable")
		self.AddFlag("animation")
	
		self.Board = ui.Board()
		self.Board.SetParent(self)
		self.Board.SetSize(475, 300)
		self.Board.AddFlag("not_pick")
		self.Board.Show()	
		
		self.boardImage = ui.ImageBox()
		self.boardImage.SetParent(self.Board)
		self.boardImage.LoadImage("d:/ymir work/ui/shop/decoration/bg3.png")
		self.boardImage.AddFlag("not_pick")
		self.boardImage.SetPosition(10,10)
		self.boardImage.Show()
		
		
		# self.textBoards = ui.ImageBox()
		# self.textBoards.SetParent(self.boardImage)
		# self.textBoards.LoadImage("d:/ymir work/ui/shop/decoration/title.png")
		# self.textBoards.AddFlag("not_pick")
		# self.textBoards.SetPosition(3,3)
		# self.textBoards.Show()


		self.btnClose = ui.MakeButton(self, 100, 265, False, "d:/ymir work/ui/shop/decoration/", "btn_normal.png", "btn_hover.png", "btn_down.png")
		self.btnClose.SetWindowHorizontalAlignCenter()
		self.btnClose.SetText(uiScriptLocale.CLOSE)
		self.btnClose.SetEvent(ui.__mem_func__(self.Close))

		self.btnSave = ui.MakeButton(self, -100, 265, False, "d:/ymir work/ui/shop/decoration/", "btn_normal.png", "btn_hover.png", "btn_down.png")
		self.btnSave.SetText(localeInfo.SWITCHBOT_SAVE)
		self.btnSave.SetWindowHorizontalAlignCenter()
		self.btnSave.SetEvent(ui.__mem_func__(self.Close))
		
		self.ModelPreview = ui.RenderTargetV2()
		self.ModelPreview.SetParent(self.boardImage)
		self.ModelPreview.SetSize(137, 230)
		self.ModelPreview.SetPosition(158, 10)
		self.ModelPreview.SetRenderTarget(RENDER_TARGET_INDEX)
		self.ModelPreview.Show()
		
		renderTarget.SetBackground(RENDER_TARGET_INDEX, "d:/ymir work/ui/shop/decoration/bg_render.png")
		renderTarget.SetVisibility(RENDER_TARGET_INDEX, True)
		renderTarget.SelectModel(RENDER_TARGET_INDEX, 30000)
		
		# Create Buttons
		self.dictButtons = {}
		dictNames = {
		"Normal" : 30000, 
		uiScriptLocale.FREEDOM_FLAG_DECO : 30001, 
		uiScriptLocale.X1001_NIGHTS_DECO : 30002, 
		uiScriptLocale.KING_BBQ_DECO : 30003, 
		uiScriptLocale.TREASURE_HUNTER_DECO : 30004, 
		uiScriptLocale.ECONOMIC_FLAME_DECO : 30005, 
		uiScriptLocale.ARMS_DEALER_DECO : 30006,
		uiScriptLocale.ARMOR_DEALER_DECO : 30007,
		uiScriptLocale.ALCHEMY_DEALER_DECO : 30008,
		}
	
		for cnt, key in enumerate(dictNames):
			if cnt > 6:
				self.dictButtons[key] = ui.MakeButton(self, 322, 47+ cnt*30 - 210, False, "d:/ymir work/ui/shop/decoration/", "slot_normal.png", "slot_hover.png", "slot_selected.png")
			else:
				self.dictButtons[key] = ui.MakeButton(self, 19, 47+ cnt*30, False, "d:/ymir work/ui/shop/decoration/", "slot_normal.png", "slot_hover.png", "slot_selected.png")

			self.dictButtons[key].SetText(key)
			self.dictButtons[key].SetEvent(ui.__mem_func__(self.SetRenderTarget), dictNames[key])
			
		self.SetSize(self.Board.GetWidth(), self.Board.GetHeight())

	def SetRenderTarget(self, Vnum):
		renderTarget.SetBackground(RENDER_TARGET_INDEX, "d:/ymir work/ui/shop/decoration/bg_render.png")
		renderTarget.SetVisibility(RENDER_TARGET_INDEX, True)
		renderTarget.SelectModel(RENDER_TARGET_INDEX, Vnum)
		
		self.SelectedDeco = Vnum
		self.ModelPreview.Show()

	def GetDecorationSelect(self):
		return self.SelectedDeco

	def Show(self):
		ui.ScriptWindow.Show(self)
		self.SetCenterPosition()
		self.SetRenderTarget(30000)
		self.SetTop()
		
	def Close(self):
		self.ModelPreview.Hide()
		renderTarget.SetVisibility(RENDER_TARGET_INDEX, False)
		self.Hide()
		
	def OnPressEscapeKey(self):
		self.Close()
		return True
		
class PrivateShopBuilder(ui.ScriptWindow):

	def __init__(self):
		ui.ScriptWindow.__init__(self)

		self.__LoadWindow()
		self.itemStock = {}
		self.tooltipItem = None
		self.priceInputBoard = None
		self.title = ""

	def __del__(self):
		ui.ScriptWindow.__del__(self)

	def __LoadWindow(self):
		self.AddFlag("float")
		self.AddFlag("movable")
		self.AddFlag("animation")
	
		self.Board = ui.BoardWithTitleBar()
		self.Board.SetParent(self)
		self.Board.SetSize(345, 385)
		self.Board.SetTitleName(uiScriptLocale.PRIVATE_SHOP_TITLE)
		self.Board.AddFlag("not_pick")
		self.Board.Show()
		
		self.SetSize(self.Board.GetWidth(), self.Board.GetHeight())
		
		# self.TitleBar = ui.TitleBar()
		# self.TitleBar.SetParent(self)
		# self.TitleBar.MakeTitleBar(354, "red")
		# self.TitleBar.SetPosition(6, 6)
		# self.TitleBar.Show()
		self.wndDecoration = OfflineShopDecoration()
		self.wndDecoration.Hide()
		
		# self.NameSlotBar = ui.MakeImageBox(self, "d:/ymir work/ui/shop/offlineshop/name_field.png", 14, 35)
		
		self.NameSlotBar = ui.SlotBar()
		self.NameSlotBar.SetParent(self.Board)
		self.NameSlotBar.SetPosition(13, 35)
		self.NameSlotBar.SetSize(317, 18)
		self.NameSlotBar.Show()
		
		self.nameLine = ui.EditLine()
		self.nameLine.SetParent(self.NameSlotBar)
		self.nameLine.SetPosition(3, 4)
		self.nameLine.SetSize(320, 18)
		self.nameLine.SetMax(30)
		self.nameLine.Show()
		self.btnOk = ui.MakeButton(self, 64, 350, False, "d:/ymir work/ui/public/", "middle_button_01.sub", "middle_button_02.sub", "middle_button_03.sub")
		self.btnClose = ui.MakeButton(self, 225, 350, False, "d:/ymir work/ui/public/", "middle_button_01.sub", "middle_button_02.sub", "middle_button_03.sub")
		self.btnDeco = ui.MakeButton(self, 155, 60, False, "d:/ymir work/ui/game/shopsearchp2p/", "shop_btn_skin_normal.dds", "shop_btn_skin_hover.dds", "shop_btn_skin_pressed.dds")
		self.btnDeco.SetEvent(ui.__mem_func__(self.ShowDeco))

		self.btnOk.SetText("OK")
		self.btnClose.SetText("Inchide")
		
		self.btnOk.SetEvent(ui.__mem_func__(self.OnOk))
		self.btnClose.SetEvent(ui.__mem_func__(self.OnClose))
		self.Board.SetCloseEvent(ui.__mem_func__(self.OnClose))
		
		self.itemSlot = ui.GridSlotWindow()
		self.itemSlot.SetParent(self)
		self.itemSlot.SetPosition(12, 81)
		self.itemSlot.ArrangeSlot(0, 10, 8, 32, 32, 0, 0)
		
		self.itemSlot.SetSlotBaseImage("d:/ymir work/ui/public/Slot_Base.sub", 1.0, 1.0, 1.0, 1.0)
		
		self.itemSlot.SetSelectEmptySlotEvent(ui.__mem_func__(self.OnSelectEmptySlot))
		self.itemSlot.SetSelectItemSlotEvent(ui.__mem_func__(self.OnSelectItemSlot))
		self.itemSlot.SetOverInItemEvent(ui.__mem_func__(self.OnOverInItem))
		self.itemSlot.SetOverOutItemEvent(ui.__mem_func__(self.OnOverOutItem))
		self.itemSlot.Show()
	
	def ShowDeco(self):
		if self.wndDecoration.IsShow() == FALSE:
			self.wndDecoration.Show()

	def Destroy(self):
		self.ClearDictionary()

		self.nameLine = None
		self.itemSlot = None
		self.btnOk = None
		self.btnClose = None
		self.titleBar = None
		self.priceInputBoard = None
	
	def Show(self):
		ui.ScriptWindow.Show(self)
		self.SetCenterPosition()
		self.nameLine.SetText("")
		shop.ClearPrivateShopStock()
		global g_isBuildingPrivateShop
		g_isBuildingPrivateShop = True
	
	def Open(self, title):

		self.title = title

		if len(title) > 25:
			title = title[:22] + "..."

		self.itemStock = {}
		shop.ClearPrivateShopStock()
		self.nameLine.SetText(title)
		self.SetCenterPosition()
		self.Refresh()
		self.Show()

		global g_isBuildingPrivateShop
		g_isBuildingPrivateShop = True

	def Close(self):
		global g_isBuildingPrivateShop
		g_isBuildingPrivateShop = False

		self.title = ""
		self.itemStock = {}
		shop.ClearPrivateShopStock()
		self.Hide()
		if self.priceInputBoard:
			self.priceInputBoard.Close()
			itemprices.PRICE_DICT[self.priceInputBoard.itemVNum] = price
			self.priceInputBoard = None

	def SetItemToolTip(self, tooltipItem):
		self.tooltipItem = tooltipItem

	def Refresh(self):
		getitemVNum=player.GetItemIndex
		getItemCount=player.GetItemCount
		setitemVNum=self.itemSlot.SetItemSlot
		delItem=self.itemSlot.ClearSlot

		for i in xrange(shop.SHOP_SLOT_COUNT):

			if not self.itemStock.has_key(i):
				delItem(i)
				continue

			pos = self.itemStock[i]

			itemCount = getItemCount(*pos)
			if itemCount <= 1:
				itemCount = 0
			setitemVNum(i, getitemVNum(*pos), itemCount)
			
			if app.ENABLE_CHANGELOOK_SYSTEM:
				itemTransmutedVnum = shop.GetItemTransmutation(*pos)
				if itemTransmutedVnum:
					self.itemSlot.DisableCoverButton(i)
				else:
					self.itemSlot.EnableCoverButton(i)			

		self.itemSlot.RefreshSlot()

	def OnSelectEmptySlot(self, selectedSlotPos):

		isAttached = mouseModule.mouseController.isAttached()
		if isAttached:
			attachedSlotType = mouseModule.mouseController.GetAttachedType()
			attachedSlotPos = mouseModule.mouseController.GetAttachedSlotNumber()
			mouseModule.mouseController.DeattachObject()

			if player.SLOT_TYPE_INVENTORY != attachedSlotType:
				return
			attachedInvenType = player.SlotTypeToInvenType(attachedSlotType)

			itemVNum = player.GetItemIndex(attachedInvenType, attachedSlotPos)
			item.SelectItem(itemVNum)

			if item.IsAntiFlag(item.ANTIFLAG_GIVE) or item.IsAntiFlag(item.ANTIFLAG_MYSHOP):
				chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.PRIVATE_SHOP_CANNOT_SELL_ITEM)
				return

			# if app.WJ_ENABLE_TRADABLE_ICON and player.SLOT_TYPE_INVENTORY == attachedSlotType:
				# self.CantTradableItem(selectedSlotPos, attachedSlotPos)

			priceInputBoard = uiCommon.MoneyInputDialog()
			priceInputBoard.SetTitle(localeInfo.PRIVATE_SHOP_INPUT_PRICE_DIALOG_TITLE)
			priceInputBoard.SetAcceptEvent(ui.__mem_func__(self.AcceptInputPrice))
			priceInputBoard.SetCancelEvent(ui.__mem_func__(self.CancelInputPrice))
			priceInputBoard.Open()

			itemPrice=GetPrivateShopItemPrice(itemVNum)

			if itemPrice>0:
				priceInputBoard.SetValue(itemPrice)
			if itemVNum in itemprices.PRICE_DICT:
				priceInputBoard.SetValue(itemprices.PRICE_DICT[itemVNum])

			self.priceInputBoard = priceInputBoard
			self.priceInputBoard.itemVNum = itemVNum
			self.priceInputBoard.sourceWindowType = attachedInvenType
			self.priceInputBoard.sourceSlotPos = attachedSlotPos
			self.priceInputBoard.targetSlotPos = selectedSlotPos

	def OnSelectItemSlot(self, selectedSlotPos):

		isAttached = mouseModule.mouseController.isAttached()
		if isAttached:
			mouseModule.mouseController.DeattachObject()

		else:
			if not selectedSlotPos in self.itemStock:
				return

			invenType, invenPos = self.itemStock[selectedSlotPos]
			shop.DelPrivateShopItemStock(invenType, invenPos)


			del self.itemStock[selectedSlotPos]

			self.Refresh()

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

		for privatePos, (itemWindowType, itemSlotIndex) in self.itemStock.items():
			if itemWindowType == attachedInvenType and itemSlotIndex == sourceSlotPos:
				shop.DelPrivateShopItemStock(itemWindowType, itemSlotIndex)
				del self.itemStock[privatePos]

		price = int(self.priceInputBoard.GetText())

		if IsPrivateShopItemPriceList():
			SetPrivateShopItemPrice(self.priceInputBoard.itemVNum, price)

		shop.AddPrivateShopItemStock(attachedInvenType, sourceSlotPos, targetSlotPos, price)
		self.itemStock[targetSlotPos] = (attachedInvenType, sourceSlotPos)

		self.Refresh()

		#####

		self.priceInputBoard = None
		return True

	def CancelInputPrice(self):

		if self.priceInputBoard:
			self.priceInputBoard.Close()
		self.priceInputBoard = None
		return 1

	def OnOk(self):

		if not self.nameLine.GetText():
			return

		if 0 == len(self.itemStock):
			return

		if app.ENABLE_OFFLINE_SHOP:
			shop.BuildPrivateShop(self.nameLine.GetText(), True, self.wndDecoration.GetDecorationSelect())
		else:
			shop.BuildPrivateShop(self.nameLine.GetText())
		self.Close()

	def OnClose(self):
		self.Close()

	def OnPressEscapeKey(self):
		self.Close()
		return True

	def OnOverInItem(self, slotIndex):

		if self.tooltipItem:
			if self.itemStock.has_key(slotIndex):
				self.tooltipItem.SetPrivateShopBuilderItem(*self.itemStock[slotIndex] + (slotIndex,))

	def OnOverOutItem(self):

		if self.tooltipItem:
			self.tooltipItem.HideToolTip()
def Clear():
	global g_itemPriceDict
	global g_isBuildingPrivateShop
	g_itemPriceDict={}
	g_isBuildingPrivateShop = False

def IsPrivateShopItemPriceList():
	global g_itemPriceDict
	if g_itemPriceDict:
		return True
	else:
		return False

def IsBuildingPrivateShop():
	global g_isBuildingPrivateShop
	if player.IsOpenPrivateShop() or g_isBuildingPrivateShop:
		return True
	else:
		return False

def SetPrivateShopItemPrice(itemVNum, itemPrice):
	global g_itemPriceDict
	g_itemPriceDict[int(itemVNum)]=itemPrice

def GetPrivateShopItemPrice(itemVNum):
	try:
		global g_itemPriceDict
		return g_itemPriceDict[itemVNum]
	except KeyError:
		return 0

def UpdateADBoard(status = 1):	
	for key in g_privateShopAdvertisementBoardDict.keys():
		if status:
			g_privateShopAdvertisementBoardDict[key].Show()
		else:
			g_privateShopAdvertisementBoardDict[key].Hide()
		

def DeleteADBoard(vid):
	if not g_privateShopAdvertisementBoardDict.has_key(vid):
		return

	del g_privateShopAdvertisementBoardDict[vid]


class PrivateShopAdvertisementBoard(ui.ThinBoard):
	def __init__(self):
		ui.ThinBoard.__init__(self, "UI_BOTTOM")
		self.shopAdvertismentBoardSeen =[]
		self.vid = None
		self.__MakeTextLine()

	def __del__(self):
		ui.ThinBoard.__del__(self)

	def __MakeTextLine(self):
		self.textLine = ui.TextLine()
		self.textLine.SetParent(self)
		self.textLine.SetWindowHorizontalAlignCenter()
		self.textLine.SetWindowVerticalAlignCenter()
		self.textLine.SetHorizontalAlignCenter()
		self.textLine.SetVerticalAlignCenter()
		self.textLine.Show()

	def Open(self, vid, text):
		self.vid = vid

		self.textLine.SetText(text)
		if vid in self.shopAdvertismentBoardSeen:
			self.textLine.SetFontColor(1.0, 0.5, 0.1)
		self.textLine.UpdateRect()
		self.SetSize(len(text)*6 + 10*2, 20)
		self.Show()

		g_privateShopAdvertisementBoardDict[vid] = self

	def OnMouseLeftButtonUp(self):
		if not self.vid:
			return
		net.SendOnClickPacket(self.vid)

		if self.vid != player.GetMainCharacterIndex():
			self.textLine.SetFontColor(1.0, 0.5, 0.1)
			self.shopAdvertismentBoardSeen.append(self.vid)

		return True

	def OnUpdate(self):
		if not self.vid:
			return

		if systemSetting.IsShowSalesText():
			self.Show()
			x, y = chr.GetProjectPosition(self.vid, 220)
			self.SetPosition(x - self.GetWidth()/2, y - self.GetHeight()/2)

		else:
			for key in g_privateShopAdvertisementBoardDict.keys():
				if  player.GetMainCharacterIndex() == key:
					g_privateShopAdvertisementBoardDict[key].Show()
					x, y = chr.GetProjectPosition(player.GetMainCharacterIndex(), 220)
					g_privateShopAdvertisementBoardDict[key].SetPosition(x - self.GetWidth()/2, y - self.GetHeight()/2)
				else:
					g_privateShopAdvertisementBoardDict[key].Hide()

