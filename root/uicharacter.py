import thenewui as ui
import uiScriptLocale
import app
import net
import dbg
import CacheEffect as player
import mouseModule
import wndMgr
import skill
import playersettingmodule
import quest
import localeInfo
import uiScriptLocale
import uiToolTip
import constInfo
import emotion
import Collision as chr
import chat
import item
import cfg

SHOW_ONLY_ACTIVE_SKILL = False
# SHOW_LIMIT_SUPPORT_SKILL_LIST = [121, 122, 126, 127, 128, 129, 131, 137, 138, 139, 140, 143, 144, 145, 146]
# SHOW_LIMIT_SUPPORT_SKILL_LIST = [121, 122, 124, 129, 130, 131, 137, 138, 139, 140, 143, 144, 145, 146]
SHOW_LIMIT_SUPPORT_SKILL_LIST = [121, 122, 123, 124, 129, 131, 137, 138, 139]
HIDE_SUPPORT_SKILL_POINT = True

FACE_IMAGE_DICT = {
	playersettingmodule.RACE_WARRIOR_M	: "icon/face/warrior_m.tga",
	playersettingmodule.RACE_WARRIOR_W	: "icon/face/warrior_w.tga",
	playersettingmodule.RACE_ASSASSIN_M	: "icon/face/assassin_m.tga",
	playersettingmodule.RACE_ASSASSIN_W	: "icon/face/assassin_w.tga",
	playersettingmodule.RACE_SURA_M		: "icon/face/sura_m.tga",
	playersettingmodule.RACE_SURA_W		: "icon/face/sura_w.tga",
	playersettingmodule.RACE_SHAMAN_M	: "icon/face/shaman_m.tga",
	playersettingmodule.RACE_SHAMAN_W	: "icon/face/shaman_w.tga",
}
if app.ENABLE_WOLFMAN_CHARACTER:
	FACE_IMAGE_DICT.update({playersettingmodule.RACE_WOLFMAN_M  : "icon/face/wolfman_m.tga",})

def unsigned32(n):
	return n & 0xFFFFFFFFL

quest_lable_expend_img_path_dict = {
	0: "d:/ymir work/ui/quest_re/tabcolor_1_main.tga",
	1: "d:/ymir work/ui/quest_re/tabcolor_2_sub.tga",
	2: "d:/ymir work/ui/quest_re/tabcolor_3_levelup.tga",
	3: "d:/ymir work/ui/quest_re/tabcolor_4_event.tga",
	4: "d:/ymir work/ui/quest_re/tabcolor_5_collection.tga",
	5: "d:/ymir work/ui/quest_re/tabcolor_6_system.tga",
	6: "d:/ymir work/ui/quest_re/tabcolor_7_scroll.tga",
	7: "d:/ymir work/ui/quest_re/tabcolor_8_daily.tga"
}

class CharacterPageCreateBonus(ui.ScriptWindow):
	def __init__(self):
		ui.ScriptWindow.__init__(self)
		self.__Initialize()
		self.__LoadWindow()
	
	def __Initialize(self):
		self.base_pos = (0, 0)
		self.bonus_name = None
		self.bonus_value = None
		self.apply_value = None
	
	def __del__(self):
		ui.ScriptWindow.__del__(self)
	
	def __LoadWindow(self):
		pyScrLoader = ui.PythonScriptLoader()
		pyScrLoader.LoadScriptFile(self, "UIScript/characterwindowbonusstruct.py")
		self.bonus_name = self.GetChild("bonus_name")
		self.bonus_value = self.GetChild("bonus_value")
		
		return self
	
	def SetBasePosition(self, x, y):
		self.base_pos = (x, y)
		self.SetPosition(x, y)
	
	def GetBasePosition(self):
		return self.base_pos
	
	def SetName(self, name):
		self.bonus_name.SetText(str(name))
	
	def SetApplyValue(self, value):
		self.apply_value = value
	
	def RefreshApplyValue(self):
		if self.apply_value != None:
			value = 0
	#		if self.apply_value == -1:
	#			value = player.GetStatus(player.POINT_BLUE_PLAYER_KILLED) + player.GetStatus(player.POINT_YELLOW_PLAYER_KILLED) + player.GetStatus(player.POINT_RED_PLAYER_KILLED)
	#		else:
			value = player.GetStatus(self.apply_value)
			self.bonus_value.SetText("{}".format(value))

