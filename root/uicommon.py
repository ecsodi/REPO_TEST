import thenewui as ui
import localeInfo
import app
import ime
import uiScriptLocale
import chat
import uiToolTip
import constInfo
import item
import skill
import nonplayer
import CacheEffect as player
import uiPrivateShopBuilder
import wndMgr
import background
import net

import grp
import uicompanion

SELECT_COLOR = grp.GenerateColor(0.0, 0.0, 0.5, 0.6)
HALF_WHITE_COLOR = grp.GenerateColor(1.0, 1.0, 1.0, 0.2)
BACKGROUND_COLOR = grp.GenerateColor(0.0, 0.0, 0.0, 1.0)

TOP_BLUE = 0
TOP_RED = 1
TOP_YELLOW = 2

PLAYER_TOP_DICT = {}

PLAYER_TOP_DICT[TOP_BLUE] = {}
PLAYER_TOP_DICT[TOP_BLUE][0] = {"Name": "Player1", "Function": "Something"}
PLAYER_TOP_DICT[TOP_BLUE][1] = {"Name": "Player2", "Function": "Something very new"}
PLAYER_TOP_DICT[TOP_BLUE][2] = {"Name": "Player3", "Function": "Something"}
PLAYER_TOP_DICT[TOP_BLUE][3] = {"Name": "Player4", "Function": "Something"}
PLAYER_TOP_DICT[TOP_BLUE][4] = {"Name": "Player5", "Function": "Something special"}
PLAYER_TOP_DICT[TOP_BLUE][5] = {"Name": "Player6", "Function": "Yo soy la bomba!"}
PLAYER_TOP_DICT[TOP_BLUE][6] = {"Name": "Player6", "Function": "Yo soy la bomba!"}
PLAYER_TOP_DICT[TOP_BLUE][7] = {"Name": "Player6", "Function": "Yo soy la bomba!"}
PLAYER_TOP_DICT[TOP_BLUE][8] = {"Name": "Player6", "Function": "Yo soy la bomba!"}
PLAYER_TOP_DICT[TOP_BLUE][9] = {"Name": "Player6", "Function": "Yo soy la bomba!"}
PLAYER_TOP_DICT[TOP_BLUE][10] = {"Name": "Player6", "Function": "Yo soy la bomba!"}

PLAYER_TOP_DICT[TOP_RED] = {}
PLAYER_TOP_DICT[TOP_RED][0] = {"Name": "Player1", "Function": "Something"}
PLAYER_TOP_DICT[TOP_RED][1] = {"Name": "Player2", "Function": "Something"}
PLAYER_TOP_DICT[TOP_RED][2] = {"Name": "Player3", "Function": "Something"}
PLAYER_TOP_DICT[TOP_RED][3] = {"Name": "Player4", "Function": "Something"}
PLAYER_TOP_DICT[TOP_RED][4] = {"Name": "Player5", "Function": "Something"}
PLAYER_TOP_DICT[TOP_RED][5] = {"Name": "Player6", "Function": "Something"}

PLAYER_TOP_DICT[TOP_YELLOW] = {}
PLAYER_TOP_DICT[TOP_YELLOW][0] = {"Name": "PLASD", "Function": "Something"}
PLAYER_TOP_DICT[TOP_YELLOW][1] = {"Name": "SDFGSD", "Function": "Something"}
PLAYER_TOP_DICT[TOP_YELLOW][2] = {"Name": "ASDA", "Function": "Something"}
PLAYER_TOP_DICT[TOP_YELLOW][3] = {"Name": "QWE", "Function": "Something"}
PLAYER_TOP_DICT[TOP_YELLOW][4] = {"Name": "FDGDG", "Function": "Something"}
PLAYER_TOP_DICT[TOP_YELLOW][5] = {"Name": "sadffdfd", "Function": "Something"}

MONDAY = 0
TUESDAY = 1
WEDNESDAY = 2
THURSDAY = 3
FRIDAY = 4
SATURDAY = 5
SUNDAY = 6

EVENTS_PANEL = {}

EVENTS_PANEL[MONDAY] = {}
EVENTS_PANEL[MONDAY][0] = {"Name": "Search the GM", "Time": "16:00"}
EVENTS_PANEL[MONDAY][1] = {"Name": "Tanaka", "Time": "16:00"}
EVENTS_PANEL[MONDAY][2] = {"Name": "OX", "Time": "16:00"}
EVENTS_PANEL[MONDAY][3] = {"Name": "NIce event", "Time": "16:00"}
EVENTS_PANEL[MONDAY][4] = {"Name": "THE BEST", "Time": "16:00"}
EVENTS_PANEL[MONDAY][5] = {"Name": "THE BEST", "Time": "16:00"}
EVENTS_PANEL[MONDAY][6] = {"Name": "THE BEST", "Time": "16:00"}
EVENTS_PANEL[MONDAY][7] = {"Name": "THE BEST", "Time": "16:00"}
EVENTS_PANEL[MONDAY][8] = {"Name": "THE BEST", "Time": "16:00"}
EVENTS_PANEL[MONDAY][9] = {"Name": "THE B2EST", "Time": "16:00"}


EVENTS_PANEL[TUESDAY] = {}
EVENTS_PANEL[TUESDAY][0] = {"Name": "Search the GM", "Time": "16:00"}
EVENTS_PANEL[TUESDAY][1] = {"Name": "Tanaka", "Time": "16:00"}


EVENTS_PANEL[WEDNESDAY] = {}
EVENTS_PANEL[WEDNESDAY][0] = {"Name": "Event 1", "Time": "16:00"}
EVENTS_PANEL[WEDNESDAY][1] = {"Name": "Event 2", "Time": "16:00"}

EVENTS_PANEL[THURSDAY] = {}
EVENTS_PANEL[THURSDAY][0] = {"Name": "Event 3", "Time": "16:00"}
EVENTS_PANEL[THURSDAY][1] = {"Name": "Event 4", "Time": "16:00"}
EVENTS_PANEL[THURSDAY][2] = {"Name": "Event 5", "Time": "16:00"}

EVENTS_PANEL[FRIDAY] = {}
EVENTS_PANEL[FRIDAY][0] = {"Name": "Event 1", "Time": "16:00"}
EVENTS_PANEL[FRIDAY][1] = {"Name": "Event 2", "Time": "16:00"}


class TopSmthWindow(ui.ScriptWindow):
	def __init__(self):
		ui.ScriptWindow.__init__(self)
		self.__LoadDialog()

	def __del__(self):
		ui.ScriptWindow.__del__(self)

	def __LoadDialog(self):
		self.AddFlag("movable")

		self.Board = ui.BoardWithTitleBar()
		self.Board.SetParent(self)
		self.Board.SetSize(460, 360)
		self.Board.SetTitleName("Ranking Empire")
		self.Board.SetCloseEvent(ui.__mem_func__(self.Close))
		self.Board.Show()
		
		self.SetSize(self.Board.GetWidth(), self.Board.GetHeight())

		self.BoardThin = ui.ThinBoard()
		self.BoardThin.SetParent(self)
		self.BoardThin.SetPosition(7, 32)
		self.BoardThin.SetSize(self.Board.GetWidth() - 15, self.Board.GetHeight() - 40)
		self.BoardThin.Show()

		self.BoardThin2 = ui.ThinBoard()
		self.BoardThin2.SetParent(self)
		self.BoardThin2.SetPosition(18, 40)
		self.BoardThin2.SetSize(160, self.Board.GetHeight() - 55)
		self.BoardThin2.Show()

		self.BoardThin3 = ui.ThinBoard()
		self.BoardThin3.SetParent(self)
		self.BoardThin3.SetPosition(190, 40)
		self.BoardThin3.SetSize(250, 28)
		self.BoardThin3.Show()

		self.Thin3Text1 = ui.TextLine()
		self.Thin3Text1.SetParent(self.BoardThin3)
		self.Thin3Text1.SetText("Name")
		self.Thin3Text1.SetPosition(35, 10)
		self.Thin3Text1.Show()

		self.Thin3Text2 = ui.TextLine()
		self.Thin3Text2.SetParent(self.BoardThin3)
		self.Thin3Text2.SetText("Function")
		self.Thin3Text2.SetPosition(145, 10)
		self.Thin3Text2.Show()

		self.BlueButton = ui.Button()
		self.BlueButton.SetParent(self)
		self.BlueButton.SetUpVisual("d:/ymir work/ranking/rank_category.png")
		self.BlueButton.SetOverVisual("d:/ymir work/ranking/rank_category_selected.png")
		self.BlueButton.SetDownVisual("d:/ymir work/ranking/rank_category.png")
		self.BlueButton.SetPosition(26, 55)
		self.BlueButton.SetEvent(ui.__mem_func__(self.OnRanking), TOP_BLUE)
		self.BlueButton.Show()

		self.BlueIcon = ui.ExpandedImageBox()
		self.BlueIcon.SetParent(self.BlueButton)
		self.BlueIcon.AddFlag("not_pick")
		self.BlueIcon.SetPosition(15, 8)
		self.BlueIcon.LoadImage("d:/ymir work/ranking/category/1.png")
		self.BlueIcon.Show()

		self.BlueText = ui.TextLine()
		self.BlueText.SetParent(self.BlueButton)
		self.BlueText.SetText("Blue Kingdom")
		self.BlueText.SetPosition(45, 14)
		self.BlueText.Show()

		self.RedButton = ui.Button()
		self.RedButton.SetParent(self)
		self.RedButton.SetUpVisual("d:/ymir work/ranking/rank_category.png")
		self.RedButton.SetOverVisual("d:/ymir work/ranking/rank_category_selected.png")
		self.RedButton.SetDownVisual("d:/ymir work/ranking/rank_category.png")
		self.RedButton.SetPosition(26, 105)
		self.RedButton.SetEvent(ui.__mem_func__(self.OnRanking), TOP_RED)
		self.RedButton.Show()

		self.RedIcon = ui.ExpandedImageBox()
		self.RedIcon.SetParent(self.RedButton)
		self.RedIcon.AddFlag("not_pick")
		self.RedIcon.SetPosition(15, 8)
		self.RedIcon.LoadImage("d:/ymir work/ranking/category/1.png")
		self.RedIcon.Show()

		self.RedText = ui.TextLine()
		self.RedText.SetParent(self.RedButton)
		self.RedText.SetText("Red Kingdom")
		self.RedText.SetPosition(45, 14)
		self.RedText.Show()

		self.YellowButton = ui.Button()
		self.YellowButton.SetParent(self)
		self.YellowButton.SetUpVisual("d:/ymir work/ranking/rank_category.png")
		self.YellowButton.SetOverVisual("d:/ymir work/ranking/rank_category_selected.png")
		self.YellowButton.SetDownVisual("d:/ymir work/ranking/rank_category.png")
		self.YellowButton.SetPosition(26, 155)
		self.YellowButton.SetEvent(ui.__mem_func__(self.OnRanking), TOP_YELLOW)
		self.YellowButton.Show()

		self.YellowIcon = ui.ExpandedImageBox()
		self.YellowIcon.SetParent(self.YellowButton)
		self.YellowIcon.AddFlag("not_pick")
		self.YellowIcon.SetPosition(15, 8)
		self.YellowIcon.LoadImage("d:/ymir work/ranking/category/1.png")
		self.YellowIcon.Show()

		self.YellowText = ui.TextLine()
		self.YellowText.SetParent(self.YellowButton)
		self.YellowText.SetText("Yellow Kingdom")
		self.YellowText.SetPosition(45, 14)
		self.YellowText.Show()
		
		self.Refresh(TOP_BLUE)
	
	def OnRanking(self, page):
		self.Refresh(page)
	
	def Refresh(self, page):
		self.bInfoPos = {}
		self.bInfoName = {}
		self.bInfoValue = {}
		self.bInfoBoard = {}

		y_pos = [94, 120, 145, 171, 197, 223, 248, 275, 300, 328] # Position
		colors = ["|cffffff00", "|cff888888", "|cFFA52A2A" ]

		for x in xrange(10):
			if x > len(y_pos):
				break
			
			if not PLAYER_TOP_DICT[page].has_key(x):
				break

			self.bInfoBoard[x] = ui.ThinBoardCircle()
			self.bInfoBoard[x].SetParent(self)
			self.bInfoBoard[x].SetPosition(200, y_pos[x] - 15)
			self.bInfoBoard[x].SetSize(230, 25)
			self.bInfoBoard[x].Show()

			self.bInfoPos[x] = ui.TextLine()
			self.bInfoPos[x].SetParent(self.bInfoBoard[x])
			self.bInfoPos[x].SetPosition(5, 6)
			self.bInfoPos[x].SetText(str(x + 1) + ".")
			self.bInfoPos[x].Show()
			
			self.bInfoName[x] = ui.TextLine()
			self.bInfoName[x].SetParent(self.bInfoBoard[x])
			self.bInfoName[x].SetPosition(-79, 6)
			self.bInfoName[x].SetWindowHorizontalAlignCenter()	
			self.bInfoName[x].SetHorizontalAlignCenter()
			
			if x < 3:
				self.bInfoName[x].SetText(colors[x] + PLAYER_TOP_DICT[page][x]["Name"])
			else:
				self.bInfoName[x].SetText(PLAYER_TOP_DICT[page][x]["Name"])
			
			self.bInfoName[x].Show()

			self.bInfoValue[x] = ui.TextLine()
			self.bInfoValue[x].SetParent(self.bInfoBoard[x])
			self.bInfoValue[x].SetPosition(40, 6)
			self.bInfoValue[x].SetWindowHorizontalAlignCenter()	
			self.bInfoValue[x].SetHorizontalAlignCenter()
			func = PLAYER_TOP_DICT[page][x]["Function"]
			if x < 3:
				self.bInfoValue[x].SetText(colors[x] + str(func))
			else:
				self.bInfoValue[x].SetText(str(func))
			self.bInfoValue[x].Show()

	def Show(self):
		self.SetCenterPosition()
		self.SetTop()
		ui.ScriptWindow.Show(self)

	def Close(self):
		self.Hide()

		self.bInfoPos = {}
		self.bInfoName = {}
		self.bInfoValue = {}
		self.bInfoBoard = {}

	def Destroy(self):
		self.Close()
		self.ClearDictionary()

	def OnPressEscapeKey(self):
		self.Close()
		return True

