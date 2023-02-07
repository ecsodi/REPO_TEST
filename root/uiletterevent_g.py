# Development By Grimm @ 2021

import thenewui as ui
import item
import net
import constInfo
import localeInfo
import uiCommon
import wndMgr
import app
import grp
import chat
import CacheEffect as player
import skill
import shop
import chr
import math
from _weakref import proxy
import uiToolTip
import ime
import cfg

class LetterEventWindow(ui.ScriptWindow):
	def __init__(self):
		ui.ScriptWindow.__init__(self)
		self.bLoaded = 0
		self.bLoadedInfo = False
		self.tooltipItem = None
		self.dictItemsLetter = {}
		self.dictItems = {}
		self.ImageSeparator = {}
		self.LoadWindow()

	def __del__(self):
		ui.ScriptWindow.__del__(self)

	def Show(self):
		self.SetCenterPosition()
		ui.ScriptWindow.Show(self)
		
		if self.bLoadedInfo == False:
			net.SendChatPacket("/letter_open")
	
	def LoadWindow(self):
		if self.bLoaded == 1:
			return

		self.bLoaded = 1
		
		self.AddFlag("float")
		self.AddFlag("movable")
		self.AddFlag("animation")
		
		self.Board = ui.BoardWithTitleBar()
		self.Board.SetParent(self)
		self.Board.SetSize(350, 440-32)
		self.Board.AddFlag("not_pick")
		self.Board.SetTitleName(localeInfo.EVENT_LETTER_TITLE)
		self.Board.SetCloseEvent(ui.__mem_func__(self.Close))

		self.Board.Show()

		self.SetSize(self.Board.GetWidth(), self.Board.GetHeight())

		for i in xrange(3):
			self.ImageSeparator[i] = ui.ImageBox()
			self.ImageSeparator[i].SetParent(self.Board)
			self.ImageSeparator[i].SetPosition(0, 0)
			self.ImageSeparator[i].LoadImage("d:/ymir work/ui/game/seperator.tga")
			self.ImageSeparator[i].SetWindowHorizontalAlignCenter()
			self.ImageSeparator[i].Show()
			
		self.ImageSeparator[0].SetPosition(0, 148)
		self.ImageSeparator[1].SetPosition(0, 188)
		self.ImageSeparator[2].SetPosition(0, 335-32)

		self.BannerImage = ui.ImageBox()
		self.BannerImage.SetParent(self.Board)
		self.BannerImage.SetPosition(7, 30)
		self.BannerImage.LoadImage("d:/ymir work/ui/game/letter_event/letter_event.tga")
		self.BannerImage.Show()

		self.LetterInfo = ui.TextLine()
		self.LetterInfo.SetParent(self.Board)
		self.LetterInfo.SetPosition(20, 361-32)
		self.LetterInfo.SetText(localeInfo.EVENT_LETTER_TEXT)
		# self.LetterInfo.SetWidth(300)

		self.LetterInfo.Show()

		self.LetterItemSlot = ui.GridSlotWindow()
		self.LetterItemSlot.SetParent(self.Board)
		self.LetterItemSlot.SetPosition(77, 176)
		self.LetterItemSlot.ArrangeSlot(0, 6, 1, 32, 32, 0, 0)		
		self.LetterItemSlot.SetSlotBaseImage("d:/ymir work/ui/public/Slot_Base.sub", 1.0, 1.0, 1.0, 1.0)
		self.LetterItemSlot.SetOverInItemEvent(ui.__mem_func__(self.OverInItemLetter))
		self.LetterItemSlot.SetOverOutItemEvent(ui.__mem_func__(self.OverOutToolTip))
		self.LetterItemSlot.Show()

		# self.btnDelivery = ui.MakeButton(self.Board, 0, 405-27, False, "d:/ymir work/ui/game/myshop_deco/", "select_btn_01.sub", "select_btn_02.sub", "select_btn_03.sub")
		self.btnDelivery = ui.MakeButton(self.Board, 0, 405-27, False, "d:/ymir work/ui/public/", "AcceptButton00.sub", "AcceptButton01.sub", "AcceptButton02.sub")
		# self.btnDelivery.SetText("|cFFFEE3AE|H|hTrimite Litere")
		self.btnDelivery.SetWindowHorizontalAlignCenter()
		self.btnDelivery.SetEvent(ui.__mem_func__(self.DoDelivery))

		self.RewardItemSlot = ui.GridSlotWindow()
		self.RewardItemSlot.SetParent(self.Board)
		self.RewardItemSlot.SetPosition(50, 225)
		self.RewardItemSlot.ArrangeSlot(0, 8, 3, 32, 32, 0, 0)
		self.RewardItemSlot.SetSlotBaseImage("d:/ymir work/ui/public/Slot_Base.sub", 1.0, 1.0, 1.0, 1.0)
		self.RewardItemSlot.SetOverInItemEvent(ui.__mem_func__(self.OverInItem))
		self.RewardItemSlot.SetOverOutItemEvent(ui.__mem_func__(self.OverOutToolTip))
		self.RewardItemSlot.Show()

	def DoDelivery(self):
		net.SendChatPacket("/letter_delivery")

	def SetLetter(self, Index, Vnum, Count):
		self.LetterItemSlot.SetItemSlot(Index, Vnum, Count)

		self.dictItemsLetter[Index] = Vnum
		
		self.bLoadedInfo = True
		
		# self.ThinDelivery.SetWindowHorizontalAlignCenter()
		# self.ThinBoardALetters.SetWindowHorizontalAlignCenter()
	
	def SetReward(self, Index, Vnum, Count):
		self.RewardItemSlot.SetItemSlot(Index, Vnum, Count)
		self.dictItems[Index] = Vnum

	def OverInItemLetter(self, slotIndex):
		if len(self.dictItemsLetter) == 0:
			return
		
		if self.tooltipItem and not slotIndex > len(self.dictItemsLetter):
			self.tooltipItem.SetItemToolTip(self.dictItemsLetter[slotIndex])
	
	def OverInItem(self, slotIndex):
		if len(self.dictItems) == 0:
			return
		
		if self.tooltipItem and not slotIndex > len(self.dictItems):
			self.tooltipItem.SetItemToolTip(self.dictItems[slotIndex])

	def OverOutToolTip(self):
		if self.tooltipItem:
			self.tooltipItem.HideToolTip()

	def SetItemToolTip(self, tooltip):
		self.tooltipItem = tooltip
	
	def Destroy(self):
		self.dictItemsLetter = {}
		self.dictItems = {}
		self.tooltipItem = None
		self.ClearDictionary()
	
	def Close(self):
		if self.tooltipItem:
			self.tooltipItem.HideToolTip()
		
		self.Hide()
	
	def OnPressEscapeKey(self):		
		self.Close()
		return True	
