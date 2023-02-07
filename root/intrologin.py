import app
import net
import thenewui as ui
import wndMgr
import systemSetting
import localeInfo
import constInfo
import ime
import uiScriptLocale
import config
import ServerStateChecker
import os
import base64
import time
import binascii
import _winreg

REG_PATH = r"SOFTWARE\Deimos"
ACCOUNTS_NUMBER = 6
ACCOUNTS = [[uiScriptLocale.ACCOUNT_SAVED, uiScriptLocale.ACCOUNT_SAVED],[uiScriptLocale.ACCOUNT_SAVED, uiScriptLocale.ACCOUNT_SAVED],[uiScriptLocale.ACCOUNT_SAVED, uiScriptLocale.ACCOUNT_SAVED],[uiScriptLocale.ACCOUNT_SAVED, uiScriptLocale.ACCOUNT_SAVED],[uiScriptLocale.ACCOUNT_SAVED, uiScriptLocale.ACCOUNT_SAVED],[uiScriptLocale.ACCOUNT_SAVED, uiScriptLocale.ACCOUNT_SAVED]]

def set_reg(name, value):
	try:
		_winreg.CreateKey(_winreg.HKEY_CURRENT_USER, REG_PATH)
		registry_key = _winreg.OpenKey(_winreg.HKEY_CURRENT_USER, REG_PATH, 0, _winreg.KEY_WRITE)
		_winreg.SetValueEx(registry_key, name, 0, _winreg.REG_SZ, value)
		_winreg.CloseKey(registry_key)
		return True
	except WindowsError:
		return False

def get_reg(name):
	try:
		registry_key = _winreg.OpenKey(_winreg.HKEY_CURRENT_USER, REG_PATH, 0, _winreg.KEY_READ)
		value, regtype = _winreg.QueryValueEx(registry_key, name)
		_winreg.CloseKey(registry_key)
		return str(value)
	except WindowsError:
		return None	

def LoadAccounts():
	for i in xrange(ACCOUNTS_NUMBER):
		if get_reg("acc_%d" % i):
			ACCOUNTS[i][0] = get_reg("acc_%d" % i).split("|")[0]
			ACCOUNTS[i][1] = get_reg("acc_%d" % i).split("|")[1]
			
def SaveAccounts():	
	for i in xrange(ACCOUNTS_NUMBER):
		set_reg("acc_%d" % i, "%s|%s" % (ACCOUNTS[i][0], ACCOUNTS[i][1]))															

class ConnectingDialog(ui.ScriptWindow):

	def __init__(self):
		ui.ScriptWindow.__init__(self)
		self.__LoadDialog()
		self.eventTimeOver = lambda *arg: None
		self.eventExit = lambda *arg: None

	def __del__(self):
		ui.ScriptWindow.__del__(self)

	def __LoadDialog(self):
		try:
			PythonScriptLoader = ui.PythonScriptLoader()
			PythonScriptLoader.LoadScriptFile(self, "UIScript/ConnectingDialog.py")

			self.board = self.GetChild("board")
			self.message = self.GetChild("message")
			self.countdownMessage = self.GetChild("countdown_message")

		except:
			import exception
			exception.Abort("ConnectingDialog.LoadDialog.BindObject")

	def Open(self, waitTime):
		curTime = time.clock()
		self.endTime = curTime + waitTime

		self.Lock()
		self.SetCenterPosition()
		self.SetTop()
		self.Show()

	def Close(self):
		self.Unlock()
		self.Hide()

	def Destroy(self):
		self.Hide()
		self.ClearDictionary()

	def SetText(self, text):
		self.message.SetText(text)

	def SetCountDownMessage(self, waitTime):
		self.countdownMessage.SetText("%.0f%s" % (waitTime, localeInfo.SECOND))

	def SAFE_SetTimeOverEvent(self, event):
		self.eventTimeOver = ui.__mem_func__(event)

	def SAFE_SetExitEvent(self, event):
		self.eventExit = ui.__mem_func__(event)

	def OnUpdate(self):
		lastTime = max(0, self.endTime - time.clock())
		if 0 == lastTime:
			self.Close()
			self.eventTimeOver()
		else:
			self.SetCountDownMessage(self.endTime - time.clock())

	def OnPressExitKey(self):
		return True
		