class DailyEventWindow(ui.ScriptWindow):
	def __init__(self):
		ui.ScriptWindow.__init__(self)
		self.__LoadDialog()

	def __del__(self):
		ui.ScriptWindow.__del__(self)

	def __LoadDialog(self):
		self.AddFlag("movable")
		self.AddFlag("animation")

		self.Board = ui.BoardWithTitleBar()
		self.Board.SetParent(self)
		self.Board.SetSize(460, 360)
		self.Board.SetTitleName("Daily Event")
		self.Board.SetCloseEvent(ui.__mem_func__(self.Close))
		self.Board.Show()
		
		self.SetSize(self.Board.GetWidth(), self.Board.GetHeight())

		self.BoardThin = ui.ThinBoard()
		self.BoardThin.SetParent(self)
		self.BoardThin.SetPosition(7, 32)
		self.BoardThin.SetSize(self.Board.GetWidth() - 15, self.Board.GetHeight() - 40)
		self.BoardThin.Show()

		self.BoardThin2 = ui.ThinBoard()
		self.BoardThin2.SetParent(self)
		self.BoardThin2.SetPosition(18, 40)
		self.BoardThin2.SetSize(160, self.Board.GetHeight() - 55)
		self.BoardThin2.Show()

		self.BoardThin3 = ui.ThinBoard()
		self.BoardThin3.SetParent(self)
		self.BoardThin3.SetPosition(190, 40)
		self.BoardThin3.SetSize(250, 28)
		self.BoardThin3.Show()

		self.Thin3Text1 = ui.TextLine()
		self.Thin3Text1.SetParent(self.BoardThin3)
		self.Thin3Text1.SetText("Event")
		self.Thin3Text1.SetPosition(35, 10)
		self.Thin3Text1.Show()

		self.Thin3Text2 = ui.TextLine()
		self.Thin3Text2.SetParent(self.BoardThin3)
		self.Thin3Text2.SetText("Time")
		self.Thin3Text2.SetPosition(175, 10)
		self.Thin3Text2.Show()
		
		self.dictDayButton = {}
		self.dictDayImage = {}
		self.dictDayText = {}
		
		days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
		for x in xrange(len(days)):
			self.CreateDayButton(x, days[x])
		
		self.Refresh(MONDAY)
	
	def CreateDayButton(self, day, name):
		self.dictDayButton[day] = ui.Button()
		self.dictDayButton[day].SetParent(self)
		self.dictDayButton[day].SetUpVisual("d:/ymir work/ranking/rank_category.png")
		self.dictDayButton[day].SetOverVisual("d:/ymir work/ranking/rank_category_selected.png")
		self.dictDayButton[day].SetDownVisual("d:/ymir work/ranking/rank_category.png")
		self.dictDayButton[day].SetPosition(26, 48 + (day *41))
		self.dictDayButton[day].SetEvent(ui.__mem_func__(self.OnRanking), day)
		self.dictDayButton[day].Show()

		self.dictDayImage[day] = ui.ExpandedImageBox()
		self.dictDayImage[day].SetParent(self.dictDayButton[day])
		self.dictDayImage[day].AddFlag("not_pick")
		self.dictDayImage[day].SetPosition(15, 8)
		self.dictDayImage[day].LoadImage("d:/ymir work/ranking/category/1.png")
		self.dictDayImage[day].Show()

		self.dictDayText[day] = ui.TextLine()
		self.dictDayText[day].SetParent(self.dictDayButton[day])
		self.dictDayText[day].SetText(str(name))
		self.dictDayText[day].SetPosition(45, 14)
		self.dictDayText[day].Show()		
	
	def OnRanking(self, page):
		self.Refresh(page)
	
	def Refresh(self, page):
		self.bInfoName = {}
		self.bInfoValue = {}
		self.bInfoBoard = {}

		y_pos = [94, 120, 145, 171, 197, 223, 248, 275, 300, 328] # Position

		for x in xrange(10):
			if x > len(y_pos):
				break

			if not EVENTS_PANEL[page].has_key(x):
				break

			self.bInfoBoard[x] = ui.ThinBoardCircle()
			self.bInfoBoard[x].SetParent(self)
			self.bInfoBoard[x].SetPosition(200, y_pos[x] - 15)
			self.bInfoBoard[x].SetSize(230, 25)
			self.bInfoBoard[x].Show()

			self.bInfoName[x] = ui.TextLine()
			self.bInfoName[x].SetParent(self.bInfoBoard[x])
			self.bInfoName[x].SetPosition(-78, 6)
			self.bInfoName[x].SetWindowHorizontalAlignCenter()	
			self.bInfoName[x].SetHorizontalAlignCenter()
			self.bInfoName[x].SetText(EVENTS_PANEL[page][x]["Name"])
			self.bInfoName[x].Show()

			self.bInfoValue[x] = ui.TextLine()
			self.bInfoValue[x].SetParent(self.bInfoBoard[x])
			self.bInfoValue[x].SetPosition(60, 6)
			self.bInfoValue[x].SetWindowHorizontalAlignCenter()	
			self.bInfoValue[x].SetHorizontalAlignCenter()
			self.bInfoValue[x].SetText(str(EVENTS_PANEL[page][x]["Time"]))
			self.bInfoValue[x].Show()

	def Show(self):
		self.SetCenterPosition()
		self.SetTop()
		ui.ScriptWindow.Show(self)

	def Close(self):
		self.Hide()

		self.dictDayButton = {}
		self.dictDayImage = {}
		self.dictDayText = {}
		
		self.bInfoName = {}
		self.bInfoValue = {}
		self.bInfoBoard = {}
		
	def Destroy(self):
		self.Close()
		self.ClearDictionary()

		self.dictDayButton = {}
		self.dictDayImage = {}
		self.dictDayText = {}
		
		self.bInfoName = {}
		self.bInfoValue = {}
		self.bInfoBoard = {}

	def OnPressEscapeKey(self):
		self.Close()
		return True

class DropInfoWindow(ui.ScriptWindow):
	def __init__(self):
		self.bExpanded = True
		self.yNotExpanedPos = 0
		self.yExpanedPos = 0

		self.dictItems = []
		self.dictIcons = []

		ui.ScriptWindow.__init__(self)
		self.__LoadDialog()

	def __del__(self):
		self.dictItems = []
		self.dictIcons = []
	
		ui.ScriptWindow.__del__(self)

	def __LoadDialog(self):
		self.AddFlag("not_pick")

		self.Board = ui.ThinBoard()
		self.Board.SetParent(self)
		self.Board.SetSize(177, 187)
		self.Board.Show()
		
		self.Board.AddFlag("attach")		
		self.SetSize(self.Board.GetWidth(), self.Board.GetHeight())

	def OnMouseLeftButtonUp(self):
		if self.bExpanded:
			self.bExpanded = False
		else:
			self.bExpanded = True

	def OnRender(self):
		self.SetPosAnim()
	
	def GetItemsSize(self):
		return len(self.dictItems)
	
	def Show(self):
		self.yNotExpanedPos = (wndMgr.GetScreenHeight() - self.GetHeight() / 2) + 25
		self.yExpanedPos = (wndMgr.GetScreenHeight() - self.GetHeight() / 2) - 55
		
		self.SetPosition((wndMgr.GetScreenWidth() - self.GetWidth()) / 7, self.yNotExpanedPos)
		
		ui.ScriptWindow.Show(self)

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

	def AppendItem(self, ItemVnum, ItemCount):
		if ItemVnum <= 0:
			return
		
		if len(self.dictItems) > 6:
			del self.dictItems[0]
		
		item.SelectItem(ItemVnum)
		_, size = item.GetItemSize()
		
		if ItemVnum == 1:
			ItemCount = self.ConvertYangAsKKK(ItemCount)
		
		y = len(self.dictItems)
		
		if ItemVnum == 1:
			Text = "+ |cFF0bd022|H|h" + str(ItemCount) + " |cFFFFFF00|H|h" + item.GetItemName()
		else:
			Text = "+ |cFFc1577c|H|h" + str(ItemCount) + "x |cFF57c189|H|h" + item.GetItemName()

		textLine = ui.TextLine()
		textLine.SetParent(self)
		textLine.SetWindowHorizontalAlignCenter()
		textLine.SetHorizontalAlignCenter()
		textLine.SetText(Text)
		textLine.Show()

		ImageBox = ui.ExpandedImageBox()
		ImageBox.SetParent(textLine)
		ImageBox.LoadImage(item.GetIconImageFileName())
		
		if size == 1:
			ImageBox.SetScale(0.5, 0.5)
		elif size == 2:
			ImageBox.SetScale(0.35, 0.3)
		elif size == 3:
			ImageBox.SetScale(0.35, 0.15)
		
		ImageBox.SetPosition((textLine.GetTextWidth() / 2) + 2, -1)
		ImageBox.Show()
	
		self.dictItems.append(textLine)
		self.dictIcons.append(ImageBox)
		
		self.ArrangeItems()
	
	def ArrangeItems(self):
		for index, item in enumerate(self.dictItems):
			item.SetPosition(0, 7 + index*14)
	
	def SetPosAnim(self):
		xMine, yMine = self.GetGlobalPosition()

		if self.bExpanded:
			yMine += 2
			
			if yMine > self.yNotExpanedPos:
				yMine = self.yNotExpanedPos
		else:
			yMine -= 2
			
			if yMine < self.yExpanedPos:
				yMine = self.yExpanedPos

		self.SetPosition((wndMgr.GetScreenWidth() - self.GetWidth()) / 7, yMine)
	
	def Close(self):
		self.Hide()

	def Destroy(self):
		self.dictItems = []
		self.dictIcons = []
	
		self.Close()
		self.ClearDictionary()

class TimerDungeonMessage(ui.ScriptWindow):
	def __init__(self):
		self.TimeLeft = None
	
		ui.ScriptWindow.__init__(self)
		self.ShowScale = False
		self.TextToolTip = None
		
		self.xA = 0
		self.yA = 0
		self.iTimeStop = 0
		self.iTimeStopGlobal = 0
		
		self.grpColor = grp.GenerateColor(100.0, 255.0, 255.0, 0.7)
		self.__LoadDialog()
		
		# self.SetNotify("Obiectiv: Omoara-l pe Razador!", 25)

	def __del__(self):
		ui.ScriptWindow.__del__(self)
		
		self.TimeLeft = None
		self.TextToolTip = None

	def OnRender(self):
		x, y = self.GetGlobalPosition()
		grp.SetColor(self.grpColor)
		
		width = self.GetWidth()
		height = self.GetHeight()

		grp.RenderBar(x - self.xA, y - self.yA, width, height)
		
		if self.iTimeStopGlobal <= app.GetGlobalTimeStamp():
			self.TimeLeft.Hide()
		else:
			TimeLeft = self.iTimeStopGlobal - app.GetGlobalTimeStamp()
			if TimeLeft < 10 and not TimeLeft > 10:
				self.SetColorGauge("red")
			elif TimeLeft > 10 and not TimeLeft > 20:
				self.SetColorGauge("blue")
		
			self.TimeLeft.SetPercentage(TimeLeft, self.iTimeStop)
			self.TimeLeft.Show()

	def __CreateGameTypeToolTip(self, title, descList):
		toolTip = uiToolTip.ToolTip()
		toolTip.SetTitle(title)
		toolTip.AppendSpace(5)

		toolTip.AutoAppendTextLine(descList)

		toolTip.AlignHorizonalCenter()
		return toolTip
	
	def SetColorGauge(self, color):
		if self.TimeLeft:
			if self.TimeLeft.CurrentColor != color:
				self.TimeLeft.imgGauge.LoadImage("d:/ymir work/ui/pattern/gauge_" + color + ".tga")
				self.TimeLeft.CurrentColor = color
	
	def __LoadDialog(self):
		self.AddFlag("attach")

		self.Text = ui.MakeText(self, False, 2, 0)
		self.Text.SetFontName("Arial:20")
		self.Text.SetPackedFontColor(0xffdddddd)
		self.Text.SetText(localeInfo.CANNOT_SKILL_REMOVE_FISHING_ROD)

		self.TimeLeft = ui.Gauge()
		self.TimeLeft.MakeGauge(108, "green")
		self.TimeLeft.CurrentColor = "green"
		self.TimeLeft.SetSize(108, 30)
		self.TimeLeft.SetPercentage(0, 100)
		self.TimeLeft.Hide()

		self.Board = ui.Window()
		self.Board.SetParent(self)
		self.Board.SetSize(self.Text.GetTextWidth() + 5, 25)
		self.Board.Show()
	
		self.SetSize(self.Board.GetWidth(), self.Board.GetHeight())
	
	def SetNotify(self, text, time_stop, bFromUpdate = False):
		self.TimeLeft.OnMouseOverIn = ui.__mem_func__(self.GaugeOnMouseOverIn)
		self.TimeLeft.OnMouseOverOut = ui.__mem_func__(self.GaugeOnMouseOverOut)

		self.Text.SetPackedFontColor(0xffdddddd)
		self.Text.SetText(text)
		if not bFromUpdate:
			self.iTimeStop = time_stop
			self.iTimeStopGlobal = time_stop + app.GetGlobalTimeStamp()

		self.Board.SetSize(self.Text.GetTextWidth() + 5, 25)
		self.SetSize(self.Board.GetWidth(), self.Board.GetHeight())

		if self.TextToolTip:
			self.TextToolTip.Hide()
			self.TextToolTip = None

		self.TextToolTip = self.__CreateGameTypeToolTip("Timp ramas pana la iesire din temnita", "30 secunde")

	def GaugeOnMouseOverIn(self):
		if self.TextToolTip:
			TimeLeft = self.iTimeStopGlobal - app.GetGlobalTimeStamp()
			if TimeLeft > 0:
				self.GaugeOnMouseOverOut()
				self.TextToolTip = None
				self.TextToolTip = self.__CreateGameTypeToolTip("Timp ramas pana la iesire din temnita", localeInfo.SecondToDHM(TimeLeft))

			self.TextToolTip.Show()
			
	def GaugeOnMouseOverOut(self):
		if self.TextToolTip:
			self.TextToolTip.Hide()	
	
	def Show(self):
		self.SetPosition((wndMgr.GetScreenWidth() / 2) - (self.Text.GetTextWidth() / 2) + 400, 100)
		self.TimeLeft.SetPosition((wndMgr.GetScreenWidth() / 2) + 560, 176)
		self.TimeLeft.Show()

		self.ShowScale = True
		self.xA = 0
		self.yA = 0
		ui.ScriptWindow.Show(self)
	
	def Hide(self):
		if self.TimeLeft:
			self.TimeLeft.Hide()
		
		ui.ScriptWindow.Hide(self)
	
	def Close(self):
		self.xA = 0
		self.yA = 0
		self.Hide()

	def Destroy(self):
		self.Close()
		self.ClearDictionary()
		
		if self.TimeLeft:
			self.TimeLeft.Hide()
		
		self.TimeLeft = None
		self.TextToolTip = None

