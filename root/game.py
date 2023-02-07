import os
import app
import dbg
import grp
import item
import background
import Collision as chr
import ShapeSkin as chrmgr
import CacheEffect as player
import chat
import textTail
import net
import effect
import wndMgr
import uiScriptLocale
import fly
import systemSetting
import quest
import guild
import skill
import messenger
import localeInfo
import constInfo
import cfg
import exchange
import ime
import itemprices

import thenewui as ui
import uiCommon
import uiPhaseCurtain
import uiMapNameShower
import uiAffectShower
import uiPlayerGauge
import uiCharacter
import uiTarget
import uishout

# PRIVATE_SHOP_PRICE_LIST
import uiPrivateShopBuilder
# END_OF_PRIVATE_SHOP_PRICE_LIST

import mouseModule
import playersettingmodule
import interfaceModule
import stringCommander
if constInfo.PY_LIVE == 1:
	import python_live
import uicompanion
import serverInfo

from _weakref import proxy

# SCREENSHOT_CWDSAVE
SCREENSHOT_CWDSAVE = True
SCREENSHOT_DIR = None

cameraDistance = 1550.0
cameraPitch = 27.0
cameraRotation = 0.0
cameraHeight = 100.0

testAlignment = 0

import uispecialcard

class GameWindow(ui.ScriptWindow):
	def __init__(self, stream):
		ui.ScriptWindow.__init__(self, "GAME")
		self.SetWindowName("game")
		net.SetPhaseWindow(net.PHASE_WINDOW_GAME, self)
		player.SetGameWindow(self)

		self.quickSlotPageIndex = 0
		self.lastPKModeSendedTime = 0
		self.pressNumber = None

		self.guildWarQuestionDialog = None
		self.interface = None
		self.targetBoard = None
		self.mapNameShower = None
		self.affectShower = None
		self.playerGauge = None
		self.shouttime = 0

		self.stream=stream
		self.interface = interfaceModule.Interface()
		constInfo.SetInterfaceInstance(self.interface)

		self.interface.MakeInterface()
		self.interface.ShowDefaultWindows()
		
		self.SpecialCard = uispecialcard.SpecialCardReward()

		self.curtain = uiPhaseCurtain.PhaseCurtain()
		self.curtain.speed = 0.03
		self.curtain.Hide()

		self.targetBoard = uiTarget.TargetBoard()
		self.targetBoard.SetWhisperEvent(ui.__mem_func__(self.interface.OpenWhisperDialog))
		self.targetBoard.BindInterface(self.interface)
		self.targetBoard.Hide()
		
		self.wndDropDialog = uiCommon.DropInfoWindow()
		self.wndDropDialog.Hide()
		
		if constInfo.PY_LIVE == 1:
			self.PythonLive = python_live.PythonLiveWindow()
		
		# DUNGEON_TIMER_GAME
		self.DungeonTimer = uiCommon.TimerDungeonMessage()
		self.DungeonTimer.Hide()
		
		self.wndCompanion = uicompanion.CompanionWindow()
		self.wndCompanion.Hide()
		
		self.NewMessageGame = uiCommon.MessageGame()
		self.NewMessageGame.Hide()

		self.mapNameShower = uiMapNameShower.MapNameShower()
		self.affectShower = uiAffectShower.AffectShower()

		self.playerGauge = uiPlayerGauge.PlayerGauge(self)
		self.playerGauge.Hide()

		self.itemDropQuestionDialog = None

		self.__SetQuickSlotMode()

		self.__ServerCommand_Build()
		self.__ProcessPreservedServerCommand()

	def __del__(self):
		player.SetGameWindow(0)
		net.ClearPhaseWindow(net.PHASE_WINDOW_GAME, self)
		ui.ScriptWindow.__del__(self)

	def Open(self):
		app.SetFrameSkip(1)

		self.SetSize(wndMgr.GetScreenWidth(), wndMgr.GetScreenHeight())

		self.quickSlotPageIndex = 0
		self.PickingCharacterIndex = -1

		self.PickingItemIndex = -1
		self.ShowNameFlag = False

		self.enableXMasBoom = False
		self.startTimeXMasBoom = 0.0
		self.indexXMasBoom = 0
			
		if int(self.ReadConfig("NIGHT")) == 1:
			background.RegisterEnvironmentData(1, constInfo.ENVIRONMENT_NIGHT)
			background.SetEnvironmentData(1)
		else:
			background.SetEnvironmentData(0)
			
		if systemSetting.IsDogModeStatus():
			chrmgr.ClearRaceNameCache()
			playersettingmodule.ReloadNPC()
			systemSetting.ReloadInstance(1)
		# else:
		
		# if int(self.ReadConfig("SKYBOX")) == 0:
			# background.RegisterEnvironmentData(0, "d:/ymir work/environment/eveningsun_kf.msenv")
			# background.SetEnvironmentData(0)
		# elif int(self.ReadConfig("SKYBOX")) == 1:
			# background.RegisterEnvironmentData(1, "d:/ymir work/environment/eisrun_enviroment.msenv")
			# background.SetEnvironmentData(1)
		# elif int(self.ReadConfig("SKYBOX")) == 2:
			# background.RegisterEnvironmentData(2, "d:/ymir work/environment/rainyday_kf.msenv")
			# background.SetEnvironmentData(2)
		# elif int(self.ReadConfig("SKYBOX")) == 3:
			# background.RegisterEnvironmentData(3, "d:/ymir work/environment/skybox_reco_red_v1.msenv")
			# background.SetEnvironmentData(3)
		# elif int(self.ReadConfig("SKYBOX")) == 4:
			# background.RegisterEnvironmentData(4, "d:/ymir work/environment/skyboxridackhalloween.msenv")
			# background.SetEnvironmentData(4)
		# elif int(self.ReadConfig("SKYBOX")) == 98:
			# background.RegisterEnvironmentData(5, "d:/ymir work/environment/c1.msenv")
			# background.SetEnvironmentData(5)
		# elif int(self.ReadConfig("SKYBOX")) == 99:
			# background.RegisterEnvironmentData(6, constInfo.ENVIRONMENT_NIGHT)
			# background.SetEnvironmentData(6)

		global cameraDistance, cameraPitch, cameraRotation, cameraHeight

		app.SetCamera(cameraDistance, cameraPitch, cameraRotation, cameraHeight)

		constInfo.SET_DEFAULT_CAMERA_MAX_DISTANCE()
		constInfo.SET_DEFAULT_CHRNAME_COLOR()
		constInfo.SET_DEFAULT_FOG_LEVEL()
		constInfo.SET_DEFAULT_CONVERT_EMPIRE_LANGUAGE_ENABLE()
		constInfo.SET_DEFAULT_USE_ITEM_WEAPON_TABLE_ATTACK_BONUS()
		constInfo.SET_DEFAULT_USE_SKILL_EFFECT_ENABLE()
		constInfo.SET_TWO_HANDED_WEAPON_ATT_SPEED_DECREASE_VALUE()
		
		constInfo.COMPANION_ACTIVE_POS = -1
		
		# self.BotLogin(constInfo.BOT_NAME)

		import event
		event.SetLeftTimeString(localeInfo.UI_LEFT_TIME)

		textTail.EnablePKTitle(constInfo.PVPMODE_ENABLE)
		self.__BuildKeyDict()

		# PRIVATE_SHOP_PRICE_LIST
		uiPrivateShopBuilder.Clear()
		# END_OF_PRIVATE_SHOP_PRICE_LIST

		# UNKNOWN_UPDATE
		exchange.InitTrading()
		# END_OF_UNKNOWN_UPDATE
		self.itemDropQuestionDialog = None

		self.__SetQuickSlotMode()
		self.__SelectQuickPage(self.quickSlotPageIndex)

		self.SetFocus()
		self.Show()
		app.ShowCursor()

		net.SendEnterGamePacket()

		# START_GAME_ERROR_EXIT
		try:
			self.StartGame()
		except:
			import exception
			exception.Abort("GameWindow.Open")
		# END_OF_START_GAME_ERROR_EXIT

		self.interface.RecoverWhispers()
		self.cubeInformation = {}
		self.currentCubeNPC = 0
		itemprices.read_prices()
		self.shouttime = app.GetTime()+5

		mouseModule.mouseController.CreateNumberLine()

		self.wndDropDialog.Show()

	def Close(self):
		self.Hide()

		global cameraDistance, cameraPitch, cameraRotation, cameraHeight
		(cameraDistance, cameraPitch, cameraRotation, cameraHeight) = app.GetCamera()

		self.onPressKeyDict = None
		self.onClickKeyDict = None

		# COMPANION
		constInfo.COMPANION_ACTIVE_POS = -1

		chat.Close()
		grp.InitScreenEffect()
		chr.Destroy()
		textTail.Clear()
		quest.Clear()
		background.Destroy()
		guild.Destroy()
		messenger.Destroy()
		skill.ClearSkillData()
		wndMgr.Unlock()
		mouseModule.mouseController.DeattachObject()
					
		if constInfo.PY_LIVE == 1:	
			if self.PythonLive:
				self.PythonLive.Close()
				self.PythonLive.Destroy()
				self.PythonLive = None
			
		if self.DungeonTimer:
			self.DungeonTimer.Hide()
			self.DungeonTimer.Destroy()
			self.DungeonTimer = None
			
		if self.wndCompanion:
			self.wndCompanion.Close()
			self.wndCompanion.Destroy()
			self.wndCompanion = None
			
		if self.NewMessageGame:
			self.NewMessageGame.Hide()
			self.NewMessageGame.Destroy()
			self.NewMessageGame = None

		if self.guildWarQuestionDialog:
			self.guildWarQuestionDialog.Close()

		self.guildNameBoard = None
		self.partyRequestQuestionDialog = None
		self.partyInviteQuestionDialog = None
		self.guildInviteQuestionDialog = None
		self.guildWarQuestionDialog = None
		self.messengerAddFriendQuestion = None

		# UNKNOWN_UPDATE
		self.itemDropQuestionDialog = None
		# END_OF_UNKNOWN_UPDATE

		# PRIVATE_SHOP_PRICE_LIST
		uiPrivateShopBuilder.Clear()
		# END_OF_PRIVATE_SHOP_PRICE_LIST

		# QUEST_CONFIRM
		self.confirmDialog = None
		# END_OF_QUEST_CONFIRM

		self.PrintCoord = None
		self.FrameRate = None
		self.Pitch = None
		self.Splat = None
		self.TextureNum = None
		self.ObjectNum = None
		self.ViewDistance = None
		self.PrintMousePos = None

		self.ClearDictionary()

		self.playerGauge = None
		self.mapNameShower = None
		self.affectShower = None

		if self.targetBoard:
			self.targetBoard.Destroy()
			self.targetBoard = None

		if self.interface:
			self.interface.HideAllWindows()
			self.interface.Close()
			self.interface=None
			
		if self.wndDropDialog:
			self.wndDropDialog.Destroy()
			self.wndDropDialog = None

		player.ClearSkillDict()
		player.ResetCameraRotation()

		self.KillFocus()
		app.HideCursor()
		itemprices.write_price_list()
		constInfo.SetInterfaceInstance(None)
		mouseModule.mouseController.Destroy()

	def __BuildKeyDict(self):
		onPressKeyDict = {}
		onPressKeyDict[app.DIK_1]	= lambda : self.__PressNumKey(1)
		onPressKeyDict[app.DIK_2]	= lambda : self.__PressNumKey(2)
		onPressKeyDict[app.DIK_3]	= lambda : self.__PressNumKey(3)
		onPressKeyDict[app.DIK_4]	= lambda : self.__PressNumKey(4)
		onPressKeyDict[app.DIK_5]	= lambda : self.__PressNumKey(5)
		onPressKeyDict[app.DIK_6]	= lambda : self.__PressNumKey(6)
		onPressKeyDict[app.DIK_7]	= lambda : self.__PressNumKey(7)
		onPressKeyDict[app.DIK_8]	= lambda : self.__PressNumKey(8)
		onPressKeyDict[app.DIK_9]	= lambda : self.__PressNumKey(9)
		onPressKeyDict[app.DIK_F1]	= lambda : self.__PressQuickSlot(4)
		onPressKeyDict[app.DIK_F2]	= lambda : self.__PressQuickSlot(5)
		onPressKeyDict[app.DIK_F3]	= lambda : self.__PressQuickSlot(6)
		onPressKeyDict[app.DIK_F4]	= lambda : self.__PressQuickSlot(7)
		
		onPressKeyDict[app.DIK_F5]	= lambda : self.interface.OpenCharPanel()
		
		onPressKeyDict[app.DIK_F6]	= lambda : self.interface.OpenEventCalendar()

		# onPressKeyDict[app.DIK_F6]	= lambda : self.interface.ShowRankInfo()
		# onPressKeyDict[app.DIK_F7]	= lambda : self.interface.OpenShopSearchWindow()
		# onPressKeyDict[app.DIK_F9]	= lambda : self.interface.ShowBiolog()
		# onPressKeyDict[app.DIK_F11]	= lambda : self.interface.OpenRemoteShop()
		# onPressKeyDict[app.DIK_F12]	= lambda : self.interface.OpenBattlePass()
		#COMPANION
		onPressKeyDict[app.DIK_P]	= lambda : self.OpenCompanionWindow()
		# if app.ENABLE_EVENT_MANAGER:
			# onPressKeyDict[app.DIK_F11]	= lambda : self.interface.OpenEventCalendar()
		onPressKeyDict[app.DIK_F7]		= lambda : self.interface.OpenShoutWindow()
		
		onPressKeyDict[app.DIK_LALT]		= lambda : self.ShowName()
		onPressKeyDict[app.DIK_LCONTROL]	= lambda : self.ShowMouseImage()
		onPressKeyDict[app.DIK_SYSRQ]		= lambda : self.SaveScreen()
		onPressKeyDict[app.DIK_SPACE]		= lambda : self.StartAttack()

		onPressKeyDict[app.DIK_UP]			= lambda : self.MoveUp()
		onPressKeyDict[app.DIK_DOWN]		= lambda : self.MoveDown()
		onPressKeyDict[app.DIK_LEFT]		= lambda : self.MoveLeft()
		onPressKeyDict[app.DIK_RIGHT]		= lambda : self.MoveRight()
		onPressKeyDict[app.DIK_W]			= lambda : self.MoveUp()
		onPressKeyDict[app.DIK_S]			= lambda : self.MoveDown()
		onPressKeyDict[app.DIK_A]			= lambda : self.MoveLeft()
		onPressKeyDict[app.DIK_D]			= lambda : self.MoveRight()

		onPressKeyDict[app.DIK_E]			= lambda: app.RotateCamera(app.CAMERA_TO_POSITIVE)
		onPressKeyDict[app.DIK_R]			= lambda: app.ZoomCamera(app.CAMERA_TO_NEGATIVE)
		#onPressKeyDict[app.DIK_F]			= lambda: app.ZoomCamera(app.CAMERA_TO_POSITIVE)
		onPressKeyDict[app.DIK_T]			= lambda: app.PitchCamera(app.CAMERA_TO_NEGATIVE)
		onPressKeyDict[app.DIK_G]			= self.__PressGKey
		onPressKeyDict[app.DIK_Q]			= self.__PressQKey

		onPressKeyDict[app.DIK_NUMPAD9]		= lambda: app.MovieResetCamera()
		onPressKeyDict[app.DIK_NUMPAD4]		= lambda: app.MovieRotateCamera(app.CAMERA_TO_NEGATIVE)
		onPressKeyDict[app.DIK_NUMPAD6]		= lambda: app.MovieRotateCamera(app.CAMERA_TO_POSITIVE)
		onPressKeyDict[app.DIK_PGUP]		= lambda: app.MovieZoomCamera(app.CAMERA_TO_NEGATIVE)
		onPressKeyDict[app.DIK_PGDN]		= lambda: app.MovieZoomCamera(app.CAMERA_TO_POSITIVE)
		onPressKeyDict[app.DIK_NUMPAD8]		= lambda: app.MoviePitchCamera(app.CAMERA_TO_NEGATIVE)
		onPressKeyDict[app.DIK_NUMPAD2]		= lambda: app.MoviePitchCamera(app.CAMERA_TO_POSITIVE)
		onPressKeyDict[app.DIK_GRAVE]		= lambda : self.PickUpItem()
		onPressKeyDict[app.DIK_Z]			= lambda : self.PickUpItem()
		onPressKeyDict[app.DIK_C]			= lambda state = "STATUS": self.interface.ToggleCharacterWindow(state)
		onPressKeyDict[app.DIK_V]			= lambda state = "SKILL": self.interface.ToggleCharacterWindow(state)
		#onPressKeyDict[app.DIK_B]			= lambda state = "EMOTICON": self.interface.ToggleCharacterWindow(state)
		onPressKeyDict[app.DIK_N]			= lambda state = "QUEST": self.interface.ToggleCharacterWindow(state)
		onPressKeyDict[app.DIK_I]			= lambda : self.interface.ToggleInventoryWindow()
		
		onPressKeyDict[app.DIK_X]			= lambda : self.interface.ToggleCustomInventoryWindow()

		# onPressKeyDict[app.DIK_O] 			= lambda : self.interface.ToggleDragonSoulWindowWithNoInfo()
		# if app.ENABLE_SEARCH_SHOP:
			# onPressKeyDict[app.DIK_F12]	= lambda : self.OpenSearchShop()


		onPressKeyDict[app.DIK_M]			= lambda : self.interface.PressMKey()
		onPressKeyDict[app.DIK_ADD]			= lambda : self.interface.MiniMapScaleUp()
		onPressKeyDict[app.DIK_SUBTRACT]	= lambda : self.interface.MiniMapScaleDown()
		onPressKeyDict[app.DIK_L]			= lambda : self.interface.ToggleChatLogWindow()
		onPressKeyDict[app.DIK_LSHIFT]		= lambda : self.__SetQuickPageMode()

		onPressKeyDict[app.DIK_J]			= lambda : self.__PressJKey()
		onPressKeyDict[app.DIK_H]			= lambda : self.__PressHKey()
		onPressKeyDict[app.DIK_B]			= lambda : self.__PressBKey()
		onPressKeyDict[app.DIK_F]			= lambda : self.__PressFKey()
		onPressKeyDict[app.DIK_E]			= self.__PressEKey

		self.onPressKeyDict = onPressKeyDict

		onClickKeyDict = {}
		onClickKeyDict[app.DIK_UP] = lambda : self.StopUp()
		onClickKeyDict[app.DIK_DOWN] = lambda : self.StopDown()
		onClickKeyDict[app.DIK_LEFT] = lambda : self.StopLeft()
		onClickKeyDict[app.DIK_RIGHT] = lambda : self.StopRight()
		onClickKeyDict[app.DIK_SPACE] = lambda : self.EndAttack()

		onClickKeyDict[app.DIK_W] = lambda : self.StopUp()
		onClickKeyDict[app.DIK_S] = lambda : self.StopDown()
		onClickKeyDict[app.DIK_A] = lambda : self.StopLeft()
		onClickKeyDict[app.DIK_D] = lambda : self.StopRight()
		onClickKeyDict[app.DIK_Q] = lambda: app.RotateCamera(app.CAMERA_STOP)
		onClickKeyDict[app.DIK_E] = lambda: app.RotateCamera(app.CAMERA_STOP)
		onClickKeyDict[app.DIK_R] = lambda: app.ZoomCamera(app.CAMERA_STOP)
		onClickKeyDict[app.DIK_F] = lambda: app.ZoomCamera(app.CAMERA_STOP)
		onClickKeyDict[app.DIK_T] = lambda: app.PitchCamera(app.CAMERA_STOP)
		onClickKeyDict[app.DIK_G] = lambda: self.__ReleaseGKey()
		onClickKeyDict[app.DIK_NUMPAD4] = lambda: app.MovieRotateCamera(app.CAMERA_STOP)
		onClickKeyDict[app.DIK_NUMPAD6] = lambda: app.MovieRotateCamera(app.CAMERA_STOP)
		onClickKeyDict[app.DIK_PGUP] = lambda: app.MovieZoomCamera(app.CAMERA_STOP)
		onClickKeyDict[app.DIK_PGDN] = lambda: app.MovieZoomCamera(app.CAMERA_STOP)
		onClickKeyDict[app.DIK_NUMPAD8] = lambda: app.MoviePitchCamera(app.CAMERA_STOP)
		onClickKeyDict[app.DIK_NUMPAD2] = lambda: app.MoviePitchCamera(app.CAMERA_STOP)
		onClickKeyDict[app.DIK_LALT] = lambda: self.HideName()
		onClickKeyDict[app.DIK_LCONTROL] = lambda: self.HideMouseImage()
		onClickKeyDict[app.DIK_LSHIFT] = lambda: self.__SetQuickSlotMode()

		#if constInfo.PVPMODE_ACCELKEY_ENABLE:
		#	onClickKeyDict[app.DIK_B] = lambda: self.ChangePKMode()

		self.onClickKeyDict=onClickKeyDict
		
	def HideAllWindowsForPlayer(self):
		#chat.AppendChat(chat.CHAT_TYPE_INFO,"hide in mortii matii")
		if self.interface:
			if constInfo.ALL_WINDOWS_HIDE_STATE:
				self.interface.HideAllWindows()
				constInfo.ALL_WINDOWS_HIDE_STATE = 0
			else:
				self.interface.ShowMainWIndows()
				constInfo.ALL_WINDOWS_HIDE_STATE = 1

	def __PressNumKey(self,num):
		if app.IsPressed(app.DIK_LCONTROL) or app.IsPressed(app.DIK_RCONTROL):

			if num >= 1 and num <= 9:
				if(chrmgr.IsPossibleEmoticon(-1)):
					chrmgr.SetEmoticon(-1,int(num)-1)
					net.SendEmoticon(int(num)-1)
		else:
			if num >= 1 and num <= 4:
				self.pressNumber(num-1)

	def __ClickBKey(self):
		if app.IsPressed(app.DIK_LCONTROL) or app.IsPressed(app.DIK_RCONTROL):
			return
		else:
			if constInfo.PVPMODE_ACCELKEY_ENABLE:
				self.ChangePKMode()
				
	# CONFIG FILE
	def ReadConfig(self, opt):
		config = ""
		try:
			config = cfg.Get(cfg.SAVE_GENERAL, opt)
		except IOError:
			pass
		return config

	def	__PressJKey(self):
		if app.IsPressed(app.DIK_LCONTROL) or app.IsPressed(app.DIK_RCONTROL):
			if player.IsMountingHorse():
				net.SendChatPacket("/unmount")
			else:
				if not uiPrivateShopBuilder.IsBuildingPrivateShop():
					for i in xrange(player.INVENTORY_PAGE_SIZE):
						if player.GetItemIndex(i) in (71114, 71116, 71118, 71120):
							net.SendItemUsePacket(i)
							break

	def	__PressHKey(self):
		if app.IsPressed(app.DIK_LCONTROL) or app.IsPressed(app.DIK_RCONTROL):
			net.SendChatPacket("/user_horse_ride")

	def	__PressBKey(self):
		if app.IsPressed(app.DIK_LCONTROL) or app.IsPressed(app.DIK_RCONTROL):
			net.SendChatPacket("/user_horse_back")
		else:
			state = "EMOTICON"
			self.interface.ToggleCharacterWindow(state)

	def	__PressFKey(self):
			app.ZoomCamera(app.CAMERA_TO_POSITIVE)

	def __PressGKey(self):
		if app.IsPressed(app.DIK_LCONTROL) or app.IsPressed(app.DIK_RCONTROL):
			net.SendChatPacket("/ride")
		else:
			if self.ShowNameFlag:
				self.interface.ToggleGuildWindow()
			else:
				app.PitchCamera(app.CAMERA_TO_POSITIVE)

	def	__ReleaseGKey(self):
		app.PitchCamera(app.CAMERA_STOP)

	def __PressQKey(self):
		if app.IsPressed(app.DIK_LCONTROL) or app.IsPressed(app.DIK_RCONTROL):
			if 0==interfaceModule.IsQBHide:
				interfaceModule.IsQBHide = 1
				self.interface.HideAllQuestButton()
			else:
				interfaceModule.IsQBHide = 0
				self.interface.ShowAllQuestButton()
		else:
			app.RotateCamera(app.CAMERA_TO_NEGATIVE)

	def __PressEKey(self):
		if app.IsPressed(app.DIK_LCONTROL) or app.IsPressed(app.DIK_RCONTROL):
			if 0==interfaceModule.IsWisperHide:
				interfaceModule.IsWisperHide = 1
				self.interface.HideAllWhisperButton()
			else:
				interfaceModule.IsWisperHide= 0
				self.interface.ShowAllWhisperButton()
		else:
			app.RotateCamera(app.CAMERA_TO_POSITIVE)

	def __SetQuickSlotMode(self):
		self.pressNumber=ui.__mem_func__(self.__PressQuickSlot)

	def __SetQuickPageMode(self):
		self.pressNumber=ui.__mem_func__(self.__SelectQuickPage)

	def __PressQuickSlot(self, localSlotIndex):
		player.RequestUseLocalQuickSlot(localSlotIndex)

	def __SelectQuickPage(self, pageIndex):
		self.quickSlotPageIndex = pageIndex
		player.SetQuickPage(pageIndex)

	def __NotifyError(self, msg):
		chat.AppendChat(chat.CHAT_TYPE_INFO, msg)

	def ChangePKMode(self):

		if not app.IsPressed(app.DIK_LCONTROL):
			return

		if player.GetStatus(player.LEVEL)<constInfo.PVPMODE_PROTECTED_LEVEL:
			self.__NotifyError(localeInfo.OPTION_PVPMODE_PROTECT % (constInfo.PVPMODE_PROTECTED_LEVEL))
			return

		curTime = app.GetTime()
		if curTime - self.lastPKModeSendedTime < constInfo.PVPMODE_ACCELKEY_DELAY:
			return

		self.lastPKModeSendedTime = curTime

		curPKMode = player.GetPKMode()
		nextPKMode = curPKMode + 1
		if nextPKMode == player.PK_MODE_PROTECT:
			if 0 == player.GetGuildID():
				chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.OPTION_PVPMODE_CANNOT_SET_GUILD_MODE)
				nextPKMode = 0
			else:
				nextPKMode = player.PK_MODE_GUILD

		elif nextPKMode == player.PK_MODE_MAX_NUM:
			nextPKMode = 0

		net.SendChatPacket("/PKMode " + str(nextPKMode))
		print "/PKMode " + str(nextPKMode)

	def OnChangePKMode(self):

		self.interface.OnChangePKMode()

		try:
			self.__NotifyError(localeInfo.OPTION_PVPMODE_MESSAGE_DICT[player.GetPKMode()])
		except KeyError:
			print "UNKNOWN PVPMode[%d]" % (player.GetPKMode())

	###############################################################################################
	###############################################################################################
	## Game Callback Functions

	# Start
	def StartGame(self):
		self.RefreshInventory()
		self.RefreshEquipment()
		self.RefreshCharacter()
		self.RefreshSkill()
	
	# Refresh
	def CheckGameButton(self):
		if self.interface:
			self.interface.CheckGameButton()

	def RefreshAlignment(self):
		self.interface.RefreshAlignment()

	def RefreshStatus(self):
		self.CheckGameButton()

		if self.interface:
			self.interface.RefreshStatus()

		if self.playerGauge:
			self.playerGauge.RefreshGauge()

	def RefreshStamina(self):
		self.interface.RefreshStamina()

	def RefreshSkill(self):
		self.CheckGameButton()
		if self.interface:
			self.interface.RefreshSkill()

	def RefreshQuest(self):
		self.interface.RefreshQuest()

	def RefreshMessenger(self):
		self.interface.RefreshMessenger()

	def RefreshGuildInfoPage(self):
		self.interface.RefreshGuildInfoPage()

	def RefreshGuildBoardPage(self):
		self.interface.RefreshGuildBoardPage()

	def RefreshGuildMemberPage(self):
		self.interface.RefreshGuildMemberPage()

	def RefreshGuildMemberPageGradeComboBox(self):
		self.interface.RefreshGuildMemberPageGradeComboBox()

	def RefreshGuildSkillPage(self):
		self.interface.RefreshGuildSkillPage()

	def RefreshGuildGradePage(self):
		self.interface.RefreshGuildGradePage()

	def RefreshMobile(self):
		if self.interface:
			self.interface.RefreshMobile()

	def OnMobileAuthority(self):
		self.interface.OnMobileAuthority()

	def OnBlockMode(self, mode):
		self.interface.OnBlockMode(mode)

	def OpenQuestWindow(self, skin, idx):
		if constInfo.INPUT_IGNORE == 1:
			return

		self.interface.OpenQuestWindow(skin, idx)

	def HideAllQuestWindow(self):
		self.interface.HideAllQuestWindow()

	def AskGuildName(self):

		guildNameBoard = uiCommon.InputDialog()
		guildNameBoard.SetTitle(localeInfo.GUILD_NAME)
		guildNameBoard.SetAcceptEvent(ui.__mem_func__(self.ConfirmGuildName))
		guildNameBoard.SetCancelEvent(ui.__mem_func__(self.CancelGuildName))
		guildNameBoard.Open()

		self.guildNameBoard = guildNameBoard

	def ConfirmGuildName(self):
		guildName = self.guildNameBoard.GetText()
		if not guildName:
			return

		if net.IsInsultIn(guildName):
			self.PopupMessage(localeInfo.GUILD_CREATE_ERROR_INSULT_NAME)
			return

		net.SendAnswerMakeGuildPacket(guildName)
		self.guildNameBoard.Close()
		self.guildNameBoard = None
		return True

	def CancelGuildName(self):
		self.guildNameBoard.Close()
		self.guildNameBoard = None
		return True

	## Refine
	def PopupMessage(self, msg):
		self.stream.popupWindow.Close()
		self.stream.popupWindow.Open(msg, 0, localeInfo.UI_OK)

	def OpenRefineDialog(self, targetItemPos, nextGradeItemVnum, cost, prob, type=0):
		self.interface.OpenRefineDialog(targetItemPos, nextGradeItemVnum, cost, prob, type)

	def AppendMaterialToRefineDialog(self, vnum, count):
		self.interface.AppendMaterialToRefineDialog(vnum, count)

	def RunUseSkillEvent(self, slotIndex, coolTime):
		self.interface.OnUseSkill(slotIndex, coolTime)

	def ClearAffects(self):
		self.affectShower.ClearAffects()

	def SetAffect(self, affect):
		self.affectShower.SetAffect(affect)

	def ResetAffect(self, affect):
		self.affectShower.ResetAffect(affect)

	# UNKNOWN_UPDATE
	def BINARY_NEW_AddAffect(self, type, pointIdx, value, duration):
		# ANTI_EXP
		if type == 543 and self.interface:
			constInfo.ANTI_EXP_STATUS = 1
			if self.interface.wndTaskBar:
				self.interface.wndTaskBar.RefreshExpButton()
			return
	
		self.affectShower.BINARY_NEW_AddAffect(type, pointIdx, value, duration)

		if chr.NEW_AFFECT_DRAGON_SOUL_DECK1 == type or chr.NEW_AFFECT_DRAGON_SOUL_DECK2 == type:
			self.interface.DragonSoulActivate(type - chr.NEW_AFFECT_DRAGON_SOUL_DECK1)
		elif chr.NEW_AFFECT_DRAGON_SOUL_QUALIFIED == type:
			self.BINARY_DragonSoulGiveQuilification()

		
	def BINARY_NEW_RemoveAffect(self, type, pointIdx):
		# ANTI_EXP
		if type == 543 and self.interface:
			constInfo.ANTI_EXP_STATUS = 0
			if self.interface.wndTaskBar:
				self.interface.wndTaskBar.RefreshExpButton()
			return
	
		self.affectShower.BINARY_NEW_RemoveAffect(type, pointIdx)
		if chr.NEW_AFFECT_DRAGON_SOUL_DECK1 == type or chr.NEW_AFFECT_DRAGON_SOUL_DECK2 == type:
			self.interface.DragonSoulDeactivate()

	def ActivateSkillSlot(self, slotIndex):
		if self.interface:
			self.interface.OnActivateSkill(slotIndex)

	def DeactivateSkillSlot(self, slotIndex):
		if self.interface:
			self.interface.OnDeactivateSkill(slotIndex)

	def RefreshEquipment(self):
		if self.interface:
			self.interface.RefreshInventory()

	def RefreshInventory(self):
		if self.interface:
			self.interface.RefreshInventory()

	def RefreshCharacter(self):
		if self.interface:
			self.interface.RefreshCharacter()

	def OnGameOver(self):
		self.CloseTargetBoard()
		self.OpenRestartDialog()

	def OpenRestartDialog(self):
		self.interface.OpenRestartDialog()

	def ChangeCurrentSkill(self, skillSlotNumber):
		self.interface.OnChangeCurrentSkill(skillSlotNumber)

	# TargetBoard
	# def SetPCTargetBoard(self, vid, name):
		# self.targetBoard.Open(vid, name)

		# if app.IsPressed(app.DIK_LCONTROL):

			# if not player.IsSameEmpire(vid):
				# return

			# if player.IsMainCharacterIndex(vid):
				# return
			# elif chr.INSTANCE_TYPE_BUILDING == chr.GetInstanceType(vid):
				# return

			# self.interface.OpenWhisperDialog(name)

	def RefreshTargetBoardByVID(self, vid):
		if self.targetBoard:
			self.targetBoard.RefreshByVID(vid)

	def RefreshTargetBoardByName(self, name):
		if self.targetBoard:
			self.targetBoard.RefreshByName(name)

	def __RefreshTargetBoard(self):
		if self.targetBoard:
			self.targetBoard.Refresh()

	def SetHPTargetBoard(self, vid, hpPercentage, iMinHP, iMaxHP):
		if self.interface:
			if chr.IsSupport(vid):
				return
				
			if vid != self.targetBoard.GetTargetVID():
				self.targetBoard.ResetTargetBoard()
				self.targetBoard.SetEnemyVID(vid)
		
		self.targetBoard.SetHP(hpPercentage, iMinHP, iMaxHP)
		self.targetBoard.Show()
		
	def CloseTargetBoardIfDifferent(self, vid):
		if vid != self.targetBoard.GetTargetVID():
			self.targetBoard.Close()

	def CloseTargetBoard(self):
		self.targetBoard.Close()

	def SetElementImagePC(self, dwVID, bElement):
		self.targetBoard.SetElementImage(bElement)
		# self.targetBoard.SetRaceElement(dwVID)

	## View Equipment
	def OpenEquipmentDialog(self, vid):
		self.interface.OpenEquipmentDialog(vid)

	def SetEquipmentDialogItem(self, vid, slotIndex, vnum, count):
		self.interface.SetEquipmentDialogItem(vid, slotIndex, vnum, count)

	def SetEquipmentDialogSocket(self, vid, slotIndex, socketIndex, value):
		self.interface.SetEquipmentDialogSocket(vid, slotIndex, socketIndex, value)

	def SetEquipmentDialogAttr(self, vid, slotIndex, attrIndex, type, value):
		self.interface.SetEquipmentDialogAttr(vid, slotIndex, attrIndex, type, value)

	# SHOW_LOCAL_MAP_NAME
	def ShowMapName(self, mapName, x, y):

		if self.mapNameShower:
			self.mapNameShower.ShowMapName(mapName, x, y)

		if self.interface:
			self.interface.SetMapName(mapName)
	# END_OF_SHOW_LOCAL_MAP_NAME

	def BINARY_OpenAtlasWindow(self):
		self.interface.BINARY_OpenAtlasWindow()

	def OnRecvWhisper(self, mode, name, line):
		if mode == chat.WHISPER_TYPE_GM:
			self.interface.RegisterGameMasterName(name)
		chat.AppendToBox(mode, name, line)
		self.interface.RecvWhisper(name)

	def OnRecvWhisperSystemMessage(self, mode, name, line):
		chat.AppendToBox(chat.WHISPER_TYPE_SYSTEM, name, line)
		self.interface.RecvWhisper(name)

	def OnRecvWhisperError(self, mode, name, line):
		if localeInfo.WHISPER_ERROR.has_key(mode):
			chat.AppendToBox(chat.WHISPER_TYPE_SYSTEM, name, localeInfo.WHISPER_ERROR[mode] % (name))
		else:
			chat.AppendToBox(chat.WHISPER_TYPE_SYSTEM, name, "Whisper Unknown Error(mode=%d, name=%s)" % (mode, name))
		self.interface.RecvWhisper(name)

	def OnPickMoney(self, money):
		# self.wndDropDialog.AppendItem(1, int(money)) // GRIMM WORK
		# if systemSetting.IsHideYang():
			# return True
	
		# chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.GAME_PICK_MONEY % (money))
		
		if app.ENABLE_CHATTING_WINDOW_RENEWAL:
			chat.AppendChat(chat.CHAT_TYPE_MONEY_INFO, localeInfo.GAME_PICK_MONEY % (money))
		else:
			chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.GAME_PICK_MONEY % (money))
			
	def OnReceiveItemDrop(self, ItemVnum, ItemCount):
		self.wndDropDialog.AppendItem(int(ItemVnum), int(ItemCount))

	def OnPickGaya(self, type, amount):
		if type == 0:
			chat.AppendChat(chat.CHAT_TYPE_INFO, "Ai primit %d Gaya Albastra." % int(amount))
		else:
			chat.AppendChat(chat.CHAT_TYPE_INFO, "Ai primit %d Gaya Verde." % int(amount))
	
	def OnShopError(self, type):
		try:
			self.PopupMessage(localeInfo.SHOP_ERROR_DICT[type])
		except KeyError:
			self.PopupMessage(localeInfo.SHOP_ERROR_UNKNOWN % (type))

	def OnSafeBoxError(self):
		self.PopupMessage(localeInfo.SAFEBOX_ERROR)

	def OnFishingSuccess(self, isFish, fishName):
		chat.AppendChatWithDelay(chat.CHAT_TYPE_INFO, localeInfo.FISHING_SUCCESS(isFish, fishName), 2000)

	def OnFishingNotifyUnknown(self):
		chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.FISHING_UNKNOWN)

	def OnFishingWrongPlace(self):
		chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.FISHING_WRONG_PLACE)

	def OnFishingNotify(self, isFish, fishName):
		chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.FISHING_NOTIFY(isFish, fishName))

	def OnFishingFailure(self):
		chat.AppendChatWithDelay(chat.CHAT_TYPE_INFO, localeInfo.FISHING_FAILURE, 2000)

	def OnCannotPickItem(self):
		chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.GAME_CANNOT_PICK_ITEM)

	def OnCannotMining(self):
		chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.GAME_CANNOT_MINING)

	def OnCannotUseSkill(self, vid, type):
		if localeInfo.USE_SKILL_ERROR_TAIL_DICT.has_key(type):
			if self.NewMessageGame:
				self.NewMessageGame.SetNotify(localeInfo.USE_SKILL_ERROR_TAIL_DICT[type])
				self.NewMessageGame.Show()
			
		if localeInfo.USE_SKILL_ERROR_CHAT_DICT.has_key(type):
			chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.USE_SKILL_ERROR_CHAT_DICT[type])

	def	OnCannotShotError(self, vid, type):
		textTail.RegisterInfoTail(vid, localeInfo.SHOT_ERROR_TAIL_DICT.get(type, localeInfo.SHOT_ERROR_UNKNOWN % (type)))

	def StartPointReset(self):
		self.interface.OpenPointResetDialog()

	def StartShop(self, vid): ## OFFLINE_SHOP
		self.interface.OpenShopDialog(vid)

	def EndShop(self):
		self.interface.CloseShopDialog()

	def RefreshShop(self):
		self.interface.RefreshShopDialog()

	def SetShopSellingPrice(self, Price):
		pass

	def StartExchange(self):
		self.interface.StartExchange()

	def EndExchange(self):
		self.interface.EndExchange()

	def RefreshExchange(self):
		self.interface.RefreshExchange()

	def RecvPartyInviteQuestion(self, leaderVID, leaderName):
		partyInviteQuestionDialog = uiCommon.QuestionDialogWithTimeLimit()
		partyInviteQuestionDialog.SetTimeOverMsg(localeInfo.PARTY_ANSWER_TIMEOVER)
		partyInviteQuestionDialog.SetTimeOverEvent(self.AnswerPartyInvite, False)
		partyInviteQuestionDialog.SetAcceptEvent(lambda arg=True: self.AnswerPartyInvite(arg))
		partyInviteQuestionDialog.SetCancelEvent(lambda arg=False: self.AnswerPartyInvite(arg))
		partyInviteQuestionDialog.Open(leaderName + localeInfo.PARTY_DO_YOU_JOIN, 10)
		partyInviteQuestionDialog.partyLeaderVID = leaderVID
		self.partyInviteQuestionDialog = partyInviteQuestionDialog

	def AnswerPartyInvite(self, answer):

		if not self.partyInviteQuestionDialog:
			return

		partyLeaderVID = self.partyInviteQuestionDialog.partyLeaderVID

		distance = player.GetCharacterDistance(partyLeaderVID)
		if distance < 0.0 or distance > 5000:
			answer = False

		net.SendPartyInviteAnswerPacket(partyLeaderVID, answer)

		self.partyInviteQuestionDialog.Close()
		self.partyInviteQuestionDialog = None

	def AddPartyMember(self, pid, name):
		self.interface.AddPartyMember(pid, name)

	def UpdatePartyMemberInfo(self, pid):
		self.interface.UpdatePartyMemberInfo(pid)

	def RemovePartyMember(self, pid):
		self.interface.RemovePartyMember(pid)
		self.__RefreshTargetBoard()

	def LinkPartyMember(self, pid, vid):
		self.interface.LinkPartyMember(pid, vid)

	def UnlinkPartyMember(self, pid):
		self.interface.UnlinkPartyMember(pid)

	def UnlinkAllPartyMember(self):
		self.interface.UnlinkAllPartyMember()

	def ExitParty(self):
		self.interface.ExitParty()
		self.RefreshTargetBoardByVID(self.targetBoard.GetTargetVID())

	def ChangePartyParameter(self, distributionMode):
		self.interface.ChangePartyParameter(distributionMode)

	def OnMessengerAddFriendQuestion(self, name):
		messengerAddFriendQuestion = uiCommon.QuestionDialogWithTimeLimit()
		messengerAddFriendQuestion.SetTimeOverMsg(localeInfo.MESSENGER_ADD_FRIEND_ANSWER_TIMEOVER)
		messengerAddFriendQuestion.SetTimeOverEvent(self.OnDenyAddFriend)
		messengerAddFriendQuestion.SetAcceptEvent(ui.__mem_func__(self.OnAcceptAddFriend))
		messengerAddFriendQuestion.SetCancelEvent(ui.__mem_func__(self.OnDenyAddFriend))
		messengerAddFriendQuestion.Open(localeInfo.MESSENGER_DO_YOU_ACCEPT_ADD_FRIEND % (name.replace("#", " ")), 10) # GRM SPACE
		messengerAddFriendQuestion.name = name
		self.messengerAddFriendQuestion = messengerAddFriendQuestion

	def OnAcceptAddFriend(self):
		name = self.messengerAddFriendQuestion.name
		net.SendChatPacket("/messenger_auth y " + name)
		self.OnCloseAddFriendQuestionDialog()
		return True

	def OnDenyAddFriend(self):
		name = self.messengerAddFriendQuestion.name
		net.SendChatPacket("/messenger_auth n " + name)
		self.OnCloseAddFriendQuestionDialog()
		return True

	def OnCloseAddFriendQuestionDialog(self):
		self.messengerAddFriendQuestion.Close()
		self.messengerAddFriendQuestion = None
		return True

	def OpenSafeboxWindow(self, size):
		self.interface.OpenSafeboxWindow(size)

	def RefreshSafebox(self):
		self.interface.RefreshSafebox()

	def RefreshSafeboxMoney(self):
		self.interface.RefreshSafeboxMoney()

	def OpenMallWindow(self, size):
		self.interface.OpenMallWindow(size)

	def RefreshMall(self):
		self.interface.RefreshMall()

	def RecvGuildInviteQuestion(self, guildID, guildName):
		guildInviteQuestionDialog = uiCommon.QuestionDialogWithTimeLimit()
		guildInviteQuestionDialog.SetTimeOverEvent(lambda arg=False: self.AnswerGuildInvite(arg))
		guildInviteQuestionDialog.SetAcceptEvent(lambda arg=True: self.AnswerGuildInvite(arg))
		guildInviteQuestionDialog.SetCancelEvent(lambda arg=False: self.AnswerGuildInvite(arg))
		guildInviteQuestionDialog.Open(guildName + localeInfo.GUILD_DO_YOU_JOIN, 10)
		guildInviteQuestionDialog.guildID = guildID
		self.guildInviteQuestionDialog = guildInviteQuestionDialog

	def AnswerGuildInvite(self, answer):

		if not self.guildInviteQuestionDialog:
			return

		guildLeaderVID = self.guildInviteQuestionDialog.guildID
		net.SendGuildInviteAnswerPacket(guildLeaderVID, answer)

		self.guildInviteQuestionDialog.Close()
		self.guildInviteQuestionDialog = None


	def DeleteGuild(self):
		self.interface.DeleteGuild()

	def ShowClock(self, second):
		self.interface.ShowClock(second)

	def HideClock(self):
		self.interface.HideClock()

	def BINARY_ActEmotion(self, emotionIndex):
		if self.interface.wndCharacter:
			self.interface.wndCharacter.ActEmotion(emotionIndex)

	def CheckFocus(self):
		if False == self.IsFocus():
			if True == self.interface.IsOpenChat():
				self.interface.ToggleChat()

			self.SetFocus()

	def SaveScreen(self):
		print "save screen"

		if SCREENSHOT_CWDSAVE:
			if not os.path.exists(os.getcwd()+os.sep+"screenshot"):
				os.mkdir(os.getcwd()+os.sep+"screenshot")

			(succeeded, name) = grp.SaveScreenShotToPath(os.getcwd()+os.sep+"screenshot"+os.sep)
		elif SCREENSHOT_DIR:
			(succeeded, name) = grp.SaveScreenShot(SCREENSHOT_DIR)
		else:
			(succeeded, name) = grp.SaveScreenShot()

		if succeeded:
			pass
			"""
			chat.AppendChat(chat.CHAT_TYPE_INFO, name + localeInfo.SCREENSHOT_SAVE1)
			chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.SCREENSHOT_SAVE2)
			"""
		else:
			chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.SCREENSHOT_SAVE_FAILURE)

	def ShowName(self):
		self.ShowNameFlag = True
		self.playerGauge.EnableShowAlways()
		player.SetQuickPage(self.quickSlotPageIndex+1)

	def __IsShowName(self):

		if systemSetting.IsAlwaysShowName():
			return True

		if self.ShowNameFlag:
			return True

		return False

	def HideName(self):
		self.ShowNameFlag = False
		self.playerGauge.DisableShowAlways()
		player.SetQuickPage(self.quickSlotPageIndex)

	def ShowMouseImage(self):
		self.interface.ShowMouseImage()

	def HideMouseImage(self):
		self.interface.HideMouseImage()

	def StartAttack(self):
		player.SetAttackKeyState(True)

	def EndAttack(self):
		player.SetAttackKeyState(False)

	def MoveUp(self):
		player.SetSingleDIKKeyState(app.DIK_UP, True)

	def MoveDown(self):
		player.SetSingleDIKKeyState(app.DIK_DOWN, True)

	def MoveLeft(self):
		player.SetSingleDIKKeyState(app.DIK_LEFT, True)

	def MoveRight(self):
		player.SetSingleDIKKeyState(app.DIK_RIGHT, True)

	def StopUp(self):
		player.SetSingleDIKKeyState(app.DIK_UP, False)

	def StopDown(self):
		player.SetSingleDIKKeyState(app.DIK_DOWN, False)

	def StopLeft(self):
		player.SetSingleDIKKeyState(app.DIK_LEFT, False)

	def StopRight(self):
		player.SetSingleDIKKeyState(app.DIK_RIGHT, False)

	def PickUpItem(self):
		if app.ENABLE_INSTANT_PICK_UP:
			player.PickCloseItemVector()
		else:
			player.PickCloseItem()

	def OnKeyDown(self, key):
		if key == app.DIK_ESC:
			self.RequestDropItem(False)
			constInfo.SET_ITEM_QUESTION_DIALOG_STATUS(0)

		try:
			self.onPressKeyDict[key]()
		except KeyError:
			pass
		except:
			raise

		return True

	def OnKeyUp(self, key):
		try:
			self.onClickKeyDict[key]()
		except KeyError:
			pass
		except:
			raise

		return True

	def OnMouseLeftButtonDown(self):
		if self.interface.BUILD_OnMouseLeftButtonDown():
			return

		if mouseModule.mouseController.isAttached():
			self.CheckFocus()
		else:
			hyperlink = ui.GetHyperlink()
			if hyperlink:
				return
			else:
				self.CheckFocus()
				player.SetMouseState(player.MBT_LEFT, player.MBS_PRESS);

		return True

	def OnMouseLeftButtonUp(self):

		if self.interface.BUILD_OnMouseLeftButtonUp():
			return

		if mouseModule.mouseController.isAttached():

			attachedType = mouseModule.mouseController.GetAttachedType()
			attachedItemIndex = mouseModule.mouseController.GetAttachedItemIndex()
			attachedItemSlotPos = mouseModule.mouseController.GetAttachedSlotNumber()
			attachedItemCount = mouseModule.mouseController.GetAttachedItemCount()

			## QuickSlot
			if player.SLOT_TYPE_QUICK_SLOT == attachedType:
				player.RequestDeleteGlobalQuickSlot(attachedItemSlotPos)

			## Inventory
			elif player.SLOT_TYPE_INVENTORY == attachedType:

				if player.ITEM_MONEY == attachedItemIndex:
					self.__PutMoney(attachedType, attachedItemCount, self.PickingCharacterIndex)
				else:
					self.__PutItem(attachedType, attachedItemIndex, attachedItemSlotPos, attachedItemCount, self.PickingCharacterIndex)

			## DragonSoul
			elif player.SLOT_TYPE_DRAGON_SOUL_INVENTORY == attachedType:
				self.__PutItem(attachedType, attachedItemIndex, attachedItemSlotPos, attachedItemCount, self.PickingCharacterIndex)

			mouseModule.mouseController.DeattachObject()

		else:
			hyperlink = ui.GetHyperlink()
			if hyperlink:
				if app.IsPressed(app.DIK_LALT):
					link = chat.GetLinkFromHyperlink(hyperlink)
					ime.PasteString(link)
				else:
					self.interface.MakeHyperlinkTooltip(hyperlink)
				return
			else:
				player.SetMouseState(player.MBT_LEFT, player.MBS_CLICK)

		#player.EndMouseWalking()
		return True

	def __PutItem(self, attachedType, attachedItemIndex, attachedItemSlotPos, attachedItemCount, dstChrID):
		if player.SLOT_TYPE_INVENTORY == attachedType or player.SLOT_TYPE_DRAGON_SOUL_INVENTORY == attachedType:
			attachedInvenType = player.SlotTypeToInvenType(attachedType)
			if True == chr.HasInstance(self.PickingCharacterIndex) and player.GetMainCharacterIndex() != dstChrID:
				if player.IsEquipmentSlot(attachedItemSlotPos) and player.SLOT_TYPE_DRAGON_SOUL_INVENTORY != attachedType:
					self.stream.popupWindow.Close()
					self.stream.popupWindow.Open(localeInfo.EXCHANGE_FAILURE_EQUIP_ITEM, 0, localeInfo.UI_OK)
				else:
					if chr.IsNPC(dstChrID) or chr.IsSupport(dstChrID):
						net.SendGiveItemPacket(dstChrID, attachedInvenType, attachedItemSlotPos, attachedItemCount)
					else:
						net.SendExchangeStartPacket(dstChrID)
						net.SendExchangeItemAddPacket(attachedInvenType, attachedItemSlotPos, 0)
			else:
				self.__DropItem(attachedType, attachedItemIndex, attachedItemSlotPos, attachedItemCount)
				
				constInfo.AUTO_REFINE_TYPE = 2
				constInfo.AUTO_REFINE_DATA["NPC"][0] = dstChrID
				constInfo.AUTO_REFINE_DATA["NPC"][1] = attachedInvenType
				constInfo.AUTO_REFINE_DATA["NPC"][2] = attachedItemSlotPos
				constInfo.AUTO_REFINE_DATA["NPC"][3] = attachedItemCount

	def __PutMoney(self, attachedType, attachedMoney, dstChrID):
		if True == chr.HasInstance(dstChrID) and player.GetMainCharacterIndex() != dstChrID:
			net.SendExchangeStartPacket(dstChrID)
			net.SendExchangeElkAddPacket(attachedMoney)
		else:
			self.__DropMoney(attachedType, attachedMoney)

	def __DropMoney(self, attachedType, attachedMoney):
		if uiPrivateShopBuilder.IsBuildingPrivateShop():
			chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.DROP_ITEM_FAILURE_PRIVATE_SHOP)
			return

		if attachedMoney>=0:
			self.stream.popupWindow.Close()
			self.stream.popupWindow.Open(localeInfo.DROP_MONEY_FAILURE_1000_OVER, 0, localeInfo.UI_OK)
			return

		itemDropQuestionDialog = uiCommon.QuestionDialog()
		itemDropQuestionDialog.SetText(localeInfo.DO_YOU_DROP_MONEY % (attachedMoney))
		itemDropQuestionDialog.SetAcceptEvent(lambda arg=True: self.RequestDropItem(arg))
		itemDropQuestionDialog.SetCancelEvent(lambda arg=False: self.RequestDropItem(arg))
		itemDropQuestionDialog.Open()
		itemDropQuestionDialog.dropType = attachedType
		itemDropQuestionDialog.dropCount = attachedMoney
		itemDropQuestionDialog.dropNumber = player.ITEM_MONEY
		self.itemDropQuestionDialog = itemDropQuestionDialog

	def __DropItem(self, attachedType, attachedItemIndex, attachedItemSlotPos, attachedItemCount):
		if uiPrivateShopBuilder.IsBuildingPrivateShop():
			chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.DROP_ITEM_FAILURE_PRIVATE_SHOP)
			return

		if player.SLOT_TYPE_INVENTORY == attachedType and player.IsEquipmentSlot(attachedItemSlotPos):
			self.stream.popupWindow.Close()
			self.stream.popupWindow.Open(localeInfo.DROP_ITEM_FAILURE_EQUIP_ITEM, 0, localeInfo.UI_OK)

		else:
			# if attachedType in [ player.SLOT_TYPE_INVENTORY, player.SLOT_TYPE_DRAGON_SOUL_INVENTORY]:
			if player.SLOT_TYPE_INVENTORY == attachedType:
				dropItemIndex = player.GetItemIndex(attachedItemSlotPos)

				item.SelectItem(dropItemIndex)
				dropItemName = item.GetItemName()

				## Question Text
				questionText = localeInfo.HOW_MANY_ITEM_DO_YOU_DROP(dropItemName, attachedItemCount)

				itemDropQuestionDialog = uiCommon.QuestionDropDialog()
				itemDropQuestionDialog.SetAcceptEvent(lambda arg=True: self.RequestDropItem(arg))
				itemDropQuestionDialog.SetDestroyEvent(lambda arg=True: self.RequestDestroyItem(arg))
				itemDropQuestionDialog.SetCancelEvent(lambda arg=False: self.RequestDropItemStorage(arg))
				itemDropQuestionDialog.SetItemSlot(attachedItemSlotPos)
				itemDropQuestionDialog.dropType = attachedType
				itemDropQuestionDialog.dropNumber = attachedItemSlotPos
				itemDropQuestionDialog.dropCount = attachedItemCount
				itemDropQuestionDialog.Open()
				self.itemDropQuestionDialog = itemDropQuestionDialog

				constInfo.SET_ITEM_QUESTION_DIALOG_STATUS(1)

			elif player.SLOT_TYPE_DRAGON_SOUL_INVENTORY == attachedType:
				dropItemIndex = player.GetItemIndex(player.DRAGON_SOUL_INVENTORY, attachedItemSlotPos)
				
				itemtype = -1
		
				if attachedType == player.SLOT_TYPE_DRAGON_SOUL_INVENTORY:
					itemtype = player.DRAGON_SOUL_INVENTORY

				item.SelectItem(dropItemIndex)
				dropItemName = item.GetItemName()

				# Question Text
				questionText = localeInfo.HOW_MANY_ITEM_DO_YOU_DROP(dropItemName, attachedItemCount)

				# Dialog
				itemDropQuestionDialog = uiCommon.ItemQuestionDialog()
				itemDropQuestionDialog.SetAcceptEvent(lambda arg=True: self.RequestDropItem(arg))
				itemDropQuestionDialog.SetCancelEvent(lambda arg=False: self.RequestDropItem(arg))
				if app.ENABLE_COSTUME_SYSTEM:
					itemDropQuestionDialog.SetDestroyEvent(lambda arg=True: self.RequestDestroyItem(arg))
				itemDropQuestionDialog.Open(dropItemIndex, attachedItemSlotPos, itemtype, questionText)
				itemDropQuestionDialog.dropType = attachedType
				itemDropQuestionDialog.dropNumber = attachedItemSlotPos
				itemDropQuestionDialog.dropCount = attachedItemCount
				self.itemDropQuestionDialog = itemDropQuestionDialog
				
				constInfo.SET_ITEM_QUESTION_DIALOG_STATUS(1)


	def RequestDropItem(self, answer):
		if not self.itemDropQuestionDialog:
			return

		if answer:
			dropType = self.itemDropQuestionDialog.dropType
			dropCount = self.itemDropQuestionDialog.dropCount
			dropNumber = self.itemDropQuestionDialog.dropNumber

			if player.SLOT_TYPE_INVENTORY == dropType:
				if dropNumber == player.ITEM_MONEY:
					net.SendGoldDropPacketNew(dropCount)
				else:
					# PRIVATESHOP_DISABLE_ITEM_DROP
					self.__SendDropItemPacket(dropNumber, dropCount)
					# END_OF_PRIVATESHOP_DISABLE_ITEM_DROP

			elif player.SLOT_TYPE_DRAGON_SOUL_INVENTORY == dropType:
				self.__SendDropItemPacket(dropNumber, dropCount, player.DRAGON_SOUL_INVENTORY)
			

		self.itemDropQuestionDialog.Close()
		self.itemDropQuestionDialog = None

		constInfo.SET_ITEM_QUESTION_DIALOG_STATUS(0)

	def RequestDropItemStorage(self, answer):
		if not self.itemDropQuestionDialog:
			return
			
		if answer:
			dropType = self.itemDropQuestionDialog.dropType
			dropCount = self.itemDropQuestionDialog.dropCount
			dropNumber = self.itemDropQuestionDialog.dropNumber

			if player.SLOT_TYPE_INVENTORY == dropType:
				if dropNumber == player.ITEM_MONEY:
					net.SendGoldDropPacketNew(dropCount)
				else:
					# PRIVATESHOP_DISABLE_ITEM_DROP
					self.__SendDropItemPacket(dropNumber, dropCount)
					# END_OF_PRIVATESHOP_DISABLE_ITEM_DROP

			if app.ENABLE_SPECIAL_STORAGE:
				if player.SLOT_TYPE_UPGRADE_INVENTORY == dropType or\
					player.SLOT_TYPE_BOOK_INVENTORY == dropType or\
					player.SLOT_TYPE_DRAGON_SOUL_INVENTORY == dropType or\
					player.SLOT_TYPE_STONE_INVENTORY == dropType:
					self.__SendDropItemPacket(dropNumber, dropCount, player.SlotTypeToInvenType(dropType))
					
		self.itemDropQuestionDialog.Close()
		self.itemDropQuestionDialog = None

		constInfo.SET_ITEM_QUESTION_DIALOG_STATUS(0)

	def RequestDestroyItem(self, answer):
		if not self.itemDropQuestionDialog:
			return

		if answer:
			dropType = self.itemDropQuestionDialog.dropType
			dropNumber = self.itemDropQuestionDialog.dropNumber
			if player.SLOT_TYPE_INVENTORY == dropType:
				if dropNumber == player.ITEM_MONEY:
					return
				else:
					self.__SendDestroyItemPacket(dropNumber)
				# chat.AppendChat(1, "Try to destroy inventory.")
			elif player.SLOT_TYPE_DRAGON_SOUL_INVENTORY == dropType:
				self.__SendDestroyItemPacket(dropNumber, player.DRAGON_SOUL_INVENTORY)
				# chat.AppendChat(1, "Try to destroy DSS")

		self.itemDropQuestionDialog.Close()
		self.itemDropQuestionDialog = None
		constInfo.SET_ITEM_DROP_QUESTION_DIALOG_STATUS(0)
		
	def __SendDropItemPacket(self, itemVNum, itemCount, itemInvenType = player.INVENTORY):
		if uiPrivateShopBuilder.IsBuildingPrivateShop():
			chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.DROP_ITEM_FAILURE_PRIVATE_SHOP)
			return

		net.SendItemDropPacketNew(itemInvenType, itemVNum, itemCount)

	def __SendDestroyItemPacket(self, itemVNum, itemInvenType = player.INVENTORY):
		if uiPrivateShopBuilder.IsBuildingPrivateShop():
			chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.DROP_ITEM_FAILURE_PRIVATE_SHOP)
			return
			
		# if itemInvenType == player.DRAGON_SOUL_INVENTORY:
			# chat.AppendChat(1, "bla bla dragonsoul inventory type")
		net.SendItemDestroyPacket(itemInvenType, itemVNum)

		# net.SendItemDestroyPacket(itemVNum)
		# chat.AppendChat(1, "__SendDestroyItemPacket")

	def OnMouseRightButtonDown(self):

		self.CheckFocus()

		if True == mouseModule.mouseController.isAttached():
			mouseModule.mouseController.DeattachObject()

		else:
			player.SetMouseState(player.MBT_RIGHT, player.MBS_PRESS)

		return True

	def OnMouseRightButtonUp(self):
		if True == mouseModule.mouseController.isAttached():
			return True

		player.SetMouseState(player.MBT_RIGHT, player.MBS_CLICK)
		return True

	def OnMouseMiddleButtonDown(self):
		player.SetMouseMiddleButtonState(player.MBS_PRESS)

	def OnMouseMiddleButtonUp(self):
		player.SetMouseMiddleButtonState(player.MBS_CLICK)

	def OnUpdate(self):
		app.UpdateGame()

		if self.mapNameShower.IsShow():
			self.mapNameShower.Update()

		if self.enableXMasBoom:
			self.__XMasBoom_Update()
			
		if self.wndDropDialog:
			if self.wndDropDialog.GetItemsSize() == 0:
				self.wndDropDialog.Hide()
			else:
				if self.wndDropDialog.IsShow() == FALSE:
					self.wndDropDialog.Show()
					
		if constInfo.auto_shout_status == 1:
			if self.shouttime <= app.GetTime():
				self.shouttime = app.GetTime()+5
				net.SendChatPacket(str(constInfo.auto_shout_text), chat.CHAT_TYPE_SHOUT)
				
		if constInfo.QUESTION != "":
			for key in constInfo.ANSWER:
				if constInfo.QUESTION.find(key) != -1:
					line = constInfo.BOT_NAME + ": " + constInfo.ANSWER[key]
					self.OnRecvWhisper(chat.WHISPER_TYPE_CHAT, constInfo.BOT_NAME, line)
					constInfo.QUESTION = ""
					return
					
			self.OnRecvWhisper(chat.WHISPER_TYPE_CHAT, constInfo.BOT_NAME, constInfo.BOT_NAME+": " + "|cff00FF7F" + uiScriptLocale.WHISPER_BOT_WARNING + "|r")
			constInfo.QUESTION = ""
			
		leftTimeBio = max(0, constInfo.END_TIME_BIO - app.GetGlobalTimeStamp())
		if constInfo.END_TIME_BIO > 0 and leftTimeBio <= 0:
			constInfo.END_TIME_BIO = 0
			if constInfo.ENABLE_BIO_NOTIF == 1:
				self.interface.LoadAppLeftTip("[BIOLOG]" ,"BIOLOG")
				# constInfo.END_TIME_BIO = 0
			
		if constInfo.CLICK_MISSIONS == 1:
			if constInfo.SET_MISSIONS == 0:
				self.interface.HideAllQuestButton()
				interfaceModule.IsQBHide = 1
			elif constInfo.SET_MISSIONS == 1:
				self.interface.ShowAllQuestButton()
				interfaceModule.IsQBHide = 0

		if player.IsPremiumUser() == 1 or player.IsPremiumUser() == 2 or player.IsPremiumUser() == 3:
			for i in xrange(9):
				self.emoticonCfg = cfg.Get(cfg.SAVE_GENERAL, "EMOTICON_%s" % i)
				player.SetEmoticonForNum(i, int(self.emoticonCfg))
		else:
			for i in xrange(9):
				player.SetEmoticonForNum(i, int(i))
				
		if systemSetting.IsEnablePremiumAffect():
			self.affectShower.Show()
		else:
			self.affectShower.Hide()

		self.interface.BUILD_OnUpdate()

	def OnRender(self):
		app.RenderGame()

		(x, y) = app.GetCursorPosition()
		textTail.UpdateAllTextTail()

		if True == wndMgr.IsPickedWindow(self.hWnd):

			self.PickingCharacterIndex = chr.Pick()

			if -1 != self.PickingCharacterIndex:
				textTail.ShowCharacterTextTail(self.PickingCharacterIndex)
			if 0 != self.targetBoard.GetTargetVID():
				textTail.ShowCharacterTextTail(self.targetBoard.GetTargetVID())

			# ADD_ALWAYS_SHOW_NAME
			if not self.__IsShowName():
				self.PickingItemIndex = item.Pick()
				if -1 != self.PickingItemIndex:
					textTail.ShowItemTextTail(self.PickingItemIndex)
			# END_OF_ADD_ALWAYS_SHOW_NAME

		# ADD_ALWAYS_SHOW_NAME
		if self.__IsShowName():
			textTail.ShowAllTextTail()
			self.PickingItemIndex = textTail.Pick(x, y)
		# END_OF_ADD_ALWAYS_SHOW_NAME

		textTail.UpdateShowingTextTail()
		textTail.ArrangeTextTail()
		if -1 != self.PickingItemIndex:
			textTail.SelectItemName(self.PickingItemIndex)

		grp.PopState()
		grp.SetInterfaceRenderState()

		textTail.Render()
		textTail.HideAllTextTail()

	def OnPressEscapeKey(self):
		if app.TARGET == app.GetCursor():
			app.SetCursor(app.NORMAL)

		elif True == mouseModule.mouseController.isAttached():
			mouseModule.mouseController.DeattachObject()

		else:
			self.itemDropQuestionDialog = None
			constInfo.SET_ITEM_QUESTION_DIALOG_STATUS(0)
			self.interface.OpenSystemDialog()

		return True

	def OnIMEReturn(self):
		if app.IsPressed(app.DIK_LSHIFT):
			self.interface.OpenWhisperDialogWithoutTarget()
		else:
			self.interface.ToggleChat()
		return True

	def OnPressExitKey(self):
		self.interface.ToggleSystemDialog()
		return True

	if app.WJ_ENABLE_TRADABLE_ICON:
		def BINARY_AddItemToExchange(self, inven_type, inven_pos, display_pos):
			if inven_type == player.INVENTORY:
				self.interface.CantTradableItemExchange(display_pos, inven_pos)

	def BINARY_LoverInfo(self, name, lovePoint):
		if self.interface.wndMessenger:
			self.interface.wndMessenger.OnAddLover(name, lovePoint)
			
		if self.affectShower:
			self.affectShower.SetLoverInfo(name, lovePoint)

	def BINARY_UpdateLovePoint(self, lovePoint):
		if self.interface.wndMessenger:
			self.interface.wndMessenger.OnUpdateLovePoint(lovePoint)
			
		if self.affectShower:
			self.affectShower.OnUpdateLovePoint(lovePoint)

	def BINARY_OnQuestConfirm(self, msg, timeout, pid):
		confirmDialog = uiCommon.QuestionDialogWithTimeLimit()
		confirmDialog.Open(msg, timeout)
		confirmDialog.SetAcceptEvent(lambda answer=True, pid=pid: net.SendQuestConfirmPacket(answer, pid) or self.confirmDialog.Hide())
		confirmDialog.SetCancelEvent(lambda answer=False, pid=pid: net.SendQuestConfirmPacket(answer, pid) or self.confirmDialog.Hide())
		self.confirmDialog = confirmDialog

	def Gift_Show(self):
		self.interface.ShowGift()

	def BINARY_CUBE_RENEWAL_LOADING(self):
		self.interface.BINARY_CUBE_RENEWAL_LOADING()
		
	def BINARY_CUBE_RENEWAL_OPEN(self):
		if self.interface:
			self.interface.BINARY_CUBE_RENEWAL_OPEN()
	
	def BINARY_Cube_Open(self, npcVNUM):
		self.currentCubeNPC = npcVNUM

	if app.ENABLE_MINIGAME_RUMI_EVENT:
		def BINARY_Cards_UpdateInfo(self, hand_1, hand_1_v, hand_2, hand_2_v, hand_3, hand_3_v, hand_4, hand_4_v, hand_5, hand_5_v, cards_left, points):
			self.interface.UpdateCardsInfo(hand_1, hand_1_v, hand_2, hand_2_v, hand_3, hand_3_v, hand_4, hand_4_v, hand_5, hand_5_v, cards_left, points)

		def BINARY_Cards_FieldUpdateInfo(self, hand_1, hand_1_v, hand_2, hand_2_v, hand_3, hand_3_v, points):
			self.interface.UpdateCardsFieldInfo(hand_1, hand_1_v, hand_2, hand_2_v, hand_3, hand_3_v, points)

		def BINARY_Cards_PutReward(self, hand_1, hand_1_v, hand_2, hand_2_v, hand_3, hand_3_v, points):
			self.interface.CardsPutReward(hand_1, hand_1_v, hand_2, hand_2_v, hand_3, hand_3_v, points)

		def BINARY_Cards_ShowIcon(self):
			self.interface.CardsShowIcon()

		def BINARY_Cards_Open(self, safemode):
			self.interface.OpenCardsWindow(safemode)

	def BINARY_SetBigMessage(self, message):
		self.interface.bigBoard.SetTip(message)

	def BINARY_SetTipMessage(self, message):
		self.interface.tipBoard.SetTip(message)

	def BINARY_AppendNotifyMessage(self, type):
		if not type in localeInfo.NOTIFY_MESSAGE:
			return
		chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.NOTIFY_MESSAGE[type])

	def BINARY_Guild_EnterGuildArea(self, areaID):
		self.interface.BULID_EnterGuildArea(areaID)

	def BINARY_Guild_ExitGuildArea(self, areaID):
		self.interface.BULID_ExitGuildArea(areaID)

	def BINARY_GuildWar_OnSendDeclare(self, guildID):
		pass

	def BINARY_GuildWar_OnRecvDeclare(self, guildID, warType):
		mainCharacterName = player.GetMainCharacterName()
		masterName = guild.GetGuildMasterName()
		if mainCharacterName == masterName:
			self.__GuildWar_OpenAskDialog(guildID, warType)

	def BINARY_GuildWar_OnRecvPoint(self, gainGuildID, opponentGuildID, point):
		self.interface.OnRecvGuildWarPoint(gainGuildID, opponentGuildID, point)

	def BINARY_GuildWar_OnStart(self, guildSelf, guildOpp):
		self.interface.OnStartGuildWar(guildSelf, guildOpp)

	def BINARY_GuildWar_OnEnd(self, guildSelf, guildOpp):
		self.interface.OnEndGuildWar(guildSelf, guildOpp)

	def BINARY_BettingGuildWar_SetObserverMode(self, isEnable):
		self.interface.BINARY_SetObserverMode(isEnable)

	def BINARY_BettingGuildWar_UpdateObserverCount(self, observerCount):
		self.interface.wndMiniMap.UpdateObserverCount(observerCount)

	def __GuildWar_UpdateMemberCount(self, guildID1, memberCount1, guildID2, memberCount2, observerCount):
		guildID1 = int(guildID1)
		guildID2 = int(guildID2)
		memberCount1 = int(memberCount1)
		memberCount2 = int(memberCount2)
		observerCount = int(observerCount)

		self.interface.UpdateMemberCount(guildID1, memberCount1, guildID2, memberCount2)
		self.interface.wndMiniMap.UpdateObserverCount(observerCount)

	def __GuildWar_OpenAskDialog(self, guildID, warType):

		guildName = guild.GetGuildName(guildID)

		# REMOVED_GUILD_BUG_FIX
		if "Noname" == guildName:
			return
		# END_OF_REMOVED_GUILD_BUG_FIX

		import uiGuild
		questionDialog = uiGuild.AcceptGuildWarDialog()
		questionDialog.SAFE_SetAcceptEvent(self.__GuildWar_OnAccept)
		questionDialog.SAFE_SetCancelEvent(self.__GuildWar_OnDecline)
		questionDialog.Open(guildName, warType)

		self.guildWarQuestionDialog = questionDialog

	def __GuildWar_CloseAskDialog(self):
		self.guildWarQuestionDialog.Close()
		self.guildWarQuestionDialog = None

	def __GuildWar_OnAccept(self):

		guildName = self.guildWarQuestionDialog.GetGuildName()

		net.SendChatPacket("/war " + guildName)
		self.__GuildWar_CloseAskDialog()

		return 1

	def __GuildWar_OnDecline(self):

		guildName = self.guildWarQuestionDialog.GetGuildName()

		net.SendChatPacket("/nowar " + guildName)
		self.__GuildWar_CloseAskDialog()

		return 1
	
	## BINARY CALLBACK
	######################################################################################

	def __ServerCommand_Build(self):
		serverCommandList={
			"SetTeamOnline" 			: self.__TeamLogin,
			"SetTeamOffline" 			: self.__TeamLogout,
			"DayMode"					: self.__DayMode_Update,
			"PRESERVE_DayMode"			: self.__PRESERVE_DayMode_Update,
			"CloseRestartWindow"		: self.__RestartDialog_Close,
			"OpenPrivateShop"			: self.__PrivateShop_Open,
			"PartyHealReady"			: self.PartyHealReady,
			"ShowMeSafeboxPassword"		: self.AskSafeboxPassword,
			"CloseSafebox"				: self.CommandCloseSafebox,
			"CloseMall"					: self.CommandCloseMall,
			"ShowMeMallPassword"		: self.AskMallPassword,
			"item_mall"					: self.__ItemMall_Open,			
			"RefineSuceeded"			: self.RefineSuceededMessage,
			"RefineFailed"				: self.RefineFailedMessage,
			"xmas_snow"					: self.__XMasSnow_Enable,
			"xmas_boom"					: self.__XMasBoom_Enable,
			"xmas_song"					: self.__XMasSong_Enable,
			"xmas_tree"					: self.__XMasTree_Enable,
			"newyear_boom"				: self.__XMasBoom_Enable,
			"PartyRequest"				: self.__PartyRequestQuestion,
			"PartyRequestDenied"		: self.__PartyRequestDenied,
			"horse_state"				: self.__Horse_UpdateState,
			"hide_horse_state"			: self.__Horse_HideState,
			"WarUC"						: self.__GuildWar_UpdateMemberCount,
			"test_server"				: self.__EnableTestServerFlag,
			"lover_login"				: self.__LoginLover,
			"lover_logout"				: self.__LogoutLover,
			"lover_near"				: self.__LoverNear,
			"lover_far"					: self.__LoverFar,
			"lover_divorce"				: self.__LoverDivorce,
			"WheelFrightSpin"			: self.__WheelOfFright,
			"LetterItem"				: self.ReceiveLetterItem,
			"LetterDropItem"			: self.ReceiveLetterDropItem,
			"OpenRingWindow"			: self.BINARY_OpenRingWindow,
			"SetPartHideCostume"		: self.SetPartHideCostume,
			"ReceiveItemDrop"			: self.OnReceiveItemDrop,
			"SET_DUNGEON_OBIECTIVE"		: self.SetDungeonObjective,
			"SetPassiveSkill"			: self.__PassiveSkill,
			"CompanionMaxExp"			: self.__NextExpCompanion,
			"SetCompanion"				: self.__SetCompanion,
			"IrMaterial"				: self.__InfoRefineMaterial,
			"IrCost"					: self.__InfoRefineCost,			
			"SELECT_JOB" 				: self.SelectJob,
			"MyShopPriceList"			: self.__PrivateShop_PriceList,
			"write_notice_info"			: self.__write_notice_info,
			"SpecialCard_AddItem"		: self.SpecialCard_AddItem,
			"SpecialCard_Open"			: self.SpecialCard_Open,
			"BINARY_Update_Mast_HP"		: self.BINARY_Update_Mast_HP,
			"BINARY_Update_Mast_Window"	: self.BINARY_Update_Mast_Window,
			"battle_pass_mission"		: self.BattlePassMission,
			"battle_pass_reward"		: self.BattlePassReward,
			"battle_pass_final"			: self.BattlePassFinalReward,
			"SetQuestTimer"				: self.SetQuestTimer,
			"battle_pass"				: self.BattlePassStatus,
		}
		if app.ENABLE_REWARD_SYSTEM:
			serverCommandList.update({"RewardInfo" : self.SetRewardPlayers})
			
		if app.ENABLE_PREMIUM_SYSTEM:
			serverCommandList["SetPremiumStatus"] = self.SetPremiumStatus
			
		if constInfo.ENABLE_PASSIVE_SKILLS_HELPER:
			serverCommandList["SkillsManager_ClearInterface"] = self.__SKILLS_MANAGER__ClearInterface
			serverCommandList["SkillsManager_RegisterInformation"] = self.__SKILLS_MANAGER__RegisterInformation

		self.serverCommander=stringCommander.Analyzer()
		
		if app.ENABLE_SWITCHBOT_WORLDARD:
			serverCommandList["SWITCHBOT_SUCCEFULL"]			= self.BINARY_SWITCHBOT_SUCCEFULL

		if app.ENABLE_SEARCH_SHOP:
			serverCommandList["RefreshSearchShop"] = self.RefreshSearchShop
		
		for serverCommandItem in serverCommandList.items():
			self.serverCommander.SAFE_RegisterCallBack(serverCommandItem[0], serverCommandItem[1])

	def BINARY_ServerCommand_Run(self, line):
		try:
			return self.serverCommander.Run(line)
		except RuntimeError, msg:
			dbg.TraceError(msg)
			return 0

	def __ProcessPreservedServerCommand(self):
		try:
			command = net.GetPreservedServerCommand()
			while command:
				print " __ProcessPreservedServerCommand", command
				self.serverCommander.Run(command)
				command = net.GetPreservedServerCommand()
		except RuntimeError, msg:
			dbg.TraceError(msg)
			return 0

	def PartyHealReady(self):
		self.interface.PartyHealReady()
		
	if app.ENABLE_PREMIUM_SYSTEM:
		def SetPremiumStatus(self, type, timeLeft, affect1, affect2):
			if self.affectShower:
				if app.ENABLE_PREMIUM_SYSTEM_EXTRA:
					self.affectShower.SetPremiumStatus(int(type), int(timeLeft), int(affect1), int(affect2))
				else:
					self.affectShower.SetPremiumStatus(int(type), int(timeLeft))

	def BattlePassMission(self, iType, iVnum, pCount, iCount):
		self.interface.BattlePassMission(int(iType), int(iVnum), int(pCount), int(iCount))

	def BattlePassReward(self, iType, iVnum, iVnumReward, iCountReward):
		self.interface.BattlePassReward(int(iType), int(iVnum), int(iVnumReward), int(iCountReward))
		
	def BattlePassFinalReward(self, iVnum, iCount):
		self.interface.BattlePassFinal(int(iVnum), int(iCount))

	def AskSafeboxPassword(self):
		self.interface.AskSafeboxPassword()

	def AskMallPassword(self):
		self.interface.AskMallPassword()

	def __ItemMall_Open(self):
		self.interface.OpenItemMall();

	def CommandCloseMall(self):
		self.interface.CommandCloseMall()

	def RefineSuceededMessage(self):
		self.PopupMessage(localeInfo.REFINE_SUCCESS)
		self.interface.CheckRefineDialog(False)

	def RefineFailedMessage(self):
		self.PopupMessage(localeInfo.REFINE_FAILURE)
		self.interface.CheckRefineDialog(True)

	def CommandCloseSafebox(self):
		self.interface.CommandCloseSafebox()

	def __PrivateShop_PriceList(self, itemVNum, itemPrice):
		uiPrivateShopBuilder.SetPrivateShopItemPrice(itemVNum, itemPrice)

	def __Horse_HideState(self):
		self.affectShower.SetHorseState(0, 0, 0)

	def __Horse_UpdateState(self, level, health, battery):
		self.affectShower.SetHorseState(int(level), int(health), int(battery))

	def __IsXMasMap(self):
		mapDict = ( "metin2_map_n_flame_01",
					"metin2_map_n_desert_01",
					"metin2_map_spiderdungeon",
					"metin2_map_deviltower1", )

		if background.GetCurrentMapName() in mapDict:
			return False

		return True
		
	def __XMasSnow_Enable(self, mode):

		self.__XMasSong_Enable(mode)

		if "1"==mode:

			if not self.__IsXMasMap():
				return

			print "XMAS_SNOW ON"
			background.EnableSnow(1)

		else:
			print "XMAS_SNOW OFF"
			background.EnableSnow(0)

	def __XMasBoom_Enable(self, mode):
		if "1"==mode:

			if not self.__IsXMasMap():
				return

			print "XMAS_BOOM ON"
			self.__DayMode_Update("dark")
			self.enableXMasBoom = True
			self.startTimeXMasBoom = app.GetTime()
		else:
			print "XMAS_BOOM OFF"
			self.__DayMode_Update("light")
			self.enableXMasBoom = False

	def __XMasTree_Enable(self, grade):

		print "XMAS_TREE ", grade
		background.SetXMasTree(int(grade))

	def __XMasSong_Enable(self, mode):
		if "1"==mode:
			print "XMAS_SONG ON"
		else:
			print "XMAS_SONG OFF"

	def __RestartDialog_Close(self):
		self.interface.CloseRestartDialog()

	def __PrivateShop_Open(self):
		self.interface.OpenPrivateShopBuilderNoDialog()

	def BINARY_PrivateShop_Appear(self, vid, text):
		self.interface.AppearPrivateShop(vid, text)

	def BINARY_PrivateShop_Disappear(self, vid):
		self.interface.DisappearPrivateShop(vid)

	def __PRESERVE_DayMode_Update(self, mode):
		if "light"==mode:
			background.SetEnvironmentData(0)
		elif "dark"==mode:

			if not self.__IsXMasMap():
				return

			background.RegisterEnvironmentData(1, constInfo.ENVIRONMENT_NIGHT)
			background.SetEnvironmentData(1)

	def __DayMode_Update(self, mode):
		if "light"==mode:
			self.curtain.SAFE_FadeOut(self.__DayMode_OnCompleteChangeToLight)
		elif "dark"==mode:

			if not self.__IsXMasMap():
				return

			self.curtain.SAFE_FadeOut(self.__DayMode_OnCompleteChangeToDark)

	def __DayMode_OnCompleteChangeToLight(self):
		background.SetEnvironmentData(0)
		self.curtain.FadeIn()

	def __DayMode_OnCompleteChangeToDark(self):
		background.RegisterEnvironmentData(1, constInfo.ENVIRONMENT_NIGHT)
		background.SetEnvironmentData(1)
		self.curtain.FadeIn()

	def __XMasBoom_Update(self):

		self.BOOM_DATA_LIST = ( (2, 5), (5, 2), (7, 3), (10, 3), (20, 5) )
		if self.indexXMasBoom >= len(self.BOOM_DATA_LIST):
			return

		boomTime = self.BOOM_DATA_LIST[self.indexXMasBoom][0]
		boomCount = self.BOOM_DATA_LIST[self.indexXMasBoom][1]

		if app.GetTime() - self.startTimeXMasBoom > boomTime:

			self.indexXMasBoom += 1

			for i in xrange(boomCount):
				self.__XMasBoom_Boom()

	def __XMasBoom_Boom(self):
		x, y, z = player.GetMainCharacterPosition()
		randX = app.GetRandom(-150, 150)
		randY = app.GetRandom(-150, 150)		

	def __PartyRequestQuestion(self, vid):
		vid = int(vid)
		partyRequestQuestionDialog = uiCommon.QuestionDialog()
		partyRequestQuestionDialog.SetText(chr.GetNameByVID(vid) + localeInfo.PARTY_DO_YOU_ACCEPT)
		partyRequestQuestionDialog.SetAcceptText(localeInfo.UI_ACCEPT)
		partyRequestQuestionDialog.SetCancelText(localeInfo.UI_DENY)
		partyRequestQuestionDialog.SetAcceptEvent(lambda arg=True: self.__AnswerPartyRequest(arg))
		partyRequestQuestionDialog.SetCancelEvent(lambda arg=False: self.__AnswerPartyRequest(arg))
		partyRequestQuestionDialog.Open()
		partyRequestQuestionDialog.vid = vid
		self.partyRequestQuestionDialog = partyRequestQuestionDialog

	def __AnswerPartyRequest(self, answer):
		if not self.partyRequestQuestionDialog:
			return

		vid = self.partyRequestQuestionDialog.vid

		if answer:
			net.SendChatPacket("/party_request_accept " + str(vid))
		else:
			net.SendChatPacket("/party_request_deny " + str(vid))

		self.partyRequestQuestionDialog.Close()
		self.partyRequestQuestionDialog = None

	def __PartyRequestDenied(self):
		self.PopupMessage(localeInfo.PARTY_REQUEST_DENIED)

	def __EnableTestServerFlag(self):
		app.EnableTestServerFlag()

	def __LoginLover(self):
		if self.interface.wndMessenger:
			self.interface.wndMessenger.OnLoginLover()

	def __LogoutLover(self):
		if self.interface.wndMessenger:
			self.interface.wndMessenger.OnLogoutLover()
			
		if self.affectShower:
			self.affectShower.HideLoverState()

	def __LoverNear(self):
		if self.affectShower:
			self.affectShower.ShowLoverState()

	def __LoverFar(self):
		if self.affectShower:
			self.affectShower.HideLoverState()

	def __LoverDivorce(self):
		if self.interface.wndMessenger:
			self.interface.wndMessenger.ClearLoverInfo()
			
		if self.affectShower:
			self.affectShower.ClearLoverState()

	if app.ENABLE_CHANGELOOK_SYSTEM:
		def ActChangeLook(self, iAct):
			if self.interface:
				self.interface.ActChangeLook(iAct)

		def AlertChangeLook(self):
			self.PopupMessage(localeInfo.CHANGE_LOOK_DEL_ITEM)

	def __TeamLogin(self, name):
		if self.interface.wndMessenger:
			self.interface.wndMessenger.OnLogin(2, name)
			chat.AppendChat(1, "I'm online admin %s" % name)
			
	def __TeamLogout(self, name):
		if self.interface.wndMessenger:
			self.interface.wndMessenger.OnLogout(2, name)
			chat.AppendChat(1, "I'm offline admin %s" % name)

	def SelectJob(self, cmd):
		# import uinewskills
		import uiselectskill
		cmd = cmd.split('#')	
		if cmd[0] == 'QID':
			constInfo.SelectJob['QID'] = int(cmd[1])
		elif cmd[0] == 'INPUT':
			constInfo.INPUT_IGNORE = int(cmd[1])
		elif cmd[0] == 'SEND':
			net.SendQuestInputStringPacket(str(constInfo.SelectJob['QCMD']))
			constInfo.SelectJob['QCMD'] = ''
		elif cmd[0] == 'OPEN':
			self.job_select = uiselectskill.SelectSkill()
			self.job_select.Show()	
		elif cmd[0] == 'CLOSE':
			self.job_select = uiselectskill.SelectSkill()
			self.job_select.RealClose()

	if app.ENABLE_INVENTORY_VIEWER:
		def BINARY_InventoryViewerAddItem(self, pageIndex, slotIndex, itemVnum, itemCount):
			if self.interface:
				self.interface.InventoryViewerAddItem(pageIndex, slotIndex, itemVnum, itemCount)

		def BINARY_InventoryViewerAddSocket(self, pageIndex, slotIndex, socketIndex, socketValue):
			if self.interface:
				self.interface.InventoryViewerAddSocket(pageIndex, slotIndex, socketIndex, socketValue)

		def BINARY_InventoryViewerAddAttr(self, pageIndex, slotIndex, attrIndex, attrType, attrValue):
			if self.interface:
				self.interface.InventoryViewerAddAttr(pageIndex, slotIndex, attrIndex, attrType, attrValue)

		def BINARY_OpenInventoryViewer(self, chrVid):
			if self.interface:
				self.interface.OpenInventoryViewerWindow(chrVid)

		if app.ENABLE_CHANGELOOK_SYSTEM:
			def BINARY_InventoryViewerAddTransmutation(self, pageIndex, slotIndex, transmutation):
				if self.interface:
					self.interface.InventoryViewerAddTransmutation(pageIndex, slotIndex, transmutation)

	def __write_notice_info(self, text):
		self.interface.RegisterGameMasterName("Etherion2")
		self.OnRecvWhisper(chat.WHISPER_TYPE_CHAT, "Etherion2", text.replace("_", " "), "ro")

	if app.ENABLE_SHOW_CHEST_DROP:
		def BINARY_AddChestDropInfo(self, chestVnum, dropChance, slotIndex, itemVnum, itemCount):
			if self.interface:
				self.interface.AddChestDropInfo(chestVnum, dropChance, slotIndex, itemVnum, itemCount)

		def BINARY_RefreshChestDropInfo(self, chestVnum):
			if self.interface:
				self.interface.RefreshChestDropInfo(chestVnum)

	if app.ENABLE_SEND_TARGET_INFO:
		def BINARY_AddTargetMonsterDropInfo(self, raceNum, itemVnum, itemCount, iChance):
			if not raceNum in constInfo.MONSTER_INFO_DATA:
				constInfo.MONSTER_INFO_DATA.update({raceNum : {}})
				constInfo.MONSTER_INFO_DATA[raceNum].update({"items" : []})
			curList = constInfo.MONSTER_INFO_DATA[raceNum]["items"]

			isUpgradeable = False
			isMetin = False
			item.SelectItem(itemVnum)
			if item.GetItemType() == item.ITEM_TYPE_WEAPON or item.GetItemType() == item.ITEM_TYPE_ARMOR:
				isUpgradeable = True
			elif item.GetItemType() == item.ITEM_TYPE_METIN:
				isMetin = True

			for curItem in curList:
				if isUpgradeable:
					if curItem.has_key("vnum_list") and curItem["vnum_list"][0] / 10 * 10 == itemVnum / 10 * 10:
						if not (itemVnum in curItem["vnum_list"]):
							curItem["vnum_list"].append(itemVnum)
						return
				elif isMetin:
					if curItem.has_key("vnum_list"):
						baseVnum = curItem["vnum_list"][0]
					if curItem.has_key("vnum_list") and (baseVnum - baseVnum%1000) == (itemVnum - itemVnum%1000):
						if not (itemVnum in curItem["vnum_list"]):
							curItem["vnum_list"].append(itemVnum)
						return
				else:
					if curItem.has_key("vnum") and curItem["vnum"] == itemVnum and curItem["count"] == itemCount and curItem["chance"] == iChance:
						return

			if isUpgradeable or isMetin:
				curList.append({"vnum_list":[itemVnum], "count":itemCount, "chance":iChance})
			else:
				curList.append({"vnum":itemVnum, "count":itemCount, "chance":iChance})

		def BINARY_RefreshTargetMonsterDropInfo(self, raceNum):
			self.targetBoard.RefreshMonsterInfoBoard()

	if app.ENABLE_SASH_SYSTEM:
		def ActSash(self, iAct, bWindow):
			if self.interface:
				self.interface.ActSash(iAct, bWindow)

		def AlertSash(self, bWindow):
			if bWindow:
				self.PopupMessage(localeInfo.SASH_DEL_SERVEITEM)
			else:
				self.PopupMessage(localeInfo.SASH_DEL_ABSORDITEM)

	#OFFLINE_SHOP
	def RefreshPrivShop(self):
		pass
		
	def	ShowOfflineShopWindow(self):
		pass

	def SetSHOPTargetBoard(self, vid, name):
		pass

	def BINARY_APPEND_WIKI_CLEAR(self):
		pass
		# self.PythonLive.ClearList()

	def BINARY_APPEND_WIKI_REFINE(self, EndIndex, vnum, refine):
		if self.interface and self.interface.dlgRefineNew:
			self.interface.dlgRefineNew.AppendWikiInfo(EndIndex, vnum, refine)

	def __InfoRefineMaterial(self, ItemVnum, MaterialVnum, MaterialCount):
		pass

	def __InfoRefineCost(self, ItemVnum, Cost):
		pass
		
	def OpenCompanionWindow(self):
		if self.wndCompanion:
			if self.wndCompanion.IsShow():
				self.wndCompanion.Hide()
			else:
				self.wndCompanion.Show()

	def __NextExpCompanion(self, dwNextExp):
		self.wndCompanion.SetNextExp(int(dwNextExp))

	def __SetCompanion(self, dwInvPos):
		if self.wndCompanion:
			self.wndCompanion.SetInventoryPet(int(dwInvPos))
			if int(dwInvPos) == -1:
				self.wndCompanion.wndInfoCompanion.Hide()
	
		constInfo.COMPANION_ACTIVE_POS = int(dwInvPos)
		if self.interface:
			self.interface.RefreshInventory()
			
	def BINARY_DragonSoulGiveQuilification(self):
		self.interface.DragonSoulGiveQuilification()
		
	def BINARY_DragonSoulRefineWindow_Open(self):
		self.interface.OpenDragonSoulRefineWindow()

	def BINARY_DragonSoulRefineWindow_RefineFail(self, reason, inven_type, inven_pos):
		self.interface.FailDragonSoulRefine(reason, inven_type, inven_pos)

	def BINARY_DragonSoulRefineWindow_RefineSucceed(self, inven_type, inven_pos):
		self.interface.SucceedDragonSoulRefine(inven_type, inven_pos)

	def BINARY_BIOLOG_BONUS(self, Index, Type, Value):
		self.interface.AppendInfoBiologBonus(Index, Type, Value)

	def BINARY_BIOLOG_TIME(self, timeLeft, maxTime):
		self.interface.AppendInfoBiologTime(timeLeft - app.GetGlobalTimeStamp(), maxTime)	

	def BINARY_BIOLOG(self, iRewardVnum, vnum, actualCount, needCount):
		self.interface.AppendInfoBiolog(iRewardVnum, vnum, actualCount, needCount)

	# GAYA
	def ClearGaya(self):
		self.interface.ClearGaya()

	def BINARY_GAYA_ITEM_POS(self, pos, dwVnumReward, bCountReward, dwVnumPrice, iCountNeed, bType):
		self.interface.AddGayaItem(pos, dwVnumReward, bCountReward, dwVnumPrice, iCountNeed, bType)

	def BINARY_SET_GAYA(self, race):
		self.interface.SetGaya(race)

	# END_OF_GAYA

	if app.ENABLE_SWITCHBOT_WORLDARD:
		def BINARY_SWITCHBOT_OPEN(self):
			self.interface.BINARY_SWITCHBOT_OPEN()
			
		def BINARY_SWITCHBOT_CLEAR_INFO(self):
			self.interface.BINARY_SWITCHBOT_CLEAR_INFO()

		def BINARY_SWITCHBOT_INFO_BONUS(self,id_bonus,bonus_value_0,bonus_value_1,bonus_value_2,bonus_value_3,bonus_value_4):
			self.interface.BINARY_SWITCHBOT_INFO_BONUS(id_bonus,bonus_value_0,bonus_value_1,bonus_value_2,bonus_value_3,bonus_value_4)

		def BINARY_SWITCHBOT_INFO_EXTRA(self):
			self.interface.BINARY_SWITCHBOT_INFO_EXTRA()

		def BINARY_SWITCHBOT_SUCCEFULL(self,count):
			self.PopupMessage(localeInfo.SWITCHBOT_TEXT_14 % (int(count)))

	def BINARY_SINFO_MOB(self, page, index, mob, vnum, count):
		if self.interface:
			self.interface.SetMobInfo(page, index, mob, vnum, count)

	def __GetServerID(self):
		serverID = 1
		for i in serverInfo.REGION_DICT[0].keys():
			if serverInfo.REGION_DICT[0][i]["name"] == net.GetServerInfo().split(",")[0]:
				serverID = int(i)
				break

		return serverID

	def RefreshChannel(self, channel):# I MARE
		channelName = ""
		serverName = serverInfo.REGION_DICT[0][self.__GetServerID()]["name"]
		if channel in serverInfo.REGION_DICT[0][self.__GetServerID()]["channel"]:
			channelName = serverInfo.REGION_DICT[0][self.__GetServerID()]["channel"][int(channel)]["name"]
		elif channel == 99:
			channelName = "Special CH"
		else:
			channelName = "Unknow CH"
			
		net.SetServerInfo("%s, %s" % (serverName, channelName))
		if self.interface:
			self.interface.wndMiniMap.serverInfo.SetText(net.GetServerInfo())
			
	# NEW_SKILL_PASSIVE
	def __PassiveSkill(self, skill, level):
		constInfo.PASSIVE_SKILL_LV[int(skill) - 1] = int(level)
		if self.interface:
			if self.interface.wndCharacter:
				self.interface.wndCharacter.RefreshSkill()

	def BINARY_RANK_APPEND(self, mode, my_pos, pos, name, value, empire):
		self.interface.AppendInfoRankGlobal(mode, my_pos, pos, name, value, empire)
		# chat.AppendChat(1, "Mod %d PosMe %d Pos %d Name %s Val %d Empire %d" % (mode, my_pos, pos, name, value, empire))

	def BINARY_Highlight_Item(self, inven_type, inven_pos):
		if self.interface:
			self.interface.Highligt_Item(inven_type, inven_pos)
		# pass
			
	def SetDungeonObjective(self, Objective, TimeLeft):
		Objective = Objective.replace("_", " ")
	
		if self.DungeonTimer:
			self.DungeonTimer.SetNotify(str(Objective), int(TimeLeft))
			self.Show()

	# if app.ENABLE_DEFENSE_WAVE:
	def BINARY_Update_Mast_HP(self, hp):
		self.interface.BINARY_Update_Mast_HP(int(hp))

	def BINARY_Update_Mast_Window(self, i):
		selfs.interface.BINARY_Update_Mast_Window(int(i))
		
	# HIDE_COSTUME
	
	def SetPartHideCostume(self, index, status):
		if self.interface:
			self.interface.SetHideCostumePart(int(index), int(status))
	
	# END_OF_HIDE_COSTUME
	
	def __WheelOfFright(self, Spin, Prizes):
		if self.interface:
			self.interface.SpinWheelOfFright(int(Spin), Prizes)
	
	def ReceiveLetterItem(self, index, vnum, count):
		if self.interface:
			self.interface.SetLetterItem(int(index), int(vnum), int(count))
	
	def ReceiveLetterDropItem(self, index, vnum, count):
		if self.interface:
			self.interface.SetLetterDropItem(int(index), int(vnum), int(count))
	
	def BINARY_OpenRingWindow(self):
		if self.interface:
			self.interface.OpenTabMap()
		
	def SpecialCard_AddItem(self, itemVnum):
		self.SpecialCard.AddItem(itemVnum)

	def SpecialCard_Open(self):
		self.SpecialCard.Open()
		
	def BattlePassStatus(self, status):
		if int(status) != 1:
			self.interface.wndBattlePass.ToggleTip()
		
	def SetQuestTimer(self, index, time):
		if time > 0:
			self.interface.wndDungeonInfo.SendInfos(int(index), int(time))

	def BotLogin(self, name):
		if self.interface.wndMessenger:
			self.interface.wndMessenger.OnLogin(3, name)
			
	if app.ENABLE_OFFLINE_SHOP:
		def UpdateShopGold(self, gold):
			self.interface.UpdateShopGold(gold)
			
		def UpdateShopLock(self, lock):
			self.interface.UpdateShopLock(lock)
		
		def UpdateShopTime(self, time):
			self.interface.UpdateShopTime(time)
		
		def UpdateShopSign(self, sign):
			# self.interface.UpdateShopSign(sign)
			pass
		
		def OpenOfflineShop(self, sign, channel, index, x, y, time, update):
			self.interface.OpenOfflineShop(sign, channel, index, x, y, time, update)
			
	if app.ENABLE_SEARCH_SHOP:
		def OpenSearchShop(self):
			self.interface.OpenSearchShop()
			
		def RefreshSearchShop(self):
			self.interface.RefreshSearchShop()
		
		def OpenPrivateMessage(self, name):
			self.interface.OpenWhisperDialog(name)
		
	if app.ENABLE_REWARD_SYSTEM:
		def SetRewardPlayers(self, data):
			self.interface.SetRewardPlayers(str(data))

	if app.ENABLE_EVENT_MANAGER:
		def ClearEventManager(self):
			self.interface.ClearEventManager()
			
		def RefreshEventManager(self):
			self.interface.RefreshEventManager()
			
		def RefreshEventStatus(self, eventID, eventStatus, eventendTime, eventEndTimeText):
			self.interface.RefreshEventStatus(int(eventID), int(eventStatus), int(eventendTime), str(eventEndTimeText))
			
		def AppendEvent(self, dayIndex, eventID, eventIndex, startTime, endTime, empireFlag, channelFlag, value0, value1, value2, value3, startRealTime, endRealTime, isAlreadyStart):
			self.interface.AppendEvent(int(dayIndex),int(eventID), int(eventIndex), str(startTime), str(endTime), int(empireFlag), int(channelFlag), int(value0), int(value1), int(value2), int(value3), int(startRealTime), int(endRealTime), int(isAlreadyStart))

	if constInfo.ENABLE_PASSIVE_SKILLS_HELPER:
		def __SKILLS_MANAGER__ClearInterface(self):
			constInfo.PASSIVE_SKILLS_DATA = {}

		def __SKILLS_MANAGER__RegisterInformation(self, iKey, iMaxLevel, iCurrent, iRequired):
			if int(iKey) not in constInfo.PASSIVE_SKILLS_DATA:
				constInfo.PASSIVE_SKILLS_DATA[int(iKey)] = {}

			constInfo.PASSIVE_SKILLS_DATA[int(iKey)] = { "MaxLv" : int(iMaxLevel), "Curr" : int(iCurrent), "Req" : int(iRequired) }

	if app.ENABLE_MAINTENANCE_SYSTEM:
		def BINARY_ShowMaintenanceSign(self, timeLeft, duration):
			self.interface.ShowMaintenanceSign(timeLeft, duration)

		def BINARY_HideMaintenanceSign(self):
			self.interface.HideMaintenanceSign()
			