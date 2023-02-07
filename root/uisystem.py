import net
import app
import thenewui as ui
import CacheEffect as player
import uiSystemOption
import uiGameOption
import uiScriptLocale
import networkModule
import constInfo
import localeInfo
import shop
import time
import uiShop

import chat,serverInfo,net,ServerStateChecker
CHANNELS = 4 #Change Number With Your Max.CH (For Switch Channel)

class SystemDialog(ui.ScriptWindow):

	def __init__(self):
		ui.ScriptWindow.__init__(self)
		self.__Initialize()

	def __Initialize(self):
		self.gameOptionDlg = None
		self.moveChannelDlg = None
		self.interface = None

	def LoadDialog(self):
		self.__LoadSystemMenu_Default()

	def __LoadSystemMenu_Default(self):
		pyScrLoader = ui.PythonScriptLoader()
		pyScrLoader.LoadScriptFile(self, "uiscript/SystemDialog.py")

		self.GetChild("system_option_button").SAFE_SetEvent(self.__ClickGameOptionButton)
		self.GetChild("change_button").SAFE_SetEvent(self.__ClickChangeCharacterButton)
		self.GetChild("logout_button").SAFE_SetEvent(self.__ClickLogOutButton)
		self.GetChild("exit_button").SAFE_SetEvent(self.__ClickExitButton)
		self.GetChild("cancel_button").SAFE_SetEvent(self.Close)
		self.GetChild("change_ch_button").SAFE_SetEvent(self.__ClickMoveChannel)
		self.GetChild("wikipedia_button").SAFE_SetEvent(self.__ClickOpenWikipedia)

	def BindInterface(self, event):
		self.interface = event
		
	def Destroy(self):
		self.ClearDictionary()

		if self.gameOptionDlg:
			self.gameOptionDlg.Destroy()
			
		if self.moveChannelDlg:
			self.moveChannelDlg.Destroy()

		self.__Initialize()

	def OpenDialog(self):
		self.Show()

	def __ClickChangeCharacterButton(self):
		self.Close()

		net.ExitGame()

	def __ClickOpenWikipedia(self):
		self.Close()

		if self.interface:
			self.interface.ShowWiki()
			
	def __ClickMoveChannel(self):
		self.Close()
		if not self.moveChannelDlg:
			self.moveChannelDlg = MoveChannelWindow()
	
		self.moveChannelDlg.Show()

	def __OnClosePopupDialog(self):
		self.popup = None

	def __ClickLogOutButton(self):
		self.Close()
		net.LogOutGame()

	def __ClickExitButton(self):
		self.Close()
		if player.IsGM():
			app.Exit()
		else:
			net.ExitApplication()

	def __ClickGameOptionButton(self):
		self.Close()

		if not self.gameOptionDlg:
			self.gameOptionDlg = uiGameOption.OptionDialog()

		self.gameOptionDlg.Show()

	def Close(self):
		self.Hide()
		return True
			
	def OnBlockMode(self, mode):
		uiGameOption.blockMode = mode
		if self.gameOptionDlg:
			self.gameOptionDlg.OnBlockMode(mode)

	def OnChangePKMode(self):
		if self.gameOptionDlg:
			self.gameOptionDlg.OnChangePKMode()

	def OnPressExitKey(self):
		self.Close()
		return True

	def OnPressEscapeKey(self):
		self.Close()
		return True
		