class CaptchaWindow(ui.ScriptWindow):
	def __init__(self):
		ui.ScriptWindow.__init__(self)
		self.cancelEvent = lambda *arg: None
		self.CodeMatch = 0
		self.__LoadDialog()

	def __del__(self):
		ui.ScriptWindow.__del__(self)

	def __LoadDialog(self):
		self.AddFlag("movable")

		self.Board = ui.BoardWithTitleBar()
		self.Board.SetParent(self)
		self.Board.SetSize(336, 187)
		self.Board.SetTitleName("Bot Verification")
		self.Board.SetCloseEvent(ui.__mem_func__(self.Close))
		self.Board.Show()
		
		self.SetSize(self.Board.GetWidth(), self.Board.GetHeight())

		self.ThinBoard = ui.MakeThinBoardCircle(self.Board, 7, 30, 320, 150, False)
		self.HorizontalBar = ui.MakeHorizontalBar(self.Board, 10, 35, 315, "Introdu numarul in caseta de mai jos!")

		self.accceptButton = ui.MakeButton(self, 123, 144, False, "d:/ymir work/ui/shop/decoration/", "btn_normal.tga", "btn_hover.tga", "btn_down.tga")
		self.accceptButton.SetText("Introdu")
		self.accceptButton.SetEvent(ui.__mem_func__(self.AcceptFunc))
	
		self.ThinBoardNameLine = ui.MakeThinBoardCircle(self.Board, 100, 115, 130, 20, False)
	
		self.NameLine = ui.EditLine()
		self.NameLine.SetParent(self.ThinBoardNameLine)
		self.NameLine.SetPosition(3, 4)
		self.NameLine.SetSize(330, 18)
		self.NameLine.SetMax(16)
		self.NameLine.SetNumberMode()
		self.NameLine.Show()

		self.wndTextCode = ui.MakeText(self.ThinBoard, False, 0, -25)
		self.wndTextCode.SetFontName("Courier:32")
		self.wndTextCode.SetText("0")

		self.wndTextCode.SetWindowHorizontalAlignCenter()
		self.wndTextCode.SetWindowVerticalAlignCenter()
		self.wndTextCode.SetHorizontalAlignCenter()
		self.wndTextCode.SetVerticalAlignCenter()

	def SetCodeMatch(self, code):
		self.CodeMatch = code
		self.wndTextCode.SetText(str(code))
	
	def Show(self):
		self.SetCenterPosition()
		self.SetTop()
		self.SetCodeMatch(app.GetRandom(1000, 99999))
		ui.ScriptWindow.Show(self)

	def Close(self):
		self.Hide()
		self.cancelEvent()

	def SetCancelEvent(self, event):
		self.cancelEvent = event

	def Destroy(self):
		self.Close()
		self.ClearDictionary()
	
	def AcceptFunc(self):
		if len(self.NameLine.GetText()) < 1:
			return
		
		Code = int(self.NameLine.GetText())
		
		if Code != self.CodeMatch:
			chat.AppendChat(1, "Codul introdus este gresit!")
			return
		
		# net.SendChatPacket("/bot_verification %d" % (Code))
		self.Close()

	def OnPressEscapeKey(self):
		self.Close()
		return True

	def OnIMEReturn(self):
		self.Close()
		return True

class MultipleAddWindow(ui.ScriptWindow):
	def __init__(self):
		ui.ScriptWindow.__init__(self)
		self.SliderPos = 1
		self.statusCommand = ""
		self.__LoadDialog()

	def __del__(self):
		ui.ScriptWindow.__del__(self)

	def __LoadDialog(self):
		self.AddFlag("movable")
	
		self.Board = ui.BoardWithTitleBar()
		self.Board.SetParent(self)
		self.Board.SetSize(210, 125)
		self.Board.AddFlag("not_pick")
		self.Board.SetTitleName("Fast Status")
		self.Board.SetCloseEvent(ui.__mem_func__(self.Close))
		self.Board.Show()

		self.SetSize(self.Board.GetWidth(), self.Board.GetHeight())
	
		self.ThinSell = ui.MakeThinBoardCircle(self.Board, 60, 40, 100, 19, False)
		self.wndMessage1 = ui.MakeText(self.ThinSell, "Suma: 1", 3, 2)

		self.wndSlider = ui.SliderBar()
		self.wndSlider.SetParent(self)
		self.wndSlider.SetPosition(15, 67)
		self.wndSlider.SetEvent(ui.__mem_func__(self.OnSliderMove))
		self.wndSlider.Show()

		self.btnAccept = ui.Button()
		self.btnAccept.SetParent(self)
		self.btnAccept.SetUpVisual("d:/ymir work/ui/public/xlarge_button_01.sub")
		self.btnAccept.SetOverVisual("d:/ymir work/ui/public/xlarge_button_02.sub")
		self.btnAccept.SetDownVisual("d:/ymir work/ui/public/xlarge_button_03.sub")
		self.btnAccept.SetPosition(14, 90)
		self.btnAccept.SetText("Adauga")
		self.btnAccept.SetEvent(ui.__mem_func__(self.OnMultipleAdd))
		self.btnAccept.Show()

	def OnSliderMove(self):
		self.SliderPos = int(self.wndSlider.GetSliderPos() * 100)
		if self.SliderPos == 0:
			self.SliderPos = 1

		self.wndMessage1.SetText("Suma: " + str(self.SliderPos))

	def Show(self):
		self.SetCenterPosition()
		self.SetTop()
		ui.ScriptWindow.Show(self)
	
	def OnMultipleAdd(self):
		net.SendChatPacket(self.statusCommand + " " + str(self.SliderPos))
		self.Close()
	
	def Open(self, command):
		self.SetTop()
		self.wndSlider.SetSliderPos(0.0)
		self.OnSliderMove()
		self.statusCommand = command
		self.Show()

	def Close(self):
		self.Hide()

	def Destroy(self):
		self.Close()
		self.ClearDictionary()
	
	def OnPressEscapeKey(self):
		self.Close()
		return True

	def OnIMEReturn(self):
		self.Close()
		return True


class MessageGame(ui.ScriptWindow):
	def __init__(self):
		ui.ScriptWindow.__init__(self)
		self.ShowScale = False
		self.xA = 0
		self.yA = 0
		self.fTimeStart = 0
		self.__LoadDialog()

	def __del__(self):
		ui.ScriptWindow.__del__(self)

	def OnRender(self):
		x, y = self.GetGlobalPosition()
		grp.SetColor(grp.GenerateColor(66.0, 255.0, 255.0, 0.7))
		
		width = self.GetWidth()
		height = self.GetHeight()
		
		if self.ShowScale == True:
			self.xA += 0.7
			self.yA += 0.7
		
			width += self.xA
			height += self.yA

			if width > self.GetWidth() + 5 and height > self.GetHeight() + 5:
				self.ShowScale = False

		elif self.xA > 0:
			self.xA -= 1
			self.yA -= 1
		
			width -= self.xA
			height -= self.yA			
		
		if self.ShowScale == True:
			grp.RenderBar(x + self.xA, y + self.yA, width, height)
		else:
			grp.RenderBar(x - self.xA, y - self.yA, width, height)
		
		if float(app.GetTime()) > self.fTimeStart or self.fTimeStart == 0:
			self.Close()

	def __LoadDialog(self):
		self.AddFlag("attach")

		self.Text = ui.MakeText(self, False, 2, 0)
		self.Text.SetFontName("Tahoma:16")
		self.Text.SetPackedFontColor(0xffdddddd)
		self.Text.SetText(localeInfo.CANNOT_SKILL_REMOVE_FISHING_ROD)
	
		self.Board = ui.Window()
		self.Board.SetParent(self)
		self.Board.SetSize(self.Text.GetTextWidth() + 5, 25)
		self.Board.Show()
	
		self.SetSize(self.Board.GetWidth(), self.Board.GetHeight())
	
	def SetNotify(self, text):
		self.Text.SetPackedFontColor(0xffdddddd)
		self.Text.SetText(text)

		self.Board.SetSize(self.Text.GetTextWidth() + 5, 25)
		self.SetSize(self.Board.GetWidth(), self.Board.GetHeight())
	
	def Show(self):
		self.SetPosition((wndMgr.GetScreenWidth() / 2) - (self.Text.GetTextWidth() / 2), (wndMgr.GetScreenHeight() / 2) + 100)
		self.ShowScale = True
		self.xA = 0
		self.yA = 0
		self.fTimeStart = app.GetTime() + 2
		ui.ScriptWindow.Show(self)

	def Close(self):
		self.xA = 0
		self.yA = 0
		self.Hide()

	def Destroy(self):
		self.Close()
		self.ClearDictionary()

