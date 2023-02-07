import thenewui as ui
import CacheEffect as player
import mouseModule
import net
import app
import item
import chat
import grp
import uiScriptLocale
import uiCommon
import localeInfo
import event
import ime
import uiToolTip
import wndMgr

Y_NORMAL = 300 - 7
Y_THIN_NORMAL = 257

TIME_CHANGE_ANIM = 0.02

class ChestViewWindow(ui.ScriptWindow):
	def __init__(self):
		ui.ScriptWindow.__init__(self)
		self.bIsLoaded = False
		self.tooltipItem = None
		
		self.dictItems = {}
		self.__LoadWindow()

	def __del__(self):
		self.dictItems = {}
		ui.ScriptWindow.__del__(self)

	def SetItemToolTip(self, tooltip):
		self.tooltipItem = tooltip

	def __LoadWindow(self):
		if self.bIsLoaded:
			return
		
		self.bIsLoaded = True
		
		self.AddFlag("movable")
		self.AddFlag("animation")
	
		self.Board = ui.BoardWithTitleBar()
		self.Board.SetParent(self)
		self.Board.SetSize(380 + 215, Y_NORMAL)
		self.Board.SetTitleName("Fereastra Vizualizare Drop Cufar")
		self.Board.Show()

		self.titleBar = ui.TitleBar()
		self.titleBar.SetParent(self.Board)
		self.titleBar.MakeTitleBar(0, "red")
		self.titleBar.SetPosition(8, 7)
		self.titleBar.SetWidth((380 + 215) - 15)
		self.titleBar.SetCloseEvent(ui.__mem_func__(self.Close))
		self.titleBar.Show()

		self.titleName = ui.TextLine()
		self.titleName.SetParent(self.titleBar)
		self.titleName.SetPosition(0, 4)
		self.titleName.SetText("Vizualizare Drop")
		self.titleName.SetWindowHorizontalAlignCenter()
		self.titleName.SetHorizontalAlignCenter()
		self.titleName.Show()

		self.infobtn = ui.Button()
		self.infobtn.SetParent(self.Board)
		self.infobtn.SetUpVisual("d:/ymir work/ui/pattern_renewal/mob_info_01.tga")
		self.infobtn.SetOverVisual("d:/ymir work/ui/pattern_renewal/mob_info_02.tga")
		self.infobtn.SetDownVisual("d:/ymir work/ui/pattern_renewal/mob_info_03.tga")
		self.infobtn.SetPosition(330 + 215, 9)
		self.infobtn.Show()

		# self.ThinBoard = ui.MakeThinBoardCircle(self.Board, 7, 34, 365 + 215, Y_THIN_NORMAL, False)
		# self.HorizontalBar = ui.MakeHorizontalBar(self.Board, 14, 41, 351 + 215, "Vizualizare Obiecte")

		self.SetSize(self.Board.GetWidth(), self.Board.GetHeight())
		
		self.CreateDesign()
		
	def CreateDesign(self):
		self.ThinBoardItems = ui.MakeBrownBoard(self.Board, 15, 70 + 65, 347 + 215, 150, False)
		self.ThinBoardLeft = ui.MakeBrownBoard(self.Board, 15, 70 + 65, 25, 150, False)
		self.ThinBoardRight = ui.MakeBrownBoard(self.Board, 554, 70 + 65, 25, 150, False)
		# TO DO TEXTLINE INSTAED OF MAKEBROWNBOARD IN DICTBOARDITEMS
		self.btnLeft = ui.Button()
		self.btnLeft.SetParent(self.ThinBoardLeft)
		self.btnLeft.SetUpVisual("d:/ymir work/ui/pagination/btn_prev_default.dds")
		self.btnLeft.SetOverVisual("d:/ymir work/ui/pagination/btn_prev_hover.dds")
		self.btnLeft.SetDownVisual("d:/ymir work/ui/pagination/btn_prev_down.dds")
		self.btnLeft.SetPosition(7, 75)
		self.btnLeft.SetEvent(ui.__mem_func__(self.OnPrev))
		self.btnLeft.Show()
		
		self.btnRight = ui.Button()
		self.btnRight.SetParent(self.ThinBoardRight)
		self.btnRight.SetUpVisual("d:/ymir work/ui/pagination/btn_next_default.dds")
		self.btnRight.SetOverVisual("d:/ymir work/ui/pagination/btn_next_hover.dds")
		self.btnRight.SetDownVisual("d:/ymir work/ui/pagination/btn_next_down.dds")
		self.btnRight.SetPosition(7, 75)
		self.btnRight.SetEvent(ui.__mem_func__(self.OnNext))
		self.btnRight.Show()
		
		self.dictBoardItems = {}
		
		self.dictBoardItems[0] = ui.MakeBrownBoard(self.Board, 39, 70 + 65, 130, 150, False)
		self.dictBoardItems[1] = ui.MakeBrownBoard(self.Board, 167, 70 + 65, 130, 150, False)
		self.dictBoardItems[2] = ui.MakeBrownBoard(self.Board, 296, 70 + 65, 130, 150, False)
		self.dictBoardItems[3] = ui.MakeBrownBoard(self.Board, 425, 70 + 65, 130, 150, False)
		
		self.dictViewItems = {}
		
		for x in xrange(4):
			self.dictViewItems[x] = ui.GridSlotWindow()
			self.dictViewItems[x].ArrangeSlot(0, 1, 1, 32, 96, 0, 0)
			self.dictViewItems[x].SetSlotStyle(wndMgr.SLOT_STYLE_NONE)
			self.dictViewItems[x].SetParent(self.dictBoardItems[x])
			self.dictViewItems[x].SetOverInItemEvent(ui.__mem_func__(self.OverInItem))
			self.dictViewItems[x].SetOverOutItemEvent(ui.__mem_func__(self.OverOutItem))
			self.dictViewItems[x].SetSlotBaseImage("d:/ymir work/ui/game/comp/slot.png", 1.0, 1.0, 1.0, 1.0)
			self.dictViewItems[x].Show()

		self.ThinBoardItemsName = ui.MakeBrownBoard(self.Board, 39, 70 + 185, 347 + 169, 30, False)

		self.ThinBoardSplitN1 = ui.MakeBrownBoard(self.Board, 167, 70 + 185, 130, 30, False)
		self.ThinBoardSplitN2 = ui.MakeBrownBoard(self.Board, 296, 70 + 185, 130, 30, False)
		
		self.dictTextRarity = {}
		
		for x in xrange(4):
			self.dictTextRarity[x] = ui.MakeText(self.Board, False, 100 + 130 * x, 70 + 200)
			self.dictTextRarity[x].SetVerticalAlignCenter()
			self.dictTextRarity[x].SetHorizontalAlignCenter()
	
		self.wndSlider = ui.SliderBar()
		self.wndSlider.SetParent(self)
		self.wndSlider.SetPosition(200, 115)
		self.wndSlider.SetEvent(ui.__mem_func__(self.OnSliderMove))
		self.wndSlider.Show()

		self.btnOpen = ui.Button()
		self.btnOpen.SetParent(self.Board)
		self.btnOpen.SetUpVisual("d:/ymir work/ui/minigame/yutnori/yut_throw_button_default.sub")
		self.btnOpen.SetOverVisual("d:/ymir work/ui/minigame/yutnori/yut_throw_button_over.sub")
		self.btnOpen.SetDownVisual("d:/ymir work/ui/minigame/yutnori/yut_throw_button_down.sub")
		self.btnOpen.SetPosition(230, 83)
		self.btnOpen.SetEvent(ui.__mem_func__(self.OnClickOpenChest))
		self.btnOpen.Show()

		# self.ThinBoardChest = ui.MakeThinBoardCircle(self.Board, 13, 218, 58, 69, False)
		# self.HorizontalBarChest = ui.MakeHorizontalBar(self.Board, 15, 220, 55, "Cufar")

		self.ItemSlot = ui.GridSlotWindow()
		self.ItemSlot.SetParent(self.Board)
		self.ItemSlot.SetPosition(270, 40)
		self.ItemSlot.ArrangeSlot(0, 1, 1, 32, 32, 0, 0)
		self.ItemSlot.SetSlotStyle(wndMgr.SLOT_STYLE_NONE)
		self.ItemSlot.SetSlotBaseImage("d:/ymir work/ui/game/comp/slot.png", 1.0, 1.0, 1.0, 1.0)
		self.ItemSlot.Show()

	def Show(self):
		self.SetCenterPosition()
		ui.ScriptWindow.Show(self)

	def OnPrev(self):
		if self.currentIdx - 1 < 0:
			return

		self.RefreshItems(self.currentChest, self.currentIdx - 1)	

	def OnNext(self):
		if self.currentIdx + 1 > len(self.dictItems[self.currentChest]) - 4:
			return

		self.RefreshItems(self.currentChest, self.currentIdx + 1)

	def OnRunMouseWheel(self, nLen):
		self.OverOutItem()
		if nLen > 0:
			self.OnNext()
		else:
			self.OnPrev()
		
		return True

	def OnSliderMove(self):
		SliderPos = int(self.wndSlider.GetSliderPos() * 20)
		if SliderPos == 0:
			SliderPos = 1

		self.btnOpen.SetText(uiScriptLocale.CHEST_OPEN_COUNT % SliderPos)
		self.openAmount = SliderPos

	def OnClickOpenChest(self):
		if self.invItemPos == -1:
			return

		itemCount = player.GetItemCount(self.invItemPos)

		for i in xrange(self.openAmount):
			if itemCount == 1:
				net.SendItemUsePacket(self.invItemPos)
				self.OnPressEscapeKey()
				break
		
			net.SendItemUsePacket(self.invItemPos)
			itemCount = itemCount - 1
		
	def __ToolTipText(self):
		tooltipItem = uiToolTip.ItemToolTip()
		tooltipItem.SetTitle("Informatie")
		
		tooltipItem.AppendTextLine("Foloseste rotita pentru a schimba obiectele")
		tooltipItem.AppendSpace(3)
		tooltipItem.AppendTextLine("mai rapid!")
		tooltipItem.UpdateRect()
		tooltipItem.Hide()
		return tooltipItem

	def AddChestDropItem(self, chestVnum, slotIndex, dropChance, itemVnum, itemCount):
		if not self.dictItems.has_key(chestVnum):
			self.dictItems[chestVnum] = {}

		self.dictItems[chestVnum][slotIndex] = [itemVnum, itemCount, dropChance]

	def RefreshItems(self, chestVnum, StartIndex = 0):
		if chestVnum:
			self.currentChest = chestVnum

		if not self.dictItems.has_key(self.currentChest):
			chat.AppendChat(chat.CHAT_TYPE_INFO, "Acest cufar nu are drop")
			self.Close()
			return
		
		if StartIndex != -1:
			for x in xrange(4):
				self.dictViewItems[x].Hide()
				self.dictBoardItems[x].SetText("")
				self.dictTextRarity[x].SetText("")
		
		cnt = 0
		idx = 0
		for key, value in self.dictItems[self.currentChest].iteritems():
			if StartIndex != 0:
				if cnt < StartIndex:
					cnt += 1
					continue
					
			if idx > 3:
				break
		
			itemVnum = value[0]
			itemCount = value[1]
			itemChance = value[2]

			if itemCount <= 1:
				itemCount = 0

			item.SelectItem(itemVnum)
			_, ItemSize = item.GetItemSize()
			
			self.dictViewItems[idx].SetItemSlotVnum(0, itemVnum, itemCount)
			
			self.itemName = item.GetItemName()
			max_len = 28
			if len(self.itemName) > max_len:
				self.itemName = self.itemName[:max_len-3] + "..."

			
			self.dictBoardItems[idx].SetText(self.itemName)
			self.dictBoardItems[idx].ButtonText.SetPosition(64, 110)

			if ItemSize == 1:
				self.dictViewItems[idx].SetPosition(50, 50)
			elif ItemSize == 2:
				self.dictViewItems[idx].SetPosition(50, 27)
			elif ItemSize == 3:
				self.dictViewItems[idx].SetPosition(50, 13)

			self.dictViewItems[idx].Show()

			################# CHANCE_ITEM #################
			if itemChance == 0:
				self.dictTextRarity[idx].SetText("Comun")
			elif itemChance < 100 and itemChance > 89:
				self.dictTextRarity[idx].SetText("Comun")
			elif itemChance <= 89 and itemChance > 69:
				self.dictTextRarity[idx].SetText("|cff00ff00Normal")
			elif itemChance <= 69 and itemChance > 50:
				self.dictTextRarity[idx].SetText("|cff00ffffRar")
			elif itemChance <= 50 and itemChance > 39:
				self.dictTextRarity[idx].SetText("|cFFFFA500Foarte Rar")
			elif itemChance <= 39 and itemChance > 2:
				self.dictTextRarity[idx].SetText("|cFF9370DBMitic")
			elif itemChance <= 2 and itemChance >= 0:
				self.dictTextRarity[idx].SetText("|cffffcc00BLegendar")
			else:
				self.dictTextRarity[idx].SetText("Comun")
			################# CHANCE_ITEM #################

			cnt += 1
			idx += 1
			
		self.currentIdx = StartIndex

	def OverInItem(self, index, itemVnum = 0):
		if mouseModule.mouseController.isAttached():
			return
			
		if self.tooltipItem and itemVnum:
			self.tooltipItem.SetItemToolTip(itemVnum)

	def OverOutItem(self):
		if self.tooltipItem:
			self.tooltipItem.HideToolTip()

	def Open(self, invItemPos):
		self.SetCenterPosition()
		self.SetTop()
		self.wndSlider.SetSliderPos(0.0)
		self.OnSliderMove()
		
		self.currentChest = -1
		self.currentIdx = 0
		self.openAmount = 1
		self.invItemPos = invItemPos

		for x in xrange(4):
			self.dictViewItems[x].Hide()
			self.dictBoardItems[x].SetText("")
			self.dictTextRarity[x].SetText("")

		itemVnum = player.GetItemIndex(invItemPos)
		itemCount = player.GetItemCount(invItemPos)		
		self.ItemSlot.SetItemSlot(0, itemVnum, itemCount)
		
		self.infobtn.SetToolTipWindow(self.__ToolTipText(), False)
		self.Show()

	def Destroy(self):
		self.ClearDictionary()
		
		self.dictItems = {}
		self.dictViewItems = {}
		self.tooltipItem = None
	
	def Close(self):
		self.dictItems = {}
		self.OverOutItem()
		self.Hide()
		
	def OnPressEscapeKey(self):
		self.Close()
		return True
