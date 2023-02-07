import thenewui as ui
import grp
import localeInfo
import app
import time
import systemSetting
import wndMgr, constInfo, chat
import CacheEffect as player
from _weakref import proxy

class TextBar(ui.Window):
	def __init__(self, width, height):
		ui.Window.__init__(self)
		self.handle = grp.CreateTextBar(width, height)

	def __del__(self):
		ui.Window.__del__(self)
		grp.DestroyTextBar(self.handle)

	def ClearBar(self):
		grp.ClearTextBar(self.handle)

	def SetClipRect(self, x1, y1, x2, y2):
		grp.SetTextBarClipRect(self.handle, x1, y1, x2, y2)

	def TextOut(self, x, y, text):
		grp.TextBarTextOut(self.handle, x, y, text)

	def OnRender(self):
		x, y = self.GetGlobalPosition()
		grp.RenderTextBar(self.handle, x, y)

	def SetTextColor(self, r, g, b):
		grp.TextBarSetTextColor(self.handle, r, g, b)

	def GetTextExtent(self, text):
		return grp.TextBarGetTextExtent(self.handle, text)

class TipBoard(ui.Bar):

	SCROLL_WAIT_TIME = 3.0
	TIP_DURATION = 4.0
	STEP_HEIGHT = 19

	def __init__(self):
		ui.Bar.__init__(self)

		self.AddFlag("not_pick")
		self.tipList = []
		self.curPos = 0
		self.dstPos = 0
		self.nextScrollTime = 0

		#self.width = wndMgr.GetScreenWidth()

		self.SetPosition(0, 105)
		self.SetSize(systemSetting.GetWidth(), 35)
		self.SetColor(grp.GenerateColor(0.0, 0.0, 0.0, 0.4))
		self.SetWindowHorizontalAlignCenter()

		self.__CreateTextBar()

	def __del__(self):
		ui.Bar.__del__(self)

	def __CreateTextBar(self):

		x, y = self.GetGlobalPosition()

		self.textBar = BigTextBar(wndMgr.GetScreenWidth(), 300, 18)
		self.textBar.SetParent(self)
		self.textBar.SetClipRect(0, y+10, systemSetting.GetWidth(), y+31)
		self.textBar.SetTextColor(255, 230, 186)
		self.textBar.Show()

	def __CleanOldTip(self):
		leaveList = []
		for tip in self.tipList:
			madeTime = tip[0]
			if app.GetTime() - madeTime > self.TIP_DURATION:
				pass
			else:
				leaveList.append(tip)

		self.tipList = leaveList

		if not leaveList:
			self.textBar.ClearBar()
			self.Hide()
			return

		self.__RefreshBoard()

	def __RefreshBoard(self):

		self.textBar.ClearBar()

		index = 0
		for tip in self.tipList:
			text = tip[1]
			(text_width, text_height) = self.textBar.GetTextExtent(text)
			self.textBar.TextOut((systemSetting.GetWidth() - text_width)/2, index*self.STEP_HEIGHT, text)
			index += 1

	def SetTip(self, text):

		if not app.IsVisibleNotice():
			return
			
		text = constInfo.StripColor(text)
		text = constInfo.StripHyperlink(text)

		curTime = app.GetTime()
		self.tipList.append((curTime, text))
		self.__RefreshBoard()

		self.nextScrollTime = app.GetTime() + 1.0

		if not self.IsShow():
			self.curPos = -self.STEP_HEIGHT
			self.dstPos = -self.STEP_HEIGHT
			(text_width, text_height) = self.textBar.GetTextExtent(text)
			self.textBar.SetPosition((systemSetting.GetWidth() - text_width)/2, 10 - self.curPos)
			self.Show()

	def OnUpdate(self):

		if not self.tipList:
			self.Hide()
			return

		if app.GetTime() > self.nextScrollTime:
			self.nextScrollTime = app.GetTime() + self.SCROLL_WAIT_TIME
			self.dstPos = self.curPos + self.STEP_HEIGHT

		if self.dstPos > self.curPos:
			self.curPos += 1
			self.textBar.SetPosition(3, 10 - self.curPos)

			if self.curPos > len(self.tipList)*self.STEP_HEIGHT:
				self.curPos = -self.STEP_HEIGHT
				self.dstPos = -self.STEP_HEIGHT

				self.__CleanOldTip()
			