class CompanionInfo(ui.ScriptWindow):
	class TextToolTip(ui.Window):
		def __init__(self, y):
			ui.Window.__init__(self, "TOP_MOST")

			textLine = ui.TextLine()
			textLine.SetParent(self)
			textLine.SetHorizontalAlignLeft()
			textLine.SetOutline()
			textLine.Show()
			self.y = y
			self.textLine = textLine

		def __del__(self):
			ui.Window.__del__(self)

		def SetText(self, text):
			self.textLine.SetText(text)

		def OnRender(self):
			(mouseX, mouseY) = wndMgr.GetMousePosition()
			self.textLine.SetPosition(mouseX, mouseY - 60 + self.y)

	def __init__(self):
		ui.ScriptWindow.__init__(self)
		self.SlotPosCompanion = 0
		self.NextExp = 1
		self.ToolTipExp = None
		self.ToolTipExp2 = None
		
		self.__LoadDialog()
	
	def SetNextExp(self, exp):
		self.NextExp = exp
	
	def __del__(self):
		ui.ScriptWindow.__del__(self)

		if self.ToolTipExp:
			self.ToolTipExp.Hide()
			self.ToolTipExp = None

		if self.ToolTipExp2:
			self.ToolTipExp2.Hide()
			self.ToolTipExp2 = None
		
	def SetExp(self, percentage):		
		pass

	def SetVnum(self, vnum):
		self.itemSlotPet.SetItemSlot(0, vnum, 0)
	
	def __LoadDialog(self):
		self.AddFlag("movable")

		self.Board = ui.ExpandedImageBox()
		self.Board.SetParent(self)
		self.Board.LoadImage("pet/pet_board.png")
		self.Board.AddFlag("not_pick")
		self.Board.Show()

		# self.IconSlot = ui.ExpandedImageBox()
		# self.IconSlot.SetParent(self)
		# self.IconSlot.LoadImage("d:/ymir work/ui/pet/mini_window/pet_slot_corver.sub")
		# self.IconSlot.SetPosition(3, 3)
		# self.IconSlot.Show()

		self.itemSlotPet = ui.GridSlotWindow()
		self.itemSlotPet.SetParent(self.Board)
		self.itemSlotPet.SetPosition(3, 6)
		self.itemSlotPet.ArrangeSlot(0, 1, 1, 32, 32, 0, 0)
		self.itemSlotPet.Show()

		self.wndExpBoard = ui.Window()
		self.wndExpBoard.SetParent(self.Board)
		self.wndExpBoard.SetSize(16 * 5 + 2 * 4, 16)
		self.wndExpBoard.SetPosition(40, 3)
		self.wndExpBoard.OnMouseOverIn = ui.__mem_func__(self.__OverInExp)
		self.wndExpBoard.OnMouseOverOut = ui.__mem_func__(self.__OverOutExp)
		self.wndExpBoard.Show()

		self.dictExpGauge = {}
		
		for x in xrange(4):
			xPos = [3, 16 + 3, 16 * 2 + 1.7 * 2, 16 * 3 + 1.7 * 2]
			self.dictExpGauge[x] = ui.ExpandedImageBox()
			self.dictExpGauge[x].SetParent(self.wndExpBoard)
			self.dictExpGauge[x].LoadImage("d:/ymir work/ui/pet/exp_gauge/exp_on.sub")
			self.dictExpGauge[x].SetPosition(xPos[x], 0)
			self.dictExpGauge[x].OnMouseOverIn = ui.__mem_func__(self.__OverInExp)
			self.dictExpGauge[x].OnMouseOverOut = ui.__mem_func__(self.__OverOutExp)
			self.dictExpGauge[x].Show()

		# self.wndLifeGauge = ui.AniImageBox()
		# self.wndLifeGauge.SetParent(self)
		# self.wndLifeGauge.SetDelay(6)
		# for x in xrange(1, 8):
			# self.wndLifeGauge.AppendImageScale("D:/Ymir Work/UI/Pattern/HPGauge/0%d.tga" % (x), 0.736, 0.636)
		
		# self.wndLifeGauge.SetPosition(36, 18)
		# self.wndLifeGauge.SetPercentage(100, 100)
		# self.wndLifeGauge.AddFlag("not_pick")
		# self.wndLifeGauge.Show()
		
		self.ToolTipExp = self.TextToolTip(15*1)
		self.ToolTipExp.Hide()

		self.ToolTipExp2 = self.TextToolTip(15*2)
		self.ToolTipExp2.Hide()
		
		self.listGauge = []
		
		bgGauge = ui.ExpandedImageBox()
		bgGauge.SetParent(self.Board)
		bgGauge.LoadImage("pet/pet_gauge.png")
		bgGauge.SetPosition(40, 20)
		bgGauge.AddFlag("not_pick")
		bgGauge.Show()			

		bgGaugeFull = ui.ExpandedImageBox()
		bgGaugeFull.SetParent(bgGauge)
		bgGaugeFull.LoadImage("pet/gauge_full.png")
		bgGaugeFull.SetPosition(0, 0)
		bgGaugeFull.AddFlag("not_pick")
		bgGaugeFull.Show()

		bgGaugeFull.SetWindowName("GaugeBar")
		
		self.listGauge.append(bgGauge)
		self.listGauge.append(bgGaugeFull)
		
		self.dictImageSkill = []
		for x in xrange(2):
			Image = ui.ExpandedImageBox()
			Image.SetParent(self)
			Image.SetPosition(56 + x * 20, 30)
			Image.LoadImage("d:/ymir work/ui/game/normal_interface/offlineshop_locked_hover.png")
			Image.SetScale(0.45, 0.45)
			Image.AddFlag("not_pick")
			Image.Show()
			
			self.dictImageSkill.append(Image)

		self.SetSize(111, 47)

	def __OverInExp(self):
		if self.ToolTipExp:
			self.ToolTipExp.Show()

		if self.ToolTipExp2:
			self.ToolTipExp2.Show()

	def __OverOutExp(self):
		if self.ToolTipExp:
			self.ToolTipExp.Hide()

		if self.ToolTipExp2:
			self.ToolTipExp2.Hide()
			
	def OnUpdate(self):
		if constInfo.COMPANION_ACTIVE_POS == None or constInfo.COMPANION_ACTIVE_POS == -1:
			return
			
		self.SlotPosCompanion = constInfo.COMPANION_ACTIVE_POS
			
		if player.GetItemIndex(self.SlotPosCompanion) == 0:
			return
	
		#UPDATE SKILLS
		attrSlot = [player.GetItemAttribute(player.INVENTORY, self.SlotPosCompanion, i) for i in xrange(player.ATTRIBUTE_SLOT_MAX_NUM)]
		
		if attrSlot != 0:
			index = 0
			for x in xrange(uicompanion.COMPANION_SKILL_1, uicompanion.COMPANION_SKILL_3):
				type = attrSlot[x][0]
				value = attrSlot[x][1]

				if value != 0:
					if uicompanion.TYPE_SKILLS.has_key(type):
						self.dictImageSkill[index].LoadImage(uicompanion.TYPE_SKILLS[type]["ICON"])
						self.dictImageSkill[index].SetScale(0.45, 0.45)				
					else:
						self.dictImageSkill[index].LoadImage("d:/ymir work/ui/game/normal_interface/offlineshop_locked_hover.png")
						self.dictImageSkill[index].SetScale(0.45, 0.45)				
				else:
					self.dictImageSkill[index].LoadImage("d:/ymir work/ui/game/normal_interface/offlineshop_locked_hover.png")
					self.dictImageSkill[index].SetScale(0.45, 0.45)
					
				index += 1
			
		## UPDATE LIFETIME
		Time = player.GetItemMetinSocket(player.INVENTORY, self.SlotPosCompanion, uicompanion.COMPANION_SOCKET_TIME)  - app.GetGlobalTimeStamp()
		if Time > 0:
			hour = int(Time) // 3600
			hour2 = uicompanion.COMPANION_MAX_TIME // 3600
			
			# self.wndLifeGauge.SetPercentage(hour, hour2)
			xList, yList = self.Board.GetGlobalPosition()
			
			for item in self.listGauge:
				if item.GetWindowName() == "GaugeBar":
				# if self.percentTotal == 0:
					# self.percentTotal = 1
					item.SetClipRect(0.0, yList, -1.0 + float(hour) / float(hour2), yList + self.Board.GetHeight(), True)
				# else:
					# item.SetClipRect(xList, yList, xList + self.Board.GetWidth(), yList + self.Board.GetHeight())

		dwExp = player.GetItemMetinSocket(player.INVENTORY, self.SlotPosCompanion, uicompanion.COMPANION_SOCKET_EXP)
		if self.NextExp > 0:
			self.SetExperience(dwExp, self.NextExp)

	def SetExperience(self, curPoint, maxPoint):
		if maxPoint <= 0:
			return

		curPoint = min(curPoint, maxPoint)
		curPoint = max(curPoint, 0)
		maxPoint = max(maxPoint, 0)

		quarterPoint = maxPoint / 4
		FullCount = 0

		if 0 != quarterPoint:
			FullCount = min(4, curPoint / quarterPoint)

		for i in xrange(4):
			self.dictExpGauge[i].Hide()

		for i in xrange(FullCount):
			self.dictExpGauge[i].SetRenderingRect(0.0, 0.0, 0.0, 0.0)
			self.dictExpGauge[i].SetScale(0.9, 0.9)
			self.dictExpGauge[i].Show()

		if 0 != quarterPoint:
			if FullCount < 4:
				Percentage = float(curPoint % quarterPoint) / quarterPoint - 1.0
				self.dictExpGauge[FullCount].SetRenderingRect(0.0, Percentage, 0.0, 0.0)
				self.dictExpGauge[FullCount].SetScale(0.9, 0.9)
				self.dictExpGauge[FullCount].Show()

		self.ToolTipExp.SetText("EXP : %d din %d" % (curPoint, maxPoint))
		self.ToolTipExp2.SetText("EXP : %.2f%%" % (float(curPoint) / maxPoint * 100))

	def Show(self):
		self.SetPosition(15, (wndMgr.GetScreenHeight() / 2) + 190)
		self.SetTop()
		ui.ScriptWindow.Show(self)

	def Close(self):
		self.Hide()

		if self.ToolTipExp:
			self.ToolTipExp.Hide()

		if self.ToolTipExp2:
			self.ToolTipExp2.Hide()
			
	def Destroy(self):
		self.Close()
		self.ClearDictionary()
		self.dictExpGauge = {}
		self.dictImageSkill = []

		if self.ToolTipExp:
			self.ToolTipExp.Hide()
			self.ToolTipExp = None

		if self.ToolTipExp2:
			self.ToolTipExp2.Hide()
			self.ToolTipExp2 = None
			
class CompanionCreate(ui.ScriptWindow):
	def __init__(self, InvPos = 0 ):
		ui.ScriptWindow.__init__(self)
		self.cancelEvent = lambda *arg: None
		self.InvPos = InvPos
		self.__LoadDialog()

	def __del__(self):
		ui.ScriptWindow.__del__(self)

	def __LoadDialog(self):
		self.AddFlag("movable")

		self.Board = ui.BoardWithTitleBar()
		self.Board.SetParent(self)
		self.Board.SetSize(176, 184)
		self.Board.SetTitleName("Incubator")
		self.Board.SetCloseEvent(ui.__mem_func__(self.Close))
		self.Board.Show()
		
		self.SetSize(self.Board.GetWidth(), self.Board.GetHeight())

		self.SlotBackground = ui.ExpandedImageBox()
		self.SlotBackground.SetParent(self)
		self.SlotBackground.LoadImage("d:/ymir work/ui/pet/Pet_Incu_slot_001.tga")
		self.SlotBackground.SetPosition(68, 34)
		self.SlotBackground.Show()

		self.PetNameBackground = ui.ExpandedImageBox()
		self.PetNameBackground.SetParent(self)
		self.PetNameBackground.LoadImage("d:/ymir work/ui/pet/Pet_Incu_001.tga")
		self.PetNameBackground.SetPosition(12, 78)
		self.PetNameBackground.Show()

		self.AdsTextLine = ui.TextLine()
		self.AdsTextLine.SetParent(self.PetNameBackground)
		self.AdsTextLine.SetWindowHorizontalAlignCenter()
		self.AdsTextLine.SetWindowVerticalAlignCenter()
		self.AdsTextLine.SetHorizontalAlignCenter()
		self.AdsTextLine.SetVerticalAlignCenter()
		self.AdsTextLine.SetPosition(0, -10)
		self.AdsTextLine.SetText("Nume Insotitor")
		self.AdsTextLine.SetPackedFontColor(0xFFFEE3AE)
		self.AdsTextLine.Show()

		self.PriceTextLine = ui.TextLine()
		self.PriceTextLine.SetParent(self.Board)
		self.PriceTextLine.SetWindowHorizontalAlignCenter()
		self.PriceTextLine.SetWindowVerticalAlignCenter()
		self.PriceTextLine.SetHorizontalAlignCenter()
		self.PriceTextLine.SetVerticalAlignCenter()
		self.PriceTextLine.SetPosition(0, 48)
		self.PriceTextLine.SetText("Pret: 5.000.000 Yang")
		self.PriceTextLine.SetPackedFontColor(0xFFFEE3AE)
		self.PriceTextLine.Show()

		self.accceptButton = ui.MakeButton(self, 13, 150, False, "d:/ymir work/ui/switchbot/", "btn_big_03.sub", "btn_big_02.sub", "btn_big_03.sub")
		self.accceptButton.SetText("Incubator")
		self.accceptButton.SetEvent(ui.__mem_func__(self.AcceptFunc))
	

		self.NameLine = ui.EditLine()
		self.NameLine.SetParent(self.PetNameBackground)
		self.NameLine.SetPosition(14, 29)
		self.NameLine.SetSize(330, 18)
		self.NameLine.SetMax(16)
		self.NameLine.Show()
		
		ItemVnum = player.GetItemIndex(self.InvPos)
		item.SelectItem(ItemVnum)
		
		self.ImageItemVnum = ui.ExpandedImageBoxAnim()
		self.ImageItemVnum.SetParent(self.SlotBackground)
		self.ImageItemVnum.LoadImage(item.GetIconImageFileName())
		self.ImageItemVnum.SetWindowVerticalAlignCenter()
		self.ImageItemVnum.SetPosition(2, -1)
		self.ImageItemVnum.Show()

	def Show(self):
		self.SetCenterPosition()
		self.SetTop()
		ui.ScriptWindow.Show(self)

	def Close(self):
		self.Hide()
		self.cancelEvent()

	def SetCancelEvent(self, event):
		self.cancelEvent = event

	def Destroy(self):
		self.Close()
		self.ClearDictionary()
	
	def AcceptFunc(self):
		if len(self.NameLine.GetText()) < 3:
			chat.AppendChat(1, "Numele trebuie sa fie mai lung.")
			return
		
		Name = self.NameLine.GetText()
		
		if not Name.isalnum():
			chat.AppendChat(1, "Numele poate contine doar caractere normale sau numere.")
			return
		
		net.SendChatPacket("/create_companion %d %s" % (self.InvPos, Name))
		self.Close()

	def OnPressEscapeKey(self):
		self.Close()
		return True

	def OnIMEReturn(self):
		self.Close()
		return True

