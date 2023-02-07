import thenewui as ui
import grp
import chat
import wndMgr
import net
import app
import ime
import localeInfo
import colorInfo
import constInfo
import systemSetting
import CacheEffect as player
import re
import cfg
if app.ENABLE_CHATTING_WINDOW_RENEWAL:
	import os
	import uiCommon
	import uiScriptLocale
	import cPickle
	
def GetFont():
	font = ""
	try:
		font = cfg.Get(cfg.SAVE_GENERAL, "FONT")
	except IOError:
		pass
	return font
	
if GetFont() == "0":
	localeInfo.UI_DEF_FONT = "Tahoma:12"
	localeInfo.UI_DEF_FONT_LARGE = "Tahoma:14"
	localeInfo.UI_DEF_FONT_SMALL = "Tahoma:9"
	
	
if GetFont() == "1":
	localeInfo.UI_DEF_FONT = "Georgia:14"
	localeInfo.UI_DEF_FONT_LARGE = "Georgia:16"
	localeInfo.UI_DEF_FONT_SMALL = "Georgia:14"
	
if GetFont() == "2":
	localeInfo.UI_DEF_FONT = "Arial:12"
	localeInfo.UI_DEF_FONT_LARGE = "Arial:14"
	localeInfo.UI_DEF_FONT_SMALL = "Arial:9"
	
if GetFont() == "3":
	localeInfo.UI_DEF_FONT = "Verdana:12"
	localeInfo.UI_DEF_FONT_LARGE = "Verdana:14"
	localeInfo.UI_DEF_FONT_SMALL = "Verdana:9"
	
if GetFont() == "4":
	localeInfo.UI_DEF_FONT = "Andale Mono:12"
	localeInfo.UI_DEF_FONT_LARGE = "Andale Mono:14"
	localeInfo.UI_DEF_FONT_SMALL = "Andale Mono:9"


ENABLE_LAST_SENTENCE_STACK = True
ENABLE_INSULT_CHECK = True

chatInputSetList = []
def InsertChatInputSetWindow(wnd):
	global chatInputSetList
	chatInputSetList.append(wnd)
def RefreshChatMode():
	global chatInputSetList
	map(lambda wnd:wnd.OnRefreshChatMode(), chatInputSetList)
def DestroyChatInputSetWindow():
	global chatInputSetList
	chatInputSetList = []

if app.ENABLE_CHATTING_WINDOW_RENEWAL:
	CHECK_BOX_X_POS = 145

	OPTION_CHECKBOX_TALKING = 1
	OPTION_CHECKBOX_PARTY = 2
	OPTION_CHECKBOX_GUILD = 3
	OPTION_CHECKBOX_SHOUT = 4
	OPTION_CHECKBOX_INFO = 5
	OPTION_CHECKBOX_NOTICE = 6
	# OPTION_CHECKBOX_DICE = 7
	OPTION_CHECKBOX_EXP_INFO = 7
	OPTION_CHECKBOX_ITEM_INFO = 8
	OPTION_CHECKBOX_MONEY_INFO = 9

	OPTION_CHECKBOX_MODE = {
		chat.CHAT_TYPE_TALKING : OPTION_CHECKBOX_TALKING,
		chat.CHAT_TYPE_INFO : OPTION_CHECKBOX_INFO,
		chat.CHAT_TYPE_NOTICE : OPTION_CHECKBOX_NOTICE,
		chat.CHAT_TYPE_PARTY : OPTION_CHECKBOX_PARTY,
		chat.CHAT_TYPE_GUILD : OPTION_CHECKBOX_GUILD,
		chat.CHAT_TYPE_SHOUT : OPTION_CHECKBOX_SHOUT,
		# chat.CHAT_TYPE_DICE_INFO : OPTION_CHECKBOX_DICE,
		chat.CHAT_TYPE_EXP_INFO : OPTION_CHECKBOX_EXP_INFO,
		chat.CHAT_TYPE_ITEM_INFO : OPTION_CHECKBOX_ITEM_INFO,
		chat.CHAT_TYPE_MONEY_INFO : OPTION_CHECKBOX_MONEY_INFO,
	}

	## ChatSettingWindow
	class ChatSettingWindow(ui.ScriptWindow):
		__author__ = "Owsap"
		__copyright__ = "Copyright 2021, Owsap Productions"

		class MouseReflector(ui.Window):
			def __init__(self, parent):
				ui.Window.__init__(self)
				self.SetParent(parent)
				self.AddFlag("not_pick")
				self.width = self.height = 0
				self.isDown = False

			def __del__(self):
				ui.Window.__del__(self)

			def Down(self):
				self.isDown = True

			def Up(self):
				self.isDown = False

			def OnRender(self):
				if self.isDown:
					grp.SetColor(ui.WHITE_COLOR)
				else:
					grp.SetColor(ui.HALF_WHITE_COLOR)

				x, y = self.GetGlobalPosition()
				grp.RenderBar(x + 2, y + 2, self.GetWidth() - 4, self.GetHeight() - 4)

		class CheckBox(ui.ImageBox):
			def __init__(self, parent, x, y, event, filename = "d:/ymir work/ui/chat/chattingoption_check_box_off.sub"):
				ui.ImageBox.__init__(self)
				self.SetParent(parent)
				self.SetPosition(x, y)
				self.LoadImage(filename)

				self.mouseReflector = parent.MouseReflector(self)
				self.mouseReflector.SetSize(self.GetWidth(), self.GetHeight())

				image = ui.MakeImageBox(self, "d:/ymir work/ui/public/check_image.sub", 0, 0)
				image.AddFlag("not_pick")
				image.SetWindowHorizontalAlignCenter()
				image.SetWindowVerticalAlignCenter()
				image.Hide()

				self.check = False
				self.enable = True
				self.image = image
				self.event = event
				self.Show()

				self.mouseReflector.UpdateRect()

			def __del__(self):
				ui.ImageBox.__del__(self)

			def GetCheck(self):
				return self.check

			def SetCheck(self, flag):
				if flag:
					self.check = True
					self.image.Show()
				else:
					self.check = False
					self.image.Hide()

			def Disable(self):
				self.enable = False

			def OnMouseOverIn(self):
				if not self.enable:
					return
				self.mouseReflector.Show()

			def OnMouseOverOut(self):
				if not self.enable:
					return
				self.mouseReflector.Hide()

			def OnMouseLeftButtonDown(self):
				if not self.enable:
					return
				self.mouseReflector.Down()

			def OnMouseLeftButtonUp(self):
				if not self.enable:
					return
				self.mouseReflector.Up()
				self.event()

		def __init__(self, parent):
			ui.ScriptWindow.__init__(self)
			self.isLoaded = False

			from _weakref import proxy
			self.parent = proxy(parent)
			self.questionDialog = None

			self.checkBoxSlotDict = {}
			self.tmpCheckBoxSettingDict = {}

			self.__LoadWindow()

		def __del__(self):
			ui.ScriptWindow.__del__(self)
			self.isLoaded = False
			self.parent = None
			self.questionDialog = None
			self.checkBoxSlotDict = {}
			self.tmpCheckBoxSettingDict = {}

		def __LoadWindow(self):
			if self.isLoaded:
				return

			self.isLoaded = 1

			try:
				pyScrLoader = ui.PythonScriptLoader()
				pyScrLoader.LoadScriptFile(self, "UIScript/ChatSettingWindow.py")
			except:
				import exception
				exception.Abort("ChatSettingWindow.LoadWindow.LoadScript")

			try:
				self.__BindObject()
			except:
				import exception
				exception.Abort("ChatSettingWindow.LoadWindow.BindObject")

			try:
				self.__CreateObject()
			except:
				import exception
				exception.Abort("ChatSettingWindow.LoadWindow.CreateObject")

			try:
				self.__LoadChattingOptionFile()
			except:
				self.__SaveDefault()

		def __BindObject(self):
			self.GetChild("board").SetCloseEvent(ui.__mem_func__(self.Close))

			self.resetBtn = self.GetChild("reset_button")
			self.resetBtn.SetEvent(ui.__mem_func__(self.__OnClickPopUpSetting), localeInfo.CHATTING_SETTING_CLEAR_QUESTION)

			self.saveBtn = self.GetChild("save_button")
			self.saveBtn.SetEvent(ui.__mem_func__(self.__OnClickSave))

			self.cancelBtn = self.GetChild("cancle_button")
			self.cancelBtn.SetEvent(ui.__mem_func__(self.Close))

		def __CreateObject(self):
			for key in xrange(1, len(OPTION_CHECKBOX_MODE) + 1):
				event = lambda index = key : ui.__mem_func__(self.SetCurrentChatOption)(index)

				# chatting_setting_talking_bg.y + (31 * y)
				yPos = 64 + (31 * 0)
				if key >= OPTION_CHECKBOX_EXP_INFO:
					yPos = 64 + (31 * 1)
				# if key >= OPTION_CHECKBOX_EXP_INFO:
					# yPos = 64 + (31 * 2)

				self.checkBoxSlotDict[key] = self.CheckBox(self, CHECK_BOX_X_POS, yPos + (18 * (key - 1)), event)

		def __OnClickSave(self):
			self.__SaveFile()

			if self.parent:
				self.parent.RefreshChatWindow()

			self.Close()

		def __GetChattingFile(self):
			path = ["UserData", "chatting"]
			try:
				if not os.path.exists(os.getcwd() + os.sep + path[0] + os.sep + path[1]):
					os.makedirs(os.getcwd() + os.sep + "UserData" + os.sep + "chatting")
			except WindowsError as error: pass
			return "%s/%s/%s" % (path[0], path[1], player.GetName())

		def __LoadChattingOptionFile(self):
			load = False
			try:
				fileName = self.__GetChattingFile()
				file = open(fileName)
				try:
					#cPickle.dumps(file)
					load = True
					self.tmpCheckBoxSettingDict = cPickle.load(file)
				except (ValueError, EOFError, cPickle.PicklingError, cPickle.UnpicklingError): pass
			except IOError: pass

			for key in xrange(1, len(OPTION_CHECKBOX_MODE) + 1):
				if not load:
					value = True
					self.tmpCheckBoxSettingDict[key] = True
				else:
					value = self.tmpCheckBoxSettingDict[key]
				self.checkBoxSlotDict[key].SetCheck(value)

			if not load:
				self.__SaveDefault()

		def __SaveFile(self):
			if not self.tmpCheckBoxSettingDict:
				return

			try:
				fileName = self.__GetChattingFile()
				file = open(fileName, 'wb')
				cPickle.dump(self.tmpCheckBoxSettingDict, file)
			except IOError:
				return

		def __SaveDefault(self):
			for key in xrange(1, len(OPTION_CHECKBOX_MODE) + 1):
				self.tmpCheckBoxSettingDict[key] = True

			try:
				fileName = self.__GetChattingFile()
				file = open(fileName, 'wb')
				cPickle.dump(self.tmpCheckBoxSettingDict, file)
			except IOError:
				return

		def __OnClickPopUpSetting(self, text):
			questionDialog = uiCommon.QuestionDialog()
			questionDialog.SetText(text)
			questionDialog.SetAcceptEvent(ui.__mem_func__(self.__QuestionPopupAccept))
			questionDialog.SetCancelEvent(ui.__mem_func__(self.__QuestionPopupCancle))
			questionDialog.Open()
			self.questionDialog = questionDialog

		def __QuestionPopupAccept(self):
			if not self.questionDialog:
				return

			self.__SaveDefault()

			if self.parent:
				self.parent.RefreshChatWindow()

			self.__QuestionPopupCancle()
			self.Close()

		def __QuestionPopupCancle(self):
			self.questionDialog.Close()
			self.questionDialog = None

		def SetCurrentChatOption(self, index):
			value = False
			if not self.checkBoxSlotDict[index].GetCheck():
				value = True

			self.checkBoxSlotDict[index].SetCheck(value)
			self.tmpCheckBoxSettingDict.update({index: value})

		def GetChatModeSetting(self, mode):
			try:
				value = OPTION_CHECKBOX_MODE[mode]
				return self.tmpCheckBoxSettingDict[value]
			except KeyError:
				return True

		def OnPressEscapeKey(self):
			self.Close()
			return True

		def Open(self):
			if not self.isLoaded:
				self.__LoadWindow()

			try:
				self.__LoadChattingOptionFile()
			except:
				self.__SaveDefault()

			self.Show()

		def Close(self):
			if self.questionDialog:
				self.questionDialog.Close()

			self.Hide()

