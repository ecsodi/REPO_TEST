import app
import thenewui as ui
import grp
import net
import guild
import messenger
import localeInfo
import constInfo
import uiToolTip
import uiGameOption

import uiCommon
from _weakref import proxy

FRIEND = 0
GUILD = 1
if app.ENABLE_COSTUME_SYSTEM:
	TEAM = 2
# if app.ENABLE_MESSENGER_INT:
	# INT = 3
# if app.ENABLE_MESSENGER_GFX:
	# GFX = 4
# BOT = 3

class MessengerItem(ui.Window):

	def __init__(self, getParentEvent):
		ui.Window.__init__(self)

		self.SetParent(getParentEvent())
		self.AddFlag("float")

		self.HideGrp = 0
		
		self.name = ""
		self.img = ui.ImageBox()
		self.img.AddFlag("not_pick")
		self.img.SetParent(self)
		self.img.SetPosition(-25,-10)
		self.img.Show()
		
		self.image = ui.ImageBox()
		self.image.AddFlag("not_pick")
		self.image.SetParent(self)
		self.image.SetPosition(-10,1)
		self.image.Show()
		
		self.text = ui.TextLine()
		self.text.SetParent(self)
		self.text.SetPosition(20, 6)
		self.text.Show()
		
		# self.selectedimg = ui.ImageBox()
		# self.selectedimg.SetParent(self)
		# self.selectedimg.SetPosition(-12, 0)
		# self.selectedimg.LoadImage("interface/messenger/selected_fill.tga")

		self.flag1 = ui.ImageBox()
		self.flag1.AddFlag("not_pick")
		self.flag1.SetParent(self)
		self.flag1.Hide()
		self.flag2 = ui.ImageBox()
		self.flag2.AddFlag("not_pick")
		self.flag2.SetParent(self)
		self.flag2.Hide()
		self.flag3 = ui.ImageBox()
		self.flag3.AddFlag("not_pick")
		self.flag3.SetParent(self)
		self.flag3.Hide()
		self.flag4 = ui.ImageBox()
		self.flag4.AddFlag("not_pick")
		self.flag4.SetParent(self)
		self.flag4.Hide()
		self.flagsimages = [self.flag1, self.flag2, self.flag3, self.flag4]

		self.lovePoint = -1
		self.lovePointToolTip = None

		self.isSelected = FALSE
		self.wasShowed = FALSE

		self.getParentEvent = getParentEvent

	def SetLast(self):
		self.img.LoadImage("interface/messenger/icon_prefix_last.tga")
		
	def SetShowed(self):
		self.wasShowed = TRUE

	def WasShowed(self):
		return self.wasShowed

	def SetName(self, name):
		self.name = name
		if name:
			self.text.SetText(name)
			self.SetSize(150, 25)

	# def SetFlags(self, f, name):
		# self.flags = f
		# if self.flags:
			# posx = 10
			# posy = 3
			# i = 0
			# for item in self.flags:
				# self.flagsimages[i].LoadImage("locale/ui/flag/%s.tga" % (item))
				# self.flagsimages[i].SetPosition(posx, posy)
				# self.flagsimages[i].Show()
				# posx += 20
				# i += 1

			# self.text.SetPosition(posx, 1)
			# self.SetSize(posx + 6*len(name), 16)

	def SetLovePoint(self, lovePoint):
		self.lovePoint = lovePoint

	def Select(self, type=1):
		self.isSelected = True
		self.HideGrp = 0
		if type != 0:
			# self.selectedimg.Show()
			self.HideGrp = 1

	def UnSelect(self):
		self.isSelected = False
		# self.selectedimg.Hide()
		
	def GetName(self):
		return self.name

	def GetStepWidth(self):
		return 0

	# Whisper
	def CanWhisper(self):
		return False

	def IsOnline(self):
		return False

	def OnWhisper(self):
		pass

	# Remove
	def CanRemove(self):
		return False

	def OnRemove(self):
		return False

	# Warp
	def CanWarp(self):
		return False

	def OnWarp(self):
		pass

	def OnMouseOverIn(self):
		if -1 != self.lovePoint:
			if not self.lovePointToolTip:
				self.lovePointToolTip = uiToolTip.ToolTip(100)
				self.lovePointToolTip.SetTitle(self.name)
				self.lovePointToolTip.AppendTextLine(localeInfo.AFF_LOVE_POINT % (self.lovePoint))
				self.lovePointToolTip.ResizeToolTip()
			self.lovePointToolTip.ShowToolTip()

	def OnMouseOverOut(self):
		if self.lovePointToolTip:
			self.lovePointToolTip.HideToolTip()

	def OnMouseLeftButtonDown(self):
		self.getParentEvent().OnSelectItem(self)

	def OnMouseLeftButtonDoubleClick(self):
		self.getParentEvent().OnDoubleClickItem(self)

	def OnRender(self):
		if self.isSelected:
			x, y = self.GetGlobalPosition()
			grp.SetColor(grp.GenerateColor(0.153,0.231,0.275, 0.7))
			grp.RenderBar(x+13, y, self.GetWidth()-20, self.GetHeight())