class CompanionChangeName(ui.ScriptWindow):
	def __init__(self, InvPos = 0 ):
		ui.ScriptWindow.__init__(self)
		self.cancelEvent = lambda *arg: None
		self.InvPos = InvPos
		self.__LoadDialog()

	def __del__(self):
		ui.ScriptWindow.__del__(self)

	def __LoadDialog(self):
		self.AddFlag("movable")

		self.Board = ui.BoardWithTitleBar()
		self.Board.SetParent(self)
		self.Board.SetSize(176, 184)
		self.Board.SetTitleName("Schimbare Nume")
		self.Board.SetCloseEvent(ui.__mem_func__(self.Close))
		self.Board.Show()
		
		self.SetSize(self.Board.GetWidth(), self.Board.GetHeight())

		self.SlotBackground = ui.ExpandedImageBox()
		self.SlotBackground.SetParent(self)
		self.SlotBackground.LoadImage("d:/ymir work/ui/pet/Pet_Incu_slot_001.tga")
		self.SlotBackground.SetPosition(68, 34)
		self.SlotBackground.Show()

		self.PetNameBackground = ui.ExpandedImageBox()
		self.PetNameBackground.SetParent(self)
		self.PetNameBackground.LoadImage("d:/ymir work/ui/pet/Pet_Incu_001.tga")
		self.PetNameBackground.SetPosition(12, 78)
		self.PetNameBackground.Show()

		self.AdsTextLine = ui.TextLine()
		self.AdsTextLine.SetParent(self.PetNameBackground)
		self.AdsTextLine.SetWindowHorizontalAlignCenter()
		self.AdsTextLine.SetWindowVerticalAlignCenter()
		self.AdsTextLine.SetHorizontalAlignCenter()
		self.AdsTextLine.SetVerticalAlignCenter()
		self.AdsTextLine.SetPosition(0, -10)
		self.AdsTextLine.SetText("Nume Insotitor")
		self.AdsTextLine.SetPackedFontColor(0xFFFEE3AE)
		self.AdsTextLine.Show()

		self.PriceTextLine = ui.TextLine()
		self.PriceTextLine.SetParent(self.Board)
		self.PriceTextLine.SetWindowHorizontalAlignCenter()
		self.PriceTextLine.SetWindowVerticalAlignCenter()
		self.PriceTextLine.SetHorizontalAlignCenter()
		self.PriceTextLine.SetVerticalAlignCenter()
		self.PriceTextLine.SetPosition(0, 48)
		self.PriceTextLine.SetText("Pret: 10.000.000 Yang +|Eicon/item/71084.tga|e")
		self.PriceTextLine.SetPackedFontColor(0xFFFEE3AE)
		self.PriceTextLine.Show()

		self.accceptButton = ui.MakeButton(self, 13, 150, False, "d:/ymir work/ui/switchbot/", "btn_big_03.sub", "btn_big_02.sub", "btn_big_03.sub")
		self.accceptButton.SetText("Schimba")
		self.accceptButton.SetEvent(ui.__mem_func__(self.AcceptFunc))
	

		self.NameLine = ui.EditLine()
		self.NameLine.SetParent(self.PetNameBackground)
		self.NameLine.SetPosition(14, 29)
		self.NameLine.SetSize(330, 18)
		self.NameLine.SetMax(16)
		self.NameLine.Show()
		
		ItemVnum = player.GetItemIndex(self.InvPos)
		item.SelectItem(ItemVnum)
		
		self.ImageItemVnum = ui.ExpandedImageBoxAnim()
		self.ImageItemVnum.SetParent(self.SlotBackground)
		self.ImageItemVnum.LoadImage(item.GetIconImageFileName())
		self.ImageItemVnum.SetWindowVerticalAlignCenter()
		self.ImageItemVnum.SetPosition(2, -1)
		self.ImageItemVnum.Show()

	def Show(self):
		self.SetCenterPosition()
		self.SetTop()
		ui.ScriptWindow.Show(self)

	def Close(self):
		self.Hide()
		self.cancelEvent()

	def SetCancelEvent(self, event):
		self.cancelEvent = event

	def Destroy(self):
		self.Close()
		self.ClearDictionary()
	
	def AcceptFunc(self):
		if len(self.NameLine.GetText()) < 3:
			chat.AppendChat(1, "Numele trebuie sa fie mai lung.")
			return
		
		Name = self.NameLine.GetText()
		
		if not Name.isalnum():
			chat.AppendChat(1, "Numele poate contine doar caractere normale sau numere.")
			return
		
		net.SendChatPacket("/create_companion %d %s" % (self.InvPos, Name))
		self.Close()

	def OnPressEscapeKey(self):
		self.Close()
		return True

	def OnIMEReturn(self):
		self.Close()
		return True

class OfflineShopNotifyWindow(ui.ScriptWindow):
	def __init__(self):
		ui.ScriptWindow.__init__(self)
		self.dicButtons = {}
		self.dicNotify = {}
		self.CanShow = True
		self.__LoadDialog()

	def __del__(self):
		ui.ScriptWindow.__del__(self)
		
	def __LoadDialog(self):
		self.Board = ui.MakeButton(self, 0, 0, False, "d:/ymir work/ui/public/", "large_button_01.sub", "large_button_02.sub", "large_button_03.sub")
		self.Board.SetText("Show")
		self.Board.SetEvent(ui.__mem_func__(self.Manage))
		self.Board.Show()
		
		self.CanShow = True

		self.AddFlag("movable")
		self.AddFlag("animation")
		# self.Board.AddFlag("not_pick")

		self.SetSize(self.Board.GetWidth(), self.Board.GetHeight() + 35)

	def Show(self): # for test
		self.SetCenterPosition()
		self.SetTop()
		for x in xrange(5):
			self.AddItemLog(19, 1)
		ui.ScriptWindow.Show(self)

	def Close(self):
		self.Hide()

	def Manage(self):
		if len(self.dicButtons) == 0:
			return
			
		cnt = 0
		for k in self.dicButtons.keys():
			if self.dicButtons[k] == None:
				continue
		
			if cnt > 5:
				chat.AppendChat(1, "Unele log-uri nu au putut fi incarcate, vor aparea cand exista spatiu suficient!")
				break
		
			if self.CanShow:
				self.dicButtons[k].Show()
			else:
				self.dicButtons[k].Hide()
				
			cnt += 1
			
		if self.CanShow:
			self.CanShow = False
			self.Board.SetText("Hide")
		else:
			self.CanShow = True
			self.Board.SetText("Show")
	
	def ArrangeButtons(self):
		cnt = 0
		for k in self.dicButtons.keys():
			if self.dicButtons[k] == None:
				continue
		
			self.dicButtons[k].SetPosition(0, 32 + cnt * 32)
			cnt += 1
	
	def Destroy(self):
		self.Close()
		self.dicButtons = {}
		self.dicNotify = {}
		self.ClearDictionary()
	
	def AddItemLog(self, vnum, count):
		item.SelectItem(vnum)
		
		index = len(self.dicButtons)
		
		self.dicButtons[index] = ui.MakeButton(self, 0, 32 + index * 32, False, "d:/ymir work/ui/public/", "large_button_01.sub", "large_button_02.sub", "large_button_03.sub")
		self.dicButtons[index].SetText(item.GetItemName())
		self.dicButtons[index].SetEvent(ui.__mem_func__(self.OpenNotify), index)
		self.dicButtons[index].baseX = vnum
		self.dicButtons[index].Hide()
		
		if self.Board.GetHeight() < 50 * 5:
			self.SetSize(self.Board.GetWidth(), self.Board.GetHeight() + 200)
	
	def OpenNotify(self, index):
		if index not in self.dicButtons:
			return
			
		if self.dicButtons[index] == None:
			return
		
		vnum = self.dicButtons[index].baseX
		
		cnt = len(self.dicNotify)
		self.dicNotify[cnt] = OfflineShopItemNotify(vnum)
		self.dicNotify[cnt].Show()
		
		self.dicButtons[index].Hide()
		self.dicButtons[index] = None
		
		self.ArrangeButtons()
		
		cnt = 0
		for k in self.dicButtons.keys():
			if self.dicButtons[k] == None or cnt > 5:
				continue

			self.dicButtons[k].Show()
			cnt += 1

	def OnPressEscapeKey(self):
		self.Close()
		return True

	def OnIMEReturn(self):
		self.Close()
		return True

class OfflineShopItemNotify(ui.ScriptWindow):
	def __init__(self, ItemVnum = 71124):
		ui.ScriptWindow.__init__(self)
		self.__LoadDialog(ItemVnum)
		self.acceptEvent = lambda *arg: None
		self.cancelEvent = lambda *arg: None

	def __del__(self):
		ui.ScriptWindow.__del__(self)

	def __LoadDialog(self, ItemVnum):
		self.AddFlag("movable")
		self.AddFlag("animation")
		
		item.SelectItem(ItemVnum)
		_, size = item.GetItemSize()
		
		self.Board = ui.BoardWithTitleBar()
		self.Board.SetParent(self)
		if size == 1:
			self.Board.SetSize(350, 200)
		elif size == 2:
			self.Board.SetSize(350, 200 + 50)
		else:
			self.Board.SetSize(350, 200 + 80)	
		self.Board.SetTitleName("Item Sold")
		self.Board.SetCloseEvent(ui.__mem_func__(self.Close))
		self.Board.Show()
		
		if size == 1:
			self.ThinBoard = ui.MakeThinBoardCircle(self.Board, 7, 34, 350 - 16, 180 - 23, False)
		elif size == 2:
			self.ThinBoard = ui.MakeThinBoardCircle(self.Board, 7, 34, 350 - 16, 180 + 50 - 23, False)
		else:
			self.ThinBoard = ui.MakeThinBoardCircle(self.Board, 7, 34, 350 - 16, 180 + 80 - 23, False)
		
		self.HorizontalBar = ui.MakeHorizontalBar(self.Board, 14, 37, 320, "Ai vandut %s pentru 1.000 Yang" % (item.GetItemName()))
		
		if size == 1:
			self.HorizontalBar2 = ui.MakeHorizontalBar(self.Board, 14, 130, 320, "Ai primit 9.990 Yang")
		elif size == 2:
			self.HorizontalBar2 = ui.MakeHorizontalBar(self.Board, 14, 130 + 50, 320, "Ai primit 9.990 Yang")
		elif size == 3:
			self.HorizontalBar2 = ui.MakeHorizontalBar(self.Board, 14, 130 + 80, 320, "Ai primit 9.990 Yang")

		self.SetSize(self.Board.GetWidth(), self.Board.GetHeight())

		self.CloseButton = ui.MakeButton(self.Board, 130, 157, False, "d:/ymir work/ui/public/", "large_button_01.sub", "large_button_02.sub", "large_button_03.sub")
		self.CloseButton.SetText("Inchide")
		self.CloseButton.SetEvent(ui.__mem_func__(self.Close))
		
		if size == 2:
			self.CloseButton.SetPosition(130, 157 + 50)
		elif size == 3:
			self.CloseButton.SetPosition(130, 157 + 80)

		self.ImageItemVnum = ui.ExpandedImageBoxAnim()
		self.ImageItemVnum.SetParent(self)
		self.ImageItemVnum.LoadImage(item.GetIconImageFileName())
		self.ImageItemVnum.SetWindowVerticalAlignCenter()
		self.ImageItemVnum.SetPosition(155, -10)
		self.ImageItemVnum.Show()

	def Show(self):
		self.SetCenterPosition()
		self.SetTop()
		ui.ScriptWindow.Show(self)

	def Close(self):
		self.Hide()

	def Destroy(self):
		self.Close()
		self.ClearDictionary()
	
	def SetButtonName(self, name):
		pass

	def OnPressEscapeKey(self):
		self.Close()
		return True

	def OnIMEReturn(self):
		self.Close()
		return True