## ChatModeButton
class ChatModeButton(ui.Window):

	OUTLINE_COLOR = grp.GenerateColor(1.0, 1.0, 1.0, 1.0)
	OVER_COLOR = grp.GenerateColor(1.0, 1.0, 1.0, 0.3)
	BUTTON_STATE_UP = 0
	BUTTON_STATE_OVER = 1
	BUTTON_STATE_DOWN = 2

	def __init__(self):
		ui.Window.__init__(self)
		self.state = None
		self.buttonText = None
		self.event = None
		self.SetWindowName("ChatModeButton")

		net.EnableChatInsultFilter(ENABLE_INSULT_CHECK)

	def __del__(self):
		ui.Window.__del__(self)

	def SAFE_SetEvent(self, event):
		self.event=ui.__mem_func__(event)

	def SetText(self, text):
		if None == self.buttonText:
			textLine = ui.TextLine()
			textLine.SetParent(self)
			textLine.SetWindowHorizontalAlignCenter()
			textLine.SetWindowVerticalAlignCenter()
			textLine.SetVerticalAlignCenter()
			textLine.SetHorizontalAlignCenter()
			textLine.SetPackedFontColor(self.OUTLINE_COLOR)
			textLine.Show()
			self.buttonText = textLine

		self.buttonText.SetText(text)

	def SetSize(self, width, height):
		self.width = width
		self.height = height
		ui.Window.SetSize(self, width, height)

	def OnMouseOverIn(self):
		self.state = self.BUTTON_STATE_OVER

	def OnMouseOverOut(self):
		self.state = self.BUTTON_STATE_UP

	def OnMouseLeftButtonDown(self):
		self.state = self.BUTTON_STATE_DOWN

	def OnMouseLeftButtonUp(self):
		self.state = self.BUTTON_STATE_UP
		if self.IsIn():
			self.state = self.BUTTON_STATE_OVER

		if None != self.event:
			self.event()

	def OnRender(self):

		(x, y) = self.GetGlobalPosition()

		grp.SetColor(self.OUTLINE_COLOR)
		grp.RenderRoundBox(x, y, self.width, self.height)

		if self.state >= self.BUTTON_STATE_OVER:
			grp.RenderRoundBox(x+1, y, self.width-2, self.height)
			grp.RenderRoundBox(x, y+1, self.width, self.height-2)

			if self.BUTTON_STATE_DOWN == self.state:
				grp.SetColor(self.OVER_COLOR)
				grp.RenderBar(x+1, y+1, self.width-2, self.height-2)