class BigTextBar(TextBar):
	def __init__(self, width, height, fontSize):
		ui.Window.__init__(self)
		self.handle = grp.CreateBigTextBar(width, height, fontSize)

	def __del__(self):
		ui.Window.__del__(self)
		grp.DestroyTextBar(self.handle)

class BigBoard(ui.Bar):
	SCROLL_WAIT_TIME = 5.0
	TIP_DURATION = 10.0
	FONT_WIDTH	= 18
	FONT_HEIGHT	= 18
	LINE_WIDTH  = 500
	LINE_HEIGHT	= FONT_HEIGHT + 5
	STEP_HEIGHT = LINE_HEIGHT * 2
	LINE_CHANGE_LIMIT_WIDTH = 350

	# FRAME_IMAGE_FILE_NAME_LIST = [
		# "season1/interface/oxevent/frame_0.sub",
		# "season1/interface/oxevent/frame_1.sub",
		# "season1/interface/oxevent/frame_2.sub",
	# ]

	FRAME_IMAGE_STEP = 256

	FRAME_BASE_X = -20
	FRAME_BASE_Y = -12

	def __init__(self):
		ui.Bar.__init__(self)

		self.AddFlag("not_pick")
		self.tipList = []
		self.curPos = 0
		self.dstPos = 0
		self.nextScrollTime = 0

		self.SetPosition(0, 150)
		self.SetSize(512, 55)
		self.SetColor(grp.GenerateColor(0.0, 0.0, 0.0, 0.5))
		self.SetWindowHorizontalAlignCenter()

		self.__CreateTextBar()
		self.__LoadFrameImages()

	def __LoadFrameImages(self):
		x = self.FRAME_BASE_X
		y = self.FRAME_BASE_Y
		self.imgList = []
		# for imgFileName in self.FRAME_IMAGE_FILE_NAME_LIST:
			# self.imgList.append(self.__LoadImage(x, y, imgFileName))
			# x += self.FRAME_IMAGE_STEP

	def __LoadImage(self, x, y, fileName):
		img = ui.ImageBox()
		img.SetParent(self)
		img.AddFlag("not_pick")
		img.LoadImage(fileName)
		img.SetPosition(x, y)
		img.Show()
		return img

	def __del__(self):
		ui.Bar.__del__(self)

	def __CreateTextBar(self):
		x, y = self.GetGlobalPosition()

		self.textBar = BigTextBar(self.LINE_WIDTH, 300, self.FONT_HEIGHT)
		self.textBar.SetParent(self)
		self.textBar.SetPosition(6, 8)
		self.textBar.SetTextColor(242, 231, 193)
		self.textBar.SetClipRect(0, y+8, wndMgr.GetScreenWidth(), y+8+self.STEP_HEIGHT)
		self.textBar.Show()

	def __CleanOldTip(self):
		curTime = app.GetTime()
		leaveList = []
		for madeTime, text in self.tipList:
			if curTime + self.TIP_DURATION <= madeTime:
				leaveList.append(text)

		self.tipList = leaveList

		if not leaveList:
			self.textBar.ClearBar()
			self.Hide()
			return

		self.__RefreshBoard()

	def __RefreshBoard(self):
		self.textBar.ClearBar()

		if len(self.tipList) == 1:
			checkTime, text = self.tipList[0]
			(text_width, text_height) = self.textBar.GetTextExtent(text)
			self.textBar.TextOut((500-text_width)/2, (self.STEP_HEIGHT-8-text_height)/2, text)
		else:
			index = 0
			for checkTime, text in self.tipList:
				(text_width, text_height) = self.textBar.GetTextExtent(text)
				self.textBar.TextOut((500-text_width)/2, index*self.LINE_HEIGHT, text)
				index += 1

	def SetTip(self, text):
		if not app.IsVisibleNotice():
			return

		curTime = app.GetTime()
		self.__AppendText(curTime, text)
		self.__RefreshBoard()

		self.nextScrollTime = curTime + 1.0

		if not self.IsShow():
			self.curPos = -self.STEP_HEIGHT
			self.dstPos = -self.STEP_HEIGHT
			self.textBar.SetPosition(3, 8 - self.curPos)
			self.Show()

	def __AppendText(self, curTime, text):
		import dbg
		prevPos = 0
		while 1:
			curPos = text.find(" ", prevPos)
			if curPos < 0:
				break

			(text_width, text_height) = self.textBar.GetTextExtent(text[:curPos])
			if text_width > self.LINE_CHANGE_LIMIT_WIDTH:
				self.tipList.append((curTime, text[:prevPos]))
				self.tipList.append((curTime, text[prevPos:]))
				return

			prevPos = curPos + 1

		self.tipList.append((curTime, text))

	def OnUpdate(self):
		if not self.tipList:
			self.Hide()
			return

		if app.GetTime() > self.nextScrollTime:
			self.nextScrollTime = app.GetTime() + self.SCROLL_WAIT_TIME

			self.dstPos = self.curPos + self.STEP_HEIGHT

		if self.dstPos > self.curPos:
			self.curPos += 1
			self.textBar.SetPosition(3, 8 - self.curPos)

			if self.curPos > len(self.tipList)*self.LINE_HEIGHT:
				self.curPos = -self.STEP_HEIGHT
				self.dstPos = -self.STEP_HEIGHT

				self.__CleanOldTip()
				
