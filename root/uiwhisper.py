import thenewui as ui
import net
import chat
import CacheEffect as player
import app
import grp
import messenger
import uiCommon
import ime
import chr
import constInfo
import re
import localeInfo
import time

class WhisperButton(ui.Button):
	def __init__(self):
		ui.Button.__init__(self, "TOP_MOST")
		self.SetWindowName("WhisperButton")

	def __del__(self):
		ui.Button.__del__(self)

	def SetToolTipText(self, text, x=0, y = 32):
		ui.Button.SetToolTipText(self, text, x, y)
		self.ToolTipText.Show()

	def SetToolTipTextWithColor(self, text, color, x=0, y = 32):
		ui.Button.SetToolTipText(self, text, x, y)
		self.ToolTipText.SetPackedFontColor(color)
		self.ToolTipText.Show()

	def ShowToolTip(self):
		if 0 != self.ToolTipText:
			self.ToolTipText.Show()

	def HideToolTip(self):
		if 0 != self.ToolTipText:
			self.ToolTipText.Show()

class WhisperDialog(ui.ScriptWindow):
	class TextRenderer(ui.Window):
		def SetTargetName(self, targetName):
			self.targetName = targetName

		def OnRender(self):
			(x, y) = self.GetGlobalPosition()
			chat.RenderBox(self.targetName, x, y)

	class ResizeButton(ui.DragButton):

		def __init__(self):
			ui.DragButton.__init__(self)
			self.SetWindowName("ResizeButton")

		def __del__(self):
			ui.DragButton.__del__(self)

		def OnMouseOverIn(self):
			app.SetCursor(app.HVSIZE)

		def OnMouseOverOut(self):
			app.SetCursor(app.NORMAL)

	def __init__(self, eventMinimize, eventClose):
		ui.ScriptWindow.__init__(self)
		self.targetName = ""
		self.eventMinimize = eventMinimize
		self.eventClose = eventClose
		self.eventAcceptTarget = None
		if app.ENABLE_RUN_MOUSE_WHEEL:
			self.onRunMouseWheelEvent = None

	def __del__(self):
		ui.ScriptWindow.__del__(self)

	def LoadDialog(self):
		try:
			pyScrLoader = ui.PythonScriptLoader()
			pyScrLoader.LoadScriptFile(self, "UIScript/WhisperDialog.py")
		except:
			import exception
			exception.Abort("WhisperDialog.LoadDialog.LoadScript")

		try:
			GetObject=self.GetChild
			self.titleName = GetObject("titlename")
			self.titleNameEdit = GetObject("titlename_edit")
			self.closeButton = GetObject("closebutton")
			self.scrollBar = GetObject("scrollbar")
			self.chatLine = GetObject("chatline")
			self.minimizeButton = GetObject("minimizebutton")
			self.acceptButton = GetObject("acceptbutton")
			self.sendButton = GetObject("sendbutton")
			self.board = GetObject("board")
			self.boardEmoticons = GetObject("board_emoticons")
			self.editBar = GetObject("editbar")
			self.nameSlot = GetObject("name_slot")
			
			self.emoticonsList = []
			
			for i in xrange(8):
				self.emoticonsList.append(GetObject("emoticon_%d" % i))
				self.emoticonsList[i].SetEvent(ui.__mem_func__(self.SelectEmoticon), i)
		except:
			import exception
			exception.Abort("DialogWindow.LoadDialog.BindObject")

		self.titleName.SetText("")
		self.titleNameEdit.SetText("")

		self.minimizeButton.SetEvent(ui.__mem_func__(self.Minimize))
		self.closeButton.SetEvent(ui.__mem_func__(self.Close))
		self.scrollBar.SetPos(1.0)
		self.scrollBar.SetScrollEvent(ui.__mem_func__(self.OnScroll))
		self.chatLine.SetReturnEvent(ui.__mem_func__(self.SendWhisper))
		self.chatLine.SetEscapeEvent(ui.__mem_func__(self.Minimize))
		self.chatLine.SetMultiLine()
		self.sendButton.SetEvent(ui.__mem_func__(self.SendWhisper))
		self.titleNameEdit.SetReturnEvent(ui.__mem_func__(self.AcceptTarget))
		self.titleNameEdit.SetEscapeEvent(ui.__mem_func__(self.Close))
		
		self.acceptButton.SetEvent(ui.__mem_func__(self.AcceptTarget))
		
		self.boardEmoticons.HideCorners(self.boardEmoticons.LT)
		self.boardEmoticons.HideCorners(self.boardEmoticons.LB)
		self.boardEmoticons.HideLine(self.boardEmoticons.L)
		
		self.textRenderer = self.TextRenderer()
		self.textRenderer.SetParent(self)
		self.textRenderer.SetPosition(20, 28)
		self.textRenderer.SetTargetName("")
		self.textRenderer.Show()

		self.resizeButton = self.ResizeButton()
		self.resizeButton.SetParent(self)
		self.resizeButton.SetSize(20, 20)
		self.resizeButton.SetPosition(280, 180)
		self.resizeButton.SetMoveEvent(ui.__mem_func__(self.ResizeWhisperDialog))
		self.resizeButton.Show()

		self.ResizeWhisperDialog()

	def Destroy(self):
		self.eventMinimize = None
		self.eventClose = None
		self.eventAcceptTarget = None
		self.ClearDictionary()
		self.scrollBar.Destroy()
		self.titleName = None
		self.titleNameEdit = None
		self.closeButton = None
		self.scrollBar = None
		self.chatLine = None
		self.sendButton = None
		self.acceptButton = None
		self.minimizeButton = None
		self.textRenderer = None
		self.board = None
		self.boardEmoticons = None
		self.editBar = None
		self.nameSlot = None
		self.resizeButton = None
		if self.emoticonsList:
			del self.emoticonsList[:]

	def SelectEmoticon(self, emoticonIdx):
		emoticonKeyList = ["|Eicon/emoticons/devil.tga|e", "|Eicon/emoticons/angel.tga|e", "|Eicon/emoticons/sunglasses.tga|e", "|Eicon/emoticons/heart.tga|e", "|Eicon/emoticons/tongue.tga|e", "|Eicon/emoticons/crying.tga|e", "|Eicon/emoticons/kiss.tga|e", "|Eicon/emoticons/smiley.tga|e"]
		
		self.chatLine.SetText("%s %s" % (self.chatLine.GetText(), emoticonKeyList[emoticonIdx]))
		self.chatLine.OnSetFocus()

	def ResizeWhisperDialog(self):
		(xPos, yPos) = self.resizeButton.GetLocalPosition()
		
		if xPos < 280:
			self.resizeButton.SetPosition(280, yPos)
			return
			
		if yPos < 150+15:
			self.resizeButton.SetPosition(xPos, 150+15)
			return
			
		self.SetWhisperDialogSize(xPos + 20, yPos + 20)

	def SetWhisperDialogSize(self, width, height):
		try:

			max = int((width-90)/6) * 3 - 6

			self.board.SetSize(width, height+15)
			self.scrollBar.SetPosition(width-25, 35)
			self.scrollBar.SetScrollBarSize(height-100+15)
			self.scrollBar.SetPos(1.0)
			self.editBar.SetSize(width-18, 50)
			self.chatLine.SetSize(width-90, 40)
			self.chatLine.SetLimitWidth(width-90)
			self.SetSize(width+ 40, height+15)

			if 0 != self.targetName:
				chat.SetBoxSize(self.targetName, width - 50, height - 90)

			self.textRenderer.SetPosition(20, 28)
			self.scrollBar.SetPosition(width-25, 35)
			self.editBar.SetPosition(10, height-60+15)
			self.sendButton.SetPosition(width-80, 10)

			self.boardEmoticons.SetPosition(self.board.GetWidth() - 17, 0)
			
			self.nameSlot.SetPosition(0, 10)
			self.acceptButton.SetPosition(0, 40)
			self.minimizeButton.SetPosition(width-42, 12)
			self.closeButton.SetPosition(width-24, 12)

			self.SetChatLineMax(max)
		except:
			import exception
			exception.Abort("WhisperDialog.SetWhisperDialogSize.BindObject")

	def SetChatLineMax(self, max):
		self.chatLine.SetMax(max)

		from grpText import GetSplitingTextLine

		text = self.chatLine.GetText()
		if text:
			self.chatLine.SetText(GetSplitingTextLine(text, max, 0))

	def OpenWithTarget(self, targetName):
		chat.CreateFloatingBox(targetName)
		chat.SetBoxSize(targetName, self.GetWidth() - 110, self.GetHeight() - 90)
		self.chatLine.SetFocus()
		self.titleName.SetText(targetName)
		self.targetName = targetName
		self.textRenderer.SetTargetName(targetName)
		self.titleNameEdit.Hide()
		self.acceptButton.Hide()
		

		
		self.minimizeButton.Show()
			
	def OpenWithoutTarget(self, event):
		self.eventAcceptTarget = event
		
		if self.titleName:
			self.titleName.SetText("")
		self.titleNameEdit.SetText("")
		self.titleNameEdit.SetFocus()
		self.targetName = 0
		self.titleNameEdit.Show()
		self.acceptButton.Show()
		self.minimizeButton.Hide()

	def Minimize(self):
		self.titleNameEdit.KillFocus()
		self.chatLine.KillFocus()
		self.Hide()

		if None != self.eventMinimize:
			self.eventMinimize(self.targetName)

	def Close(self):
		chat.ClearBox(self.targetName)
		self.titleNameEdit.KillFocus()
		self.chatLine.KillFocus()
		self.Hide()

		if None != self.eventClose:
			self.eventClose(self.targetName)

	def AcceptTarget(self):
		name = self.titleNameEdit.GetText()
		if len(name) <= 0:
			self.Close()
			return

		if None != self.eventAcceptTarget:
			self.titleNameEdit.KillFocus()
			self.eventAcceptTarget(name)

	def OnScroll(self):
		chat.SetBoxPosition(self.targetName, self.scrollBar.GetPos())

	def GetLinks(self, string, ret):
		def __IsAllowedLink(link):
			return link.find("https://go.twitch.tv") <> -1 or link.find("youtube.com") <> -1 or link.find("www.twitch.tv") <> -1 or link.find("youtu.be") <> -1 or link.find("etherion") <> -1 or link.find("vid.me") <> -1 or link.find("facebook.com") <> -1 or link.find("fb.me") <> -1

		links = re.findall("(?:(?:https?|ftp|file):\/\/|www\.|ftp\.)(?:\([-A-Z0-9+&@#/%=~_|$?!:,.]*\)|[-A-Z0-9+&@#/%=~_|$?!:,.])*(?:\([-A-Z0-9+&@#/%=~_|$?!:,.]*\)|[A-Z0-9+&@#/%=~_|$])", string, re.I)
		if not (hasattr(ret, "clear") and hasattr(ret, "update")):
			return False

		ret.clear()
		map(lambda link: (ret.update({link:"|cFF00C0FC|Hweb:%s|h[%s]|h|r"%(re.sub("://", "w<?", link), link)})) if link and __IsAllowedLink(link) else None, links)
		return len(links) > 0

	def SendWhisper(self):
		text = self.chatLine.GetText()
		textLength = len(text)
		

		if len(text) == 0:
			return

		links={}
		if self.GetLinks(text, links):
			for k,v in links.iteritems():
				text = text.replace(k, v)

		timeStamp = time.strftime("%H:%M:%S")
		if textLength > 0:
			if net.IsInsultIn(text):
				chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.CHAT_INSULT_STRING)
				return
				
			net.SendWhisperPacket(self.targetName, "|cFF8EC292|H|hLv. " + str(player.GetStatus(player.LEVEL) )+ "|h|r : " + text[0:])

			self.chatLine.SetText("")
			chat.AppendToBox(chat.WHISPER_TYPE_CHAT, self.targetName, player.GetName() + " |cFF8EC292|H|hLv. " + str(player.GetStatus(player.LEVEL)) + "|h|r : " + text[0:])

	def OnTop(self):
		if self.chatLine:
			self.chatLine.SetFocus()

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

	if app.ENABLE_RUN_MOUSE_WHEEL:
		def OnRunMouseWheel(self, nLen):
			x, y = self.GetMouseLocalPosition()
			if x <= 400:	
				if nLen > 0:
					self.scrollBar.OnUp()
				else:
					self.scrollBar.OnDown()

		def SetOnRunMouseWheelEvent(self, event):
			self.onRunMouseWheelEvent = __mem_func__(event)