class MessengerMemberItem(MessengerItem):

	STATE_OFFLINE = 0
	STATE_ONLINE = 1

	IMAGE_FILE_NAME = {	"ONLINE" : "d:/ymir work/ui/game/comp/mes/online.tga",
						"OFFLINE" : "d:/ymir work/ui/game/comp/mes/offline.tga",}

	def __init__(self, getParentEvent):
		MessengerItem.__init__(self, getParentEvent)
		self.key = None
		self.state = self.STATE_OFFLINE
		self.Offline()

	def GetStepWidth(self):
		return 17

	def SetKey(self, key):
		self.key = key

	def IsSameKey(self, key):
		return self.key == key

	def IsOnline(self):
		if self.STATE_ONLINE == self.state:
			return True

		return False

	def Online(self):
		self.img.LoadImage("d:/ymir work/ui/game/comp/mes/icon_prefix_last.tga")
		self.image.LoadImage(self.IMAGE_FILE_NAME["ONLINE"])
		# self.text.SetPackedFontColor(0xffa08784)
		self.state = self.STATE_ONLINE

	def Offline(self):
		self.image.LoadImage(self.IMAGE_FILE_NAME["OFFLINE"])
		self.state = self.STATE_OFFLINE
		# self.text.SetPackedFontColor(0xff757170)
		self.img.LoadImage("d:/ymir work/ui/game/comp/mes/icon_prefix_last.tga")

	def CanWhisper(self):
		if self.IsOnline():
			return True

		return False

	def OnWhisper(self):
		if self.IsOnline():
			self.getParentEvent().whisperButtonEvent(self.GetName())

	def Select(self):
		MessengerItem.Select(self)

class MessengerGroupItem(MessengerItem):

	IMAGE_FILE_NAME = {	"OPEN" : "d:/ymir work/ui/game/comp/mes/not_expanded2.png",
						"CLOSE" : "d:/ymir work/ui/game/comp/mes/expanded2.png", }

	def __init__(self, getParentEvent):
		self.isOpen = False
		self.memberList = []

		self.count = 0
		MessengerItem.__init__(self, getParentEvent)

	def AppendMember(self, member, key, name):
		member.SetKey(key)
		member.SetName(name)
		self.memberList.append(member)
		return member

	def RemoveMember(self, item):
		for i in xrange(len(self.memberList)):
			if item == self.memberList[i]:
				del self.memberList[i]
				return

	def ClearMember(self):
		self.memberList = []

	def FindMember(self, key):
		list = filter(lambda argMember, argKey=key: argMember.IsSameKey(argKey), self.memberList)
		if list:
			return list[0]

		return None

	def GetLoginMemberList(self):
		return filter(MessengerMemberItem.IsOnline, self.memberList)

	def GetLogoutMemberList(self):
		return filter(lambda arg: not arg.IsOnline(), self.memberList)

	def IsOpen(self):
		return self.isOpen

	def Open(self):
		self.image.LoadImage(self.IMAGE_FILE_NAME["OPEN"])
		self.isOpen = True

	def Close(self):
		self.image.LoadImage(self.IMAGE_FILE_NAME["CLOSE"])
		self.isOpen = False

		map(ui.Window.Hide, self.memberList)

	def Select(self):

		if self.IsOpen():
			self.Close()
		else:
			self.Open()

		MessengerItem.Select(self, 0)
		self.getParentEvent().OnRefreshList()

