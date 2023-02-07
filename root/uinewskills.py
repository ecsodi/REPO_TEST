import thenewui as ui
import event, constInfo, uiCommon, chat, playersettingmodule, localeInfo, wndMgr
import app
import net
import CacheEffect as player

JOB_NAME_DICT = {
	0	:	[localeInfo.SKILL_GROUP_WARRIOR_1,localeInfo.SKILL_GROUP_WARRIOR_2],
	1	:	[localeInfo.SKILL_GROUP_ASSASSIN_1,localeInfo.SKILL_GROUP_ASSASSIN_2],
	2	:	[localeInfo.SKILL_GROUP_SURA_1,localeInfo.SKILL_GROUP_SURA_2],
	3	:	[localeInfo.SKILL_GROUP_SHAMAN_1,localeInfo.SKILL_GROUP_SHAMAN_2],
	4	:	["Instinct","N.A"],
}


JOB_DESC_DICT = {
	0	:	[localeInfo.SKILL_WARRIOR_CORPORAL, localeInfo.SKILL_WARRIOR_MENTAL],
	1	:	[localeInfo.SKILL_NINJA_DAGGER, localeInfo.SKILL_NINJA_BOW],
	2	:	[localeInfo.SKILL_SURA_AM, localeInfo.SKILL_SURA_BM],
	3	:	[localeInfo.SKILL_SHAMAN_DRAGON, localeInfo.SKILL_SHAMAN_HEALER],
	4	:	[localeInfo.SKILL_LYCAN_INSTINCT, "No skillset here."],
}

JOB_LIST = {
	0	:	localeInfo.JOB_WARRIOR,
	1	:	localeInfo.JOB_ASSASSIN,
	2	:	localeInfo.JOB_SURA,
	3	:	localeInfo.JOB_SHAMAN,
	4	:	localeInfo.JOB_WOLFMAN,
}

class MultiTextLine(ui.TextLine):
	def __init__(self, parent, text, x, y, range = 15):
		ui.TextLine.__init__(self)
		
		self.TextList = []
		self.CreateUI(parent, text, x, y, range)
		
	def __del__(self):
		del self.TextList
		ui.TextLine.__del__(self)
	
	def CreateUI(self, parent, text, x, y, range):
		if "\n" in str(text):
			self.first_text = ui.TextLine()
			self.first_text.SetParent(parent)
			self.first_text.SetPosition(x, y)		
			self.first_text.SetText(text.split("\n")[0])
			self.first_text.Show()
			self.TextList.append(self.first_text)
			for i in xrange(text.count("\n")):
				self.i = ui.TextLine()
				self.i.SetParent(parent)
				self.i.SetPosition(x, (i + 1) * range + y)		
				self.i.SetText(text.split("\n")[i+1])
				self.i.Show()
				self.TextList.append(self.i)
				
	def SetText(self, text):
		tmpMiktar = 0
		if "\n" in str(text):				
			for i in self.TextList:
				if i == self.TextList[0]:
					i.SetText(text.split("\n")[0])
				else:
					i.SetText(text.split("\n")[tmpMiktar])
				tmpMiktar += 1
	
	def Close(self):
		for i in self.TextList: i.Hide()
		self.__del__()

