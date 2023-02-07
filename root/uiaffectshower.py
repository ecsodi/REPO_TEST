import thenewui as ui
import localeInfo
import Collision as chr
import item
import app
import skill
import CacheEffect as player
import uiToolTip
import math
import chat

import net
import uiCommon
import collections

AFF_ID_MULTI_FARM = 2900

# WEDDING
class LovePointImage(ui.ExpandedImageBox):

	FILE_PATH = "d:/ymir work/ui/pattern/LovePoint/"
	FILE_DICT = {
		0 : FILE_PATH + "01.dds",
		1 : FILE_PATH + "02.dds",
		2 : FILE_PATH + "02.dds",
		3 : FILE_PATH + "03.dds",
		4 : FILE_PATH + "04.dds",
		5 : FILE_PATH + "05.dds",
	}

	def __init__(self):
		ui.ExpandedImageBox.__init__(self)

		self.loverName = ""
		self.lovePoint = 0

		self.toolTip = uiToolTip.ToolTip(100)
		self.toolTip.HideToolTip()

	def __del__(self):
		ui.ExpandedImageBox.__del__(self)

	def SetLoverInfo(self, name, lovePoint):
		self.loverName = name
		self.lovePoint = lovePoint
		self.__Refresh()

	def OnUpdateLovePoint(self, lovePoint):
		self.lovePoint = lovePoint
		self.__Refresh()

	def __Refresh(self):
		self.lovePoint = max(0, self.lovePoint)
		self.lovePoint = min(100, self.lovePoint)

		if 0 == self.lovePoint:
			loveGrade = 0
		else:
			loveGrade = self.lovePoint / 25 + 1
		fileName = self.FILE_DICT.get(loveGrade, self.FILE_PATH+"00.dds")

		try:
			self.LoadImage(fileName)
		except:
			import dbg
			dbg.TraceError("LovePointImage.SetLoverInfo(lovePoint=%d) - LoadError %s" % (self.lovePoint, fileName))

		self.SetScale(0.7, 0.7)

		self.toolTip.ClearToolTip()
		self.toolTip.SetTitle(self.loverName)
		self.toolTip.AppendTextLine(localeInfo.AFF_LOVE_POINT % (self.lovePoint))
		self.toolTip.ResizeToolTip()

	def OnMouseOverIn(self):
		self.toolTip.ShowToolTip()

	def OnMouseOverOut(self):
		self.toolTip.HideToolTip()
# END_OF_WEDDING


class HorseImage(ui.ExpandedImageBox):

	FILE_PATH = "d:/ymir work/ui/pattern/HorseState/"

	FILE_DICT = {
		00 : FILE_PATH+"00.dds",
		01 : FILE_PATH+"00.dds",
		02 : FILE_PATH+"00.dds",
		03 : FILE_PATH+"00.dds",
		10 : FILE_PATH+"10.dds",
		11 : FILE_PATH+"11.dds",
		12 : FILE_PATH+"12.dds",
		13 : FILE_PATH+"13.dds",
		20 : FILE_PATH+"20.dds",
		21 : FILE_PATH+"21.dds",
		22 : FILE_PATH+"22.dds",
		23 : FILE_PATH+"23.dds",
		30 : FILE_PATH+"30.dds",
		31 : FILE_PATH+"31.dds",
		32 : FILE_PATH+"32.dds",
		33 : FILE_PATH+"33.dds",
	}

	def __init__(self):
		ui.ExpandedImageBox.__init__(self)

		#self.textLineList = []
		self.toolTip = uiToolTip.ToolTip(100)
		self.toolTip.HideToolTip()

	def __GetHorseGrade(self, level):
		if 0 == level:
			return 0

		return (level-1)/10 + 1

	def SetState(self, level, health, battery):
		#self.textLineList=[]
		self.toolTip.ClearToolTip()

		if level>0:

			try:
				grade = self.__GetHorseGrade(level)
				self.__AppendText(localeInfo.LEVEL_LIST[grade])
			except IndexError:
				print "HorseImage.SetState(level=%d, health=%d, battery=%d) - Unknown Index" % (level, health, battery)
				return

			try:
				healthName=localeInfo.HEALTH_LIST[health]
				if len(healthName)>0:
					self.__AppendText(healthName)
			except IndexError:
				print "HorseImage.SetState(level=%d, health=%d, battery=%d) - Unknown Index" % (level, health, battery)
				return

			if health>0:
				if battery==0:
					self.__AppendText(localeInfo.NEEFD_REST)

			try:
				fileName=self.FILE_DICT[health*10+battery]
			except KeyError:
				print "HorseImage.SetState(level=%d, health=%d, battery=%d) - KeyError" % (level, health, battery)

			try:
				self.LoadImage(fileName)
			except:
				print "HorseImage.SetState(level=%d, health=%d, battery=%d) - LoadError %s" % (level, health, battery, fileName)

		self.SetScale(0.7, 0.7)

	def __AppendText(self, text):

		self.toolTip.AppendTextLine(text)
		self.toolTip.ResizeToolTip()

		#x=self.GetWidth()/2
		#textLine = ui.TextLine()
		#textLine.SetParent(self)
		#textLine.SetSize(0, 0)
		#textLine.SetOutline()
		#textLine.Hide()
		#textLine.SetPosition(x, 40+len(self.textLineList)*16)
		#textLine.SetText(text)
		#self.textLineList.append(textLine)

	def OnMouseOverIn(self):
		#for textLine in self.textLineList:
		#	textLine.Show()

		self.toolTip.ShowToolTip()

	def OnMouseOverOut(self):
		#for textLine in self.textLineList:
		#	textLine.Hide()

		self.toolTip.HideToolTip()