class CharacterWindow(ui.ScriptWindow):

	ACTIVE_PAGE_SLOT_COUNT = 8
	SUPPORT_PAGE_SLOT_COUNT = 12

	PAGE_SLOT_COUNT = 12
	PAGE_HORSE = 2

	SKILL_GROUP_NAME_DICT = {
		playersettingmodule.JOB_WARRIOR	: { 1 : localeInfo.SKILL_GROUP_WARRIOR_1,	2 : localeInfo.SKILL_GROUP_WARRIOR_2, },
		playersettingmodule.JOB_ASSASSIN	: { 1 : localeInfo.SKILL_GROUP_ASSASSIN_1,	2 : localeInfo.SKILL_GROUP_ASSASSIN_2, },
		playersettingmodule.JOB_SURA		: { 1 : localeInfo.SKILL_GROUP_SURA_1,		2 : localeInfo.SKILL_GROUP_SURA_2, },
		playersettingmodule.JOB_SHAMAN		: { 1 : localeInfo.SKILL_GROUP_SHAMAN_1,	2 : localeInfo.SKILL_GROUP_SHAMAN_2, },
	}
	if app.ENABLE_WOLFMAN_CHARACTER:
		SKILL_GROUP_NAME_DICT.update({playersettingmodule.JOB_WOLFMAN		: { 1 : localeInfo.JOB_WOLFMAN1,	2 : localeInfo.JOB_WOLFMAN2, },})

	STAT_DESCRIPTION =	{
		"HTH" : localeInfo.STAT_TOOLTIP_CON,
		"INT" : localeInfo.STAT_TOOLTIP_INT,
		"STR" : localeInfo.STAT_TOOLTIP_STR,
		"DEX" : localeInfo.STAT_TOOLTIP_DEX,
	}

	IMAGE_DESCRIPTION =	{
		"MSPD"	: localeInfo.STAT_TOOLTIP_MOVE_SPEED,
		"ASPD"	: localeInfo.STAT_TOOLTIP_ATT_SPEED,
		"CSPD"	: localeInfo.STAT_TOOLTIP_CAST_SPEED,
		"MATT"	: localeInfo.STAT_TOOLTIP_MAG_ATT,
		"MDEF"	: localeInfo.STAT_TOOLTIP_MAG_DEF,
		"ER"	: localeInfo.STAT_TOOLTIP_DEX,
		"DEX"	: localeInfo.STAT_TOOLTIP_IMG_DEX,
		"STR"	: localeInfo.STAT_TOOLTIP_IMG_STR,
		"INT"	: localeInfo.STAT_TOOLTIP_IMG_INT,
		"HTH"	: localeInfo.STAT_TOOLTIP_IMG_CON,
		"DEF"	: localeInfo.STAT_TOOLTIP_DEF,
		"ATT"	: localeInfo.STAT_TOOLTIP_ATT,
		"SP"	: localeInfo.STAT_TOOLTIP_SP,
		"HEL"	: localeInfo.STAT_TOOLTIP_CON,
	}
	
	TAB_DESC =	{
		"STATUS"	: localeInfo.STAT_TOOLTIP_TAB_CHARACTER,
		"SKILL"		: localeInfo.STAT_TOOLTIP_TAB_SKILL,
		"EMOTICON"	: localeInfo.STAT_TOOLTIP_TAB_EMOTICON,
		"QUEST"		: localeInfo.STAT_TOOLTIP_TAB_QUEST,
	}
	NEWBUTTONS_DESC =	{
		"STAT"		: localeInfo.STAT_TOOLTIP_STAT,
		"POINTS_ACTIVE"	: localeInfo.STAT_TOOLTIP_POINT,
		"POINTS_SUPPORT": localeInfo.STAT_TOOLTIP_POINT,
		"POINTS_STATUS"	: localeInfo.STAT_TOOLTIP_POINT,
	}
	STAT_MINUS_DESCRIPTION = localeInfo.STAT_MINUS_DESCRIPTION

	def __init__(self):
		ui.ScriptWindow.__init__(self)
		self.state = "STATUS"
		self.isLoaded = 0

		self.toolTipSkill = 0
		self.NewEmotionWait = 0
		self.character_actual_page = 0

		self.__Initialize()
		self.__LoadWindow()

		self.statusPlusCommandDict={
			"HTH" : "/stat ht",
			"INT" : "/stat iq",
			"STR" : "/stat st",
			"DEX" : "/stat dx",
		}

		self.statusMinusCommandDict={
			"HTH-" : "/stat- ht",
			"INT-" : "/stat- iq",
			"STR-" : "/stat- st",
			"DEX-" : "/stat- dx",
		}

	def __del__(self):
		ui.ScriptWindow.__del__(self)

	def __Initialize(self):
		self.refreshToolTip = 0
		self.curSelectedSkillGroup = 0
		self.canUseHorseSkill = -1

		self.toolTip = None
		self.toolTipJob = None
		self.toolTipAlignment = None
		self.toolTipTest = None
		self.toolTipSkill = None

		self.faceImage = None
		self.statusPlusLabel = None
		self.statusPlusValue = None
		self.activeSlot = None
		self.newButtonsDict = None
		self.tabDict = None
		self.imageDict = None
		self.tabButtonDict = None
		self.tabCharacterPageDict = None
		self.pageDict = None
		self.titleBarDict = None
		self.statusPlusButtonDict = None
		self.statusMinusButtonDict = None

		self.skillPageDict = None
		self.questShowingStartIndex = 0
		self.questScrollBar = None
		self.questSlot = None
		self.questNameList = None
		self.questLastTimeList = None
		self.questLastCountList = None
		self.skillGroupButton = ()

		self.bonusPageItemsInfo = {}
		self.bonusPageObjectManage = {}
		self.bonusPageCategoryList = []
		self.bonusPageCategoryBasePos = []
		self.bonusPageObjectList = []
		self.bonusPageSelectedCategory = -1
		
		self.activeSlot = None
		self.activeSkillPointValue = None
		self.supportSkillPointValue = None
		self.skillGroupButton1 = None
		self.skillGroupButton2 = None
		self.activeSkillGroupName = None

		self.guildNameSlot = None
		self.guildNameValue = None
		self.characterNameSlot = None
		self.characterNameValue = None

		self.emotionToolTip = None
		self.soloEmotionSlot = None
		self.premiumEmotionSlot = None
		self.dualEmotionSlot = None

	def Show(self):
		self.__LoadWindow()
		ui.ScriptWindow.Show(self)

	def __LoadScript(self, fileName):
		pyScrLoader = ui.PythonScriptLoader()
		pyScrLoader.LoadScriptFile(self, fileName)	
		
	def __BindObject(self):
		self.toolTip = uiToolTip.ToolTip()
		self.toolTipJob = uiToolTip.ToolTip()
		self.toolTipAlignment = uiToolTip.ToolTip(130)		
		self.toolTipTest = uiToolTip.ToolTip()

		self.faceImage = self.GetChild("Face_Image")

		faceSlot=self.GetChild("Face_Slot")
		self.statusPlusLabel = self.GetChild("Status_Plus_Label")
		self.statusPlusValue = self.GetChild("Status_Plus_Value")

		self.characterNameSlot = self.GetChild("Character_Name_Slot")
		self.characterNameValue = self.GetChild("Character_Name")
		self.guildNameSlot = self.GetChild("Guild_Name_Slot")
		self.guildNameValue = self.GetChild("Guild_Name")
		self.characterNameSlot.SAFE_SetStringEvent("MOUSE_OVER_IN", self.__ShowAlignmentToolTip)
		self.characterNameSlot.SAFE_SetStringEvent("MOUSE_OVER_OUT", self.__HideAlignmentToolTip)

		self.activeSlot = self.GetChild("Skill_Active_Slot")
		self.activeSkillPointValue = self.GetChild("Active_Skill_Point_Value")
		self.supportSkillPointValue = self.GetChild("Support_Skill_Point_Value")
		self.skillGroupButton1 = self.GetChild("Skill_Group_Button_1")
		self.skillGroupButton2 = self.GetChild("Skill_Group_Button_2")
		self.activeSkillGroupName = self.GetChild("Active_Skill_Group_Name")

		self.tabDict = {
			"STATUS"	: self.GetChild("Tab_01"),
			"SKILL"		: self.GetChild("Tab_02"),
			"EMOTICON"	: self.GetChild("Tab_03"),
			"QUEST"		: self.GetChild("Tab_04"),
		}	
		
		self.newButtonsDict = {
			"STAT"		: self.GetChild("Char_Info_Status_img"),
			"POINTS_ACTIVE"	: self.GetChild("Active_Skill_Point_Label"),
			"POINTS_SUPPORT": self.GetChild("Support_Skill_Point_Label"),
			"POINTS_STATUS"	: self.GetChild("Status_Plus_Label"),
		}

		self.imageDict = {
			"MSPD"	: self.GetChild("MSPD_IMG"),
			"ASPD"	: self.GetChild("ASPD_IMG"),
			"CSPD"	: self.GetChild("CSPD_IMG"),
			"MATT"	: self.GetChild("MATT_IMG"),
			"MDEF"	: self.GetChild("MDEF_IMG"),
			"ER"	: self.GetChild("ER_IMG"),
			"DEX"	: self.GetChild("DEX_IMG"),
			"STR"	: self.GetChild("STR_IMG"),
			"INT"	: self.GetChild("INT_IMG"),
			"HTH"	: self.GetChild("HTH_IMG"),
			"DEF"	: self.GetChild("DEF_IMG"),
			"ATT"	: self.GetChild("ATT_IMG"),
			"SP"	: self.GetChild("SP_IMG"),
			"HEL"	: self.GetChild("HEL_IMG"),

		}

		self.tabButtonDict = {
			"STATUS"	: self.GetChild("Tab_Button_01"),
			"SKILL"		: self.GetChild("Tab_Button_02"),
			"EMOTICON"	: self.GetChild("Tab_Button_03"),
			"QUEST"		: self.GetChild("Tab_Button_04")
		}

		self.tabCharacterPageDict = {
			0	: self.GetChild("change_status_button"),
			1	: self.GetChild("change_bonus_button"),
			# 2	: self.GetChild("change_other_button"),
		}


		self.pageDict = {
			"STATUS"	: self.GetChild("Character_Page"),
			"SKILL"		: self.GetChild("Skill_Page"),
			"EMOTICON"	: self.GetChild("Emoticon_Page"),
			"QUEST"		: self.GetChild("Quest_Page")
		}

		self.titleBarDict = {
			"STATUS"	: self.GetChild("Character_TitleBar"),
			"SKILL"		: self.GetChild("Skill_TitleBar"),
			"EMOTICON"	: self.GetChild("Emoticon_TitleBar"),
			"QUEST"		: self.GetChild("Quest_TitleBar")
		}

		self.statusPlusButtonDict = {
			"HTH"		: self.GetChild("HTH_Plus"),
			"INT"		: self.GetChild("INT_Plus"),
			"STR"		: self.GetChild("STR_Plus"),
			"DEX"		: self.GetChild("DEX_Plus"),
		}

		self.statusMinusButtonDict = {
			"HTH-"		: self.GetChild("HTH_Minus"),
			"INT-"		: self.GetChild("INT_Minus"),
			"STR-"		: self.GetChild("STR_Minus"),
			"DEX-"		: self.GetChild("DEX_Minus"),
		}

		self.skillPageDict = {
			"ACTIVE" : self.GetChild("Skill_Active_Slot"),
			"SUPPORT" : self.GetChild("Skill_ETC_Slot"),
			"HORSE" : self.GetChild("Skill_Active_Slot"),
		}

		self.skillPageStatDict = {
			"SUPPORT"	: player.SKILL_SUPPORT,
			"ACTIVE"	: player.SKILL_ACTIVE,
			"HORSE"		: player.SKILL_HORSE,
		}

		self.skillGroupButton = (
			self.GetChild("Skill_Group_Button_1"),
			self.GetChild("Skill_Group_Button_2"),
		)

		self.characterPageDict = {
			0 : self.GetChild("status_window"),
			1 : self.GetChild("bonus_window"),
			# 2 : self.GetChild("special_other_window")
		}

		self.bonusPageItemsInfo = {
			0 : {
				"Bonusuri ofensive" :
				[
					(localeInfo.DETAILS_1, item.GetApplyPoint(item.APPLY_ATTBONUS_HUMAN)),
					(localeInfo.DETAILS_3, item.GetApplyPoint(item.APPLY_ATTBONUS_ORC)),
					(localeInfo.DETAILS_4, item.GetApplyPoint(item.APPLY_ATTBONUS_UNDEAD)),
					(localeInfo.DETAILS_5, item.GetApplyPoint(item.APPLY_ATTBONUS_MONSTER)),
					(localeInfo.DETAILS_7, item.GetApplyPoint(item.APPLY_ATTBONUS_ANIMAL)),
					(localeInfo.DETAILS_8, item.GetApplyPoint(item.APPLY_ATTBONUS_MILGYO)),
					(localeInfo.DETAILS_9, item.GetApplyPoint(item.APPLY_ATTBONUS_DEVIL)),
					(localeInfo.DETAILS_10, 158),
					(localeInfo.DETAILS_11, 157),
					(localeInfo.DETAILS_12, item.GetApplyPoint(item.APPLY_ATT_GRADE_BONUS)),
					(localeInfo.DETAILS_14, item.GetApplyPoint(item.APPLY_NORMAL_HIT_DAMAGE_BONUS)),
					(localeInfo.DETAILS_16, item.GetApplyPoint(item.APPLY_SKILL_DAMAGE_BONUS)),
					(localeInfo.DETAILS_19, item.GetApplyPoint(item.APPLY_MAGIC_ATTBONUS_PER)),
					(localeInfo.DETAILS_20, item.GetApplyPoint(item.APPLY_CRITICAL_PCT)),
					(localeInfo.DETAILS_21, item.GetApplyPoint(item.APPLY_PENETRATE_PCT)),
					(localeInfo.DETAILS_78, 138),
					(localeInfo.DETAILS_79, 51),
					(localeInfo.DETAILS_80, 141),
					(localeInfo.DETAILS_81, 50),
					(localeInfo.DETAILS_82, 139),
					(localeInfo.DETAILS_83, 140),
					(localeInfo.DETAILS_36, item.GetApplyPoint(item.APPLY_ATTBONUS_WARRIOR)),
					(localeInfo.DETAILS_37, item.GetApplyPoint(item.APPLY_ATTBONUS_ASSASSIN)),
					(localeInfo.DETAILS_38, item.GetApplyPoint(item.APPLY_ATTBONUS_SURA)),
					(localeInfo.DETAILS_39, item.GetApplyPoint(item.APPLY_ATTBONUS_SHAMAN)),
					(localeInfo.DETAILS_40, item.GetApplyPoint(item.APPLY_ATTBONUS_WOLFMAN)),
				],
			},
			1 : {
				"Bonusuri defensive" :
				[
					(localeInfo.DETAILS_13, item.GetApplyPoint(item.APPLY_DEF_GRADE_BONUS)),
					(localeInfo.DETAILS_15, item.GetApplyPoint(item.APPLY_NORMAL_HIT_DEFEND_BONUS)),
					(localeInfo.DETAILS_17, item.GetApplyPoint(item.APPLY_SKILL_DEFEND_BONUS)),
					(localeInfo.DETAILS_76, item.GetApplyPoint(item.APPLY_RESIST_MAGIC)),
					(localeInfo.DETAILS_41, item.GetApplyPoint(item.APPLY_RESIST_WARRIOR)),
					(localeInfo.DETAILS_42, item.GetApplyPoint(item.APPLY_RESIST_ASSASSIN)),
					(localeInfo.DETAILS_43, item.GetApplyPoint(item.APPLY_RESIST_SURA)),
					(localeInfo.DETAILS_44, item.GetApplyPoint(item.APPLY_RESIST_SHAMAN)),
					(localeInfo.DETAILS_45, item.GetApplyPoint(item.APPLY_RESIST_WOLFMAN)),
					(localeInfo.DETAILS_90, item.GetApplyPoint(item.APPLY_RESIST_HUMAN)),
					(localeInfo.DETAILS_46, item.GetApplyPoint(item.APPLY_RESIST_SWORD)),
					(localeInfo.DETAILS_48, item.GetApplyPoint(item.APPLY_RESIST_TWOHAND)),
					(localeInfo.DETAILS_47, item.GetApplyPoint(item.APPLY_RESIST_DAGGER)),
					(localeInfo.DETAILS_50, item.GetApplyPoint(item.APPLY_RESIST_BELL)),
					(localeInfo.DETAILS_51, item.GetApplyPoint(item.APPLY_RESIST_FAN)),
					(localeInfo.DETAILS_52, item.GetApplyPoint(item.APPLY_RESIST_BOW)),
				],
			},
			2 : {
				"Alte bonusuri" :
				[
					(localeInfo.DETAILS_53, item.GetApplyPoint(item.APPLY_STUN_PCT)),
					(localeInfo.DETAILS_54, item.GetApplyPoint(item.APPLY_SLOW_PCT)),
					(localeInfo.DETAILS_55, item.GetApplyPoint(item.APPLY_POISON_PCT)),
					(localeInfo.DETAILS_56, item.GetApplyPoint(item.APPLY_POISON_REDUCE)),
					(localeInfo.DETAILS_59, item.GetApplyPoint(item.APPLY_STEAL_HP)),
					(localeInfo.DETAILS_60, item.GetApplyPoint(item.APPLY_STEAL_SP)),
					(localeInfo.DETAILS_61, item.GetApplyPoint(item.APPLY_HP_REGEN)),
					(localeInfo.DETAILS_62, item.GetApplyPoint(item.APPLY_SP_REGEN)),
					(localeInfo.DETAILS_63, item.GetApplyPoint(item.APPLY_BLOCK)),
					(localeInfo.DETAILS_64, item.GetApplyPoint(item.APPLY_DODGE)),
					(localeInfo.DETAILS_65, item.GetApplyPoint(item.APPLY_REFLECT_MELEE)),
					(localeInfo.DETAILS_66, item.GetApplyPoint(item.APPLY_KILL_HP_RECOVER)),
					(localeInfo.DETAILS_67, item.GetApplyPoint(item.APPLY_KILL_SP_RECOVER)),
					(localeInfo.DETAILS_68, item.GetApplyPoint(item.APPLY_EXP_DOUBLE_BONUS)),
					(localeInfo.DETAILS_69, item.GetApplyPoint(item.APPLY_GOLD_DOUBLE_BONUS)),
					(localeInfo.DETAILS_70, item.GetApplyPoint(item.APPLY_ITEM_DROP_BONUS)),
				],
			},
			3 : {
				"Bonusuri procentuale" :
				[
					(localeInfo.DETAILS_71, item.GetApplyPoint(item.APPLY_MALL_ATTBONUS)),
					(localeInfo.DETAILS_72, item.GetApplyPoint(item.APPLY_MALL_DEFBONUS)),
					(localeInfo.DETAILS_73, item.GetApplyPoint(item.APPLY_MALL_EXPBONUS)),
					(localeInfo.DETAILS_74, item.GetApplyPoint(item.APPLY_MALL_ITEMBONUS)),
					(localeInfo.DETAILS_75, item.GetApplyPoint(item.APPLY_MALL_GOLDBONUS)),
				],
			},
		}

		self.bonusPageObjectManage = {
			"label" : self.GetChild("bonus_base_image"),
			"scrollbar" : self.GetChild("bonus_scrollbar"),
			"max_height" : 213,
			"scroll_distance" : 0,
		}
		self.bonusPageObjectManage["scrollbar"].Hide()

		global SHOW_ONLY_ACTIVE_SKILL
		global HIDE_SUPPORT_SKILL_POINT
		if SHOW_ONLY_ACTIVE_SKILL or HIDE_SUPPORT_SKILL_POINT:
			self.GetChild("Support_Skill_Point_Label").Hide()
		
		self.soloEmotionSlot = self.GetChild("SoloEmotionSlot")
		self.premiumEmotionSlot = self.GetChild("PremiumEmotionSlot")
		self.dualEmotionSlot = self.GetChild("DualEmotionSlot")
		self.__SetEmotionSlot()

		self.questShowingStartIndex = 0
		self.questScrollBar = self.GetChild("Quest_ScrollBar")
		self.questScrollBar.SetScrollEvent(ui.__mem_func__(self.OnQuestScroll))
		self.questSlot = self.GetChild("Quest_Slot")
		for i in xrange(quest.QUEST_MAX_NUM):
			self.questSlot.HideSlotBaseImage(i)
			self.questSlot.SetCoverButton(i,\
											"d:/ymir work/ui/game/quest/slot_button_01.sub",\
											"d:/ymir work/ui/game/quest/slot_button_02.sub",\
											"d:/ymir work/ui/game/quest/slot_button_03.sub",\
											"d:/ymir work/ui/game/quest/slot_button_03.sub", True)

		self.questNameList = []
		self.questLastTimeList = []
		self.questLastCountList = []
		for i in xrange(quest.QUEST_MAX_NUM):
			self.questNameList.append(self.GetChild("Quest_Name_0" + str(i)))
			self.questLastTimeList.append(self.GetChild("Quest_LastTime_0" + str(i)))
			self.questLastCountList.append(self.GetChild("Quest_LastCount_0" + str(i)))

	def __SetSkillSlotEvent(self):
		for skillPageValue in self.skillPageDict.itervalues():
			skillPageValue.SetSlotStyle(wndMgr.SLOT_STYLE_NONE)
			skillPageValue.SetSelectItemSlotEvent(ui.__mem_func__(self.SelectSkill))
			skillPageValue.SetSelectEmptySlotEvent(ui.__mem_func__(self.SelectEmptySlot))
			skillPageValue.SetUnselectItemSlotEvent(ui.__mem_func__(self.ClickSkillSlot))
			skillPageValue.SetUseSlotEvent(ui.__mem_func__(self.ClickSkillSlot))
			skillPageValue.SetOverInItemEvent(ui.__mem_func__(self.OverInItem))
			skillPageValue.SetOverOutItemEvent(ui.__mem_func__(self.OverOutItem))
			skillPageValue.SetPressedSlotButtonEvent(ui.__mem_func__(self.OnPressedSlotButton))
			skillPageValue.AppendSlotButton("d:/ymir work/ui/game/windows/btn_plus_up.sub",\
											"d:/ymir work/ui/game/windows/btn_plus_over.sub",\
											"d:/ymir work/ui/game/windows/btn_plus_down.sub")
	def __SetEmotionSlot(self):
		self.emotionToolTip = uiToolTip.ToolTipEmotion()
		#self.emotionToolTip.ModelPreview()

		for slot in (self.soloEmotionSlot, self.premiumEmotionSlot, self.dualEmotionSlot):
			slot.SetSlotStyle(wndMgr.SLOT_STYLE_NONE)
			slot.SetSelectItemSlotEvent(ui.__mem_func__(self.__SelectEmotion))
			slot.SetUnselectItemSlotEvent(ui.__mem_func__(self.__ClickEmotionSlot))
			slot.SetUseSlotEvent(ui.__mem_func__(self.__ClickEmotionSlot))
			slot.SetOverInItemEvent(ui.__mem_func__(self.__OverInEmotion))
			slot.SetOverOutItemEvent(ui.__mem_func__(self.__OverOutEmotion))
			slot.AppendSlotButton("d:/ymir work/ui/game/windows/btn_plus_up.sub",\
											"d:/ymir work/ui/game/windows/btn_plus_over.sub",\
											"d:/ymir work/ui/game/windows/btn_plus_down.sub")

		for slotIdx, datadict in emotion.EMOTION_DICT.items():
			emotionIdx = slotIdx

			slot = self.soloEmotionSlot
			
			if slotIdx > 50:
				slot = self.dualEmotionSlot

			if slotIdx > 59:
				slot = self.premiumEmotionSlot
				slot.DisableCoverButton(slotIdx)

			slot.SetEmotionSlot(slotIdx, emotionIdx)
			slot.SetCoverButton(slotIdx)

	def __SelectEmotion(self, slotIndex):
		if not slotIndex in emotion.EMOTION_DICT:
			return

		if app.IsPressed(app.DIK_LCONTROL):
			player.RequestAddToEmptyLocalQuickSlot(player.SLOT_TYPE_EMOTION, slotIndex)
			return

		mouseModule.mouseController.AttachObject(self, player.SLOT_TYPE_EMOTION, slotIndex, slotIndex)

	def __ClickEmotionSlot(self, slotIndex):
		print "click emotion"
		if not slotIndex in emotion.EMOTION_DICT:
			return

		print "check acting"
		if player.IsActingEmotion():
			return

		command = emotion.EMOTION_DICT[slotIndex]["command"]
		print "command", command
		
		if slotIndex > 50 and slotIndex < 54:
		# if slotIndex > 50:
			vid = player.GetTargetVID()

			if 0 == vid or vid == player.GetMainCharacterIndex() or chr.IsNPC(vid) or chr.IsEnemy(vid):
				import chat
				chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.EMOTION_CHOOSE_ONE)
				return

			command += " " + chr.GetNameByVID(vid)

		print "send_command", command
		net.SendChatPacket(command)

	def ActEmotion(self, emotionIndex):
		self.__ClickEmotionSlot(emotionIndex)

	def __OverInEmotion(self, slotIndex):
		if self.emotionToolTip:

			if not slotIndex in emotion.EMOTION_DICT:
				return

			self.emotionToolTip.ClearToolTip()
			self.emotionToolTip.SetTitle(emotion.EMOTION_DICT[slotIndex]["name"])
			self.emotionToolTip.AlignHorizonalCenter()
			if not emotion.EMOTION_DICT[slotIndex]["emotion_key"] == 255:
				self.emotionToolTip.ModelPreviewEmotion(emotion.EMOTION_DICT[slotIndex]["emotion_key"])
			self.emotionToolTip.ShowToolTip()

	def __OverOutEmotion(self):
		if self.emotionToolTip:
			self.emotionToolTip.HideToolTip()
			self.emotionToolTip.ModelPreviewClose()

	def __BindEvent(self):
		for i in xrange(len(self.skillGroupButton)):
			self.skillGroupButton[i].SetEvent(lambda arg=i: self.__SelectSkillGroup(arg))

		self.RefreshQuest()
		self.__HideJobToolTip()
		
		for (tabCharacterKey, tabCharacterButton) in self.tabCharacterPageDict.items():
			tabCharacterButton.SetEvent(ui.__mem_func__(self.SetStatusPage), tabCharacterKey)

		for (tabKey, tabButton) in self.tabButtonDict.items():
			tabButton.SetEvent(ui.__mem_func__(self.__OnClickTabButton), tabKey)
			tabButton.ShowToolTip = lambda arg=tabKey: self.__OverInTabFunc(arg)
			tabButton.HideToolTip = lambda arg=tabKey: self.__OverOutImageFunc()
			
		for (statusPlusKey, statusPlusButton) in self.statusPlusButtonDict.items():
			statusPlusButton.SAFE_SetEvent(self.__OnClickStatusPlusButton, statusPlusKey)
			statusPlusButton.ShowToolTip = lambda arg=statusPlusKey: self.__OverInStatButton(arg)
			statusPlusButton.HideToolTip = lambda arg=statusPlusKey: self.__OverOutStatButton()

		for (imagePlusKey, imagePlus) in self.imageDict.items():
			imagePlus.ShowToolTip = lambda arg=imagePlusKey: self.__OverInImageFunc(arg)
			imagePlus.HideToolTip = lambda arg=imagePlusKey: self.__OverOutImageFunc()
			
		for (newButtonsPlusKey, newButtonsPlus) in self.newButtonsDict.items():
			newButtonsPlus.ShowToolTip = lambda arg=newButtonsPlusKey: self.__OverInNewButtonsFunc(arg)
			newButtonsPlus.HideToolTip = lambda arg=newButtonsPlusKey: self.__OverOutImageFunc()

		for (statusMinusKey, statusMinusButton) in self.statusMinusButtonDict.items():
			statusMinusButton.SAFE_SetEvent(self.__OnClickStatusMinusButton, statusMinusKey)
			statusMinusButton.ShowToolTip = lambda arg=statusMinusKey: self.__OverInStatMinusButton(arg)
			statusMinusButton.HideToolTip = lambda arg=statusMinusKey: self.__OverOutStatMinusButton()

		for titleBarValue in self.titleBarDict.itervalues():
			titleBarValue.SetCloseEvent(ui.__mem_func__(self.Close))

		self.questSlot.SetSelectItemSlotEvent(ui.__mem_func__(self.__SelectQuest))

		self.bonusPageObjectManage["scrollbar"].SetScrollEvent(ui.__mem_func__(self.__OnScrollBonusPage))

	def __LoadWindow(self):
		if self.isLoaded == 1:
			return

		self.isLoaded = 1

		try:
			self.__LoadScript("UIScript/CharacterWindow_Norm.py")

			self.__BindObject()
			self.__BindEvent()
		except:
			import exception
			exception.Abort("CharacterWindow.__LoadWindow")

		self.SetState("STATUS")
		self.SetStatusPage(self.character_actual_page)
		self.__LoadBonusPagesCategory()

	def Destroy(self):
		self.ClearDictionary()
		self.__Initialize()
		
	def OnRunMouseWheel(self, nLen):
		if nLen > 0:
			self.GetChild("bonus_scrollbar").OnUp()
		else:
			self.GetChild("bonus_scrollbar").OnDown()
			
	########################################
	########################################
	########################################
	########################################
	########################################
	########################################
	########################################
	########################################
	OBJECT_PARM_HEIGHT = 20

	def __LoadBonusPagesCategory(self):
		for (index, info) in self.bonusPageItemsInfo.items():
			name = list(info.keys())[0]
			bonus = info[name]
			separator = ui.SubTitleBar()
			separator.SetParent(self.bonusPageObjectManage["label"])
			separator.MakeSubTitleBar(210, "red")
			separator.SetSize(210, 16)
			separator.SetPosition(3, 3+(18 * index) + (2 * index))
			separator.SetTextAlignLeft(name)
			separator.SetQuestLabel(quest_lable_expend_img_path_dict[index], len(bonus))
			separator.SetMiniImageNorm("d:/ymir work/ui/game/windows/red_icon_bonus.sub")
			separator.SetMiniImageOpen("d:/ymir work/ui/game/windows/red_icon_bonus.sub")
			separator.SetEvent(ui.__mem_func__(self.__OnClickBonusPageSeparator), index, bonus)
			separator.Show()
			self.bonusPageCategoryList.append((separator, bonus))
	
	def GetBonusBoardEndPosition(self):
		return self.bonusPageObjectManage["max_height"]
	
	def GetFirstBonusPageObjectPosition(self):
		return (self.bonusPageCategoryList[0][0].GetLocalPosition()[1])
	
	def GetLastBonusPageObjectPosition(self):
		if (self.bonusPageSelectedCategory +1) == len(self.bonusPageCategoryList):
			return (self.bonusPageObjectList[-1].GetLocalPosition()[1] + self.OBJECT_PARM_HEIGHT)
		
		return (self.bonusPageCategoryList[-1][0].GetLocalPosition()[1] + self.bonusPageCategoryList[-1][0].GetHeight())
	
	def GetOpenedCategorySize(self):
		return (self.bonusPageObjectList[-1].GetLocalPosition()[1] + self.OBJECT_PARM_HEIGHT) - self.bonusPageObjectList[0].GetLocalPosition()[1]
	
	def RefreshCategoryBasePosition(self):
		self.bonusPageCategoryBasePos = []
		for (label, _) in self.bonusPageCategoryList:
			self.bonusPageCategoryBasePos.append(label.GetLocalPosition())
	
	def RefreshScrollDistance(self):
		distance = self.GetLastBonusPageObjectPosition() - self.GetBonusBoardEndPosition()
		self.bonusPageObjectManage["scroll_distance"] = distance
	
	def RefreshScrollBarState(self):
		self.bonusPageObjectManage["scrollbar"].SetPos(0)
		canShowScroll = bool(self.GetLastBonusPageObjectPosition() > self.GetBonusBoardEndPosition())
		self.bonusPageObjectManage["scrollbar"].Show() if canShowScroll else self.bonusPageObjectManage["scrollbar"].Hide()
	
	def RefreshBonusPageItemInfo(self):
		for bonusObject in self.bonusPageObjectList:
			bonusObject.RefreshApplyValue()
	
	def CloseAllBonusPageCat(self):
		for object in self.bonusPageObjectList:	object.Hide()
		for ((label, _), index) in zip(self.bonusPageCategoryList, xrange(len(self.bonusPageCategoryList))):
			label.SetPosition(3, 3+(18 * index) + (2 * index))
			label.Show()
			label.SetTop()
		
		self.bonusPageObjectList = []
	
	def SetBonusPageCategory(self, category):
		self.bonusPageSelectedCategory = category
	
	def __OnClickBonusPageSeparator(self, catIndex, bonus):
		if self.bonusPageSelectedCategory == catIndex:
			self.SetBonusPageCategory(-1)
			self.CloseAllBonusPageCat()
			self.bonusPageObjectManage["scrollbar"].Hide()
			return
		
		self.CloseAllBonusPageCat()
		self.SetBonusPageCategory(catIndex)
		
		catLabel = self.bonusPageCategoryList[catIndex][0]
		catLabel_x, catLabel_y = catLabel.GetLocalPosition()
		
		for (bonus_info, index) in zip(bonus, xrange(len(bonus))):
			tmpCreatedObject = CharacterPageCreateBonus()
			tmpCreatedObject.SetParent(self.bonusPageObjectManage["label"])
			tmpCreatedObject.SetBasePosition(catLabel_x, catLabel_y + 25 + (self.OBJECT_PARM_HEIGHT* index) + (3 * index))
			bonusDesc, bonusType = bonus_info
			tmpCreatedObject.SetName(bonusDesc)
			tmpCreatedObject.SetApplyValue(bonusType)
			tmpCreatedObject.RefreshApplyValue()
			tmpCreatedObject.Show()
			tmpCreatedObject.SetTop()
			self.bonusPageObjectList.append(tmpCreatedObject)
		
		
		

		categorySize = self.GetOpenedCategorySize()
		for ((label, _), labelKey) in zip(self.bonusPageCategoryList, xrange(len(self.bonusPageCategoryList))):
			if labelKey <= catIndex:	continue
			
			label_x, label_y = label.GetLocalPosition()
			label.SetPosition(label_x, label_y + categorySize + (self.OBJECT_PARM_HEIGHT/2))
		
		self.RefreshCategoryBasePosition()
		self.RefreshScrollDistance()
		self.RefreshScrollBarState()
		self.CheckBonusPageRect()
	
	def __OnScrollBonusPage(self):
		scrollDistance = self.bonusPageObjectManage["scroll_distance"]
		scrollPos = self.bonusPageObjectManage["scrollbar"].GetPos()
		
		heightDistance = scrollPos * scrollDistance
		
		for bonusObject in self.bonusPageObjectList:
			bonusObject_x, bonusObject_y = bonusObject.GetBasePosition()
			bonusObject.SetPosition(bonusObject_x, bonusObject_y - heightDistance)
		
		for categoryKey in xrange(len(self.bonusPageCategoryList)):
			catObject = self.bonusPageCategoryList[categoryKey][0]
			category_x, category_y = self.bonusPageCategoryBasePos[categoryKey]
			catObject.SetPosition(category_x, category_y - heightDistance)
		
		self.CheckBonusPageRect()
	
	def CheckBonusPageRect(self):
		def CanShow(posY, height):
			if posY < 1 or posY + height > self.GetBonusBoardEndPosition():
				return False
			return True
		
		for bonusObject in self.bonusPageObjectList:
			bonusObject_x, bonusObject_y = bonusObject.GetLocalPosition()
			bonusObject_height = bonusObject.GetHeight()
			
			bonusObject.Show() if CanShow(bonusObject_y, bonusObject_height) else bonusObject.Hide()
		
		for (label, _) in self.bonusPageCategoryList:
			blabel_x, label_y = label.GetLocalPosition()
			label_height = label.GetHeight()
			
			label.Show() if CanShow(label_y, label_height) else label.Hide()
	
	########################################
	########################################
	########################################
	########################################
	########################################
	########################################
	########################################
	########################################

	def Close(self):
		if self.toolTipSkill:
			self.toolTipSkill.Hide()
	
		self.Hide()

	def SetSkillToolTip(self, toolTipSkill):
		self.toolTipSkill = toolTipSkill

	def __OnClickStatusPlusButton(self, statusKey):
		try:
			statusPlusCommand=self.statusPlusCommandDict[statusKey]
			if app.IsPressed(app.DIK_LCONTROL):
				if self.NewEmotionWait > app.GetTime():
					TimeFloat = float(self.NewEmotionWait - app.GetTime())
					import chat
					chat.AppendChat(1, localeInfo.CHAR_WAIT % (TimeFloat))
					return

				self.NewEmotionWait = app.GetTime() + 0.5
				statusPlusPoint = player.GetStatus(player.STAT)
				if statusPlusPoint > 0 and statusPlusPoint < 10:
					net.SendChatPacket(statusPlusCommand + " " + str(statusPlusPoint))
				elif statusPlusPoint > 0:
					net.SendChatPacket(statusPlusCommand + " 10")
			else:
				net.SendChatPacket(statusPlusCommand)
		except KeyError, msg:
			dbg.TraceError("CharacterWindow.__OnClickStatusPlusButton KeyError: %s", msg)

	def __OnClickStatusMinusButton(self, statusKey):
		try:
			statusMinusCommand=self.statusMinusCommandDict[statusKey]
			net.SendChatPacket(statusMinusCommand)
		except KeyError, msg:
			dbg.TraceError("CharacterWindow.__OnClickStatusMinusButton KeyError: %s", msg)


	def __OnClickTabButton(self, stateKey):
		self.SetState(stateKey)

	def GetStatusPage(self):
		return self.character_actual_page
	
	def SetStatusPage(self, statusPage):
		if self.state != "STATUS":
			return
		
		self.character_actual_page = statusPage
		for key, label in self.characterPageDict.items():
			label.Show() if key == statusPage else label.Hide()
		
		for key_b, button  in self.tabCharacterPageDict.items():
			button.SetUp() if key_b != statusPage else button.Down()

	def SetState(self, stateKey):

		self.state = stateKey

		for (tabKey, tabButton) in self.tabButtonDict.items():
			if stateKey!=tabKey:
				tabButton.SetUp()

		for tabValue in self.tabDict.itervalues():
			tabValue.Hide()

		for pageValue in self.pageDict.itervalues():
			pageValue.Hide()

		for titleBarValue in self.titleBarDict.itervalues():
			titleBarValue.Hide()
		
		if stateKey == "STATUS": #Reset status sub pages
			self.SetStatusPage(0)

		self.titleBarDict[stateKey].Show()
		self.tabDict[stateKey].Show()
		self.pageDict[stateKey].Show()

	def GetState(self):
		return self.state

	def __GetTotalAtkText(self):
		minAtk=player.GetStatus(player.ATT_MIN)
		maxAtk=player.GetStatus(player.ATT_MAX)
		atkBonus=player.GetStatus(player.ATT_BONUS)
		attackerBonus=player.GetStatus(player.ATTACKER_BONUS)

		if minAtk==maxAtk:
			return "%d" % (minAtk+atkBonus+attackerBonus)
		else:
			return "%d-%d" % (minAtk+atkBonus+attackerBonus, maxAtk+atkBonus+attackerBonus)

	def __GetTotalMagAtkText(self):
		minMagAtk=player.GetStatus(player.MAG_ATT)+player.GetStatus(player.MIN_MAGIC_WEP)
		maxMagAtk=player.GetStatus(player.MAG_ATT)+player.GetStatus(player.MAX_MAGIC_WEP)

		if minMagAtk==maxMagAtk:
			return "%s" % (localeInfo.AddPointToNumberString(minMagAtk))
		else:
			return "%s-%s" % (localeInfo.AddPointToNumberString(minMagAtk), localeInfo.AddPointToNumberString(maxMagAtk))

	def __GetTotalDefText(self):
		defValue=player.GetStatus(player.DEF_GRADE)
		if constInfo.ADD_DEF_BONUS_ENABLE:
			defValue+=player.GetStatus(player.DEF_BONUS)
		return "%s" % (localeInfo.AddPointToNumberString(defValue))
	
	def RefreshStatus(self):
		if self.isLoaded==0:
			return

		try:
			self.GetChild("Level_Value").SetText(str(player.GetStatus(player.LEVEL)))
			self.GetChild("Exp_Value").SetText(str(unsigned32(player.GetEXP())))
			self.GetChild("RestExp_Value").SetText(str(unsigned32(player.GetStatus(player.NEXT_EXP)) - unsigned32(player.GetStatus(player.EXP))))
			self.GetChild("HP_Value").SetText(localeInfo.AddPointToNumberString(player.GetStatus(player.HP)) + '/' + localeInfo.AddPointToNumberString(player.GetStatus(player.MAX_HP)))
			self.GetChild("SP_Value").SetText(localeInfo.AddPointToNumberString(player.GetStatus(player.SP)) + '/' + localeInfo.AddPointToNumberString(player.GetStatus(player.MAX_SP)))

			self.GetChild("STR_Value").SetText(str(player.GetStatus(player.ST)))
			self.GetChild("DEX_Value").SetText(str(player.GetStatus(player.DX)))
			self.GetChild("HTH_Value").SetText(str(player.GetStatus(player.HT)))
			self.GetChild("INT_Value").SetText(str(player.GetStatus(player.IQ)))

			self.GetChild("ATT_Value").SetText(self.__GetTotalAtkText())
			self.GetChild("DEF_Value").SetText(self.__GetTotalDefText())

			self.GetChild("MATT_Value").SetText(self.__GetTotalMagAtkText())
			#self.GetChild("MATT_Value").SetText(str(player.GetStatus(player.MAG_ATT)))

			self.GetChild("MDEF_Value").SetText(localeInfo.AddPointToNumberString(player.GetStatus(player.MAG_DEF)))
			self.GetChild("ASPD_Value").SetText(localeInfo.AddPointToNumberString(player.GetStatus(player.ATT_SPEED)))
			self.GetChild("MSPD_Value").SetText(localeInfo.AddPointToNumberString(player.GetStatus(player.MOVING_SPEED)))
			self.GetChild("CSPD_Value").SetText(localeInfo.AddPointToNumberString(player.GetStatus(player.CASTING_SPEED)))
			self.GetChild("ER_Value").SetText(localeInfo.AddPointToNumberString(player.GetStatus(player.EVADE_RATE)))

		except:
			pass

		self.__RefreshStatusPlusButtonList()
		self.__RefreshStatusMinusButtonList()
		self.RefreshAlignment()
		
		if self.refreshToolTip:
			self.refreshToolTip()

		self.RefreshBonusPageItemInfo()

	def __RefreshStatusPlusButtonList(self):
		if self.isLoaded==0:
			return

		statusPlusPoint=player.GetStatus(player.STAT)

		if statusPlusPoint>0:
			self.statusPlusValue.SetText(str(statusPlusPoint))
			self.statusPlusLabel.Show()
			self.ShowStatusPlusButtonList()
		else:
			self.statusPlusValue.SetText(str(0))
			self.statusPlusLabel.Hide()
			self.HideStatusPlusButtonList()

	def __RefreshStatusMinusButtonList(self):
		if self.isLoaded==0:
			return

		statusMinusPoint=self.__GetStatMinusPoint()

		if statusMinusPoint>0:
			self.__ShowStatusMinusButtonList()
		else:
			self.__HideStatusMinusButtonList()

	def RefreshAlignment(self):
		point, grade = player.GetAlignmentData()

		import colorInfo
		COLOR_DICT = {	0 : colorInfo.TITLE_RGB_GOOD_4,
						1 : colorInfo.TITLE_RGB_GOOD_3,
						2 : colorInfo.TITLE_RGB_GOOD_2,
						3 : colorInfo.TITLE_RGB_GOOD_1,
						4 : colorInfo.TITLE_RGB_NORMAL,
						5 : colorInfo.TITLE_RGB_EVIL_1,
						6 : colorInfo.TITLE_RGB_EVIL_2,
						7 : colorInfo.TITLE_RGB_EVIL_3,
						8 : colorInfo.TITLE_RGB_EVIL_4,
						9 : colorInfo.TITLE_RGB_SA,
						10 : colorInfo.TITLE_RGB_CM,
						11 : colorInfo.TITLE_RGB_YT,
						12 : colorInfo.TITLE_RGB_H,				
						13 : colorInfo.TITLE_RGB_DEV,}					
						
		colorList = COLOR_DICT.get(grade, colorInfo.TITLE_RGB_NORMAL)
		gradeColor = ui.GenerateColor(colorList[0], colorList[1], colorList[2])

		self.toolTipAlignment.ClearToolTip()
		self.toolTipAlignment.AutoAppendTextLine(localeInfo.TITLE_NAME_LIST[grade], gradeColor)
		self.toolTipAlignment.AutoAppendTextLine(localeInfo.ALIGNMENT_NAME + str(point))
		self.toolTipAlignment.AlignHorizonalCenter()

	def __ShowStatusMinusButtonList(self):
		for (stateMinusKey, statusMinusButton) in self.statusMinusButtonDict.items():
			statusMinusButton.Show()

	def __HideStatusMinusButtonList(self):
		for (stateMinusKey, statusMinusButton) in self.statusMinusButtonDict.items():
			statusMinusButton.Hide()

	def ShowStatusPlusButtonList(self):
		for (statePlusKey, statusPlusButton) in self.statusPlusButtonDict.items():
			statusPlusButton.Show()

	def HideStatusPlusButtonList(self):
		for (statePlusKey, statusPlusButton) in self.statusPlusButtonDict.items():
			statusPlusButton.Hide()

	def SelectSkill(self, skillSlotIndex):
		mouseController = mouseModule.mouseController

		if False == mouseController.isAttached():

			srcSlotIndex = self.__RealSkillSlotToSourceSlot(skillSlotIndex)
			selectedSkillIndex = player.GetSkillIndex(srcSlotIndex)

			if skill.CanUseSkill(selectedSkillIndex):

				if app.IsPressed(app.DIK_LCONTROL):

					player.RequestAddToEmptyLocalQuickSlot(player.SLOT_TYPE_SKILL, srcSlotIndex)
					return

				mouseController.AttachObject(self, player.SLOT_TYPE_SKILL, srcSlotIndex, selectedSkillIndex)

		else:

			mouseController.DeattachObject()

	def SelectEmptySlot(self, SlotIndex):
		mouseModule.mouseController.DeattachObject()

	## ToolTip
	def OverInItem(self, slotNumber):

		if mouseModule.mouseController.isAttached():
			return

		if 0 == self.toolTipSkill:
			return

		srcSlotIndex = self.__RealSkillSlotToSourceSlot(slotNumber)
		skillIndex = player.GetSkillIndex(srcSlotIndex)
		
		if 0 == skillIndex:
			return
		
		skillLevel = player.GetSkillLevel(srcSlotIndex)
		skillGrade = player.GetSkillGrade(srcSlotIndex)
		skillType = skill.GetSkillType(skillIndex)

		## ACTIVE
		if skill.SKILL_TYPE_ACTIVE == skillType:
			overInSkillGrade = self.__GetSkillGradeFromSlot(slotNumber)

			if overInSkillGrade == skill.SKILL_GRADE_COUNT-1 and skillGrade == skill.SKILL_GRADE_COUNT:
				self.toolTipSkill.SetSkillNew(srcSlotIndex, skillIndex, skillGrade, skillLevel)
			elif overInSkillGrade == skillGrade:
				self.toolTipSkill.SetSkillNew(srcSlotIndex, skillIndex, overInSkillGrade, skillLevel)
			else:
				self.toolTipSkill.SetSkillOnlyName(srcSlotIndex, skillIndex, overInSkillGrade)

		else:
			self.toolTipSkill.SetSkillNew(srcSlotIndex, skillIndex, skillGrade, skillLevel)

	def OverOutItem(self):
		if 0 != self.toolTipSkill:
			self.toolTipSkill.HideToolTip()

	## Quest
	def __SelectQuest(self, slotIndex):
		questIndex = quest.GetQuestIndex(self.questShowingStartIndex+slotIndex)

		import event
		event.QuestButtonClick(-2147483648 + questIndex)

	def RefreshQuest(self):

		if self.isLoaded==0:
			return

		questCount = quest.GetQuestCount()
		questRange = range(quest.QUEST_MAX_NUM)

		if questCount > quest.QUEST_MAX_NUM:
			self.questScrollBar.Show()
		else:
			self.questScrollBar.Hide()

		for i in questRange[:questCount]:
			(questName, questIcon, questCounterName, questCounterValue) = quest.GetQuestData(self.questShowingStartIndex+i)
			if constInfo.ENABLE_COLOR_SCROLL and ('#' in questName):
				for s_color in ("green","blue","purple"):
					if questName.endswith(s_color):
						#questIcon="locale/icon/scroll_open_%s.tga"%s_color
						questName = questName[:-1-len(s_color)]
						break
			self.questNameList[i].SetText(questName)
			self.questNameList[i].Show()
			self.questLastCountList[i].Show()
			self.questLastTimeList[i].Show()

			if len(questCounterName) > 0:
				self.questLastCountList[i].SetText("%s : %d" % (questCounterName, questCounterValue))
			else:
				self.questLastCountList[i].SetText("")

			## Icon
			self.questSlot.SetSlot(i, i, 1, 1, questIcon)

		for i in questRange[questCount:]:
			self.questNameList[i].Hide()
			self.questLastTimeList[i].Hide()
			self.questLastCountList[i].Hide()
			self.questSlot.ClearSlot(i)
			self.questSlot.HideSlotBaseImage(i)

		self.__UpdateQuestClock()

	def __UpdateQuestClock(self):
		if "QUEST" == self.state:
			# QUEST_LIMIT_COUNT_BUG_FIX
			for i in xrange(min(quest.GetQuestCount(), quest.QUEST_MAX_NUM)):
			# END_OF_QUEST_LIMIT_COUNT_BUG_FIX
				(lastName, lastTime) = quest.GetQuestLastTime(i)

				clockText = localeInfo.QUEST_UNLIMITED_TIME
				if len(lastName) > 0:

					if lastTime <= 0:
						clockText = localeInfo.QUEST_TIMEOVER

					else:
						questLastMinute = lastTime / 60
						questLastSecond = lastTime % 60

						clockText = lastName + " : "

						if questLastMinute > 0:
							clockText += str(questLastMinute) + localeInfo.QUEST_MIN
							if questLastSecond > 0:
								clockText += " "

						if questLastSecond > 0:
							clockText += str(questLastSecond) + localeInfo.QUEST_SEC

				self.questLastTimeList[i].SetText(clockText)

	def __GetStatMinusPoint(self):
		POINT_STAT_RESET_COUNT = 112
		return player.GetStatus(POINT_STAT_RESET_COUNT)

	def __OverInStatMinusButton(self, stat):
		try:
			self.__ShowStatToolTip(self.STAT_MINUS_DESCRIPTION[stat] % self.__GetStatMinusPoint())
		except KeyError:
			pass

		self.refreshToolTip = lambda arg=stat: self.__OverInStatMinusButton(arg)

	def __OverOutStatMinusButton(self):
		self.__HideStatToolTip()
		self.refreshToolTip = 0

	def __OverInStatButton(self, stat):
		try:
			self.__ShowStatToolTip(self.STAT_DESCRIPTION[stat])
		except KeyError:
			pass

	def __OverOutStatButton(self):
		self.__HideStatToolTip()

	def __ShowStatToolTip(self, statDesc):
		self.toolTip.ClearToolTip()
		self.toolTip.AppendTextLine(statDesc)
		self.toolTip.AppendTextLine("|Eicon/emoji/ctrl.tga|e + |Eicon/emoji/m_left.tga|e - x10")
		self.toolTip.Show()

	def __HideStatToolTip(self):
		self.toolTip.Hide()
		
	def __OverInImageFunc(self, image):	
		try:
			self.__ShowImageToolTip(self.IMAGE_DESCRIPTION[image])
		except KeyError:
			pass

	def __OverInNewButtonsFunc(self, image):	
		try:
			self.__ShowImageToolTip(self.NEWBUTTONS_DESC[image])
		except KeyError:
			pass

	def __OverInTabFunc(self, image):	
		try:
			self.__ShowImageToolTip(self.TAB_DESC[image])
		except KeyError:
			pass

	def __OverOutImageFunc(self):
		self.__HideImageToolTip()

	def __ShowImageToolTip(self, imageDesc):
		self.toolTipTest.ClearToolTip()
		self.toolTipTest.AutoAppendTextLine(imageDesc)
		self.toolTipTest.AlignHorizonalCenter()
		self.toolTipTest.Show()

	def __HideImageToolTip(self):
		self.toolTipTest.Hide()

	def OnPressEscapeKey(self):
		self.Close()
		return True

	def OnUpdate(self):
		self.__UpdateQuestClock()

		if self.pageDict["EMOTICON"].IsShow():
			for slotIdx, datadict in emotion.EMOTION_DICT.items():
				slot = self.premiumEmotionSlot
				if slotIdx >= 60 and slotIdx <= 71:
					if player.IsPremiumUser() == 1 or player.IsPremiumUser() == 2 or player.IsPremiumUser() == 3:
						slot.EnableCoverButton(slotIdx)
					else:
						slot.DisableCoverButton(slotIdx)

	## Skill Process
	def __RefreshSkillPage(self, name, slotCount):
		global SHOW_LIMIT_SUPPORT_SKILL_LIST

		skillPage = self.skillPageDict[name]

		startSlotIndex = skillPage.GetStartIndex()
		if "ACTIVE" == name:
			if self.PAGE_HORSE == self.curSelectedSkillGroup:
				startSlotIndex += slotCount
		elif name == "SUPPORT":
			startSlotIndex = 101
		
		getSkillType=skill.GetSkillType
		getSkillIndex=player.GetSkillIndex
		getSkillGrade=player.GetSkillGrade
		getSkillLevel=player.GetSkillLevel
		getSkillLevelUpPoint=skill.GetSkillLevelUpPoint
		getSkillMaxLevel=skill.GetSkillMaxLevel

		for i in xrange(slotCount+1):

			slotIndex = i + startSlotIndex
			skillIndex = getSkillIndex(slotIndex)
			
			for j in xrange(skill.SKILL_GRADE_COUNT):
				skillPage.ClearSlot(self.__GetRealSkillSlot(j, i))

			if 0 == skillIndex:
				continue

			skillGrade = getSkillGrade(slotIndex)
			skillLevel = getSkillLevel(slotIndex)
			skillType = getSkillType(skillIndex)

			##
			if player.SKILL_INDEX_RIDING == skillIndex:
				if 1 == skillGrade:
					skillLevel += 19
				elif 2 == skillGrade:
					skillLevel += 29
				elif 3 == skillGrade:
					skillLevel = 40

				skillPage.SetSkillSlotNew(slotIndex, skillIndex, max(skillLevel-1, 0), skillLevel)
				skillPage.SetSlotCount(slotIndex, skillLevel)

			## ACTIVE
			elif skill.SKILL_TYPE_ACTIVE == skillType:
				for j in xrange(skill.SKILL_GRADE_COUNT):
					realSlotIndex = self.__GetRealSkillSlot(j, slotIndex)
					skillPage.SetSkillSlotNew(realSlotIndex, skillIndex, j, skillLevel)
					skillPage.SetCoverButton(realSlotIndex)

					if (skillGrade == skill.SKILL_GRADE_COUNT) and j == (skill.SKILL_GRADE_COUNT-1):
						skillPage.SetSlotCountNew(realSlotIndex, skillGrade, skillLevel)
					elif (not self.__CanUseSkillNow()) or (skillGrade != j):
						skillPage.SetSlotCount(realSlotIndex, 0)
						skillPage.DisableCoverButton(realSlotIndex)
						skillPage.DeactivateSlot(realSlotIndex) # Grimm Fix highlight
					else:
						skillPage.SetSlotCountNew(realSlotIndex, skillGrade, skillLevel)
			##
			else:
				if not SHOW_LIMIT_SUPPORT_SKILL_LIST or skillIndex in SHOW_LIMIT_SUPPORT_SKILL_LIST:
					realSlotIndex = self.__GetETCSkillRealSlotIndex(slotIndex)

					skillPage.SetSkillSlot(realSlotIndex, skillIndex, skillLevel)
					skillPage.SetSlotCountNew(realSlotIndex, skillGrade, skillLevel)

					if skill.CanUseSkill(skillIndex):
						skillPage.SetCoverButton(realSlotIndex)

			skillPage.RefreshSlot()
	
	def GetLevelFromGrade(self, level):
		if level < 17:
			return level

		if level >= 37:
			return 1

		if level >= 27:
			return level - 26
	
		if level >= 17 and level < 27:
			return level - 16
			
		return level
	
	def GetGradeFromLevel(self, level):
		if level < 17:
			return 0
		
		if level >= 37:
			return 3
		
		if level >= 27:
			return 2	
	
		if level >= 17 and level < 27:
			return 1
			
		return 0
	
	def RefreshSkill(self):

		if self.isLoaded==0:
			return

		if self.__IsChangedHorseRidingSkillLevel():
			self.RefreshCharacter()
			return


		global SHOW_ONLY_ACTIVE_SKILL
		if SHOW_ONLY_ACTIVE_SKILL:
			self.__RefreshSkillPage("ACTIVE", self.ACTIVE_PAGE_SLOT_COUNT)
		else:
			self.__RefreshSkillPage("ACTIVE", self.ACTIVE_PAGE_SLOT_COUNT)
			self.__RefreshSkillPage("SUPPORT", self.SUPPORT_PAGE_SLOT_COUNT)

		self.RefreshSkillPlusButtonList()

	def CanShowPlusButton(self, skillIndex, skillLevel, curStatPoint):

		## 
		if 0 == skillIndex:
			return False

		##
		if not skill.CanLevelUpSkill(skillIndex, skillLevel):
			return False

		return True

	def __RefreshSkillPlusButton(self, name):

		global HIDE_SUPPORT_SKILL_POINT
		if HIDE_SUPPORT_SKILL_POINT and "SUPPORT" == name:
			return

		slotWindow = self.skillPageDict[name]
		slotWindow.HideAllSlotButton()

		slotStatType = self.skillPageStatDict[name]
		if 0 == slotStatType:
			return

		statPoint = player.GetStatus(slotStatType)
		startSlotIndex = slotWindow.GetStartIndex()
		if "HORSE" == name:
			startSlotIndex += self.ACTIVE_PAGE_SLOT_COUNT

		if statPoint > 0:
			for i in xrange(self.PAGE_SLOT_COUNT):
				slotIndex = i + startSlotIndex
				skillIndex = player.GetSkillIndex(slotIndex)
				skillGrade = player.GetSkillGrade(slotIndex)
				skillLevel = player.GetSkillLevel(slotIndex)

				if skillIndex == 0:
					continue
				if skillGrade != 0:
					continue
				
				if name == "HORSE":
					if player.GetStatus(player.LEVEL) >= skill.GetSkillLevelLimit(skillIndex):
						if skillLevel < 20:
							slotWindow.ShowSlotButton(self.__GetETCSkillRealSlotIndex(slotIndex))

				else:
					if "SUPPORT" == name:
						if not SHOW_LIMIT_SUPPORT_SKILL_LIST or skillIndex in SHOW_LIMIT_SUPPORT_SKILL_LIST:
							if self.CanShowPlusButton(skillIndex, skillLevel, statPoint):
								slotWindow.ShowSlotButton(slotIndex)
					else:
						if self.CanShowPlusButton(skillIndex, skillLevel, statPoint):
							slotWindow.ShowSlotButton(slotIndex)
		
	def RefreshSkillPlusButtonList(self):

		if self.isLoaded==0:
			return

		self.RefreshSkillPlusPointLabel()

		if not self.__CanUseSkillNow():
			return

		try:
			if self.PAGE_HORSE == self.curSelectedSkillGroup:
				self.__RefreshSkillPlusButton("HORSE")
			else:
				self.__RefreshSkillPlusButton("ACTIVE")

			self.__RefreshSkillPlusButton("SUPPORT")

		except:
			import exception
			exception.Abort("CharacterWindow.RefreshSkillPlusButtonList.BindObject")

	def RefreshSkillPlusPointLabel(self):
		if self.isLoaded==0:
			return

		if self.PAGE_HORSE == self.curSelectedSkillGroup:
			activeStatPoint = player.GetStatus(player.SKILL_HORSE)
			self.activeSkillPointValue.SetText(str(activeStatPoint))

		else:
			activeStatPoint = player.GetStatus(player.SKILL_ACTIVE)
			self.activeSkillPointValue.SetText(str(activeStatPoint))

		supportStatPoint = max(0, player.GetStatus(player.SKILL_SUPPORT))
		self.supportSkillPointValue.SetText(str(supportStatPoint))

	## Skill Level Up Button
	def OnPressedSlotButton(self, slotNumber):
		srcSlotIndex = self.__RealSkillSlotToSourceSlot(slotNumber)

		skillIndex = player.GetSkillIndex(srcSlotIndex)
		curLevel = player.GetSkillLevel(srcSlotIndex)
		maxLevel = skill.GetSkillMaxLevel(skillIndex)

		net.SendChatPacket("/skillup " + str(skillIndex))

	## Use Skill
	def ClickSkillSlot(self, slotIndex):
		srcSlotIndex = self.__RealSkillSlotToSourceSlot(slotIndex)
		skillIndex = player.GetSkillIndex(srcSlotIndex)
		skillType = skill.GetSkillType(skillIndex)

		if not self.__CanUseSkillNow():
			if skill.SKILL_TYPE_ACTIVE == skillType:
				return

		for slotWindow in self.skillPageDict.values():
			if slotWindow.HasSlot(slotIndex):
				if skill.CanUseSkill(skillIndex):
					player.ClickSkillSlot(srcSlotIndex)
					return

		mouseModule.mouseController.DeattachObject()

	## FIXME 
	##
	def OnUseSkill(self, slotIndex, coolTime):
		skillIndex = player.GetSkillIndex(slotIndex)
		skillType = skill.GetSkillType(skillIndex)

		## ACTIVE
		if skill.SKILL_TYPE_ACTIVE == skillType:
			skillGrade = player.GetSkillGrade(slotIndex)
			slotIndex = self.__GetRealSkillSlot(skillGrade, slotIndex)
		## ETC
		else:
			slotIndex = self.__GetETCSkillRealSlotIndex(slotIndex)

		for slotWindow in self.skillPageDict.values():
			if slotWindow.HasSlot(slotIndex):
				slotWindow.SetSlotCoolTime(slotIndex, coolTime)
				return

	def OnActivateSkill(self, slotIndex):
		self.DeactiveOldBug(slotIndex) # FIX BUG ACTIVATED_SLOT
	
		skillGrade = player.GetSkillGrade(slotIndex)
		slotIndex = self.__GetRealSkillSlot(skillGrade, slotIndex)
		for slotWindow in self.skillPageDict.values():
			if slotWindow.HasSlot(slotIndex):
				if app.ENABLE_CHANGELOOK_SYSTEM:
					slotWindow.ActivateSlot(slotIndex)
				else:
					slotWindow.ActivateSlot(slotIndex)
				
				return

	def OnDeactivateSkill(self, slotIndex):
		skillGrade = player.GetSkillGrade(slotIndex)
		slotIndex = self.__GetRealSkillSlot(skillGrade, slotIndex)
		for slotWindow in self.skillPageDict.values():
			if slotWindow.HasSlot(slotIndex):
				if app.ENABLE_CHANGELOOK_SYSTEM:
					slotWindow.DeactivateSlot(slotIndex)
				else:
					slotWindow.DeactivateSlot(slotIndex)
				
				return

	def DeactiveOldBug(self, slotIndex):# GRM
		skillGrade = 0
		slotIndex = self.__GetRealSkillSlot(skillGrade, slotIndex)

		for slotWindow in self.skillPageDict.values():
			if slotWindow.HasSlot(slotIndex):
				slotWindow.DeactivateSlot(slotIndex)
				break

		skillGrade = 1
		slotIndex = self.__GetRealSkillSlot(skillGrade, slotIndex)

		for slotWindow in self.skillPageDict.values():
			if slotWindow.HasSlot(slotIndex):
				slotWindow.DeactivateSlot(slotIndex)
				break

		skillGrade = 2
		slotIndex = self.__GetRealSkillSlot(skillGrade, slotIndex)

		for slotWindow in self.skillPageDict.values():
			if slotWindow.HasSlot(slotIndex):
				slotWindow.DeactivateSlot(slotIndex)
				break

	def __ShowJobToolTip(self):
		self.toolTipJob.ShowToolTip()

	def __HideJobToolTip(self):
		self.toolTipJob.HideToolTip()

	def __SetJobText(self, mainJob, subJob):
		if player.GetStatus(player.LEVEL)<5:
			subJob=0

	def __ShowAlignmentToolTip(self):
		self.toolTipAlignment.ShowToolTip()

	def __HideAlignmentToolTip(self):
		self.toolTipAlignment.HideToolTip()

	def RefreshCharacter(self):

		if self.isLoaded==0:
			return

		## Name
		try:
			characterName = player.GetName()
			guildName = player.GetGuildName()
			self.characterNameValue.SetText(characterName)
			self.guildNameValue.SetText(guildName)
			if not guildName:
				self.characterNameSlot.SetPosition(109, 34)

				self.guildNameSlot.Hide()
			else:
				self.characterNameSlot.SetPosition(153, 34)
				self.guildNameSlot.Show()
		except:
			import exception
			exception.Abort("CharacterWindow.RefreshCharacter.BindObject")

		race = net.GetMainActorRace()
		group = net.GetMainActorSkillGroup()
		empire = net.GetMainActorEmpire()

		## Job Text
		job = chr.RaceToJob(race)
		self.__SetJobText(job, group)

		## FaceImage
		try:
			faceImageName = FACE_IMAGE_DICT[race]

			try:
				self.faceImage.LoadImage(faceImageName)
			except:
				print "CharacterWindow.RefreshCharacter(race=%d, faceImageName=%s)" % (race, faceImageName)
				self.faceImage.Hide()

		except KeyError:
			self.faceImage.Hide()

		## GroupName
		self.__SetSkillGroupName(race, group)

		## Skill
		if 0 == group:
			self.__SelectSkillGroup(0)

		else:
			self.__SetSkillSlotData(race, group, empire)

			if self.__CanUseHorseSkill():
				self.__SelectSkillGroup(0)

	def __SetSkillGroupName(self, race, group):

		job = chr.RaceToJob(race)

		if not self.SKILL_GROUP_NAME_DICT.has_key(job):
			return

		nameList = self.SKILL_GROUP_NAME_DICT[job]

		if 0 == group:
			self.skillGroupButton1.SetText(nameList[1])
			self.skillGroupButton2.SetText(nameList[2])
			self.skillGroupButton1.Show()
			self.skillGroupButton2.Show()
			self.activeSkillGroupName.Hide()

			if app.ENABLE_WOLFMAN_CHARACTER and playersettingmodule.RACE_WOLFMAN_M == race:
				self.skillGroupButton2.Hide()
		else:

			if self.__CanUseHorseSkill():
				self.activeSkillGroupName.Hide()
				self.skillGroupButton1.SetText(nameList.get(group, "Noname"))
				self.skillGroupButton2.SetText(localeInfo.SKILL_GROUP_HORSE)
				self.skillGroupButton1.Show()
				self.skillGroupButton2.Show()

			else:
				self.activeSkillGroupName.SetText(nameList.get(group, "Noname"))
				self.activeSkillGroupName.Show()
				self.skillGroupButton1.Hide()
				self.skillGroupButton2.Hide()

	def __SetSkillSlotData(self, race, group, empire=0):

		## SkillIndex
		playersettingmodule.RegisterSkill(race, group, empire)

		## Event
		self.__SetSkillSlotEvent()

		## Refresh
		self.RefreshSkill()

	def __SelectSkillGroup(self, index):
		for btn in self.skillGroupButton:
			btn.SetUp()
		self.skillGroupButton[index].Down()

		if self.__CanUseHorseSkill():
			if 0 == index:
				index = net.GetMainActorSkillGroup()-1
			elif 1 == index:
				index = self.PAGE_HORSE

		self.curSelectedSkillGroup = index
		self.__SetSkillSlotData(net.GetMainActorRace(), index+1, net.GetMainActorEmpire())

	def __CanUseSkillNow(self):
		if 0 == net.GetMainActorSkillGroup():
			return False

		return True

	def __CanUseHorseSkill(self):

		slotIndex = player.GetSkillSlotIndex(player.SKILL_INDEX_RIDING)

		if not slotIndex:
			return False

		grade = player.GetSkillGrade(slotIndex)
		level = player.GetSkillLevel(slotIndex)
		if level < 0:
			level *= -1
		if grade >= 1 and level >= 1:
			return True

		return False

	def __IsChangedHorseRidingSkillLevel(self):
		ret = False

		if -1 == self.canUseHorseSkill:
			self.canUseHorseSkill = self.__CanUseHorseSkill()

		if self.canUseHorseSkill != self.__CanUseHorseSkill():
			ret = True

		self.canUseHorseSkill = self.__CanUseHorseSkill()
		return ret

	def __GetRealSkillSlot(self, skillGrade, skillSlot):
		return skillSlot + min(skill.SKILL_GRADE_COUNT-1, skillGrade)*skill.SKILL_GRADE_STEP_COUNT

	def __GetETCSkillRealSlotIndex(self, skillSlot):
		if skillSlot > 100:
			return skillSlot
		return skillSlot % self.ACTIVE_PAGE_SLOT_COUNT

	def __RealSkillSlotToSourceSlot(self, realSkillSlot):
		if realSkillSlot > 100:
			return realSkillSlot
		if self.PAGE_HORSE == self.curSelectedSkillGroup:
			return realSkillSlot + self.ACTIVE_PAGE_SLOT_COUNT
		return realSkillSlot % skill.SKILL_GRADE_STEP_COUNT

	def __GetSkillGradeFromSlot(self, skillSlot):
		return int(skillSlot / skill.SKILL_GRADE_STEP_COUNT)

	def SelectSkillGroup(self, index):
		self.__SelectSkillGroup(index)

	def OnQuestScroll(self):
		questCount = quest.GetQuestCount()
		scrollLineCount = max(0, questCount - quest.QUEST_MAX_NUM)
		startIndex = int(scrollLineCount * self.questScrollBar.GetPos())

		if startIndex != self.questShowingStartIndex:
			self.questShowingStartIndex = startIndex
			self.RefreshQuest()
