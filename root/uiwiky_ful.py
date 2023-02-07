# @ Development by Grimmjock

import thenewui as ui
import CacheEffect as player
import mouseModule
import net
import app
import item
import chat
import grp
import uiScriptLocale
import uiCommon
import localeInfo
import event
import wndMgr
import uiToolTip
import renderTarget
import Collision as chr
import nonplayer
import math
import wikipedia

from _weakref import proxy
from operator import truediv

RENDER_TARGET_INDEX = 10
RENDER_TARGET_PREVIEW = 9
GetItems = item.GetNames()
GetMobs = nonplayer.GetMobs()

PATH = "d:/ymir work/ui/wiki/"
ARROW_EMOJI = "|Ed:/ymir work/ui/wiki/arrow_2.tga|e"

# Limits
MAX_LINE_COSTUMATION_ITER = 26 # (10 * 4 = 40)

# ANIMATIONS_CONFIG
SHOW_ANIMATION_CATEGORY = FALSE
SHOW_ANIMATION_SCALE = TRUE

SELECT_COLOR = grp.GenerateColor(0.153,0.231,0.275, 0.7)
HALF_WHITE_COLOR = grp.GenerateColor(1.0, 1.0, 1.0, 0.2)
BACKGROUND_COLOR = grp.GenerateColor(0.0, 0.0, 0.0, 1.0)

def HAS_FLAG(value, flag):
	return (value & flag) == flag

RACE_FLAG_TO_NAME = {
	1 << 0  : localeInfo.TARGET_INFO_RACE_ANIMAL,
	1 << 1 	: localeInfo.TARGET_INFO_RACE_UNDEAD,
	1 << 2  : localeInfo.TARGET_INFO_RACE_DEVIL,
	1 << 3  : localeInfo.TARGET_INFO_RACE_HUMAN,
	1 << 4  : localeInfo.TARGET_INFO_RACE_ORC,
	1 << 5  : localeInfo.TARGET_INFO_RACE_MILGYO,
}

SUB_RACE_FLAG_TO_NAME = {
	1 << 11 : localeInfo.TARGET_INFO_RACE_ELEC,
	1 << 12 : localeInfo.TARGET_INFO_RACE_FIRE,
	1 << 13 : localeInfo.TARGET_INFO_RACE_ICE,
	1 << 14 : localeInfo.TARGET_INFO_RACE_WIND,
	1 << 15 : localeInfo.TARGET_INFO_RACE_EARTH,
	1 << 16 : localeInfo.TARGET_INFO_RACE_DARK,
	1 << 17 : localeInfo.TARGET_INFO_RACE_SEFI,
	1 << 18 : localeInfo.TARGET_INFO_RACE_METINE,
}

ANTI_FLAG_DICT = {
	0 : item.ITEM_ANTIFLAG_WARRIOR,
	1 : item.ITEM_ANTIFLAG_ASSASSIN,
	2 : item.ITEM_ANTIFLAG_SURA,
	3 : item.ITEM_ANTIFLAG_SHAMAN,
	4 : item.ITEM_ANTIFLAG_WOLFMAN,
}

class WikiScrollBar(ui.Window):
	BASE_COLOR = grp.GenerateColor(0.0, 0.0, 0.0, 1.0)
	CORNERS_AND_LINES_COLOR = grp.GenerateColor(0.3411, 0.3411, 0.3411, 1.0)
	
	BAR_NUMB = 9 #This is static value! Please dont touch in him.
	
	class MiddleBar(ui.DragButton):
		MIDDLE_BAR_COLOR = grp.GenerateColor(0.6470, 0.6470, 0.6470, 1.0)
		
		def __init__(self, horizontal_scroll):
			ui.DragButton.__init__(self)
			self.AddFlag("movable")
			
			self.horizontal_scroll = horizontal_scroll
			
			self.middle = ui.Bar()
			self.middle.SetParent(self)
			self.middle.AddFlag("attach")
			self.middle.AddFlag("not_pick")
			self.middle.SetColor(self.MIDDLE_BAR_COLOR)
			self.middle.SetSize(1, 1)
			self.middle.Show()
		
		def SetStaticScale(self, size):
			(base_width, base_height) = (self.middle.GetWidth(), self.middle.GetHeight())
			
			if not self.horizontal_scroll:
				ui.DragButton.SetSize(self, base_width, size)
				self.middle.SetSize(base_width, size)
			else:
				ui.DragButton.SetSize(self, size, base_height)
				self.middle.SetSize(size, base_height)
		
		def SetSize(self, selfSize, fullSize):
			(base_width, base_height) = (self.middle.GetWidth(), self.middle.GetHeight())
			
			if not self.horizontal_scroll:
				ui.DragButton.SetSize(self, base_width, truediv(int(selfSize), int(fullSize)) * selfSize)
				self.middle.SetSize(base_width, truediv(int(selfSize), int(fullSize)) * selfSize)
			else:
				ui.DragButton.SetSize(self, truediv(int(selfSize), int(fullSize)) * selfSize, base_height)
				self.middle.SetSize(truediv(int(selfSize), int(fullSize)) * selfSize, base_height)
		
		def SetStaticSize(self, size):
			size = max(2, size)
			
			if not self.horizontal_scroll:
				ui.DragButton.SetSize(self, size, self.middle.GetHeight())
				self.middle.SetSize(size, self.middle.GetHeight())
			else:
				ui.DragButton.SetSize(self, self.middle.GetWidth(), size)
				self.middle.SetSize(self.middle.GetWidth(), size)
	
	def __init__(self, horizontal_scroll = False):
		ui.Window.__init__(self)
		
		self.horizontal_scroll = horizontal_scroll
		
		self.scrollEvent = None
		self.scrollSpeed = 1
		self.sizeScale = 1.0
		
		self.bars = []
		for i in xrange(self.BAR_NUMB):
			br = ui.Bar()
			br.SetParent(self)
			br.AddFlag("attach")
			br.AddFlag("not_pick")
			br.SetColor([self.CORNERS_AND_LINES_COLOR, self.BASE_COLOR][i == (self.BAR_NUMB-1)])
			if not (i % 2 == 0): br.SetSize(1, 1)
			br.Show()
			
			self.bars.append(br)
		
		self.middleBar = self.MiddleBar(self.horizontal_scroll)
		self.middleBar.SetParent(self)
		self.middleBar.SetMoveEvent(ui.__mem_func__(self.OnScrollMove))
		self.middleBar.Show()
	
	def SetParentGlobal(self, parent):
		pass
		# self.SetParent(parent)
		# self.SetInsideRender(True)
	
	def OnScrollMove(self):
		if not self.scrollEvent:
			return
		
		arg = float(self.middleBar.GetLocalPosition()[1] - 1) / float(self.GetHeight() - 2 - self.middleBar.GetHeight()) if not self.horizontal_scroll else\
				float(self.middleBar.GetLocalPosition()[0] - 1) / float(self.GetWidth() - 2 - self.middleBar.GetWidth())
		
		self.scrollEvent(arg)
	
	def SetScrollEvent(self, func):
		self.scrollEvent = ui.__mem_func__(func)
	
	def SetScrollSpeed(self, speed):
		self.scrollSpeed = speed
	
	def OnMouseLeftButtonDown(self):
		(xMouseLocalPosition, yMouseLocalPosition) = self.GetMouseLocalPosition()
		
		if not self.horizontal_scroll:
			if xMouseLocalPosition == 0 or xMouseLocalPosition == self.GetWidth():
				return
			
			y_pos = (yMouseLocalPosition - self.middleBar.GetHeight() / 2)
			self.middleBar.SetPosition(1, y_pos)
		else:
			if yMouseLocalPosition == 0 or yMouseLocalPosition == self.GetHeight():
				return
			
			x_pos = (xMouseLocalPosition - self.middleBar.GetWidth() / 2)
			self.middleBar.SetPosition(x_pos, 1)
		
		self.OnScrollMove()
	
	def SetSize(self, w, h):
		(width, height) = (max(3, w), max(3, h))
		
		ui.Window.SetSize(self, width, height)
		
		self.bars[0].SetSize(1, (height - 2))
		self.bars[0].SetPosition(0, 1)
		self.bars[2].SetSize((width - 2), 1)
		self.bars[2].SetPosition(1, 0)
		self.bars[4].SetSize(1, (height - 2))
		self.bars[4].SetPosition((width - 1), 1)
		self.bars[6].SetSize((width - 2), 1)
		self.bars[6].SetPosition(1, (height - 1))
		self.bars[8].SetSize((width - 2), (height - 2))
		self.bars[8].SetPosition(1, 1)
		
		self.bars[1].SetPosition(0, 0)
		self.bars[3].SetPosition((width - 1), 0)
		self.bars[5].SetPosition((width - 1), (height - 1))
		self.bars[7].SetPosition(0, (height - 1))
		
		if not self.horizontal_scroll:
			self.middleBar.SetStaticSize(width - 2)
			self.middleBar.SetSize(12, self.GetHeight())
		else:
			self.middleBar.SetStaticSize(height - 2)
			self.middleBar.SetSize(12, self.GetWidth())
		
		self.middleBar.SetRestrictMovementArea(1, 1, width - 2, height - 2)
	
	def SetScale(self, selfSize, fullSize):
		self.sizeScale = float(selfSize/fullSize)
		self.middleBar.SetSize(selfSize, fullSize)
	
	def SetStaticScale(self, r_size):
		self.middleBar.SetStaticScale(r_size)
	
	def SetPosScale(self, fScale):
		pos = (math.ceil((self.GetHeight() - 2 - self.middleBar.GetHeight()) * fScale) + 1) if not self.horizontal_scroll else\
				(math.ceil((self.GetWidth() - 2 - self.middleBar.GetWidth()) * fScale) + 1)
		
		self.SetPos(pos)
	
	def SetPos(self, pos):
		wPos = (1, pos) if not self.horizontal_scroll else (pos, 1)
		self.middleBar.SetPosition(*wPos)

class ListBoxItemDrop(ui.Window):
	ELEM_X_PADDING = 0
	ELEM_PADDING = 0
	SCROLL_SPEED = 25
	ELEM_PER_LINE = 11
	
	def __init__(self, parent, width, height, sendParent = True):
		ui.Window.__init__(self)
		
		self.SetSize(width, height)

		self.parent = proxy(parent)
		self.parent2 = proxy(parent)
		self.sendParent = sendParent
		
		self.elements = []
		self.posMap = {}
		self.scrollBar = None

		self.MainWindow = ui.Window()
		self.MainWindow.SetParent(self)
		self.MainWindow.AddFlag("attach")
		self.MainWindow.AddFlag("not_pick")
		self.MainWindow.SetSize(width-6, self.GetHeight())
		self.MainWindow.SetPosition(0, 0)
		self.MainWindow.Show()

		self.scrollBoard = ui.Window()
		self.scrollBoard.SetParent(self.MainWindow)
		self.scrollBoard.AddFlag("attach")
		self.scrollBoard.AddFlag("not_pick")
		self.scrollBoard.Show()
	
	def OnRender(self):
		xList, yList = self.parent2.GetGlobalPosition()
		widthList, heightList = self.parent2.GetWidth(), self.parent2.GetHeight()
	
		for item in self.elements:
			if item[1]:
				xText, yText = item[1].GetGlobalPosition()
				if yText < yList or yText + item[1].GetTextSize()[1] > yList + heightList:
					item[1].Hide()
				else:
					item[1].Show()

	def AddItem(self, Vnum, Count):
		if not self.scrollBar:
			self.RegisterScrollBar()

		item.SelectItem(Vnum)
		
		tmp = ui.ExpandedImageBox()
		tmp.SetParent(self.scrollBoard)
		tmp.LoadImage(item.GetIconImageFileName())

		tmp.itemSize = item.GetItemSize()[1]
		tmp.vnum = Vnum
		
		tmpDropText = ui.TextLine()
		tmpDropText.SetParent(tmp, self.MainWindow.hWnd)
		tmpDropText.AddFlag("attach")
		tmpDropText.AddFlag("not_pick")
		tmpDropText.SetText(str(Count))
		tmpDropText.SetPosition(tmp.GetWidth() - tmpDropText.GetTextSize()[0],\
									tmp.GetHeight() - tmpDropText.GetTextSize()[1])
		
		totalElem = len(self.elements)
		if totalElem > 0:
			currAdd = 0
			
			while True:
				if currAdd in self.posMap:
					currAdd += 1
					continue
				
				break
			
			totalLine = (currAdd % self.ELEM_PER_LINE)
			currH = (math.floor(currAdd / self.ELEM_PER_LINE) * (32 + self.ELEM_PADDING))
			
			for i in xrange(tmp.itemSize):
				self.posMap[currAdd + i * self.ELEM_PER_LINE] = True
			
			tmp.SetPosition(1 + totalLine * (36 + self.ELEM_X_PADDING), 0 + currH)
		else:
			for i in xrange(tmp.itemSize):
				self.posMap[i * self.ELEM_PER_LINE] = True
			
			tmp.SetPosition(1, 0)
		
		tmp.Show()
		tmpDropText.Show()
		
		self.elements.append((tmp, tmpDropText))
		
		self.scrollBoard.SetSize(self.MainWindow.GetWidth(), max(self.scrollBoard.GetHeight(), tmp.GetLocalPosition()[1] + tmp.GetHeight()))
		self.UpdateScrollbar()
		
		return tmp

	# def OnRunMouseWheel(self, length):
		# if self.MainWindow.IsInPosition() and self.scrollBar:
			# if self.scrollBar.IsShow():
				# self.UpdateScrollbar(int((length * 0.01) * self.SCROLL_SPEED))
			# return True
		
		# return False

	def OnScrollBar(self, fScale):
		curr = min(0, max(math.ceil((self.scrollBoard.GetHeight() - self.MainWindow.GetHeight()) * fScale * -1.0), -self.scrollBoard.GetHeight() + self.MainWindow.GetHeight()))
		self.scrollBoard.SetPosition(0, curr)

	def ChangeScrollbar(self):
		if not self.scrollBar:
			return
		
		if self.scrollBoard.GetHeight() <= self.GetHeight():
			self.scrollBar.Hide()
		else:
			self.scrollBar.SetScale(self.GetHeight(), self.scrollBoard.GetHeight())
			self.scrollBar.SetPosScale(truediv(abs(self.scrollBoard.GetLocalPosition()[1]), (self.scrollBoard.GetHeight() - self.MainWindow.GetHeight())))
			self.scrollBar.Show()
	
	def UpdateScrollbar(self, val = 0):
		curr = min(0, max(self.scrollBoard.GetLocalPosition()[1] + val, -self.scrollBoard.GetHeight() + self.MainWindow.GetHeight()))
		self.scrollBoard.SetPosition(0, curr)
		
		self.ChangeScrollbar()
	
	def RegisterScrollBar(self):
		self.scrollBar = WikiScrollBar()
		self.scrollBar.SetParent(self)
		self.scrollBar.SetPosition(self.MainWindow.GetLocalPosition()[0] + self.MainWindow.GetWidth(),\
									self.MainWindow.GetLocalPosition()[1])
		self.scrollBar.SetSize(7, self.MainWindow.GetHeight())
		self.scrollBar.SetScrollEvent(self.OnScrollBar)
		self.scrollBar.SetScrollSpeed(self.SCROLL_SPEED)
		self.scrollBar.Show()
		
		self.scrollBar.SetInsideRender(True)
		
		self.ChangeScrollbar()

