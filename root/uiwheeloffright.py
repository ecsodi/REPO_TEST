import thenewui as ui
import app
import net
import chat
import uiToolTip
import item
import uiScriptLocale
import localeInfo

class WheelOfFrightWindow(ui.ScriptWindow):
	def __init__(self):
		ui.ScriptWindow.__init__(self)
		self.__LoadWindow()
		self.tooltipItem = None
		self.itemsArr = []
		self.spin = False
		self.spins = 0
		self.degree = 0
		self.endDegree = 0
		self.totalDegree = 0
		self.successWnd = None

	def __del__(self):
		ui.ScriptWindow.__del__(self)

	def __LoadWindow(self):
		try:
			pyScrLoader = ui.PythonScriptLoader()
			pyScrLoader.LoadScriptFile(self, "uiscript/wheeloffright.py")
		except:
			import exception
			exception.Abort("WheelOfFrightWindow.LoadWindow.LoadObject")

		try:
			self.GetChild("TitleBar").SetCloseEvent(ui.__mem_func__(self.Close))
			self.pointer = self.GetChild("WheelPointer")
			self.pointer.OnMouseLeftButtonDown = ui.__mem_func__(self.StartSpin)
			self.pointer.Hide()
			self.startBtn = self.GetChild("WheelStartButton")
			self.startBtn.SAFE_SetEvent(self.StartSpin)
			self.itemSlots = self.GetChild("ItemSlots")
			self.itemSlots.SetOverInItemEvent(ui.__mem_func__(self.__OnOverInItem))
			self.itemSlots.SetOverOutItemEvent(ui.__mem_func__(self.__OnOverOutItem))
		except:
			import exception
			exception.Abort("WheelOfFrightWindow.LoadWindow.BindObject")

		self.sliceImgList = []
		for x in xrange(10):
			img = self.GetChild("Slice%d" % (x + 1))
			img.SetAlpha(0.0)
			img.Show()
			self.sliceImgList.append(img)

		start, end, add = -18, 18, 36
		self.slicesPos = []
		for x in xrange(10):
			dX = start + (add * x)
			dY = end + (add * x)
			dA = dX + end
			self.slicesPos.append([dX, dY, dA])
	
	def Show(self):
		self.SetTop()
		self.SetCenterPosition()
		ui.ScriptWindow.Show(self)

	def StartSpin(self):
		if self.spin:
			return
	
		net.SendChatPacket("/halloween_minigame")
		self.Reset()

	def Spin(self, spins, items):
		self.pointer.Show()
		self.startBtn.Hide()
		self.spins = spins
		self.spin = True
		self.degree = 0
		self.endDegree = app.GetRandom(-12, 12) + spins * 36
		self.totalDegree = 0

		itemList = items.split("#")
		x = 0
		self.itemsArr = []
		for item in itemList:
			try:
				vnum, count = item.split("|")
				self.itemSlots.SetItemSlot(x, int(vnum), int(count))
				self.itemsArr.append([int(vnum), int(count)])
				x += 1
			except Exception:
				pass

	def RenderSlices(self):
		for i in range(len(self.sliceImgList)):
			if self.degree >= self.slicesPos[i][0] and self.degree <= self.slicesPos[i][1]:
				self.sliceImgList[i].SetAlpha(1.0)
			else:
				self.sliceImgList[i].SetAlpha(0.0)

	def OnUpdate(self):
		if not self.spin:
			return

		self.pointer.SetRotation(self.degree)
		self.RenderSlices()

		slice1 = 36
		move = 0

		if self.totalDegree + slice1*4 >= self.endDegree:
			move = 0.7
		if self.totalDegree + slice1*6 >= self.endDegree:
			move = 1
		elif self.totalDegree + slice1*10 >= self.endDegree:
			move = 2
		elif self.totalDegree + slice1*18 >= self.endDegree:
			move = 3
		elif self.totalDegree + slice1*30 >= self.endDegree:
			move = 4
		else:
			move = 5

		self.degree += move
		self.totalDegree += move

		if self.degree >= 360 - 18:
			self.degree = -18

		if self.totalDegree >= self.endDegree:
			self.spin = False
			idx = self.spins - int(self.spins / 10)*10
			
			net.SendChatPacket("/wheel_minigame_collect")

	def __OnOverInItem(self, slotIndex):
		if self.tooltipItem:
			self.tooltipItem.SetItemToolTip(self.itemsArr[slotIndex][0])

	def __OnOverOutItem(self):
		if self.tooltipItem:
			self.tooltipItem.HideToolTip()

	def Open(self):
		self.Show()

	def Close(self):
		self.Hide()

	def OnPressEscapeKey(self):
		self.Close()
		return True

	def Reset(self):
		self.pointer.Hide()
		self.startBtn.Show()

	def Destroy(self):
		self.ClearDictionary()
		self.pointer = None
		self.itemSlots = None
		self.sliceImgList = []
		self.spins = 0
		self.itemsArr = []
		self.successWnd = None
		self.tooltipItem = None
	
	def SetItemToolTip(self, itemTooltip):
		self.tooltipItem = itemTooltip