class OfflineShopInput(ui.ScriptWindow):
	def __init__(self, ItemVnum):
		ui.ScriptWindow.__init__(self)
		self.__LoadDialog(ItemVnum)
		self.acceptEvent = lambda *arg: None
		self.cancelEvent = lambda *arg: None

	def __del__(self):
		ui.ScriptWindow.__del__(self)

	def __LoadDialog(self, ItemVnum):
		self.AddFlag("movable")
		self.AddFlag("animation")
	
		self.Board = ui.BoardWithTitleBar()
		self.Board.SetParent(self)
		self.Board.SetSize(300, 280)
		self.Board.AddFlag("not_pick")
		self.Board.SetTitleName("Vanzare Obiect")
		self.Board.SetCloseEvent(ui.__mem_func__(self.Close))
		self.Board.Show()
	
		self.ThinBoard = ui.MakeThinBoardCircle(self.Board, 7, 30, self.Board.GetWidth() - 16, self.Board.GetHeight() - 39, False)
		self.HorizontalBar = ui.MakeHorizontalBar(self.Board, 9, 32, 280, "Introdu suma pentru a vinde obiectul!")
		self.ThinSplit = ui.MakeThinBoardCircle(self.Board, 7, 170, self.Board.GetWidth() - 16, 111 - 10, False)

		self.ThinSell = ui.MakeThinBoardCircle(self.Board, 73 + 25, 175 + 5, 150, 19, False)
		self.ThinGive = ui.MakeThinBoardCircle(self.Board, 73 + 25, 200 + 5, 150, 19, False)

		self.SetSize(self.Board.GetWidth(), self.Board.GetHeight())
		
		self.wndMessage1 = ui.MakeText(self.ThinSell, "Suma:", -50, 2)
		self.wndMessage2 = ui.MakeText(self.ThinGive, "Primesti:", -50, 2)

		self.accceptButton = ui.MakeButton(self, 25, 237, False, "d:/ymir work/ui/shop/decoration/", "btn_normal.tga", "btn_hover.tga", "btn_down.tga")
		self.accceptButton.SetText("Vinde")
		self.accceptButton.SetEvent(ui.__mem_func__(self.AcceptFunc))
		
		self.closeButton = ui.MakeButton(self, 186, 237, False, "d:/ymir work/ui/shop/decoration/", "btn_normal.tga", "btn_hover.tga", "btn_down.tga")
		self.closeButton.SetText("Inchide")
		self.closeButton.SetEvent(ui.__mem_func__(self.Close))
		
		self.YangLine = ui.EditLine()
		self.YangLine.SetParent(self.ThinSell)
		self.YangLine.SetPosition(3, 3)
		self.YangLine.SetSize(330, 18)
		self.YangLine.SetMax(15)
		self.YangLine.SetNumberMode()
		self.YangLine.OnIMEUpdate = ui.__mem_func__(self.OnYangInputUpdate)
		self.YangLine.Show()
		
		self.wndYangGive = ui.MakeText(self.ThinGive, "0", 3, 3)
		
		item.SelectItem(ItemVnum)
		
		self.ImageItemVnum = ui.ExpandedImageBoxAnim()
		self.ImageItemVnum.SetParent(self)
		self.ImageItemVnum.LoadImage(item.GetIconImageFileName())
		self.ImageItemVnum.SetWindowVerticalAlignCenter()
		self.ImageItemVnum.SetPosition(132, -48)
		self.ImageItemVnum.Show()
	
	def OnYangInputUpdate(self):
		ui.EditLine.OnIMEUpdate(self.YangLine)
		if len(self.YangLine.GetText()) > 0:
			Price = int(self.YangLine.GetText())
			Tax = Price * 3 / 100;
			Price = Price - Tax
			Price = localeInfo.AddPointToNumberString(long(Price))
			self.wndYangGive.SetText(Price)
		else:
			self.wndYangGive.SetText("0")
	
	# def Show(self):
		# self.SetCenterPosition()
		# self.SetTop()
		# ui.ScriptWindow.Show(self)
	
	def Open(self):
		self.SetCenterPosition()
		self.SetTop()
		self.Show()
		self.YangLine.SetFocus()

	def Close(self):
		self.Hide()
		self.cancelEvent()

	def Destroy(self):
		self.Close()
		self.ClearDictionary()
	
	def AcceptFunc(self):
		self.acceptEvent()
	
	def SetAcceptEvent(self, event):
		self.acceptEvent = event

	def SetCancelEvent(self, event):
		self.cancelEvent = event

	def SetButtonName(self, name):
		pass
		# self.accceptButton.SetText(name)

	def OnPressEscapeKey(self):
		self.Close()
		return True

	def OnIMEReturn(self):
		self.Close()
		return True

class PopupDialog(ui.ScriptWindow):

	def __init__(self):
		ui.ScriptWindow.__init__(self)
		self.__LoadDialog()
		self.acceptEvent = lambda *arg: None

	def __del__(self):
		ui.ScriptWindow.__del__(self)

	def __LoadDialog(self):
		try:
			PythonScriptLoader = ui.PythonScriptLoader()
			PythonScriptLoader.LoadScriptFile(self, "UIScript/PopupDialog.py")

			self.board = self.GetChild("board")
			self.message = self.GetChild("message")
			self.accceptButton = self.GetChild("accept")
			self.accceptButton.SetEvent(ui.__mem_func__(self.Close))

		except:
			import exception
			exception.Abort("PopupDialog.LoadDialog.BindObject")

	def Open(self):
		self.SetCenterPosition()
		self.SetTop()
		self.Show()

	def Close(self):
		self.Hide()
		self.acceptEvent()

	def Destroy(self):
		self.Close()
		self.ClearDictionary()

	def SetWidth(self, width):
		height = self.GetHeight()
		self.SetSize(width, height)
		self.board.SetSize(width, height)
		self.SetCenterPosition()
		self.UpdateRect()

	def SetText(self, text):
		self.message.SetText(text)

	def SetAcceptEvent(self, event):
		self.acceptEvent = event

	def SetButtonName(self, name):
		self.accceptButton.SetText(name)

	def OnPressEscapeKey(self):
		self.Close()
		return True

	def OnIMEReturn(self):
		self.Close()
		return True

class InputDialog(ui.ScriptWindow):

	def __init__(self):
		ui.ScriptWindow.__init__(self)

		self.__CreateDialog()

	def __del__(self):
		ui.ScriptWindow.__del__(self)

	def __CreateDialog(self):

		pyScrLoader = ui.PythonScriptLoader()
		pyScrLoader.LoadScriptFile(self, "uiscript/inputdialog.py")

		getObject = self.GetChild
		self.board = getObject("Board")
		self.acceptButton = getObject("AcceptButton")
		self.cancelButton = getObject("CancelButton")
		self.inputSlot = getObject("InputSlot")
		self.inputValue = getObject("InputValue")

	def Open(self):
		self.inputValue.SetFocus()
		self.SetCenterPosition()
		self.SetTop()
		self.Show()

	def Close(self):
		self.ClearDictionary()
		self.board = None
		self.acceptButton = None
		self.cancelButton = None
		self.inputSlot = None
		self.inputValue = None
		self.Hide()

	def SetTitle(self, name):
		self.board.SetTitleName(name)

	def SetNumberMode(self):
		self.inputValue.SetNumberMode()

	def SetSecretMode(self):
		self.inputValue.SetSecret()

	def SetFocus(self):
		self.inputValue.SetFocus()

	def SetMaxLength(self, length):
		width = length * 6 + 10
		self.SetBoardWidth(max(width + 50, 160))
		self.SetSlotWidth(width)
		self.inputValue.SetMax(length)

	def SetSlotWidth(self, width):
		self.inputSlot.SetSize(width, self.inputSlot.GetHeight())
		self.inputValue.SetSize(width, self.inputValue.GetHeight())
		if self.IsRTL():
			self.inputValue.SetPosition(self.inputValue.GetWidth(), 0)

	def SetBoardWidth(self, width):
		self.SetSize(max(width + 50, 160), self.GetHeight())
		self.board.SetSize(max(width + 50, 160), self.GetHeight())
		if self.IsRTL():
			self.board.SetPosition(self.board.GetWidth(), 0)
		self.UpdateRect()

	def SetAcceptEvent(self, event):
		self.acceptButton.SetEvent(event)
		self.inputValue.OnIMEReturn = event

	def SetCancelEvent(self, event):
		self.board.SetCloseEvent(event)
		self.cancelButton.SetEvent(event)
		self.inputValue.OnPressEscapeKey = event

	def GetText(self):
		return self.inputValue.GetText()

class InputDialogWithDescription(InputDialog):

	def __init__(self):
		ui.ScriptWindow.__init__(self)

		self.__CreateDialog()

	def __del__(self):
		InputDialog.__del__(self)

	def __CreateDialog(self):

		pyScrLoader = ui.PythonScriptLoader()
		pyScrLoader.LoadScriptFile(self, "uiscript/inputdialogwithdescription.py")

		try:
			getObject = self.GetChild
			self.board = getObject("Board")
			self.acceptButton = getObject("AcceptButton")
			self.cancelButton = getObject("CancelButton")
			self.inputSlot = getObject("InputSlot")
			self.inputValue = getObject("InputValue")
			self.description = getObject("Description")

		except:
			import exception
			exception.Abort("InputDialogWithDescription.LoadBoardDialog.BindObject")

	def SetDescription(self, text):
		self.description.SetText(text)

class InputDialogWithDescription2(InputDialog):

	def __init__(self):
		ui.ScriptWindow.__init__(self)

		self.__CreateDialog()

	def __del__(self):
		InputDialog.__del__(self)

	def __CreateDialog(self):

		pyScrLoader = ui.PythonScriptLoader()
		pyScrLoader.LoadScriptFile(self, "uiscript/inputdialogwithdescription2.py")

		try:
			getObject = self.GetChild
			self.board = getObject("Board")
			self.acceptButton = getObject("AcceptButton")
			self.cancelButton = getObject("CancelButton")
			self.inputSlot = getObject("InputSlot")
			self.inputValue = getObject("InputValue")
			self.description1 = getObject("Description1")
			self.description2 = getObject("Description2")

		except:
			import exception
			exception.Abort("InputDialogWithDescription.LoadBoardDialog.BindObject")

	def SetDescription1(self, text):
		self.description1.SetText(text)

	def SetDescription2(self, text):
		self.description2.SetText(text)

class QuestionDialog(ui.ScriptWindow):

	def __init__(self):
		ui.ScriptWindow.__init__(self)
		self.__CreateDialog()

	def __del__(self):
		ui.ScriptWindow.__del__(self)

	def __CreateDialog(self):
		pyScrLoader = ui.PythonScriptLoader()
		pyScrLoader.LoadScriptFile(self, "uiscript/questiondialog.py")

		self.board = self.GetChild("board")
		self.textLine = self.GetChild("message")
		self.acceptButton = self.GetChild("accept")
		self.cancelButton = self.GetChild("cancel")

	def Open(self):
		self.SetCenterPosition()
		self.SetTop()
		self.Show()

	def Close(self):
		self.Hide()

	def SetWidth(self, width):
		height = self.GetHeight()
		self.SetSize(width, height)
		self.board.SetSize(width, height)
		self.SetCenterPosition()
		self.UpdateRect()

	def SAFE_SetAcceptEvent(self, event):
		self.acceptButton.SAFE_SetEvent(event)

	def SAFE_SetCancelEvent(self, event):
		self.cancelButton.SAFE_SetEvent(event)

	def SetAcceptEvent(self, event):
		self.acceptButton.SetEvent(event)

	def SetCancelEvent(self, event):
		self.cancelButton.SetEvent(event)

	def SetText(self, text):
		self.textLine.SetText(text)

	def SetAcceptText(self, text):
		self.acceptButton.SetText(text)

	def SetCancelText(self, text):
		self.cancelButton.SetText(text)

	def OnPressEscapeKey(self):
		self.Close()
		return True
		
class QuestionDialog2(QuestionDialog):

	def __init__(self):
		QuestionDialog.__init__(self)
		self.__CreateDialog()

	def __del__(self):
		QuestionDialog.__del__(self)

	def __CreateDialog(self):
		pyScrLoader = ui.PythonScriptLoader()
		pyScrLoader.LoadScriptFile(self, "uiscript/questiondialog2.py")

		self.board = self.GetChild("board")
		self.textLine1 = self.GetChild("message1")
		self.textLine2 = self.GetChild("message2")
		self.acceptButton = self.GetChild("accept")
		self.cancelButton = self.GetChild("cancel")

	def SetText1(self, text, alignLeft = False):
		self.textLine1.SetText(text)
		if alignLeft == True:
			self.textLine1.SetPosition(15, 30)
			self.textLine1.SetWindowHorizontalAlignLeft()
			self.textLine1.SetHorizontalAlignLeft()
		else:
			self.textLine1.SetPosition(0, 25)
			self.textLine1.SetWindowHorizontalAlignCenter()
			self.textLine1.SetHorizontalAlignCenter()

	def SetText2(self, text, alignLeft = False):
		self.textLine2.SetText(text)
		if alignLeft == True:
			self.textLine2.SetPosition(15, 50)
			self.textLine2.SetWindowHorizontalAlignLeft()
			self.textLine2.SetHorizontalAlignLeft()
		else:
			self.textLine2.SetPosition(0, 50)
			self.textLine2.SetWindowHorizontalAlignCenter()
			self.textLine2.SetHorizontalAlignCenter()
		
	def AutoResize(self, minWidth = 30):
		if self.textLine1.GetTextSize()[0] > self.textLine2.GetTextSize()[0]:
			self.SetWidth(self.textLine1.GetTextSize()[0] + minWidth)
		else:
			self.SetWidth(self.textLine2.GetTextSize()[0] + minWidth)
		