class ListBoxItem(ui.Window):
	class NewItemText(ui.Window):
		ELEM_PADDING = 0
		SCROLL_SPEED = 50
		
		def __init__(self):
			ui.Window.__init__(self)
			
			self.SetSize(555, 355)

			self.elements = []
			self.images = []
			self.scrollBar = None
			
			self.peekWindow = ui.Window()
			self.peekWindow.SetParent(self)
			self.peekWindow.AddFlag("attach")
			self.peekWindow.AddFlag("not_pick")
			self.peekWindow.SetSize(self.GetWidth() - 8 - 5, self.GetHeight() - 5)
			self.peekWindow.SetPosition(5, 5)
			self.peekWindow.SetInsideRender(True)
			self.peekWindow.Show()
			
			self.scrollBoard = ui.Window()
			self.scrollBoard.SetParent(self.peekWindow)
			self.scrollBoard.AddFlag("attach")
			self.scrollBoard.AddFlag("not_pick")
			self.scrollBoard.Show()

		def __del__(self):
			ui.Window.__del__(self)
			self.ResetInit()

		def ResetInit(self):
			del self.elements[:]
			del self.images[:]
			
			self.banner = None

		def SetParent(self, parent):
			ui.Window.SetParent(self, parent)
			self.parent = proxy(parent)

		def RegisterScroll(self, parent):
			self.RegisterScrollBar(parent)
		
		def ParseToken(self, data):
			# import chat
			# chat.AppendChat(1, data)
			# data = data.replace(chr(10), "").replace(chr(13), "")
			# if not (len(data) and data[0] == "["):
				# return (False, {}, data)
			
			# chat.AppendChat(1, data)
			
			fnd = data.find("]")
			if fnd <= 0:
				return (False, {}, data)
			
			content = data[1:fnd]
			data = data[fnd+1:]
			
			content = content.split(";")
			container = {}
			
			for i in content:
				i = i.strip()
				splt = i.split("=")
				
				if len(splt) == 1:
					container[splt[0].lower().strip()] = True
				else:
					container[splt[0].lower().strip()] = splt[1].lower().strip()
			
			return (True, container, data)
		
		def GetColorFromString(self, strCol):
			retData = []
			dNum = 4
			hCol = long(strCol, 16)
			
			if hCol <= 0xFFFFFF:
				retData.append(1.0)
				dNum = 3
			
			for i in xrange(dNum):
				retData.append(float((hCol >> (8 * i)) & 0xFF) / 255.0)
			
			retData.reverse()
			return retData

		def SetBasePosition(self, x, y):
			self.xBase = x
			self.yBase = y

		def GetBasePosition(self):
			return (self.xBase, self.yBase)
		
		def SetBannerImage(self, image):
			self.banner = image
		
		def LoadFile(self, filename):
			del self.elements[:]
			del self.images[:]
			
			self.scrollBoard.SetSize(0, 0)
			self.UpdateScrollbar()
			
			open_filename = "{}/wiki/{}".format(app.GetLocalePath(), filename)
			loadF = open(open_filename, 'r')
			
			for i in loadF.readlines()[1:]:
				(ret, tokenMap, i) = self.ParseToken(i)
				
				if ret:
					if tokenMap.has_key("banner_img"):
						if self.banner:
							self.banner.LoadImage(tokenMap["banner_img"])

						tokenMap.pop("banner_img")
					
					if tokenMap.has_key("img"):
						cimg = ui.ExpandedImageBox()
						cimg.SetParent(self.scrollBoard)
						cimg.AddFlag("attach")
						cimg.AddFlag("not_pick")
						cimg.LoadImage(tokenMap["img"])
						cimg.Show()
						
						tokenMap.pop("img")
						
						x = 0
						if tokenMap.has_key("x"):
							x = int(tokenMap["x"])
							tokenMap.pop("x")
						
						y = 0
						if tokenMap.has_key("y"):
							y = int(tokenMap["y"])
							tokenMap.pop("y")
						
						if tokenMap.has_key("center_align"):
							cimg.SetPosition(self.peekWindow.GetWidth() / 2 - cimg.GetWidth() / 2, y)
							tokenMap.pop("center_align")
						elif tokenMap.has_key("right_align"):
							cimg.SetPosition(self.peekWindow.GetWidth() - cimg.GetWidth(), y)
							tokenMap.pop("right_align")
						else:
							cimg.SetPosition(x, y)
						
						self.images.append(cimg)
				
				if ret and not len(i):
					continue
				
				tmp = ui.Window()
				tmp.SetParent(self.scrollBoard)
				tmp.AddFlag("attach")
				tmp.AddFlag("not_pick")
				
				tmp.txt = ui.TextLine()
				tmp.txt.SetParent(tmp, self.parent.hWnd)
				if tokenMap.has_key("font_size"):
					splt = localeInfo.UI_DEF_FONT.split(":")
					tmp.txt.SetFontName(splt[0]+":"+tokenMap["font_size"])
					tokenMap.pop("font_size")
				else:
					tmp.txt.SetFontName(localeInfo.UI_DEF_FONT)
				tmp.txt.SetText(i)

				tmp.txt.Show()
				tmp.SetSize(*tmp.txt.GetTextSize())
				
				if len(i) > 0 and i[0] == "*":
					tmp.txt.SetText(i[1:])
					
					tmp.img = ui.ExpandedImageBox()
					tmp.img.SetParent(tmp)
					tmp.img.AddFlag("attach")
					tmp.img.AddFlag("not_pick")
					tmp.img.LoadImage("d:/ymir work/ui/wiki/arrow_2.tga")
					tmp.img.Show()
					
					tmp.SetSize(tmp.img.GetWidth() + 5 + tmp.txt.GetTextSize()[0], max(tmp.img.GetHeight(), tmp.txt.GetTextSize()[1]))
					tmp.img.SetPosition(0, abs(tmp.GetHeight() / 2 - tmp.img.GetHeight() / 2))
					
					tmp.txt.SetPosition(tmp.img.GetWidth() + 5, abs(tmp.GetHeight() / 2 - tmp.txt.GetTextSize()[1] / 2) - 1)
				
				if tokenMap.has_key("color"):
					fontColor = self.GetColorFromString(tokenMap["color"])
					tmp.txt.SetPackedFontColor(grp.GenerateColor(fontColor[0], fontColor[1], fontColor[2], fontColor[3]))
					
					tokenMap.pop("color")
				
				addPadding = 0
				totalElem = len(self.elements)
				
				if tokenMap.has_key("y_padding"):
					addPadding = int(tokenMap["y_padding"])
					tokenMap.pop("y_padding")
				
				if totalElem > 0:
					lastIndex = totalElem
					
					self.elements.insert(lastIndex, tmp)
					totalElem += 1
					
					for i in xrange(lastIndex, totalElem):
						self.elements[i].SetPosition(0,\
							(0 if i ==0 else self.elements[i - 1].GetLocalPosition()[1] + self.elements[i - 1].GetHeight() + addPadding))
				else:
					self.elements.append(tmp)
					tmp.SetPosition(0, addPadding)
				
				if tokenMap.has_key("center_align"):
					tmp.SetPosition(self.peekWindow.GetWidth() / 2 - tmp.GetWidth() / 2, tmp.GetLocalPosition()[1])
					tokenMap.pop("center_align")
				elif tokenMap.has_key("right_align"):
					tmp.SetPosition(self.peekWindow.GetWidth() - tmp.GetWidth(), tmp.GetLocalPosition()[1])
					tokenMap.pop("right_align")
				elif tokenMap.has_key("x_padding"):
					tmp.SetPosition(int(tokenMap["x_padding"]), tmp.GetLocalPosition()[1])
					tokenMap.pop("x_padding")
				
				tmp.Show()
				
				self.scrollBoard.SetSize(self.peekWindow.GetWidth(), self.scrollBoard.GetHeight() + addPadding + tmp.GetHeight())
			
			for i in self.images:
				mxSize = i.GetLocalPosition()[1] + i.GetHeight()
				if mxSize > self.scrollBoard.GetHeight():
					self.scrollBoard.SetSize(self.peekWindow.GetWidth(), mxSize)
			
			self.UpdateScrollbar()
			wndMgr.Show(self.hWnd)

		def OnScrollBar(self, fScale):
			curr = min(0, max(math.ceil((self.scrollBoard.GetHeight() - self.peekWindow.GetHeight()) * fScale * -1.0), -self.scrollBoard.GetHeight() + self.peekWindow.GetHeight()))
			self.scrollBoard.SetPosition(0, curr)
		
		def ChangeScrollbar(self):
			if not self.scrollBar:
				return
			
			if self.scrollBoard.GetHeight() <= self.GetHeight():
				self.scrollBar.Hide()
			else:
				self.scrollBar.SetScale(self.GetHeight(), self.scrollBoard.GetHeight())
				self.scrollBar.SetPosScale(truediv(abs(self.scrollBoard.GetLocalPosition()[1]), (self.scrollBoard.GetHeight() - self.peekWindow.GetHeight())))
				self.scrollBar.Show()
		
		def UpdateScrollbar(self, val = 0):
			curr = min(0, max(self.scrollBoard.GetLocalPosition()[1] + val, -self.scrollBoard.GetHeight() + self.peekWindow.GetHeight()))
			self.scrollBoard.SetPosition(0, curr)
			
			self.ChangeScrollbar()
		
		def RegisterScrollBar(self, parent):
			self.scrollBar = WikiScrollBar()
			self.scrollBar.SetParent(parent)
			self.scrollBar.SetPosition(693, 150 - 40)
			self.scrollBar.SetSize(7, 307 + 40)
			self.scrollBar.SetScrollEvent(self.OnScrollBar)
			self.scrollBar.SetScrollSpeed(self.SCROLL_SPEED)
			self.scrollBar.Show()
			
			self.ChangeScrollbar()

	class NewItemChest(ui.Window):
		def __init__(self, parent, ItemVnum):
			ui.Window.__init__(self)
			self.background = None
			self.ResetInit()

			self.SetInsideRender(True)

			self.background = ui.ExpandedImageBox()
			self.background.SetParent(self)
			self.background.LoadImage(PATH + "detail_chest.tga")
			self.background.Show()
			
			item.SelectItem(ItemVnum)
			iMonsterOrigin = wikipedia.GetChestOriginByVnum(ItemVnum)

			self.ChestIcon = ui.ExpandedImageBox()
			self.ChestIcon.SetParent(self)
			self.ChestIcon.LoadImage(item.GetIconImageFileName())
			self.ChestIcon.SetPosition(7, 32)
			self.ChestIcon.SetEvent(ui.__mem_func__(self.OnMouseInIcon), "MOUSE_OVER_IN", ItemVnum)
			self.ChestIcon.SetEvent(ui.__mem_func__(self.OnMouseOutIcon), "MOUSE_OVER_OUT")
			self.ChestIcon.Show()
		
			self.ChestName = ui.TextLine()
			self.ChestName.SetParent(self, parent.hWnd)
			self.ChestName.SetText(localeInfo.WIKI_TEXT_01 + item.GetItemName())
			self.ChestName.SetPosition(0, 4)
			self.ChestName.SetWindowHorizontalAlignCenter()
			self.ChestName.SetHorizontalAlignCenter()
			self.ChestName.Show()
			
			lines = uiToolTip.SplitDescription(nonplayer.GetMonsterName(iMonsterOrigin), 15)
			
			self.dictOriginText = []
			for index, line in enumerate(lines):
				ChestOrigin = ui.TextLine()
				ChestOrigin.SetParent(self, parent.hWnd)
				ChestOrigin.SetText(line)
				ChestOrigin.SetPosition(225, 40 + 13*index)
				ChestOrigin.SetWindowHorizontalAlignCenter()
				ChestOrigin.SetHorizontalAlignCenter()
				ChestOrigin.Show()
				
				self.dictOriginText.append(ChestOrigin)
			
			self.ChestOrigin = ui.TextLine()
			self.ChestOrigin.SetParent(self, parent.hWnd)
			self.ChestOrigin.SetText(localeInfo.WIKI_TEXT_02)
			self.ChestOrigin.SetPosition(225, 4)
			self.ChestOrigin.SetWindowHorizontalAlignCenter()
			self.ChestOrigin.SetHorizontalAlignCenter()
			self.ChestOrigin.Show()

			self.ChestOriginMonster = ui.TextLine()
			self.ChestOriginMonster.SetParent(self, parent.hWnd)
			self.ChestOriginMonster.SetText("")
			self.ChestOriginMonster.SetPosition(225, 50)
			self.ChestOriginMonster.SetWindowHorizontalAlignCenter()
			self.ChestOriginMonster.SetHorizontalAlignCenter()
			self.ChestOriginMonster.Show()

			self.dropList = ListBoxItemDrop(parent, 401, 66)
			self.dropList.AddFlag("attach")
			self.dropList.SetParent(self.background)
			self.dropList.SetPosition(49, 22)
			self.dropList.Show()

			for index, itemDrop in enumerate(wikipedia.GetChestDropByVnum(ItemVnum)):
				ItemVnum = itemDrop["item"][0]
				ItemCount = itemDrop["item"][1]
				
				if ItemVnum == 0:
					continue

				ret = self.dropList.AddItem(ItemVnum, ItemCount)
				ret.SetEvent(ui.__mem_func__(self.OnMouseInIcon), "MOUSE_OVER_IN", ItemVnum)
				ret.SetEvent(ui.__mem_func__(self.OnMouseOutIcon), "MOUSE_OVER_OUT")

			self.SetSize(self.background.GetWidth(), self.background.GetHeight())

		def OnMouseInIcon(self, type, vnum):
			if self.overInEventFunc:
				self.overInEventFunc(vnum)

		def OnMouseOutIcon(self, type):
			if self.overOutEventFunc:
				self.overOutEventFunc()

		def __del__(self):
			ui.Window.__del__(self)
			self.ResetInit()

		def ResetInit(self):
			self.xBase = 0
			self.yBase = 0
			self.overInEventFunc = None
			self.overOutEventFunc = None
			self.clickEvent = None
			self.background = None
			self.ItemVnum = None
			self.currentIdx = 0

		def SetParent(self, parent):
			ui.Window.SetParent(self, parent)
			self.parent = proxy(parent)

		def SetBasePosition(self, x, y):
			self.xBase = x
			self.yBase = y
			
		def GetBasePosition(self):
			return (self.xBase, self.yBase)
			
		def SetOverInEvent(self, event):
			self.overInEventFunc = event
			
		def SetOverOutEvent(self, event):
			self.overOutEventFunc = event
			
		def SetClickEvent(self, event):
			self.clickEvent = event

	class NewItemPreviewMonster(ui.Window):
		def __init__(self, parent, MonsterVnum):
			ui.Window.__init__(self)
			self.background = None
			self.ResetInit()
			
			self.SetInsideRender(True)

			self.background = ui.ExpandedImageBox()
			self.background.SetParent(self)
			self.background.LoadImage(PATH + "detail_monster.tga")
			self.background.Show()

			self.ModelPreview = ui.RenderTarget()
			self.ModelPreview.SetParent(self)
			self.ModelPreview.SetSize(185, 159)
			self.ModelPreview.SetPosition(3, 4)
			self.ModelPreview.SetRenderTarget(RENDER_TARGET_PREVIEW)
			self.ModelPreview.Show()

			self.MonsterList = ui.TextLine()
			self.MonsterList.SetParent(self, parent.hWnd)
			self.MonsterList.SetText(localeInfo.WIKI_TEXT_03 + nonplayer.GetMonsterName(MonsterVnum))
			self.MonsterList.SetPosition(90, 4)
			self.MonsterList.SetWindowHorizontalAlignCenter()
			self.MonsterList.SetHorizontalAlignCenter()
			self.MonsterList.Show()

			renderTarget.SelectModel(RENDER_TARGET_PREVIEW, MonsterVnum)
			renderTarget.SetVisibility(RENDER_TARGET_PREVIEW, True)
			renderTarget.SetBackground(RENDER_TARGET_PREVIEW, "d:/ymir work/ui/game/myshop_deco/model_view_bg.sub")

			self.dropList = ListBoxItemDrop(parent, 345, 130)
			self.dropList.ELEM_PER_LINE = 9
			self.dropList.AddFlag("attach")
			self.dropList.SetParent(self.background)
			self.dropList.SetPosition(189, 22)
			self.dropList.Show()

			for itemDrop in wikipedia.GetMonsterDropByVnum(MonsterVnum):
				ItemVnum = itemDrop["item"][0]
				ItemCount = itemDrop["item"][1]
				
				if ItemVnum == 0:
					break

				item = self.dropList.AddItem(ItemVnum, ItemCount)
				item.SetEvent(ui.__mem_func__(self.OnMouseInIcon), "MOUSE_OVER_IN", ItemVnum)
				item.SetEvent(ui.__mem_func__(self.OnMouseOutIcon), "MOUSE_OVER_OUT")
			
			self.dictTextMonster = []
			MonsterStatistic = ui.TextLine()
			MonsterStatistic.SetParent(self, parent.hWnd)
			MonsterStatistic.SetText(localeInfo.WIKI_TEXT_04 + str(nonplayer.GetMonsterName(MonsterVnum)))
			MonsterStatistic.SetPosition(0, 169)
			MonsterStatistic.SetWindowHorizontalAlignCenter()
			MonsterStatistic.SetHorizontalAlignCenter()
			MonsterStatistic.Show()
			
			self.dictTextMonster.append(MonsterStatistic)

			mainrace = ""
			subrace = ""
			
			dwRaceFlag = nonplayer.GetMonsterRaceFlag(MonsterVnum)
			for i in xrange(19):
				curFlag = 1 << i
				if HAS_FLAG(dwRaceFlag, curFlag):
					if RACE_FLAG_TO_NAME.has_key(curFlag):
						mainrace += RACE_FLAG_TO_NAME[curFlag] + ", "
					elif SUB_RACE_FLAG_TO_NAME.has_key(curFlag):
						subrace += SUB_RACE_FLAG_TO_NAME[curFlag] + ", "

			if nonplayer.IsMonsterStone(MonsterVnum):
				mainrace += localeInfo.TARGET_INFO_RACE_METIN + ", "
			if mainrace == "":
				mainrace = localeInfo.TARGET_INFO_NO_RACE
			else:
				mainrace = mainrace[:-2]
			if subrace == "":
				subrace = localeInfo.TARGET_INFO_NO_RACE
			else:
				subrace = subrace[:-2]
			
			iDamMin, iDamMax = nonplayer.GetMonsterDamage(MonsterVnum)
			INFO_DICT = [
				localeInfo.TARGET_INFO_MAX_HP % str(nonplayer.GetMonsterMaxHP(MonsterVnum)),
				localeInfo.WIKI_TEXT_05 + str(nonplayer.GetMonsterLevel(MonsterVnum)),
				localeInfo.TARGET_INFO_MAINRACE % mainrace,
				localeInfo.TARGET_INFO_SUBRACE % subrace,
				localeInfo.WIKI_TEXT_06 + str(nonplayer.GetMonsterExp(MonsterVnum)),
				localeInfo.WIKI_TEXT_07 + str(iDamMin) + " | " + localeInfo.WIKI_TEXT_08 + str(iDamMax),
			]
			
			for x in xrange(len(INFO_DICT)):
				MonsterInfo = ui.TextLine()
				MonsterInfo.SetParent(self, parent.hWnd)
				MonsterInfo.SetFontName("Ariel:14")
				MonsterInfo.SetText(ARROW_EMOJI + " " + INFO_DICT[x])
				MonsterInfo.SetPosition(7, 190 + x*18)
				MonsterInfo.Show()				
			
				self.dictTextMonster.append(MonsterInfo)
			
			self.SetSize(self.background.GetWidth(), self.background.GetHeight())

		def OnMouseInIcon(self, type, vnum):
			if self.overInEventFunc:
				self.overInEventFunc(vnum)

		def OnMouseOutIcon(self, type):
			if self.overOutEventFunc:
				self.overOutEventFunc()

		def __del__(self):
			ui.Window.__del__(self)
			self.ResetInit()
			
			if self.ModelPreview:
				self.ModelPreview = None
				renderTarget.SetVisibility(RENDER_TARGET_PREVIEW, False)

		def ResetInit(self):
			self.xBase = 0
			self.yBase = 0
			self.overInEventFunc = None
			self.overOutEventFunc = None
			self.background = None
			self.ItemVnum = None
			self.currentIdx = 0
			
			self.ModelPreview = None

		def SetParent(self, parent):
			ui.Window.SetParent(self, parent)
			self.parent = proxy(parent)

		def SetBasePosition(self, x, y):
			self.xBase = x
			self.yBase = y
			
		def GetBasePosition(self):
			return (self.xBase, self.yBase)
			
		def SetOverInEvent(self, event):
			self.overInEventFunc = event
			
		def SetOverOutEvent(self, event):
			self.overOutEventFunc = event

	class NewItemMonster(ui.Window):
		def __init__(self, parent, MonsterVnum, indexRender):
			ui.Window.__init__(self)
			self.background = None
			self.ModelPreview = None
			self.dropList = None

			self.indexRender = indexRender
			self.SetInsideRender(True)
			
			self.ResetInit()
			self.MonsterVnum = MonsterVnum

			self.background = ui.ExpandedImageBox()
			self.background.SetParent(self)
			self.background.LoadImage(PATH + "detail_chest.tga")
			self.background.Show()

			self.MonsterList = ui.TextLine()
			self.MonsterList.SetParent(self, parent.hWnd)
			self.MonsterList.SetText(localeInfo.WIKI_TEXT_03 + nonplayer.GetMonsterName(MonsterVnum))
			self.MonsterList.SetPosition(0, 4)
			self.MonsterList.SetWindowHorizontalAlignCenter()
			self.MonsterList.SetHorizontalAlignCenter()
			self.MonsterList.Show()

			self.MonsterOrigin = ui.TextLine()
			self.MonsterOrigin.SetParent(self, parent.hWnd)
			self.MonsterOrigin.SetText(localeInfo.WIKI_TEXT_09)
			self.MonsterOrigin.SetPosition(225, 4)
			self.MonsterOrigin.SetWindowHorizontalAlignCenter()
			self.MonsterOrigin.SetHorizontalAlignCenter()
			self.MonsterOrigin.Show()

			mainrace = ""
			dwRaceFlag = nonplayer.GetMonsterRaceFlag(MonsterVnum)
			for i in xrange(19):
				curFlag = 1 << i
				if HAS_FLAG(dwRaceFlag, curFlag):
					if RACE_FLAG_TO_NAME.has_key(curFlag):
						mainrace += RACE_FLAG_TO_NAME[curFlag] + ", "
			if nonplayer.IsMonsterStone(MonsterVnum):
				mainrace += localeInfo.TARGET_INFO_RACE_METIN + ", "
			if mainrace == "":
				mainrace = localeInfo.TARGET_INFO_NO_RACE
			else:
				mainrace = mainrace[:-2]

			self.MonsterRace = ui.TextLine()
			self.MonsterRace.SetParent(self, parent.hWnd)
			self.MonsterRace.SetText(mainrace)
			self.MonsterRace.SetPosition(225, 50)
			self.MonsterRace.SetWindowHorizontalAlignCenter()
			self.MonsterRace.SetHorizontalAlignCenter()
			self.MonsterRace.Show()

			self.ModelPreview = ui.RenderTarget()
			self.ModelPreview.SetParent(self)
			self.ModelPreview.SetSize(47, 87)
			self.ModelPreview.SetPosition(1 + 47 / 2 - self.ModelPreview.GetWidth() / 2, 1 + 87 / 2 - self.ModelPreview.GetHeight() / 2)
			self.ModelPreview.SetRenderTarget(RENDER_TARGET_INDEX + self.indexRender)
			self.ModelPreview.OnMouseLeftButtonDown = ui.__mem_func__(self.OnPreview)
			self.ModelPreview.Show()

			self.dropList = ListBoxItemDrop(parent, 401, 66)
			self.dropList.AddFlag("attach")
			self.dropList.SetParent(self.background)
			self.dropList.SetPosition(49, 22)
			self.dropList.Show()
			
			self.MonsterDrop = wikipedia.GetMonsterDropByVnum(self.MonsterVnum)

			self.SetSize(self.background.GetWidth(), self.background.GetHeight())

		def CreateDropMonster(self, parent):
			if len(self.dropList.elements) > 0:
				return

			renderTarget.SelectModel(RENDER_TARGET_INDEX + self.indexRender, self.MonsterVnum)
			renderTarget.SetVisibility(RENDER_TARGET_INDEX + self.indexRender, True)
			renderTarget.SetBackground(RENDER_TARGET_INDEX + self.indexRender, "d:/ymir work/ui/game/myshop_deco/model_view_bg.sub")
			
			for index, itemDrop in enumerate(self.MonsterDrop):
				ItemVnum = itemDrop["item"][0]
				ItemCount = itemDrop["item"][1]
				
				if ItemVnum == 0:
					break

				item = self.dropList.AddItem(ItemVnum, ItemCount)
				item.SetEvent(ui.__mem_func__(self.OnMouseInIcon), "MOUSE_OVER_IN", ItemVnum)
				item.SetEvent(ui.__mem_func__(self.OnMouseOutIcon), "MOUSE_OVER_OUT")

			return True

		def OnPreview(self):
			if self.clickEventFnc:
				self.clickEventFnc(self.MonsterVnum)
		
		def OnMouseInIcon(self, type, vnum):
			if self.overInEventFunc:
				self.overInEventFunc(vnum)

		def OnMouseOutIcon(self, type):
			if self.overOutEventFunc:
				self.overOutEventFunc()

		def __del__(self):
			ui.Window.__del__(self)
			self.ResetInit()
			if self.ModelPreview:
				self.ModelPreview = None
				renderTarget.SetVisibility(RENDER_TARGET_INDEX + self.indexRender, False)

		def ResetInit(self):
			self.xBase = 0
			self.yBase = 0
			self.overInEventFunc = None
			self.overOutEventFunc = None
			self.clickEventFnc = None
			self.background = None
			self.ItemVnum = None
			self.currentIdx = 0

		def SetParent(self, parent):
			ui.Window.SetParent(self, parent)
			self.parent = proxy(parent)

		def SetBasePosition(self, x, y):
			self.xBase = x
			self.yBase = y
			
		def GetBasePosition(self):
			return (self.xBase, self.yBase)
			
		def SetOverInEvent(self, event):
			self.overInEventFunc = event
			
		def SetOverOutEvent(self, event):
			self.overOutEventFunc = event
			
		def SetClickEvent(self, event):
			self.clickEventFnc = event

	class NewItemRefine(ui.Window):
		def __init__(self, parent, ItemVnum, RefineSet):
			ui.Window.__init__(self)
			self.background = None
			self.ItemVnum = ItemVnum
			self.ResetInit()

			if ItemVnum == 0:
				return
				
			item.SelectItem(ItemVnum)
			name = item.GetItemName()
			name = name[:name.find("+")] if name.find("+") else name

			self.background = ui.ExpandedImageBox()
			self.background.SetParent(self, parent.hWnd)
			self.background.LoadImage(PATH + "detail_item.tga")
			self.background.Show()

			self.NameItem = ui.TextLine()
			self.NameItem.SetParent(self, parent.hWnd)
			self.NameItem.SetText(name)
			self.NameItem.SetPosition(5, 4)
			self.NameItem.Show()

			self.LevelItem = ui.TextLine()
			self.LevelItem.SetParent(self, parent.hWnd)
			self.LevelItem.SetPosition(78, 4)
			self.LevelItem.SetWindowHorizontalAlignRight()
			self.LevelItem.Show()
			
			self.ImageItemVnum = ui.ExpandedImageBox()
			self.ImageItemVnum.SetParent(self, parent.hWnd)
			self.ImageItemVnum.LoadImage(item.GetIconImageFileName())
			self.ImageItemVnum.SetWindowVerticalAlignCenter()
			self.ImageItemVnum.SetPosition(8, 15)
			self.ImageItemVnum.SetEvent(ui.__mem_func__(self.OnMouseInIcon), "MOUSE_OVER_IN", ItemVnum)
			self.ImageItemVnum.SetEvent(ui.__mem_func__(self.OnMouseOutIcon), "MOUSE_OVER_OUT")
			self.ImageItemVnum.Show()
			
			for i in xrange(item.LIMIT_MAX_NUM):
				(limitType, limitValue) = item.GetLimit(i)
				if item.LIMIT_LEVEL == limitType:
					self.LevelItem.SetText(localeInfo.TOOLTIP_ITEM_LIMIT_LEVEL % (limitValue))
					break
				
			self.dictUpgradeCost = []
			self.dictYangCost = []
			
			xUpgradeCosts = [145, 186, 225, 265, 305, 350, 390, 430, 475, 515]
			for x in xrange(12):
				dictUpgradeCost = ui.TextLine()
				dictUpgradeCost.SetParent(self, parent.hWnd)
				if x == 0:
					dictUpgradeCost.SetText(localeInfo.WIKI_TEXT_10)
					dictUpgradeCost.SetPosition(54, 24)
				elif x == 1:
					dictUpgradeCost.SetText(localeInfo.WIKI_TEXT_11)
					dictUpgradeCost.SetPosition(56, 139)
				else:
					dictUpgradeCost.SetText("+" + str(x - 2))
					dictUpgradeCost.SetPosition(xUpgradeCosts[x- 2], 24)

				dictUpgradeCost.Show()

				self.dictUpgradeCost.append(dictUpgradeCost)

			for x in xrange(9):
				dictYangCost = ui.TextLine()
				dictYangCost.SetParent(self, parent.hWnd)
				dictYangCost.SetText("0")
				dictYangCost.SetPosition(xUpgradeCosts[x + 1], 139)

				dictYangCost.Show()

				self.dictYangCost.append(dictYangCost)
				
			CurrentRefine = RefineSet
			CurrentVnum = ItemVnum
			
			self.dictUpgradeItems = []
			
			xUpgradeIcon = [132, 173, 215, 256, 298, 339, 380, 422, 464, 503]
			yUpgradeIcon = [48, 48+48, 48+48+44, 48+48+44+44, 48+48+44+44+44, 48+48+44+44+44+44]
			
			bHasThree = False
			for i in xrange(1, 10):
				for x in xrange(5):
					MaterialVnum = wikipedia.GetMaterialVnum(CurrentRefine, x)
					
					if MaterialVnum == 0:
						continue
					
					if x == 2 and bHasThree == False:
						self.background.LoadImage(PATH + "detail_item_2.tga")
						self.ImageItemVnum.SetPosition(8, 12)
						self.dictUpgradeCost[1].SetPosition(56, 180)
						for idxY, ItemYang in enumerate(self.dictYangCost):
							ItemYang.SetPosition(xUpgradeCosts[idxY + 1], 180)
						
						self.SetSize(self.background.GetWidth(), self.background.GetHeight())
					elif x == 3:
						self.background.LoadImage(PATH + "detail_item_4.tga")
						self.ImageItemVnum.SetPosition(8, 15)
						self.dictUpgradeCost[1].SetPosition(56, 230)
						for idxY, ItemYang in enumerate(self.dictYangCost):
							ItemYang.SetPosition(xUpgradeCosts[idxY + 1], 230)
						
						self.SetSize(self.background.GetWidth(), self.background.GetHeight())
						bHasThree = True		
					elif x == 4:
						self.background.LoadImage(PATH + "detail_item_5.tga")
						self.ImageItemVnum.SetPosition(8, 18)
						self.dictUpgradeCost[1].SetPosition(56, 280)
						for idxY, ItemYang in enumerate(self.dictYangCost):
							ItemYang.SetPosition(xUpgradeCosts[idxY + 1], 280)
						
						self.SetSize(self.background.GetWidth(), self.background.GetHeight())
						bHasThree = True

					item.SelectItem(MaterialVnum)
					IconUpgrade = ui.ExpandedImageBox()
					IconUpgrade.SetParent(self, parent.hWnd)
					IconUpgrade.LoadImage(item.GetIconImageFileName())
					IconUpgrade.SetPosition(xUpgradeIcon[i], yUpgradeIcon[x])
					IconUpgrade.SetEvent(ui.__mem_func__(self.OnMouseInIcon), "MOUSE_OVER_IN", MaterialVnum)
					IconUpgrade.SetEvent(ui.__mem_func__(self.OnMouseOutIcon), "MOUSE_OVER_OUT")
					IconUpgrade.Show()
					
					TextUpgrade = ui.TextLine()
					TextUpgrade.SetParent(IconUpgrade, parent.hWnd)
					TextUpgrade.SetWindowHorizontalAlignRight()
					TextUpgrade.SetWindowVerticalAlignBottom()
					xex = 5 if wikipedia.GetMaterialCount(CurrentRefine, x) > 99 else 0
					xex += 5 if wikipedia.GetMaterialCount(CurrentRefine, x) > 999 else 0
					TextUpgrade.SetText(str(wikipedia.GetMaterialCount(CurrentRefine, x)))
					TextUpgrade.SetPosition(7 + xex, 13)
					TextUpgrade.Show()
					
					self.dictUpgradeItems.append(IconUpgrade)
					self.dictUpgradeItems.append(TextUpgrade)
				
				YangCost = self.ConvertYangAsKKK(wikipedia.GetUpgradeCost(CurrentRefine))
				self.dictYangCost[i-1].SetText(YangCost)
				self.dictYangCost[i-1].SetPosition(self.dictYangCost[i-1].GetLeft() - len(YangCost), self.dictYangCost[i-1].GetTop())
				
				# Set Current-RefineSet
				VnumCurent = CurrentVnum
				CurrentVnum = wikipedia.GetNextRefineVnum(VnumCurent)
				CurrentRefine = wikipedia.GetRefineSetByVnum(CurrentVnum)
				
				if CurrentVnum == 0:
					continue

			self.SetSize(self.background.GetWidth(), self.background.GetHeight())
		
		def ConvertYangAsKKK(self, Gold):
			Yang = str(Gold)
			if Gold >= 1000 and Gold <= 999999:
				return Yang[0:-3] + "k"
			elif Gold >= 1000000 and Gold <= 999999999:
				return Yang[0:-6] + "kk"
			elif Gold >= 1000000000 and Gold <= 999999999999:
				return Yang[0:-9] + "kkk"
			elif Gold >= 1000000000000 and Gold <= 999999999999999:
				return Yang[0:-12] + "kkkk"

			return Yang
		
		def __del__(self):
			ui.Window.__del__(self)
			self.ResetInit()

		def ResetInit(self):
			self.xBase = 0
			self.yBase = 0
			self.overInEventFunc = None
			self.overOutEventFunc = None
			self.clickEvent = None
			self.background = []

		def SetParent(self, parent):
			ui.Window.SetParent(self, parent)
			self.parent = proxy(parent)

		def SetBasePosition(self, x, y):
			self.xBase = x
			self.yBase = y
			
		def GetBasePosition(self):
			return (self.xBase, self.yBase)
			
		def SetOverInEvent(self, event):
			self.overInEventFunc = event
			
		def SetOverOutEvent(self, event):
			self.overOutEventFunc = event
			
		def SetClickEvent(self, event):
			self.clickEvent = event

		def OnMouseInIcon(self, type, vnum):
			if self.overInEventFunc:
				self.overInEventFunc(vnum)

		def OnMouseOutIcon(self, type):
			if self.overOutEventFunc:
				self.overOutEventFunc()

	class NewItemCostume(ui.Window):
		def __init__(self, parent, ItemVnum, Type):
			ui.Window.__init__(self)
			self.background = None
			self.Type = Type
			self.ResetInit()
			
			self.ItemVnum = ItemVnum

			if len(ItemVnum) == 0:
				return

			self.background = []
			for index in xrange(len(ItemVnum)):
				background = ui.ExpandedImageBox()
				background.SetParent(self, parent.hWnd)
				background.LoadImage(PATH + "detail_item_small.tga")
				background.SetPosition(index* 138, 0)
				background.Show()
				
				if ItemVnum[index] == 0:
					continue
				
				item.SelectItem(ItemVnum[index])

				ItemSlot = ui.ExpandedImageBox()
				ItemSlot.SetParent(background, parent.hWnd)
				ItemSlot.LoadImage(item.GetIconImageFileName())
				ItemSlot.SetPosition(45, 0)
				ItemSlot.SetWindowVerticalAlignCenter()
				ItemSlot.SetWindowVerticalAlignCenter()			
				if index == 0:
					ItemSlot.OnMouseOverIn = ui.__mem_func__(self.OnMouseOverIn1)
				elif index == 1:
					ItemSlot.OnMouseOverIn = ui.__mem_func__(self.OnMouseOverIn2)
				elif index == 2:
					ItemSlot.OnMouseOverIn = ui.__mem_func__(self.OnMouseOverIn3)
				elif index == 3:
					ItemSlot.OnMouseOverIn = ui.__mem_func__(self.OnMouseOverIn4)
				ItemSlot.OnMouseOverOut = ui.__mem_func__(self.OnMouseOverOutF)
				ItemSlot.Show()

				NameItem = ui.TextLine()
				NameItem.SetParent(background, parent.hWnd)
				NameItem.SetVerticalAlignCenter()	
				NameItem.SetWindowVerticalAlignCenter()
				NameItem.SetWindowVerticalAlignCenter()	
				NameItem.SetHorizontalAlignCenter()
				NameItem.SetText(item.GetItemName())
				NameItem.SetPosition(65, 60)
				NameItem.Show()

				self.background.append(background)
				self.background.append(ItemSlot)
				self.background.append(NameItem)
				
			self.SetSize(len(ItemVnum) * 138, self.background[0].GetHeight() + 4)

		def __del__(self):
			ui.Window.__del__(self)
			self.ResetInit()

		def ResetInit(self):
			self.xBase = 0
			self.yBase = 0
			self.overInEventItem = None
			self.overOutEventItem = None
			self.clickEvent = None
			self.background = []
			self.ItemVnum = None

		def SetParent(self, parent):
			ui.Window.SetParent(self, parent)
			self.parent = proxy(parent)

		def SetBasePosition(self, x, y):
			self.xBase = x
			self.yBase = y
			
		def GetBasePosition(self):
			return (self.xBase, self.yBase)
			
		def SetOverInEvent(self, event):
			self.overInEventItem = event
			
		def SetOverOutEvent(self, event):
			self.overOutEventItem = event
			
		def SetClickEvent(self, event):
			self.clickEvent = event
		
		def CanEquip(self, RaceIdx, itemVnum):
			item.SelectItem(itemVnum)

			race = RaceIdx
			job = chr.RaceToJob(race)
			if not ANTI_FLAG_DICT.has_key(job):
				return False

			if item.IsAntiFlag(ANTI_FLAG_DICT[job]):
				return False

			if item.IsAntiFlag(item.ITEM_ANTIFLAG_MALE) == False and chr.RaceToSex(race) == 1:
				return True

			if item.IsAntiFlag(item.ITEM_ANTIFLAG_FEMALE) == False and chr.RaceToSex(race) == 0:
				return True
				
			return False

		def OverInItemFunc(self, index):	
			if self.overInEventItem == None or self.ItemVnum[index] == 0:
				return
		
			if self.Type == item.COSTUME_TYPE_MOUNT or self.Type == 3:
				item.SelectItem(self.ItemVnum[index])
				self.overInEventItem(item.GetValue(1), 0, -1)
				return
		
			if self.CanEquip(player.GetRace(), self.ItemVnum[index]):
				if self.Type == item.COSTUME_TYPE_HAIR:
					item.SelectItem(self.ItemVnum[index])
					self.overInEventItem(player.GetRace(), item.GetValue(3), self.Type)
				else:
					self.overInEventItem(player.GetRace(), self.ItemVnum[index], self.Type)
			else:
				for race in xrange(9):
					if self.CanEquip(race, self.ItemVnum[index]):
						if self.Type == item.COSTUME_TYPE_HAIR:
							item.SelectItem(self.ItemVnum[index])
							self.overInEventItem(race, item.GetValue(3), self.Type)
						else:
							self.overInEventItem(race, self.ItemVnum[index], self.Type)
						break

		def OnMouseOverIn1(self):
			self.OverInItemFunc(0)

		def OnMouseOverIn2(self):
			self.OverInItemFunc(1)
				
		def OnMouseOverIn3(self):
			self.OverInItemFunc(2)
				
		def OnMouseOverIn4(self):
			self.OverInItemFunc(3)
		
		def OnMouseOverOutF(self):			
			if self.overOutEventItem:
				self.overOutEventItem()

	def __init__(self):
		ui.Window.__init__(self)
		self.ResetInit()
		self.itemTooltip = uiToolTip.ItemToolTip()
		self.itemTooltip.SetSize(160, 211)
		self.itemTooltip.toolTipHeight = 211
		self.itemTooltip.HideToolTip()

		self.ModelPreviewBoard = ui.ThinBoardCircle()
		self.ModelPreviewBoard.SetParent(self.itemTooltip)
		self.ModelPreviewBoard.SetSize(150+10, 180+30)
		self.ModelPreviewBoard.SetPosition(0, 0)
		self.ModelPreviewBoard.Show()

		self.ModelPreview = ui.RenderTarget()
		self.ModelPreview.SetParent(self.ModelPreviewBoard)
		self.ModelPreview.SetSize(150, 180)
		self.ModelPreview.SetPosition(5, 22)
		self.ModelPreview.SetRenderTarget(RENDER_TARGET_INDEX)
		self.ModelPreview.Show()

	def __del__(self):
		ui.Window.__del__(self)
		self.ResetInit()
		
	def Destroy(self):
		self.ResetInit()
		
	def ResetInit(self):
		self.SetFuncDown = None
		self.itemList = []
		self.scrollBar = None

		self.itemTooltip = None
		self.ModelPreview = None
		self.ModelPreviewBoard = None
		self.selectEvent = None

	def SetParent(self, parent):
		ui.Window.SetParent(self, parent)
		
		self.parent = proxy(parent)
		self.SetPosition(5, 5)
		self.SetSize(parent.GetWidth() - 10, parent.GetHeight() - 10)
		
	def SetScrollBar(self, scrollBar):
		scrollBar.SetScrollEvent(ui.__mem_func__(self.__OnScroll))
		scrollBar.SetScrollStep(0.2)
		self.scrollBar=scrollBar

	def SetEventSelect(self, event):
		self.selectEvent = event
		
	def __OnScroll(self):
		self.AdjustItemPositions(True)

	def GetTotalItemHeight(self):
		totalHeight = 0

		if self.itemList:
			for itemH in self.itemList:
				totalHeight += itemH.GetHeight() + 2
			
		return totalHeight
	
	def GetItemCount(self):
		return len(self.itemList)

	def AppendItemCostume(self, ItemVnum, Type):
		item = self.NewItemCostume(self, ItemVnum, Type)
		item.SetParent(self)

		if len(self.itemList) == 0:
			item.SetBasePosition(0, 0)
		else:
			x, y = self.itemList[-1].GetLocalPosition()
			y += 2
			item.SetBasePosition(0, y + self.itemList[-1].GetHeight())

		item.SetOverInEvent(ui.__mem_func__(self.OverInItemRender))
		item.SetOverOutEvent(ui.__mem_func__(self.OverOutItemRender))
			
		item.Show()
		self.itemList.append(item)

		self.AdjustScrollBar()
		self.AdjustItemPositions()
		self.scrollBar.Show()

	def AppendItemRefine(self, ItemVnum, Refine):
		item = self.NewItemRefine(self, ItemVnum, Refine)
		item.SetParent(self)

		if len(self.itemList) == 0:
			item.SetBasePosition(0, 0)
		else:
			x, y = self.itemList[-1].GetLocalPosition()
			y += 2
			item.SetBasePosition(0, y + self.itemList[-1].GetHeight())

		item.SetOverInEvent(ui.__mem_func__(self.OverInItem))
		item.SetOverOutEvent(ui.__mem_func__(self.OverOutItem))
			
		item.Show()
		self.itemList.append(item)
		
		self.AdjustScrollBar()
		self.AdjustItemPositions()
		
		self.scrollBar.Show()
	
	def AppendItemPreviewMonster(self, MonsterVnum):
		item = self.NewItemPreviewMonster(self, MonsterVnum)
		item.SetParent(self)

		if len(self.itemList) == 0:
			item.SetBasePosition(0, 0)
		else:
			x, y = self.itemList[-1].GetLocalPosition()
			y += 2
			item.SetBasePosition(0, y + self.itemList[-1].GetHeight())

		item.SetOverInEvent(ui.__mem_func__(self.OverInItem))
		item.SetOverOutEvent(ui.__mem_func__(self.OverOutItem))
			
		item.Show()
		self.itemList.append(item)
		
		self.AdjustScrollBar()
		self.AdjustItemPositions()

		self.scrollBar.Show()		

	def AppendItemMonster(self, MonsterVnum):
		item = self.NewItemMonster(self, MonsterVnum, len(self.itemList) + 1)
		item.SetParent(self)

		if len(self.itemList) == 0:
			item.SetBasePosition(0, 0)
		else:
			x, y = self.itemList[-1].GetLocalPosition()
			y += 2
			item.SetBasePosition(0, y + self.itemList[-1].GetHeight())

		item.SetOverInEvent(ui.__mem_func__(self.OverInItem))
		item.SetOverOutEvent(ui.__mem_func__(self.OverOutItem))
		item.SetClickEvent(ui.__mem_func__(self.SelectPreview))
			
		item.Show()
		self.itemList.append(item)
		
		self.AdjustScrollBar()
		self.AdjustItemPositions()
		
		self.scrollBar.Show()
		item.CreateDropMonster(self)
	
	def SelectPreview(self, MonsterVnum):
		self.Clear()
		self.ResetScrollbar()
		self.AppendItemPreviewMonster(MonsterVnum)
	
	def AppendItemChest(self, ItemVnum):
		item = self.NewItemChest(self, ItemVnum)
		item.SetParent(self)

		if len(self.itemList) == 0:
			item.SetBasePosition(0, 0)
		else:
			x, y = self.itemList[-1].GetLocalPosition()
			y += 2
			item.SetBasePosition(0, y + self.itemList[-1].GetHeight())

		item.SetOverInEvent(ui.__mem_func__(self.OverInItem))
		item.SetOverOutEvent(ui.__mem_func__(self.OverOutItem))
			
		item.Show()
		self.itemList.append(item)
		
		self.AdjustScrollBar()
		self.AdjustItemPositions()
		
		self.scrollBar.Show()

	def AppendItemTextFile(self, banner, TextFile):
		item = self.NewItemText()
		item.SetParent(self)
		item.RegisterScroll(self.parent)
		item.SetBannerImage(banner)
		item.LoadFile(TextFile)

		if len(self.itemList) == 0:
			item.SetBasePosition(0, 0)
		else:
			x, y = self.itemList[-1].GetLocalPosition()
			y += 2
			item.SetBasePosition(0, y + self.itemList[-1].GetHeight())

		# item.SetOverInEvent(ui.__mem_func__(self.OverInItem))
		# item.SetOverOutEvent(ui.__mem_func__(self.OverOutItem))
			
		item.Show()
		self.itemList.append(item)
		
		self.AdjustScrollBar()
		self.AdjustItemPositions()
		
		self.scrollBar.Hide()

	def OverInItem(self, ItemVnum):
		if self.itemTooltip and ItemVnum != 0:
			self.itemTooltip.SetItemToolTip(ItemVnum)
			self.ModelPreviewBoard.Hide()
			
	def OverOutItem(self):
		if self.itemTooltip:
			self.itemTooltip.HideToolTip()
			self.itemTooltip.ClearToolTip()

	def OverOutItemRender(self):
		if not self.itemTooltip:
			return
	
		self.itemTooltip.ClearToolTip()
		self.itemTooltip.HideToolTip()
		renderTarget.SetVisibility(RENDER_TARGET_INDEX, False)
		self.ModelPreviewBoard.Hide()
	
	def OverInItemRender(self, Race, Vnum, TypeItem):
		if not self.itemTooltip:
			return
		
		self.itemTooltip.ClearToolTip()
		
		renderTarget.SetVisibility(RENDER_TARGET_INDEX, True)
		renderTarget.SelectModel(RENDER_TARGET_INDEX, Race)
		renderTarget.SetBackground(RENDER_TARGET_INDEX, "d:/ymir work/ui/game/myshop_deco/model_view_bg.sub")

		self.itemTooltip.SetSize(160, 211)
		self.itemTooltip.toolTipHeight = 211
		self.ModelPreviewBoard.Show()
		self.itemTooltip.ShowToolTip()
		
		if TypeItem == -1: # is monster
			return

		if TypeItem == item.COSTUME_TYPE_BODY:
			renderTarget.SetArmor(RENDER_TARGET_INDEX, Vnum)
		elif TypeItem == item.COSTUME_TYPE_WEAPON:
			renderTarget.SetWeapon(RENDER_TARGET_INDEX, Vnum)
		elif TypeItem == item.COSTUME_TYPE_HAIR:
			renderTarget.SetHair(RENDER_TARGET_INDEX, Vnum)
		elif TypeItem == item.COSTUME_TYPE_SASH or TypeItem == item.COSTUME_SKIN_SASH:
			renderTarget.SetSash(RENDER_TARGET_INDEX, Vnum - 85000)
		elif TypeItem == item.COSTUME_TYPE_CROWN:
			item.SelectItem(Vnum)
			renderTarget.SetCrown(RENDER_TARGET_INDEX, item.GetValue(2))

	def AdjustScrollBar(self):
		totalHeight = float(self.GetTotalItemHeight())
		if totalHeight:
			scrollBarHeight = min(float(self.GetHeight() - 10) / totalHeight, 1.0)
		else:
			scrollBarHeight = 1.0
			
		self.scrollBar.SetMiddleBarSize(scrollBarHeight)
		
	def ResetScrollbar(self):
		self.scrollBar.SetPos(0)

	def AdjustItemPositions(self, scrolling = False, startIndex = -1):		
		scrollPos = self.scrollBar.GetPos()
		totalHeight = self.GetTotalItemHeight() - self.GetHeight()

		idx = 0
		if startIndex >= 0:
			idx = startIndex
		
		for item in self.itemList[idx:]:
			xB, yB = item.GetBasePosition()
			
			if startIndex >= 0:
				yB -= ITEM_HEIGHT + 2
			
			if scrolling:
				setPos = yB - int(scrollPos * totalHeight)
				item.SetPosition(xB, setPos)
			else:
				item.SetPosition(xB, yB)
				
			item.SetBasePosition(xB, yB)

	def Clear(self):
		if len(self.itemList) == 0:
			return

		for item in self.itemList:
			item.ResetInit()
			item.Hide()
			del item
		
		self.OverOutItemRender()
		self.itemList = []