class LeftTipBoard(ui.ScriptWindow):
	PAGE_BASE_POS = (-169, 240)
	PAGE_SIZE = (273, 90)
	
	def __init__(self):
		def IntializeWindow():
			self.AddFlag("not_pick")
			self.SetSize(*self.PAGE_SIZE)
			self.SetWindowVerticalAlignBottom()
			self.SetPosition(*self.PAGE_BASE_POS)
			self.Hide()
		
		ui.ScriptWindow.__init__(self, "UI_BOTTOM")
		IntializeWindow()
		
		self.__Initialize()
		self.__InitializeObjects()
	
	def __Initialize(self):
		self.textLine = None
		self.interface = None
		self.getName = None
		self.window_bg = None
		self.raceBg = None
		self.childName = None
		self.childText = None
		
		self.wndWidth = self.GetWidth()
		
		self.isActiveSlide = False
		self.isActiveSlideOut = False
		self.endTime = 0
		
		self.actual_text = ""
		self.tipCache = []
	
	def __InitializeObjects(self):
		self.window_bg = ui.ImageBox()
		self.window_bg.SetParent(self)
		self.window_bg.LoadImage("d:/ymir work/ui/game/ranking/main.png")
		self.window_bg.OnMouseLeftButtonDown = ui.__mem_func__(self.SendChatTest)
		self.window_bg.Show()
		
		self.raceBg = ui.ImageBox()
		self.raceBg.SetParent(self.window_bg)
		self.raceBg.SetPosition(4, 26)
		self.raceBg.LoadImage("d:/ymir work/ui/game/ranking/shaman_w.tga")
		self.raceBg.Show()
		
		self.childName = ui.TextLine()
		self.childName.SetParent(self.window_bg)
		self.childName.SetPosition(77, 47)
		self.childName.SetText(localeInfo.NEW_NOTIF)
		self.childName.SetPackedFontColor(0xffffdd9b)
		self.childName.Show()

		self.childText = ui.TextLine()
		self.childText.SetParent(self.window_bg)
		self.childText.SetPosition(77, 46 + 13)
		self.childText.SetText(localeInfo.NEW_PLAYER_ONLINE % self.getName)
		self.childText.SetPackedFontColor(0xff9bd1ff)
		self.childText.Show()
		
		x, y = self.GetGlobalPosition()
		self.textLine = TextBar(370, 300)
		self.textLine.SetParent(self.window_bg)
		self.textLine.SetTextColor(*constInfo.TOOLTIP_KEYS_COLOR_RGB)
		self.textLine.SetWindowVerticalAlignCenter()
		self.textLine.SetPosition(10, -2)
		self.textLine.SetClipRect(0, y, 165, y+35)
		self.textLine.Hide()
	
	def __del__(self):
		ui.ScriptWindow.__del__(self)
	
	def Destroy(self):
		self.Close()

	def BindInterface(self, interface):
		self.interface = proxy(interface)
		
	def SetTip(self, *args):

		(base_text, type) = args
		if type == "FRIEND" and base_text == player.GetMainCharacterName():
			return

		self.tipCache.append((base_text, type))
		
		self.textLine.ClearBar()
		
		if self.LoadTip(*args) is False:
			return
		
		self.tipCache = []
		self.Show()
		
		self.isActiveSlide = True
		self.endTime = app.GetGlobalTimeStamp() + 8

	def LoadTip(self, base_text, type):
		m_type = {
			"FRIEND" : "Jucatorul {} este online.",
			"SHOP" : "{}",
			"STUFF" : "{}",
			"BIOLOG": "Biolog: Poti livra un nou obiect!"
		}
		
		if not m_type.has_key(type):	return False
		if type == "FRIEND" and base_text == player.GetMainCharacterName():
			return False
			
		self.actual_text = m_type[type].format(str(base_text))
		self.textLine.TextOut(0, -2, self.actual_text)
		self.getName = str(base_text)
		
		if ("[DEV]" in self.getName):
			self.childText.SetText(localeInfo.NEW_DEV_ONLINE % self.getName)
			self.raceBg.LoadImage("d:/ymir work/ui/game/ranking/shaman_w.tga")
			self.window_bg.OnMouseLeftButtonDown = ui.__mem_func__(self.SendChatTest)
		elif ("[DS]" in self.getName):
			self.childText.SetText(localeInfo.NEW_SA_ONLINE % self.getName)
			self.raceBg.LoadImage("d:/ymir work/ui/game/ranking/shaman_w.tga")
			self.window_bg.OnMouseLeftButtonDown = ui.__mem_func__(self.SendChatTest)
		elif ("[GM]" in self.getName):
			self.childText.SetText(localeInfo.NEW_GM_ONLINE % self.getName)
			self.raceBg.LoadImage("d:/ymir work/ui/game/ranking/shaman_w.tga")
			self.window_bg.OnMouseLeftButtonDown = ui.__mem_func__(self.SendChatTest)
		elif ("[H]" in self.getName):
			self.childText.SetText(localeInfo.NEW_H_ONLINE % self.getName)
			self.raceBg.LoadImage("d:/ymir work/ui/game/ranking/shaman_w.tga")
			self.window_bg.OnMouseLeftButtonDown = ui.__mem_func__(self.SendChatTest)
		elif ("[BIOLOG]" in self.getName):
			self.childText.SetText(localeInfo.DELIVER_NEW_BIO)
			self.raceBg.LoadImage("d:/ymir work/ui/game/ranking/biolog.tga")
			self.window_bg.OnMouseLeftButtonDown = ui.__mem_func__(self.OpenBiologWindow)
		else:
			self.childText.SetText(localeInfo.NEW_PLAYER_ONLINE % self.getName)
			self.raceBg.LoadImage("d:/ymir work/ui/game/ranking/shaman_w.tga")
			self.window_bg.OnMouseLeftButtonDown = ui.__mem_func__(self.SendChatTest)

		self.SetPosition(*self.PAGE_BASE_POS)
		return True
	
	def Close(self):
		self.Hide()
	
	def SendChatTest(self):
		self.interface.OpenWhisperDialog(self.getName)
	
	def OpenBiologWindow(self):
		self.interface.ShowBiolog()

	def OnUpdate(self):
		if self.endTime - app.GetGlobalTimeStamp() <= 0 and self.isActiveSlideOut == False and self.isActiveSlide == True:
			self.isActiveSlide = False
			self.isActiveSlideOut = True
			self.textLine.Hide()
		
		if self.isActiveSlide and self.isActiveSlide == True:
			x, y = self.GetLocalPosition()
			if x < 0:	self.SetPosition(min(0, x + 4), y)
			else:
				(text_width, text_height) = self.textLine.GetTextExtent(self.actual_text)
				
				if not self.textLine.IsShow():
					self.textLine.SetPosition(-text_width, -2)
					self.textLine.Show()
				
				x, y = self.textLine.GetLocalPosition()
				if x <= -text_width:
					self.textLine.SetPosition(self.wndWidth, y)
				else:
					self.textLine.SetPosition(x - 1, y)
		
		elif self.isActiveSlideOut and self.isActiveSlideOut == True:
			x, y = self.GetLocalPosition()
			if x > -(self.wndWidth):
				self.SetPosition(x - 4, y)
			elif x <= -(self.wndWidth):
				self.isActiveSlideOut = False
				if len(self.tipCache) != 0:
					self.LoadNextTip()
				else:
					self.Close()
	
	def LoadNextTip(self):
		self.textLine.ClearBar()
		self.LoadTip(*self.tipCache[0])
		del self.tipCache[0]
		self.isActiveSlide = True
		self.endTime = app.GetGlobalTimeStamp() + 4
		
