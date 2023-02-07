import chr
import grp
import app
import wndMgr
import net
import event
import systemSetting
import localeInfo
import ui
import uiToolTip
import uiScriptLocale
import networkModule
import playerSettingModule
import constInfo
import uiCommon                    
import uiMapNameShower             
import uiAffectShower              
import uiPlayerGauge               
import uiCharacter                 
import uiTarget                              
import interfaceModule
import uiTaskBar                   
import uiInventory
import item
import cfg
import time

M2_INIT_VALUE = -1
CHARACTER_SLOT_COUNT_MAX = 5

JOB_WARRIOR		= 0
JOB_ASSASSIN	= 1
JOB_SURA		= 2
JOB_SHAMAN		= 3
if app.ENABLE_WOLFMAN_CHARACTER:
	JOB_WOLFMAN		= 4
	
class MyCharacters :
	class MyUnit :
		def __init__(self, const_id, name, level, race, playtime, guildname, form, hair, acce, head, weapon, stat_str, stat_dex, stat_hth, stat_int, change_name):
			self.UnitDataDic = {
				"ID" 	: 	const_id,
				"NAME"	:	name,
				"LEVEL"	:	level,
				"RACE"	:	race,
				"PLAYTIME"	:	playtime,
				"GUILDNAME"	:	guildname,
				"FORM"	:	form,
				"HAIR"	:	hair,
				"ACCE"	:	acce,
				"HEAD"	:	head,
				"WEAPON"	:	weapon,
				"STR"	:	stat_str,
				"DEX"	:	stat_dex,
				"HTH"	:	stat_hth,
				"INT"	:	stat_int,
				"CHANGENAME"	:	change_name,
			}

		def __del__(self) :
			self.UnitDataDic = None
		
		def GetUnitData(self) :
			return self.UnitDataDic

	def __init__(self, stream) :
		self.MainStream = stream
		self.PriorityData = []
		self.myUnitDic = {}
		self.HowManyChar = 0
		self.EmptySlot	=  []
		self.Race 		= [None, None, None, None, None]
		self.Name 		= ["", "", "", "", ""]
		self.Job		= [None, None, None, None, None]
		self.Guild_Name = [None, None, None, None, None]
		self.Play_Time 	= [None, None, None, None, None]
		self.Change_Name= [None, None, None, None, None]
		self.Stat_Point = { 0 : None, 1 : None, 2 : None, 3 : None, 4 : None }
	
	def __del__(self) :
		self.MainStream = None 
		
		for i in xrange(self.HowManyChar) :
			chr.DeleteInstance(i)
			
		self.PriorityData = None
		self.myUnitDic = None
		self.HowManyChar = None
		self.EmptySlot	= None
		self.Race = None
		self.Name = None
		self.Job = None 		
		self.Guild_Name = None
		self.Play_Time = None
		self.Change_Name = None
		self.Stat_Point = None
			
	def LoadCharacterData(self) :
		self.RefreshData()
		self.MainStream.All_ButtonInfoHide()
		for i in xrange(CHARACTER_SLOT_COUNT_MAX) :
			pid 			= net.GetAccountCharacterSlotDataInteger(i, net.ACCOUNT_CHARACTER_SLOT_ID) 
			
			if not pid :
				self.EmptySlot.append(i)
				continue
				
			name 			= net.GetAccountCharacterSlotDataString(i, net.ACCOUNT_CHARACTER_SLOT_NAME)
			level 			= net.GetAccountCharacterSlotDataInteger(i, net.ACCOUNT_CHARACTER_SLOT_LEVEL)
			race 			= net.GetAccountCharacterSlotDataInteger(i, net.ACCOUNT_CHARACTER_SLOT_RACE)
			playtime 		= net.GetAccountCharacterSlotDataInteger(i, net.ACCOUNT_CHARACTER_SLOT_PLAYTIME)
			guildname 		= net.GetAccountCharacterSlotDataString(i, net.ACCOUNT_CHARACTER_SLOT_GUILD_NAME)
			form 			= net.GetAccountCharacterSlotDataInteger(i, net.ACCOUNT_CHARACTER_SLOT_FORM)
			hair 			= net.GetAccountCharacterSlotDataInteger(i, net.ACCOUNT_CHARACTER_SLOT_HAIR)
			stat_str 		= net.GetAccountCharacterSlotDataInteger(i, net.ACCOUNT_CHARACTER_SLOT_STR)
			stat_dex		= net.GetAccountCharacterSlotDataInteger(i, net.ACCOUNT_CHARACTER_SLOT_DEX)
			stat_hth		= net.GetAccountCharacterSlotDataInteger(i, net.ACCOUNT_CHARACTER_SLOT_HTH)
			stat_int		= net.GetAccountCharacterSlotDataInteger(i, net.ACCOUNT_CHARACTER_SLOT_INT)
			last_playtime	= net.GetAccountCharacterSlotDataInteger(i, net.ACCOUNT_CHARACTER_SLOT_ID)
			change_name		= net.GetAccountCharacterSlotDataInteger(i, net.ACCOUNT_CHARACTER_SLOT_CHANGE_NAME_FLAG)
			acce = net.GetAccountCharacterSlotDataInteger(i, net.ACCOUNT_CHARACTER_SLOT_SASH)
			head = net.GetAccountCharacterSlotDataInteger(i, net.ACCOUNT_CHARACTER_SLOT_CROWN)
			# weapon = net.GetAccountCharacterSlotDataInteger(i, net.ACCOUNT_CHARACTER_SLOT_WEAPON)
			weapon = 0

			self.SetPriorityData(last_playtime)
			self.myUnitDic[last_playtime] = self.MyUnit(i, name, level, race, playtime, guildname, form, hair, acce, head, weapon, stat_str, stat_dex, stat_hth, stat_int, change_name)

		self.PriorityData.sort(reverse = False)

		for i in xrange(len(self.PriorityData)) :
			time = self.PriorityData[i]
			DestDataDic = self.myUnitDic[time].GetUnitData()
			
			self.SetSortingData(i, DestDataDic["RACE"], DestDataDic["GUILDNAME"], DestDataDic["PLAYTIME"], DestDataDic["STR"], DestDataDic["DEX"], DestDataDic["HTH"], DestDataDic["INT"], DestDataDic["CHANGENAME"], DestDataDic["NAME"])
			self.MakeCharacter(i, DestDataDic["NAME"], DestDataDic["RACE"], DestDataDic["FORM"], DestDataDic["HAIR"], DestDataDic["ACCE"], DestDataDic["HEAD"], DestDataDic["WEAPON"])


			self.MainStream.InitDataSet(i, DestDataDic["NAME"], DestDataDic["LEVEL"], DestDataDic["ID"])

		if self.HowManyChar :
			self.MainStream.SelectButton(0)
			
		return self.HowManyChar;
		
	def SetPriorityData(self, last_playtime) :
		self.PriorityData.append(last_playtime)
	

	def MakeCharacter(self, slot, name, race, form, hair, acce, head, weapon):
		chr.CreateInstance(slot)
		chr.SelectInstance(slot)
		chr.SetVirtualID(slot)
		# myName = name.replace("#", " ") # Grimm Space-Name
		chr.SetNameString(name)
		chr.SetRace(race)
		chr.SetArmor(form)
		chr.SetHair(hair)
		chr.SetSash(acce)
		chr.SetCrown(head)
		chr.SetCanSelect(0)
		
		# if weapon > 0:
			# chr.ChangeWeapon(weapon, 0, weapon)	
		# else:			
			# chr.SetMotionMode(chr.MOTION_MODE_GENERAL)
		chr.SetLoopMotion(chr.MOTION_INTRO_WAIT)

		chr.SetRotation(0.0)
	
		chr.Hide()
	
		
	def SetSortingData(self, slot, race, guildname, playtime, pStr, pDex, pHth, pInt, changename, name = ""):	
		self.HowManyChar += 1
		self.Race[slot] = race
		self.Job[slot] = chr.RaceToJob(race)
		self.Guild_Name[slot] = guildname
		self.Play_Time[slot] = playtime
		self.Change_Name[slot] = changename
		self.Stat_Point[slot] = [pHth, pInt, pStr, pDex]
		
		self.Name[slot] = name

	def GetName(self, slot) :
		return self.Name[slot]

	def GetRace(self, slot) :
		return self.Race[slot]
	
	def GetJob(self, slot) :
		return self.Job[slot]
		
	def GetMyCharacterCount(self) :
		return self.HowManyChar
		
	def GetEmptySlot(self) :
		if not len(self.EmptySlot) :
			return M2_INIT_VALUE

		return self.EmptySlot[0]
		
	def GetStatPoint(self, slot) :			
		return self.Stat_Point[slot]
	
	def GetGuildNamePlayTime(self, slot) :
		return self.Guild_Name[slot], self.Play_Time[slot]
		
	def GetChangeName(self, slot) :
		return self.Change_Name[slot]
		
	def SetChangeNameSuccess(self, slot) :
		self.Change_Name[slot] = 0
		
	def RefreshData(self) :
		self.HowManyChar = 0
		self.EmptySlot	=  []
		self.PriorityData = []
		self.Race 		= [None, None, None, None, None]
		self.Guild_Name = [None, None, None, None, None]
		self.Play_Time 	= [None, None, None, None, None]
		self.Change_Name= [None, None, None, None, None]
		self.Stat_Point = { 0 : None, 1 : None, 2 : None, 3 : None, 4 : None }
		