# AUTO_POTION
class AutoPotionImage(ui.ExpandedImageBox):

	FILE_PATH_HP = "d:/ymir work/ui/pattern/auto_hpgauge/"
	FILE_PATH_SP = "d:/ymir work/ui/pattern/auto_spgauge/"

	def __init__(self):
		ui.ExpandedImageBox.__init__(self)

		self.loverName = ""
		self.lovePoint = 0
		self.potionType = player.AUTO_POTION_TYPE_HP
		self.filePath = ""

		self.toolTip = uiToolTip.ToolTip(100)
		self.toolTip.HideToolTip()

	def __del__(self):
		ui.ExpandedImageBox.__del__(self)

	def SetPotionType(self, type):
		self.potionType = type

		if player.AUTO_POTION_TYPE_HP == type:
			self.filePath = self.FILE_PATH_HP
		elif player.AUTO_POTION_TYPE_SP == type:
			self.filePath = self.FILE_PATH_SP


	def OnUpdateAutoPotionImage(self):
		self.__Refresh()

	def __Refresh(self):
		print "__Refresh"

		isActivated, currentAmount, totalAmount, slotIndex = player.GetAutoPotionInfo(self.potionType)

		amountPercent = (float(currentAmount) / totalAmount) * 100.0
		grade = math.ceil(amountPercent / 20)

		if 5.0 > amountPercent:
			grade = 0

		if 80.0 < amountPercent:
			grade = 4
			if 90.0 < amountPercent:
				grade = 5

		fmt = self.filePath + "%.2d.dds"
		fileName = fmt % grade

		print self.potionType, amountPercent, fileName

		try:
			self.LoadImage(fileName)
		except:
			import dbg
			dbg.TraceError("AutoPotionImage.__Refresh(potionType=%d) - LoadError %s" % (self.potionType, fileName))

		self.SetScale(0.7, 0.7)

		self.toolTip.ClearToolTip()

		if player.AUTO_POTION_TYPE_HP == type:
			self.toolTip.SetTitle(localeInfo.TOOLTIP_AUTO_POTION_HP)
		else:
			self.toolTip.SetTitle(localeInfo.TOOLTIP_AUTO_POTION_SP)

		self.toolTip.AppendTextLine(localeInfo.TOOLTIP_AUTO_POTION_REST	% (amountPercent))
		self.toolTip.ResizeToolTip()

	def OnMouseOverIn(self):
		self.toolTip.ShowToolTip()

	def OnMouseOverOut(self):
		self.toolTip.HideToolTip()
# END_OF_AUTO_POTION


class AffectImage(ui.ExpandedImageBox):

	SKILLS_CAN_BE_REMOVED = [chr.AFFECT_KWAESOK, chr.AFFECT_JEUNGRYEOK, chr.AFFECT_HOSIN, chr.AFFECT_BOHO, chr.AFFECT_GICHEON]
	def __init__(self):
		ui.ExpandedImageBox.__init__(self)

		self.toolTipText = None
		self.isSkillAffect = True
		self.description = None
		self.endTime = 0
		self.QuestionDialog = None
		self.affect = None
		self.isClocked = True
		self.itemImage = None
		self.bStepImage = -1

	def SetAffect(self, affect):
		self.affect = affect

	def GetAffect(self):
		return self.affect

	def SetItemImage(self, fileName):
		if not self.itemImage:
			self.itemImage = ui.ExpandedImageBox()
			self.itemImage.SetParent(self)
			self.itemImage.AddFlag("not_pick")
			self.itemImage.SetWindowHorizontalAlignCenter()
			self.itemImage.SetWindowVerticalAlignCenter()
			
		self.itemImage.LoadImage(fileName)
		self.itemImage.SetScale(0.65, 0.65)
		self.itemImage.SetPosition(0, -1)
		self.itemImage.Show()

	def SetToolTipText(self, text, x = 0, y = -19):

		if not self.toolTipText:
			textLine = ui.TextLine()
			textLine.SetParent(self)
			textLine.SetSize(0, 0)
			textLine.SetOutline()
			textLine.Hide()
			self.toolTipText = textLine

		self.toolTipText.SetText(text)
		w, h = self.toolTipText.GetTextSize()
		self.toolTipText.SetPosition(max(0, x + self.GetWidth()/2 - w/2), y)

	def SetDescription(self, description):
		self.description = description

	def SetDuration(self, duration):
		self.endTime = 0
		if duration > 0:
			self.endTime = app.GetGlobalTimeStamp() + duration

	def UpdateAutoPotionDescription(self):

		potionType = 0
		if self.affect == chr.NEW_AFFECT_AUTO_HP_RECOVERY:
			potionType = player.AUTO_POTION_TYPE_HP
		else:
			potionType = player.AUTO_POTION_TYPE_SP

		self.SetToolTipText(localeInfo.SOCKET_PERMANENT, 0, 40)

	def SetClock(self, isClocked):
		self.isClocked = isClocked

	def UpdateDescription(self):
		if not self.isClocked:
			self.__UpdateDescription2()
			return

		if not self.description:
			return

		toolTip = self.description
		if self.endTime > 0:
			leftTime = localeInfo.SecondToDHM(self.endTime - app.GetGlobalTimeStamp())
			toolTip += " (%s : %s)" % (localeInfo.LEFT_TIME, leftTime)
		self.SetToolTipText(toolTip, 0, 40)
		# self.UpdateBackgroundImage(self.endTime - app.GetGlobalTimeStamp())

	def UpdateBackgroundImage(self, leftSec):
		if self.itemImage == None:
			return

		if leftSec < 5 * 60:
			if self.bStepImage == 0:
				return

			self.LoadImage("d:/ymir work/ui/game/blend/default_red.tga")
			self.bStepImage = 0

		elif leftSec >= 5 * 60 and leftSec < 10 * 60:
			if self.bStepImage == 1:
				return

			self.LoadImage("d:/ymir work/ui/game/blend/default_yellow.tga")
			self.bStepImage = 1

		elif leftSec >= 10 * 60:
			if self.bStepImage == 2:
				return

			self.LoadImage("d:/ymir work/ui/game/blend/default.tga")
			self.bStepImage = 2

		self.SetScale(0.65, 0.65)
		
		if self.itemImage:
			self.itemImage.SetWindowHorizontalAlignCenter()
			self.itemImage.SetWindowVerticalAlignCenter()

	def __UpdateDescription2(self):
		if not self.description:
			return

		toolTip = self.description
		self.SetToolTipText(toolTip, 0, 40)

	def SetSkillAffectFlag(self, flag):
		self.isSkillAffect = flag

	def IsSkillAffect(self):
		return self.isSkillAffect

	def OnQuestionDialog(self):
		import uiCommon
		self.QuestionDialog = uiCommon.QuestionDialog()
		self.QuestionDialog.SetText(localeInfo.BUFF_REMOVE_ASK)
		self.QuestionDialog.SetWidth(350)
		self.QuestionDialog.SetAcceptEvent(lambda arg = TRUE: self.OnCloseQuestionDialog(arg))
		self.QuestionDialog.SetCancelEvent(lambda arg = FALSE: self.OnCloseQuestionDialog(arg))
		self.QuestionDialog.Open()
		
	def OnCloseQuestionDialog(self, answer):
		import net

		if not self.QuestionDialog:
			return

		self.QuestionDialog.Close()
		self.QuestionDialog = None
				
		if not answer:
			return

		net.SendChatPacket("/remove_affect %d" % (self.affect))
		return TRUE

	def OnMouseLeftButtonDown(self):
		if self.QuestionDialog == None:
			for i in range(len(self.SKILLS_CAN_BE_REMOVED)):
				if self.SKILLS_CAN_BE_REMOVED[i] == self.affect:
					self.OnQuestionDialog()
					break
		
	def OnMouseOverIn(self):
		# SET-ANIM-SCALE (Third Argument "True" its "IsScaleTemporary = True")
		if self.xScaleImage != 0 and self.yScaleImage != 0:
			self.SetScale(self.xScaleImage + 0.15, self.yScaleImage + 0.15, True)
		if self.itemImage:
			if self.itemImage.xScaleImage != 0 and self.itemImage.yScaleImage != 0:
				self.itemImage.SetScale(self.itemImage.xScaleImage + 0.15, self.itemImage.yScaleImage + 0.15, True)
		# SET-ANIM-SCALE

		if self.toolTipText:
			self.toolTipText.Show()

	def OnMouseOverOut(self):
		# SET-ANIM-SCALE (Third Argument "Non-Present" its "IsScaleTemporary = False")
		if self.xScaleImage != 0 and self.yScaleImage != 0:
			self.SetScale(self.xScaleImage, self.yScaleImage)
		if self.itemImage:
			if self.itemImage.xScaleImage != 0 and self.itemImage.yScaleImage != 0:
				self.itemImage.SetScale(self.itemImage.xScaleImage, self.itemImage.yScaleImage)
		# SET-ANIM-SCALE
	
		if self.toolTipText:
			self.toolTipText.Hide()