## LISTBOX_ITEM

class ListBoxCategory(ui.Window):
	class NewItem(ui.Window):
		def __init__(self, parent, name, type, ForType, Subtype, IsSubCategory):
			ui.Window.__init__(self)
			self.ThinBoardCircle = None
			self.background = None
			self.Arrow = None
			self.Bar = None
			self.Banner = ""
			self.ResetInit()

			self.Type = type
			self.ForType = ForType
			self.Subtype = Subtype
			self.IsSubCategory = IsSubCategory
			self.IsExpanded = False
			self.IsVisible = False
	
			if IsSubCategory == False:
				self.SplitLine = ui.ExpandedImageBox()
				self.SplitLine.AddFlag("attach")
				self.SplitLine.AddFlag("not_pick")
				self.SplitLine.LoadImage("d:/ymir work/ui/game/comp/split_line.tga")
				self.SplitLine.SetParent(self, parent.hWnd)
				self.SplitLine.SetPosition(0, 0)
				self.SplitLine.Show()

				self.AppendCategory(parent, name, type)
			else:
				self.AppendSubCategory(parent, name, ForType)
		
		def CreateNewCorner(self):
			length = len(self.Corners)
		
			Corner = ui.ExpandedImageBox()
			Corner.AddFlag("attach")
			Corner.AddFlag("not_pick")
			Corner.LoadImage("d:/ymir work/ui/game/comp/left_right_line.tga")
			Corner.SetParent(self, self.parent.hWnd)
			Corner.SetPosition(0, 18 + length*20)
			Corner.Show()
			
			self.Corners.append(Corner)
		
		def AppendCategory(self, MainParent, name, type):
			self.background = ui.ExpandedImageBox()
			self.background.SetParent(self, MainParent.hWnd)
			self.background.LoadImage(PATH + "category.tga")
			self.background.OnMouseLeftButtonDown = self.OnSelectImageBox
			self.background.Show()

			self.Arrow = ui.ExpandedImageBox()
			self.Arrow.SetParent(self.background, MainParent.hWnd)
			self.Arrow.LoadImage(PATH + "arrow.tga")
			self.Arrow.SetPosition(94, 6)
			self.Arrow.Show()

			self.NameCategory = ui.TextLine()
			self.NameCategory.SetParent(self.background, MainParent.hWnd)
			self.NameCategory.SetVerticalAlignCenter()	
			self.NameCategory.SetWindowVerticalAlignCenter()
			self.NameCategory.SetText(name)
			self.NameCategory.SetPosition(7, -1)
			self.NameCategory.Show()

			self.SetSize(self.background.GetWidth(), self.background.GetHeight())

		def Show(self):
			if self.IsShow() == FALSE:
				if SHOW_ANIMATION_CATEGORY:
					self.ResetAnim()
				ui.Window.Show(self)
			
		def Hide(self):
			ui.Window.Hide(self)

		def AppendSubCategory(self, MainParent, name, ForType):
			self.Bar = ui.Bar()
			self.Bar.SetParent(self)
			self.Bar.AddFlag("attach")
			self.Bar.AddFlag("not_pick")
			self.Bar.SetColor(SELECT_COLOR)
			self.Bar.SetSize(108 - 1, 20 - 3)
			self.Bar.SetPosition(2, 0)
			self.SetInsideRender(True)
			self.Bar.Hide()

			self.NameCategory = ui.TextLine()
			self.NameCategory.SetParent(self, MainParent.hWnd)
			self.NameCategory.SetText(name)
			self.NameCategory.SetPosition(7, 3)
			self.NameCategory.Show()

			self.SetSize(108, 20)
		
		def SetVisible(self, flag):
			self.IsVisible = flag

		def GetItemType(self):
			return self.ForType
		
		def CanRender(self):
			if self.NameCategory.IsShow():
				return True
				
			return False
		
		def IsHide(self):
			return self.IsVisible

		def IsExpanded(self):
			return self.IsExpanded
		
		def SetSelect(self, flag):
			self.selected = flag
		
		def OnMouseLeftButtonDown(self):
			if self.IsSubCategory == False:
				return

			if self.clickEvent:
				self.clickEvent(self.Banner, self.ForType, self.Type, self.Subtype, False)
	
			self.selected = True

			if SHOW_ANIMATION_CATEGORY:
				self.ResetAnim()
	
		def OnSelectImageBox(self):
			if self.IsSubCategory:
				return
		
			if self.IsExpanded:
				self.IsExpanded = False
				self.Arrow.LoadImage(PATH + "arrow.tga")
				
				for corner in self.Corners:
					if corner:
						corner.Show()
				if self.SplitLine:
					self.SplitLine.Show()
			else:
				self.IsExpanded = True
				self.Arrow.LoadImage(PATH + "arrow_up.tga")
				
				for corner in self.Corners:
					if corner:
						corner.Hide()
				if self.SplitLine:
					self.SplitLine.Hide()

			if self.clickEvent:
				self.clickEvent("", 99, self.Type, 0, self.IsExpanded)
		
		# ANIMATION_CODE
		def ResetAnim(self):
			self.widthAnim = 0
	
		def __del__(self):
			ui.Window.__del__(self)
			self.ResetInit()

		def ResetInit(self):
			self.selected = False
			self.vnum = 0
			self.xBase = 0
			self.yBase = 0

			self.overInEvent = None
			self.overOutEvent = None
			self.clickEvent = None
			self.NameCategory = None
			if self.background != None:
				self.background.Hide()
			if self.Arrow != None:
				self.Arrow.Hide()
			self.background = None
			self.Arrow = None
			self.SplitLine = None
			self.Corners = []

		def SetParent(self, parent):
			ui.Window.SetParent(self, parent)
			self.parent = proxy(parent)

		def SetBasePosition(self, x, y):
			self.xBase = x
			self.yBase = y
			
		def GetBasePosition(self):
			return (self.xBase, self.yBase)
			
		def SetOverInEvent(self, event):
			self.overInEvent = event
			
		def SetOverOutEvent(self, event):
			self.overOutEvent = event
			
		def SetClickEvent(self, event):
			self.clickEvent = event

		def IsSelected(self):
			return self.selected
				
		def RefreshSelectState(self, isIn):
			if not self.background:
				return

		def OnRenderWiki(self):	
			if self.Bar:
				if self.IsIn():
					self.Bar.Show()
				elif self.selected:
					self.Bar.Show()
				else:
					self.Bar.Hide()

	def __init__(self):
		ui.Window.__init__(self)
		self.ResetInit()

	def __del__(self):
		ui.Window.__del__(self)
		self.ResetInit()
		
	def Destroy(self):
		self.ResetInit()
		
	def ResetInit(self):
		self.SetFuncDown = None
		self.itemList = []
		self.scrollBar = None

		self.selectEvent = None

	def SetParent(self, parent):
		ui.Window.SetParent(self, parent)
		
		self.SetPosition(5, 5)
		self.SetSize(parent.GetWidth() - 10, parent.GetHeight() - 10)
		
	def SetScrollBar(self, scrollBar):
		scrollBar.SetScrollEvent(ui.__mem_func__(self.__OnScroll))
		scrollBar.SetScrollStep(0.2)
		self.scrollBar=scrollBar

	def SetEventSelect(self, event):
		self.selectEvent = event
		
	def __OnScroll(self):
		self.AdjustItemPositions(True)
			
	def GetTotalItemHeight(self):
		totalHeight = 0
		
		if self.itemList:
			for itemH in self.itemList:
				totalHeight += itemH.GetHeight() + 2
			
		return totalHeight + 20

	def GetItemCount(self):
		return len(self.itemList)
			
	def AppendItem(self, Name, Type, ForType = -1, Subtype = -1, IsSubCategory = False):
		item = self.NewItem(self, Name, Type, ForType, Subtype, IsSubCategory)
		item.SetParent(self)

		if len(self.itemList) == 0:
			item.SetBasePosition(0, 0)
		else:
			x, y = self.itemList[-1].GetLocalPosition()
			y += 2
			item.SetBasePosition(0, y + self.itemList[-1].GetHeight())

		item.SetClickEvent(ui.__mem_func__(self.SelectItem))
			
		item.Show()
		self.itemList.append(item)

		self.AdjustScrollBar()
		self.AdjustItemPositions()
		return item

	def SelectItem(self, Banner, ForType, Type, SubType, flag):
		for item in self.itemList:
			if ForType == 99:
				if item.GetItemType() == Type:
					item.SetVisible(flag)
			else:
				if item.IsSubCategory:
					item.SetSelect(flag)

		self.AdjustItemPositions(True)
		
		if ForType > -2 and ForType != 99: # ONLY_FOR_SUBCATEGORIES
			self.selectEvent(Banner, ForType, Type, SubType)

	def AppendSubCategory(self, Banner, name, ForType, Type, Subtype = -1):
		SubCat = self.AppendItem(name, Type, ForType, Subtype, 1)
		SubCat.Banner = Banner
		
		for item in self.itemList:
			if item.IsSubCategory == False and item.Type == ForType:
				item.CreateNewCorner()
				length = len(item.Corners) + 1
				item.SplitLine.SetPosition(0, (20 * length) - 3)
	
	def AdjustScrollBar(self):
		totalHeight = float(self.GetTotalItemHeight())
		if totalHeight:
			scrollBarHeight = min(float(self.GetHeight() - 10) / totalHeight, 1.0)
		else:
			scrollBarHeight = 1.0
			
		self.scrollBar.SetMiddleBarSize(scrollBarHeight)
		
	def ResetScrollbar(self):
		self.scrollBar.SetPos(0)

	def AdjustItemPositions(self, scrolling = False, startIndex = -1):		
		scrollPos = self.scrollBar.GetPos()
		totalHeight = self.GetTotalItemHeight() - self.GetHeight()

		idx = 0
		if startIndex >= 0:
			idx = startIndex
		
		CurIdx, yAccumulate = 0, 0
		for item in self.itemList[idx:]:
			if startIndex >= 0:
				yAccumulate -= 20 + 2 # 20-item-height

			if item.IsHide():
				item.Hide()
				continue
			else:
				item.Show()
				
			if item.IsSubCategory == False and CurIdx > 0:
				yAccumulate += 5
	
			if scrolling:
				setPos = yAccumulate - int(scrollPos * totalHeight)
				item.SetPosition(0, setPos)
			else:
				item.SetPosition(0, yAccumulate)
				
			item.SetBasePosition(0, yAccumulate)
			
			CurIdx += 1
			yAccumulate += 20

	def Clear(self):
		if len(self.itemList) == 0:
			return
	
		range = len(self.itemList)
		for i in xrange(int(range)):
			self.itemList[i].ResetInit()
			self.itemList[i].Hide()
		
		del self.itemList[:]
		self.itemList = []
		
	def GetList(self):
		return self.itemList