class MissionBoard(ui.Bar):
	FONT_HEIGHT = 15
	LINE_HEIGHT = FONT_HEIGHT + 5
	STEP_HEIGHT = LINE_HEIGHT + 5
	LONG_TEXT_START_X = 300
	SCREEN_WIDTH = wndMgr.GetScreenWidth()

	def __init__(self):
		ui.Bar.__init__(self)

		self.AddFlag("not_pick")
		self.missionText = None
		self.missionFullText = None
		self.curPos = 0
		self.dstPos = -5
		self.nextScrollTime = 0
		self.flowMode = False
		self.ScrollStartTime = 0.0

		self.SetPosition(0, 100)
		self.SetSize(self.SCREEN_WIDTH, 35)
		self.SetColor(grp.GenerateColor(0.0, 0.0, 0.0, 0.5))
		self.SetWindowHorizontalAlignCenter()

		self.__CreateTextBar()

	def __del__(self):
		ui.Bar.__del__(self)

	def __CreateTextBar(self):
		x, y = self.GetGlobalPosition()

		self.textBar = BigTextBar(self.SCREEN_WIDTH*2, 300, self.FONT_HEIGHT)
		self.textBar.SetParent(self)
		self.textBar.SetPosition(6, 8)
		self.textBar.SetTextColor(242, 231, 193)
		self.textBar.SetClipRect(0, y, self.SCREEN_WIDTH, y+8+self.STEP_HEIGHT)
		self.textBar.Show()

	def CleanMission(self):
		self.missionText = None
		self.missionFullText = None
		self.textBar.ClearBar()
		self.Hide()

	def __RefreshBoard(self):
		self.textBar.ClearBar()

		if self.missionFullText:
			(text_width, text_height) = self.textBar.GetTextExtent(self.missionFullText)

			if text_width>self.SCREEN_WIDTH:
				self.textBar.TextOut(0, (self.STEP_HEIGHT-8-text_height)/2, self.missionFullText)
				self.flowMode = True
			else:
				self.textBar.TextOut((wndMgr.GetScreenWidth()-text_width)/2, (self.STEP_HEIGHT-8-text_height)/2, self.missionFullText)
				self.flowMode = False

	def SetMission(self, text):
		self.__AppendText(text)
		self.__RefreshBoard()

		if self.flowMode:
			self.dstPos = -text_width
			self.curPos = self.LONG_TEXT_START_X
			self.textBar.SetPosition(3 + self.curPos, 8)
		else:
			self.dstPos = 0
			self.curPos = self.STEP_HEIGHT
			self.textBar.SetPosition(3, 8 + self.curPos)

		if not self.IsShow():
			self.Show()

	def SetSubMission(self, text):
		self.missionFullText = self.missionText + text
		preflowMode = self.flowMode

		self.__RefreshBoard()

		if preflowMode != self.flowMode:
			if self.flowMode:
				self.dstPos = -text_width
				self.curPos = self.LONG_TEXT_START_X
				self.textBar.SetPosition(3 + self.curPos, 8)
			else:
				self.dstPos = 0
				self.curPos = self.STEP_HEIGHT
				self.textBar.SetPosition(3, 8 + self.curPos)

	def __AppendText(self, text):
		if text == "":
			self.CleanMission()
			return

		self.missionText = text
		self.missionFullText = text

	def OnUpdate(self):
		if self.missionFullText == None:
			self.Hide()
			return

		if self.dstPos < self.curPos:
			self.curPos -= 1
			if self.flowMode:
				self.textBar.SetPosition(3 + self.curPos, 8)
			else:
				self.textBar.SetPosition(3, 8 + self.curPos)
		else:
			if self.flowMode:
				self.curPos = self.SCREEN_WIDTH
				