class MessengerFriendItem(MessengerMemberItem):

	def __init__(self, getParentEvent):
		MessengerMemberItem.__init__(self, getParentEvent)

	def CanRemove(self):
		return True

	def OnRemove(self):
		messenger.RemoveFriend(self.key)
		net.SendMessengerRemovePacket(self.key, self.name)
		return True

class MessengerGuildItem(MessengerMemberItem):

	def __init__(self, getParentEvent):
		MessengerMemberItem.__init__(self, getParentEvent)

	def CanWarp(self):
		if not self.IsOnline():
			return False
		return True

	def OnWarp(self):
		net.SendGuildUseSkillPacket(155, self.key)

	def CanRemove(self):
		for i in xrange(guild.ENEMY_GUILD_SLOT_MAX_COUNT):
			if guild.GetEnemyGuildName(i) != "":
				return False

		if guild.MainPlayerHasAuthority(guild.AUTH_REMOVE_MEMBER):
			if guild.IsMemberByName(self.name):
				return True

		return False

	def OnRemove(self):
		net.SendGuildRemoveMemberPacket(self.key)
		return True

class MessengerFriendGroup(MessengerGroupItem):

	def __init__(self, getParentEvent):
		MessengerGroupItem.__init__(self, getParentEvent)
		self.SetName(localeInfo.MESSENGER_FRIEND)
		
	def SetMembers(self, on, off):
		self.SetName("%s (%d on/ %d off)" % (localeInfo.MESSENGER_FRIEND , on, off))

	def AppendMember(self, key, name):
		item = MessengerFriendItem(self.getParentEvent)
		return MessengerGroupItem.AppendMember(self, item, key, name)

if app.ENABLE_COSTUME_SYSTEM:
	class MessengerTeamGroup(MessengerGroupItem):
		def __init__(self, getParentEvent):
			MessengerGroupItem.__init__(self, getParentEvent)
			self.SetName(localeInfo.MESSENGER_TEAM)
			self.AddFlag("float")
			
		def SetMembers(self, on, off):
			self.SetName("%s (%d online)" % (localeInfo.MESSENGER_TEAM , on))

		def AppendMember(self, key, name):
			item = MessengerMemberItem(self.getParentEvent)
			return MessengerGroupItem.AppendMember(self, item, key, name)

# class MessengerBotItem(MessengerMemberItem):

	# def __init__(self, getParentEvent):
		# MessengerMemberItem.__init__(self, getParentEvent)

	# def CanRemove(self):
		# return False

	# def OnRemove(self):
		# messenger.RemoveFriend(self.key)
		# net.SendMessengerRemovePacket(self.key, self.name)
		# return False

# class MessengerBotGroup(MessengerGroupItem):
	# def __init__(self, getParentEvent):
		# MessengerGroupItem.__init__(self, getParentEvent)
		# self.SetName("Server Info")

	# def SetMembers(self, on, off):
		# pass
		
	# def AppendMember(self, key, name):
		# item = MessengerBotItem(self.getParentEvent)
		# return MessengerGroupItem.AppendMember(self, item, key, name)

class MessengerGuildGroup(MessengerGroupItem):

	def __init__(self, getParentEvent):
		MessengerGroupItem.__init__(self, getParentEvent)
		self.SetName(localeInfo.MESSENGER_GUILD)
		self.AddFlag("float")

	def SetMembers(self, on, off):
		self.SetName("%s (%d on/ %d off)" % (localeInfo.MESSENGER_GUILD , on, off))
		
	def AppendMember(self, key, name):
		item = MessengerGuildItem(self.getParentEvent)
		return MessengerGroupItem.AppendMember(self, item, key, name)

class MessengerFamilyGroup(MessengerGroupItem):

	def __init__(self, getParentEvent):
		MessengerGroupItem.__init__(self, getParentEvent)
		self.SetName(localeInfo.MESSENGER_FAMILY)
		self.AddFlag("float")

		self.lover = None
		
	def SetMembers(self, on, off):
		pass
		
	def AppendMember(self, key, name):
		item = MessengerGuildItem(self.getParentEvent)
		self.lover = item
		return MessengerGroupItem.AppendMember(self, item, key, name)

	def GetLover(self):
		return self.lover