class WikiNewWindow(ui.ScriptWindow):
	def __init__(self):
		ui.ScriptWindow.__init__(self)
		self.bIsLoaded = False
		self.tooltipItem = None
		self.TypeSelected = -1
		self.SubTypeSelected = -1
		self.CurentSize = 0
		self.PrevSize = 0

		self.__LoadWindow()

	def __del__(self):
		ui.ScriptWindow.__del__(self)
	
	def __LoadWindow(self):
		if self.bIsLoaded:
			return
		
		self.bIsLoaded = True

		self.AddFlag("float")
		self.AddFlag("movable")
		self.AddFlag("animation")

		self.Board = ui.BoardWithTitleBar()
		self.Board.SetParent(self)
		self.Board.SetSize(715, 485)
		self.Board.SetTitleName("Wikipedia")
		self.Board.AddFlag("not_pick")
		self.Board.SetCloseEvent(ui.__mem_func__(self.Close))
		self.Board.Show()	
		
		self.borderNew = ui.BorderNew()
		self.borderNew.SetParent(self.Board)
		self.borderNew.SetPosition(145, 34)
		self.borderNew.SetSize(560, 440)
		self.borderNew.Show()
		
		self.borderThin = ui.ThinBoard()
		self.borderThin.SetParent(self.borderNew)
		self.borderThin.SetPosition(1, 1)
		self.borderThin.SetSize(558, 70)
		self.borderThin.Show()	
		
		# self.Board = ui.ExpandedImageBox()
		# self.Board.SetParent(self)
		# self.Board.LoadImage(PATH + "bg.tga")
		# self.Board.Show()
		
		# self.TitleBar = ui.TitleBar()
		# self.TitleBar.SetParent(self)
		# self.TitleBar.MakeTitleBar(712 - 15, "red")
		# self.TitleBar.SetPosition(8, 7)
		# self.TitleBar.SetCloseEvent(ui.__mem_func__(self.Close))
		# self.TitleBar.Show()

		# self.TitleName = ui.TextLine()
		# self.TitleName.SetParent(self)
		# self.TitleName.AddFlag("not_pick")
		# self.TitleName.SetText("Wikipedia")
		# self.TitleName.SetPosition(0, 9)
		# self.TitleName.SetWindowHorizontalAlignCenter()
		# self.TitleName.SetHorizontalAlignCenter()
		# self.TitleName.Show()

		# self.ThinFull = ui.MakeThinBoardCircle(self.Board, 7, 34, 130, self.Board.GetHeight() - 40, False)
		self.ThinFull = ui.BorderNew()
		self.ThinFull.SetParent(self.Board)
		self.ThinFull.SetPosition(7, 34)
		self.ThinFull.SetSize(130, self.Board.GetHeight() - 45)
		self.ThinFull.Show()
		
		self.ImgItemName = ui.MakeImageBox(self, PATH+"searchfield.tga", 11, 41)
		
		self.banner = ui.ExpandedImageBox()
		self.banner.SetParent(self)
		self.banner.SetPosition(149, 37)
		self.banner.LoadImage("d:/ymir work/ui/wiki/banners2/alegecategorie.png")
		self.banner.Show()
		
		self.sItemName = ui.EditLine()
		self.sItemName.SetParent(self.ImgItemName)
		self.sItemName.SetPosition(5, 6)
		self.sItemName.SetSize(150, 20)
		self.sItemName.SetMax(25)
		self.sItemName.OnIMEUpdate = ui.__mem_func__(self.__OnValueUpdate)
		self.sItemName.SetReturnEvent(ui.__mem_func__(self.OnSearch))
		self.sItemName.SetTabEvent(ui.__mem_func__(self.OnReturnItemName))
		self.sItemName.SelectedItemVnum = 0
		self.sItemName.SelectedIsMonster = 0
		self.sItemName.SelectedType = 0
		self.sItemName.Show()
		
		self.wndMatchItemName = ui.TextLine()
		self.wndMatchItemName.SetParent(self.sItemName)
		self.wndMatchItemName.AddFlag("not_pick")
		self.wndMatchItemName.SetPosition(self.sItemName.GetTextSize()[0] + 1, 0)
		self.wndMatchItemName.SetOutline(True)
		self.wndMatchItemName.SetPackedFontColor(0xff888888)
		self.wndMatchItemName.Show()

		self.searchButton = ui.Button()
		self.searchButton.SetParent(self)
		self.searchButton.SetUpVisual("d:/ymir work/ui/switchbot/btn_small_01.sub")
		self.searchButton.SetOverVisual("d:/ymir work/ui/switchbot/btn_small_02.sub")
		self.searchButton.SetDownVisual("d:/ymir work/ui/switchbot/btn_small_03.sub")
		self.searchButton.SetDisableVisual("d:/ymir work/ui/switchbot/btn_small_01.sub")
		self.searchButton.SetPosition(45, 120)
		self.searchButton.SetText(localeInfo.WIKI_TEXT_12)
		self.searchButton.SetEvent(ui.__mem_func__(self.OnSearch))
		# self.searchButton.Show()

		self.MakeCategory()

		self.RacesImage = {}
		self.RacesImage[0] = ui.MakeRadioButton(self, 155, 113, PATH, "ingame_wiki_wolfman/class_w_normal.tga", "ingame_wiki_wolfman/class_w_hover.tga", "ingame_wiki_wolfman/class_w_selected.tga")
		self.RacesImage[1] = ui.MakeRadioButton(self, 265, 113, PATH, "ingame_wiki_wolfman/class_n_normal.tga", "ingame_wiki_wolfman/class_n_hover.tga", "ingame_wiki_wolfman/class_n_selected.tga")
		self.RacesImage[2] = ui.MakeRadioButton(self, 375, 113, PATH, "ingame_wiki_wolfman/class_su_normal.tga", "ingame_wiki_wolfman/class_su_hover.tga", "ingame_wiki_wolfman/class_su_selected.tga")
		self.RacesImage[3] = ui.MakeRadioButton(self, 485, 113, PATH, "ingame_wiki_wolfman/class_s_normal.tga", "ingame_wiki_wolfman/class_s_hover.tga", "ingame_wiki_wolfman/class_s_selected.tga")
		self.RacesImage[4] = ui.MakeRadioButton(self, 595, 113, PATH, "ingame_wiki_wolfman/class_l_normal.tga", "ingame_wiki_wolfman/class_l_hover.tga", "ingame_wiki_wolfman/class_l_selected.tga")

		for x in xrange(5):
			self.RacesImage[x].SetEvent(ui.__mem_func__(self.SelectRaceFlag), x)
	
		self.PrevButton = ui.MakeButton(self, 13, 450, False, PATH, "btn_arrow_left_normal.tga", "btn_arrow_left_hover.tga", "btn_arrow_left_down.tga")
		self.PrevButton.SetEvent(ui.__mem_func__(self.OnPrev))
	
		self.NextButton = ui.MakeButton(self, 74, 450, False, PATH, "btn_arrow_right_normal.tga", "btn_arrow_right_hover.tga", "btn_arrow_right_down.tga")
		self.NextButton.SetEvent(ui.__mem_func__(self.OnNext))
		
		self.ItemScrollBar = ui.ScrollBar()
		self.ItemScrollBar.SetParent(self)
		self.ItemScrollBar.SetScrollBarSize(307 + 40)
		self.ItemScrollBar.SetPosition(693, 150 - 40)
		self.ItemScrollBar.Show()
	
		self.ItemList = ListBoxItem()
		self.ItemList.SetParent(self)
		self.ItemList.SetSize(543, 356)
		self.ItemList.SetPosition(149, 110)
		self.ItemList.SetScrollBar(self.ItemScrollBar)
		self.ItemList.Show()

		self.SetSize(self.Board.GetWidth(), self.Board.GetHeight())
		self.ManageRacesImage()
		self.SelectRaceFlag(0)

	def SelectRaceFlag(self, index):
		for i in xrange(5):
			if i == index:
				self.RacesImage[i].Down()
			else:
				self.RacesImage[i].SetUp()	

		self.SelectAntiFlag = ANTI_FLAG_DICT[index]
		self.SearchEquipment(self.TypeSelected, self.SubTypeSelected)

	def ManageRacesImage(self, Hide = True):
		for x in xrange(len(self.RacesImage)):
			if Hide:
				self.RacesImage[x].Hide()
			else:
				self.RacesImage[x].Show()
				
		if Hide:
			self.ItemList.SetSize(543, 356)
			self.ItemList.SetPosition(149, 110)
			
			self.ItemScrollBar.SetScrollBarSize(307 + 40)
			self.ItemScrollBar.SetPosition(693, 150 - 40)
		else:
			self.ItemList.SetSize(543, 320)
			self.ItemList.SetPosition(149, 150)
			
			self.ItemScrollBar.SetScrollBarSize(320)
			self.ItemScrollBar.SetPosition(693, 150)

	def MakeCategory(self):
		self.wndCategories = ui.TextLine()
		self.wndCategories.SetParent(self)
		self.wndCategories.AddFlag("not_pick")
		self.wndCategories.SetText(localeInfo.WIKI_TEXT_13)
		self.wndCategories.SetPosition(10, 72)
		self.wndCategories.SetPackedFontColor(0xff888888)
		self.wndCategories.Show()
	
		self.CategoryScrollBar = ui.ScrollBar()
		self.CategoryScrollBar.SetParent(self)
		self.CategoryScrollBar.SetScrollBarSize(350)
		self.CategoryScrollBar.SetPosition(125, 89)
		self.CategoryScrollBar.Show()
	
		self.CategoryList = ListBoxCategory()
		self.CategoryList.SetParent(self)
		self.CategoryList.SetSize(109, 350)
		self.CategoryList.SetPosition(10, 89)
		self.CategoryList.SetScrollBar(self.CategoryScrollBar)
		self.CategoryList.SetEventSelect(ui.__mem_func__(self.SelectFromCategory))
		self.CategoryList.Show()
	
		self.CategoryList.AppendItem(localeInfo.SEARCH_OBJECT_EQUIP, 1)
		self.CategoryList.AppendSubCategory("d:/ymir work/ui/wiki/banners2/arme.png", "Arme", 1, item.ITEM_TYPE_WEAPON)
		self.CategoryList.AppendSubCategory("d:/ymir work/ui/wiki/banners2/armuri.png", "Armuri", 1, item.ITEM_TYPE_ARMOR, item.ARMOR_BODY)
		self.CategoryList.AppendSubCategory("d:/ymir work/ui/wiki/banners2/coifuri.png", localeInfo.SEARCH_OBJECT_HEAD, 1, item.ITEM_TYPE_ARMOR, item.ARMOR_HEAD)
		self.CategoryList.AppendSubCategory("d:/ymir work/ui/wiki/banners2/scuturi.png", localeInfo.SEARCH_OBJECT_SHIELD, 1, item.ITEM_TYPE_ARMOR, item.ARMOR_SHIELD)
		self.CategoryList.AppendSubCategory("d:/ymir work/ui/wiki/banners2/cercei.png", localeInfo.SEARCH_OBJECT_EAR, 1, item.ITEM_TYPE_ARMOR, item.ARMOR_EAR)
		self.CategoryList.AppendSubCategory("d:/ymir work/ui/wiki/banners2/bratari.png", localeInfo.SEARCH_OBJECT_WRIST, 1, item.ITEM_TYPE_ARMOR, item.ARMOR_WRIST)
		self.CategoryList.AppendSubCategory("d:/ymir work/ui/wiki/banners2/coliere.png", localeInfo.SEARCH_OBJECT_NECK, 1, item.ITEM_TYPE_ARMOR, item.ARMOR_NECK)
		self.CategoryList.AppendSubCategory("d:/ymir work/ui/wiki/banners2/papuci.png", localeInfo.SEARCH_OBJECT_SHOES, 1, item.ITEM_TYPE_ARMOR, item.ARMOR_FOOTS)
		self.CategoryList.AppendSubCategory("d:/ymir work/ui/wiki/banners2/curele.png", "Curele", 1, item.ITEM_TYPE_BELT)

		self.CategoryList.AppendItem(localeInfo.WIKI_CAT_01, 2)
		self.CategoryList.AppendSubCategory("d:/ymir work/ui/wiki/banners2/sefi.png", "Nivel 1 - 105", 2, 0, [3, 1, 150])
		# self.CategoryList.AppendSubCategory("d:/ymir work/ui/wiki/banners2/sefi.png", "Nivel 75 - 100", 2, 0, [3, 75, 100])
		# self.CategoryList.AppendSubCategory("d:/ymir work/ui/wiki/banners2/sefi.png", "Nivel 100+", 2, 0, [3, 100, 150])

		self.CategoryList.AppendItem(localeInfo.WIKI_CAT_02, 3)
		self.CategoryList.AppendSubCategory("d:/ymir work/ui/wiki/banners2/pietremetin.png", "Nivel 1 - 105", 3, 0, [2, 1, 150])

		self.CategoryList.AppendItem(localeInfo.WIKI_CAT_03, 4)
		self.CategoryList.AppendSubCategory("d:/ymir work/ui/wiki/banners2/monstrii.png", "Nivel 1 - 105", 4, 0, [0, 1, 150])
		# self.CategoryList.AppendSubCategory("d:/ymir work/ui/wiki/banners/monster.tga", "Nivel 75 - 100", 4, 0, [0, 75, 100])
		# self.CategoryList.AppendSubCategory("d:/ymir work/ui/wiki/banners/monster.tga", "Nivel 100+", 4, 0, [0, 100, 150])

		self.CategoryList.AppendItem(localeInfo.WIKI_CAT_04, 6)
		self.CategoryList.AppendSubCategory("d:/ymir work/ui/wiki/banners2/cufere.png", "Cufere", 6, 0, 0)
		# self.CategoryList.AppendSubCategory("d:/ymir work/ui/wiki/banners2/cufere.png", "Cufere", 6, 0, 1)
		# self.CategoryList.AppendSubCategory("d:/ymir work/ui/wiki/banners2/cufere.png", "Cufere", 6, 0, 2)
		# self.CategoryList.AppendSubCategory("d:/ymir work/ui/wiki/banners2/cufere.png", "Cufere Metine", 6, 0, 2)
		# self.CategoryList.AppendSubCategory("d:/ymir work/ui/wiki/banners2/cufere.png", localeInfo.WIKI_OBJECT_MOBCHEST, 6, 0, 1)

		self.CategoryList.AppendItem(localeInfo.SEARCH_OBJECT_COSTUME, 5)
		self.CategoryList.AppendSubCategory("d:/ymir work/ui/wiki/banners2/costumearma.png", localeInfo.SEARCH_OBJECT_COSTUMEWEAP, 5, item.ITEM_TYPE_COSTUME, item.COSTUME_TYPE_WEAPON)
		self.CategoryList.AppendSubCategory("d:/ymir work/ui/wiki/banners2/costume.png", localeInfo.SEARCH_OBJECT_COSTUME, 5, item.ITEM_TYPE_COSTUME, item.COSTUME_TYPE_BODY)
		self.CategoryList.AppendSubCategory("d:/ymir work/ui/wiki/banners2/frizuri.png", localeInfo.SEARCH_OBJECT_HAIR, 5, item.ITEM_TYPE_COSTUME, item.COSTUME_TYPE_HAIR)
		self.CategoryList.AppendSubCategory("d:/ymir work/ui/wiki/banners2/accesoriicostum.png", localeInfo.SEARCH_OBJECT_COSTUMEACC, 5, item.ITEM_TYPE_COSTUME, item.COSTUME_TYPE_CROWN)
		self.CategoryList.AppendSubCategory("d:/ymir work/ui/wiki/banners2/esarfe.png", localeInfo.SEARCH_OBJECT_SASH, 5, item.ITEM_TYPE_COSTUME, item.COSTUME_TYPE_SASH)
		self.CategoryList.AppendSubCategory("d:/ymir work/ui/wiki/banners2/costumesarfa.png", localeInfo.SEARCH_OBJECT_SASHSKIN, 5, item.ITEM_TYPE_COSTUME, item.COSTUME_SKIN_SASH)
		self.CategoryList.AppendSubCategory("d:/ymir work/ui/wiki/banners2/peturi.png", localeInfo.SEARCH_OBJECT_PET, 5, item.ITEM_TYPE_COSTUME, 3)
		self.CategoryList.AppendSubCategory("d:/ymir work/ui/wiki/banners2/mounts.png", localeInfo.SEARCH_OBJECT_MOUNT, 5, item.ITEM_TYPE_COSTUME, item.COSTUME_TYPE_MOUNT)
		
		self.CategoryList.AppendItem("Evenimente", 7)
		self.CategoryList.AppendSubCategory("", localeInfo.EVENT_01, 7, "events/cufere_hexagoane_event.txt")
		self.CategoryList.AppendSubCategory("", localeInfo.EVENT_02, 7, "events/50_tare_metine.txt")
		self.CategoryList.AppendSubCategory("", localeInfo.EVENT_03, 7, "events/cult_intunecat.txt")
		self.CategoryList.AppendSubCategory("", localeInfo.EVENT_04, 7, "events/dublu_drop_metine.txt")
		self.CategoryList.AppendSubCategory("", localeInfo.EVENT_05, 7, "events/dublu_drop_sefi.txt")
		self.CategoryList.AppendSubCategory("", localeInfo.EVENT_06, 7, "events/eveniment_litere.txt")
		self.CategoryList.AppendSubCategory("", localeInfo.EVENT_07, 7, "events/ruleta_cult_intunecat.txt")

	def SelectFromCategory(self, Banner, ForType, Type, subcategory):
		self.ForTypeSelected = ForType
		self.TypeSelected = Type
		self.SubTypeSelected = subcategory
		
		self.ItemList.Clear()
		self.ItemList.ResetScrollbar()
		self.ManageRacesImage()

		self.CurentSize = 0
		self.PrevSize = 0
		
		if ForType == 1:
			self.SearchEquipment(Type, subcategory)
			self.ManageRacesImage(False)
		elif ForType == 2 or ForType == 3 or ForType == 4:
			self.SearchMonster(subcategory[0], subcategory[1], subcategory[2])
		elif ForType == 6:
			self.SearchChest(subcategory)
		elif ForType == 5:
			self.SearchCostumation(Type, subcategory)
		elif ForType == 7:
			self.ItemList.AppendItemTextFile(self.banner, Type)
			
		if len(Banner) > 1:
			self.banner.LoadImage(Banner)

	def OnPrev(self):
		if self.ItemList.GetItemCount() == 0:
			return

		temp = self.PrevSize

		if temp <= 0:
			temp = -1
		
		# chat.AppendChat(1, "prev Size: %d, Temp :%d" % (self.CurentSize, temp))

		if self.ForTypeSelected == 1:
			self.SearchEquipment(self.TypeSelected, self.SubTypeSelected, temp)
		elif self.ForTypeSelected == 2 or self.ForTypeSelected == 3 or self.ForTypeSelected == 4:
			self.SearchMonster(self.SubTypeSelected[0], self.SubTypeSelected[1], self.SubTypeSelected[2], temp)
		elif self.ForTypeSelected == 6:
			self.SearchChest(self.SubTypeSelected, temp)
		elif self.ForTypeSelected == 5:
			self.SearchCostumation(self.TypeSelected, self.SubTypeSelected, temp)
		
	def OnNext(self):
		count = self.ItemList.GetItemCount()*4 if self.ForTypeSelected == 5 else self.ItemList.GetItemCount()
		if count < MAX_LINE_COSTUMATION_ITER - 1:
			return
		
		# chat.AppendChat(1, "Size: %d" % (self.CurentSize -1))
		
		if self.ForTypeSelected == 1:
			self.SearchEquipment(self.TypeSelected, self.SubTypeSelected, self.CurentSize)
		elif self.ForTypeSelected == 2 or self.ForTypeSelected == 3 or self.ForTypeSelected == 4:
			self.SearchMonster(self.SubTypeSelected[0], self.SubTypeSelected[1], self.SubTypeSelected[2], self.CurentSize)
		elif self.ForTypeSelected == 6:
			self.SearchChest(self.SubTypeSelected, self.CurentSize)
		elif self.ForTypeSelected == 5:
			self.SearchCostumation(self.TypeSelected, self.SubTypeSelected, self.CurentSize - 1)

	def SearchChest(self, Type, StartIndex = -1):
		bCanUpdatePage = -2

		for xitem in wikipedia.RequestChest(Type, StartIndex, MAX_LINE_COSTUMATION_ITER):
			if xitem["vnum"][0] == 0:
				continue

			if self.ItemList.GetItemCount() > 0 and bCanUpdatePage == -2:
				self.ItemList.Clear()
				self.ItemList.ResetScrollbar()
			
			bCanUpdatePage = xitem["vnum"][1]
			
			self.ItemList.AppendItemChest(xitem["vnum"][0])
			
		if bCanUpdatePage != -2:
			self.PrevSize = StartIndex - MAX_LINE_COSTUMATION_ITER
			self.CurentSize = bCanUpdatePage

	def SearchEquipment(self, Type, SubType, StartIndex = -1):
		bCanUpdatePage = -2

		for xitem in wikipedia.Request(StartIndex, Type, SubType, self.SelectAntiFlag, MAX_LINE_COSTUMATION_ITER):
			iVnum = xitem["item"][0]
			RefineSet = xitem["item"][1]
			
			if iVnum == 0:
				continue
			
			if self.ItemList.GetItemCount() > 0 and bCanUpdatePage == -2:
				self.ItemList.Clear()
				self.ItemList.ResetScrollbar()
			
			bCanUpdatePage = xitem["item"][2]
		
			self.ItemList.AppendItemRefine(iVnum, RefineSet)

		if bCanUpdatePage != -2:
			self.PrevSize = StartIndex - MAX_LINE_COSTUMATION_ITER
			self.CurentSize = bCanUpdatePage
	
	def SearchMonster(self, Type, MinLevel, MaxLevel, StartIndex = -1):
		bCanUpdatePage = -2

		for xitem in wikipedia.RequestMonster(Type, MinLevel, MaxLevel, StartIndex, MAX_LINE_COSTUMATION_ITER):
			if xitem["vnum"][0] == 0:
				continue

			if self.ItemList.GetItemCount() > 0 and bCanUpdatePage == -2:
				self.ItemList.Clear()
				self.ItemList.ResetScrollbar()
			
			bCanUpdatePage = xitem["vnum"][1]
			
			self.ItemList.AppendItemMonster(xitem["vnum"][0])
			
		if bCanUpdatePage != -2:
			self.PrevSize = StartIndex - MAX_LINE_COSTUMATION_ITER
			self.CurentSize = bCanUpdatePage		
	
	def SearchCostumation(self, Type, SubType, StartIndex = -1):
		tempDict = []
		bCanUpdatePage = -2

		for xitem in item.GetNamesVnum(Type, SubType, StartIndex, MAX_LINE_COSTUMATION_ITER):
			iVnum = xitem["vnum"][0]
			
			if iVnum == 0:
				continue
			
			if self.ItemList.GetItemCount() > 0 and bCanUpdatePage == -2:
				self.ItemList.Clear()
				self.ItemList.ResetScrollbar()
			
			tempDict.append(iVnum)
			bCanUpdatePage = xitem["vnum"][1]
			
			if len(tempDict) >= 4:
				self.ItemList.AppendItemCostume(tempDict, SubType)
				tempDict = []
			
		if len(tempDict) > 0:
			self.ItemList.AppendItemCostume(tempDict, SubType)
		
		if bCanUpdatePage != -2:
			self.PrevSize = StartIndex - MAX_LINE_COSTUMATION_ITER + 2
			self.CurentSize = bCanUpdatePage

	def OnRunMouseWheel(self, nLen):
		if self.CategoryList.IsInPosition() or self.CategoryScrollBar.IsInPosition():
			if nLen > 0:
				self.CategoryScrollBar.OnUp()
			else:
				self.CategoryScrollBar.OnDown()
		elif self.ItemScrollBar.IsShow():
			if nLen > 0:
				self.ItemScrollBar.OnUp()
			else:
				self.ItemScrollBar.OnDown()

		return True
	
	# Extern search by value
	def SearchByInfo(self, Type, Vnum):
		self.ItemList.Clear()
		self.ItemList.ResetScrollbar()
		
		if Type == 0:
			self.ItemList.AppendItemPreviewMonster(Vnum)
			
		if self.IsShow() == FALSE:
			self.Show()
		
	def OnSearch(self):
		if not len(self.sItemName.GetText()) > 2:
			return
		
		if self.sItemName.SelectedItemVnum == 0:
			return
		
		self.ManageRacesImage()
		
		if self.sItemName.SelectedIsMonster == 0:
			item.SelectItem(self.sItemName.SelectedItemVnum)
			
			#SEARCH ALL CATEGORIES
			if item.GetItemType() != item.ITEM_TYPE_COSTUME:
				self.ItemList.Clear()
				self.ItemList.ResetScrollbar()
				
				if item.GetItemType() == item.ITEM_TYPE_ARMOR or item.GetItemType() == item.ITEM_TYPE_WEAPON:
					self.ItemList.AppendItemRefine(self.sItemName.SelectedItemVnum, item.GetRefineSe())
				for ItemCat in wikipedia.FindItemInCategories(self.sItemName.SelectedItemVnum):
					Type = ItemCat["vnum"][0]
					Vnum = ItemCat["vnum"][1]

					# chat.AppendChat(1, "Type :%d Vnum: %d" % (Type, Vnum))
					
					if Type == 0:
						self.ItemList.AppendItemChest(Vnum)
					elif Type == 2:
						self.ItemList.AppendItemMonster(Vnum)
				return
			
			if item.GetItemType() == item.ITEM_TYPE_COSTUME:
				self.ItemList.Clear()
				self.ItemList.ResetScrollbar()
				self.ItemList.AppendItemCostume([self.sItemName.SelectedItemVnum], self.SubTypeSelected)
			# elif item.GetItemType() == item.ITEM_TYPE_ARMOR or item.GetItemType() == item.ITEM_TYPE_WEAPON:
				# self.ItemList.Clear()
				# self.ItemList.ResetScrollbar()
				# self.ItemList.AppendItemRefine(self.sItemName.SelectedItemVnum, item.GetRefineSe())
			# elif item.GetItemType() == item.ITEM_TYPE_GIFTBOX:
				# self.ItemList.Clear()
				# self.ItemList.ResetScrollbar()
				# self.ItemList.AppendItemChest(self.sItemName.SelectedItemVnum)
		else:
			self.ItemList.Clear()
			self.ItemList.ResetScrollbar()
			self.ItemList.AppendItemPreviewMonster(self.sItemName.SelectedItemVnum)
	
	def OnReturnItemName(self):
		if len(self.wndMatchItemName.GetText()) > 0:
			self.sItemName.SetText(self.sItemName.GetText() + self.wndMatchItemName.GetText())
			self.wndMatchItemName.SetText("")
			self.sItemName.SetEndPosition()

	def __OnValueUpdate(self):
		ui.EditLine.OnIMEUpdate(self.sItemName)
		self.sItemName.Disable()
		val = self.sItemName.GetText()
		self.wndMatchItemName.SetPosition(self.sItemName.GetTextSize()[0] + 1, 0)
		
		bFound = False
		if len(val) >= 3:
			for IterItem in GetItems:
				stName = IterItem["name"]
				iVnum  = int(IterItem["vnum"])
				
				if item.IsEquipmentVID(iVnum) and iVnum % 10 > 0:
					continue
				
				if len(stName) >= len(val) and stName[:len(val)].lower() == val.lower():
					self.sItemName.SetText(self.sItemName.GetText())
					self.wndMatchItemName.SetText(stName[len(val):])
					self.wndMatchItemName.SetPosition(self.sItemName.GetTextSize()[0] + 1, 0)
					self.sItemName.SelectedItemVnum = int(iVnum)
					self.sItemName.SelectedIsMonster = 0
					bFound = True
					break

			for iterMob in GetMobs:
				stName = iterMob["name"]
				iVnum  = iterMob["vnum"]
				
				if len(stName) >= len(val) and stName[:len(val)].lower() == val.lower():
					self.sItemName.SetText(self.sItemName.GetText())
					self.wndMatchItemName.SetText(stName[len(val):])
					self.wndMatchItemName.SetPosition(self.sItemName.GetTextSize()[0] + 1, 0)
					self.sItemName.SelectedItemVnum = int(iVnum)
					self.sItemName.SelectedIsMonster = 1
					bFound = True
					break
		
		if not bFound:
			if len(val) >= 3:
				self.sItemName.SetPackedFontColor(0xffFF0000)
			self.wndMatchItemName.SetText("")
			self.sItemName.SelectedItemVnum = 0
		else:
			self.sItemName.SetPackedFontColor(0xffFFFFFF)

	def Show(self):
		ui.ScriptWindow.Show(self)
		self.SetCenterPosition()
		self.SetTop()

	def SetItemToolTip(self, tooltip):
		self.tooltipItem = tooltip	

	def Destroy(self):
		if self.ItemList:
			self.ItemList.Clear()
			self.ItemList = None
			
		if self.CategoryList:
			self.CategoryList.Clear()
			self.CategoryList = None
			
		self.ClearDictionary()
		self.tooltipItem = None
		self.Board = None
	
	def ClearThings(self):
		pass

	def Close(self):
		self.ClearThings()
		self.Hide()
		
	def OnPressEscapeKey(self):
		self.Close()
		return True