## ChatLine
class ChatLine(ui.EditLine):

	CHAT_MODE_NAME = {	chat.CHAT_TYPE_TALKING : localeInfo.CHAT_NORMAL,
						chat.CHAT_TYPE_PARTY : localeInfo.CHAT_PARTY,
						chat.CHAT_TYPE_GUILD : localeInfo.CHAT_GUILD,
						chat.CHAT_TYPE_SHOUT : localeInfo.CHAT_SHOUT, }

	def __init__(self):
		ui.EditLine.__init__(self)
		self.SetWindowName("Chat Line")
		self.lastShoutTime = 0
		self.eventEscape = lambda *arg: None
		self.eventReturn = lambda *arg: None
		self.eventTab = None
		self.chatMode = chat.CHAT_TYPE_TALKING
		self.bCodePage = True

		self.overTextLine = ui.TextLine()
		self.overTextLine.SetParent(self)
		self.overTextLine.SetPosition(-1, 0)
		self.overTextLine.SetFontColor(1.0, 1.0, 0.0)
		self.overTextLine.SetOutline()
		self.overTextLine.Hide()

		self.lastSentenceStack = []
		self.lastSentencePos = 0

	def SetChatMode(self, mode):
		self.chatMode = mode

	def GetChatMode(self):
		return self.chatMode

	def ChangeChatMode(self):
		if chat.CHAT_TYPE_TALKING == self.GetChatMode():
			self.SetChatMode(chat.CHAT_TYPE_PARTY)
			self.SetText("#")
			self.SetEndPosition()

		elif chat.CHAT_TYPE_PARTY == self.GetChatMode():
			self.SetChatMode(chat.CHAT_TYPE_GUILD)
			self.SetText("%")
			self.SetEndPosition()

		elif chat.CHAT_TYPE_GUILD == self.GetChatMode():
			self.SetChatMode(chat.CHAT_TYPE_SHOUT)
			self.SetText("!")
			self.SetEndPosition()

		elif chat.CHAT_TYPE_SHOUT == self.GetChatMode():
			self.SetChatMode(chat.CHAT_TYPE_TALKING)
			self.SetText("")

		self.__CheckChatMark()

	def GetCurrentChatModeName(self):
		try:
			return self.CHAT_MODE_NAME[self.chatMode]
		except:
			import exception
			exception.Abort("ChatLine.GetCurrentChatModeName")

	def SAFE_SetEscapeEvent(self, event):
		self.eventReturn = ui.__mem_func__(event)

	def SAFE_SetReturnEvent(self, event):
		self.eventEscape = ui.__mem_func__(event)

	def SAFE_SetTabEvent(self, event):
		self.eventTab = ui.__mem_func__(event)

	def SetTabEvent(self, event):
		self.eventTab = event

	def OpenChat(self):
		self.SetFocus()
		self.__ResetChat()

	def __ClearChat(self):
		self.SetText("")
		self.lastSentencePos = 0

	def __ResetChat(self):
		if chat.CHAT_TYPE_PARTY == self.GetChatMode():
			self.SetText("#")
			self.SetEndPosition()
		elif chat.CHAT_TYPE_GUILD == self.GetChatMode():
			self.SetText("%")
			self.SetEndPosition()
		elif chat.CHAT_TYPE_SHOUT == self.GetChatMode():
			self.SetText("!")
			self.SetEndPosition()
		else:
			self.__ClearChat()

		self.__CheckChatMark()

	def GetLinks(self, string, ret):
		def __IsAllowedLink(link):
			return link.find("https://go.twitch.tv") <> -1 or link.find("youtube.com") <> -1 or link.find("www.twitch.tv") <> -1 or link.find("youtu.be") <> -1 or link.find("etherion") <> -1 or link.find("vid.me") <> -1 or link.find("facebook.com") <> -1 or link.find("fb.me") <> -1

		links = re.findall("(?:(?:https?|ftp|file):\/\/|www\.|ftp\.)(?:\([-A-Z0-9+&@#/%=~_|$?!:,.]*\)|[-A-Z0-9+&@#/%=~_|$?!:,.])*(?:\([-A-Z0-9+&@#/%=~_|$?!:,.]*\)|[A-Z0-9+&@#/%=~_|$])", string, re.I)
		if not (hasattr(ret, "clear") and hasattr(ret, "update")):
			return False

		ret.clear()
		map(lambda link: (ret.update({link:"|cFF00C0FC|Hweb:%s|h[%s]|h|r"%(re.sub("://", "w<?", link), link)})) if link and __IsAllowedLink(link) else None, links)
		return len(links) > 0

	def __SendChatPacket(self, text, type):
		if net.IsChatInsultIn(text):
			chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.CHAT_INSULT_STRING)
		elif text.find("/restart_here") != -1 or text.find("/restart_town") != -1:
			chat.AppendChat(chat.CHAT_TYPE_INFO, "Aceasta comanda nu exista.")
		else:
			text = constInfo.EmojiFilter(text)
			links={}
			if self.GetLinks(text, links):
				for k,v in links.iteritems():
					text = text.replace(k, v)
					
			net.SendChatPacket(text, type)

	def __SendPartyChatPacket(self, text):

		if 1 == len(text):
			self.RunCloseEvent()
			return

		self.__SendChatPacket(text[1:], chat.CHAT_TYPE_PARTY)
		self.__ResetChat()

	def __SendGuildChatPacket(self, text):

		if 1 == len(text):
			self.RunCloseEvent()
			return

		self.__SendChatPacket(text[1:], chat.CHAT_TYPE_GUILD)
		self.__ResetChat()

	def __SendShoutChatPacket(self, text):

		if 1 == len(text):
			self.RunCloseEvent()
			return
			
		if text.find("|E") > 0:
			self.RunCloseEvent()
			return

		self.__SendChatPacket(text[1:], chat.CHAT_TYPE_SHOUT)
		self.__ResetChat()

		self.lastShoutTime = app.GetTime()

	def __SendTalkingChatPacket(self, text):
		self.__SendChatPacket(text, chat.CHAT_TYPE_TALKING)
		self.__ResetChat()

	def OnIMETab(self):
		#if None != self.eventTab:
		#	self.eventTab()
		#return True
		return False

	def OnIMEUpdate(self):
		ui.EditLine.OnIMEUpdate(self)
		self.__CheckChatMark()

	def __CheckChatMark(self):

		self.overTextLine.Hide()

		text = self.GetText()
		if len(text) > 0:
			if '#' == text[0]:
				self.overTextLine.SetText("#")
				self.overTextLine.Show()
			elif '%' == text[0]:
				self.overTextLine.SetText("%")
				self.overTextLine.Show()
			elif '!' == text[0]:
				self.overTextLine.SetText("!")
				self.overTextLine.Show()

	def OnIMEKeyDown(self, key):
		# LAST_SENTENCE_STACK
		if app.VK_UP == key:
			self.__PrevLastSentenceStack()
			return True

		if app.VK_DOWN == key:
			self.__NextLastSentenceStack()
			return True
		# END_OF_LAST_SENTENCE_STACK

		ui.EditLine.OnIMEKeyDown(self, key)

	# LAST_SENTENCE_STACK
	def __PrevLastSentenceStack(self):
		if self.lastSentencePos < chat.GetChatStackSize():
			self.lastSentencePos += 1
			lastSentence = chat.GetChatStack(self.lastSentencePos)
			self.SetText(lastSentence)
			self.SetEndPosition()

	def __NextLastSentenceStack(self):
		if self.lastSentencePos > 1:
			self.lastSentencePos -= 1
			lastSentence = chat.GetChatStack(self.lastSentencePos)
			self.SetText(lastSentence)
			self.SetEndPosition()

	def __PushLastSentenceStack(self, text):
		global ENABLE_LAST_SENTENCE_STACK
		if not ENABLE_LAST_SENTENCE_STACK:
			return

		if len(text) <= 0:
			return

		LAST_SENTENCE_STACK_SIZE = 32
		if len(self.lastSentenceStack) > LAST_SENTENCE_STACK_SIZE:
			self.lastSentenceStack.pop(0)

		chat.AppendChatStack(text)##Scp1453_2
	# END_OF_LAST_SENTENCE_STACK

	def OnIMEReturn(self):
		text = self.GetText()
		textLen=len(text)

		# LAST_SENTENCE_STACK
		self.__PushLastSentenceStack(text)
		# END_OF_LAST_SENTENCE_STACK

		textSpaceCount=text.count(' ')

		if (textLen > 0) and (textLen != textSpaceCount):
			if '#' == text[0]:
				self.__SendPartyChatPacket(text)
			elif '%' == text[0]:
				self.__SendGuildChatPacket(text)
			elif '!' == text[0]:
				self.__SendShoutChatPacket(text)
				# self.__SendShoutChatPacket(str("||H"+str(player.GetMainCharacterName())+":13|h[PM]|h|r ")+text[1:len(text)]) 
			else:
				self.__SendTalkingChatPacket(text)
		else:
			self.__ClearChat()
			self.eventReturn()

		return True

	def OnPressEscapeKey(self):
		self.__ClearChat()
		self.eventEscape()
		return True

	def RunCloseEvent(self):
		self.eventEscape()

	def BindInterface(self, interface):
		self.interface = interface

	def OnMouseLeftButtonDown(self):
		hyperlink = ui.GetHyperlink()
		if hyperlink:
			if app.IsPressed(app.DIK_LALT):
				link = chat.GetLinkFromHyperlink(hyperlink)
				ime.PasteString(link)
			else:
				self.interface.MakeHyperlinkTooltip(hyperlink)
		else:
			ui.EditLine.OnMouseLeftButtonDown(self)

