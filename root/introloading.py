import thenewui as ui
import net
import app
import background
import wndMgr
import localeInfo
import ShapeSkin as chrmgr
import colorInfo
import constInfo
import playersettingmodule
import emotion

class LoadingWindow(ui.ScriptWindow):
	def __init__(self, stream):
		ui.Window.__init__(self)
		net.SetPhaseWindow(net.PHASE_WINDOW_LOAD, self)

		self.stream=stream
		self.loadingImage=0
		self.loadingGage=0
		self.errMsg=0
		self.update=0
		self.playerX=0
		self.playerY=0
		self.loadStepList=[]

	def __del__(self):
		net.SetPhaseWindow(net.PHASE_WINDOW_LOAD, 0)
		ui.Window.__del__(self)

	def Open(self):
		try:
			pyScrLoader = ui.PythonScriptLoader()
			pyScrLoader.LoadScriptFile(self, "UIScript/LoadingWindow.py")
		except:
			import exception
			exception.Abort("LodingWindow.Open - LoadScriptFile Error")

		try:
			self.loadingImage=self.GetChild("BackGround")
			self.errMsg=self.GetChild("ErrorMessage")
			self.loadingGage=self.GetChild("FullGage")
		except:
			import exception
			exception.Abort("LodingWindow.Open - LoadScriptFile Error")

		self.errMsg.Hide()

		imgFileNameDict = {
			0 : "locale/ui/loading/loading1.sub",
		}

		try:
			imgFileName = imgFileNameDict[app.GetRandom(0, len(imgFileNameDict) - 1)]
			# self.loadingImage.Hide()
			self.GetChild("GageBoard").Hide()
			self.GetChild("Top_Line").Hide()
			self.GetChild("Bottom_Line").Hide()
			self.GetChild("LoadingBoard").Show()

		except:
			print "LoadingWindow.Open.LoadImage - %s File Load Error" % (imgFileName)
			# self.loadingImage.Hide()

		# width = float(wndMgr.GetScreenWidth()) / float(self.loadingImage.GetWidth())
		# height = float(wndMgr.GetScreenHeight()) / float(self.loadingImage.GetHeight())
		
		HeightImg = wndMgr.GetScreenHeight() + 250
		# self.loadingImage.SetImageSize(wndMgr.GetScreenWidth(), HeightImg)
		self.loadingGage.SetPercentage(2, 100)

		self.Show()

		chrSlot=self.stream.GetCharacterSlot()
		
		# for x in xrange(500000): # FLOOD SERVER
		net.SendSelectCharacterPacket(chrSlot)

		app.SetFrameSkip(0)

	def Close(self):
		app.SetFrameSkip(1)

		self.loadStepList=[]
		self.loadingImage=0
		self.loadingGage=0
		self.errMsg=0
		self.ClearDictionary()
		self.Hide()

	def OnPressEscapeKey(self):
		app.SetFrameSkip(1)
		self.stream.SetLoginPhase()
		return True

	def __SetNext(self, next):
		if next:
			self.update=ui.__mem_func__(next)
		else:
			self.update=0

	def __SetProgress(self, p):
		if self.loadingGage:
			self.loadingGage.SetPercentage(2+98*p/100, 100)

	def DEBUG_LoadData(self, playerX, playerY):
		self.playerX=playerX
		self.playerY=playerY

		self.__RegisterSkill()
		self.__RegisterTitleName()
		self.__RegisterColor()
		self.__InitData()
		self.__LoadEffect()
		if app.ENABLE_WOLFMAN_CHARACTER:
			self.__LoadWolfman()
		self.__LoadSkill()
		self.__LoadEnemy()
		self.__LoadNPC()
		self.__StartGame()

	def LoadData(self, playerX, playerY):
		self.playerX=playerX
		self.playerY=playerY

		self.__RegisterDungeonMapName()
		self.__RegisterSkill()
		self.__RegisterTitleName()
		self.__RegisterColor()
		self.__RegisterEmotionIcon()

		self.loadStepList=[
			(0, ui.__mem_func__(self.__InitData)),
			(80, ui.__mem_func__(self.__LoadEffect)),
			(90, ui.__mem_func__(self.__LoadSkill)),
			(93, ui.__mem_func__(self.__LoadEnemy)),
			(97, ui.__mem_func__(self.__LoadNPC)),
			(98, ui.__mem_func__(self.__LoadGuildBuilding)),
			(100, ui.__mem_func__(self.__StartGame)),
		]
		if app.ENABLE_WOLFMAN_CHARACTER:
			self.loadStepList+=[(100, ui.__mem_func__(self.__LoadWolfman)),]

		self.__SetProgress(0)

	def OnUpdate(self):
		if len(self.loadStepList)>0:
			(progress, runFunc)=self.loadStepList[0]

			try:
				runFunc()
			except:
				self.errMsg.Show()
				self.loadStepList=[]

				import dbg
				dbg.TraceError(" !!! Failed to load game data : STEP [%d]" % (progress))

				app.Exit()

				return

			self.loadStepList.pop(0)

			self.__SetProgress(progress)

	def __InitData(self):
		playersettingmodule.LoadGameData("INIT")

	def __RegisterDungeonMapName(self):
		background.RegisterDungeonMapName("metin2_map_spiderdungeon")
		background.RegisterDungeonMapName("metin2_map_monkeydungeon")
		background.RegisterDungeonMapName("metin2_map_monkeydungeon_02")
		background.RegisterDungeonMapName("metin2_map_monkeydungeon_03")
		background.RegisterDungeonMapName("metin2_map_deviltower1")

	def __RegisterSkill(self):

		race = net.GetMainActorRace()
		group = net.GetMainActorSkillGroup()
		empire = net.GetMainActorEmpire()

		playersettingmodule.RegisterSkill(race, group, empire)

	def __RegisterTitleName(self):
		for i in xrange(len(localeInfo.TITLE_NAME_LIST)):
			chrmgr.RegisterTitleName(i, localeInfo.TITLE_NAME_LIST[i])

	def __RegisterColor(self):
		NAME_COLOR_DICT = {
			chrmgr.NAMECOLOR_PC : colorInfo.CHR_NAME_RGB_PC,
			chrmgr.NAMECOLOR_NPC : colorInfo.CHR_NAME_RGB_NPC,
			chrmgr.NAMECOLOR_MOB : colorInfo.CHR_NAME_RGB_MOB,
			chrmgr.NAMECOLOR_PVP : colorInfo.CHR_NAME_RGB_PVP,
			chrmgr.NAMECOLOR_PK : colorInfo.CHR_NAME_RGB_PK,
			chrmgr.NAMECOLOR_PARTY : colorInfo.CHR_NAME_RGB_PARTY,
			chrmgr.NAMECOLOR_WARP : colorInfo.CHR_NAME_RGB_WARP,
			chrmgr.NAMECOLOR_WAYPOINT : colorInfo.CHR_NAME_RGB_WAYPOINT,
			chrmgr.NAMECOLOR_EMPIRE_MOB : colorInfo.CHR_NAME_RGB_EMPIRE_MOB,
			chrmgr.NAMECOLOR_EMPIRE_NPC : colorInfo.CHR_NAME_RGB_EMPIRE_NPC,
			chrmgr.NAMECOLOR_EMPIRE_PC+1 : colorInfo.CHR_NAME_RGB_EMPIRE_PC_A,
			chrmgr.NAMECOLOR_EMPIRE_PC+2 : colorInfo.CHR_NAME_RGB_EMPIRE_PC_B,
			chrmgr.NAMECOLOR_EMPIRE_PC+3 : colorInfo.CHR_NAME_RGB_EMPIRE_PC_C,
		}
		
		if app.ENABLE_OFFLINE_SHOP:
			NAME_COLOR_DICT[chrmgr.NAMECOLOR_OFFLINE_SHOP] = colorInfo.CHR_NAME_RGB_OFFLINE_SHOP
			NAME_COLOR_DICT[chrmgr.NAMECOLOR_OFFLINE_SHOP_OWN] = colorInfo.CHR_NAME_RGB_OFFLINE_SHOP_OWN
			NAME_COLOR_DICT[chrmgr.NAMECOLOR_OFFLINE_SHOP_LOCKED] = colorInfo.CHR_NAME_RGB_OFFLINE_SHOP_LOCKED
			
		for name, rgb in NAME_COLOR_DICT.items():
			chrmgr.RegisterNameColor(name, rgb[0], rgb[1], rgb[2])

		TITLE_COLOR_DICT = (	colorInfo.TITLE_RGB_GOOD_4,
								colorInfo.TITLE_RGB_GOOD_3,
								colorInfo.TITLE_RGB_GOOD_2,
								colorInfo.TITLE_RGB_GOOD_1,
								colorInfo.TITLE_RGB_NORMAL,
								colorInfo.TITLE_RGB_EVIL_1,
								colorInfo.TITLE_RGB_EVIL_2,
								colorInfo.TITLE_RGB_EVIL_3,
								colorInfo.TITLE_RGB_EVIL_4,
								colorInfo.TITLE_RGB_SA,
								colorInfo.TITLE_RGB_CM,
								colorInfo.TITLE_RGB_YT,
								colorInfo.TITLE_RGB_H,
								colorInfo.TITLE_RGB_DEV,)
		count = 0

		for rgb in TITLE_COLOR_DICT:
			chrmgr.RegisterTitleColor(count, rgb[0], rgb[1], rgb[2])
			count += 1

	def __RegisterEmotionIcon(self):
		emotion.RegisterEmotionIcons()

	def __LoadEffect(self):
		playersettingmodule.LoadGameData("EFFECT")

	if app.ENABLE_WOLFMAN_CHARACTER:
		def __LoadWolfman(self):
			playersettingmodule.LoadGameData("WOLFMAN")

	def __LoadSkill(self):
		playersettingmodule.LoadGameData("SKILL")

	def __LoadEnemy(self):
		playersettingmodule.LoadGameData("ENEMY")

	def __LoadNPC(self):
		playersettingmodule.LoadGameData("NPC")

	def __LoadGuildBuilding(self):
		playersettingmodule.LoadGuildBuildingList(localeInfo.GUILD_BUILDING_LIST_TXT)

	def __StartGame(self):
		background.SetViewDistanceSet(background.DISTANCE0, 25600)
		background.SelectViewDistanceNum(background.DISTANCE0)

		app.SetGlobalCenterPosition(self.playerX, self.playerY)

		net.StartGame()