class SelectSkillWindow(ui.Window):
	def __init__(self):
		ui.Window.__init__(self)
		self.isLoaded = 0
		self.__LoadWindow()

	def __LoadWindow(self):
		if (self.isLoaded == 1):
			return

		self.isLoaded = 1
		
		self.SetSize(430, 320)
		self.AddFlag("float")
		# self.AddFlag("movable")
		self.AddFlag("animation")
		self.Boards = {}
		self.loadingAnimations = {}
		self.BoardSecond = {}
		self.SkillName = {}
		self.BoardThird = {}
		self.BoardFourth = {}
		self.typeTextLine = {}
		self.ChooseSkillSet = {}
		self.skillSlot = {}
		self.skillSlotBack = {}
		self.TextLineDesc = {}
		
		for i in xrange(2):
			self.Boards[i] = ui.BorderA()
			self.Boards[i].SetParent(self)
			self.Boards[i].SetSize(210, 210)
			self.Boards[i].Show()
		
			self.loadingAnimations[i] = ui.AniImageBox()
			self.loadingAnimations[i].SetParent(self.Boards[i])
			self.loadingAnimations[i].SetPosition(3, 3)
			self.loadingAnimations[i].SetDelay(5)
			
			self.loadingAnimations[i].UpdateRect()
			self.loadingAnimations[i].Show()
	
			self.BoardSecond[i] = ui.BorderA()
			self.BoardSecond[i].SetParent(self)
			self.BoardSecond[i].SetSize(170, 25)
			self.BoardSecond[i].Show()
			
			self.SkillName[i] = ui.ImageBox()
			self.SkillName[i].SetParent(self.BoardSecond[i])
			self.SkillName[i].SetWindowHorizontalAlignCenter()
			self.SkillName[i].SetWindowVerticalAlignCenter()
			self.SkillName[i].LoadImage("d:/ymir work/ui/game/myshop_deco/select_btn_01.sub")
			self.SkillName[i].SetPosition(0, 0)
			self.SkillName[i].Show()	

			self.BoardThird[i] = ui.BorderA()
			self.BoardThird[i].SetParent(self)
			self.BoardThird[i].SetSize(210, 75)
			self.BoardThird[i].Show()
			
			self.BoardFourth[i] = ui.ThinBoardCircle()
			self.BoardFourth[i].SetParent(self.BoardThird[i])
			self.BoardFourth[i].SetSize(200, 40)
			self.BoardFourth[i].SetPosition(5, 5)
			self.BoardFourth[i].Show()
	
			self.typeTextLine[i] = ui.TextLine()
			self.typeTextLine[i].SetVerticalAlignCenter()
			self.typeTextLine[i].SetWindowVerticalAlignCenter()
			self.typeTextLine[i].SetHorizontalAlignCenter()
			self.typeTextLine[i].SetWindowHorizontalAlignCenter()
			self.typeTextLine[i].SetPosition(0, -1)
			self.typeTextLine[i].Show()
	
			self.ChooseSkillSet[i] = ui.Button()
			self.ChooseSkillSet[i].SetParent(self.BoardThird[i])
			self.ChooseSkillSet[i].SetPosition(5,47)
			self.ChooseSkillSet[i].SetUpVisual("d:/ymir work/ui/game/myshop_deco/select_btn_01.sub")
			self.ChooseSkillSet[i].SetOverVisual("d:/ymir work/ui/game/myshop_deco/select_btn_02.sub")
			self.ChooseSkillSet[i].SetDownVisual("d:/ymir work/ui/game/myshop_deco/select_btn_03.sub")
			self.ChooseSkillSet[i].SetButtonScale(1.36, 1.0)
			self.ChooseSkillSet[i].SetText("Choose")
			self.ChooseSkillSet[i].Show()
	
			self.skillSlotBack[i] = ui.GridSlotWindow()
			self.skillSlotBack[i].SetParent(self.Boards[i])
			self.skillSlotBack[i].SetPosition(4, 175)
			self.skillSlotBack[i].ArrangeSlot(0, 6, 1, 34, 32, 0, 0)
			self.skillSlotBack[i].RefreshSlot()
			self.skillSlotBack[i].Show()
			
			self.skillSlot[i] = ui.GridSlotWindow()
			self.skillSlot[i].SetParent(self.Boards[i])
			self.skillSlot[i].SetPosition(4, 175)
			self.skillSlot[i].ArrangeSlot(0, 6, 1, 34, 32, 0, 0)
			self.skillSlot[i].RefreshSlot()
			self.skillSlot[i].Show()
			
			self.TextLineDesc[i] = MultiTextLine(self.BoardFourth[i], JOB_DESC_DICT[self.GetRealRace()][i], 0, 0, 15)

		if self.GetRealRace() == 1:
			for i in xrange(33):
				self.loadingAnimations[1].AppendImageScale("d:/ymir work/ui/game/skills/assassin_1/frame_%d_delay-0.1s.png" % int(i), 0.91, 0.82)
	
			for i in xrange(35):
				self.loadingAnimations[0].AppendImageScale("d:/ymir work/ui/game/skills/assassin_2/frame_%d_delay-0.1s.png" % int(i), 0.63, 0.63)
			
		elif self.GetRealRace() == 3:
			for i in xrange(35):
				self.loadingAnimations[0].AppendImageScale("d:/ymir work/ui/game/skills/shaman_1/frame_%d_delay-0.1s.png" % int(i), 0.84, 0.69)
	
			for i in xrange(38):
				self.loadingAnimations[1].AppendImageScale("d:/ymir work/ui/game/skills/shaman_2/frame_%d_delay-0.1s.png" % int(i), 0.73, 0.67)
				
		elif self.GetRealRace() == 4:
			for i in xrange(36):
				self.loadingAnimations[0].AppendImageScale("d:/ymir work/ui/game/skills/wolfman_1/frame_%d_delay-0.03s.png" % int(i), 0.57, 0.58)
	
		elif self.GetRealRace() == 2:
			for i in xrange(35):
				self.loadingAnimations[0].AppendImageScale("d:/ymir work/ui/game/skills/sura_1/%d.png" % int(i), 0.62, 0.65)
	
			for i in xrange(40):
				self.loadingAnimations[1].AppendImageScale("d:/ymir work/ui/game/skills/sura_2/%d.png" % int(i), 0.81, 0.71)
	
		elif self.GetRealRace() == 0:
			for i in xrange(36):
				self.loadingAnimations[0].AppendImageScale("d:/ymir work/ui/game/skills/warrior_1/frame_%d_delay-0.1s.png" % int(i), 0.67, 0.68)
	
			for i in xrange(40):
				self.loadingAnimations[1].AppendImageScale("d:/ymir work/ui/game/skills/warrior_2/frame_%d_delay-0.1s.png" % int(i), 0.65, 0.65)
			
		self.Boards[0].SetPosition(0, 32)
		self.Boards[1].SetPosition(220, 32)

		self.BoardSecond[0].SetPosition(20, 0)
		self.BoardSecond[1].SetPosition(240, 0)
		
		self.BoardThird[0].SetPosition(0, 242)
		self.BoardThird[1].SetPosition(220, 242)

		self.typeTextLine[0].SetParent(self.SkillName[0])
		self.typeTextLine[1].SetParent(self.SkillName[1])
		
		self.typeTextLine[0].SetText(JOB_NAME_DICT[self.GetRealRace()][0])
		self.typeTextLine[1].SetText(JOB_NAME_DICT[self.GetRealRace()][1])

		self.ChooseSkillSet[0].SetEvent(ui.__mem_func__(self.SelectJobFirstQuestion))
		self.ChooseSkillSet[1].SetEvent(ui.__mem_func__(self.SelectJobSecondQuestion))

		if self.GetRealRace() == 4:
			self.ChooseSkillSet[1].SetEvent(ui.__mem_func__(self.EmptyFunc))
			self.typeTextLine[1].Hide()
			self.ChooseSkillSet[1].Hide()
			self.Boards[1].Hide()
			self.BoardSecond[1].Hide()
			self.BoardThird[1].Hide()
			self.loadingAnimations[1].Hide()
			self.Boards[0].SetPosition(0 + 70, 32)
			self.BoardSecond[0].SetPosition(20 + 70, 0)
			self.BoardThird[0].SetPosition(0 + 70, 242)

			for k in xrange(6):
				self.skillSlotBack[1].SetSlotStyle(wndMgr.SLOT_STYLE_NONE)

				self.skillSlot[1].ClearSlot(k)
				self.skillSlot[1].SetCoverButton(k, "d:/ymir work/ui/pet/skill_button/skill_enable_button.sub", "d:/ymir work/ui/pet/skill_button/skill_enable_button.sub", "d:/ymir work/ui/pet/skill_button/skill_enable_button.sub", "d:/ymir work/ui/pet/skill_button/skill_enable_button.sub", False, False)
				self.skillSlot[1].SetAlwaysRenderCoverButton(k)

				self.skillSlot[1].SetSlotStyle(wndMgr.SLOT_STYLE_NONE)

		for i in xrange(6):
			self.skillSlotBack[0].SetSlotStyle(wndMgr.SLOT_STYLE_NONE)

			self.skillSlot[0].SetSkillSlotNew(i, self.GetSkillIndex()+i, 3, 1)
			self.skillSlot[0].SetSlotStyle(wndMgr.SLOT_STYLE_NONE)

		if self.GetRealRace() != 4:
			for j in xrange(6):
				self.skillSlotBack[1].SetSlotStyle(wndMgr.SLOT_STYLE_NONE)

				self.skillSlot[1].SetSkillSlotNew(j, self.GetSkillIndex()+j+15, 3, 1)
				self.skillSlot[1].SetSlotStyle(wndMgr.SLOT_STYLE_NONE)

		self.SetCenterPosition()

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

	def __del__(self):
		ui.Window.__del__(self)

	def Open(self):
		self.SetCenterPosition()
		self.SetTop()
		self.Show()

	def Close(self):
		self.wndpopupdialog = uiCommon.PopupDialog()
		self.wndpopupdialog.SetText(localeInfo.CANT_CLOSE_WINDOW)
		self.wndpopupdialog.Open()

	def RealClose(self):
		self.Hide()

	def Destroy(self):
		self.RealClose()
		self.ClearDictionary()
		
	def OnPressEscapeKey(self):
		self.Close()
		return True