class MoveChannelWindow(ui.ScriptWindow):
	def __init__(self):
		ui.ScriptWindow.__init__(self)
		self.titleBar = None
		ServerStateChecker.Create(self)
		self.channelButtonList = []
		self.currentChannel = 0
		self.__LoadBoard()
		self.RefreshChannelButtons()
		self.Show()
		self.SetCenterPosition()
		self.__RequestServerStateList()

	def __del__(self):
		ui.ScriptWindow.__del__(self)

	def __LoadBoard(self):
		try:
			pyScrLoader = ui.PythonScriptLoader()
			pyScrLoader.LoadScriptFile(self, "uiscript/movechanneldialog.py")
		except:
			import exception
			exception.Abort("MoveChannelWindow.__LoadBoard.LoadScript")

		try:
			self.board = self.GetChild("MoveChannelBoard")
			self.titleBar = self.GetChild("MoveChannelTitle")
			# self.thinboard = self.GetChild("BoardThin")
			self.blackBoard = self.GetChild("BlackBoard")
			self.okButton = self.GetChild("AcceptButton")
			self.cancelButton = self.GetChild("CancelButton")
		except:
			import exception
			exception.Abort("MoveChannelWindow.__LoadBoard.BindObject")

		self.titleBar.SetCloseEvent(ui.__mem_func__(self.Close))
		self.okButton.SetEvent(ui.__mem_func__(self.ChangeChannel))
		self.cancelButton.SetEvent(ui.__mem_func__(self.Close))
		self.SetCurentChannel()
		self.AddChannels()
		
	def SetCurentChannel(self):
		try:
			self.currentChannel = int( int(net.GetServerInfo().split(",")[1][-1:]) - 1 )
		except:
			return
		
	def __GetServerID(self):
		serverID = 0
		for i in serverInfo.REGION_DICT[0].keys():
			if serverInfo.REGION_DICT[0][i]["name"] == net.GetServerInfo().split(",")[0]:
				serverID = int(i)
				break
				
		return serverID
	
	def __RequestServerStateList(self):
		try:
			channelDict = serverInfo.REGION_DICT[0][self.__GetServerID()]["channel"]
		except:
			return
		
		ServerStateChecker.Initialize(self)
		for id, channelDataDict in channelDict.items():
			key = channelDataDict["key"]
			ip = channelDataDict["ip"]
			udp_port = channelDataDict["udp_port"]
			ServerStateChecker.AddChannel(key, ip, udp_port)
		
		ServerStateChecker.Request()

	def NotifyChannelState(self, addrKey, state):
		try:
			stateName = serverInfo.STATE_DICT[state]
		except:
			stateName = serverInfo.STATE_NONE
		
		regionID  = int(addrKey / 1000)
		serverID  = int(addrKey / 10) % 100
		channelID = addrKey % 10
		try:
			serverInfo.REGION_DICT[regionID][serverID]["channel"][channelID]["state"] = stateName
			self.__RefreshChannelStateList()
		except:
			pass

	def AddChannels(self):				
		self.SetSize(190,80+30*CHANNELS)
		self.board.SetSize(190,80+30*CHANNELS)
		# self.thinboard.SetSize(175, (41*CHANNELS) - 2)
		self.blackBoard.SetSize(163,7+30*CHANNELS)
		
		for i in xrange(CHANNELS):
			self.channelButtonList.append(ui.MakeRadioButton(self.blackBoard, 7, 7+30*i, "d:/ymir work/ui/switchbot/", "btn_big_03.sub", "btn_big_02.sub", "btn_big_02.sub"))
			self.channelButtonList[i].SetText(str(serverInfo.REGION_DICT[0][self.__GetServerID()]["channel"][i+1]["name"]))
			self.channelButtonList[i].SetEvent(lambda arg=i: self.SelectChannel(arg))
			self.channelButtonList[i].Show()

	def SelectChannel(self,channel):
		self.currentChannel = channel
		self.RefreshChannelButtons()
				
	def RefreshChannelButtons(self):
		for i in xrange(CHANNELS):
			if i == self.currentChannel:
				self.channelButtonList[i].Down()
			else:
				self.channelButtonList[i].SetUp()
		
	def ChangeChannel(self):
		ServerStateChecker.Update()
		channelID = self.currentChannel+1
		channelState = serverInfo.REGION_DICT[0][self.__GetServerID()]["channel"][channelID]["state"]
		if not channelID:
			return
		
		if channelState == serverInfo.STATE_NONE or channelState == serverInfo.STATE_DICT[0]:
			chat.AppendChat(chat.CHAT_TYPE_INFO , "Acest canal este offline")
			return
			
		self.Close()
		net.SendChatPacket("/channel " + str(channelID))
				
	def Destroy(self):
		self.ClearDictionary()
		self.Hide()
		
	def Close(self):
		ServerStateChecker.Initialize(self)
		self.Hide()
		
	def OnUpdate(self):
		ServerStateChecker.Update()
		
	def OnPressEscapeKey(self):
		self.Close()
		return True