class LoginWindow(ui.ScriptWindow):

	# IS_TEST = net.IsTest()

	def __init__(self, stream):
		ui.ScriptWindow.__init__(self)
		
		net.SetPhaseWindow(net.PHASE_WINDOW_LOGIN, self)
		net.SetAccountConnectorHandler(self)

		self.stream = stream
		self.channels = 0 
		self.channelButton = None
		self.panelButton = None

		self.try_login = 0
		
	def __del__(self):
		ui.ScriptWindow.__del__(self)
		
		net.ClearPhaseWindow(net.PHASE_WINDOW_LOGIN, self)
		net.SetAccountConnectorHandler(0)

	def Open(self):
		ServerStateChecker.Create(self)
		self.loginFailureMsgDict={

			"ALREADY"	: localeInfo.LOGIN_FAILURE_ALREAY,
			"NOID"		: localeInfo.LOGIN_FAILURE_NOT_EXIST_ID,
			"WRONGPWD"	: localeInfo.LOGIN_FAILURE_WRONG_PASSWORD,
			"FULL"		: localeInfo.LOGIN_FAILURE_TOO_MANY_USER,
			"SHUTDOWN"	: localeInfo.LOGIN_FAILURE_SHUTDOWN,
			"REPAIR"	: localeInfo.LOGIN_FAILURE_REPAIR_ID,
			"BLOCK"		: localeInfo.LOGIN_FAILURE_BLOCK_ID,
			"BESAMEKEY"	: localeInfo.LOGIN_FAILURE_BE_SAME_KEY,
			"NOTAVAIL"	: localeInfo.LOGIN_FAILURE_NOT_AVAIL,
			"NOBILL"	: localeInfo.LOGIN_FAILURE_NOBILL,
			"BLKLOGIN"	: localeInfo.LOGIN_FAILURE_BLOCK_LOGIN,
			"WEBBLK"	: localeInfo.LOGIN_FAILURE_WEB_BLOCK,
			"HWBANNED"		: "Esti liber sa alegi alt server.",
			"BRTFRC"		: "Ai depasit 5 logari eronate, asteapta 10 minute.",

		}

		self.loginFailureFuncDict = {
			"WRONGPWD"	: localeInfo.LOGIN_FAILURE_WRONG_PASSWORD,
			"QUIT"		: app.Exit,
		}

		self.SetSize(wndMgr.GetScreenWidth(), wndMgr.GetScreenHeight())
		self.SetWindowName("LoginWindow")

		self.__LoadScript("UIScript/LoginWindow.py")

		ime.AddExceptKey(91)
		ime.AddExceptKey(93)
		
		self.SetChannel("CH1")
		
		self.Show()
		app.ShowCursor()

	def Close(self):
		ServerStateChecker.Initialize(self)

		self.Hide()
		self.stream.popupWindow.Close()
		app.HideCursor()
		ime.ClearExceptKey()

	def SetPasswordEditLineFocus(self):
		if self.idEditLine != None:
			self.idEditLine.SetText("")
			self.idEditLine.SetFocus()

		if self.pwdEditLine != None:
			self.pwdEditLine.SetText("")
					
	def OnConnectFailure(self):
		self.PopupNotifyMessage(localeInfo.LOGIN_CONNECT_FAILURE, self.EmptyFunc)

	def OnHandShake(self):
		self.PopupDisplayMessage(localeInfo.LOGIN_CONNECT_SUCCESS)
		constInfo.ACCOUNT_NAME = str(self.idEditLine.GetText())

	def OnLoginStart(self):
		self.PopupDisplayMessage(localeInfo.LOGIN_PROCESSING)
		
	def OnLoginFailure(self, error):
		try:
			loginFailureMsg = self.loginFailureMsgDict[error]
		except KeyError:
		
			loginFailureMsg = localeInfo.LOGIN_FAILURE_UNKNOWN  + error

		loginFailureFunc = self.loginFailureFuncDict.get(error, self.EmptyFunc)

		self.PopupNotifyMessage(loginFailureMsg, loginFailureFunc)
		
		# self.loginButton.Enable()
		self.pwdEditLine.SetReturnEvent(ui.__mem_func__(self.__OnClickLoginButton))
		self.try_login = 0
		
	def __LoadScript(self, fileName):
		try:
			pyScrLoader = ui.PythonScriptLoader()
			pyScrLoader.LoadScriptFile(self, fileName)
		except:
			import exception
			exception.Abort("LoginWindow.__LoadScript.LoadObject")

		try:
			self.idEditLine = self.GetChild("ID_EditLine")
			self.pwdEditLine = self.GetChild("Password_EditLine")
			self.loginButton = self.GetChild("LoginButton")
			self.exitButton = self.GetChild("LoginExitButton")
			self.SaveAccountButton = self.GetChild("SaveAccountButton")
			self.LoginBoard = self.GetChild("LoginBoard")
			#mutli-lang
			self.regButton = self.GetChild("RegButton")
			self.commButton = self.GetChild("CommButton")
			
			self.channels_dict = []
			self.account_name_dict = []
			self.account_button_dict = []
			self.account_button_delete_dict = []
			for i in xrange(1,7):
				self.account_name_dict.append(self.GetChild("SlotLine%s_Text" % i))
				self.account_button_dict.append(self.GetChild("SlotLine%s_Button" % i))
				self.account_button_delete_dict.append(self.GetChild("SlotLine%s_Button_Delete" % i))
				
			# for i in xrange(1,7):
				self.channels_dict.append(self.GetChild("on_ch%s_img" % i))


				
			self.channelButton = {
				"CH1" : self.GetChild("Ch1Button"),
				"CH2" :	self.GetChild("Ch2Button"),
				"CH3" : self.GetChild("Ch3Button"),
				"CH4" : self.GetChild("Ch4Button"),
				"CH5" : self.GetChild("Ch5Button"),
				"CH6" : self.GetChild("Ch6Button")
				}

			for (channelID, channelButtons) in self.channelButton.items():
				channelButtons.SetEvent(ui.__mem_func__(self.SetChannel), channelID)
				
			for i in xrange(len(self.account_button_dict)):
				self.account_button_dict[i].SetEvent(ui.__mem_func__(self.ConnectOnAccount), i)
				
			for i in xrange(len(self.account_button_delete_dict)):
				self.account_button_delete_dict[i].Hide()
				self.account_button_delete_dict[i].SetEvent(ui.__mem_func__(self.DeleteAccount), i)
				
		except:
			import exception
			exception.Abort("LoginWindow.__LoadScript.BindObject")

		self.loginButton.SetEvent(ui.__mem_func__(self.__OnClickLoginButton))
		self.exitButton.SetEvent(ui.__mem_func__(self.OnPressExitKey))
		
		self.SaveAccountButton.SetEvent(ui.__mem_func__(self.SaveAccounts))
		self.regButton.SetEvent(ui.__mem_func__(self.registerFunc))
		self.commButton.SetEvent(ui.__mem_func__(self.commFunc))

		self.idEditLine.SetReturnEvent(ui.__mem_func__(self.pwdEditLine.SetFocus))
		self.idEditLine.SetTabEvent(ui.__mem_func__(self.pwdEditLine.SetFocus))
		self.pwdEditLine.SetReturnEvent(ui.__mem_func__(self.__OnClickLoginButton))
		self.pwdEditLine.SetTabEvent(ui.__mem_func__(self.idEditLine.SetFocus))
		self.idEditLine.SetFocus()
		
		try:
			self.LoadAccounts()
		except:
			import exception
			exception.Abort("Nu poate incarca lista cu conturi")
			
	def registerFunc(self):
		app.ExecuteShell("https://play.deimos2.net/users/register")

	def commFunc(self):
		app.ExecuteShell("https://discord.gg/deimos2")

	def SaveAccounts(self):
		global ACCOUNTS
		id = self.idEditLine.GetText()
		pwd = self.pwdEditLine.GetText()
		
		for i in xrange(len(ACCOUNTS)):
			if ACCOUNTS[i][0] == uiScriptLocale.ACCOUNT_SAVED and id != "" and pwd != "":
				ACCOUNTS[i][0] = id
				ACCOUNTS[i][1] = pwd
				SaveAccounts()
				self.LoadAccounts()
				break
			elif ACCOUNTS[i][0] == id:
				self.PopupDisplayMessage("Cont deja salvat.")
				break
				
	def DeleteAccount(self, nAccount):
		if str(ACCOUNTS[nAccount][0]) != uiScriptLocale.ACCOUNT_SAVED:
			ACCOUNTS[nAccount][0] = uiScriptLocale.ACCOUNT_SAVED
			ACCOUNTS[nAccount][1] = uiScriptLocale.ACCOUNT_SAVED
			SaveAccounts()
			
		for i in xrange(len(self.account_button_delete_dict)):
			self.account_button_delete_dict[i].Hide()
				
		self.LoadAccounts()
			
	def LoadAccounts(self):
		global ACCOUNTS
		LoadAccounts()	
		for i in xrange(len(self.account_name_dict)):
			self.account_name_dict[i].SetText(str(ACCOUNTS[i][0]))
			
		for i in xrange(len(self.account_button_delete_dict)):
			if ACCOUNTS[i][0] != uiScriptLocale.ACCOUNT_SAVED:
				self.account_button_delete_dict[i].Show()
			
	def ConnectOnAccount(self, nAccount):
		if str(ACCOUNTS[nAccount][0]) != uiScriptLocale.ACCOUNT_SAVED:
			self.idEditLine.SetText(str(ACCOUNTS[nAccount][0]))
			self.pwdEditLine.SetText(str(ACCOUNTS[nAccount][1]))
			self.Connect(str(ACCOUNTS[nAccount][0]), str(ACCOUNTS[nAccount][1]))
			self.idEditLine.SetInfoMessage("")
			self.pwdEditLine.SetInfoMessage("")
			
	def NotificationHide(self):
		# self.loginButton.Enable()
		self.pwdEditLine.SetReturnEvent(ui.__mem_func__(self.__OnClickLoginButton))
		self.try_login = 0
			
	def __RequestServerStateList(self):
		ServerStateChecker.Initialize();
		for id, channelDataDict in config.CHANNELS_DICT.items():
			key=channelDataDict["key"]
			ip=config.SERVER_SETTINGS["IP"]
			port=channelDataDict["port"]
			ServerStateChecker.AddChannel(key, ip, port)

		ServerStateChecker.Request()
			
	def NotifyChannelState(self, addrKey, state):
		channelID=addrKey%10
		config.CHANNELS_DICT[channelID]["state"] = config.CHANNELS_DICT_IMAGES[state]
		self.__RefreshServerStateList()

	def __RefreshServerStateList(self):
		for channelID, channelDataDict in config.CHANNELS_DICT.items():
			channelState = channelDataDict["state"]
			self.channels_dict[channelID - 1].LoadImage(channelState)

	def SetChannel(self, ch):
		for (channelID, channelButtons) in self.channelButton.items():
			channelButtons.SetUp()
			
		self.channelButton[ch].Down()
		
		self.stream.SetConnectInfo(config.SERVER_SETTINGS["IP"], config.SERVER_SETTINGS[ch], config.SERVER_SETTINGS["IP"], config.SERVER_SETTINGS["AUTH"])
		net.SetMarkServer(config.SERVER_SETTINGS["IP"], config.SERVER_SETTINGS["MARK"])
		app.SetGuildMarkPath("10.tga")
		app.SetGuildSymbolPath("10")
		net.SetServerInfo("%s, %s" % (config.SERVER_SETTINGS["SERVER_NAME"], ch))
				
		self.__RequestServerStateList()
		self.__RefreshServerStateList()
				
	def Connect(self, id, pwd):
		if constInfo.SEQUENCE_PACKET_ENABLE:
			net.SetPacketSequenceMode()
	
		self.stream.popupWindow.Close()
		self.stream.popupWindow.Open(localeInfo.LOGIN_CONNETING, self.SetPasswordEditLineFocus, localeInfo.UI_CANCEL)
		# self.stream.popupWindow.SetWait(app.GetGlobalTimeStamp() + 2)

		self.stream.SetLoginInfo(id, pwd)
		self.stream.Connect()
		
		# self.loginButton.Disable()
		self.pwdEditLine.SetReturnEvent(ui.__mem_func__(self.EmptyFunc))
		self.try_login = 1

	def PopupDisplayMessage(self, msg):
		self.stream.popupWindow.Close()
		self.stream.popupWindow.Open(msg)

	def PopupNotifyMessage(self, msg, func=0):
		if not func:
			func = self.EmptyFunc

		self.stream.popupWindow.Close()
		self.stream.popupWindow.Open(msg, func, localeInfo.UI_OK)

		
	def OnPressExitKey(self):
		self.stream.SetPhaseWindow(0)
		return True
		
	def OnKeyDown(self, key):
		try:
			if key == app.DIK_F1:
				if str(ACCOUNTS[0][0]) != uiScriptLocale.ACCOUNT_SAVED:
					self.idEditLine.SetText(str(ACCOUNTS[0][0]))
					self.pwdEditLine.SetText(str(ACCOUNTS[0][1]))
					self.Connect(str(ACCOUNTS[0][0]), str(ACCOUNTS[0][1]))
			if key == app.DIK_F2:
				if str(ACCOUNTS[1][0]) != uiScriptLocale.ACCOUNT_SAVED:
					self.idEditLine.SetText(str(ACCOUNTS[1][0]))
					self.pwdEditLine.SetText(str(ACCOUNTS[1][1]))
					self.Connect(str(ACCOUNTS[1][0]), str(ACCOUNTS[1][1]))
			if key == app.DIK_F3:
				if str(ACCOUNTS[2][0]) != uiScriptLocale.ACCOUNT_SAVED:
					self.idEditLine.SetText(str(ACCOUNTS[2][0]))
					self.pwdEditLine.SetText(str(ACCOUNTS[2][1]))
					self.Connect(str(ACCOUNTS[2][0]), str(ACCOUNTS[2][1]))
			if key == app.DIK_F4:
				if str(ACCOUNTS[3][0]) != uiScriptLocale.ACCOUNT_SAVED:
					self.idEditLine.SetText(str(ACCOUNTS[3][0]))
					self.pwdEditLine.SetText(str(ACCOUNTS[3][1]))
					self.Connect(str(ACCOUNTS[3][0]), str(ACCOUNTS[3][1]))
			if key == app.DIK_F5:
				if str(ACCOUNTS[4][0]) != uiScriptLocale.ACCOUNT_SAVED:
					self.idEditLine.SetText(str(ACCOUNTS[4][0]))
					self.pwdEditLine.SetText(str(ACCOUNTS[4][1]))
					self.Connect(str(ACCOUNTS[4][0]), str(ACCOUNTS[4][1]))
			if key == app.DIK_F6:
				if str(ACCOUNTS[5][0]) != uiScriptLocale.ACCOUNT_SAVED:
					self.idEditLine.SetText(str(ACCOUNTS[5][0]))
					self.pwdEditLine.SetText(str(ACCOUNTS[5][1]))
					self.Connect(str(ACCOUNTS[5][0]), str(ACCOUNTS[5][1]))
					
			self.idEditLine.SetInfoMessage("")
			self.pwdEditLine.SetInfoMessage("")
			
		except KeyError:
			pass
		except:
			raise

		return True
			
	def EmptyFunc(self):
		pass

	def __OnClickLoginButton(self):		
		id = self.idEditLine.GetText()
		pwd = self.pwdEditLine.GetText()

		if len(id)==0:
			# self.msg_text.SetText(localeInfo.LOGIN_INPUT_ID)
			return

		if len(pwd)==0:
			# self.msg_text.SetText(localeInfo.LOGIN_INPUT_PASSWORD)
			return
					
		self.Connect(id, pwd)
		# self.loginButton.Disable()
		self.pwdEditLine.SetReturnEvent(ui.__mem_func__(self.EmptyFunc))
		self.try_login = 1

	def OnUpdate(self):
		ServerStateChecker.Update()