class MessengerWindow(ui.ScriptWindow):

	START_POSITION = 30

	# class ResizeButton(ui.DragButton):

		# def OnMouseOverIn(self):
			# app.SetCursor(app.VSIZE)

		# def OnMouseOverOut(self):
			# app.SetCursor(app.NORMAL)

	def __init__(self):
		ui.ScriptWindow.__init__(self)
		messenger.SetMessengerHandler(self)

		self.board = None
		self.groupList = []
		self.imgList = []
		self.showingItemList = []
		self.selectedItem = None
		self.whisperButtonEvent = lambda *arg: None
		self.familyGroup = None
		self.interface = None

		self.guildButtonEvent = None

		self.showingPageSize = 0
		self.startLine = 0

		self.isLoaded = 0

		self.__AddGroup()
		messenger.RefreshGuildMember()

	def Show(self):
		if self.isLoaded==0:
			self.isLoaded=1

			self.__LoadWindow()
			self.OnRefreshList()
			#self.OnResizeDialog()
			if app.ENABLE_COSTUME_SYSTEM:
				self.RefreshTeamState()
				
		ui.ScriptWindow.Show(self)

	def __LoadWindow(self):

		pyScrLoader = ui.PythonScriptLoader()
		pyScrLoader.LoadScriptFile(self, "UIScript/MessengerWindow.py")

		try:
			self.board = self.GetChild("board")
			self.whisperButton = self.GetChild("WhisperButton")
			self.removeButton = self.GetChild("RemoveButton")
			self.addFriendButton = self.GetChild("AddFriendButton")
			self.guildButton = self.GetChild("GuildButton")
			self.borderNew2 = self.GetChild("Board_Name2")
			self.borderNew3 = self.GetChild("Board_Name")
		except:
			import exception
			exception.Abort("MessengerWindow.__LoadWindow.__Bind")

		self.board.SetCloseEvent(ui.__mem_func__(self.Close))
		self.whisperButton.SetEvent(ui.__mem_func__(self.OnPressWhisperButton))
		self.removeButton.SetEvent(ui.__mem_func__(self.OnPressRemoveButton))
		self.addFriendButton.SetEvent(ui.__mem_func__(self.OnPressAddFriendButton))
		self.guildButton.SetEvent(ui.__mem_func__(self.OnPressGuildButton))

		width = self.GetWidth()
		height = self.GetHeight()
		self.addFriendButton.SetPosition(-65, 39)
		self.whisperButton.SetPosition(-25, 39)
		self.removeButton.SetPosition(15, 39)
		self.guildButton.SetPosition(55, 39)
		
		self.testScrollBar = ui.ScrollBar()
		self.testScrollBar.SetParent(self)
		self.testScrollBar.SetPosition(185, 31)
		self.testScrollBar.SetScrollEvent(ui.__mem_func__(self.OnScroll))
		self.testScrollBar.SetSize(15, 150)
		self.testScrollBar.SetMiddleBarSize(0.6)
		self.testScrollBar.SetScrollBarSize(257)
		self.testScrollBar.Show()

		self.whisperButton.Disable()
		self.removeButton.Disable()

		for list in self.groupList:
			list.SetTop()

	def __del__(self):
		messenger.SetMessengerHandler(None)
		ui.ScriptWindow.__del__(self)

	def Destroy(self):
		self.board = None
		self.testScrollBar = None
		self.friendNameBoard = None
		self.questionDialog = None
		self.popupDialog = None
		self.inputDialog = None
		self.familyGroup = None
		self.interface = None

		self.whisperButton = None
		self.removeButton = None

	def OnCloseQuestionDialog(self):
		self.questionDialog.Close()
		self.questionDialog = None
		return True

	def Close(self):
		self.questionDialog = None
		self.Hide()

	def SetSize(self, width, height):
		ui.ScriptWindow.SetSize(self, width, height)
		if self.board:
			self.board.SetSize(width, height)
			
	def __LocateMember(self):

		if self.isLoaded==0:
			return

		if (self.showingPageSize/20)-1 >= len(self.showingItemList):
			self.testScrollBar.Hide()
			self.startLine = 0
		else:
			# if self.showingItemList:
				# self.testScrollBar.SetMiddleBarSize(float(self.showingPageSize/20) / float(len(self.showingItemList)))
			self.testScrollBar.Show()

		#####

		yPos = self.START_POSITION
		heightLimit = self.GetHeight() - (self.START_POSITION + 13)-20

		map(ui.Window.Hide, self.showingItemList)

		
		for item in self.showingItemList[self.startLine:]:
			item.SetPosition(20 + item.GetStepWidth(), yPos)
			item.SetTop()
			item.Show()

			yPos += 30
			if yPos > heightLimit:
				break
		# self.testScrollBar.Hide()

	def OnRunMouseWheel(self, nLen):
		if nLen > 0:
			self.testScrollBar.OnUp()
		else:
			self.testScrollBar.OnDown()

	def __AddGroup(self):
		member = MessengerFriendGroup(ui.__mem_func__(self.GetSelf))
		member.Open()
		member.Show()
		self.groupList.append(member)

		member = MessengerGuildGroup(ui.__mem_func__(self.GetSelf))
		member.Open()
		member.Show()
		self.groupList.append(member)

		if app.ENABLE_COSTUME_SYSTEM:
			member = MessengerTeamGroup(ui.__mem_func__(self.GetSelf))
			member.Open()
			member.Show()
			self.groupList.append(member)

		# member = MessengerBotGroup(ui.__mem_func__(self.GetSelf))
		# member.Open()
		# member.Show()
		# self.BotGroup = member
		# self.groupList.append(member)

	def __AddFamilyGroup(self):
		member = MessengerFamilyGroup(ui.__mem_func__(self.GetSelf))
		member.Open()
		member.Show()

		self.familyGroup = member

	def ClearGuildMember(self):
		self.groupList[GUILD].ClearMember()

	def SetWhisperButtonEvent(self, event):
		self.whisperButtonEvent=event

	def SetGuildButtonEvent(self, event):
		self.guildButtonEvent=event
		
	def OnPressGuildButton(self):
		self.guildButtonEvent()

	def OnPressAddFriendButton(self):
		friendNameBoard = uiCommon.InputDialog()
		friendNameBoard.SetMaxLength(localeInfo.CHARACTER_NAME_MAX_LEN)
		friendNameBoard.SetTitle(localeInfo.MESSENGER_ADD_FRIEND)
		friendNameBoard.SetAcceptEvent(ui.__mem_func__(self.OnAddFriend))
		friendNameBoard.SetCancelEvent(ui.__mem_func__(self.OnCancelAddFriend))
		friendNameBoard.Open()
		self.friendNameBoard = friendNameBoard

	def OnAddFriend(self):
		text = self.friendNameBoard.GetText()
		if text:
			net.SendMessengerAddByNamePacket(text)
		self.friendNameBoard.Close()
		self.friendNameBoard = None
		return True

	def OnCancelAddFriend(self):
		self.friendNameBoard.Close()
		self.friendNameBoard = None
		return True

	def OnPressWhisperButton(self):
		if self.selectedItem:
			self.selectedItem.OnWhisper()

	def OnPressRemoveButton(self):
		if self.selectedItem:
			if self.selectedItem.CanRemove():
				self.questionDialog = uiCommon.QuestionDialog()
				self.questionDialog.SetText(localeInfo.MESSENGER_DO_YOU_DELETE)
				self.questionDialog.SetAcceptEvent(ui.__mem_func__(self.OnRemove))
				self.questionDialog.SetCancelEvent(ui.__mem_func__(self.OnCloseQuestionDialog))
				self.questionDialog.Open()

	def OnRemove(self):
		if self.selectedItem:
			if self.selectedItem.CanRemove():
				map(lambda arg, argDeletingItem=self.selectedItem: arg.RemoveMember(argDeletingItem), self.groupList)
				self.selectedItem.OnRemove()
				self.selectedItem.UnSelect()
				self.selectedItem = None
				self.OnRefreshList()

		self.OnCloseQuestionDialog()

	def OnScroll(self):
		scrollLineCount = len(self.showingItemList) - (self.showingPageSize/20)
		startLine = int(scrollLineCount * self.testScrollBar.GetPos())

		if startLine != self.startLine:
			self.startLine = startLine
			self.__LocateMember()

	def OnPressEscapeKey(self):
		self.Close()
		return True

	## CallBack
	def OnSelectItem(self, item):

		if self.selectedItem:
			if item != self.selectedItem:
				self.selectedItem.UnSelect()

		self.selectedItem = item

		if self.selectedItem:
			self.selectedItem.Select()

			if self.selectedItem.CanWhisper():
				self.whisperButton.Enable()
			else:
				self.whisperButton.Disable()
				
			if self.selectedItem.CanRemove():
				self.removeButton.Enable()
			else:
				self.removeButton.Disable()

	def OnDoubleClickItem(self, item):

		if not self.selectedItem:
			return

		if self.selectedItem.IsOnline():
			self.OnPressWhisperButton()

	def GetSelf(self):
		return self

	def OnRefreshList(self):
		self.showingItemList = []

		if self.familyGroup:
			self.showingItemList.append(self.familyGroup)
			if self.familyGroup.GetLover():
				self.showingItemList.append(self.familyGroup.GetLover())

		for group in self.groupList:

			self.showingItemList.append(group)

			if group.IsOpen():

				loginMemberList = group.GetLoginMemberList()
				logoutMemberList = group.GetLogoutMemberList()

				if loginMemberList or logoutMemberList:
					for member in loginMemberList:
						self.showingItemList.append(member)
					for member in logoutMemberList:
						self.showingItemList.append(member)
						
					group.SetMembers(len(loginMemberList), len(logoutMemberList))
					
				else:
					item = MessengerItem(ui.__mem_func__(self.GetSelf))
					item.SetName(localeInfo.MESSENGER_EMPTY_LIST)
					self.showingItemList.append(item)

		self.__LocateMember()

	def RefreshMessenger(self):
		self.OnRefreshList()
	
	def BindInterface(self, interface):
		self.interface = proxy(interface)
		
	## EventHandler
	def __AddList(self, groupIndex, key, name):
		group = self.groupList[groupIndex]
		member = group.FindMember(key)
		if not member:
			member = group.AppendMember(key, name)
			self.OnSelectItem(None)
		return member

	def OnRemoveList(self, groupIndex, key):
		group = self.groupList[groupIndex]
		group.RemoveMember(group.FindMember(key))
		self.OnRefreshList()

	def OnRemoveAllList(self, groupIndex):
		group = self.groupList[groupIndex]
		group.ClearMember()
		self.OnRefreshList()

	def OnLogin(self, groupIndex, key, name=None):
		if not name:
			name = key
		group = self.groupList[groupIndex]
		member = self.__AddList(groupIndex, key, name)
		member.SetName(name)
		
		member.Online()
		self.OnRefreshList()
		
		if name != constInfo.BOT_NAME:
			self.interface.LoadAppLeftTip(name, "FRIEND")
		
	def OpenWhisper(self, eventType, userName):
		self.whisperButtonEvent(userName)

	def OnLogout(self, groupIndex, key, name=None):
		group = self.groupList[groupIndex]
		member = self.__AddList(groupIndex, key, name)
		if not name:
			name = key
		member.SetName(name)
		member.Offline()
		self.OnRefreshList()

	def OnAddLover(self, name, lovePoint):
		if not self.familyGroup:
			self.__AddFamilyGroup()

		member = self.familyGroup.AppendMember(0, name)

		member.SetName(name)
		member.SetLovePoint(lovePoint)
		member.Offline()
		self.OnRefreshList()

	def OnUpdateLovePoint(self, lovePoint):
		if not self.familyGroup:
			return

		lover = self.familyGroup.GetLover()
		if not lover:
			return

		lover.SetLovePoint(lovePoint)

	def OnLoginLover(self):
		if not self.familyGroup:
			return

		lover = self.familyGroup.GetLover()
		if not lover:
			return

		lover.Online()

	def OnLogoutLover(self):
		if not self.familyGroup:
			return

		lover = self.familyGroup.GetLover()
		if not lover:
			return

		lover.Offline()

	def ClearLoverInfo(self):
		if not self.familyGroup:
			return

		self.familyGroup.ClearMember()
		self.familyGroup = None
		self.OnRefreshList()

	if app.ENABLE_COSTUME_SYSTEM:
		def RefreshTeamState(self):
			group = self.groupList[TEAM]
