import ui, app, wndMgr, grp, game, net, chat, uiCommon, uiGuild, time, localeInfo, uiAffectShower

def pTableTranslate(i): 
	translate = {
					1	:	"[i] Are you sure you want this bonus?",
					2	:	"[i] You don't have a bonus selected!",
				}

	if translate.has_key(i):
		return translate[i]

BIOLOG_BINARY_LOADED = {
	"checkIndex"  : {
		0 : 0,
	},
}

TAKEN = -1

class CreateWindow:
	def _AppendSlot(self, parent, text, x, y, width, height):
		SlotBar = ui.SlotBar()
		if parent != None:
			SlotBar.SetParent(parent)
		SlotBar.SetSize(width, height)
		SlotBar.SetPosition(x, y)
		SlotBar.Show()
		textline = ui.TextLine()
		textline.SetParent(SlotBar)
		textline.SetPosition(5, 1)
		textline.SetText(text)
		textline.Show()
		return SlotBar, textline

	def _AppendTextLine(self, parent, textlineText, x, y, color):
		textline = ui.TextLine()
		if parent != None:
			textline.SetParent(parent)
		textline.SetPosition(x, y)
		if color != None:
			textline.SetFontColor(color[0], color[1], color[2])
		textline.SetText(textlineText)
		textline.Show()
		return textline

	def RGB(self, r, g, b):
		return (r*255, g*255, b*255)

class PremiumSelectAttribute(ui.ScriptWindow):
	def __init__(self):
		ui.ScriptWindow.__init__(self)
		self.dialogQuestion = uiCommon.QuestionDialog()
		self.createWindow = CreateWindow()
		self.__CreateDialog()

	def __del__(self):
		ui.ScriptWindow.__del__(self)

	def __CreateDialog(self):
		pyScrLoader = ui.PythonScriptLoader()
		pyScrLoader.LoadScriptFile(self, "uiscript/premium_selectrewards.py")
		getObject = self.GetChild
		self.board = getObject("Board")
		self.board.SetCloseEvent(self.CloseSelectReward)

		self.acceptButton = getObject("AcceptButton")
		self.TextLine_1 = getObject("TextLine_1")
		self.TextLine_2 = getObject("TextLine_2")
		self.TextLine_3 = getObject("TextLine_3")

		self.checkBoxTable	=	{
									0	:	[uiGuild.CheckBox(self, 288, 40, lambda arg = 0: self.SetType(arg)), 0, 0],
									1	:	[uiGuild.CheckBox(self, 288, 70, lambda arg = 1: self.SetType(arg)), 0, 0],
									2	:	[uiGuild.CheckBox(self, 288, 100, lambda arg = 2: self.SetType(arg)), 0, 0]
								}
		if self.acceptButton:
			self.acceptButton.SetEvent(ui.__mem_func__(self.GetDialogQuestion))	

		self.bonusValue = {}
		count = 0
		pos = 1 + 43
		while count < 3:
			self.bonusValue[count] = self.createWindow._AppendTextLine(self.board, '', 235, pos, self.createWindow.RGB(185, 218, 143))
			count = count + 1
			pos = pos + 30

		BIOLOG_BINARY_LOADED["checkIndex"][0] = 0
		self.index = 0

	def CloseSelectReward(self):
		if self.dialogQuestion:
			self.dialogQuestion.Close()
		self.ClearDictionary()
		self.board = None
		self.acceptButton = None
		self.cancelButton = None
		self.Hide()

	def SetType(self, arg):
		if TAKEN == arg:
			return
		if arg == 0:
			BIOLOG_BINARY_LOADED["checkIndex"][0] = 1
			self.checkBoxTable[2][0].SetCheck(0)
			self.checkBoxTable[1][0].SetCheck(0)
			self.checkBoxTable[0][0].SetCheck(1)
		elif arg == 1:
			BIOLOG_BINARY_LOADED["checkIndex"][0] = 2
			self.checkBoxTable[0][0].SetCheck(0)
			self.checkBoxTable[2][0].SetCheck(0)
			self.checkBoxTable[1][0].SetCheck(1)
		elif arg == 2:
			BIOLOG_BINARY_LOADED["checkIndex"][0] = 3
			self.checkBoxTable[0][0].SetCheck(0)
			self.checkBoxTable[1][0].SetCheck(0)
			self.checkBoxTable[2][0].SetCheck(1)

	def SetText(self, text, arg):
		if arg == 1:
			self.TextLine_1.SetText(text)
		elif arg == 2:
			self.TextLine_2.SetText(text)
		elif arg == 3:
			self.TextLine_3.SetText(text)
			
	def SetTitle(self, name):
		self.board.SetTitleName(name)

	def Open(self, index, arg):
		values = [
			[ localeInfo.TOOLTIP_APPLY_ATTBONUS_MONSTER, 10, 15, 25, 63 ],
			[ localeInfo.TOOLTIP_APPLY_ATTBONUS_METIN, 10, 15, 25, 110 ],
			[ localeInfo.TOOLTIP_APPLY_ATTBONUS_BOSS, 10, 15, 25, 111 ],
		]
		
		if arg == 3:
			if not uiAffectShower.PREMIUM_TYPE:
				return
				
			if uiAffectShower.CHOSEN_ATTRIBUTES[0] and uiAffectShower.CHOSEN_ATTRIBUTES[1]:
				return
				
			arg = uiAffectShower.PREMIUM_TYPE - 1
		# else:
			# if uiAffectShower.PREMIUM_TYPE:
				# return
		
		for x in xrange(3):
			self.bonusValue[x].SetText(values[x][0](values[x][arg + 1]))
			self.bonusValue[x].SetWindowHorizontalAlignRight()
			self.bonusValue[x].SetHorizontalAlignRight()
			self.bonusValue[x].SetPosition(94 if x < 1 else 87, 42 + (30 * x))
			
			if values[x][4] in uiAffectShower.CHOSEN_ATTRIBUTES:
				self.bonusValue[x].SetFontColor(0.9, 0.4745, 0.4627)
				global TAKEN
				TAKEN = x
			else:
				self.bonusValue[x].SetFontColor(0.5411, 0.7254, 0.5568)
				
		self.index = index
		self.Show()
		self.SetTop()
		self.SetCenterPosition()

	def _AcceptReward(self):
		net.SendChatPacket("/premium_extra %d %d" % (self.index, BIOLOG_BINARY_LOADED["checkIndex"][0] - 1))
		self.CloseSelectReward()

	def GetDialogQuestion(self):
		if BIOLOG_BINARY_LOADED["checkIndex"][0] != 0:
			self.dialogQuestion.SetWidth(300)
			self.dialogQuestion.SetText((pTableTranslate(1)))
			self.dialogQuestion.SetAcceptEvent(ui.__mem_func__(self._AcceptReward))
			self.dialogQuestion.SetCancelEvent(ui.__mem_func__(self._DeclineReward))
			self.dialogQuestion.Open()	
		else:
			chat.AppendChat(chat.CHAT_TYPE_INFO, (pTableTranslate(2)))

	def _DeclineReward(self):
		if self.dialogQuestion:
			self.dialogQuestion.Close()