class SelectCharacterWindow(ui.Window) :	
	EMPIRE_NAME = { 
		net.EMPIRE_A : localeInfo.EMPIRE_A, 
		net.EMPIRE_B : localeInfo.EMPIRE_B, 
		net.EMPIRE_C : localeInfo.EMPIRE_C 
	}
	# EMPIRE_NAME_COLOR = { 
		# net.EMPIRE_A : (0.7450, 0, 0), 
		# net.EMPIRE_B : (0.8666, 0.6156, 0.1843), 
		# net.EMPIRE_C : (0.2235, 0.2549, 0.7490) 
	# }
	RACE_FACE_PATH = {
		playerSettingModule.RACE_WARRIOR_M		:	"D:/ymir work/ui/game/select_interface/faces/icon_mwarrior",
		playerSettingModule.RACE_ASSASSIN_W		:	"D:/ymir work/ui/game/select_interface/faces/icon_wninja",
		playerSettingModule.RACE_SURA_M			:	"D:/ymir work/ui/game/select_interface/faces/icon_msura",
		playerSettingModule.RACE_SHAMAN_W		:	"D:/ymir work/ui/game/select_interface/faces/icon_wshaman",
		playerSettingModule.RACE_WARRIOR_W		:	"D:/ymir work/ui/game/select_interface/faces/icon_wwarrior",
		playerSettingModule.RACE_ASSASSIN_M		:	"D:/ymir work/ui/game/select_interface/faces/icon_mninja",
		playerSettingModule.RACE_SURA_W			:	"D:/ymir work/ui/game/select_interface/faces/icon_wsura",
		playerSettingModule.RACE_SHAMAN_M		:	"D:/ymir work/ui/game/select_interface/faces/icon_mshaman",
		playerSettingModule.RACE_WOLFMAN_M		:	"D:/ymir work/ui/game/select_interface/faces/icon_mlykaner",
	}

	DESCRIPTION_FILE_NAME =	(
		uiScriptLocale.JOBDESC_WARRIOR_PATH,
		uiScriptLocale.JOBDESC_ASSASSIN_PATH,
		uiScriptLocale.JOBDESC_SURA_PATH,
		uiScriptLocale.JOBDESC_SHAMAN_PATH,
		uiScriptLocale.JOBDESC_WOLFMAN_PATH,
	)

	JOB_LIST = { 	
		0	:	localeInfo.JOB_WARRIOR,	
		1	:	localeInfo.JOB_ASSASSIN,	
		2	:	localeInfo.JOB_SURA,
		3	:	localeInfo.JOB_SHAMAN,		 
		4	:	localeInfo.JOB_WOLFMAN,	 
	}
	
	class DescriptionBox(ui.Window):
		def __init__(self):
			ui.Window.__init__(self)
			self.descIndex = 0
		def __del__(self):
			ui.Window.__del__(self)
		def SetIndex(self, index):
			self.descIndex = index
		def OnRender(self):
			event.RenderEventSet(self.descIndex)
			
	class CharacterRenderer(ui.Window):
		def OnRender(self):
			grp.ClearDepthBuffer()

			grp.SetGameRenderState()
			grp.PushState()
			grp.SetOmniLight()

			screenWidth = wndMgr.GetScreenWidth()
			screenHeight = wndMgr.GetScreenHeight()
			newScreenWidth = float(screenWidth)
			newScreenHeight = float(screenHeight)

			grp.SetViewport(0.0, 0.0, newScreenWidth/screenWidth, newScreenHeight/screenHeight)

			app.SetCenterPosition(0.0, 0.0, 0.0) 
			app.SetCamera(1550.0, 15.0, 180.0, 95.0)
			grp.SetPerspective(10.0, newScreenWidth/newScreenHeight, 1000.0, 3000.0)
			
			(x, y) = app.GetCursorPosition()
			grp.SetCursorPosition(x, y)

			chr.Deform()
			chr.Render()
			
			# for i in xrange(5):#slotcount = 5
				# chr.SelectInstance(i)
			chr.RenderAllAttachingEffect()
				
			grp.RestoreViewport()
			grp.PopState()
			grp.SetInterfaceRenderState()
	
	def __init__(self, stream):
		ui.Window.__init__(self)
		net.SetPhaseWindow(net.PHASE_WINDOW_SELECT, self)
		self.stream = stream
		
		##Init Value##
		self.SelectSlot = M2_INIT_VALUE
		self.SelectEmpire = False
		self.ShowToolTip = False
		self.select_job = M2_INIT_VALUE
		self.select_race = M2_INIT_VALUE
		self.LEN_STATPOINT = 4
		self.descIndex = 0
		self.statpoint = [0, 0, 0, 0]
		self.curGauge  = [0.0, 0.0, 0.0, 0.0]
		self.Name_FontColor_Def	 = grp.GenerateColor(0.7215, 0.7215, 0.7215, 1.0)
		self.Name_FontColor		 = grp.GenerateColor(197.0/255.0, 134.0/255.0, 101.0/255.0, 1.0)
		self.Level_FontColor 	 = grp.GenerateColor(250.0/255.0, 211.0/255.0, 136.0/255.0, 1.0)
		self.Text_FontC 	 = grp.GenerateColor(0.996,0.686,0.518,1.0)
		self.Not_SelectMotion = False
		self.MotionStart = False
		self.MotionTime = 0.0
		self.RealSlot = []
		self.Disable = False

	def __del__(self):
		ui.Window.__del__(self)
		net.SetPhaseWindow(net.PHASE_WINDOW_SELECT, 0)
		
	def Open(self):
		playerSettingModule.LoadGameData("INIT")
		# deimos2chrmgr.StartLoadPlayerInfo()

		dlgBoard = ui.ScriptWindow()
		self.dlgBoard = dlgBoard
		pythonScriptLoader = ui.PythonScriptLoader()
		pythonScriptLoader.LoadScriptFile( self.dlgBoard, "uiscript/New_SelectCharacterWindow.py" ) 
		getChild = self.dlgBoard.GetChild

		# self.backGroundDict = {
			# net.EMPIRE_A : "d:/ymir work/ui/intro/empire/background/empire_shinsoo.sub",
			# net.EMPIRE_B : "d:/ymir work/ui/intro/empire/background/empire_chunjo.sub",
			# net.EMPIRE_C : "d:/ymir work/ui/intro/empire/background/empire_jinno.sub",
		# }
		self.backGround = getChild("BackGround")

		#self.NameList = []
		#self.NameList.append(getChild("name_warrior"))
		#self.NameList.append(getChild("name_assassin"))
		#self.NameList.append(getChild("name_sura"))
		#self.NameList.append(getChild("name_shaman"))
		#self.NameList.append(getChild("name_wolfman"))

		# self.empireName = getChild("EmpireName")
		self.flagDict = {
			net.EMPIRE_A : "d:/ymir work/ui/game/select_interface/red_kingdom.png",
			net.EMPIRE_B : "d:/ymir work/ui/game/select_interface/yellow_kingdom.png",
			net.EMPIRE_C : "d:/ymir work/ui/game/select_interface/blue_king.png",
		}
		self.flag = getChild("EmpireFlag")

		##Button List##
		self.btnStart		= getChild("start_button")
		self.btnCreate		= getChild("create_button")
		self.btnDelete		= getChild("delete_button")
		self.btnExit		= getChild("exit_button")
		
		##Face Image##
		self.FaceImage = []
		self.FaceImage.append(getChild("CharacterFace_0"))
		self.FaceImage.append(getChild("CharacterFace_1"))
		self.FaceImage.append(getChild("CharacterFace_2"))
		self.FaceImage.append(getChild("CharacterFace_3"))
		self.FaceImage.append(getChild("CharacterFace_4"))
		
		##Select Character List##
		self.CharacterButtonList = []
		self.CharacterButtonList.append(getChild("CharacterSlot_0"))
		self.CharacterButtonList.append(getChild("CharacterSlot_1"))
		self.CharacterButtonList.append(getChild("CharacterSlot_2"))
		self.CharacterButtonList.append(getChild("CharacterSlot_3"))
		self.CharacterButtonList.append(getChild("CharacterSlot_4"))
		
		##ToolTip : GuildName, PlayTime##
		getChild("CharacterSlot_0").ShowToolTip = lambda arg = 0 : self.OverInToolTip(arg)
		getChild("CharacterSlot_0").HideToolTip = lambda : self.OverOutToolTip()
		getChild("CharacterSlot_1").ShowToolTip = lambda arg = 1 : self.OverInToolTip(arg)
		getChild("CharacterSlot_1").HideToolTip = lambda : self.OverOutToolTip()
		getChild("CharacterSlot_2").ShowToolTip = lambda arg = 2 : self.OverInToolTip(arg)
		getChild("CharacterSlot_2").HideToolTip = lambda : self.OverOutToolTip()
		getChild("CharacterSlot_3").ShowToolTip = lambda arg = 3 : self.OverInToolTip(arg)
		getChild("CharacterSlot_3").HideToolTip = lambda : self.OverOutToolTip()
		getChild("CharacterSlot_4").ShowToolTip = lambda arg = 4 : self.OverInToolTip(arg)
		getChild("CharacterSlot_4").HideToolTip = lambda : self.OverOutToolTip()
		
		## ToolTip etc : Create, Delete, Start, Exit, Prev, Next ##
		getChild("create_button").ShowToolTip = lambda arg = uiScriptLocale.SELECT_CREATE : self.OverInToolTipETC(arg)
		getChild("create_button").HideToolTip = lambda : self.OverOutToolTip()
		getChild("delete_button").ShowToolTip = lambda arg = uiScriptLocale.SELECT_DELETE : self.OverInToolTipETC(arg)
		getChild("delete_button").HideToolTip = lambda : self.OverOutToolTip()
		getChild("start_button").ShowToolTip = lambda arg = uiScriptLocale.SELECT_SELECT : self.OverInToolTipETC(arg)
		getChild("start_button").HideToolTip = lambda : self.OverOutToolTip()
		getChild("exit_button").ShowToolTip = lambda arg = uiScriptLocale.SELECT_EXIT : self.OverInToolTipETC(arg)
		getChild("exit_button").HideToolTip = lambda : self.OverOutToolTip()
		
		
		##StatPoint Value##
		self.statValue = []
		self.statValue.append(getChild("hth_value"))
		self.statValue.append(getChild("int_value"))
		self.statValue.append(getChild("str_value"))
		self.statValue.append(getChild("dex_value"))
		
		##Gauge UI##
		self.GaugeList = []
		self.GaugeList.append(getChild("hth_gauge"))
		self.GaugeList.append(getChild("int_gauge"))
		self.GaugeList.append(getChild("str_gauge"))
		self.GaugeList.append(getChild("dex_gauge"))

		##Button Event##
		self.btnStart.SetEvent(ui.__mem_func__(self.StartGameButton))
		self.btnCreate.SetEvent(ui.__mem_func__(self.CreateCharacterButton))
		self.btnExit.SetEvent(ui.__mem_func__(self.ExitButton))
		self.btnDelete.SetEvent(ui.__mem_func__(self.InputPrivateCode))		
		
		##Select MyCharacter##
		self.CharacterButtonList[0].SetEvent(ui.__mem_func__(self.SelectButton), 0)
		self.CharacterButtonList[1].SetEvent(ui.__mem_func__(self.SelectButton), 1)
		self.CharacterButtonList[2].SetEvent(ui.__mem_func__(self.SelectButton), 2)
		self.CharacterButtonList[3].SetEvent(ui.__mem_func__(self.SelectButton), 3)
		self.CharacterButtonList[4].SetEvent(ui.__mem_func__(self.SelectButton), 4)
		
		self.FaceImage[0].SetEvent(ui.__mem_func__(self.EventProgress), "MOUSE_LEFT_BUTTON_UP", 0)
		self.FaceImage[1].SetEvent(ui.__mem_func__(self.EventProgress), "MOUSE_LEFT_BUTTON_UP", 1)
		self.FaceImage[2].SetEvent(ui.__mem_func__(self.EventProgress), "MOUSE_LEFT_BUTTON_UP", 2)
		self.FaceImage[3].SetEvent(ui.__mem_func__(self.EventProgress), "MOUSE_LEFT_BUTTON_UP", 3)
		self.FaceImage[4].SetEvent(ui.__mem_func__(self.EventProgress), "MOUSE_LEFT_BUTTON_UP", 4)
		
		self.FaceImage[0].SetEvent(ui.__mem_func__(self.EventProgress), "MOUSE_OVER_IN", 0)
		self.FaceImage[1].SetEvent(ui.__mem_func__(self.EventProgress), "MOUSE_OVER_IN", 1)
		self.FaceImage[2].SetEvent(ui.__mem_func__(self.EventProgress), "MOUSE_OVER_IN", 2)
		self.FaceImage[3].SetEvent(ui.__mem_func__(self.EventProgress), "MOUSE_OVER_IN", 3)
		self.FaceImage[4].SetEvent(ui.__mem_func__(self.EventProgress), "MOUSE_OVER_IN", 4)
		
		self.FaceImage[0].SetEvent(ui.__mem_func__(self.EventProgress), "MOUSE_OVER_OUT", 0)
		self.FaceImage[1].SetEvent(ui.__mem_func__(self.EventProgress), "MOUSE_OVER_OUT", 1)
		self.FaceImage[2].SetEvent(ui.__mem_func__(self.EventProgress), "MOUSE_OVER_OUT", 2)
		self.FaceImage[3].SetEvent(ui.__mem_func__(self.EventProgress), "MOUSE_OVER_OUT", 3)
		self.FaceImage[4].SetEvent(ui.__mem_func__(self.EventProgress), "MOUSE_OVER_OUT", 4)

		##MyCharacter CLASS##
		self.mycharacters = MyCharacters(self);
		self.mycharacters.LoadCharacterData()
				
		if not self.mycharacters.GetMyCharacterCount() :
			self.stream.SetCharacterSlot(self.mycharacters.GetEmptySlot())
			self.SelectEmpire = True
		
		##Job Description Box##
		self.descriptionBox = self.DescriptionBox()
		self.descriptionBox.Show()
		
		##Tool Tip(Guild Name, PlayTime)##
		self.toolTip = uiToolTip.ToolTip()
		self.toolTip.ClearToolTip()
		
		self.dlgBoard.Show()
		self.SetWindowName("SelectCharacterWindow")
		self.Show()
		self.SetFocus()
		
		my_empire = net.GetEmpireID()
		self.SetEmpire(my_empire)
	
		app.ShowCursor()
		##Character Render##
		self.chrRenderer = self.CharacterRenderer()
		self.chrRenderer.SetParent(self.backGround)
		self.chrRenderer.Show()
		
		if self.stream.isAutoSelect:
			chrSlot=self.stream.GetCharacterSlot()
			self.SelectSlot = chrSlot
			self.StartGameButton()
		
		##Default Setting##
	def EventProgress(self, event_type, slot) :
		if self.Disable :
			return

		if "MOUSE_LEFT_BUTTON_UP" == event_type :
			if slot == self.SelectSlot :
				return 
				
			#snd.PlaySound("sound/ui/click.wav")
			self.SelectButton(slot)
		elif "MOUSE_OVER_IN" == event_type :
			for button in self.CharacterButtonList :
				button.SetUp()
		
			# self.CharacterButtonList[slot].Over()
			self.CharacterButtonList[self.SelectSlot].Down()
			self.OverInToolTip(slot)
		elif "MOUSE_OVER_OUT" == event_type :
			for button in self.CharacterButtonList :
				button.SetUp()
			
			self.CharacterButtonList[self.SelectSlot].Down()
			self.OverOutToolTip()

	def SelectButton(self, slot):		
		if slot >= self.mycharacters.GetMyCharacterCount() or slot == self.SelectSlot :
			return
			
		if self.Not_SelectMotion or self.MotionTime != 0.0 :
			self.CharacterButtonList[slot].SetUp()
			self.CharacterButtonList[slot].Over()
			return
		
		for button in self.CharacterButtonList:
			button.SetUp()
					
		self.SelectSlot = slot
		self.CharacterButtonList[self.SelectSlot].Down()
		self.stream.SetCharacterSlot(self.RealSlot[self.SelectSlot])
		
		self.select_job = self.mycharacters.GetJob(self.SelectSlot)
		
		##Job Descirption##
		event.ClearEventSet(self.descIndex)
		self.descIndex = event.RegisterEventSet(self.DESCRIPTION_FILE_NAME[self.select_job])
		event.SetFontColor(self.descIndex, 0.7843, 0.7843, 0.7843)
		
		event.SetRestrictedCount(self.descIndex, 35)
		
		self.ResetStat()
		
		## ÇÑ¹® Setting ##
		#for i in xrange(len(self.NameList)):
		#	if self.select_job == i	: 
		#		self.NameList[i].SetAlpha(1)
		#	else :
		#		self.NameList[i].SetAlpha(0)
		
		## Face Setting & Font Color Setting ##
		self.select_race = self.mycharacters.GetRace(self.SelectSlot)
		for i in xrange(self.mycharacters.GetMyCharacterCount()) :
			if slot == i :
				self.FaceImage[slot].LoadImage(self.RACE_FACE_PATH[self.select_race] + ".png")
				# self.CharacterButtonList[slot].SetAppendTextColor(0, self.Name_FontColor)
			else :
				self.FaceImage[i].LoadImage(self.RACE_FACE_PATH[self.mycharacters.GetRace(i)] + ".png")
				# self.CharacterButtonList[i].SetAppendTextColor(0, self.Name_FontColor_Def)
		
		chr.Hide()
		chr.SelectInstance(self.SelectSlot)
		chr.Show()
				
		## WEAPONNNNNNNNNN
		# weapon = net.GetAccountCharacterSlotDataInteger(self.SelectSlot, net.ACCOUNT_CHARACTER_SLOT_WEAPON)
		# if weapon > 0:
			# chr.ChangeWeapon(weapon, 0, weapon)	
		
	def Close(self):
		del self.mycharacters
		self.EMPIRE_NAME = None
		# self.EMPIRE_NAME_COLOR = None
		self.RACE_FACE_PATH = None
		#self.DISC_FACE_PATH = None
		self.DESCRIPTION_FILE_NAME = None
		self.JOB_LIST = None
		
		##Default Value##
		self.SelectSlot = None
		self.SelectEmpire = None
		self.ShowToolTip = None
		self.LEN_STATPOINT = None
		self.descIndex = None
		self.statpoint = None#[]
		self.curGauge  = None#[]
		self.Name_FontColor_Def	 = None
		self.Name_FontColor		 = None
		self.Level_FontColor 	 = None
		self.Not_SelectMotion = None
		self.MotionStart = None
		self.MotionTime = None
		self.RealSlot = None
	
		self.select_job = None
		self.select_race = None
		
		##Open Func##
		self.dlgBoard = None
		self.backGround = None
		# self.backGroundDict = None
		#self.NameList = None#[]
		self.empireName = None
		self.flag = None
		self.flagDict = None#{}
		self.btnStart = None	
		self.btnCreate = None	
		self.btnDelete = None	
		self.btnExit = None	
		self.FaceImage = None#[]
		self.CharacterButtonList = None#[]
		self.statValue = None#[]
		self.GaugeList = None#[]
		#self.raceNameText = None
		#self.descPhaseText = None
		
		self.descriptionBox = None
		self.toolTip = None
		self.Disable = None
		
		self.Hide()
		self.KillFocus()
		app.HideCursor()
		event.Destroy()
		
	def SetEmpire(self, empire_id):
		# self.empireName.SetText(self.EMPIRE_NAME.get(empire_id, ""))
		# rgb = self.EMPIRE_NAME_COLOR[empire_id]
		# self.empireName.SetFontColor(rgb[0], rgb[1], rgb[2])
		# if empire_id != net.EMPIRE_A :
		self.flag.LoadImage(self.flagDict[empire_id])
		# self.flag.SetScale(0.45, 0.45)

	def CreateCharacterButton(self):
		slotNumber = self.mycharacters.GetEmptySlot()
			
		if slotNumber == M2_INIT_VALUE :
			# self.btnCreate.Hide()
			self.stream.popupWindow.Close()
			self.stream.popupWindow.Open(localeInfo.CREATE_FULL, 0, localeInfo.UI_OK)
			return 
		
		pid = self.GetCharacterSlotPID(slotNumber)
		
		if not pid:
			self.stream.SetCharacterSlot(slotNumber)

			if not self.mycharacters.GetMyCharacterCount() :
				self.SelectEmpire = True
			else :
				self.stream.SetCreateCharacterPhase()
				self.Hide()
		
		if self.SelectEmpire :
			self.SelectEmpire = False
			self.stream.SetReselectEmpirePhase()
			self.Hide()
			
	def ExitButton(self):
		self.stream.SetLoginPhase()		
		self.Hide()
		
	def StartGameButton(self):
		if not self.mycharacters.GetMyCharacterCount() or self.MotionTime != 0.0 :
			return
		
		self.DisableWindow()
		
		IsChangeName = self.mycharacters.GetChangeName(self.SelectSlot)
		if IsChangeName :
			self.OpenChangeNameDialog()
			return

		chr.PushOnceMotion(chr.MOTION_INTRO_SELECTED)
		self.MotionStart = True
		self.MotionTime = app.GetTime() - 5
	
	def OnUpdate(self):
		chr.Update()
		chr.EffectUpdate()
		self.ToolTipProgress()
		
		slotNumber = self.mycharacters.GetEmptySlot()
			
		if slotNumber == M2_INIT_VALUE :
			self.btnCreate.Hide()
		else:
			self.btnCreate.Show()
		
		# if self.SelectEmpire :
			# self.SelectEmpire = False
			# self.stream.SetReselectEmpirePhase()
			# self.Hide()
			
		if self.MotionStart and app.GetTime() - self.MotionTime >= 2.0 :
			self.MotionStart = False
			chrSlot = self.stream.GetCharacterSlot()
			net.DirectEnter(chrSlot)
			playTime = net.GetAccountCharacterSlotDataInteger(chrSlot, net.ACCOUNT_CHARACTER_SLOT_PLAYTIME)

			import player
			player.SetPlayTime(playTime)
			
			import chat
			chat.Clear()

		for i in xrange(self.LEN_STATPOINT):
			self.GaugeList[i].SetPercentage(self.curGauge[i], 1.0)
	
	# def Refresh(self):
	def GetCharacterSlotPID(self, slotIndex):
		return net.GetAccountCharacterSlotDataInteger(slotIndex, net.ACCOUNT_CHARACTER_SLOT_ID)
	
	def All_ButtonInfoHide(self) :
		for i in xrange(CHARACTER_SLOT_COUNT_MAX):
			self.CharacterButtonList[i].Hide()
			self.FaceImage[i].Hide()
			
	def InitDataSet(self, slot, name, level, real_slot):	
		width = self.CharacterButtonList[slot].GetWidth()
		height = self.CharacterButtonList[slot].GetHeight()
		myName = name.replace("#", " ") # Grimm Space-Name

		self.CharacterButtonList[slot].AppendTextLine(myName , localeInfo.UI_DEF_FONT, self.Text_FontC	, "left", 97, 23)
		self.CharacterButtonList[slot].AppendTextLine("Lv." + str(level), localeInfo.UI_DEF_FONT, self.Text_FontC		, "left", width - 38, (height*3/4) -7)
		
		GuildName = localeInfo.GUILD_NAME
		myGuildName, myPlayTime = self.mycharacters.GetGuildNamePlayTime(slot)
		pos_x, pos_y = self.CharacterButtonList[slot].GetGlobalPosition()
		
		if not myGuildName :
			myGuildName = localeInfo.SELECT_NOT_JOIN_GUILD

		# guild_name = GuildName + " : " + myGuildName
		
		self.CharacterButtonList[slot].AppendTextLine(myGuildName , localeInfo.UI_DEF_FONT, self.Text_FontC	, "left", 103, 40)

		self.CharacterButtonList[slot].Show()
		self.FaceImage[slot].LoadImage(self.RACE_FACE_PATH[self.mycharacters.GetRace(slot)] + ".png")
		self.FaceImage[slot].Show()
		self.RealSlot.append(real_slot)
				
	def InputPrivateCode(self) :
		if not self.mycharacters.GetMyCharacterCount() :
			return
			
		privateInputBoard = uiCommon.InputDialogWithDescription()
		privateInputBoard.SetTitle(localeInfo.INPUT_PRIVATE_CODE_DIALOG_TITLE)
		privateInputBoard.SetAcceptEvent(ui.__mem_func__(self.AcceptInputPrivateCode))
		privateInputBoard.SetCancelEvent(ui.__mem_func__(self.CancelInputPrivateCode))
		privateInputBoard.SetNumberMode()
			
		privateInputBoard.SetSecretMode()
		privateInputBoard.SetMaxLength(7)
			
		privateInputBoard.SetBoardWidth(250)
		privateInputBoard.SetDescription(localeInfo.INPUT_PRIVATE_CODE_DIALOG_DESCRIPTION)
		privateInputBoard.Open()
		self.privateInputBoard = privateInputBoard
		
		self.DisableWindow()
		
		if not self.Not_SelectMotion:
			self.Not_SelectMotion = True
			chr.PushOnceMotion(chr.MOTION_INTRO_NOT_SELECTED, 0.1)
		
	def AcceptInputPrivateCode(self) :
		privateCode = self.privateInputBoard.GetText()
		if not privateCode:
			return
		
		pid = net.GetAccountCharacterSlotDataInteger(self.RealSlot[self.SelectSlot], net.ACCOUNT_CHARACTER_SLOT_ID)
		
		if not pid :
			self.PopupMessage(localeInfo.SELECT_EMPTY_SLOT)
			return

		net.SendDestroyCharacterPacket(self.RealSlot[self.SelectSlot], privateCode)
		self.PopupMessage(localeInfo.SELECT_DELEING)

		self.CancelInputPrivateCode()
		return True
	
	def CancelInputPrivateCode(self) :
		self.privateInputBoard = None
		self.Not_SelectMotion = False
		chr.SetLoopMotion(chr.MOTION_INTRO_WAIT)
		self.EnableWindow()
		return True
		
	def OnDeleteSuccess(self, slot):
		self.PopupMessage(localeInfo.SELECT_DELETED)
		for i in xrange(len(self.RealSlot)):
			chr.DeleteInstance(i)
			
		self.RealSlot = []
		self.SelectSlot = M2_INIT_VALUE
		
		for button in self.CharacterButtonList :
			button.AppendTextLineAllClear()
					
		if not self.mycharacters.LoadCharacterData() :
			self.stream.popupWindow.Close()
			self.stream.SetCharacterSlot(self.mycharacters.GetEmptySlot())
			self.SelectEmpire = True
	
	def OnDeleteFailure(self):
		self.PopupMessage(localeInfo.SELECT_CAN_NOT_DELETE)
	
	def OnDeleteTimeIsTooLow(self):
		self.PopupMessage("Poti sterge caracterul dupa 24 ore de la creearea sa.")
		
	def EmptyFunc(self):
		pass

	def PopupMessage(self, msg, func=0):
		if not func:
			func=self.EmptyFunc

		self.stream.popupWindow.Close()
		self.stream.popupWindow.Open(msg, func, localeInfo.UI_OK)
	
	def RefreshStat(self):
		statSummary = 90.0 
		self.curGauge =	[
			float(self.statpoint[0])/statSummary,
			float(self.statpoint[1])/statSummary,
			float(self.statpoint[2])/statSummary,
			float(self.statpoint[3])/statSummary,
		]
							
		for i in xrange(self.LEN_STATPOINT) :
			self.statValue[i].SetText(str(self.statpoint[i]))

	def ResetStat(self):
		myStatPoint = self.mycharacters.GetStatPoint(self.SelectSlot)
		
		if not myStatPoint :
			return
		
		for i in xrange(self.LEN_STATPOINT) :
			self.statpoint[i] = myStatPoint[i]
		
		self.RefreshStat()
	
	##Job Description Prev & Next Button##
	def PrevDescriptionPage(self):
		if True == event.IsWait(self.descIndex) :
			if event.GetVisibleStartLine(self.descIndex) - event.BOX_VISIBLE_LINE_COUNT >= 0:
				event.SetVisibleStartLine(self.descIndex, event.GetVisibleStartLine(self.descIndex) - event.BOX_VISIBLE_LINE_COUNT)
				event.Skip(self.descIndex)
		else :
			event.Skip(self.descIndex)
	
	def NextDescriptionPage(self):
		if True == event.IsWait(self.descIndex) :
			event.SetVisibleStartLine(self.descIndex, event.GetVisibleStartLine(self.descIndex) + event.BOX_VISIBLE_LINE_COUNT)
			event.Skip(self.descIndex)
		else :
			event.Skip(self.descIndex)
	
	##ToolTip : GuildName, PlayTime##
	def OverInToolTip(self, slot) :
		GuildName = localeInfo.GUILD_NAME
		myGuildName, myPlayTime = self.mycharacters.GetGuildNamePlayTime(slot)
		pos_x, pos_y = self.CharacterButtonList[slot].GetGlobalPosition()
		
		if not myGuildName :
			myGuildName = localeInfo.SELECT_NOT_JOIN_GUILD

		guild_name = GuildName + " : " + myGuildName
		play_time = uiScriptLocale.SELECT_PLAYTIME + " :"
		day = myPlayTime / (60 * 24)
		if day : 
			play_time = play_time + " " + str(day) + localeInfo.DAY
		hour = (myPlayTime - (day * 60 * 24))/60
		if hour :
			play_time = play_time + " " + str(hour) + localeInfo.HOUR
		min = myPlayTime - (hour * 60) - (day * 60 * 24)
	
		play_time = play_time + " " + str(min) + localeInfo.MINUTE
		
		textlen = max(len(guild_name), len(play_time))
		tooltip_width = 6 * textlen + 22

		self.toolTip.ClearToolTip()
		self.toolTip.SetThinBoardSize(tooltip_width)

		self.toolTip.SetToolTipPosition(pos_x + 173 + tooltip_width/2, pos_y + 34)
		self.toolTip.AppendTextLine(guild_name, 0xffe4cb1b, False) 	##YELLOW## 
		self.toolTip.AppendTextLine(play_time, 0xffffff00, False) 	##YELLOW## 

		self.toolTip.Show()
	
	def OverInToolTipETC(self, arg) :
		arglen = len(str(arg))
		pos_x, pos_y = wndMgr.GetMousePosition()
		
		self.toolTip.ClearToolTip()
		self.toolTip.SetThinBoardSize(11 * arglen)
		self.toolTip.SetToolTipPosition(pos_x + 50, pos_y + 50)
		self.toolTip.AppendTextLine(arg, 0xffffff00)
		self.toolTip.Show()
		self.ShowToolTip = True
		
	def OverOutToolTip(self) :
		self.toolTip.Hide()
		self.ShowToolTip = False
	
	def ToolTipProgress(self) :
		if self.ShowToolTip :
			pos_x, pos_y = wndMgr.GetMousePosition()
			self.toolTip.SetToolTipPosition(pos_x + 50, pos_y + 50)
	
	def SameLoginDisconnect(self):
		self.stream.popupWindow.Close()
		self.stream.popupWindow.Open(localeInfo.LOGIN_FAILURE_SAMELOGIN, self.ExitButton, localeInfo.UI_OK)
		
	def OnKeyDown(self, key):
		if self.MotionTime != 0.0 :
			return
			
		if 1 == key:
			self.ExitButton()
		elif 2 == key:
			self.SelectButton(0)
		elif 3 == key:
			self.SelectButton(1)
		elif 4 == key:
			self.SelectButton(2)
		elif 5 == key:
			self.SelectButton(3)
		elif 6 == key:
			self.SelectButton(4)
		elif 28 == key:
			self.StartGameButton()
		elif 200 == key or 208 == key :
			self.KeyInputUpDown(key)
		else:
			return True

		return True
		
	def KeyInputUpDown(self, key) :
		idx = self.SelectSlot
		maxValue = self.mycharacters.GetMyCharacterCount()
		if 200 == key:
			idx = idx - 1
			if idx < 0 :
				idx = maxValue - 1
 
		elif 208 == key:
			idx = idx + 1 
			if idx >= maxValue :
				idx = 0
		else:
			self.SelectButton(0)

		self.SelectButton(idx)

	def OnPressExitKey(self):
		self.ExitButton()
		return True
	
	def DisableWindow(self):
		self.btnStart.Disable()
		self.btnCreate.Disable()
		self.btnExit.Disable()
		self.btnDelete.Disable()
		self.toolTip.Hide()
		self.ShowToolTip = False
		self.Disable = True
		for button in self.CharacterButtonList :
			button.Disable()

	def EnableWindow(self):
		self.btnStart.Enable()
		self.btnCreate.Enable()
		self.btnExit.Enable()
		self.btnDelete.Enable()
		self.Disable = False
		for button in self.CharacterButtonList :
			button.Enable()

	def OpenChangeNameDialog(self):
		import uiCommon
		nameInputBoard = uiCommon.InputDialogWithDescription()
		nameInputBoard.SetTitle(localeInfo.SELECT_CHANGE_NAME_TITLE)
		nameInputBoard.SetAcceptEvent(ui.__mem_func__(self.AcceptInputName))
		nameInputBoard.SetCancelEvent(ui.__mem_func__(self.CancelInputName))
		nameInputBoard.SetMaxLength(chr.PLAYER_NAME_MAX_LEN)
		nameInputBoard.SetBoardWidth(200)
		nameInputBoard.SetDescription(localeInfo.SELECT_INPUT_CHANGING_NAME)
		nameInputBoard.Open()
		nameInputBoard.slot = self.RealSlot[self.SelectSlot]
		self.nameInputBoard = nameInputBoard
		
	def AcceptInputName(self):
		changeName = self.nameInputBoard.GetText()
		if not changeName:
			return

		net.SendChangeNamePacket(self.nameInputBoard.slot, changeName)
		return self.CancelInputName()

	def CancelInputName(self):
		self.nameInputBoard.Close()
		self.nameInputBoard = None
		self.EnableWindow()
		return True

	def OnCreateFailure(self, type):
		if 0 == type:
			self.PopupMessage(localeInfo.SELECT_CHANGE_FAILURE_STRANGE_NAME)
		elif 1 == type:
			self.PopupMessage(localeInfo.SELECT_CHANGE_FAILURE_ALREADY_EXIST_NAME)
		elif 100 == type:
			self.PopupMessage(localeInfo.SELECT_CHANGE_FAILURE_STRANGE_INDEX)
			
	def OnChangeName(self, slot, name):
		for i in xrange(len(self.RealSlot)) :
			if self.RealSlot[i] == slot :
				self.ChangeNameButton(i, name)
				self.SelectButton(i)
				self.PopupMessage(localeInfo.SELECT_CHANGED_NAME)
				break
				
	def ChangeNameButton(self, slot, name) :
		self.CharacterButtonList[slot].SetAppendTextChangeText(0, name)
		self.mycharacters.SetChangeNameSuccess(slot)

