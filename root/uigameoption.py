import thenewui as ui
import systemSetting
import net
import chat
import app
import localeInfo
import constInfo
import ShapeSkin as chrmgr
import CacheEffect as player
import uiPrivateShopBuilder
import interfaceModule
import background
import os
import cfg
import textTail

blockMode = 0
viewChatMode = 0

if app.ENABLE_DOG_MODE:
	import playerSettingModule

class OptionDialog(ui.ScriptWindow):

	def __init__(self):
		ui.ScriptWindow.__init__(self)
		self.__Initialize()
		self.__Load()
		self.RefreshAlwaysShowName()
		if app.ENABLE_DOG_MODE:
			self.RefreshDogModeStatus()
			
	def __del__(self):
		ui.ScriptWindow.__del__(self)
		print " -------------------------------------- DELETE GAME OPTION DIALOG"

	def __Initialize(self):
		self.titleBar = 0

		self.nameColorModeButtonList = 0
		self.pvpModeButtonDict = {}
		self.blockButtonList = []
		self.cameraModeButtonList = []
		self.fogModeButtonList = []
		self.tilingModeButtonList = []
		self.alwaysShowNameButtonList = 0
		self.EnvModeOption = []
		self.gameOptionButton = []
		self.gameOptionBackground = []
		self.gamecharButton = []
		self.gameOptions = []
		self.graphicsButton = []
		self.graphicsBg = []
		self.targetMenuModeButtonList = []
		self.chatLineModeButtonList = []
		self.damageModeButtonList = []
		self.shopNameButtonList = []
		self.noticeModeButtonList = []
		self.showEffectsButtonList = []
		self.missionsButtonList = []
		self.affectButtonList = []
		self.animButtonList = []
		# self.interfaceButtonList = []
		self.nightButtonList = []
		self.fovSlider = 0
		self.scaleSlider = 0
		self.showNewHideButtonList = []
		if app.ENABLE_DOG_MODE:
			self.dogModeStatusButtonList = []

	def Destroy(self):
		self.ClearDictionary()

		self.__Initialize()
		print " -------------------------------------- DESTROY GAME OPTION DIALOG"
	
	def __Load_LoadScript(self, fileName):
		try:
			pyScriptLoader = ui.PythonScriptLoader()
			pyScriptLoader.LoadScriptFile(self, fileName)
		except:
			import exception
			exception.Abort("OptionDialog.__Load_LoadScript")

	def __Load_BindObject(self):
		try:
			GetObject = self.GetChild
			self.titleBar = GetObject("titlebar")

			## work

			## Character
			self.nameColorModeButtonList = GetObject("name_color")
			self.alwaysShowNameButtonList = GetObject("always_show_name")
			# self.alwaysShowNameButtonPartialList = GetObject("always_show_name_partial")

			self.pvpModeButtonDict[player.PK_MODE_PEACE] = GetObject("pvp_peace")
			self.pvpModeButtonDict[player.PK_MODE_REVENGE] = GetObject("pvp_revenge")
			self.pvpModeButtonDict[player.PK_MODE_GUILD] = GetObject("pvp_guild")
			self.pvpModeButtonDict[player.PK_MODE_FREE] = GetObject("pvp_free")

			self.blockButtonList.append(GetObject("block_exchange_button"))
			self.blockButtonList.append(GetObject("block_party_button"))
			self.blockButtonList.append(GetObject("block_guild_button"))
			self.blockButtonList.append(GetObject("block_whisper_button"))
			self.blockButtonList.append(GetObject("block_friend_button"))
			self.blockButtonList.append(GetObject("block_party_request_button"))

			## End of Character

			## Graphics
			self.cameraModeButtonList.append(GetObject("camera_mode_1"))
			self.cameraModeButtonList.append(GetObject("camera_mode_2"))
			self.fogModeButtonList.append(GetObject("fog_level0"))
			self.fogModeButtonList.append(GetObject("fog_level1"))
			self.fogModeButtonList.append(GetObject("fog_level2"))
			self.tilingModeButtonList.append(GetObject("tiling_cpu"))
			self.tilingModeButtonList.append(GetObject("tiling_gpu"))
			## End of graphics
			
			self.targetMenuModeButtonList.append(GetObject("target_board_on"))
			self.targetMenuModeButtonList.append(GetObject("target_board_off"))
			
			self.chatLineModeButtonList.append(GetObject("chat_mode_on"))
			self.chatLineModeButtonList.append(GetObject("chat_mode_off"))
			
			self.damageModeButtonList.append(GetObject("damage_mode_on"))
			self.damageModeButtonList.append(GetObject("damage_mode_off"))

			self.shopNameButtonList.append(GetObject("shopname_mode_on"))
			self.shopNameButtonList.append(GetObject("shopname_mode_off"))

			self.noticeModeButtonList.append(GetObject("notice_mode_on"))
			self.noticeModeButtonList.append(GetObject("notice_mode_off"))
			
			self.showEffectsButtonList.append(GetObject("hide_effects_on"))
			self.showEffectsButtonList.append(GetObject("hide_effects_off"))
			
			self.missionsButtonList.append(self.GetChild("missions_off"))
			self.missionsButtonList.append(self.GetChild("missions_on"))

			self.affectButtonList.append(self.GetChild("affects_off"))
			self.affectButtonList.append(self.GetChild("affects_on"))
		
			self.animButtonList.append(self.GetChild("anim_off"))
			self.animButtonList.append(self.GetChild("anim_on"))
				
			# self.interfaceButtonList.append(self.GetChild("interface_off"))
			# self.interfaceButtonList.append(self.GetChild("interface_on"))
						
			self.nightButtonList.append(self.GetChild("night_off"))
			self.nightButtonList.append(self.GetChild("night_on"))
		
			## UI
			# self.enable_hd_mode = GetObject("hd_mode")
			## End of UI
	
			self.fovSlider = self.GetChild("fov_bar")
			self.scaleSlider = self.GetChild("scale_bar")
			
			self.showNewHideButtonList.append(self.GetChild("hide_pets"))
			self.showNewHideButtonList.append(self.GetChild("hide_mounts"))
			self.showNewHideButtonList.append(self.GetChild("hide_shops"))
			
			## Ambient
			# self.EnvModeOption.append(GetObject("env_01"))
			# self.EnvModeOption.append(GetObject("env_02"))
			# self.EnvModeOption.append(GetObject("env_03"))
			# self.EnvModeOption.append(GetObject("env_04"))
			# self.EnvModeOption.append(GetObject("env_05"))
			# self.EnvModeOption.append(GetObject("env_06"))
			# self.EnvModeOption.append(GetObject("env_07"))
			## End of Ambient

			## Category
			self.gameOptionButton.append(GetObject("category_game_option"))
			self.gameOptionButton.append(GetObject("category_graphics_option"))
			
			self.gameOptionBackground.append(GetObject("background_game"))
			self.gameOptionBackground.append(GetObject("background_graphics"))

			self.gameOptions.append(GetObject("char_opt_board"))
			self.gameOptions.append(GetObject("ui_opt_board"))
			# self.gameOptions.append(GetObject("ambient_opt_board"))

			self.gamecharButton.append(GetObject("character"))
			self.gamecharButton.append(GetObject("character1"))
			# self.gamecharButton.append(GetObject("character2"))

			self.graphicsButton.append(GetObject("display_settings_graphics"))
			self.graphicsButton.append(GetObject("advanced_settings_graphics"))
			self.graphicsBg.append(GetObject("display_settings_option_board"))
			self.graphicsBg.append(GetObject("advanced_option_board"))
			
			if app.ENABLE_DOG_MODE:
				self.dogModeStatusButtonList.append(GetObject("dog_mode_on"))
				self.dogModeStatusButtonList.append(GetObject("dog_mode_off"))

		except:
			import exception
			exception.Abort("OptionDialog.__Load_BindObject")

	def __Load(self):
		self.__Load_LoadScript("uiscript/gameoptiondialog.py")

		self.__Load_BindObject()

		self.SetCenterPosition()

		self.titleBar.SetCloseEvent(ui.__mem_func__(self.Close))

		## Character
		self.nameColorModeButtonList.SetToggleDownEvent(self.__OnClickNameColorModeEmpireButton)
		self.nameColorModeButtonList.SetToggleUpEvent(self.__OnClickNameColorModeNormalButton)

		self.pvpModeButtonDict[player.PK_MODE_PEACE].SAFE_SetEvent(self.__OnClickPvPModePeaceButton)
		self.pvpModeButtonDict[player.PK_MODE_REVENGE].SAFE_SetEvent(self.__OnClickPvPModeRevengeButton)
		self.pvpModeButtonDict[player.PK_MODE_GUILD].SAFE_SetEvent(self.__OnClickPvPModeGuildButton)
		self.pvpModeButtonDict[player.PK_MODE_FREE].SAFE_SetEvent(self.__OnClickPvPModeFreeButton)

		self.blockButtonList[0].SetToggleUpEvent(self.__OnClickBlockExchangeButton)
		self.blockButtonList[1].SetToggleUpEvent(self.__OnClickBlockPartyButton)
		self.blockButtonList[2].SetToggleUpEvent(self.__OnClickBlockGuildButton)
		self.blockButtonList[3].SetToggleUpEvent(self.__OnClickBlockWhisperButton)
		self.blockButtonList[4].SetToggleUpEvent(self.__OnClickBlockFriendButton)
		self.blockButtonList[5].SetToggleUpEvent(self.__OnClickBlockPartyRequest)

		self.blockButtonList[0].SetToggleDownEvent(self.__OnClickBlockExchangeButton)
		self.blockButtonList[1].SetToggleDownEvent(self.__OnClickBlockPartyButton)
		self.blockButtonList[2].SetToggleDownEvent(self.__OnClickBlockGuildButton)
		self.blockButtonList[3].SetToggleDownEvent(self.__OnClickBlockWhisperButton)
		self.blockButtonList[4].SetToggleDownEvent(self.__OnClickBlockFriendButton)
		self.blockButtonList[5].SetToggleDownEvent(self.__OnClickBlockPartyRequest)

		## End of Character

		## Graphics
		self.cameraModeButtonList[0].SetEvent(lambda arg=0: self.__SetCameraMode(arg))
		self.cameraModeButtonList[1].SetEvent(lambda arg=1: self.__SetCameraMode(arg))
		
		self.fogModeButtonList[0].SetEvent(lambda arg=0: self.__SetFogLevel(arg))
		self.fogModeButtonList[1].SetEvent(lambda arg=1: self.__SetFogLevel(arg))
		self.fogModeButtonList[2].SetEvent(lambda arg=2: self.__SetFogLevel(arg))

		self.tilingModeButtonList[0].SAFE_SetEvent(self.__OnClickTilingModeCPUButton)
		self.tilingModeButtonList[1].SAFE_SetEvent(self.__OnClickTilingModeGPUButton)
		
		self.targetMenuModeButtonList[0].SetEvent(lambda arg=0: self.__SetTargetMode(arg))
		self.targetMenuModeButtonList[1].SetEvent(lambda arg=1: self.__SetTargetMode(arg))
		
		self.chatLineModeButtonList[0].SetEvent(lambda arg=0: self.__SetChatMode(arg))
		self.chatLineModeButtonList[1].SetEvent(lambda arg=1: self.__SetChatMode(arg))
		
		self.damageModeButtonList[0].SetEvent(lambda arg=0: self.__SetDamageMode(arg))
		self.damageModeButtonList[1].SetEvent(lambda arg=1: self.__SetDamageMode(arg))

		self.shopNameButtonList[0].SetEvent(lambda arg=0: self.__SetSalesTextMode(arg))
		self.shopNameButtonList[1].SetEvent(lambda arg=1: self.__SetSalesTextMode(arg))
	
		self.noticeModeButtonList[0].SetEvent(lambda arg=0: self.__SetNoticeMode(arg))
		self.noticeModeButtonList[1].SetEvent(lambda arg=1: self.__SetNoticeMode(arg))
		
		self.showEffectsButtonList[0].SetEvent(lambda arg=0: self.__SetEffectMode(arg))
		self.showEffectsButtonList[1].SetEvent(lambda arg=1: self.__SetEffectMode(arg))
		
		self.missionsButtonList[0].SetEvent(lambda arg=0: self.__SetMissionMode(arg))
		self.missionsButtonList[1].SetEvent(lambda arg=1: self.__SetMissionMode(arg))
		
		self.affectButtonList[0].SetEvent(lambda arg=0: self.__SetAffectsMode(arg))
		self.affectButtonList[1].SetEvent(lambda arg=1: self.__SetAffectsMode(arg))
		
		self.animButtonList[0].SetEvent(lambda arg=0: self.__SetAnimMode(arg))
		self.animButtonList[1].SetEvent(lambda arg=1: self.__SetAnimMode(arg))
		
		# self.interfaceButtonList[0].SetEvent(lambda arg=0: self.__SetInterfaceMode(arg))
		# self.interfaceButtonList[1].SetEvent(lambda arg=1: self.__SetInterfaceMode(arg))
		
		self.nightButtonList[0].SetEvent(lambda arg=0: self.__SetNightMode(arg))
		self.nightButtonList[1].SetEvent(lambda arg=1: self.__SetNightMode(arg))

		## End of Graphics
		## UI
		self.alwaysShowNameButtonList.SetToggleUpEvent(self.__OnClickAlwaysShowNameOffButton)
		self.alwaysShowNameButtonList.SetToggleDownEvent(self.__OnClickAlwaysShowNameOnButton)

		self.fovSlider.SetSliderPos(float(systemSetting.GetFieldOfView() * 2))
		self.fovSlider.SetEvent(ui.__mem_func__(self.OnChangeFOV))
		
		self.scaleSlider.SetSliderPos(float(systemSetting.GetMetinScale()))
		self.scaleSlider.SetEvent(ui.__mem_func__(self.OnChangeScale))
		
		self.showNewHideButtonList[0].SetToggleUpEvent(self.__OnTogglePetButton)
		self.showNewHideButtonList[0].SetToggleDownEvent(self.__OnTogglePetButton)

		self.showNewHideButtonList[1].SetToggleUpEvent(self.__OnToggleMountButton)
		self.showNewHideButtonList[1].SetToggleDownEvent(self.__OnToggleMountButton)

		self.showNewHideButtonList[2].SetToggleUpEvent(self.__OnToggleShopButton)
		self.showNewHideButtonList[2].SetToggleDownEvent(self.__OnToggleShopButton)
		
		## End of UI
		if app.ENABLE_DOG_MODE:
			self.dogModeStatusButtonList[0].SAFE_SetEvent(self.__OnClickDogModeStatusButton, 1) # on
			self.dogModeStatusButtonList[1].SAFE_SetEvent(self.__OnClickDogModeStatusButton, 0) # off
		## Environment
		# self.EnvModeOption[0].SAFE_SetEvent(self.__OnClickChangeEnv, 0)
		# self.EnvModeOption[1].SAFE_SetEvent(self.__OnClickChangeEnv, 1)
		# self.EnvModeOption[2].SAFE_SetEvent(self.__OnClickChangeEnv, 2)
		# self.EnvModeOption[3].SAFE_SetEvent(self.__OnClickChangeEnv, 3)
		# self.EnvModeOption[4].SAFE_SetEvent(self.__OnClickChangeEnv, 4)
		# self.EnvModeOption[5].SAFE_SetEvent(self.__OnClickChangeEnv, 5)
		# self.EnvModeOption[6].SAFE_SetEvent(self.__OnClickChangeEnv, 6)
		## End of Environment
		
		## work
		self.gameOptionButton[0].SAFE_SetEvent(self.__SwitchGameOption)
		self.gameOptionButton[1].SAFE_SetEvent(self.__SwitchGraphicsOption)
		
		self.gameOptionButton[0].Down()
		self.gamecharButton[0].Down()
		
		self.gamecharButton[0].SAFE_SetEvent(self.__ShowCharOptions)
		self.gamecharButton[1].SAFE_SetEvent(self.__ShowUiOptions)
		# self.gamecharButton[2].SAFE_SetEvent(self.__ShowAmbientOptions)
		
		self.graphicsButton[0].SAFE_SetEvent(self.__ShowDisplaySettings)
		self.graphicsButton[1].SAFE_SetEvent(self.__ShowAdvancedSettings)
		
		self.gameOptions[0].Show()
		self.gameOptions[1].Hide()
		# self.gameOptions[2].Hide()
		
		self.graphicsBg[0].Hide()
		self.graphicsBg[1].Hide()
		
		self.gameOptionBackground[0].Show()
		self.gameOptionBackground[1].Hide()

		# self.__OnClickChangeEnv(int(self.ReadConfig("SKYBOX")))

		self.__SetCurTilingMode()

		self.__ClickRadioButton(self.fogModeButtonList, constInfo.GET_FOG_LEVEL_INDEX())
		self.__ClickRadioButton(self.cameraModeButtonList, constInfo.GET_CAMERA_MAX_DISTANCE_INDEX())
		self.__ClickRadioButton(self.shopNameButtonList, int(self.ReadConfig("SHOP_NAME")))
		self.__ClickRadioButton(self.damageModeButtonList, int(self.ReadConfig("SHOW_DAMAGE")))
		self.__ClickRadioButton(self.chatLineModeButtonList, int(self.ReadConfig("VIEW_CHAT")))
		self.__ClickRadioButton(self.noticeModeButtonList, int(self.ReadConfig("BIGBOARD")))
		self.__ClickRadioButton(self.targetMenuModeButtonList, int(self.ReadConfig("TARGET")))
		self.__ClickRadioButton(self.showEffectsButtonList, int(self.ReadConfig("EFFECTS")))
		self.__ClickRadioButton(self.missionsButtonList, int(self.ReadConfig("MISSIONS")))
		self.__ClickRadioButton(self.affectButtonList, int(self.ReadConfig("HIDDEN_AFFECTS")))
		self.__ClickRadioButton(self.animButtonList, int(self.ReadConfig("SHOW_ANIMATION")))
		# self.__ClickRadioButton(self.interfaceButtonList, int(self.ReadConfig("DEIMOS_INTERFACE")))
		self.__ClickRadioButton(self.nightButtonList, int(self.ReadConfig("NIGHT")))
		
		if app.ENABLE_DOG_MODE:
			self.__ClickRadioButton(self.dogModeStatusButtonList, systemSetting.IsDogModeStatus())
		self.__SetPeacePKMode()
		
	def __OnClickTilingModeCPUButton(self):
		self.__NotifyChatLine(localeInfo.SYSTEM_OPTION_CPU_TILING_1)
		self.__NotifyChatLine(localeInfo.SYSTEM_OPTION_CPU_TILING_2)
		self.__NotifyChatLine(localeInfo.SYSTEM_OPTION_CPU_TILING_3)
		self.__SetTilingMode(0)

	def __OnClickTilingModeGPUButton(self):
		self.__NotifyChatLine(localeInfo.SYSTEM_OPTION_GPU_TILING_1)
		self.__NotifyChatLine(localeInfo.SYSTEM_OPTION_GPU_TILING_2)
		self.__NotifyChatLine(localeInfo.SYSTEM_OPTION_GPU_TILING_3)
		self.__SetTilingMode(1)

	def __OnClickTilingApplyButton(self):
		self.__NotifyChatLine(localeInfo.SYSTEM_OPTION_TILING_EXIT)
		if 0==self.tilingMode:
			background.EnableSoftwareTiling(1)
		else:
			background.EnableSoftwareTiling(0)

		net.ExitGame()
		
	# CONFIG FILE
	def ReadConfig(self, opt):
		config = ""
		try:
			config = cfg.Get(cfg.SAVE_GENERAL, opt)
		except IOError:
			pass
		return config
		
	def SetConfig(self, opt, val):
		config_read = cfg.Set(cfg.SAVE_GENERAL, opt, val)

	def __ShowDisplaySettings(self):
		if self.graphicsBg[0].IsShow():
			return
		else:
			self.graphicsBg[1].Hide()
			self.graphicsBg[0].Show()
			
			self.UpdateGraphicsOpt()
	
	def __ShowAdvancedSettings(self):
		if self.graphicsBg[1].IsShow():
			return
		else:
			self.graphicsBg[0].Hide()
			self.graphicsBg[1].Show()
			self.UpdateGraphicsOpt()

	def __OnClickChangeEnv(self, index):
		self.index = index
		
		SKYBOX_LIST = {
			0: "d:/ymir work/environment/eveningsun_kf.msenv",
			1: "d:/ymir work/environment/eisrun_enviroment.msenv",
			2: "d:/ymir work/environment/rainyday_kf.msenv",
			3: "d:/ymir work/environment/skybox_reco_red_v1.msenv",
			4: "d:/ymir work/environment/skyboxridackhalloween.msenv",
			98: "d:/ymir work/environment/c1.msenv",
			99: constInfo.ENVIRONMENT_NIGHT,
		}
		
		background.RegisterEnvironmentData(index, SKYBOX_LIST[index])
		background.SetEnvironmentData(index)
		
		self.EnvModeOption[0].SetUp()
		self.EnvModeOption[1].SetUp()
		self.EnvModeOption[2].SetUp()
		self.EnvModeOption[3].SetUp()
		self.EnvModeOption[4].SetUp()
		self.EnvModeOption[5].SetUp()
		self.EnvModeOption[6].SetUp()
			
		self.EnvModeOption[int(self.index)].Down()
		self.SetConfig("SKYBOX", index)

	def	__ShowCharOptions(self):
		if self.gameOptions[0].IsShow():
			return
		else:
			self.gameOptions[1].Hide()
			# self.gameOptions[2].Hide()
			self.gameOptions[0].Show()
			self.UpdateGameOpt()
		
	def	__ShowUiOptions(self):
		self.gameOptions[0].Hide()
		# self.gameOptions[2].Hide()
		self.gameOptions[1].Show()
		self.UpdateGameOpt()

	# def	__ShowAmbientOptions(self):
		# self.gameOptions[0].Hide()
		
		# self.gameOptions[1].Hide()
		# self.gameOptions[2].Show()
		# self.UpdateGameOpt()

	def __SwitchGameOption(self):
		if self.gameOptionBackground[0].IsShow():
			return
		else:
			self.gameOptionBackground[1].Hide()
			self.gameOptionBackground[0].Show()
			
			self.UpdateOptionButton()
		

	def __SwitchGraphicsOption(self):
		if self.gameOptionBackground[1].IsShow():
			return
		else:
			self.gameOptionBackground[0].Hide()
			self.gameOptionBackground[1].Show()
			
			self.UpdateGraphicsOpt()
			self.UpdateOptionButton()
		
	def UpdateGraphicsOpt(self):
		if self.graphicsBg[0].IsShow():
			self.graphicsButton[0].Down()
			self.graphicsButton[1].SetUp()
		elif self.graphicsBg[1].IsShow():
			self.graphicsButton[0].SetUp()
			self.graphicsButton[1].Down()
		else:
			self.graphicsButton[0].Down()
			self.graphicsButton[1].SetUp()
			self.__ShowDisplaySettings()
		
	def UpdateGameOpt(self):
		if self.gameOptions[0].IsShow():
			self.gamecharButton[0].Down()
			self.gamecharButton[1].SetUp()
			# self.gamecharButton[2].SetUp()
		elif self.gameOptions[1].IsShow():
			self.gamecharButton[0].SetUp()
			self.gamecharButton[1].Down()
			# self.gamecharButton[2].SetUp()
		# elif self.gameOptions[2].IsShow():
			# self.gamecharButton[0].SetUp()
			# self.gamecharButton[1].SetUp()
			# self.gamecharButton[2].Down()
		else:
			self.gamecharButton[0].Down()
			self.gamecharButton[1].SetUp()
			# self.gamecharButton[2].SetUp()
		
	def UpdateOptionButton(self):
		if self.gameOptionBackground[0].IsShow():
			self.gameOptionButton[1].SetUp()
			self.gameOptionButton[0].Down()
			
		elif self.gameOptionBackground[1].IsShow():
			self.gameOptionButton[0].SetUp()
			self.gameOptionButton[1].Down()
			
		elif self.gameOptionBackground[2].IsShow():
			self.gameOptionButton[0].SetUp()
			self.gameOptionButton[1].SetUp()
		else:
			self.gameOptionButton[1].SetUp()
			self.gameOptionButton[0].Down()
		
	def __SetTilingMode(self, index):
		self.__ClickRadioButton(self.tilingModeButtonList, index)
		self.tilingMode=index

	def __SetCameraMode(self, index):
		constInfo.SET_CAMERA_MAX_DISTANCE_INDEX(index)
		self.__ClickRadioButton(self.cameraModeButtonList, index)

	def __SetFogLevel(self, index):
		constInfo.SET_FOG_LEVEL_INDEX(index)
		self.__ClickRadioButton(self.fogModeButtonList, index)

	def __ClickRadioButton(self, buttonList, buttonIndex):
		try:
			selButton=buttonList[buttonIndex]
		except IndexError:
			return

		for eachButton in buttonList:
			eachButton.SetUp()

		selButton.Down()

	def __OnClickNameColorModeNormalButton(self):
		constInfo.SET_CHRNAME_COLOR_INDEX(0)

	def __OnClickNameColorModeEmpireButton(self):
		constInfo.SET_CHRNAME_COLOR_INDEX(1)

	def __OnClickBlockExchangeButton(self):
		self.RefreshBlock()
		global blockMode
		net.SendChatPacket("/setblockmode " + str(blockMode ^ player.BLOCK_EXCHANGE))
	def __OnClickBlockPartyButton(self):
		self.RefreshBlock()
		global blockMode
		net.SendChatPacket("/setblockmode " + str(blockMode ^ player.BLOCK_PARTY))
	def __OnClickBlockGuildButton(self):
		self.RefreshBlock()
		global blockMode
		net.SendChatPacket("/setblockmode " + str(blockMode ^ player.BLOCK_GUILD))
	def __OnClickBlockWhisperButton(self):
		self.RefreshBlock()
		global blockMode
		net.SendChatPacket("/setblockmode " + str(blockMode ^ player.BLOCK_WHISPER))
	def __OnClickBlockFriendButton(self):
		self.RefreshBlock()
		global blockMode
		net.SendChatPacket("/setblockmode " + str(blockMode ^ player.BLOCK_FRIEND))
	def __OnClickBlockPartyRequest(self):
		self.RefreshBlock()
		global blockMode
		net.SendChatPacket("/setblockmode " + str(blockMode ^ player.BLOCK_PARTY_REQUEST))

	def __OnClickAlwaysShowNameOnButton(self):
		systemSetting.SetAlwaysShowNameFlag(1)
		self.RefreshAlwaysShowName()

	def __OnClickAlwaysShowNameOffButton(self):
		systemSetting.SetAlwaysShowNameFlag(2)
		self.RefreshAlwaysShowName()

	# def __OnClickAlwaysPartialNameOnButton(self):
		# systemSetting.SetAlwaysShowNameFlag(3)
		# self.RefreshAlwaysShowName()

	# def __OnClickAlwaysPartialNameOffButton(self):
		# systemSetting.SetAlwaysShowNameFlag(1)
		# self.RefreshAlwaysShowName()

	def __CheckPvPProtectedLevelPlayer(self):	
		if player.GetStatus(player.LEVEL)<constInfo.PVPMODE_PROTECTED_LEVEL:
			self.__SetPeacePKMode()
			chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.OPTION_PVPMODE_PROTECT % (constInfo.PVPMODE_PROTECTED_LEVEL))
			return 1

		return 0

	def __SetPKMode(self, mode):
		for btn in self.pvpModeButtonDict.values():
			btn.SetUp()
		if self.pvpModeButtonDict.has_key(mode):
			self.pvpModeButtonDict[mode].Down()

	def __SetPeacePKMode(self):
		self.__SetPKMode(player.PK_MODE_PEACE)

	def __RefreshPVPButtonList(self):
		self.__SetPKMode(player.GetPKMode())

	def __OnClickPvPModePeaceButton(self):
		if self.__CheckPvPProtectedLevelPlayer():
			return

		self.__RefreshPVPButtonList()

		if constInfo.PVPMODE_ENABLE:
			net.SendChatPacket("/pkmode 0", chat.CHAT_TYPE_TALKING)
		else:
			chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.OPTION_PVPMODE_NOT_SUPPORT)

	def __OnClickPvPModeRevengeButton(self):
		if self.__CheckPvPProtectedLevelPlayer():
			return

		self.__RefreshPVPButtonList()

		if constInfo.PVPMODE_ENABLE:
			net.SendChatPacket("/pkmode 1", chat.CHAT_TYPE_TALKING)
		else:
			chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.OPTION_PVPMODE_NOT_SUPPORT)

	def __OnClickPvPModeFreeButton(self):
		if self.__CheckPvPProtectedLevelPlayer():
			return

		self.__RefreshPVPButtonList()

		if constInfo.PVPMODE_ENABLE:
			net.SendChatPacket("/pkmode 2", chat.CHAT_TYPE_TALKING)
		else:
			chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.OPTION_PVPMODE_NOT_SUPPORT)

	def __OnClickPvPModeGuildButton(self):
		if self.__CheckPvPProtectedLevelPlayer():
			return

		self.__RefreshPVPButtonList()

		if 0 == player.GetGuildID():
			chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.OPTION_PVPMODE_CANNOT_SET_GUILD_MODE)
			return

		if constInfo.PVPMODE_ENABLE:
			net.SendChatPacket("/pkmode 4", chat.CHAT_TYPE_TALKING)
		else:
			chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.OPTION_PVPMODE_NOT_SUPPORT)

	def OnChangePKMode(self):
		self.__RefreshPVPButtonList()

	def OnCloseInputDialog(self):
		self.inputDialog.Close()
		self.inputDialog = None
		return TRUE

	def OnCloseQuestionDialog(self):
		self.questionDialog.Close()
		self.questionDialog = None
		return TRUE

	def OnPressEscapeKey(self):
		self.Close()
		return TRUE

	def RefreshBlock(self):
		global blockMode
		for i in xrange(len(self.blockButtonList)):
			if 0 != (blockMode & (1 << i)):
				self.blockButtonList[i].Down()
			else:
				self.blockButtonList[i].SetUp()

	def RefreshAlwaysShowName(self):
		if systemSetting.IsAlwaysShowName():
			self.alwaysShowNameButtonList.Down()
		else:
			self.alwaysShowNameButtonList.SetUp()

	# def RefreshAlwaysShowName(self):
		# x = systemSetting.IsAlwaysShowName()
		# if x == 1:
			# self.alwaysShowNameButtonList.Down()
			# self.alwaysShowNameButtonPartialList.SetUp()
		# elif x == 2:
			# self.alwaysShowNameButtonList.SetUp()
			# self.alwaysShowNameButtonPartialList.SetUp()
		# elif x == 3:
			# textTail.HideAllTextTail()
			# textTail.ShowAllTextTail()
			# self.alwaysShowNameButtonList.SetUp()
			# self.alwaysShowNameButtonPartialList.Down()

	def OnBlockMode(self, mode):
		global blockMode
		blockMode = mode
		self.RefreshBlock()

	def Show(self):
		self.RefreshBlock()
		ui.ScriptWindow.Show(self)

	def __SetCurTilingMode(self):
		if background.IsSoftwareTiling():
			self.__SetTilingMode(0)
		else:
			self.__SetTilingMode(1)	

	def Close(self):
		self.Hide()

	# def IsActiveModeGraphic(self):
		# idx = open("enbconvertor.ini", "r").readlines()

		# if int(idx[1][-2]) > 0:
			# return TRUE

		# return FALSE

	# def __ClickSystemModeButton(self):
		# import dbg, os, app, localeInfo

		# if self.IsActiveModeGraphic():
			# dam = 0
		# else:
			# dam = 1

		# idxCurMode = "EnableProxyLibrary=%d" % (dam)
		# f = []
		# getLine = 2

		# if os.path.exists("enbconvertor.ini"):
			# idx = open("enbconvertor.ini", "r")

			# for it in idx:
				# f.append(it)
			# idx.close()

		# while len(f) < int(getLine):
			# f.append("")

		# f[int(getLine)-1] = str(idxCurMode)
		# idx = open("enbconvertor.ini", "w")

		# for it in f:
			# idx.write(it)
			# if (len(it) > 0 and it[-1:] != "\n") or len(it) == 0:
				# idx.write("\n")

		# idx.close()
		# self.Close()

		# if dam > 0:
			# dbg.LogBox(localeInfo.GRAPHIC_MODE_ENABLE)
		# else:
			# dbg.LogBox(localeInfo.GRAPHIC_MODE_DISABLE)

		# dbg.LogBox(localeInfo.GRAPHIC_MODE_RESTART)
		# os.system('start Aries2.exe') ### Change with your name of application.
		# app.Exit()
		
	def __SetSalesTextMode(self, index):
		systemSetting.SetShowSalesTextFlag(index)
		uiPrivateShopBuilder.UpdateADBoard(index)
		self.__ClickRadioButton(self.shopNameButtonList, index)
		self.SetConfig("SHOP_NAME", index)

	def __SetDamageMode(self, index):
		if index == 0:
			systemSetting.SetShowDamageFlag(True)
		else:
			systemSetting.SetShowDamageFlag(False)
		
		self.__ClickRadioButton(self.damageModeButtonList, index)
		self.SetConfig("SHOW_DAMAGE", index)

	def __SetEffectMode(self, index):
		if index == 0:
			systemSetting.SetHideEffectsFlag(systemSetting.HIDE_EFFECTS, True)
		else:
			systemSetting.SetHideEffectsFlag(systemSetting.HIDE_EFFECTS, False)

		self.__ClickRadioButton(self.showEffectsButtonList, index)
		self.SetConfig("EFFECTS", index)
		self.__NotifyChatLine(localeInfo.RELOG_OPTION)

	def __SetMissionMode(self, index):
		constInfo.CLICK_MISSIONS = 1
		constInfo.SET_MISSIONS = index
		self.__ClickRadioButton(self.missionsButtonList, index)
		self.SetConfig("MISSIONS", index)

	def __SetAffectsMode(self, index):
		if index == 1:
			systemSetting.SetPremiumAffect(True)
		else:
			systemSetting.SetPremiumAffect(False)

		self.__ClickRadioButton(self.affectButtonList, index)
		self.SetConfig("HIDDEN_AFFECTS", index)

	def __SetAnimMode(self, index):
		self.__ClickRadioButton(self.animButtonList, index)
		self.SetConfig("SHOW_ANIMATION", index)
		self.__NotifyChatLine(localeInfo.RELOG_OPTION)

	# def __SetInterfaceMode(self, index):
		# self.__ClickRadioButton(self.interfaceButtonList, index)
		# self.SetConfig("DEIMOS_INTERFACE", index)
		# self.__NotifyChatLine(localeInfo.RELOG_OPTION)

	def __SetNightMode(self, index):
		if index == 1:
			background.RegisterEnvironmentData(1, constInfo.ENVIRONMENT_NIGHT)
			background.SetEnvironmentData(1)
			constInfo.Night = 1
		else:
			background.SetEnvironmentData(0)
			constInfo.Night = 0
	
		self.__ClickRadioButton(self.nightButtonList, index)
		self.SetConfig("NIGHT", index)
		# self.__NotifyChatLine(localeInfo.RELOG_OPTION)

	def __SetChatMode(self, index):
		systemSetting.SetViewChatFlag(index)
		self.__ClickRadioButton(self.chatLineModeButtonList, index)
		self.SetConfig("VIEW_CHAT", index)
		
	def __SetNoticeMode(self, index):
		if index == 0:
			app.SetVisibleNotice(True)
		else:
			app.SetVisibleNotice(False)

		self.__ClickRadioButton(self.noticeModeButtonList, index)
		self.SetConfig("BIGBOARD", index)

	def __SetTargetMode(self, index):
		constInfo.SET_VIEW_OTHER_EMPIRE_PLAYER_TARGET_BOARD(index)
		self.__ClickRadioButton(self.targetMenuModeButtonList, index)
		self.SetConfig("TARGET", index)
		
	def __NotifyChatLine(self, text):
		chat.AppendChat(chat.CHAT_TYPE_INFO, text)
		
	def OnChangeFOV(self):
		pos = self.fovSlider.GetSliderPos() / 2
		systemSetting.SetFieldOfView(pos)

	def OnChangeScale(self):
		pos = self.scaleSlider.GetSliderPos()
		systemSetting.SetMetinScale(pos)
		
	def __OnTogglePetButton(self):
		if systemSetting.IsHidePets():
			systemSetting.SetHidePets(0)
		else:
			systemSetting.SetHidePets(1)
			
		self.RefreshNewHides()

	def __OnToggleMountButton(self):
		if systemSetting.IsHideMounts():
			systemSetting.SetHideMounts(0)
		else:
			systemSetting.SetHideMounts(1)
			
		self.RefreshNewHides()

	def __OnToggleShopButton(self):
		if systemSetting.IsHideShops():
			systemSetting.SetHideShops(0)
		else:
			systemSetting.SetHideShops(1)
			
		self.RefreshNewHides()

	def __OnToggleSalesButton(self):
		if systemSetting.IsShowSalesText():
			systemSetting.SetShowSalesTextFlag(0)
			uiPrivateShopBuilder.UpdateADBoard(0)
		else:
			systemSetting.SetShowSalesTextFlag(1)
			uiPrivateShopBuilder.UpdateADBoard(1)
			
		self.RefreshNewHides()

	def RefreshNewHides(self):
		DICT_HIDES = [systemSetting.IsHidePets(), systemSetting.IsHideMounts(), systemSetting.IsHideShops()]

		for index in xrange(len(DICT_HIDES)):
			if DICT_HIDES[index] == 1:
				self.showNewHideButtonList[index].Down()
			else:
				self.showNewHideButtonList[index].SetUp()
				
	if app.ENABLE_DOG_MODE:
		def __OnClickDogModeStatusButton(self, flag):
			self.__ClickRadioButton(self.dogModeStatusButtonList, flag)
			systemSetting.SetDogModeStatusFlag(flag)

			chrmgr.ClearRaceNameCache()
			playerSettingModule.ReloadNPC()
			systemSetting.ReloadInstance(flag)
			# chat.AppendChat(1, "flag is %s" % flag)
			self.RefreshDogModeStatus()

		def RefreshDogModeStatus(self):
			if systemSetting.IsDogModeStatus():
				self.dogModeStatusButtonList[1].SetUp()
				self.dogModeStatusButtonList[0].Down()
			else:
				self.dogModeStatusButtonList[1].Down()
				self.dogModeStatusButtonList[0].SetUp()