class ChatInputSet(ui.Window):

	CHAT_OUTLINE_COLOR = grp.GenerateColor(1.0, 1.0, 1.0, 1.0)

	def __init__(self):
		ui.Window.__init__(self)
		self.SetWindowName("ChatInputSet")

		InsertChatInputSetWindow(self)
		self.__Create()

	def __del__(self):
		ui.Window.__del__(self)

	def __Create(self):
		chatModeButton = ChatModeButton()
		chatModeButton.SetParent(self)
		chatModeButton.SetSize(40, 17)
		chatModeButton.SetText(localeInfo.CHAT_NORMAL)
		chatModeButton.SetPosition(7, 2)
		chatModeButton.SAFE_SetEvent(self.OnChangeChatMode)
		self.chatModeButton = chatModeButton

		chatLine = ChatLine()
		chatLine.SetParent(self)
		chatLine.SetMax(512)
		chatLine.SetUserMax(76)
		chatLine.SetText("")
		chatLine.SAFE_SetTabEvent(self.OnChangeChatMode)
		chatLine.x = 0
		chatLine.y = 0
		chatLine.width = 0
		chatLine.height = 0
		self.chatLine = chatLine

		btnSend = ui.Button()
		btnSend.SetParent(self)
		btnSend.SetUpVisual("d:/ymir work/ui/game/taskbar/Send_Chat_Button_01.sub")
		btnSend.SetOverVisual("d:/ymir work/ui/game/taskbar/Send_Chat_Button_02.sub")
		btnSend.SetDownVisual("d:/ymir work/ui/game/taskbar/Send_Chat_Button_03.sub")
		btnSend.SetToolTipText(localeInfo.CHAT_SEND_CHAT)
		btnSend.SAFE_SetEvent(self.chatLine.OnIMEReturn)
		self.btnSend = btnSend

	def Destroy(self):
		self.chatModeButton = None
		self.chatLine = None
		self.btnSend = None

	def Open(self):
		self.chatLine.Show()
		self.chatLine.SetPosition(57, 5)
		self.chatLine.SetFocus()
		self.chatLine.OpenChat()

		self.chatModeButton.SetPosition(7, 2)
		self.chatModeButton.Show()

		self.btnSend.Show()
		self.Show()

		self.RefreshPosition()
		return True

	def Close(self):
		self.chatLine.KillFocus()
		self.chatLine.Hide()
		self.chatModeButton.Hide()
		self.btnSend.Hide()
		self.Hide()
		return True

	def SetEscapeEvent(self, event):
		self.chatLine.SetEscapeEvent(event)

	def SetReturnEvent(self, event):
		self.chatLine.SetReturnEvent(event)

	def OnChangeChatMode(self):
		RefreshChatMode()

	def OnRefreshChatMode(self):
		self.chatLine.ChangeChatMode()
		self.chatModeButton.SetText(self.chatLine.GetCurrentChatModeName())

	def SetChatFocus(self):
		self.chatLine.SetFocus()

	def KillChatFocus(self):
		self.chatLine.KillFocus()

	def SetChatMax(self, max):
		self.chatLine.SetUserMax(max)

	def RefreshPosition(self):
		self.chatLine.SetSize(self.GetWidth() - 93, 13)

		self.btnSend.SetPosition(self.GetWidth() - 25, 2)

		(self.chatLine.x, self.chatLine.y, self.chatLine.width, self.chatLine.height) = self.chatLine.GetRect()

	def BindInterface(self, interface):
		self.chatLine.BindInterface(interface)

	def OnRender(self):
		(x, y, width, height) = self.chatLine.GetRect()
		ui.RenderRoundBox(x-4, y-3, width+7, height+4, self.CHAT_OUTLINE_COLOR)