if app.ENABLE_PREMIUM_SYSTEM:
	PREMIUM_TYPE = 0
	CHOSEN_ATTRIBUTES = [ -1, -1 ]
	class PremiumImage(ui.ExpandedImageBox):

		images = {
			1 : "icon/item/tickets/vip_30_zile.png",	# put your own images
			2 : "icon/item/tickets/vip_60_zile.png",
			3 : "icon/item/tickets/vip_90_zile.png",
		}

		def __init__(self, parent):
			ui.ExpandedImageBox.__init__(self)
			self.SetParent(parent)

			self.toolTip = uiToolTip.ToolTip(200)
			self.toolTip.HideToolTip()

			self.endTime = 0

			if app.ENABLE_PREMIUM_SYSTEM_EXTRA:
				self.affects = [ 0, 0 ]

		def __del__(self):
			ui.ExpandedImageBox.__del__(self)

		if app.ENABLE_PREMIUM_SYSTEM_EXTRA:
			def SetPremiumStatus(self, type, timeLeft, affect1, affect2):
				self.LoadImage(self.images[type])
				self.SetScale(0.7, 0.7)

				self.endTime = app.GetGlobalTimeStamp() + timeLeft
				self.UpdateTime()

				self.affects[0] = affect1
				self.affects[1] = affect2
				
				global CHOSEN_ATTRIBUTES
				CHOSEN_ATTRIBUTES[0] = affect1
				CHOSEN_ATTRIBUTES[1] = affect2
				
				global PREMIUM_TYPE
				PREMIUM_TYPE = type
		else:
			def SetPremiumStatus(self, type, timeLeft):
				self.LoadImage(self.images[type])
				self.SetScale(0.7, 0.7)

				self.endTime = app.GetGlobalTimeStamp() + timeLeft
				self.UpdateTime()

		def UpdateTime(self):
			if self.IsIn():
				self.toolTip.ClearToolTip()
				leftTime = localeInfo.SecondToDHM(self.endTime - app.GetGlobalTimeStamp())

				if app.ENABLE_PREMIUM_SYSTEM_EXTRA:
					self.toolTip.AppendTextLine(leftTime)

					affects = {
						18 : [ localeInfo.TOOLTIP_APPLY_ATTBONUS_MONSTER, 10, 15, 25 ],
						53 : [ localeInfo.TOOLTIP_APPLY_ATTBONUS_METIN, 10, 15, 25 ],
						43 : [ localeInfo.TOOLTIP_APPLY_ATTBONUS_BOSS, 10, 15, 25 ]
					}

					if self.affects[0]:
						self.toolTip.AppendTextLine(affects[self.affects[0]][0](affects[self.affects[0]][PREMIUM_TYPE]))
					if self.affects[1]:
						self.toolTip.AppendTextLine(affects[self.affects[1]][0](affects[self.affects[1]][PREMIUM_TYPE]))
				else:
					self.toolTip.AppendTextLine(leftTime)

				self.toolTip.ResizeToolTip()

		def OnMouseOverIn(self):
			self.UpdateTime()
			self.toolTip.Show()

		def OnMouseOverOut(self):
			self.toolTip.HideToolTip()

