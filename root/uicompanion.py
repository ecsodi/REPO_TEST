# Development by @Grimm

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
import constInfo
import ime
import uiToolTip
import wndMgr
import cfg

COMPANION_SOCKET_LEVEL		= 0
COMPANION_SOCKET_EXP		= 1
COMPANION_SOCKET_TIME		= 2

COMPANION_PROGRESS_BONUS1	= 3
COMPANION_PROGRESS_BONUS2	= 4

COMPANION_SKILL_1			= 5
COMPANION_SKILL_2			= 6
COMPANION_SKILL_3			= 7

TYPE_SKILLS = {
	63 : { "ICON"		: "d:/ymir work/ui/skill/pet/mob_bonus.sub",},
	78 : { "ICON"		: "d:/ymir work/ui/skill/pet/jijoong.sub",},
	79 : { "ICON"		: "d:/ymir work/ui/skill/pet/jijoong.sub",},
	80 : { "ICON"		: "d:/ymir work/ui/skill/pet/jijoong.sub",},
	81 : { "ICON"		: "d:/ymir work/ui/skill/pet/jijoong.sub",},
	86 : { "ICON"		: "d:/ymir work/ui/skill/pet/pacheon.sub",},
	71 : { "ICON"		: "d:/ymir work/ui/skill/pet/banya.sub",},
	16 : { "ICON"		: "d:/ymir work/ui/skill/pet/choehoenbimu.sub",},
	47 : { "ICON"		: "d:/ymir work/ui/skill/pet/stealhp.sub",},
	23 : { "ICON"		: "d:/ymir work/ui/skill/pet/stealmp.sub",},
	24 : { "ICON"		: "d:/ymir work/ui/skill/pet/block.sub",},
	27 : { "ICON"		: "d:/ymir work/ui/skill/pet/reflect_melee.sub",},
	39 : { "ICON"		: "d:/ymir work/ui/skill/pet/gold_drop.sub",},
	44 : { "ICON"		: "d:/ymir work/ui/skill/pet/bow_distance.sub",},
	43 : { "ICON"		: "d:/ymir work/ui/skill/pet/exp.sub",},
}

## SET_EVOLVE_NEED_ITEM
DICT_EVOLVE_ITEMS = {
	0 : {
		0	: [55003, 10],
		1	: [1, 5000000],
	},
	
	1 : {
		0	: [55004, 10],
		1	: [1, 7000000],
	},
	
	2 : {
		0	: [55005, 10],
		1	: [1, 20000000],
	},
}
## SET_EVOLVE_NEED_ITEM

COMPANION_MAX_TIME = 432000 ## SECONDS

