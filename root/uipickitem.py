import wndMgr
import thenewui as ui
import ime
import localeInfo
import re
import player
import item
import chat

class PickItemDialog(ui.ScriptWindow):
	def __init__(self):
		ui.ScriptWindow.__init__(self)

		self.unitValue = 1
		self.maxValue = 0
		self.eventAccept = 0
		self.itemVnumPrice = 0
		self.moneyValueTest = 0
		self.itemVnumCount = 0
		self.itemPrice = 0

	def __del__(self):
		ui.ScriptWindow.__del__(self)

	def LoadDialog(self):
		try:
			pyScrLoader = ui.PythonScriptLoader()
			pyScrLoader.LoadScriptFile(self, "UIScript/pickitemdialog.py")
		except:
			import exception
			exception.Abort("PickItemDialog.LoadDialog.LoadScript")

		try:
			self.board = self.GetChild("board")
			self.itemValueTextLine = self.GetChild("item_value")
			self.maxValueTextLine = self.GetChild("max_value")
			self.pickValueEditLine = self.GetChild("money_value")
			self.acceptButton = self.GetChild("accept_button")
			self.cancelButton = self.GetChild("cancel_button")
		except:
			import exception
			exception.Abort("PickItemDialog.LoadDialog.BindObject")
			
		self.pickValueEditLine.OnIMEUpdate = ui.__mem_func__(self.__OnValueUpdate)
		self.pickValueEditLine.SetReturnEvent(ui.__mem_func__(self.OnAccept))
		self.pickValueEditLine.SetEscapeEvent(ui.__mem_func__(self.Close))
		self.acceptButton.SetEvent(ui.__mem_func__(self.OnAccept))
		self.cancelButton.SetEvent(ui.__mem_func__(self.Close))
		self.board.SetCloseEvent(ui.__mem_func__(self.Close))

	def Destroy(self):
		self.ClearDictionary()
		self.eventAccept = 0
		self.maxValue = 0
		self.moneyValueTest = 0
		self.itemVnumPrice = 0
		self.itemVnumCount = 0
		self.itemPrice = 0
		self.pickValueEditLine = 0
		self.acceptButton = 0
		self.cancelButton = 0
		self.board = None

	def SetTitleName(self, text):
		self.board.SetTitleName(text)

	def SetAcceptEvent(self, event):
		self.eventAccept = event

	def SetMax(self, max):
		self.pickValueEditLine.SetMax(max)

	def SetItem(self, vNum, itemCount, itemPrice):
		item.SelectItem(vNum)
		self.itemVnumPrice = itemPrice
		self.itemVnumCount = itemCount
		# chat.AppendChat(1, "item vnum set : %d and count %d with price %d" % (vNum, self.itemVnumCount, self.itemVnumPrice))

	def Open(self, maxValue, unitValue=1):
		width = self.GetWidth()
		(mouseX, mouseY) = wndMgr.GetMousePosition()

		if mouseX + width/2 > wndMgr.GetScreenWidth():
			xPos = wndMgr.GetScreenWidth() - width
		elif mouseX - width/2 < 0:
			xPos = 0
		else:
			xPos = mouseX - width/2
			
		self.itemPrice = 0

		self.SetPosition(xPos - 200, mouseY - self.GetHeight() + 50)

		self.maxValueTextLine.SetText(" / " + str(localeInfo.AddPointToNumberString(maxValue)))

		self.pickValueEditLine.SetText(str(unitValue))
		self.pickValueEditLine.SetFocus()

		ime.SetCursorPosition(1)

		self.unitValue = unitValue
		self.maxValue = maxValue
		self.Show()
		self.SetTop()

	def __OnValueUpdate(self):
		ui.EditLine.OnIMEUpdate(self.pickValueEditLine)

		self.moneyValueTest = self.pickValueEditLine.GetText()
		if self.pickValueEditLine.GetText() == "":
			self.moneyValueTest = 0
		self.itemPrice = int(self.itemVnumPrice) * int(self.moneyValueTest)
		self.itemValueTextLine.SetText(localeInfo.TOOLTIP_SELLPRICE % localeInfo.NumberToGoldString(int(self.itemPrice)))
		# chat.AppendChat(1, "%d" % int(self.itemPrice))

	def Close(self):
		self.pickValueEditLine.KillFocus()
		self.Hide()
		
	def __ConvertMoneyText(self, text, powers=dict(k=10**3, m=10**6, b=10**9)):
		match = re.search(r'(\d+)({:s}+)?'.format('+|'.join(powers.keys())), text, re.I)
		if match:
			moneyValue, suffixName = match.groups()
			moneyValue = int(moneyValue)
			if not suffixName:
				return moneyValue

			return moneyValue * (powers[suffixName[0]] ** len(suffixName))

		return 0

	# def OnUpdate(self):
		# if self.pickValueEditLine.GetText() > 100:
			# self.pickValueEditLine.SetText("100")
		# self.moneyValueTest = self.pickValueEditLine.GetText()

		# self.itemPrice = self.itemVnumPrice * self.moneyValueTest
		# self.itemValueTextLine.SetText(localeInfo.TOOLTIP_SELLPRICE % localeInfo.NumberToGoldString(int(self.itemPrice)))
		# chat.AppendChat(1, "OnUpdate: price tst %d" % moneyValue)

	def OnAccept(self):
		text = self.pickValueEditLine.GetText()
		
		if text:
			moneyValue = min(self.__ConvertMoneyText(text), self.maxValue)
			
			if moneyValue:
				if self.eventAccept:
					self.eventAccept(moneyValue)

		self.Close()
		