class AffectShower(ui.Window):

	MALL_DESC_IDX_START = 1000
	IMAGE_STEP = 25
	AFFECT_MAX_NUM = 32

	INFINITE_AFFECT_DURATION = 0x1FFFFFFF

	AFFECT_DATA_DICT =	{
			chr.AFFECT_POISON : (localeInfo.SKILL_TOXICDIE, "d:/ymir work/ui/skill/common/affect/poison.sub"),
			chr.AFFECT_SLOW : (localeInfo.SKILL_SLOW, "d:/ymir work/ui/skill/common/affect/slow.sub"),
			chr.AFFECT_STUN : (localeInfo.SKILL_STUN, "d:/ymir work/ui/skill/common/affect/stun.sub"),

			chr.AFFECT_ATT_SPEED_POTION : (localeInfo.SKILL_INC_ATKSPD, "icon/affect/greenpotion.dds"),
			chr.AFFECT_MOV_SPEED_POTION : (localeInfo.SKILL_INC_MOVSPD, "icon/affect/purplepotion.dds"),
			chr.AFFECT_FISH_MIND : (localeInfo.SKILL_FISHMIND, "icon/item/27610.tga"),

			chr.AFFECT_JEONGWI : (localeInfo.SKILL_JEONGWI, "d:/ymir work/ui/skill/warrior/jeongwi_03.sub",),
			chr.AFFECT_GEOMGYEONG : (localeInfo.SKILL_GEOMGYEONG, "d:/ymir work/ui/skill/warrior/geomgyeong_03.sub",),
			chr.AFFECT_CHEONGEUN : (localeInfo.SKILL_CHEONGEUN, "d:/ymir work/ui/skill/warrior/cheongeun_03.sub",),
			chr.AFFECT_GYEONGGONG : (localeInfo.SKILL_GYEONGGONG, "d:/ymir work/ui/skill/assassin/gyeonggong_03.sub",),
			chr.AFFECT_EUNHYEONG : (localeInfo.SKILL_EUNHYEONG, "d:/ymir work/ui/skill/assassin/eunhyeong_03.sub",),
			chr.AFFECT_GWIGEOM : (localeInfo.SKILL_GWIGEOM, "d:/ymir work/ui/skill/sura/gwigeom_03.sub",),
			chr.AFFECT_GONGPO : (localeInfo.SKILL_GONGPO, "d:/ymir work/ui/skill/sura/gongpo_03.sub",),
			chr.AFFECT_JUMAGAP : (localeInfo.SKILL_JUMAGAP, "d:/ymir work/ui/skill/sura/jumagap_03.sub"),
			chr.AFFECT_HOSIN : (localeInfo.SKILL_HOSIN, "d:/ymir work/ui/skill/shaman/hosin_03.sub",),
			chr.AFFECT_BOHO : (localeInfo.SKILL_BOHO, "d:/ymir work/ui/skill/shaman/boho_03.sub",),
			chr.AFFECT_KWAESOK : (localeInfo.SKILL_KWAESOK, "d:/ymir work/ui/skill/shaman/kwaesok_03.sub",),
			chr.AFFECT_HEUKSIN : (localeInfo.SKILL_HEUKSIN, "d:/ymir work/ui/skill/sura/heuksin_03.sub",),
			chr.AFFECT_MUYEONG : (localeInfo.SKILL_MUYEONG, "d:/ymir work/ui/skill/sura/muyeong_03.sub",),
			chr.AFFECT_GICHEON : (localeInfo.SKILL_GICHEON, "d:/ymir work/ui/skill/shaman/gicheon_03.sub",),
			chr.AFFECT_JEUNGRYEOK : (localeInfo.SKILL_JEUNGRYEOK, "d:/ymir work/ui/skill/shaman/jeungryeok_03.sub",),
			chr.AFFECT_PABEOP : (localeInfo.SKILL_PABEOP, "d:/ymir work/ui/skill/sura/pabeop_03.sub",),
			chr.AFFECT_FALLEN_CHEONGEUN : (localeInfo.SKILL_CHEONGEUN, "d:/ymir work/ui/skill/warrior/cheongeun_03.sub",),
			28 : (localeInfo.SKILL_FIRE, "d:/ymir work/ui/skill/sura/hwayeom_03.sub",),
			chr.AFFECT_CHINA_FIREWORK : (localeInfo.SKILL_POWERFUL_STRIKE, "d:/ymir work/ui/skill/common/affect/powerfulstrike.sub",),

			#64 - END
			chr.NEW_AFFECT_EXP_BONUS : (localeInfo.TOOLTIP_MALL_EXPBONUS_STATIC, "d:/ymir work/ui/skill/common/affect/exp_bonus.sub",),

			chr.NEW_AFFECT_ITEM_BONUS : (localeInfo.TOOLTIP_MALL_ITEMBONUS_STATIC, "d:/ymir work/ui/skill/common/affect/item_bonus.sub",),
			chr.NEW_AFFECT_SAFEBOX : (localeInfo.TOOLTIP_MALL_SAFEBOX, "d:/ymir work/ui/skill/common/affect/safebox.sub",),
			chr.NEW_AFFECT_AUTOLOOT : (localeInfo.TOOLTIP_MALL_AUTOLOOT, "d:/ymir work/ui/skill/common/affect/autoloot.sub",),
			chr.NEW_AFFECT_FISH_MIND : (localeInfo.TOOLTIP_MALL_FISH_MIND, "icon/item/27610.tga",),
			chr.NEW_AFFECT_MARRIAGE_FAST : (localeInfo.TOOLTIP_MALL_MARRIAGE_FAST, "d:/ymir work/ui/skill/common/affect/marriage_fast.sub",),
			chr.NEW_AFFECT_GOLD_BONUS : (localeInfo.TOOLTIP_MALL_GOLDBONUS_STATIC, "d:/ymir work/ui/skill/common/affect/gold_bonus.sub",),

			chr.NEW_AFFECT_NO_DEATH_PENALTY : (localeInfo.TOOLTIP_APPLY_NO_DEATH_PENALTY, "d:/ymir work/ui/skill/common/affect/gold_premium.sub"),
			chr.NEW_AFFECT_SKILL_BOOK_BONUS : (localeInfo.TOOLTIP_APPLY_SKILL_BOOK_BONUS, "icon/item/71094.tga"),
			chr.NEW_AFFECT_SKILL_BOOK_NO_DELAY : (localeInfo.TOOLTIP_APPLY_SKILL_BOOK_NO_DELAY, "icon/item/71001.tga"),
			chr.NEW_AFFECT_AUTO_HP_RECOVERY : (localeInfo.TOOLTIP_AUTO_POTION_REST, "icon/item/72726.tga"),
			chr.NEW_AFFECT_AUTO_SP_RECOVERY : (localeInfo.TOOLTIP_AUTO_POTION_REST, "icon/item/72730.tga"),
			
			# chr.NEW_AFFECT_BATTLE_PASS : ("Battlepass", "icon/item/79600.tga"),
			#chr.NEW_AFFECT_AUTO_HP_RECOVERY : (localeInfo.TOOLTIP_AUTO_POTION_REST, "d:/ymir work/ui/skill/common/affect/gold_premium.sub"),
			#chr.NEW_AFFECT_AUTO_SP_RECOVERY : (localeInfo.TOOLTIP_AUTO_POTION_REST, "d:/ymir work/ui/skill/common/affect/gold_bonus.sub"),

			MALL_DESC_IDX_START+player.POINT_MALL_ATTBONUS : (localeInfo.TOOLTIP_MALL_ATTBONUS_STATIC, "d:/ymir work/ui/skill/common/affect/att_bonus.sub",),
			MALL_DESC_IDX_START+player.POINT_MALL_DEFBONUS : (localeInfo.TOOLTIP_MALL_DEFBONUS_STATIC, "d:/ymir work/ui/skill/common/affect/def_bonus.sub",),
			MALL_DESC_IDX_START+player.POINT_MALL_EXPBONUS : (localeInfo.TOOLTIP_MALL_EXPBONUS, "d:/ymir work/ui/skill/common/affect/exp_bonus.sub",),
			MALL_DESC_IDX_START+player.POINT_MALL_ITEMBONUS : (localeInfo.TOOLTIP_MALL_ITEMBONUS, "d:/ymir work/ui/skill/common/affect/item_bonus.sub",),
			MALL_DESC_IDX_START+player.POINT_MALL_GOLDBONUS : (localeInfo.TOOLTIP_MALL_GOLDBONUS, "d:/ymir work/ui/skill/common/affect/gold_bonus.sub",),
			MALL_DESC_IDX_START+player.POINT_CRITICAL_PCT : (localeInfo.TOOLTIP_APPLY_CRITICAL_PCT,"d:/ymir work/ui/skill/common/affect/critical.sub"),
			MALL_DESC_IDX_START+player.POINT_PENETRATE_PCT : (localeInfo.TOOLTIP_APPLY_PENETRATE_PCT, "d:/ymir work/ui/skill/common/affect/gold_premium.sub"),
			MALL_DESC_IDX_START+player.POINT_MAX_HP_PCT : (localeInfo.TOOLTIP_MAX_HP_PCT, "d:/ymir work/ui/skill/common/affect/gold_premium.sub"),
			MALL_DESC_IDX_START+player.POINT_MAX_SP_PCT : (localeInfo.TOOLTIP_MAX_SP_PCT, "d:/ymir work/ui/skill/common/affect/gold_premium.sub"),

			MALL_DESC_IDX_START+player.POINT_PC_BANG_EXP_BONUS : (localeInfo.TOOLTIP_MALL_EXPBONUS_P_STATIC, "d:/ymir work/ui/skill/common/affect/EXP_Bonus_p_on.sub",),
			MALL_DESC_IDX_START+player.POINT_PC_BANG_DROP_BONUS: (localeInfo.TOOLTIP_MALL_ITEMBONUS_P_STATIC, "d:/ymir work/ui/skill/common/affect/Item_Bonus_p_on.sub",),

			# AFF_ID_MULTI_FARM: ("Activeaza/Dezactiveaza contul ca farmer", "icon/item/70038.tga",),
			chr.AFFECT_HOSIN_NEW : (localeInfo.SKILL_HOSIN, "d:/ymir work/ui/skill/shaman/hosin_03.sub",),

			846 : (localeInfo.TOOLTIP_APPLY_PASSIVE_SKILL_BOOK_BONUS, "icon/item/90022.tga"),
			847 : (localeInfo.TOOLTIP_APPLY_PASSIVE_SKILL_BOOK_NO_DELAY, "icon/item/90023.tga"),
			850 : ("Utilizator Premium", "icon/item/tickets/vip_90_zile.png"),

	}
	if app.ENABLE_DRAGON_SOUL_SYSTEM:
		AFFECT_DATA_DICT[chr.NEW_AFFECT_DRAGON_SOUL_DECK1] = (localeInfo.TOOLTIP_DRAGON_SOUL_DECK1, "d:/ymir work/ui/dragonsoul/buff_ds_sky1.tga")
		AFFECT_DATA_DICT[chr.NEW_AFFECT_DRAGON_SOUL_DECK2] = (localeInfo.TOOLTIP_DRAGON_SOUL_DECK2, "d:/ymir work/ui/dragonsoul/buff_ds_land1.tga")
	if app.ENABLE_WOLFMAN_CHARACTER:
		AFFECT_DATA_DICT[chr.AFFECT_BLEEDING] = (localeInfo.SKILL_BLEEDING, "d:/ymir work/ui/skill/common/affect/poison.sub")
		AFFECT_DATA_DICT[chr.AFFECT_RED_POSSESSION] = (localeInfo.SKILL_RED_POSSESSION, "d:/ymir work/ui/skill/wolfman/red_possession_03.sub")
		AFFECT_DATA_DICT[chr.AFFECT_BLUE_POSSESSION] = (localeInfo.SKILL_BLUE_POSSESSION, "d:/ymir work/ui/skill/wolfman/blue_possession_03.sub")
	# if app.ENABLE_PREMIUM_MEMBERS:
		# AFFECT_DATA_DICT[chr.AFFECT_DEIMOS_PREMIUM] = ("Utilizator Premium", "d:/ymir work/ui/dragonsoul/buff_ds_sky1.tga")
		# AFFECT_DATA_DICT[850] = ("Utilizator Premium", "d:/ymir work/ui/dragonsoul/buff_ds_sky1.tga")
		
	AFF_BLEND_DICT = {
		0 : {
			"AFF" : 531,
			"POINT" : 40,
			"IMAGE" : "icon/affect/blend_red.dds",
			"TEXT" : localeInfo.TOOLTIP_APPLY_CRITICAL_PCT,
		},

		1 : {
			"AFF" : 531,
			"POINT" : 41,
			"IMAGE" : "icon/affect/blend_orange.dds",
			"TEXT" : localeInfo.TOOLTIP_APPLY_PENETRATE_PCT,
		},

		2 : {
			"AFF" : 531,
			"POINT" : 17,
			"IMAGE" : "icon/affect/greenpotion.dds",
			"TEXT" : localeInfo.TOOLTIP_ATT_SPEED,
		},

		3 : {
			"AFF" : 531,
			"POINT" : 77,
			"IMAGE" : "icon/affect/blend_green.dds",
			"TEXT" : localeInfo.TOOLTIP_RESIST_MAGIC,
		},

		4 : {
			"AFF" : 531,
			"POINT" : 95,
			"IMAGE" : "icon/affect/blend_blue.dds",
			"TEXT" : localeInfo.TOOLTIP_MALL_ATTBONUS,
		},

		5 : {
			"AFF" : 531,
			"POINT" : 96,
			"IMAGE" : "icon/affect/blend_white.dds",
			"TEXT" : localeInfo.TOOLTIP_MALL_DEFBONUS,
		},

		# BLEND_TIME

		6 : {
			"AFF" : 531,
			"POINT" : 40,
			"VALUE" : 10,
			"IMAGE" : "icon/item/50821.tga",
			"TEXT" : localeInfo.TOOLTIP_MALL_EXPBONUS_STATIC,
		},

		7 : {
			"AFF" : 531,
			"POINT" : 41,
			"VALUE" : 10,
			"IMAGE" : "icon/item/50822.tga",
			"TEXT" : localeInfo.TOOLTIP_MALL_EXPBONUS_STATIC,
		},

		8 : {
			"AFF" : 531,
			"POINT" : 17,
			"VALUE" : 5,
			"IMAGE" : "icon/item/50823.tga",
			"TEXT" : localeInfo.TOOLTIP_MALL_EXPBONUS_STATIC,
		},

		9 : {
			"AFF" : 531,
			"POINT" : 77,
			"VALUE" : 10,
			"IMAGE" : "icon/item/50824.tga",
			"TEXT" : localeInfo.TOOLTIP_MALL_EXPBONUS_STATIC,
		},

		10 : {
			"AFF" : 531,
			"POINT" : 95,
			"VALUE" : 100,
			"IMAGE" : "icon/item/50825.tga",
			"TEXT" : localeInfo.TOOLTIP_MALL_EXPBONUS_STATIC,
		},

		11 : {
			"AFF" : 531,
			"POINT" : 96,
			"VALUE" : 120,
			"IMAGE" : "icon/item/50826.tga",
			"TEXT" : localeInfo.TOOLTIP_MALL_EXPBONUS_STATIC,
		},

		# ZEU_BLEND_TIME

		12 : {
			"AFF" : 519,
			"POINT" : 40,
			"IMAGE" : "icon/affect/critical_pct.dds",
			"TEXT" : localeInfo.TOOLTIP_APPLY_CRITICAL_PCT,
		},

		13 : {
			"AFF" : 519,
			"POINT" : 41,
			"IMAGE" : "icon/affect/penetrate_pct.dds",
			"TEXT" : localeInfo.TOOLTIP_APPLY_PENETRATE_PCT,
		},

		14 : {
			"AFF" : 519,
			"POINT" : 119,
			"IMAGE" : "icon/affect/71027.dds",
			"TEXT" : localeInfo.TOOLTIP_APPLY_MAX_HP_PCT,
		},

		15 : {
			"AFF" : 519,
			"POINT" : 120,
			"IMAGE" : "icon/affect/71028.dds",
			"TEXT" : localeInfo.TOOLTIP_APPLY_MAX_SP_PCT,
		},

		16 : {
			"AFF" : 519,
			"POINT" : 158,
			"IMAGE" : "icon/affect/71029.dds",
			"TEXT" : localeInfo.TOOLTIP_APPLY_ATTBONUS_BOSS,
		},

		17 : {
			"AFF" : 519,
			"POINT" : 157,
			"IMAGE" : "icon/affect/71030.dds",
			"TEXT" : localeInfo.TOOLTIP_APPLY_ATTBONUS_METIN,
		},

		18 : {
			"AFF" : 204,
			"POINT" : 12,
			"IMAGE" : "icon/item/27870.tga",
			"TEXT" : localeInfo.TOOLTIP_MALL_EXPBONUS_STATIC,
		},

		19 : {
			"AFF" : 531,
			"POINT" : 53,
			"IMAGE" : "icon/affect/blend_purple.tga",
			"TEXT" : localeInfo.TOOLTIP_APPLY_ATTBONUS_MONSTER,
		},

		20 : {
			"AFF" : 531,
			"POINT" : 162,
			"IMAGE" : "icon/affect/blend_black.tga",
			"TEXT" : localeInfo.TOOLTIP_APPLY_ATTBONUS_DUNGEON,
		},

		# PESTI
		21 : {
			"AFF" : 523,
			"POINT" : 6,
			"IMAGE" : "icon/item/27802.tga",
			"TEXT" : localeInfo.TOOLTIP_APPLY_MAX_HP_PCT,
		},
		
		22 : {
			"AFF" : 523,
			"POINT" : 162,
			"IMAGE" : "icon/item/27803.tga",
			"TEXT" : localeInfo.TOOLTIP_APPLY_ATTBONUS_DUNGEON,
		},
		
		23 : {
			"AFF" : 523,
			"POINT" : 53,
			"IMAGE" : "icon/item/27804.tga",
			"TEXT" : localeInfo.TOOLTIP_APPLY_ATTBONUS_MONSTER,
		},
		
		24 : {
			"AFF" : 523,
			"POINT" : 149,
			"IMAGE" : "icon/item/27805.tga",
			"TEXT" : localeInfo.TOOLTIP_RESIST_HUMAN,
		},
		
		25 : {
			"AFF" : 523,
			"POINT" : 121,
			"IMAGE" : "icon/item/27806.tga",
			"TEXT" : localeInfo.TOOLTIP_SKILL_DAMAGE_BONUS,
		},
		
		26 : {
			"AFF" : 523,
			"POINT" : 122,
			"IMAGE" : "icon/item/27807.tga",
			"TEXT" : localeInfo.TOOLTIP_NORMAL_HIT_DAMAGE_BONUS,
		},
		
		27 : {
			"AFF" : 523,
			"POINT" : 40,
			"IMAGE" : "icon/item/27808.tga",
			"TEXT" : localeInfo.TOOLTIP_APPLY_CRITICAL_PCT,
		},
		
		## zeuri
		28 : {
			"AFF" : 519,
			"POINT" : 115,
			"IMAGE" : "icon/affect/71030.dds",
			"TEXT" : localeInfo.TOOLTIP_MALL_DEFBONUS,
		},
		29 : {
			"AFF" : 519,
			"POINT" : 93,
			"IMAGE" : "icon/affect/71028.dds",
			"TEXT" : localeInfo.TOOLTIP_MALL_ATTBONUS,
		},
		
		30 : {
			"AFF" : 519,
			"POINT" : 95,
			"IMAGE" : "icon/affect/71028.dds",
			"TEXT" : localeInfo.TOOLTIP_MALL_DEFBONUS,
		},	
		
		31 : {
			"AFF" : 850,
			"POINT" : 0,
			"IMAGE" : "icon/item/tickets/vip_90_zile.png",
			"TEXT" : "Utilizator Premium",
		},
		
	}

	def __init__(self):
		ui.Window.__init__(self)

		self.serverPlayTime=0
		self.clientPlayTime=0

		self.lastUpdateTime=0
		self.affectImageDict={}
		self.horseImage=None
		self.lovePointImage=None
		self.autoPotionImageHP = AutoPotionImage()
		self.autoPotionImageSP = AutoPotionImage()
		if app.ENABLE_PREMIUM_SYSTEM:
			self.premiumImage = None
		self.SetPosition(10, 10)
		self.Show()
		
		# self.BINARY_NEW_AddAffect(AFF_ID_MULTI_FARM, 0, 0, 0)
	
	# def __del__()
	
	def ClearAllAffects(self):
		# self.__RemoveAffect(AFF_ID_MULTI_FARM)
		self.horseImage=None
		self.lovePointImage=None
		self.affectImageDict={}
		self.__ArrangeImageList()

	def ClearAffects(self):
		# self.__RemoveAffect(AFF_ID_MULTI_FARM)
	
		self.living_affectImageDict={}
		for key, image in self.affectImageDict.items():
			if not image.IsSkillAffect():
				self.living_affectImageDict[key] = image
		self.affectImageDict = self.living_affectImageDict
		self.__ArrangeImageList()

	def BINARY_NEW_AddAffect(self, type, pointIdx, value, duration):

		print "BINARY_NEW_AddAffect", type, pointIdx, value, duration
		
		# import chat
		# chat.AppendChat(1, "Type: %d, Point: %d, Value: %d" % (type, pointIdx, value))
		
		for x in xrange(len(self.AFF_BLEND_DICT)):
			if self.AFF_BLEND_DICT[x]["AFF"] == type and self.AFF_BLEND_DICT[x]["POINT"] == pointIdx:
				description = self.AFF_BLEND_DICT[x]["TEXT"]
				filename = self.AFF_BLEND_DICT[x]["IMAGE"]

				if type == chr.NEW_AFFECT_MALL:
					affect = self.MALL_DESC_IDX_START + pointIdx
				else:
					affect = type

				if affect != chr.NEW_AFFECT_AUTO_SP_RECOVERY and affect != chr.NEW_AFFECT_AUTO_HP_RECOVERY and affect != AFF_ID_MULTI_FARM:
					try:
						description = description(float(value))
					except:
						return

				# HAS_KEY
				if self.affectImageDict.has_key(500 + affect + pointIdx*2):
					return

				try:
					print "Add affect %s" % affect
					image = AffectImage()
					image.SetParent(self)
					image.LoadImage("d:/ymir work/ui/game/blend/default.tga")
					image.SetItemImage(filename)
					image.SetDescription(description)
					image.SetDuration(duration)
					image.SetAffect(affect)
					if affect == chr.NEW_AFFECT_EXP_BONUS_EURO_FREE or\
						affect == chr.NEW_AFFECT_EXP_BONUS_EURO_FREE_UNDER_15 or\
						self.INFINITE_AFFECT_DURATION < duration:
						image.SetClock(False)
						image.UpdateDescription()
					elif affect == chr.NEW_AFFECT_AUTO_SP_RECOVERY or affect == chr.NEW_AFFECT_AUTO_HP_RECOVERY:
						image.UpdateAutoPotionDescription()
					else:
						image.UpdateDescription()

					if affect == chr.NEW_AFFECT_DRAGON_SOUL_DECK1 or affect == chr.NEW_AFFECT_DRAGON_SOUL_DECK2:
						image.SetScale(1, 1)
					else:
						image.SetScale(0.7, 0.7)

					# if affect == chr.AFFECT_DEIMOS_PREMIUM:
						# image.SetScale(1, 1)
					# else:
						# image.SetScale(0.7, 0.7)

					image.SetSkillAffectFlag(False)
					image.Show()
					self.affectImageDict[500 + affect + pointIdx*2] = image
					self.__ArrangeImageList()
				except:
					pass

				break
		
		if type < 500:
			return

		# if type == chr.AFFECT_DEIMOS_PREMIUM:
			# chat.AppendChat(1, "Deimos Premium User!")
			
		if type == chr.NEW_AFFECT_MALL:
			affect = self.MALL_DESC_IDX_START + pointIdx
		else:
			affect = type

		if self.affectImageDict.has_key(affect):
			return

		if not self.AFFECT_DATA_DICT.has_key(affect):
			return

		if affect == chr.NEW_AFFECT_NO_DEATH_PENALTY or\
		   affect == chr.NEW_AFFECT_SKILL_BOOK_BONUS or\
		   affect == chr.NEW_AFFECT_AUTO_SP_RECOVERY or\
		   affect == chr.NEW_AFFECT_AUTO_HP_RECOVERY or\
		   affect == chr.NEW_AFFECT_SKILL_BOOK_NO_DELAY:
			duration = 0

		affectData = self.AFFECT_DATA_DICT[affect]
		description = affectData[0]
		filename = affectData[1]

		if pointIdx == player.POINT_MALL_ITEMBONUS or\
		   pointIdx == player.POINT_MALL_GOLDBONUS:
			value = 1 + float(value) / 100.0

		trashValue = 123
		#if affect == chr.NEW_AFFECT_AUTO_SP_RECOVERY or affect == chr.NEW_AFFECT_AUTO_HP_RECOVERY:
		if trashValue == 1:
			try:
				#image = AutoPotionImage()
				#image.SetParent(self)
				image = None

				if affect == chr.NEW_AFFECT_AUTO_SP_RECOVERY:
					image.SetPotionType(player.AUTO_POTION_TYPE_SP)
					image = self.autoPotionImageSP
					#self.autoPotionImageSP = image;
				else:
					image.SetPotionType(player.AUTO_POTION_TYPE_HP)
					image = self.autoPotionImageHP
					#self.autoPotionImageHP = image;

				image.SetParent(self)
				image.Show()
				image.OnUpdateAutoPotionImage()

				self.affectImageDict[affect] = image
				self.__ArrangeImageList()

			except Exception, e:
				print "except Aff auto potion affect ", e
				pass

		else:
			if affect != chr.NEW_AFFECT_AUTO_SP_RECOVERY and affect != chr.NEW_AFFECT_AUTO_HP_RECOVERY and affect != AFF_ID_MULTI_FARM and affect != 846 and affect != 847:
				try:
					description = description(float(value))
				except Exception:
					return

			try:
				print "Add affect %s" % affect
				image = AffectImage()
				image.SetParent(self)
				image.LoadImage(filename)
				image.SetDescription(description)
				image.SetDuration(duration)
				image.SetAffect(affect)
				if affect == chr.NEW_AFFECT_EXP_BONUS_EURO_FREE or\
					affect == chr.NEW_AFFECT_EXP_BONUS_EURO_FREE_UNDER_15 or\
					self.INFINITE_AFFECT_DURATION < duration:
					image.SetClock(False)
					image.UpdateDescription()
				elif affect == chr.NEW_AFFECT_AUTO_SP_RECOVERY or affect == chr.NEW_AFFECT_AUTO_HP_RECOVERY:
					image.UpdateAutoPotionDescription()
				else:
					image.UpdateDescription()

				if affect == chr.NEW_AFFECT_DRAGON_SOUL_DECK1 or affect == chr.NEW_AFFECT_DRAGON_SOUL_DECK2:
					image.SetScale(1, 1)
				else:
					image.SetScale(0.7, 0.7)
					
				# if affect == chr.AFFECT_DEIMOS_PREMIUM:
					# image.SetScale(1, 1)
				# else:
					# image.SetScale(0.7, 0.7)

				image.SetSkillAffectFlag(False)
				image.Show()
				self.affectImageDict[affect] = image
				self.__ArrangeImageList()
			except Exception, e:
				print "except Aff affect ", e
				pass

	def BINARY_NEW_RemoveAffect(self, type, pointIdx):
		if type == chr.NEW_AFFECT_MALL:
			affect = self.MALL_DESC_IDX_START + pointIdx
		else:
			affect = type

		print "Remove Affect %s %s" % ( type , pointIdx )
		self.__RemoveAffect(affect)
		self.__RemoveAffect(500 + affect + pointIdx*2)# BLEND
		self.__ArrangeImageList()

	def SetAffect(self, affect):
		self.__AppendAffect(affect)
		self.__ArrangeImageList()

	def ResetAffect(self, affect):
		self.__RemoveAffect(affect)
		self.__ArrangeImageList()

	def SetLoverInfo(self, name, lovePoint):
		image = LovePointImage()
		image.SetParent(self)
		image.SetLoverInfo(name, lovePoint)
		self.lovePointImage = image
		self.__ArrangeImageList()

	def ShowLoverState(self):
		if self.lovePointImage:
			self.lovePointImage.Show()
			self.__ArrangeImageList()

	def HideLoverState(self):
		if self.lovePointImage:
			self.lovePointImage.Hide()
			self.__ArrangeImageList()

	def ClearLoverState(self):
		self.lovePointImage = None
		self.__ArrangeImageList()

	def OnUpdateLovePoint(self, lovePoint):
		if self.lovePointImage:
			self.lovePointImage.OnUpdateLovePoint(lovePoint)

	def SetHorseState(self, level, health, battery):
		if level==0:
			self.horseImage=None
		else:
			image = HorseImage()
			image.SetParent(self)
			image.SetState(level, health, battery)
			image.Show()

			self.horseImage=image
		self.__ArrangeImageList()
		
	if app.ENABLE_PREMIUM_SYSTEM_EXTRA:
		def SetPremiumStatus(self, type, timeLeft, affect1, affect2):
			if type == 0:
				self.premiumImage = None
				if app.ENABLE_PREMIUM_SYSTEM_EXTRA:
					global CHOSEN_ATTRIBUTES
					CHOSEN_ATTRIBUTES[0] = -1
					CHOSEN_ATTRIBUTES[1] = -1
					
					global PREMIUM_TYPE
					PREMIUM_TYPE = type
			else:
				premiumImage = PremiumImage(self)
				premiumImage.SetPremiumStatus(type, timeLeft, affect1, affect2)
				premiumImage.Show()

				self.premiumImage = premiumImage
			self.__ArrangeImageList()
	elif app.ENABLE_PREMIUM_SYSTEM:
		def SetPremiumStatus(self, type, timeLeft):
			if type == 0:
				self.premiumImage = None
			else:
				premiumImage = PremiumImage(self)
				premiumImage.SetPremiumStatus(type, timeLeft)
				premiumImage.Show()

				self.premiumImage = premiumImage
			self.__ArrangeImageList()
			
	def SetPlayTime(self, playTime):
		self.serverPlayTime = playTime
		self.clientPlayTime = app.GetTime()

	def __AppendAffect(self, affect):

		if self.affectImageDict.has_key(affect):
			return

		try:
			affectData = self.AFFECT_DATA_DICT[affect]
		except KeyError:
			return

		name = affectData[0]
		filename = affectData[1]

		skillIndex = player.AffectIndexToSkillIndex(affect)
		if 0 != skillIndex:
			name = skill.GetSkillName(skillIndex)

		image = AffectImage()
		image.SetParent(self)
		image.SetAffect(affect)
		image.SetSkillAffectFlag(True)

		try:
			image.LoadImage(filename)
		except:
			pass

		image.SetToolTipText(name, 0, 40)
		image.SetScale(0.7, 0.7)
		image.Show()
		self.affectImageDict[affect] = image

	def __RemoveAffect(self, affect):
		"""
		if affect == chr.NEW_AFFECT_AUTO_SP_RECOVERY:
			self.autoPotionImageSP.Hide()

		if affect == chr.NEW_AFFECT_AUTO_HP_RECOVERY:
			self.autoPotionImageHP.Hide()
		"""

		if not self.affectImageDict.has_key(affect):
			print "__RemoveAffect %s ( No Affect )" % affect
			return

		print "__RemoveAffect %s ( Affect )" % affect
		del self.affectImageDict[affect]

		self.__ArrangeImageList()

	# def __ArrangeImageList(self):

		# xPos = 0
		# yPos = 0
		# AffectCount = 0

		# if self.lovePointImage:
			# if self.lovePointImage.IsShow():
				# self.lovePointImage.SetPosition(xPos, 0)
				# xPos += self.IMAGE_STEP
				# AffectCount += 1

		# if self.horseImage:
			# self.horseImage.SetPosition(xPos, 0)
			# xPos += self.IMAGE_STEP
			# AffectCount += 1

		# for image in self.affectImageDict.values():
			# image.SetPosition(xPos, yPos)
			# xPos += self.IMAGE_STEP
			# AffectCount += 1
			# if AffectCount % 8 == 0:
				# yPos += self.IMAGE_STEP
				# xPos = 0

		# self.SetSize(8 * self.IMAGE_STEP, yPos + self.IMAGE_STEP)

	def __ArrangeImageList(self):
		xPos = 0
		i = 0
		numberOnRow = 12
		
		self.SetSize(numberOnRow * self.IMAGE_STEP, 26 * 3)
		if self.lovePointImage:
			if self.lovePointImage.IsShow():
				self.lovePointImage.SetPosition(xPos, 0)
				xPos += self.IMAGE_STEP
				i = i + 1

		if self.horseImage:
			self.horseImage.SetPosition(xPos, 0)
			xPos += self.IMAGE_STEP
			i = i + 1
			
		if app.ENABLE_PREMIUM_SYSTEM:
			if self.premiumImage:
				self.premiumImage.SetPosition(xPos, 0)
				xPos += self.IMAGE_STEP
				i = i + 1

		if len(self.affectImageDict) <= 0:
			return
		
		newDict = collections.OrderedDict(sorted(self.affectImageDict.items()))
		
		for image in newDict.values():
			if i >= numberOnRow and i < numberOnRow * 2:
				image.SetPosition(xPos - (numberOnRow * self.IMAGE_STEP), 26)
				xPos += self.IMAGE_STEP
				i = i + 1
			elif i >= numberOnRow * 2 and i < numberOnRow * 3:
				image.SetPosition(xPos - ((numberOnRow * 2) * self.IMAGE_STEP), 52)
				xPos += self.IMAGE_STEP
				i = i + 1
			elif i >= numberOnRow * 3:
				image.SetPosition(xPos - ((numberOnRow * 3) * self.IMAGE_STEP), 52 + 26)
				xPos += self.IMAGE_STEP
				i = i + 1
			else:
				image.SetPosition(xPos, 0)
				xPos += self.IMAGE_STEP
				i = i + 1

	def OnUpdate(self):
		try:
			if app.GetGlobalTime() - self.lastUpdateTime > 500:
			#if 0 < app.GetGlobalTime():
				self.lastUpdateTime = app.GetGlobalTime()
				if app.ENABLE_PREMIUM_SYSTEM:
					if self.premiumImage:
						self.premiumImage.UpdateTime()

				for image in self.affectImageDict.values():
					if image.GetAffect() == chr.NEW_AFFECT_AUTO_HP_RECOVERY or image.GetAffect() == chr.NEW_AFFECT_AUTO_SP_RECOVERY:
						image.UpdateAutoPotionDescription()
						continue

					if not image.IsSkillAffect():
						image.UpdateDescription()
		except Exception, e:
			print "AffectShower::OnUpdate error : ", e