class CompanionWindow(ui.ScriptWindow):
	class TextToolTip(ui.Window):
		def __init__(self, y):
			ui.Window.__init__(self, "TOP_MOST")

			textLine = ui.TextLine()
			textLine.SetParent(self)
			textLine.SetHorizontalAlignLeft()
			textLine.SetOutline()
			textLine.Show()
			self.y = y
			self.textLine = textLine

		def __del__(self):
			ui.Window.__del__(self)

		def SetText(self, text):
			self.textLine.SetText(text)

		def OnRender(self):
			(mouseX, mouseY) = wndMgr.GetMousePosition()
			self.textLine.SetPosition(mouseX, mouseY - 60 + self.y)

	def __init__(self):
		ui.ScriptWindow.__init__(self)

		self.bIsLoaded = False
		self.PetIsActive = False

		self.interface = None
		self.tooltipItem = uiToolTip.ItemToolTip()
		self.tooltipItem.HideToolTip()

		self.QuestionDialog = None
		self.SlotPosCompanion = 0
		self.NextExp = 1
		
		self.ToolTipExp = None
		self.ToolTipExp2 = None
		
		# COMPANION_GAME_INFO
		self.wndInfoCompanion = uiCommon.CompanionInfo()
		self.wndInfoCompanion.Hide()
		
		self.__LoadWindow()

	def SetItemToolTip(self, tooltip):
		self.tooltipItem = tooltip
	
	def __del__(self):
		ui.ScriptWindow.__del__(self)

		if self.wndInfoCompanion:
			self.wndInfoCompanion.Hide()
			self.wndInfoCompanion.Destroy()
			self.wndInfoCompanion = None

		if self.ToolTipExp:
			self.ToolTipExp.Hide()
			self.ToolTipExp = None

		if self.ToolTipExp2:
			self.ToolTipExp2.Hide()
			self.ToolTipExp2 = None
		
		if self.tooltipItem:
			self.tooltipItem.HideToolTip()
			self.tooltipItem = None

	def __LoadWindow(self):
		if self.bIsLoaded:
			return
		
		self.bIsLoaded = True
		self.AddFlag("movable")
	
		self.Board = ui.ExpandedImageBox()
		self.Board.SetParent(self)
		self.Board.LoadImage("d:/ymir work/ui/pet/pet_ui_bg.tga")
		self.Board.AddFlag("not_pick")
		self.Board.Show()

		self.SetSize(self.Board.GetWidth(), self.Board.GetHeight())
		
		self.TitleBar = ui.TitleBar()
		self.TitleBar.SetParent(self)
		self.TitleBar.MakeTitleBar(265, "red")
		self.TitleBar.SetPosition(5, 3)
		self.TitleBar.SetCloseEvent(ui.__mem_func__(self.Close))
		self.TitleBar.Show()
		
		self.wndInfoPet = {}

		for x in xrange(0, 2):
			self.wndInfoPet[x] = ui.MakeText(self, False, 50, 47)
			self.wndInfoPet[x].Hide()

		self.wndBonus = {}
		
		self.wndBonus[0] = ui.MakeText(self, False, 65, 197)
		self.wndBonus[0].SetWindowHorizontalAlignCenter()
		self.wndBonus[0].SetHorizontalAlignCenter()
		
		self.wndBonus[1] = ui.MakeText(self, False, 65, 197 + 23)
		self.wndBonus[1].SetWindowHorizontalAlignCenter()
		self.wndBonus[1].SetHorizontalAlignCenter()

		self.wndBonus[2] = ui.MakeText(self, False, 65, 197 + 23 + 21)
		self.wndBonus[2].SetWindowHorizontalAlignCenter()
		self.wndBonus[2].SetHorizontalAlignCenter()
		
		self.wndTitleName = ui.MakeText(self.TitleBar, localeInfo.PET_TEXT_3, 0, 3)
		self.wndTitleName.SetWindowHorizontalAlignCenter()
		self.wndTitleName.SetHorizontalAlignCenter()
		self.wndTitleName.Show()

		self.btnEvolve = ui.MakeButton(self, 165, 130, False, "d:/ymir work/ui/public/", "large_button_01.sub", "large_button_02.sub", "large_button_03.sub")
		self.btnEvolve.SetText(localeInfo.PET_TEXT_4)
		self.btnEvolve.SetEvent(ui.__mem_func__(self.ShowEvolve))

		self.btnChangeName = ui.MakeButton(self, 165, 153, False, "d:/ymir work/ui/public/", "large_button_01.sub", "large_button_02.sub", "large_button_03.sub")
		self.btnChangeName.SetText(localeInfo.PET_TEXT_5)
		self.btnChangeName.SetEvent(ui.__mem_func__(self.DoRefillTime))
		
		self.dictImageSkill = []
		for x in xrange(2):
			Image = ui.ExpandedImageBox()
			Image.SetParent(self)
			Image.SetPosition(143 + x * 41, 35)
			Image.LoadImage("d:/ymir work/ui/game/normal_interface/offlineshop_locked_hover.png")
			if x == 0:
				Image.OnMouseOverIn = ui.__mem_func__(self.__OverInSkill1)
				Image.OnMouseLeftButtonDown = ui.__mem_func__(self.__ResetAbility1)
			elif x == 1:
				Image.OnMouseOverIn = ui.__mem_func__(self.__OverInSkill2)
				Image.OnMouseLeftButtonDown = ui.__mem_func__(self.__ResetAbility2)
			elif x == 2:
				Image.OnMouseOverIn = ui.__mem_func__(self.__OverInSkill3)
			Image.OnMouseOverOut = ui.__mem_func__(self.OverOutToolTip)
			Image.Show()
			
			self.dictImageSkill.append(Image)
		
		self.CreateDesignText()
		self.CreateEvolvePage()

	def __ResetAbility1(self):
		if self.QuestionDialog:
			return
		
		attrSlot = player.GetItemAttribute(player.INVENTORY, self.SlotPosCompanion, COMPANION_SKILL_1)
		
		if attrSlot == 0:
			return
		
		type = attrSlot[0]
		value = attrSlot[1]
		
		if type == 0 or value == 0:
			return
		
		affectString = uiToolTip.AFFECT_DICT[type](value)
		affectString = self.SplitStringBonus(affectString, 0)
		
		if not affectString:
			return
		
		QuestionDialog = uiCommon.QuestionDialog()
		QuestionDialog.SetText(localeInfo.PET_TEXT_6 % (affectString))
		QuestionDialog.SetAcceptEvent(ui.__mem_func__(self.OnResetAbility))
		QuestionDialog.SetCancelEvent(ui.__mem_func__(self.OnCloseQuestionDialog))
		QuestionDialog.Open()
		self.QuestionDialog = QuestionDialog
		self.QuestionDialog.SetWidth(380)
		self.QuestionDialog.index = 5
		
		constInfo.SET_ITEM_QUESTION_DIALOG_STATUS(1)
	
	def __ResetAbility2(self):
		if self.QuestionDialog:
			return
		
		attrSlot = player.GetItemAttribute(player.INVENTORY, self.SlotPosCompanion, COMPANION_SKILL_2)
		
		if attrSlot == 0:
			return
		
		type = attrSlot[0]
		value = attrSlot[1]
		
		if type == 0 or value == 0:
			return
		
		affectString = uiToolTip.AFFECT_DICT[type](value)
		affectString = self.SplitStringBonus(affectString, 0)
		
		if not affectString:
			return
		
		QuestionDialog = uiCommon.QuestionDialog()
		QuestionDialog.SetText(localeInfo.PET_TEXT_6 % (affectString))
		QuestionDialog.SetAcceptEvent(ui.__mem_func__(self.OnResetAbility))
		QuestionDialog.SetCancelEvent(ui.__mem_func__(self.OnCloseQuestionDialog))
		QuestionDialog.Open()
		self.QuestionDialog = QuestionDialog
		self.QuestionDialog.SetWidth(350)
		self.QuestionDialog.index = 6
		
		constInfo.SET_ITEM_QUESTION_DIALOG_STATUS(1)
	
	def OnResetAbility(self):
		if not self.QuestionDialog:
			return True

		index = self.QuestionDialog.index

		net.SendChatPacket("/reset_ability_companion %d" % (index))
		
		constInfo.SET_ITEM_QUESTION_DIALOG_STATUS(0)
		self.OnCloseQuestionDialog()
		return True
	
	def OnCloseQuestionDialog(self):
		if not self.QuestionDialog:
			return
			
		self.QuestionDialog.Close()
		self.QuestionDialog = None
		constInfo.SET_ITEM_QUESTION_DIALOG_STATUS(0)	
	
	def DoRefillTime(self):
		net.SendChatPacket("/refill_companion")

	def DoEvolve(self):
		net.SendChatPacket("/evolve_companion")
	
	def SplitStringBonus(self, text, IsGetVal):
		txtNr = ""
		for index in xrange(len(text)):
			txt = text[index]
			
			if txt.isdigit():
				if IsGetVal:
					txtNr += txt
				else:
					return text[:index]
		
		if IsGetVal:
			return txtNr
			
		return text
	
	def __OverInSkill1(self):
		if self.tooltipItem:
			attrSlot = player.GetItemAttribute(player.INVENTORY, self.SlotPosCompanion, COMPANION_SKILL_1)

			self.tooltipItem.ClearToolTip()
			self.tooltipItem.SetTitle(localeInfo.PET_TEXT_7)
			# self.tooltipItem.SetThinBoardSize(300, 50)

			if attrSlot != 0:
				type = attrSlot[0]
				value = attrSlot[1]
				
				if type == 0 or value == 0:
					if player.GetItemTransmutation(player.INVENTORY, self.SlotPosCompanion) == 3:
						self.tooltipItem.AppendDescription(localeInfo.PET_TEXT_8, 26)
					else:
						self.tooltipItem.AppendDescription(localeInfo.PET_TEXT_9, 26)
				else:
					affectString = uiToolTip.AFFECT_DICT[type](value)
					affectString = self.SplitStringBonus(affectString, 0)
					if affectString:
						value = float(value) / 10
						self.tooltipItem.AppendDescription(affectString + str(value), 26)
			else:
				self.tooltipItem.AppendDescription(localeInfo.PET_TEXT_9, 26)
				
			self.tooltipItem.ShowToolTip()

	def __OverInSkill2(self):
		if self.tooltipItem:
			attrSlot = player.GetItemAttribute(player.INVENTORY, self.SlotPosCompanion, COMPANION_SKILL_2)

			self.tooltipItem.ClearToolTip()
			self.tooltipItem.SetTitle(localeInfo.PET_TEXT_12)

			if attrSlot != 0:
				type = attrSlot[0]
				value = attrSlot[1]
				
				if type == 0 or value == 0:
					if player.GetItemTransmutation(player.INVENTORY, self.SlotPosCompanion) == 3:
						self.tooltipItem.AppendDescription(localeInfo.PET_TEXT_8, 26)
					else:
						self.tooltipItem.AppendDescription(localeInfo.PET_TEXT_9, 26)
				else:
					affectString = uiToolTip.AFFECT_DICT[type](value)
					affectString = self.SplitStringBonus(affectString, 0)
					if affectString:
						value = float(value) / 10
						self.tooltipItem.AppendDescription(affectString + str(value), 26)
			else:
				self.tooltipItem.AppendDescription(localeInfo.PET_TEXT_9, 26)
				
			self.tooltipItem.ShowToolTip()
			
	def __OverInSkill3(self):
		if self.tooltipItem:
			attrSlot = player.GetItemAttribute(player.INVENTORY, self.SlotPosCompanion, COMPANION_SKILL_3)

			self.tooltipItem.ClearToolTip()
			self.tooltipItem.SetTitle(localeInfo.PET_TEXT_13)

			if attrSlot != 0:
				type = attrSlot[0]
				value = attrSlot[1]
				
				if type == 0 or value == 0:
					self.tooltipItem.AppendDescription(localeInfo.PET_TEXT_9, 26)
				else:
					affectString = uiToolTip.AFFECT_DICT[type](value)
					affectString = self.SplitStringBonus(affectString, 0)
					if affectString:
						value = float(value) / 10
						self.tooltipItem.AppendTextLine(affectString + str(value), grp.GenerateColor(0.8824, 0.9804, 0.8824, 1.0))
			else:
				self.tooltipItem.AppendDescription(localeInfo.PET_TEXT_9, 26)
				
			self.tooltipItem.ShowToolTip()

	def CreateDesignText(self):
		self.wndTitleNameLv = ui.MakeText(self, "Nivel", 42, 88)
		self.wndTitleNameLv.SetPackedFontColor(0xFFFEE3AE)
		self.wndTitleNameLv.Show()

		self.wndTitleNameExp = ui.MakeText(self, localeInfo.TASKBAR_EXP, 100, 88)
		self.wndTitleNameExp.SetPackedFontColor(0xFFFEE3AE)
		self.wndTitleNameExp.Show()

		self.wndTitleNameEvo = ui.MakeText(self, localeInfo.PET_TEXT_4, 192, 88)
		self.wndTitleNameEvo.SetPackedFontColor(0xFFFEE3AE)
		self.wndTitleNameEvo.Show()

		self.wndTitleNameAbilities = ui.MakeText(self, localeInfo.STAT_TOOLTIP_TAB_SKILL, 85, 45)
		self.wndTitleNameAbilities.SetPackedFontColor(0xFF12c767)
		self.wndTitleNameAbilities.Show()

		self.wndTitleNameHP = ui.MakeText(self, "HP", 75, 196)
		self.wndTitleNameHP.SetPackedFontColor(0xFFFEE3AE)
		self.wndTitleNameHP.Show()

		self.wndTitleNameAttack = ui.MakeText(self, "Atac", 71, 196 + 23)
		self.wndTitleNameAttack.SetPackedFontColor(0xFFFEE3AE)
		self.wndTitleNameAttack.Show()

		self.wndTitleNameMonsters = ui.MakeText(self, localeInfo.PET_TEXT_10, 32, 196 + 23 + 21)
		self.wndTitleNameMonsters.SetPackedFontColor(0xFFFEE3AE)
		self.wndTitleNameMonsters.Show()
		
		self.wndTitleNameDuration = ui.MakeText(self, "Dur.: 15/120 Ore", 45, 137)
		self.wndTitleNameDuration.SetPackedFontColor(0xFFFEE3AE)
		self.wndTitleNameDuration.Show()		
		
		self.ToolTipExp = self.TextToolTip(15*1)
		self.ToolTipExp.Hide()

		self.ToolTipExp2 = self.TextToolTip(15*2)
		self.ToolTipExp2.Hide()
		
		self.wndExpBoard = ui.Window()
		self.wndExpBoard.SetParent(self)
		self.wndExpBoard.SetSize(16 * 5 + 2 * 4, 16)
		self.wndExpBoard.SetPosition(89, 109)
		self.wndExpBoard.AddFlag("ltr")
		self.wndExpBoard.OnMouseOverIn = ui.__mem_func__(self.__OverInExp)
		self.wndExpBoard.OnMouseOverOut = ui.__mem_func__(self.__OverOutExp)
		self.wndExpBoard.Show()

		self.dictExpGauge = {}
		
		for x in xrange(4):
			xPos = [0, 16 + 2, 16 * 2 + 2 * 2, 16 * 3 + 3 * 2]
			self.dictExpGauge[x] = ui.ExpandedImageBox()
			self.dictExpGauge[x].SetParent(self.wndExpBoard)
			self.dictExpGauge[x].LoadImage("d:/ymir work/ui/pet/exp_gauge/exp_on.sub")
			self.dictExpGauge[x].SetPosition(xPos[x], 0)
			self.dictExpGauge[x].OnMouseOverIn = ui.__mem_func__(self.__OverInExp)
			self.dictExpGauge[x].OnMouseOverOut = ui.__mem_func__(self.__OverOutExp)
			self.dictExpGauge[x].Show()
			
		self.wndLifeGauge = ui.AniImageBox()
		self.wndLifeGauge.SetParent(self)
		self.wndLifeGauge.SetDelay(6)
		for x in xrange(1, 8):
			self.wndLifeGauge.AppendImage("D:/Ymir Work/UI/Pattern/HPGauge/0%d.tga" % (x))
		
		self.wndLifeGauge.SetPosition(32, 155)
		self.wndLifeGauge.Show()
	
		self.itemSlotPet = ui.GridSlotWindow()
		self.itemSlotPet.SetParent(self.Board)
		self.itemSlotPet.SetPosition(13, 35)
		self.itemSlotPet.ArrangeSlot(0, 1, 1, 32, 32, 0, 0)
		self.itemSlotPet.Show()
	
	
	def CreateEvolvePage(self):
		self.BoardEvolve = ui.BorderA()
		self.BoardEvolve.SetParent(self)
		self.BoardEvolve.SetSize(255, 100)
		self.BoardEvolve.SetPosition(10, 80)
		self.BoardEvolve.Hide()

		self.TitleNameEvolve = ui.ExpandedImageBox()
		self.TitleNameEvolve.SetParent(self.BoardEvolve)
		self.TitleNameEvolve.LoadImage("d:/ymir work/ui/minigame/catchking/challenge_text_bg.png")
		self.TitleNameEvolve.SetPosition(28, 4)
		self.TitleNameEvolve.Show()

		self.TitleEvolve = ui.TextLine()
		self.TitleEvolve.SetParent(self.TitleNameEvolve)
		self.TitleEvolve.SetWindowHorizontalAlignCenter()
		self.TitleEvolve.SetHorizontalAlignCenter()
		self.TitleEvolve.SetText(localeInfo.PET_TEXT_11)
		self.TitleEvolve.SetPosition(0, 3)
		self.TitleEvolve.Show()

		self.EvolveItemSlot = ui.GridSlotWindow()
		self.EvolveItemSlot.SetParent(self.BoardEvolve)
		self.EvolveItemSlot.SetPosition(49, 30)
		self.EvolveItemSlot.ArrangeSlot(0, 5, 1, 32, 32, 0, 0)
		self.EvolveItemSlot.SetSlotBaseImage("d:/ymir work/ui/public/Slot_Base.sub", 1.0, 1.0, 1.0, 1.0)	

		self.EvolveItemSlot.SetOverInItemEvent(ui.__mem_func__(self.OverInItem))
		self.EvolveItemSlot.SetOverOutItemEvent(ui.__mem_func__(self.OverOutToolTip))
		self.EvolveItemSlot.Show()
		
		self.btnStartEvolve = ui.MakeButton(self.BoardEvolve, 55, 70, False, "d:/ymir work/ui/switchbot/", "btn_big_03.sub", "btn_big_02.sub", "btn_big_03.sub")
		self.btnStartEvolve.SetText(localeInfo.PET_TEXT_1)
		self.btnStartEvolve.SetEvent(ui.__mem_func__(self.DoEvolve))

		self.btnCloseEvolve = ui.MakeButton(self.BoardEvolve, 235, 5, localeInfo.UI_CLOSE, "d:/ymir work/ui/public/", "close_button_01.sub", "close_button_02.sub", "close_button_03.sub")
		self.btnCloseEvolve.SetEvent(ui.__mem_func__(self.CloseEvolve))

	def ShowEvolve(self):
		self.BoardEvolve.Show()

	def CloseEvolve(self):
		self.BoardEvolve.Hide()

	def __OverInExp(self):
		if self.ToolTipExp:
			self.ToolTipExp.Show()

		if self.ToolTipExp2:
			self.ToolTipExp2.Show()

	def __OverOutExp(self):
		if self.ToolTipExp:
			self.ToolTipExp.Hide()

		if self.ToolTipExp2:
			self.ToolTipExp2.Hide()

	def OverInItem(self, slotIndex):
		if mouseModule.mouseController.isAttached():
			return
			
		if self.PetIsActive == False:
			return
		
		Evolve = player.GetItemTransmutation(player.INVENTORY, self.SlotPosCompanion)
		
		ItemVnum = 0
		if DICT_EVOLVE_ITEMS.has_key(Evolve):
			ItemVnum = DICT_EVOLVE_ITEMS[Evolve][slotIndex][0]

		if self.tooltipItem and ItemVnum:
			if ItemVnum == 1:
				price = DICT_EVOLVE_ITEMS[Evolve][slotIndex][1]
				self.tooltipItem.ClearToolTip()
				self.tooltipItem.AppendTextLine("Yang")
				self.tooltipItem.AppendSpace(5)
				self.tooltipItem.AppendTextLine(localeInfo.NumberToGoldString(long(price)), self.tooltipItem.GetPriceColor(long(price)))
				self.tooltipItem.ShowToolTip()
			else:
				self.tooltipItem.SetItemToolTip(ItemVnum)

	def OverOutToolTip(self):
		if self.tooltipItem:
			self.tooltipItem.HideToolTip()

	def SelectEmptySkill(self, SkillNum):
		if constInfo.GET_ITEM_QUESTION_DIALOG_STATUS() == 1:
			return

		if self.PetIsActive == False:
			return
			
		chat.AppendChat(1, "Doresti sa deblochezi skill-ul cu numarul %d", SkillNum)

	def OnRender(self):
		if self.PetIsActive == False: # PET_UNSUMMON (ClearInfo)
			self.ClearInfo()
		else:
			self.RefreshPet(self.SlotPosCompanion)

	def ClearInfo(self):
		self.ManageText()
		
		constInfo.COMPANION_ACTIVE_POS = -1

		# Companion
		self.wndInfoCompanion.Hide()
		
		for index in xrange(2):
			self.dictImageSkill[index].LoadImage("d:/ymir work/ui/game/normal_interface/offlineshop_locked_hover.png")

	def SetNextExp(self, dwNextExp):
		self.NextExp = dwNextExp
		self.wndInfoCompanion.SetNextExp(self.NextExp)

	def SetExperience(self, curPoint, maxPoint):
		if maxPoint <= 0:
			return

		curPoint = min(curPoint, maxPoint)
		curPoint = max(curPoint, 0)
		maxPoint = max(maxPoint, 0)

		quarterPoint = maxPoint / 4
		FullCount = 0

		if 0 != quarterPoint:
			FullCount = min(4, curPoint / quarterPoint)

		for i in xrange(4):
			self.dictExpGauge[i].Hide()

		for i in xrange(FullCount):
			self.dictExpGauge[i].SetRenderingRect(0.0, 0.0, 0.0, 0.0)
			self.dictExpGauge[i].Show()

		if 0 != quarterPoint:
			if FullCount < 4:
				Percentage = float(curPoint % quarterPoint) / quarterPoint - 1.0
				self.dictExpGauge[FullCount].SetRenderingRect(0.0, Percentage, 0.0, 0.0)
				self.dictExpGauge[FullCount].Show()

		self.ToolTipExp.SetText("EXP : %d din %d" % (curPoint, maxPoint))
		self.ToolTipExp2.SetText("EXP : %.2f%%" % (float(curPoint) / maxPoint * 100))

	def SetInventoryPet(self, index):
		if index == -1:
			self.PetIsActive = False
			return
		else:
			self.PetIsActive = True

		ItemVnum = player.GetItemIndex(index)
		item.SelectItem(ItemVnum)
		
		if ItemVnum == 0:
			self.PetIsActive = False
			return

		self.SlotPosCompanion = index
		self.RefreshPet(self.SlotPosCompanion)
		self.ManageText(True)

		constInfo.COMPANION_ACTIVE_POS = index
		
		self.itemSlotPet.SetItemSlot(0, ItemVnum, 0)
		
		# Companion
		self.wndInfoCompanion.SetVnum(ItemVnum)
		self.wndInfoCompanion.Show()

	def RefreshPet(self, index):
		ItemVnum = player.GetItemIndex(index)
		
		if ItemVnum == 0:
			self.PetIsActive = False
			return
			
		AttributeI = self.GetFromAttr(index, COMPANION_PROGRESS_BONUS1) / 10
		AttributeII = self.GetFromAttr(index, COMPANION_PROGRESS_BONUS1, True) / 10
		AttributeIII = self.GetFromAttr(index, COMPANION_PROGRESS_BONUS2) / 10
		
		self.AttributeStringI = str(AttributeI)
		self.AttributeStringII = str(AttributeII)
		self.AttributeStringIII = str(AttributeIII)
		
		self.AttributeStringI.strip("0")
		self.AttributeStringII.strip("0")
		self.AttributeStringIII.strip("0")
		
		if AttributeI != 0:
			self.wndBonus[0].SetText("%.1f%%" % float(self.AttributeStringI))
		
		if AttributeII != 0:
			self.wndBonus[1].SetText("%.1f%%" % float(self.AttributeStringII))
		
		if AttributeIII != 0:
			self.wndBonus[2].SetText("%.1f%%" % float(self.AttributeStringIII))
		
		LvPet = player.GetItemMetinSocket(player.INVENTORY, index, COMPANION_SOCKET_LEVEL)
		self.wndInfoPet[0].SetText("%d" % (LvPet))
		self.wndInfoPet[0].SetWindowHorizontalAlignCenter()
		self.wndInfoPet[0].SetHorizontalAlignCenter()
		self.wndInfoPet[0].SetPosition(-86, 109)
		self.wndInfoPet[0].Show()
		
		Evolve = player.GetItemTransmutation(player.INVENTORY, index)
		if Evolve == 0:
			self.wndInfoPet[1].SetText("%s" % (localeInfo.PET_SYS_YOUNG))
			self.wndInfoPet[1].SetPackedFontColor(0xFF964B00)
		elif Evolve == 1:
			self.wndInfoPet[1].SetText(" %s" % (localeInfo.PET_SYS_WILD))
			self.wndInfoPet[1].SetPackedFontColor(0xFF40bee3)
		elif Evolve == 2:
			self.wndInfoPet[1].SetText("%s" % (localeInfo.PET_SYS_BRAVE))
			self.wndInfoPet[1].SetPackedFontColor(0xFFdcdd54)
		elif Evolve == 3:
			self.wndInfoPet[1].SetText("%s" % (localeInfo.PET_SYS_HEROIC))
			self.wndInfoPet[1].SetPackedFontColor(0xFFdb4a4a)
		
		# Evolve Items
		for indexH in xrange(5):
			self.EvolveItemSlot.ClearSlot(indexH)
		
		if DICT_EVOLVE_ITEMS.has_key(Evolve):
			for indexH in DICT_EVOLVE_ITEMS[Evolve]:
				ItemVnum = DICT_EVOLVE_ITEMS[Evolve][indexH][0]
				ItemCount = DICT_EVOLVE_ITEMS[Evolve][indexH][1]
				
				if ItemVnum == 1:
					ItemCount = 0
				
				self.EvolveItemSlot.SetItemSlot(indexH, ItemVnum, ItemCount)

		self.wndInfoPet[1].SetWindowHorizontalAlignCenter()
		self.wndInfoPet[1].SetHorizontalAlignCenter()
		self.wndInfoPet[1].SetPosition(72, 110)
		self.wndInfoPet[1].Show()
		
		dwExp = player.GetItemMetinSocket(player.INVENTORY, self.SlotPosCompanion, COMPANION_SOCKET_EXP)
		if self.NextExp > 0:
			self.SetExperience(dwExp, self.NextExp)
			self.ToolTipExp.SetText("EXP : %d din %d" % (dwExp, self.NextExp))
			self.ToolTipExp2.SetText("EXP : %.2f%%" % (float(dwExp) / self.NextExp * 100))
			
		Time = player.GetItemMetinSocket(player.INVENTORY, self.SlotPosCompanion, COMPANION_SOCKET_TIME)  - app.GetGlobalTimeStamp()
		if Time > 0:
			hour = int(Time) // 3600
			hour2 = COMPANION_MAX_TIME // 3600
			
			self.wndLifeGauge.SetPercentage(hour, hour2)
			self.wndTitleNameDuration.SetText(localeInfo.PET_TEXT_2 % (hour, hour2))
			
		attrSlot = [player.GetItemAttribute(player.INVENTORY, self.SlotPosCompanion, i) for i in xrange(player.ATTRIBUTE_SLOT_MAX_NUM)]
		
		if attrSlot != 0:
			index = 0
			for x in xrange(COMPANION_SKILL_1, COMPANION_SKILL_3):
				type = attrSlot[x][0]
				value = attrSlot[x][1]

				if value != 0:
					if TYPE_SKILLS.has_key(type):
						self.dictImageSkill[index].LoadImage(TYPE_SKILLS[type]["ICON"])
				else:
					self.dictImageSkill[index].LoadImage("d:/ymir work/ui/game/normal_interface/offlineshop_locked_hover.png")
				
				index += 1
		else:
			for index in xrange(2):
				self.dictImageSkill[index].LoadImage("d:/ymir work/ui/game/normal_interface/offlineshop_locked_hover.png")
		
	def GetExp(self, curPoint, maxPoint):
		curPoint = min(curPoint, maxPoint)
		curPoint = max(curPoint, 0)
		maxPoint = max(maxPoint, 0)
	
		return float(curPoint) / max(1, float(maxPoint)) * 100
	
	def ManageText(self, CanShow = False):
		if not CanShow:
			for x in xrange(len(self.wndBonus)):
				self.wndBonus[x].Hide()
				
			for x in xrange(len(self.wndInfoPet)):
				self.wndInfoPet[x].Hide()
			
			self.itemSlotPet.ClearSlot(0)
			self.wndTitleNameDuration.SetText("")
		else:
			for x in xrange(len(self.wndBonus)):
				self.wndBonus[x].Show()
				
			for x in xrange(len(self.wndInfoPet)):
				self.wndInfoPet[x].Show()
	
	def GetFromAttr(self, SlotPos, index, IsType = False):
		Attribute = player.GetItemAttribute(player.INVENTORY, SlotPos, index)
		
		if IsType:
			return float(Attribute[0])

		return float(Attribute[1])
	
	def Show(self):
		self.SetCenterPosition()
		self.SetTop()
		ui.ScriptWindow.Show(self)
	
	def Open(self, vid):
		self.SetCenterPosition()
		self.SetTop()
		self.Show()
		
	def Destroy(self):
		self.ClearDictionary()
		self.wndBonus = {}
		self.wndInfoPet = {}

		if self.QuestionDialog:
			self.QuestionDialog.Close()
			self.QuestionDialog = None

		if self.wndInfoCompanion:
			self.wndInfoCompanion.Hide()
			self.wndInfoCompanion.Destroy()
			self.wndInfoCompanion = None

		if self.ToolTipExp:
			self.ToolTipExp.Hide()
			self.ToolTipExp = None

		if self.ToolTipExp2:
			self.ToolTipExp2.Hide()
			self.ToolTipExp2 = None

		if self.tooltipItem:
			self.tooltipItem.HideToolTip()
			self.tooltipItem = None

	def Close(self):
		if self.QuestionDialog:
			self.QuestionDialog.Close()
			self.QuestionDialog = None
			constInfo.SET_ITEM_QUESTION_DIALOG_STATUS(0)

		if self.tooltipItem:
			self.tooltipItem.HideToolTip()

		if self.ToolTipExp:
			self.ToolTipExp.Hide()

		if self.ToolTipExp2:
			self.ToolTipExp2.Hide()

		self.Hide()
		
	def OnPressEscapeKey(self):
		self.Close()
		return True
