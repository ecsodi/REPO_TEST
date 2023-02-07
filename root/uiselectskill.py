import uiCommon
import app
import wndMgr
import net 
import player 
import ui 
import uiToolTip 
import background 
import uiScriptLocale
import constInfo
import localeInfo
import chat
import cfg
import item
import uiAffectShower
import grp
import dbg
import skill
from _weakref import proxy
import Collision as chr
import renderTarget
import event

BOARD_WIDTH = 545
BOARD_HEIGHT = 365

JOB_NAME_DICT = {
	0	:	[localeInfo.SKILL_GROUP_WARRIOR_1,localeInfo.SKILL_GROUP_WARRIOR_2],
	1	:	[localeInfo.SKILL_GROUP_ASSASSIN_1,localeInfo.SKILL_GROUP_ASSASSIN_2],
	2	:	[localeInfo.SKILL_GROUP_SURA_1,localeInfo.SKILL_GROUP_SURA_2],
	3	:	[localeInfo.SKILL_GROUP_SHAMAN_1,localeInfo.SKILL_GROUP_SHAMAN_2],
	4	:	["Instinct","N.A"],
}

class SelectSkill(ui.ScriptWindow):
	def __init__(self):
		ui.ScriptWindow.__init__(self)
		self.isLoaded = 0

		self.__LoadWindow()
		
	def __del__(self):
		ui.ScriptWindow.__del__(self)
		
	def __LoadWindow(self):
		if self.isLoaded == 1:
			return

		self.isLoaded = 1
		
		self.AddFlag("float")
		self.AddFlag("animation")
		
		self.ChooseSkillSet = {}

		self.Board = ui.Board()
		self.Board.SetParent(self)
		self.Board.SetPosition(0, 0)
		self.Board.SetSize(BOARD_WIDTH, BOARD_HEIGHT)
		self.Board.AddFlag("not_pick")
		self.Board.Show()
		
		self.imageTypeOne = ui.MakeImageBox(self.Board, "skill_select/number_one.png", 8, 8 )
		self.imageTypeTwo = ui.MakeImageBox(self.Board, "skill_select/number_two.png", 405, 8 )
		
		self.skillTypeOne = ui.MakeText(self.imageTypeOne, JOB_NAME_DICT[self.GetRealRace()][0], 60, 20 )
		self.skillTypeTwo = ui.MakeText(self.imageTypeTwo, JOB_NAME_DICT[self.GetRealRace()][1], 60, 20 )

		self.skillSlotOne = ui.GridSlotWindow()
		self.skillSlotOne.SetParent(self.imageTypeOne)
		self.skillSlotOne.SetPosition(50, 95)
		self.skillSlotOne.ArrangeSlot(0, 1, 6, 34, 37, 0, 0)
		self.skillSlotOne.RefreshSlot()
		self.skillSlotOne.SetOverInItemEvent(ui.__mem_func__(self.OverInItem), 1)
		self.skillSlotOne.Show()
						
		self.skillSlotTwo = ui.GridSlotWindow()
		self.skillSlotTwo.SetParent(self.imageTypeTwo)
		self.skillSlotTwo.SetPosition(50, 95)
		self.skillSlotTwo.ArrangeSlot(0, 1, 6, 34, 37, 0, 0)
		self.skillSlotTwo.RefreshSlot()
		self.skillSlotTwo.SetOverInItemEvent(ui.__mem_func__(self.OverInItem), 2)
		self.skillSlotTwo.Show()
		
		for i in xrange(2):
			self.ChooseSkillSet[i] = ui.Button()
			self.ChooseSkillSet[i].SetParent(self.Board)
			self.ChooseSkillSet[i].SetPosition(19, 315)
			self.ChooseSkillSet[i].SetUpVisual("skill_select/button_1.png")
			self.ChooseSkillSet[i].SetOverVisual("skill_select/button_2.png")
			self.ChooseSkillSet[i].SetDownVisual("skill_select/button_3.png")
			self.ChooseSkillSet[i].SetText("Alege")
			self.ChooseSkillSet[i].Show()
			
		self.ChooseSkillSet[0].SetEvent(ui.__mem_func__(self.SelectJobFirstQuestion))
		self.ChooseSkillSet[1].SetEvent(ui.__mem_func__(self.SelectJobSecondQuestion))
		self.ChooseSkillSet[0].SetParent(self.imageTypeOne)
		self.ChooseSkillSet[1].SetParent(self.imageTypeTwo)
		
		if self.GetRealRace() == 2 or self.GetRealRace() == 3 or self.GetRealRace() == 4:
			self.skillSlotTwo.SetPosition(50, 79)
			self.skillSlotOne.SetPosition(50, 79)
			
		if self.GetRealRace() == 4:
			for k in xrange(6):

				self.skillSlotTwo.ClearSlot(k)
				self.skillSlotTwo.SetAlwaysRenderCoverButton(k)
				self.skillSlotTwo.SetCoverButton(k, "d:/ymir work/ui/pet/skill_button/skill_enable_button.sub", "d:/ymir work/ui/pet/skill_button/skill_enable_button.sub", "d:/ymir work/ui/pet/skill_button/skill_enable_button.sub", "d:/ymir work/ui/pet/skill_button/skill_enable_button.sub", False, False)

				self.skillSlotTwo.SetSlotStyle(wndMgr.SLOT_STYLE_NONE)
			self.ChooseSkillSet[1].SetEvent(ui.__mem_func__(self.EmptyFunc))

		for i in xrange(6):
			self.skillSlotOne.SetSkillSlotNew(i, self.GetSkillIndex()+i, 3, 1)
			self.skillSlotOne.SetSlotStyle(wndMgr.SLOT_STYLE_NONE)

		if self.GetRealRace() != 4:
			for j in xrange(6):
				self.skillSlotTwo.SetSkillSlotNew(j, self.GetSkillIndex()+j+15, 3, 1)
				self.skillSlotTwo.SetSlotStyle(wndMgr.SLOT_STYLE_NONE)

		self.RENDER_TARGET_INDEX = 22
		self.ModelPreview = ui.RenderTarget()
		self.ModelPreview.SetParent(self)
		self.ModelPreview.SetSize(261, 347)
		self.ModelPreview.SetPosition(142, 8)
		self.ModelPreview.SetRenderTarget(self.RENDER_TARGET_INDEX)
		self.ModelPreview.Show()
		self.SetSize(self.Board.GetWidth(), self.Board.GetHeight())

	def OverInItem(self, slotIndex, dummyarg):
		self.isValue = slotIndex + 1
		
		if dummyarg == 2:
			self.emotionValue = int(self.GetRealRace() * 30 + self.isValue + 15)
		else:
			self.emotionValue = int(self.GetRealRace() * 30 + self.isValue)
					
		self.DoModelEmotion(self.emotionValue)
		
	def GetSkillIndex(self):
		if self.GetRealRace() == 4:
			return 170
		else:
			return self.GetRealRace() * 30 + 1

	def GetRealRace(self):
		race = net.GetMainActorRace()
		if race >= 4:
			return race-4
		else:
			return race
			
	def DoModelEmotion(self, emotionValue):
		if self.GetRealRace() == 2: # SURA
			self.ModelPreviewEmotion(emotionValue+20 - 5)
		elif self.GetRealRace() == 3: # SHAMAN
			self.ModelPreviewEmotion(emotionValue+ 10) 
		elif self.GetRealRace() == 4: # LYCAN
			self.ModelPreviewEmotion(emotionValue + 5)
		elif self.GetRealRace() == 1: # NINJA
			self.ModelPreviewEmotion(emotionValue+20)
		elif self.GetRealRace() == 0: # WAR
			self.ModelPreviewEmotion(emotionValue + 35 + 15)

	def ModelPreviewEmotion(self, emotion):
		self.ModelPreview.Show()
		renderTarget.ChangeEffect(self.RENDER_TARGET_INDEX)

		renderTarget.SetBackground(self.RENDER_TARGET_INDEX, "skill_select/render_bg.png")
		renderTarget.SetVisibility(self.RENDER_TARGET_INDEX, True)
		
		renderTarget.SelectModel(self.RENDER_TARGET_INDEX, player.GetRace())
		
		if player.GetItemIndex(item.COSTUME_SLOT_BODY) != 0:
			armorVnum = player.GetItemIndex(item.COSTUME_SLOT_BODY)
		else:
			armorVnum = player.GetItemIndex(item.EQUIPMENT_BODY)
		weaponVnum = player.GetItemIndex(item.EQUIPMENT_WEAPON)

		if player.GetItemIndex(item.COSTUME_SLOT_HAIR) != 0:
			item.SelectItem(player.GetItemIndex(item.COSTUME_SLOT_HAIR))
			renderTarget.SetHair(self.RENDER_TARGET_INDEX, item.GetValue(3))

		renderTarget.SetArmor(self.RENDER_TARGET_INDEX, armorVnum)
		renderTarget.SetWeapon(self.RENDER_TARGET_INDEX, weaponVnum)
		renderTarget.SetAutoRotate(self.RENDER_TARGET_INDEX, False)
		renderTarget.DoEmotion(self.RENDER_TARGET_INDEX, int(emotion))

	def ModelPreviewClose(self):
		self.ModelPreview.Hide()
		renderTarget.SetVisibility(self.RENDER_TARGET_INDEX, False)

	def Destroy(self):
		self.ClearDictionary()
		
	def __OnCloseQuestionDialog(self):
		if self.questionDialog:
			self.questionDialog.Close()
		self.questionDialog = None

	def EmptyFunc(self):
		chat.AppendChat(chat.CHAT_TYPE_INFO, "Lycan are doar un set de abilitati disponibil momentan.")

	def SelectJobFirstQuestion(self):
		self.questionDialog = uiCommon.QuestionDialog()
		self.questionDialog.SetText(localeInfo.CHOOSE_SKILLS_SURE % JOB_NAME_DICT[self.GetRealRace()][0])
		self.questionDialog.SetAcceptEvent(ui.__mem_func__(self.SelectJobFirst))
		self.questionDialog.SetCancelEvent(ui.__mem_func__(self.__OnCloseQuestionDialog))
		self.questionDialog.Open()

	def SelectJobFirst(self):
		constInfo.SelectJob['QCMD'] = str(1)
		event.QuestButtonClick(constInfo.SelectJob['QID'])
		self.RealClose()
		self.__OnCloseQuestionDialog()

	def SelectJobSecondQuestion(self):
		self.questionDialog = uiCommon.QuestionDialog()
		self.questionDialog.SetText(localeInfo.CHOOSE_SKILLS_SURE % JOB_NAME_DICT[self.GetRealRace()][1])
		self.questionDialog.SetAcceptEvent(ui.__mem_func__(self.SelectJobSecond))
		self.questionDialog.SetCancelEvent(ui.__mem_func__(self.__OnCloseQuestionDialog))
		self.questionDialog.Open()

	def SelectJobSecond(self):
		constInfo.SelectJob['QCMD'] = str(2)
		event.QuestButtonClick(constInfo.SelectJob['QID'])
		self.RealClose()
		self.__OnCloseQuestionDialog()

	def Close(self):
		self.wndpopupdialog = uiCommon.PopupDialog()
		self.wndpopupdialog.SetText(localeInfo.CANT_CLOSE_WINDOW)
		self.wndpopupdialog.Open()

	def RealClose(self):
		self.Hide()

	def Show(self):
		self.SetTop()
		self.SetCenterPosition()
		ui.ScriptWindow.Show(self)
		
	def OnPressEscapeKey(self):
		self.Close()
		return True
		