## ChatWindow
class ChatWindow(ui.Window):

	# BOARD_START_COLOR = grp.GenerateColor(0.0, 0.0, 0.0, 0.0)
	# BOARD_END_COLOR = grp.GenerateColor(0.0, 0.0, 0.0, 0.8)
	# BOARD_MIDDLE_COLOR = grp.GenerateColor(0.0, 0.0, 0.0, 0.5)
	# CHAT_OUTLINE_COLOR = grp.GenerateColor(1.0, 1.0, 1.0, 1.0)
	
	BOARD_START_COLOR = grp.GenerateColor(0.0, 0, 0.0, 0.6)
	BOARD_END_COLOR = grp.GenerateColor(0.0, 0, 0.0, 0.45)
	BOARD_MIDDLE_COLOR = grp.GenerateColor(0.0, 0, 0.0, 0.55)
	CHAT_OUTLINE_COLOR = grp.GenerateColor(0.0, 0, 0.0, 1.0)

	EDIT_LINE_HEIGHT = 45
	CHAT_WINDOW_WIDTH = 600
	if app.ENABLE_CHATTING_WINDOW_RENEWAL:
		EDIT_LINE_HIDE_HEIGHT = 20

	class ChatBackBoard(ui.Window):
		def __init__(self):
			ui.Window.__init__(self)
		def __del__(self):
			ui.Window.__del__(self)

	class ChatButton(ui.DragButton):

		def __init__(self):
			ui.DragButton.__init__(self)
			self.AddFlag("float")
			self.AddFlag("movable")
			self.AddFlag("restrict_x")
			self.topFlag = False
			self.SetWindowName("ChatWindow:ChatButton")


		def __del__(self):
			ui.DragButton.__del__(self)

		def SetOwner(self, owner):
			self.owner = owner

		def OnMouseOverIn(self):
			app.SetCursor(app.VSIZE)

		def OnMouseOverOut(self):
			app.SetCursor(app.NORMAL)

		def OnTop(self):
			if True == self.topFlag:
				return

			self.topFlag = True
			self.owner.SetTop()
			self.topFlag = False

	def __init__(self):
		ui.Window.__init__(self)
		self.AddFlag("float")

		self.SetWindowName("ChatWindow")
		self.__RegisterChatColorDict()

		self.boardState = chat.BOARD_STATE_VIEW
		self.chatID = chat.CreateChatSet(chat.CHAT_SET_CHAT_WINDOW)
		chat.SetBoardState(self.chatID, chat.BOARD_STATE_VIEW)

		self.xBar = 0
		self.yBar = 0
		self.widthBar = 0
		self.heightBar = 0
		self.curHeightBar = 0
		self.visibleLineCount = 0
		self.scrollBarPos = 1.0
		self.scrollLock = False

		chatInputSet = ChatInputSet()
		chatInputSet.SetParent(self)
		chatInputSet.SetEscapeEvent(ui.__mem_func__(self.CloseChat))
		chatInputSet.SetReturnEvent(ui.__mem_func__(self.CloseChat))
		chatInputSet.SetSize(550, 25)
		self.chatInputSet = chatInputSet

		btnSendWhisper = ui.Button()
		btnSendWhisper.SetParent(self)
		btnSendWhisper.SetUpVisual("d:/ymir work/ui/game/taskbar/Send_Whisper_Button_01.sub")
		btnSendWhisper.SetOverVisual("d:/ymir work/ui/game/taskbar/Send_Whisper_Button_02.sub")
		btnSendWhisper.SetDownVisual("d:/ymir work/ui/game/taskbar/Send_Whisper_Button_03.sub")
		btnSendWhisper.SetToolTipText(localeInfo.CHAT_SEND_MEMO)
		btnSendWhisper.Hide()
		self.btnSendWhisper = btnSendWhisper
		self.emoticonsList = {}
		btnChatLog = ui.Button()
		btnChatLog.SetParent(self)
		btnChatLog.SetUpVisual("d:/ymir work/ui/game/taskbar/Open_Chat_Log_Button_01.sub")
		btnChatLog.SetOverVisual("d:/ymir work/ui/game/taskbar/Open_Chat_Log_Button_02.sub")
		btnChatLog.SetDownVisual("d:/ymir work/ui/game/taskbar/Open_Chat_Log_Button_03.sub")
		btnChatLog.SetToolTipText(localeInfo.CHAT_LOG)
		btnChatLog.Hide()
		self.btnChatLog = btnChatLog

		btnChatSizing = self.ChatButton()
		btnChatSizing.SetOwner(self)
		btnChatSizing.SetMoveEvent(ui.__mem_func__(self.Refresh))
		btnChatSizing.Hide()
		self.btnChatSizing = btnChatSizing

		if app.ENABLE_CHATTING_WINDOW_RENEWAL:
			imgChatBarLeft = ui.ImageBox()
			imgChatBarLeft.SetParent(self.btnChatSizing)
			imgChatBarLeft.AddFlag("not_pick")
			imgChatBarLeft.LoadImage("d:/ymir work/ui/chat/chat_linebar_left.tga")
			imgChatBarLeft.Show()
			self.imgChatBarLeft = imgChatBarLeft

			imgChatBarRight = ui.ImageBox()
			imgChatBarRight.SetParent(self.btnChatSizing)
			imgChatBarRight.AddFlag("not_pick")
			imgChatBarRight.LoadImage("d:/ymir work/ui/chat/chat_linebar_right.tga")
			imgChatBarRight.Show()
			self.imgChatBarRight = imgChatBarRight

			imgChatBarMiddle = ui.ExpandedImageBox()
			imgChatBarMiddle.SetParent(self.btnChatSizing)
			imgChatBarMiddle.AddFlag("not_pick")
			imgChatBarMiddle.LoadImage("d:/ymir work/ui/chat/chatmenutab_line.tga")
			imgChatBarMiddle.Show()
			self.imgChatBarMiddle = imgChatBarMiddle

			btnChatTab = ui.Button()
			btnChatTab.SetParent(self.btnChatSizing)
			btnChatTab.SetUpVisual("d:/ymir work/ui/chat/chatmenutab_down.tga")
			btnChatTab.SetOverVisual("d:/ymir work/ui/chat/chatmenutab_down.tga")
			btnChatTab.SetDownVisual("d:/ymir work/ui/chat/chatmenutab_down.tga")
			btnChatTab.SetToolTipText(uiScriptLocale.CHATTING_SETTING_TALKING, 0, -23)
			btnChatTab.Show()
			btnChatTab.Down()
			self.btnChatTab = btnChatTab

			btnChatSettingOption = ui.Button()
			btnChatSettingOption.SetParent(self.btnChatSizing)
			btnChatSettingOption.SetUpVisual("d:/ymir work/ui/chat/btn_option01_default.tga")
			btnChatSettingOption.SetOverVisual("d:/ymir work/ui/chat/btn_option01_over.tga")
			btnChatSettingOption.SetDownVisual("d:/ymir work/ui/chat/btn_option01_down.tga")
			btnChatSettingOption.SetToolTipText(localeInfo.CHATTING_SETTING_SETTING, 0, -23)
			btnChatSettingOption.SetEvent(ui.__mem_func__(self.__SettingOptionWndOpen))
			btnChatSettingOption.Show()
			self.btnChatSettingOption = btnChatSettingOption

			self.wndChatSettingOption = ChatSettingWindow(self)
		else:
			imgChatBarLeft = ui.ImageBox()
			imgChatBarLeft.SetParent(self.btnChatSizing)
			imgChatBarLeft.AddFlag("not_pick")
			imgChatBarLeft.LoadImage("d:/ymir work/ui/pattern/chat_bar_left.tga")
			imgChatBarLeft.Show()
			self.imgChatBarLeft = imgChatBarLeft

			imgChatBarRight = ui.ImageBox()
			imgChatBarRight.SetParent(self.btnChatSizing)
			imgChatBarRight.AddFlag("not_pick")
			imgChatBarRight.LoadImage("d:/ymir work/ui/pattern/chat_bar_right.tga")
			imgChatBarRight.Show()
			self.imgChatBarRight = imgChatBarRight

			imgChatBarMiddle = ui.ExpandedImageBox()
			imgChatBarMiddle.SetParent(self.btnChatSizing)
			imgChatBarMiddle.AddFlag("not_pick")
			imgChatBarMiddle.LoadImage("d:/ymir work/ui/pattern/chat_bar_middle.tga")
			imgChatBarMiddle.Show()
			self.imgChatBarMiddle = imgChatBarMiddle

		scrollBar = ui.ScrollBar()
		scrollBar.AddFlag("float")
		scrollBar.SetScrollEvent(ui.__mem_func__(self.OnScroll))
		self.scrollBar = scrollBar

		self.Refresh()
		self.chatInputSet.RefreshPosition()
		if app.ENABLE_CHATTING_WINDOW_RENEWAL:
			self.RefreshChatWindow()
			
	def __del__(self):
		ui.Window.__del__(self)

	def __RegisterChatColorDict(self):
		CHAT_COLOR_DICT = {
			chat.CHAT_TYPE_TALKING : colorInfo.CHAT_RGB_TALK,
			chat.CHAT_TYPE_INFO : colorInfo.CHAT_RGB_INFO,
			chat.CHAT_TYPE_NOTICE : colorInfo.CHAT_RGB_NOTICE,
			chat.CHAT_TYPE_PARTY : colorInfo.CHAT_RGB_PARTY,
			chat.CHAT_TYPE_GUILD : colorInfo.CHAT_RGB_GUILD,
			chat.CHAT_TYPE_COMMAND : colorInfo.CHAT_RGB_COMMAND,
			chat.CHAT_TYPE_SHOUT : colorInfo.CHAT_RGB_SHOUT,
			chat.CHAT_TYPE_WHISPER : colorInfo.CHAT_RGB_WHISPER,
		}
		if app.ENABLE_CHATTING_WINDOW_RENEWAL:
			CHAT_COLOR_DICT.update({
				chat.CHAT_TYPE_EXP_INFO : colorInfo.CHAT_RGB_INFO,
				chat.CHAT_TYPE_ITEM_INFO : colorInfo.CHAT_RGB_INFO,
				chat.CHAT_TYPE_MONEY_INFO : colorInfo.CHAT_RGB_INFO,
			})

		for colorItem in CHAT_COLOR_DICT.items():
			type=colorItem[0]
			rgb=colorItem[1]
			chat.SetChatColor(type, rgb[0], rgb[1], rgb[2])

	def Destroy(self):
		self.chatInputSet.Destroy()
		self.chatInputSet = None

		self.btnSendWhisper = 0
		self.btnChatLog = 0
		self.btnChatSizing = 0
		if app.ENABLE_CHATTING_WINDOW_RENEWAL:
			self.btnChatTab = None
			self.btnChatSettingOption = None

			if self.wndChatSettingOption:
				self.wndChatSettingOption.Close()
				self.wndChatSettingOption = None
				
	################
	## Open & Close
	def OpenChat(self):
		self.SetSize(self.CHAT_WINDOW_WIDTH, 45)
		chat.SetBoardState(self.chatID, chat.BOARD_STATE_EDIT)
		self.boardState = chat.BOARD_STATE_EDIT

		(x, y, width, height) = self.GetRect()
		(btnX, btnY) = self.btnChatSizing.GetGlobalPosition()

		chat.SetPosition(self.chatID, x + 10, y)

		chat.SetHeight(self.chatID, y - btnY - self.EDIT_LINE_HEIGHT + 100)
		
		for i in xrange(1, 36):
			self.emoticonsList[i] = ui.Button()
			self.emoticonsList[i].SetParent(self)
			self.emoticonsList[i].SetPosition(-12 + (17 * i), 25)
			self.emoticonsList[i].SetOverVisual("icon/emoji/chat/%d.png" % i)
			self.emoticonsList[i].SetDownVisual("icon/emoji/chat/%d.png" % i)
			self.emoticonsList[i].SetUpVisual("icon/emoji/chat/%d.png" % i)
			self.emoticonsList[i].SetEvent(ui.__mem_func__(self.SelectEmoticon), (i - 1))
			self.emoticonsList[i].Show()

		if self.IsShow():
			self.btnChatSizing.Show()
		if app.ENABLE_CHATTING_WINDOW_RENEWAL:
			self.RefreshChatWindow()
		self.Refresh()

		self.btnSendWhisper.SetPosition(self.GetWidth() - 50, 2)
		self.btnSendWhisper.Show()

		self.btnChatLog.SetPosition(self.GetWidth() - 25, 2)
		self.btnChatLog.Show()

		self.chatInputSet.Open()
		self.chatInputSet.SetTop()
		self.SetTop()

	def CloseChat(self):
		chat.SetBoardState(self.chatID, chat.BOARD_STATE_VIEW)
		self.boardState = chat.BOARD_STATE_VIEW

		(x, y, width, height) = self.GetRect()

		chat.SetPosition(self.chatID, x + 10, y + self.EDIT_LINE_HEIGHT)
		for i in xrange(1,36):
			self.emoticonsList[i].Hide()

		self.SetSize(self.CHAT_WINDOW_WIDTH, 0)

		self.chatInputSet.Close()
		self.btnSendWhisper.Hide()
		self.btnChatLog.Hide()
		self.btnChatSizing.Hide()

		self.Refresh()
		if app.ENABLE_CHATTING_WINDOW_RENEWAL:
			self.RefreshChatWindow()
			
	def SelectEmoticon(self, emoticonIdx):
		emoticonKeyList = ["<1>","<2>","<3>","<4>","<5>","<6>","<7>","<8>","<9>","<10>","<11>","<12>","<13>","<14>","<15>","<16>","<17>","<18>","<19>","<20>","<21>","<22>","<23>","<24>","<25>","<26>","<27>","<28>","<29>","<30>","<31>","<32>","<33>","<34>","<35>","<36>"]
		self.chatInputSet.chatLine.SetText("%s%s" % (self.chatInputSet.chatLine.GetText(), emoticonKeyList[emoticonIdx]))

	def SetSendWhisperEvent(self, event):
		self.btnSendWhisper.SetEvent(event)

	def SetOpenChatLogEvent(self, event):
		self.btnChatLog.SetEvent(event)

	def IsEditMode(self):
		if chat.BOARD_STATE_EDIT == self.boardState:
			return True

		return False

	def __RefreshSizingBar(self):
		(x, y, width, height) = self.GetRect()
		gxChat, gyChat = self.btnChatSizing.GetGlobalPosition()
		self.btnChatSizing.SetPosition(x, gyChat)
		self.btnChatSizing.SetSize(width, 22)
		if app.ENABLE_CHATTING_WINDOW_RENEWAL:
			self.imgChatBarLeft.SetPosition(0, 17)
			self.imgChatBarRight.SetPosition(width - 57, 0)

			self.imgChatBarMiddle.SetPosition(57.0, 0)
			self.imgChatBarMiddle.SetRenderingRect(0.0, 0.0, float(width - 57.0 * 2) / 57.0 - 1.0, 0.0)

			self.btnChatTab.SetTextAddPos(uiScriptLocale.CHATTING_SETTING_DEFAULT_TITLE, -2)
			self.btnChatTab.SetPosition(4, 0)
			self.btnChatSettingOption.SetPosition(width - 27, 3)
		else:
			self.imgChatBarLeft.SetPosition(0, 0)
			self.imgChatBarRight.SetPosition(width - 64, 0)
			self.imgChatBarMiddle.SetPosition(64, 0)
			self.imgChatBarMiddle.SetRenderingRect(0.0, 0.0, float(width - 128) / 64.0 - 1.0, 0.0)

	def SetPosition(self, x, y):
		ui.Window.SetPosition(self, x, y)
		self.__RefreshSizingBar()

	def SetSize(self, width, height):
		ui.Window.SetSize(self, width, height)
		self.__RefreshSizingBar()

	def SetHeight(self, height):
		gxChat, gyChat = self.btnChatSizing.GetGlobalPosition()
		self.btnChatSizing.SetPosition(gxChat, wndMgr.GetScreenHeight() - height)

	###########
	## Refresh
	def Refresh(self):
		if self.boardState == chat.BOARD_STATE_EDIT:
			self.RefreshBoardEditState()
		elif self.boardState == chat.BOARD_STATE_VIEW:
			self.RefreshBoardViewState()

	def RefreshBoardEditState(self):

		(x, y, width, height) = self.GetRect()
		(btnX, btnY) = self.btnChatSizing.GetGlobalPosition()

		self.xBar = x
		self.yBar = btnY
		self.widthBar = width
		self.heightBar = y - btnY + self.EDIT_LINE_HEIGHT
		self.curHeightBar = self.heightBar

		chat.SetPosition(self.chatID, x + 10, y)

		chat.SetHeight(self.chatID, y - btnY - self.EDIT_LINE_HEIGHT)
		chat.ArrangeShowingChat(self.chatID)

		if btnY > y:
			self.btnChatSizing.SetPosition(btnX, y)
			self.heightBar = self.EDIT_LINE_HEIGHT

	def RefreshBoardViewState(self):
		(x, y, width, height) = self.GetRect()
		(btnX, btnY) = self.btnChatSizing.GetGlobalPosition()
		textAreaHeight = self.visibleLineCount * chat.GetLineStep(self.chatID)

		chat.SetPosition(self.chatID, x + 10, y + self.EDIT_LINE_HEIGHT)

		chat.SetHeight(self.chatID, y - btnY - self.EDIT_LINE_HEIGHT + 100)

		if self.boardState == chat.BOARD_STATE_EDIT:
			textAreaHeight += 45
		elif self.visibleLineCount != 0:
			textAreaHeight += 10 + 10

		self.xBar = x
		self.yBar = y + self.EDIT_LINE_HEIGHT - textAreaHeight
		self.widthBar = width
		self.heightBar = textAreaHeight

		self.scrollBar.Hide()

	##########
	## Render
	def OnUpdate(self):
		if self.boardState == chat.BOARD_STATE_EDIT:
			chat.Update(self.chatID)
		elif self.boardState == chat.BOARD_STATE_VIEW:
			if systemSetting.IsViewChat():
				chat.Update(self.chatID)

	def OnRender(self):
		if chat.GetVisibleLineCount(self.chatID) != self.visibleLineCount:
			self.visibleLineCount = chat.GetVisibleLineCount(self.chatID)
			self.Refresh()

		if self.curHeightBar != self.heightBar:
			self.curHeightBar += (self.heightBar - self.curHeightBar) / 10

		if self.boardState == chat.BOARD_STATE_EDIT:
			grp.SetColor(self.BOARD_MIDDLE_COLOR)
			if app.ENABLE_CHATTING_WINDOW_RENEWAL:
				grp.RenderBar(self.xBar, self.yBar + (self.heightBar - self.curHeightBar) + self.EDIT_LINE_HIDE_HEIGHT, self.widthBar, self.curHeightBar)
			else:
				grp.RenderBar(self.xBar, self.yBar + (self.heightBar - self.curHeightBar) + 10, self.widthBar, self.curHeightBar)

			chat.Render(self.chatID)
		elif self.boardState == chat.BOARD_STATE_VIEW:
			if systemSetting.IsViewChat():
				grp.RenderGradationBar(self.xBar, self.yBar + (self.heightBar - self.curHeightBar), self.widthBar, self.curHeightBar, self.BOARD_START_COLOR, self.BOARD_END_COLOR)
				chat.Render(self.chatID)

	##########
	## Event
	def OnTop(self):
		self.btnChatSizing.SetTop()
		self.scrollBar.SetTop()

	def OnScroll(self):
		if not self.scrollLock:
			self.scrollBarPos = self.scrollBar.GetPos()

		lineCount = chat.GetLineCount(self.chatID)
		visibleLineCount = chat.GetVisibleLineCount(self.chatID)
		endLine = visibleLineCount + int(float(lineCount - visibleLineCount) * self.scrollBarPos)

		chat.SetEndPos(self.chatID, self.scrollBarPos)

	def OnChangeChatMode(self):
		self.chatInputSet.OnChangeChatMode()

	def SetChatFocus(self):
		self.chatInputSet.SetChatFocus()

	def BindInterface(self, interface):
		self.chatInputSet.BindInterface(interface)
		
	if app.ENABLE_CHATTING_WINDOW_RENEWAL:
		def __SettingOptionWndOpen(self):
			if self.wndChatSettingOption:
				if self.wndChatSettingOption.IsShow():
					self.wndChatSettingOption.Close()
				else:
					self.wndChatSettingOption.Open()

		def RefreshChatWindow(self):
			if self.wndChatSettingOption:
				for mode in OPTION_CHECKBOX_MODE.iterkeys():
					enable = self.wndChatSettingOption.GetChatModeSetting(mode)
					if enable:
						chat.EnableChatMode(self.chatID, mode)
					else:
						chat.DisableChatMode(self.chatID, mode)