class QuestionDropDialog(ui.ScriptWindow):					
	def __init__(self):
		ui.ScriptWindow.__init__(self)
		self.itemToolTip = None
		self.__CreateDialog()

	def __del__(self):
		self.itemToolTip = None
		ui.ScriptWindow.__del__(self)

	def __CreateDialog(self):
		pyScrLoader = ui.PythonScriptLoader()
		pyScrLoader.LoadScriptFile(self, "uiscript/questiondropdialog.py")
		
		self.board = ui.Window()
		self.board.SetParent(self)
		self.board.SetSize(192, 102)
		self.board.SetPosition(39, 7)
		self.board.Show()
		
		self.GetChild("message2").Hide()

		self.textLine = self.GetChild("message")
		self.textLine.SetParent(self.board)
		self.textLine.SetPosition(0, 35)
		self.SetText(uiScriptLocale.ASK_DROP_ITEM)
		
		self.acceptButton = self.GetChild("accept")
		self.acceptButton.SetParent(self.board)
		self.acceptButton.SetPosition(15, 54)
		
		self.cancelButton = self.GetChild("cancel")
		self.cancelButton.SetParent(self.board)
		self.cancelButton.SetPosition(105, 54)
		
		self.destroyButton = self.GetChild("destroy")	
		self.destroyButton.SetParent(self.board)
		self.destroyButton.SetPosition(58, 79)

		self.itemSlot = self.GetChild("ItemSlot")
		self.itemSlot.SetPosition(6, 8)
		
		self.itemSlot.SetOverInItemEvent(ui.__mem_func__(self.OverInItem))
		self.itemSlot.SetOverOutItemEvent(ui.__mem_func__(self.OverOutItem))

		self.ThinBoard = ui.MakeThinBoardCircle(self.board, 10, 5, 171, 16, False)
		self.ThinBoard.Base.SetColor(grp.GenerateColor(0.0, 0.0, 0.0, 0.11))
		
	def SetItemSlot(self, slotIndex):
		itemIndex = player.GetItemIndex(slotIndex)
		itemCount = player.GetItemCount(slotIndex)
		self.itemSlot.SetItemSlot(0, itemIndex, itemCount)

		item.SelectItem(player.GetItemIndex(slotIndex))

		metinSlot = [player.GetItemMetinSocket(slotIndex, i) for i in xrange(player.METIN_SOCKET_MAX_NUM)]
		attrSlot = [player.GetItemAttribute(slotIndex, i) for i in xrange(player.ATTRIBUTE_SLOT_MAX_NUM)]
		
		if item.IsAntiFlag(item.ITEM_ANTIFLAG_DROP) or self.CheckMap():
			self.acceptButton.Down()
			self.acceptButton.Disable()
		
		if self.itemToolTip:
			self.itemToolTip.Hide()
			self.itemToolTip = None
		
		self.itemToolTip = uiToolTip.ItemToolTip()
		self.itemToolTip.AddItemData(player.GetItemIndex(slotIndex), metinSlot, attrSlot)
		self.itemToolTip.Hide()
		
		if itemCount <= 1:
			self.ThinBoard.SetText("%s" % (item.GetItemName()))
		else:
			self.ThinBoard.SetText("%s x %s" % (item.GetItemName(),str(itemCount)))
		
	def Open(self):
		if self.itemToolTip:
			self.itemToolTip.HideToolTip()
			
		self.SetCenterPosition()
		self.SetTop()
		self.Show()

	def Close(self):
		if self.itemToolTip:
			self.itemToolTip.HideToolTip()
			self.itemToolTip = None
		self.Hide()

	def SetDlgSize(self, width, height):
		self.SetSize(width, height)
		self.board.SetSize(width, height)
		self.SetCenterPosition()
		self.UpdateRect()
		
	def OverInItem(self, slotNumber):
		if self.itemToolTip:
			self.itemToolTip.ShowToolTip()
			
	def OverOutItem(self):
		if self.itemToolTip:
			self.itemToolTip.HideToolTip()

	def SAFE_SetAcceptEvent(self, event):
		self.acceptButton.SAFE_SetEvent(event)

	def SAFE_SetCancelEvent(self, event):
		self.cancelButton.SAFE_SetEvent(event)

	def SetAcceptEvent(self, event):
		self.acceptButton.SetEvent(event)

	def SetCancelEvent(self, event):
		self.cancelButton.SetEvent(event)
		
	def SetDestroyEvent(self, event):
		self.destroyButton.SetEvent(event)
		
	def SetText(self, text):
		self.textLine.SetText(text)
		self.textLine.SetFontColor(0.72, 1.0, 0.0)

	def SetAcceptText(self, text):
		self.acceptButton.SetText(text)

	def SetCancelText(self, text):
		self.cancelButton.SetText(text)

	def OnPressEscapeKey(self):
		self.Close()
		return True

	def CheckMap(self):
		mapcontrol = [
			"metin2_map_a1",
			"metin2_map_b1",
			"metin2_map_duel",
			"metin2_map_t3",
			"metin2_map_oxevent",
		]

		if str(background.GetCurrentMapName()) in mapcontrol:
			return True

		return False

class ItemQuestionDialog(ui.ScriptWindow):
	def __init__(self):
		ui.ScriptWindow.__init__(self)
		self.__CreateDialog()
		
		self.tooltipItem = uiToolTip.ItemToolTip()
		self.window_type = 0 # "inv" or "shop"
		self.count = 0
		self.height = 0 # 30 for buy & sell

	def __del__(self):
		ui.ScriptWindow.__del__(self)

	def __CreateDialog(self):
		pyScrLoader = ui.PythonScriptLoader()
		pyScrLoader.LoadScriptFile(self, "uiscript/questiondialogitem.py")

		self.board = self.GetChild("board")
		self.textLine = self.GetChild("message")
		self.acceptButton = self.GetChild("accept")
		self.cancelButton = self.GetChild("cancel")
		self.destroyButton = self.GetChild("destroy")

		self.board = ui.Window()
		self.board.SetParent(self)
		self.board.SetSize(192, 102)
		self.board.SetPosition(39, 7)
		self.board.Show()

		self.textLine = self.GetChild("message")
		self.textLine.SetParent(self.board)
		self.textLine.SetPosition(0, 35)
		self.SetText(uiScriptLocale.ASK_DROP_ITEM)
		
		self.acceptButton = self.GetChild("accept")
		self.acceptButton.SetParent(self.board)
		self.acceptButton.SetPosition(15, 54)
		
		self.cancelButton = self.GetChild("cancel")
		self.cancelButton.SetParent(self.board)
		self.cancelButton.SetPosition(105, 54)
		
		self.destroyButton = self.GetChild("destroy")	
		self.destroyButton.SetParent(self.board)
		self.destroyButton.SetPosition(58, 79)

		self.ThinBoard = ui.MakeThinBoardCircle(self.board, 10, 5, 171, 16, False)
		self.ThinBoard.Base.SetColor(grp.GenerateColor(0.0, 0.0, 0.0, 0.11))

		self.slotList = []
		for i in xrange(3):
			slot = ui.ImageBox()
			slot.LoadImage("d:/ymir work/ui/public/slot_base.sub")
			slot.SetParent(self)
			self.slotList.append(slot)

	def Open(self, vnum, slot, type_w, text="", mode = 0):
		item.SelectItem(vnum)
		xSlotCount, ySlotCount = item.GetItemSize()
		self.window_type = type_w
		metinSlot = [player.GetItemMetinSocket(type_w, slot, i) for i in xrange(player.METIN_SOCKET_MAX_NUM)]
		self.count = player.GetItemCount(type_w, slot)
		
		if self.count <= 1:
			self.ThinBoard.SetText("%s" % (item.GetItemName()))
		else:
			self.ThinBoard.SetText("%s x %s" % (item.GetItemName(),str(self.count)))
		
		if text:
			textLine2 = ui.TextLine()
			textLine2.SetPosition(0, 80 + 32*ySlotCount)
			textLine2.SetWindowHorizontalAlignCenter()
			textLine2.SetHorizontalAlignCenter()
			textLine2.SetVerticalAlignCenter()
			textLine2.SetParent(self.board)
			textLine2.SetText(text)
			textLine2.Hide()
			self.textLine2 = textLine2
			# self.textLine.SetText(text)
			self.textLine.SetFontColor(0.72, 1.0, 0.0)

		slotGrid = ui.SlotWindow()
		slotGrid.SetParent(self)
		slotGrid.SetPosition(8, 8)
		slotGrid.AppendSlot(0, 0, 0, 32*xSlotCount, 32*ySlotCount)
		slotGrid.AddFlag("not_pick")
		slotGrid.Show()
		self.slotGrid = slotGrid
		
		if self.count > 1:
			self.slotGrid.SetItemSlot(0, vnum, self.count)
		else:
			self.slotGrid.SetItemSlot(0, vnum)

		if text:
			self.height -= 10

		self.board.AddFlag("not_pick")

		for i in xrange(min(3, 3)):
			self.slotList[i].SetPosition(8, 8)
			self.slotList[i].OnMouseOverIn = lambda arg = slot: self.OverInItem(arg)
			self.slotList[i].OnMouseOverOut = lambda arg = self.tooltipItem: self.OverOutItem(arg)
			self.slotList[i].Show()

		self.SetCenterPosition()
		self.SetTop()
		self.Show()

	def SetMessage(self, text):
		self.textLine.SetText(text)

	def OverInItem(self, slot):
		if self.window_type == 0:
			self.tooltipItem.SetInventoryItem(slot)
		else:
			self.tooltipItem.SetInventoryItem(slot, self.window_type)
		
	def OverOutItem(self, tooltipItem):
		if 0 != tooltipItem:
			self.tooltipItem.HideToolTip()
			self.tooltipItem.ClearToolTip()
	
	def Close(self):
		self.ClearDictionary()
		self.slotList = []
		self.textLine2 = None
		self.slotGrid = None
		self.tooltipItem = 0
		self.Hide()
		constInfo.SET_ITEM_QUESTION_DIALOG_STATUS(0)
		
	def SetWidth(self, width):
		height = self.GetHeight()
		self.SetSize(width, height)
		self.board.SetSize(width, height)
		self.SetCenterPosition()
		self.UpdateRect()

	def SAFE_SetAcceptEvent(self, event):
		self.acceptButton.SAFE_SetEvent(event)

	def SAFE_SetCancelEvent(self, event):
		self.cancelButton.SAFE_SetEvent(event)

	def SetAcceptEvent(self, event):
		self.acceptButton.SetEvent(event)
			
	def SetAcceptEvent_Shop(self, event):
		self.acceptButton.SetEvent(event)

	def SetDestroyEvent(self, event):
		self.destroyButton.SetEvent(event)

	def SetCancelEvent(self, event):
		self.cancelButton.SetEvent(event)

	def SetText(self, text):
		self.textLine.SetText(text)

	def SetAcceptText(self, text):
		self.acceptButton.SetText(text)

	def SetCancelText(self, text):
		self.cancelButton.SetText(text)

	def OnPressEscapeKey(self):
		self.Close()
		
		return True		

class QuestionDialogWithTimeLimit(QuestionDialog2):
	def __init__(self):
		ui.ScriptWindow.__init__(self)

		self.__CreateDialog()
		self.endTime = 0
		self.timeOverMsg = 0
		self.timeOverEvent = None
		self.timeOverEventArgs = None

	def __del__(self):
		QuestionDialog2.__del__(self)

	def __CreateDialog(self):
		pyScrLoader = ui.PythonScriptLoader()
		pyScrLoader.LoadScriptFile(self, "uiscript/questiondialog2.py")

		self.board = self.GetChild("board")
		self.textLine1 = self.GetChild("message1")
		self.textLine2 = self.GetChild("message2")
		self.acceptButton = self.GetChild("accept")
		self.cancelButton = self.GetChild("cancel")

	def Open(self, msg, timeout):
		self.SetCenterPosition()
		self.SetTop()
		self.Show()

		self.SetText1(msg)
		self.endTime = app.GetTime() + timeout

	def SetTimeOverEvent(self, event, *args):
		self.timeOverEvent = event
		self.timeOverEventArgs = args

	def SetTimeOverMsg(self, msg):
		self.timeOverMsg = msg

	def OnTimeOver(self):
		if self.timeOverEvent:
			apply(self.timeOverEvent, self.timeOverEventArgs)
		if self.timeOverMsg:
			chat.AppendChat(chat.CHAT_TYPE_INFO, self.timeOverMsg)

	def OnUpdate(self):
		leftTime = max(0, self.endTime - app.GetTime())
		self.SetText2(localeInfo.UI_LEFT_TIME % (leftTime))
		if leftTime <= 0:
			self.OnTimeOver()

class MoneyInputDialog(ui.ScriptWindow):

	def __init__(self):
		ui.ScriptWindow.__init__(self)

		self.moneyHeaderText = localeInfo.MONEY_INPUT_DIALOG_SELLPRICE
		self.__CreateDialog()
		self.SetMaxLength(13)

	def __del__(self):
		ui.ScriptWindow.__del__(self)

	def __CreateDialog(self):

		pyScrLoader = ui.PythonScriptLoader()
		pyScrLoader.LoadScriptFile(self, "uiscript/moneyinputdialog.py")

		getObject = self.GetChild
		self.board = self.GetChild("board")
		self.acceptButton = getObject("AcceptButton")
		self.cancelButton = getObject("CancelButton")
		self.inputValue = getObject("InputValue")
		self.inputValue.SetNumberMode()
		self.inputValue.OnIMEUpdate = ui.__mem_func__(self.__OnValueUpdate)
		self.moneyText = getObject("MoneyValue")

	def Open(self):
		self.inputValue.SetText("")
		self.inputValue.SetFocus()
		self.__OnValueUpdate()
		self.SetCenterPosition()
		self.SetTop()
		self.Show()

	def Close(self):
		self.ClearDictionary()
		self.board = None
		self.acceptButton = None
		self.cancelButton = None
		self.inputValue = None
		self.Hide()

	def SetTitle(self, name):
		self.board.SetTitleName(name)

	def SetFocus(self):
		self.inputValue.SetFocus()

	def SetMaxLength(self, length):
		length = min(13, length)
		self.inputValue.SetMax(length)

	def SetMoneyHeaderText(self, text):
		self.moneyHeaderText = text

	def SetAcceptEvent(self, event):
		self.acceptButton.SetEvent(event)
		self.inputValue.OnIMEReturn = event

	def SetCancelEvent(self, event):
		self.board.SetCloseEvent(event)
		self.cancelButton.SetEvent(event)
		self.inputValue.OnPressEscapeKey = event

	def SetValue(self, value):
		value=str(value)
		self.inputValue.SetText(value)
		self.__OnValueUpdate()
		ime.SetCursorPosition(len(value))


	def GetText(self):
		return self.inputValue.GetText()

	def __OnValueUpdate(self):
		ui.EditLine.OnIMEUpdate(self.inputValue)

		text = self.inputValue.GetText()

		money = 0
		if text and text.isdigit():
			try:
				money = long(text)
			except ValueError:
				money = 199999999

		self.moneyText.SetText(self.moneyHeaderText + localeInfo.NumberToMoneyString(money))