## ChatLogWindow
class ChatLogWindow(ui.Window):

	BLOCK_WIDTH = 32
	CHAT_MODE_NAME = ( localeInfo.CHAT_NORMAL, localeInfo.CHAT_PARTY, localeInfo.CHAT_GUILD, localeInfo.CHAT_SHOUT, localeInfo.CHAT_INFORMATION, localeInfo.CHAT_NOTICE, )
	CHAT_MODE_INDEX = ( chat.CHAT_TYPE_TALKING,
						chat.CHAT_TYPE_PARTY,
						chat.CHAT_TYPE_GUILD,
						chat.CHAT_TYPE_SHOUT,
						chat.CHAT_TYPE_INFO,
						chat.CHAT_TYPE_NOTICE, )

	CHAT_LOG_WINDOW_MINIMUM_WIDTH = 450
	CHAT_LOG_WINDOW_MINIMUM_HEIGHT = 120

	class ResizeButton(ui.DragButton):

		def __init__(self):
			ui.DragButton.__init__(self)

		def __del__(self):
			ui.DragButton.__del__(self)

		def OnMouseOverIn(self):
			app.SetCursor(app.HVSIZE)

		def OnMouseOverOut(self):
			app.SetCursor(app.NORMAL)

	def __init__(self):

		self.allChatMode = True
		self.chatInputSet = None

		ui.Window.__init__(self)
		self.AddFlag("float")
		self.AddFlag("movable")
		self.SetWindowName("ChatLogWindow")
		self.__CreateChatInputSet()
		self.__CreateWindow()
		self.__CreateButton()
		self.__CreateScrollBar()

		self.chatID = chat.CreateChatSet(chat.CHAT_SET_LOG_WINDOW)
		chat.SetBoardState(self.chatID, chat.BOARD_STATE_LOG)
		for i in self.CHAT_MODE_INDEX:
			chat.EnableChatMode(self.chatID, i)
		if app.ENABLE_CHATTING_WINDOW_RENEWAL:
			chat.EnableChatMode(self.chatID, chat.CHAT_TYPE_EXP_INFO)
			chat.EnableChatMode(self.chatID, chat.CHAT_TYPE_ITEM_INFO)
			chat.EnableChatMode(self.chatID, chat.CHAT_TYPE_MONEY_INFO)
		self.SetPosition(20, 20)
		self.SetSize(self.CHAT_LOG_WINDOW_MINIMUM_WIDTH, self.CHAT_LOG_WINDOW_MINIMUM_HEIGHT)
		self.btnSizing.SetPosition(self.CHAT_LOG_WINDOW_MINIMUM_WIDTH-self.btnSizing.GetWidth(), self.CHAT_LOG_WINDOW_MINIMUM_HEIGHT-self.btnSizing.GetHeight()+2)

		self.OnResize()

	def __CreateChatInputSet(self):
		chatInputSet = ChatInputSet()
		chatInputSet.SetParent(self)
		chatInputSet.SetEscapeEvent(ui.__mem_func__(self.Close))
		chatInputSet.SetWindowVerticalAlignBottom()
		chatInputSet.Open()
		self.chatInputSet = chatInputSet

	def __CreateWindow(self):
		imgLeft = ui.ImageBox()
		imgLeft.AddFlag("not_pick")
		imgLeft.SetParent(self)

		imgCenter = ui.ExpandedImageBox()
		imgCenter.AddFlag("not_pick")
		imgCenter.SetParent(self)

		imgRight = ui.ImageBox()
		imgRight.AddFlag("not_pick")
		imgRight.SetParent(self)

		imgLeft.LoadImage("d:/ymir work/ui/pattern/chatlogwindow_titlebar_left.tga")
		imgCenter.LoadImage("d:/ymir work/ui/pattern/chatlogwindow_titlebar_middle.tga")
		imgRight.LoadImage("d:/ymir work/ui/pattern/chatlogwindow_titlebar_right.tga")

		imgLeft.Show()
		imgCenter.Show()
		imgRight.Show()

		btnClose = ui.Button()
		btnClose.SetParent(self)
		btnClose.SetUpVisual("d:/ymir work/ui/public/close_button_01.sub")
		btnClose.SetOverVisual("d:/ymir work/ui/public/close_button_02.sub")
		btnClose.SetDownVisual("d:/ymir work/ui/public/close_button_03.sub")
		btnClose.SetToolTipText(localeInfo.UI_CLOSE, 0, -23)
		btnClose.SetEvent(ui.__mem_func__(self.Close))
		btnClose.Show()

		btnSizing = self.ResizeButton()
		btnSizing.SetParent(self)
		btnSizing.SetMoveEvent(ui.__mem_func__(self.OnResize))
		btnSizing.SetSize(16, 16)
		btnSizing.Show()

		titleName = ui.TextLine()
		titleName.SetParent(self)

		titleName.SetPosition(20, 6)

		titleName.SetText(localeInfo.CHAT_LOG_TITLE)
		titleName.Show()

		self.imgLeft = imgLeft
		self.imgCenter = imgCenter
		self.imgRight = imgRight
		self.btnClose = btnClose
		self.btnSizing = btnSizing
		self.titleName = titleName

	def __CreateButton(self):

		bx = 13

		btnAll = ui.RadioButton()
		btnAll.SetParent(self)
		btnAll.SetPosition(bx, 24)
		btnAll.SetUpVisual("d:/ymir work/ui/public/xsmall_button_01.sub")
		btnAll.SetOverVisual("d:/ymir work/ui/public/xsmall_button_02.sub")
		btnAll.SetDownVisual("d:/ymir work/ui/public/xsmall_button_03.sub")
		btnAll.SetText(localeInfo.CHAT_ALL)
		btnAll.SetEvent(ui.__mem_func__(self.ToggleAllChatMode))
		btnAll.Down()
		btnAll.Show()
		self.btnAll = btnAll

		x = bx + 48
		i = 0
		self.modeButtonList = []
		for name in self.CHAT_MODE_NAME:
			btn = ui.ToggleButton()
			btn.SetParent(self)
			btn.SetPosition(x, 24)
			btn.SetUpVisual("d:/ymir work/ui/public/xsmall_button_01.sub")
			btn.SetOverVisual("d:/ymir work/ui/public/xsmall_button_02.sub")
			btn.SetDownVisual("d:/ymir work/ui/public/xsmall_button_03.sub")
			btn.SetText(name)
			btn.Show()

			mode = self.CHAT_MODE_INDEX[i]
			btn.SetToggleUpEvent(lambda arg=mode: self.ToggleChatMode(arg))
			btn.SetToggleDownEvent(lambda arg=mode: self.ToggleChatMode(arg))
			self.modeButtonList.append(btn)

			x += 48
			i += 1

	def __CreateScrollBar(self):
		scrollBar = ui.SmallThinScrollBar()
		scrollBar.SetParent(self)
		scrollBar.Show()
		scrollBar.SetScrollEvent(ui.__mem_func__(self.OnScroll))
		self.scrollBar = scrollBar
		self.scrollBarPos = 1.0

	def __del__(self):
		ui.Window.__del__(self)

	def Destroy(self):
		self.imgLeft = None
		self.imgCenter = None
		self.imgRight = None
		self.btnClose = None
		self.btnSizing = None
		self.modeButtonList = []
		self.scrollBar = None
		self.chatInputSet = None

	def ToggleAllChatMode(self):
		if self.allChatMode:
			return

		self.allChatMode = True

		for i in self.CHAT_MODE_INDEX:
			chat.EnableChatMode(self.chatID, i)
			
		if app.ENABLE_CHATTING_WINDOW_RENEWAL:
			chat.EnableChatMode(self.chatID, chat.CHAT_TYPE_EXP_INFO)
			chat.EnableChatMode(self.chatID, chat.CHAT_TYPE_ITEM_INFO)
			chat.EnableChatMode(self.chatID, chat.CHAT_TYPE_MONEY_INFO)

		for btn in self.modeButtonList:
			btn.SetUp()

	if app.ENABLE_CHAT_HISTORY_UPDATE:
		def ToggleChatMode(self, mode):
			if self.allChatMode:
				self.allChatMode = False
				
				if app.ENABLE_CHATTING_WINDOW_RENEWAL:
					if mode == chat.CHAT_TYPE_INFO:
						chat.EnableChatMode(self.chatID, chat.CHAT_TYPE_EXP_INFO)
						chat.EnableChatMode(self.chatID, chat.CHAT_TYPE_ITEM_INFO)
						chat.EnableChatMode(self.chatID, chat.CHAT_TYPE_MONEY_INFO)
					else:
						chat.DisableChatMode(self.chatID, chat.CHAT_TYPE_EXP_INFO)
						chat.DisableChatMode(self.chatID, chat.CHAT_TYPE_ITEM_INFO)
						chat.DisableChatMode(self.chatID, chat.CHAT_TYPE_MONEY_INFO)

				for i in self.CHAT_MODE_INDEX:
					chat.DisableChatMode(self.chatID, i)
					
				chat.EnableChatMode(self.chatID, mode)
				
				self.btnAll.SetUp()
			else:
				chat.ToggleChatMode(self.chatID, mode)
				ison, modeflag = chat.GetChatMode(self.chatID)
				if not ison:
					self.btnAll.Down()
					self.ToggleAllChatMode()
	else:
		def ToggleChatMode(self, mode):
			if self.allChatMode:
				self.allChatMode = False
				for i in self.CHAT_MODE_INDEX:
					chat.DisableChatMode(self.chatID, i)
				chat.EnableChatMode(self.chatID, mode)
				if app.ENABLE_CHATTING_WINDOW_RENEWAL:
					if mode == chat.CHAT_TYPE_INFO:
						chat.EnableChatMode(self.chatID, chat.CHAT_TYPE_EXP_INFO)
						chat.EnableChatMode(self.chatID, chat.CHAT_TYPE_ITEM_INFO)
						chat.EnableChatMode(self.chatID, chat.CHAT_TYPE_MONEY_INFO)
				self.btnAll.SetUp()
			else:
				chat.ToggleChatMode(self.chatID, mode)

	def SetSize(self, width, height):
		self.imgCenter.SetRenderingRect(0.0, 0.0, float((width - self.BLOCK_WIDTH*2) - self.BLOCK_WIDTH) / self.BLOCK_WIDTH, 0.0)
		self.imgCenter.SetPosition(self.BLOCK_WIDTH, 0)
		self.imgRight.SetPosition(width - self.BLOCK_WIDTH, 0)

		self.btnClose.SetPosition(width - self.btnClose.GetWidth() - 5, 5)
		self.scrollBar.SetPosition(width - 15, 45)

		self.scrollBar.SetScrollBarSize(height - 45 - 12)
		self.scrollBar.SetPos(self.scrollBarPos)
		ui.Window.SetSize(self, width, height)

	def Open(self):
		self.OnResize()
		self.chatInputSet.SetChatFocus()
		self.Show()

	def Close(self):
		if self.chatInputSet:
			self.chatInputSet.KillChatFocus()
		self.Hide()

	def OnResize(self):
		x, y = self.btnSizing.GetLocalPosition()
		width = self.btnSizing.GetWidth()
		height = self.btnSizing.GetHeight()

		if x < self.CHAT_LOG_WINDOW_MINIMUM_WIDTH - width:
			self.btnSizing.SetPosition(self.CHAT_LOG_WINDOW_MINIMUM_WIDTH - width, y)
			return
		if y < self.CHAT_LOG_WINDOW_MINIMUM_HEIGHT - height:
			self.btnSizing.SetPosition(x, self.CHAT_LOG_WINDOW_MINIMUM_HEIGHT - height)
			return

		self.scrollBar.LockScroll()
		self.SetSize(x + width, y + height)
		self.scrollBar.UnlockScroll()

		self.chatInputSet.SetPosition(0, 25)

		self.chatInputSet.SetSize(self.GetWidth() - 20, 20)
		self.chatInputSet.RefreshPosition()
		self.chatInputSet.SetChatMax(self.GetWidth() / 8)

	def OnScroll(self):
		self.scrollBarPos = self.scrollBar.GetPos()

		lineCount = chat.GetLineCount(self.chatID)
		visibleLineCount = chat.GetVisibleLineCount(self.chatID)
		endLine = visibleLineCount + int(float(lineCount - visibleLineCount) * self.scrollBarPos)

		chat.SetEndPos(self.chatID, self.scrollBarPos)

	def OnRender(self):
		(x, y, width, height) = self.GetRect()

		grp.SetColor(0x77000000)
		grp.RenderBar(x+width-15, y+45, 13, height-45)

		grp.SetColor(0x77000000)
		grp.RenderBar(x, y, width, height)
		grp.SetColor(0x77000000)
		grp.RenderBox(x, y, width-2, height)
		grp.SetColor(0x77000000)
		grp.RenderBox(x+1, y+1, width-2, height)

		grp.SetColor(0xff989898)
		grp.RenderLine(x+width-13, y+height-1, 11, -11)
		grp.RenderLine(x+width-9, y+height-1, 7, -7)
		grp.RenderLine(x+width-5, y+height-1, 3, -3)

		#####

		chat.ArrangeShowingChat(self.chatID)

		chat.SetPosition(self.chatID, x + 10, y + height - 25)

		chat.SetHeight(self.chatID, height - 45 - 25)
		chat.Update(self.chatID)
		chat.Render(self.chatID)

	def OnPressEscapeKey(self):
		self.Close()
		return True

	def BindInterface(self, interface):
		self.interface = interface

	def OnMouseLeftButtonDown(self):
		hyperlink = ui.GetHyperlink()
		if hyperlink:
			if app.IsPressed(app.DIK_LALT):
				link = chat.GetLinkFromHyperlink(hyperlink)
				ime.PasteString(link)
			else:
				self.interface.MakeHyperlinkTooltip(hyperlink)