class OnlinePopup(ui.BorderB):
	def __init__(self):
		ui.BorderB.__init__(self)

		self.isActiveSlide = False
		self.isActiveSlideOut = False
		self.endTime = 0
		self.wndWidth = 0

		self.textLine = ui.TextLine()
		self.textLine.SetParent(self)
		self.textLine.SetWindowHorizontalAlignCenter()
		self.textLine.SetWindowVerticalAlignCenter()
		self.textLine.SetHorizontalAlignCenter()
		self.textLine.SetVerticalAlignCenter()
		self.textLine.SetPosition(13, 0)
		self.textLine.Show()

		self.onlineImage = ui.ImageBox()
		self.onlineImage.SetParent(self)
		self.onlineImage.SetPosition(8, 8)
		self.onlineImage.LoadImage("d:/ymir work/ui/game/windows/messenger_list_online.sub")
		self.onlineImage.Show()

	def __del__(self):
		ui.BorderB.__del__(self)

	def SlideIn(self):
		self.SetTop()
		self.Show()

		self.isActiveSlide = True
		self.endTime = app.GetGlobalTimeStamp() + 5

	def Close(self):
		self.Hide()

	def Destroy(self):
		self.Close()

	def SetUserName(self, name):
		self.textLine.SetText("%s este online." % str(name))

		self.wndWidth = self.textLine.GetTextSize()[0] + 40
		self.SetSize(self.wndWidth, 25)
		self.SetPosition(-self.wndWidth, wndMgr.GetScreenHeight() - 200)

	def OnUpdate(self):
		if self.isActiveSlide and self.isActiveSlide == True:
			x, y = self.GetLocalPosition()
			if x < 0:
				self.SetPosition(x + 4, y)

		if self.endTime - app.GetGlobalTimeStamp() <= 0 and self.isActiveSlideOut == False and self.isActiveSlide == True:
			self.isActiveSlide = False
			self.isActiveSlideOut = True

		if self.isActiveSlideOut and self.isActiveSlideOut == True:
			x, y = self.GetLocalPosition()
			if x > -(self.wndWidth):
				self.SetPosition(x - 4, y)

			if x <= -(self.wndWidth):
				self.isActiveSlideOut = False
				self.Close()
				
class NotifyPopup(ui.BorderB):
	def __init__(self):
		ui.BorderB.__init__(self)

		self.isActiveSlide = False
		self.isActiveSlideOut = False
		self.endTime = 0
		self.wndWidth = 0

		self.textLine = ui.TextLine()
		self.textLine.SetParent(self)
		self.textLine.SetWindowHorizontalAlignCenter()
		self.textLine.SetWindowVerticalAlignCenter()
		self.textLine.SetHorizontalAlignCenter()
		self.textLine.SetVerticalAlignCenter()
		self.textLine.SetPosition(0, -15)
		self.textLine.Show()

		self.textLine2 = ui.TextLine()
		self.textLine2.SetParent(self)
		self.textLine2.SetWindowHorizontalAlignCenter()
		self.textLine2.SetWindowVerticalAlignCenter()
		self.textLine2.SetHorizontalAlignCenter()
		self.textLine2.SetVerticalAlignCenter()
		self.textLine2.SetPosition(0, 15)
		self.textLine2.Show()

	def __del__(self):
		ui.BorderB.__del__(self)

	def SlideIn(self):
		self.SetTop()
		self.Show()

		self.isActiveSlide = True
		self.endTime = app.GetGlobalTimeStamp() + 5

	def Close(self):
		self.Hide()

	def Destroy(self):
		self.Close()

	def SetTextNotify(self, text):
		self.textLine.SetText(text)

		self.wndWidth = self.textLine.GetTextSize()[0] + 40
		self.SetSize(self.wndWidth, 25)
		self.SetPosition(-self.wndWidth, wndMgr.GetScreenHeight() - 200)

	def SetText2Notify(self, text):
		self.textLine2.SetText(text)
		
		if self.wndWidth < self.textLine2.GetTextSize()[0] + 40:
			self.wndWidth = self.textLine2.GetTextSize()[0] + 40
			
			self.SetSize(self.wndWidth, 25)

		self.SetPosition(-self.wndWidth, wndMgr.GetScreenHeight() - 200)

	def OnUpdate(self):
		if self.isActiveSlide and self.isActiveSlide == True:
			x, y = self.GetLocalPosition()
			if x < 0:
				self.SetPosition(x + 4, y)

		if self.endTime - app.GetGlobalTimeStamp() <= 0 and self.isActiveSlideOut == False and self.isActiveSlide == True:
			self.isActiveSlide = False
			self.isActiveSlideOut = True

		if self.isActiveSlideOut and self.isActiveSlideOut == True:
			x, y = self.GetLocalPosition()
			if x > -(self.wndWidth):
				self.SetPosition(x - 4, y)

			if x <= -(self.wndWidth):
				self.isActiveSlideOut = False
				self.Close()
				
class BuyItemPopupDialog(ui.ScriptWindow):
	def __init__(self):
		ui.ScriptWindow.__init__(self)
		self.LoadDialog()
		self.itemVnum = 0
		self.itemVnum2 = 0
		self.itemToolTip = None
		self.itemToolTipSecond = None

	def __del__(self):
		ui.ScriptWindow.__del__(self)

	def LoadDialog(self):
		try:
			PythonScriptLoader = ui.PythonScriptLoader()
			PythonScriptLoader.LoadScriptFile(self, "UIScript/BuyItemPopupDialog.py")

			self.board = self.GetChild("board")
			self.firstText = self.GetChild("firstText")
			self.testWindow = self.GetChild("testWindow")
			self.itemImage = self.GetChild("itemImage")
			self.itemImage2 = self.GetChild("itemImage2")
			self.secondText = self.GetChild("secondText")
			self.questionText = self.GetChild("questionText")
			self.acceptButton = self.GetChild("accept")
			self.cancelButton = self.GetChild("cancel")
			
			# self.secondText.Hide()
			self.questionText.Hide()
			
			self.itemImage.SetEvent(ui.__mem_func__(self.OverInItem), "MOUSE_OVER_IN")
			self.itemImage.SetEvent(ui.__mem_func__(self.OverOutItem), "MOUSE_OVER_OUT")
			self.itemImage2.SetEvent(ui.__mem_func__(self.OverInItemSecond), "MOUSE_OVER_IN")
			self.itemImage2.SetEvent(ui.__mem_func__(self.OverOutItemSecond), "MOUSE_OVER_OUT")
			
			self.itemImage.Hide()
			self.itemImage2.Hide()
		except:
			import exception
			exception.Abort("PopupDialog.LoadDialog.BindObject")

	def Open(self):
		self.SetCenterPosition()
		self.SetTop()
		self.SetFocus()
		self.Show()

	def Close(self):
		self.Hide()
		self.itemVnum = 0
		self.itemVnum2 = 0
		self.secondText.Hide()
		self.questionText.Hide()
		self.itemImage.Hide()
		self.itemImage2.Hide()
		
		if self.itemToolTip:
			self.itemToolTip.ClearToolTip()
			self.itemToolTip.HideToolTip()
		
		if self.itemToolTipSecond:
			self.itemToolTipSecond.ClearToolTip()
			self.itemToolTipSecond.HideToolTip()

	def Destroy(self):
		self.Close()
		self.ClearDictionary()
		self.itemToolTip = None
		self.itemToolTipSecond = None

	def SetWidth(self, width):
		height = self.GetHeight()
		self.SetSize(width, height)
		self.board.SetSize(width, height)
		self.SetCenterPosition()
		self.UpdateRect()
		
	def AutoResize(self, minWidth = 30, hasMoreItems = False):
		if hasMoreItems == False:
			self.SetWidth(self.firstText.GetTextSize()[0] + self.itemImage.GetWidth() + 6 + minWidth)
			self.testWindow.SetSize(self.firstText.GetTextSize()[0] + self.itemImage.GetWidth() + 6, 32)
		elif hasMoreItems == True:
			self.SetWidth(self.firstText.GetTextSize()[0] + self.itemImage.GetWidth() + self.itemImage2.GetWidth() + self.secondText.GetTextSize()[0] + 6 + minWidth)
			self.testWindow.SetSize(self.firstText.GetTextSize()[0] + self.itemImage.GetWidth() + self.itemImage2.GetWidth() + self.secondText.GetTextSize()[0] + 6, 32)
		else:
			self.SetWidth(self.firstText.GetTextSize()[0] + minWidth)
			self.testWindow.SetSize(self.firstText.GetTextSize()[0], 32)

	def SetText(self, text):
		if self.itemVnum:
			item.SelectItem(self.itemVnum)
			splitText = text.split("|")
			self.firstText.SetText(splitText[0])
			
			self.itemImage.LoadImage(item.GetIconImageFileName())
			self.itemImage.SetPosition(self.firstText.GetTextSize()[0] + 2, 0)
			self.itemImage.Show()
						
			if self.itemVnum2 > 0:
				self.questionText.SetText(splitText[2])

				item.SelectItem(self.itemVnum2)
				
				self.secondText.SetText(splitText[1])
				self.secondText.SetPosition(self.firstText.GetTextSize()[0] + self.itemImage.GetWidth() - 5, 15)
				self.secondText.Show()
				
				self.itemImage2.LoadImage(item.GetIconImageFileName())
				self.itemImage2.SetPosition(self.firstText.GetTextSize()[0]+ self.secondText.GetTextSize()[0] + 26, 0)
				self.itemImage2.Show()
				
				self.questionText.SetPosition(self.firstText.GetTextSize()[0] + self.secondText.GetTextSize()[0] + self.itemImage.GetWidth() + self.itemImage2.GetWidth() - 8, 15)

			else:
				self.secondText.Hide()
				self.itemImage2.Hide()
				self.questionText.SetPosition(self.firstText.GetTextSize()[0] + self.itemImage.GetWidth() - 1, 15)
				self.questionText.SetText(splitText[1])
				
			self.questionText.Show()

		else:
			self.firstText.SetText(text)
		
	def SetItem(self, itemVnum):
		self.itemVnum = itemVnum
		
		if not self.itemToolTip:
			self.itemToolTip = uiToolTip.ItemToolTip()
			
		metinSlot = []
		for i in xrange(player.METIN_SOCKET_MAX_NUM):
			metinSlot.append(0)
		attrSlot = []
		for i in xrange(player.ATTRIBUTE_SLOT_MAX_NUM):
			attrSlot.append((0, 0))
		
		self.itemToolTip.ClearToolTip()

		self.itemToolTip.AddItemData(self.itemVnum, metinSlot, attrSlot)
		self.itemToolTip.HideToolTip()

	def SetItem2(self, itemVnum2):
		self.itemVnum2 = itemVnum2
		
		if not self.itemToolTipSecond:
			self.itemToolTipSecond = uiToolTip.ItemToolTip()
			
		metinSlot = []
		for i in xrange(player.METIN_SOCKET_MAX_NUM):
			metinSlot.append(0)
		attrSlot = []
		for i in xrange(player.ATTRIBUTE_SLOT_MAX_NUM):
			attrSlot.append((0, 0))
		
		self.itemToolTipSecond.ClearToolTip()
		
		self.itemToolTipSecond.AddItemData(self.itemVnum2, metinSlot, attrSlot)
		self.itemToolTipSecond.HideToolTip()
		
	def SAFE_SetAcceptEvent(self, event):
		self.acceptButton.SAFE_SetEvent(event)

	def SAFE_SetCancelEvent(self, event):
		self.cancelButton.SAFE_SetEvent(event)

	def SetAcceptEvent(self, event):
		self.acceptButton.SetEvent(event)

	def SetCancelEvent(self, event):
		self.cancelButton.SetEvent(event)

	def OverInItem(self, eventArg):
		if self.itemToolTip:
			self.itemToolTip.ShowToolTip()
			
	def OverOutItem(self, eventArg):
		if self.itemToolTip:
			self.itemToolTip.HideToolTip()
			
	def OverInItemSecond(self, eventArg):
		if self.itemToolTipSecond:
			self.itemToolTipSecond.ShowToolTip()
			
	def OverOutItemSecond(self, eventArg):
		if self.itemToolTipSecond:
			self.itemToolTipSecond.HideToolTip()
			
	def ScaleIcons(self, scaleX, scaleY):
		if self.itemImage:
			self.itemImage.SetScale(scaleX, scaleY)
		if self.itemImage2:
			self.itemImage2.SetScale(scaleX, scaleY)

	def OnPressEscapeKey(self):
		self.Close()
		return True

	def OnIMEReturn(self):
		self.Close()
		return True