import app
import ime
import grp
import wndMgr
import item
import skill
import localeInfo
import dbg
import constInfo
import cfg
# MARK_BUG_FIX
import guild
# END_OF_MARK_BUG_FIX
import renderTarget

from _weakref import proxy

BACKGROUND_COLOR = grp.GenerateColor(0.0, 0.0, 0.0, 1.0)
DARK_COLOR = grp.GenerateColor(0.2, 0.2, 0.2, 1.0)
BRIGHT_COLOR = grp.GenerateColor(0.7, 0.7, 0.7, 1.0)
BLUE_COLOR = grp.GenerateColor(0.0, 100.0, 255.0, 0.5)
BLUE_COLOR_2 = grp.GenerateColor(25.0, 100.0, 255.0, 0.5)
BLUE_COLOR_3 = grp.GenerateColor(45.0, 100.0, 255.0, 0.5)
BLUE_COLOR_4 = grp.GenerateColor(75.0, 100.0, 255.0, 0.5)
BLUE_COLOR_5 = grp.GenerateColor(105.0, 100.0, 255.0, 0.5)

# FOR UITARGET_SYSTEM_COLOR
TIME_CHANGE_PER_COLOR = 0.7

SELECT_COLOR = grp.GenerateColor(0.0, 0.0, 0.5, 0.3)

WHITE_COLOR = grp.GenerateColor(1.0, 1.0, 1.0, 0.5)
HALF_WHITE_COLOR = grp.GenerateColor(1.0, 1.0, 1.0, 0.2)

createToolTipWindowDict = {}
def RegisterCandidateWindowClass(codePage, candidateWindowClass):
	EditLine.candidateWindowClassDict[codePage]=candidateWindowClass
def RegisterToolTipWindow(type, createToolTipWindow):
	createToolTipWindowDict[type]=createToolTipWindow

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

app.SetDefaultFontName(localeInfo.UI_DEF_FONT)

## Window Manager Event List##
##############################
## "OnMouseLeftButtonDown"
## "OnMouseLeftButtonUp"
## "OnMouseLeftButtonDoubleClick"
## "OnMouseRightButtonDown"
## "OnMouseRightButtonUp"
## "OnMouseRightButtonDoubleClick"
## "OnMouseDrag"
## "OnSetFocus"
## "OnKillFocus"
## "OnMouseOverIn"
## "OnMouseOverOut"
## "OnRender"
## "OnUpdate"
## "OnKeyDown"
## "OnKeyUp"
## "OnTop"
## "OnIMEUpdate" ## IME Only
## "OnIMETab"	## IME Only
## "OnIMEReturn" ## IME Only
##############################
## Window Manager Event List##

if constInfo.DETECT_LEAKING_WINDOWS:
	import weakref
	import sys
	def trace_calls_and_returns(frame, event, arg): #as the name (somewhat) implies build trace of calls and remove trace on returns
		co = frame.f_code
		func_name = co.co_name
		line_no = frame.f_lineno
		filename = co.co_filename
		if event == 'call' or event == 'c_call':
			constInfo.WINDOW_OBJ_TRACE.append('Call to %s on line %s of %s' % (func_name, line_no, filename))
			return trace_calls_and_returns
		elif (event == 'return' or event == 'c_return') and len(constInfo.WINDOW_OBJ_TRACE):
			constInfo.WINDOW_OBJ_TRACE.pop(-1)
		return

	sys.settrace(trace_calls_and_returns)

	class ExtendedRef(weakref.ref): # extended weakref object to store the backtrace, type of actual object and the parent name, if any
		def __init__(self, ob, callback=None):
			super(ExtendedRef, self).__init__(ob, callback)
			self.typeStr = str(ob)
			self.strParent = ""
			self.traceBack = constInfo.WINDOW_OBJ_TRACE[:] # just deepcopy the current trace


class __mem_func__:
	class __noarg_call__:
		def __init__(self, cls, obj, func):
			self.cls=cls
			self.obj=proxy(obj)
			self.func=proxy(func)

		def __call__(self, *arg):
			return self.func(self.obj)

	class __arg_call__:
		def __init__(self, cls, obj, func):
			self.cls=cls
			self.obj=proxy(obj)
			self.func=proxy(func)

		def __call__(self, *arg):
			return self.func(self.obj, *arg)

	def __init__(self, mfunc):
		if mfunc.im_func.func_code.co_argcount>1:
			self.call=__mem_func__.__arg_call__(mfunc.im_class, mfunc.im_self, mfunc.im_func)
		else:
			self.call=__mem_func__.__noarg_call__(mfunc.im_class, mfunc.im_self, mfunc.im_func)

	def __call__(self, *arg):
		return self.call(*arg)


class Window(object):
	def NoneMethod(cls):
		pass

	NoneMethod = classmethod(NoneMethod)

	def __init__(self, layer = "UI"):
		if constInfo.DETECT_LEAKING_WINDOWS:
			constInfo.WINDOW_TOTAL_OBJ_COUNT += 1 # increase total obj count
			if constInfo.WINDOW_COUNT_OBJ: # if we are counting window objects increase the normal obj count and save the traceback to know where the window creation have been called from
				constInfo.WINDOW_OBJ_COUNT += 1
				constInfo.WINDOW_OBJ_LIST[id(self)] = ExtendedRef(self) # save trace and other data

	
		self.hWnd = None
		self.parentWindow = 0
		self.onMouseLeftButtonUpEvent = None
		self.onRunMouseWheelEvent = None
		self.xPosLast = 0
		self.yPostLast = 0
		self.RegisterWindow(layer)
		self.Hide()
		
		if app.ENABLE_SEND_TARGET_INFO:
			self.mouseLeftButtonDownEvent = None
			self.mouseLeftButtonDownArgs = None
			self.mouseLeftButtonUpEvent = None
			self.mouseLeftButtonUpArgs = None
			self.mouseLeftButtonDoubleClickEvent = None
			self.mouseRightButtonDownEvent = None
			self.mouseRightButtonDownArgs = None
			self.moveWindowEvent = None
			self.renderEvent = None
			self.renderArgs = None

			self.overInEvent = None
			self.overInArgs = None

			self.overOutEvent = None
			self.overOutArgs = None

			self.baseX = 0
			self.baseY = 0

			self.SetWindowName("NONAME_Window")

	def __del__(self):
		if constInfo.DETECT_LEAKING_WINDOWS: #looks like this window is not leaking cus __del__ has been called, remove it from the active window list
			constInfo.WINDOW_TOTAL_OBJ_COUNT -= 1
			if constInfo.WINDOW_COUNT_OBJ and id(self) in constInfo.WINDOW_OBJ_LIST:
				constInfo.WINDOW_OBJ_COUNT -= 1
				constInfo.WINDOW_OBJ_LIST.pop(id(self))
	

		wndMgr.Destroy(self.hWnd)

	def RegisterWindow(self, layer):
		self.hWnd = wndMgr.Register(self, layer)

	def Destroy(self):
		pass

	def GetWindowHandle(self):
		return self.hWnd

	def AddFlag(self, style):
		if style == "animation" and int(cfg.Get(cfg.SAVE_GENERAL, "SHOW_ANIMATION")) == 0:
			return
			
		wndMgr.AddFlag(self.hWnd, style)

	def IsRTL(self):
		return wndMgr.IsRTL(self.hWnd)

	def SetWindowName(self, Name):
		wndMgr.SetName(self.hWnd, Name)

	def GetWindowName(self):
		return wndMgr.GetName(self.hWnd)

	if app.ENABLE_SEND_TARGET_INFO:
		def SetParent(self, parent, bCanRect = None): # NEW_RECT
			if parent:
				if bCanRect != None:
					wndMgr.SetParent(self.hWnd, parent.hWnd, bCanRect)
				else:
					wndMgr.SetParent(self.hWnd, parent.hWnd)
				if constInfo.DETECT_LEAKING_WINDOWS: # find our window in the saved obj list and save its parent address
					if constInfo.WINDOW_COUNT_OBJ and id(self) in constInfo.WINDOW_OBJ_LIST:
						constInfo.WINDOW_OBJ_LIST[id(self)].strParent = str(parent)
			else:
				wndMgr.SetParent(self.hWnd, 0)
	
		def SetAttachParent(self, parent):
			wndMgr.SetAttachParent(self.hWnd, parent.hWnd)
	else:
		def SetParent(self, parent, bCanRect = None): # NEW_RECT
			if bCanRect != None:
				wndMgr.SetParent(self.hWnd, parent.hWnd, bCanRect)
			else:
				wndMgr.SetParent(self.hWnd, parent.hWnd)
			# wndMgr.SetParent(self.hWnd, parent.hWnd, bCanRect)
			if constInfo.DETECT_LEAKING_WINDOWS: # find our window in the saved obj list and save its parent address
				if constInfo.WINDOW_COUNT_OBJ and id(self) in constInfo.WINDOW_OBJ_LIST:
					constInfo.WINDOW_OBJ_LIST[id(self)].strParent = str(parent)

	def SetParentProxy(self, parent):
		self.parentWindow=proxy(parent)
		wndMgr.SetParent(self.hWnd, parent.hWnd)
		if constInfo.DETECT_LEAKING_WINDOWS: # find our window in the saved obj list and save its parent address
			if constInfo.WINDOW_COUNT_OBJ and id(self) in constInfo.WINDOW_OBJ_LIST:
				constInfo.WINDOW_OBJ_LIST[id(self)].strParent = str(parent)

	def GetParentProxy(self):
		return self.parentWindow

	def SetPickAlways(self):
		wndMgr.SetPickAlways(self.hWnd)

	def SetWindowHorizontalAlignLeft(self):
		wndMgr.SetWindowHorizontalAlign(self.hWnd, wndMgr.HORIZONTAL_ALIGN_LEFT)

	def SetWindowHorizontalAlignCenter(self):
		wndMgr.SetWindowHorizontalAlign(self.hWnd, wndMgr.HORIZONTAL_ALIGN_CENTER)

	def SetWindowHorizontalAlignRight(self):
		wndMgr.SetWindowHorizontalAlign(self.hWnd, wndMgr.HORIZONTAL_ALIGN_RIGHT)

	def SetWindowVerticalAlignTop(self):
		wndMgr.SetWindowVerticalAlign(self.hWnd, wndMgr.VERTICAL_ALIGN_TOP)

	def SetWindowVerticalAlignCenter(self):
		wndMgr.SetWindowVerticalAlign(self.hWnd, wndMgr.VERTICAL_ALIGN_CENTER)

	def SetWindowVerticalAlignBottom(self):
		wndMgr.SetWindowVerticalAlign(self.hWnd, wndMgr.VERTICAL_ALIGN_BOTTOM)

	def SetTop(self):
		wndMgr.SetTop(self.hWnd)

	def Show(self):
		wndMgr.Show(self.hWnd)

	def ShowScale(self):
		wndMgr.Show(self.hWnd)
		# wndMgr.ShowWithAnim(self.hWnd)

	def Hide(self):
		wndMgr.Hide(self.hWnd)

	if app.ENABLE_SEND_TARGET_INFO:
		def SetVisible(self, is_show):
			if is_show:
				self.Show()
			else:
				self.Hide()

	def Lock(self):
		wndMgr.Lock(self.hWnd)

	def Unlock(self):
		wndMgr.Unlock(self.hWnd)

	def IsShow(self):
		return wndMgr.IsShow(self.hWnd)

	def UpdateRect(self):
		wndMgr.UpdateRect(self.hWnd)

	def SetSize(self, width, height):
		wndMgr.SetWindowSize(self.hWnd, width, height)

	def GetWidth(self):
		return wndMgr.GetWindowWidth(self.hWnd)

	def GetHeight(self):
		return wndMgr.GetWindowHeight(self.hWnd)

	def GetLocalPosition(self):
		return wndMgr.GetWindowLocalPosition(self.hWnd)

	if app.ENABLE_SEND_TARGET_INFO:
		def GetLeft(self):
			x, y = self.GetLocalPosition()
			return x
	
		def GetGlobalLeft(self):
			x, y = self.GetGlobalPosition()
			return x
	
		def GetTop(self):
			x, y = self.GetLocalPosition()
			return y
	
		def GetGlobalTop(self):
			x, y = self.GetGlobalPosition()
			return y
	
		def GetRight(self):
			return self.GetLeft() + self.GetWidth()
	
		def GetBottom(self):
			return self.GetTop() + self.GetHeight()

	def GetGlobalPosition(self):
		return wndMgr.GetWindowGlobalPosition(self.hWnd)

	def GetMouseLocalPosition(self):
		return wndMgr.GetMouseLocalPosition(self.hWnd)

	def GetRect(self):
		return wndMgr.GetWindowRect(self.hWnd)

	if app.ENABLE_SEND_TARGET_INFO:
		def SetLeft(self, x):
			wndMgr.SetWindowPosition(self.hWnd, x, self.GetTop())

	if app.ENABLE_SEND_TARGET_INFO:
		def SavePosition(self):
			self.baseX = self.GetLeft()
			self.baseY = self.GetTop()
	
		def UpdatePositionByScale(self, scale):
			self.SetPosition(self.baseX * scale, self.baseY * scale)

	def SetPosition(self, x, y, IsMoving = False):
		if IsMoving:
			if x > self.xPosLast:
				x = self.xPosLast
				
			if y > self.yPostLast:
				y = self.yPostLast
	
		wndMgr.SetWindowPosition(self.hWnd, x, y)

		if not IsMoving:
			self.xPosLast = x
			self.yPostLast = y

	def SetCenterPosition(self, x = 0, y = 0):
		self.SetPosition((wndMgr.GetScreenWidth() - self.GetWidth()) / 2 + x, (wndMgr.GetScreenHeight() - self.GetHeight()) / 2 + y)

	def IsFocus(self):
		return wndMgr.IsFocus(self.hWnd)

	def SetFocus(self):
		wndMgr.SetFocus(self.hWnd)

	def KillFocus(self):
		wndMgr.KillFocus(self.hWnd)

	def GetChildCount(self):
		return wndMgr.GetChildCount(self.hWnd)

	# def IsIn(self):
		# return wndMgr.IsIn(self.hWnd)
	
	# WIKIPEDIA
	def IsIn(self, checkChilds = False):
		return wndMgr.IsIn(self.hWnd, checkChilds)
		
	def GetRenderBox(self):
		return wndMgr.GetRenderBox(self.hWnd)
	
	def SetInsideRender(self, val):
		wndMgr.SetInsideRender(self.hWnd, val)
	
	def AdjustSize(self):
		x, y = self.GetTextSize()
		wndMgr.SetWindowSize(self.hWnd, x, y)
	#END_OF_WIKIPEDIA
	
	def SetOnMouseLeftButtonUpEvent(self, event):
		self.onMouseLeftButtonUpEvent = event

	def OnMouseLeftButtonUp(self):
		if self.onMouseLeftButtonUpEvent:
			self.onMouseLeftButtonUpEvent()

	def OnRunMouseWheel(self, nLen):
		if not self.onRunMouseWheelEvent:
			return False

		apply(self.onRunMouseWheelEvent, nLen)
		return True

	def SetOnRunMouseWheelEvent(self, event):
		self.onRunMouseWheelEvent = __mem_func__(event)

	if app.ENABLE_SEND_TARGET_INFO:
		def IsInPosition(self):
			xMouse, yMouse = wndMgr.GetMousePosition()
			x, y = self.GetGlobalPosition()
			return xMouse >= x and xMouse < x + self.GetWidth() and yMouse >= y and yMouse < y + self.GetHeight()
	
		def SetMouseLeftButtonDownEvent(self, event, *args):
			self.mouseLeftButtonDownEvent = event
			self.mouseLeftButtonDownArgs = args
	
		def OnMouseLeftButtonDown(self):
			if self.mouseLeftButtonDownEvent:
				apply(self.mouseLeftButtonDownEvent, self.mouseLeftButtonDownArgs)

		def SetMouseLeftButtonDoubleClickEvent(self, event):
			self.mouseLeftButtonDoubleClickEvent = event
	
		def OnMouseLeftButtonDoubleClick(self):
			if self.mouseLeftButtonDoubleClickEvent:
				self.mouseLeftButtonDoubleClickEvent()
	
		def SetMouseRightButtonDownEvent(self, event, *args):
			self.mouseRightButtonDownEvent = event
			self.mouseRightButtonDownArgs = args
	
		def OnMouseRightButtonDown(self):
			if self.mouseRightButtonDownEvent:
				apply(self.mouseRightButtonDownEvent, self.mouseRightButtonDownArgs)
	
		def SetMoveWindowEvent(self, event):
			self.moveWindowEvent = event
	
		def OnMoveWindow(self, x, y):
			if self.moveWindowEvent:
				self.moveWindowEvent(x, y)
	
		def SAFE_SetOverInEvent(self, func, *args):
			self.overInEvent = __mem_func__(func)
			self.overInArgs = args
	
		def SetOverInEvent(self, func, *args):
			self.overInEvent = func
			self.overInArgs = args
	
		def SAFE_SetOverOutEvent(self, func, *args):
			self.overOutEvent = __mem_func__(func)
			self.overOutArgs = args
	
		def SetOverOutEvent(self, func, *args):
			self.overOutEvent = func
			self.overOutArgs = args
	
		def OnMouseOverIn(self):
			if self.overInEvent:
				apply(self.overInEvent, self.overInArgs)
	
		def OnMouseOverOut(self):
			if self.overOutEvent:
				apply(self.overOutEvent, self.overOutArgs)
	
		def SAFE_SetRenderEvent(self, event, *args):
			self.renderEvent = __mem_func__(event)
			self.renderArgs = args
	
		def ClearRenderEvent(self):
			self.renderEvent = None
			self.renderArgs = None
	
		def OnRender(self):
			if self.renderEvent:
				apply(self.renderEvent, self.renderArgs)

class CheckBox_Biolog(Window):

	STATE_UNSELECTED = 0
	STATE_SELECTED = 1

	def __init__(self, layer = "UI"):
		Window.__init__(self, layer)

		self.state = self.STATE_UNSELECTED
		self.eventFunc = None
		self.eventArgs = None

		self.overIn = ""

		self.btnBox = {
			self.STATE_UNSELECTED : self.__init_MakeButton("d:/ymir work/ui/game/bio/checkbox_empty.png"),
			self.STATE_SELECTED : self.__init_MakeButton("d:/ymir work/ui/game/bio/checkbox_full.png", "d:/ymir work/ui/game/bio/checkbox_full.png"),
		}

		text = TextLine()
		text.SetParent(self)
		text.SetWindowVerticalAlignCenter()
		text.SetVerticalAlignCenter()
		text.Show()
		self.text = text

		self.__Refresh()

		self.SetWindowName("NONAME_CheckBox")

	def __del__(self):
		Window.__del__(self)

	def __ConvertPath(self, path, subStr):
		if path.find("%s") != -1:
			return path % subStr
		else:
			return path

	def __init_MakeButton(self, path, disablePath = None):
		btn = Button()
		btn.SetParent(self)
		btn.SetWindowVerticalAlignCenter()
		btn.SetUpVisual(self.__ConvertPath(path, "01"))
		btn.SetOverVisual(self.__ConvertPath(path, "02"))
		btn.SetDownVisual(self.__ConvertPath(path, "03"))
		if disablePath:
			btn.SetDisableVisual(disablePath)
		else:
			btn.SetDisableVisual(self.__ConvertPath(path, "01"))
		btn.SAFE_SetEvent(self.OnClickButton)
		btn.baseWidth = btn.GetWidth()
		return btn

	def __UpdateRect(self):
		if self.text.GetText():
			width = self.btnBox[self.state].baseWidth + 5 + self.text.GetTextWidth()
		else:
			width = self.btnBox[self.state].baseWidth
		height = max(self.btnBox[self.state].GetHeight(), self.text.GetTextHeight())
		self.SetSize(width, height)

		self.btnBox[self.state].SetSize(width, self.btnBox[self.state].GetHeight())
		self.text.SetPosition(self.btnBox[self.state].baseWidth + 5, 0)

		self.text.UpdateRect()
		self.btnBox[self.state].UpdateRect()
		self.UpdateRect()

	def __Refresh(self):
		self.__UpdateRect()

		self.btnBox[self.STATE_UNSELECTED].SetVisible(self.state == self.STATE_UNSELECTED)
		self.btnBox[self.STATE_SELECTED].SetVisible(self.state == self.STATE_SELECTED)

	def SAFE_SetOverInData(self, data):
		self.btnBox[self.state].SetToolTipText(data)

	def OnClickButton(self):
		if self.state == self.STATE_UNSELECTED:
			self.state = self.STATE_SELECTED
		else:
			self.state = self.STATE_UNSELECTED

		self.__Refresh()

		if self.eventFunc:
			apply(self.eventFunc, self.eventArgs)

	def SetChecked(self, state):
		self.state = state
		self.__Refresh()

	def IsChecked(self):
		return self.state != self.STATE_UNSELECTED

	def SetText(self, text):
		self.text.SetText(text)
		self.__UpdateRect()

	def SetEvent(self, event, *args):
		self.eventFunc = event
		self.eventArgs = args

	def SAFE_SetEvent(self, event, *args):
		self.eventFunc = __mem_func__(event)
		self.eventArgs = args

	def Disable(self):
		self.btnBox[self.STATE_UNSELECTED].Disable()
		self.btnBox[self.STATE_SELECTED].Disable()

	def Enable(self):
		self.btnBox[self.STATE_UNSELECTED].Enable()
		self.btnBox[self.STATE_SELECTED].Enable()

class BoxedBoard(Window):
	BORDER_TOP = 0
	BORDER_RIGHT = 1
	BORDER_BOTTOM = 2
	BORDER_LEFT = 3
	
	DEFAULT_BORDER_COLOR = grp.GenerateColor(0.3, 0.3, 0.3, 1.0)
	DEFAULT_BASE_COLOR = grp.GenerateColor(0, 0, 0, 0.5)
	
	def __init__(self):
		Window.__init__(self)
		
		self.borderSize = 1
		
		# Create Borders
		self.borders = [
			Bar(),
			Bar(),
			Bar(),
			Bar()
		]
		
		for border in self.borders:
			border.SetParent(self)
			border.AddFlag("not_pick")
			border.Show()
		
		# Create Base
		self.base = Bar()
		self.base.SetParent(self)
		self.base.AddFlag("not_pick")
		self.base.Show()
		
		# Set Default Colors
		self.SetBorderColor(self.DEFAULT_BORDER_COLOR)
		self.SetBaseColor(self.DEFAULT_BASE_COLOR)
	
	def __del__(self):
		self.Destroy()
		Window.__del__(self)
	
	def Destroy(self):
		del self.borders[:]
		self.base = None
		
		Window.Destroy(self)
	
	def SetBorderColor(self, color):
		for border in self.borders:
			border.SetColor(color)
	
	def SetBorderSize(self, borderSize):
		self.borderSize = borderSize
		self.SetSize(self.GetWidth(), self.GetHeight())
	
	def SetBaseColor(self, color):
		self.base.SetColor(color)
	
	def SetSize(self, width, height):
		width = max(width, (2 * self.borderSize) + 1)
		height = max(height, (2 * self.borderSize) + 1)
		
		Window.SetSize(self, width, height)
		self.UpdateBoard()
	
	def UpdateBoard(self):
		width = self.GetWidth()
		height = self.GetHeight()
		
		top, right, bottom, left = self.borders
		
		# Top Border
		top.SetSize(width - self.borderSize, self.borderSize)
		
		# Right Border
		right.SetSize(self.borderSize, height - self.borderSize)
		right.SetPosition(width - self.borderSize, 0)
		
		# Bottom Border
		bottom.SetSize(width - self.borderSize, self.borderSize)
		bottom.SetPosition(self.borderSize, height - self.borderSize)
		
		# Left Border
		left.SetSize(self.borderSize, height - self.borderSize)
		left.SetPosition(0, self.borderSize)
		
		# Base
		self.base.SetSize(width - (2 * self.borderSize), height - (2 * self.borderSize))
		self.base.SetPosition(self.borderSize, self.borderSize)

class ListBoxEx(Window):

	class Item(Window):
		def __init__(self):
			Window.__init__(self)

		def __del__(self):
			Window.__del__(self)

		def SetParent(self, parent):
			Window.SetParent(self, parent)
			self.parent=proxy(parent)

		def OnMouseLeftButtonDown(self):
			self.parent.SelectItem(self)

		def OnRender(self):
			if self.parent.GetSelectedItem()==self:
				self.OnSelectedRender()

		def OnSelectedRender(self):
			x, y = self.GetGlobalPosition()
			grp.SetColor(grp.GenerateColor(0.0, 0.0, 0.7, 0.7))
			grp.RenderBar(x, y, self.GetWidth(), self.GetHeight())

	def __init__(self, isHorizontal = False):
		Window.__init__(self)

		self.viewItemCount=10
		self.basePos=0
		self.itemHeight=16
		self.itemStep=20
		self.selItem=0
		self.itemList=[]
		self.y_extra = 0
		self.x_extra = 0
		self.onSelectItemEvent = lambda *arg: None
		self.itemWidth=100

		self.scrollBar=None
		self.isHorizontal = isHorizontal
		self.__UpdateSize()

	def __del__(self):
		Window.__del__(self)

	def __UpdateSize(self):
		if self.isHorizontal:
			width = self.itemStep * self.__GetViewItemCount()
			self.SetSize(width, self.itemHeight)
		else:
			height = self.itemStep * self.__GetViewItemCount()
			self.SetSize(self.itemWidth, height)

	def IsEmpty(self):
		if len(self.itemList)==0:
			return 1
		return 0

	def SetItemStep(self, itemStep):
		self.itemStep=itemStep
		self.__UpdateSize()

	def SetItemSize(self, itemWidth, itemHeight):
		self.itemWidth=itemWidth
		self.itemHeight=itemHeight
		self.__UpdateSize()

	def SetViewItemCount(self, viewItemCount):
		self.viewItemCount=viewItemCount

	def SetSelectEvent(self, event):
		self.onSelectItemEvent = event

	def SetParinte(self, parent):
		self.parinte = proxy(parent)

	def SetPositionExtra(self, x, y):
		self.y_extra = y
		self.x_extra = x

	def GetItemCounts(self):
		return len(self.itemList)
		
	def GetBasePos(self):
		return self.basePos

	def SetBasePos(self, basePos):
		for oldItem in self.itemList[self.basePos:self.basePos+self.viewItemCount]:
			oldItem.Hide()

		self.basePos=basePos

		pos=basePos
		for newItem in self.itemList[self.basePos:self.basePos+self.viewItemCount]:
			(x, y)=self.GetItemViewCoord(pos, newItem.GetWidth())
			newItem.SetPosition(x + self.x_extra, y + self.y_extra)
			newItem.Show()
			pos+=1

	def GetItemIndex(self, argItem):
		return self.itemList.index(argItem)

	def GetSelectedItem(self):
		return self.selItem

	def SelectIndex(self, index):

		if index >= len(self.itemList) or index < 0:
			self.selItem = None
			return

		try:
			self.selItem=self.itemList[index]
		except:
			pass

	def SelectItem(self, selItem):
		self.selItem=selItem
		self.onSelectItemEvent(selItem)

	def RemoveAllItems(self):
		self.selItem=None
		self.itemList=[]
		
		if len(self.itemList) > 0:
			for item in self.itemList:
				item.Hide()
				item.Destroy()
				del item
		
		self.itemList=[]
		
		if self.scrollBar:
			self.scrollBar.SetPos(0)

	def RemoveAllItemsFromList(self):
		self.selItem=None
		# for xitem in xrange(len(self.itemList)): #hide items
			# try:
				# self.itemList[xitem].Hide()
				# del self.itemList[xitem]
			# except:
				# continue
		
		# self.itemList=[]

		# if self.scrollBar:
			# self.scrollBar.SetPos(0)
			
		# @Grimm
		self.RemoveAllItems()

	def GetItems(self):
		return self.itemList

	def RemoveItem(self, delItem):
		if delItem==self.selItem:
			self.selItem=None

		self.itemList.remove(delItem)

	def AppendItem(self, newItem, grimm = 0):
		if grimm == 0:
			newItem.SetParent(self)
		else:
			newItem.SetParent(self.parinte)
		newItem.SetSize(self.itemWidth, self.itemHeight)

		pos=len(self.itemList)
		if self.__IsInViewRange(pos):
			(x, y)=self.GetItemViewCoord(pos, newItem.GetWidth())
			newItem.SetPosition(x + self.x_extra, y + self.y_extra)
			newItem.Show()
		else:
			newItem.Hide()

		self.itemList.append(newItem)

	def SetScrollBar(self, scrollBar):
		scrollBar.SetScrollEvent(__mem_func__(self.__OnScroll))
		self.scrollBar=scrollBar

	def __OnScroll(self):
		self.SetBasePos(int(self.scrollBar.GetPos()*self.__GetScrollLen()))

	def __GetScrollLen(self):
		scrollLen=self.__GetItemCount()-self.__GetViewItemCount()
		if scrollLen<0:
			return 0

		return scrollLen

	def __GetViewItemCount(self):
		return self.viewItemCount

	def __GetItemCount(self):
		return len(self.itemList)

	def GetScrollLen(self):
		scrollLen=self.__GetItemCount()-self.__GetViewItemCount()
		if scrollLen<0:
			return 0

		return scrollLen

	def GetViewItemCount(self):
		return self.__GetViewItemCount()

	def GetItemCount(self):
		return self.__GetItemCount()

	def GetItemViewCoord(self, pos, itemWidth):
		if self.isHorizontal:
			return ((pos - self.basePos) * self.itemStep, 0)
		return (0, (pos - self.basePos) * self.itemStep)

	def __IsInViewRange(self, pos):
		if pos<self.basePos:
			return 0
		if pos>=self.basePos+self.viewItemCount:
			return 0
		return 1

class ListBoxExLey(Window):

	class Item(Window):
		def __init__(self):
			Window.__init__(self)

		def __del__(self):
			Window.__del__(self)

		def SetParent(self, parent):
			Window.SetParent(self, parent)
			self.parent=proxy(parent)

		def OnMouseLeftButtonDown(self):
			self.parent.SelectItem(self)

		def OnRender(self):
			if self.parent.GetSelectedItem()==self:
				self.OnSelectedRender()

		def OnSelectedRender(self):
			x, y = self.GetGlobalPosition()
			grp.SetColor(grp.GenerateColor(0.0, 0.0, 0.7, 0.7))
			grp.RenderBar(x, y, self.GetWidth(), self.GetHeight())

	def __init__(self, isHorizontal = False):
		Window.__init__(self)

		self.xPos = 0
		self.yPos = 0

		self.viewItemCount=10
		self.basePos=0
		self.itemHeight=16
		self.itemStep=20
		self.selItem=0
		self.itemList=[]
		self.onSelectItemEvent = lambda *arg: None

		self.itemWidth=100
		self.isHorizontal = isHorizontal

		self.scrollBar=None
		self.__UpdateSize()

	def __del__(self):
		Window.__del__(self)

	def __UpdateSize(self):
		if self.isHorizontal:
			width = self.itemStep * self.__GetViewItemCount()
			self.SetSize(width, self.itemHeight)
		else:
			height = self.itemStep * self.__GetViewItemCount()
			self.SetSize(self.itemWidth, height)

	def IsEmpty(self):
		if len(self.itemList)==0:
			return 1
		return 0

	def SetItemStep(self, itemStep):
		self.itemStep=itemStep
		self.__UpdateSize()
	
	def SetNewPos(self, x, y):
		self.xPos = x
		self.yPos = y
		
		self.SetPosition(x, y)
	
	def SetItemSize(self, itemWidth, itemHeight):
		self.itemWidth=itemWidth
		self.itemHeight=itemHeight
		self.__UpdateSize()

	def SetViewItemCount(self, viewItemCount):
		self.viewItemCount=viewItemCount

	def SetSelectEvent(self, event):
		self.onSelectItemEvent = event

	def SetBasePos(self, basePos):
		for oldItem in self.itemList[self.basePos:self.basePos+self.viewItemCount]:
			oldItem.Hide()

		self.basePos=basePos

		pos=basePos
		for newItem in self.itemList[self.basePos:self.basePos+self.viewItemCount]:
			(x, y)=self.GetItemViewCoord(pos, newItem.GetWidth())
			newItem.SetPosition(x + self.xPos, y + self.yPos)
			newItem.Show()
			pos+=1

	def GetItemIndex(self, argItem):
		return self.itemList.index(argItem)

	def GetSelectedItem(self):
		return self.selItem

	def SelectIndex(self, index):

		if index >= len(self.itemList) or index < 0:
			self.selItem = None
			return

		try:
			self.selItem=self.itemList[index]
		except:
			pass

	def SelectItem(self, selItem):
		self.selItem=selItem
		self.onSelectItemEvent(selItem)
		
	def RemoveAllItems(self):
		for item in self.itemList:
			item.Hide()

		self.selItem=None
		self.itemList=[]

		if self.scrollBar:
			self.scrollBar.SetPos(0)
			
	# if app.ENABLE_SWITCHBOT:
	def GetItems(self):
		return self.itemList
			
	def RemoveItem(self, delItem):
		if delItem==self.selItem:
			self.selItem=None

		self.itemList.remove(delItem)

	def AppendItem(self, newItem, hwndParent = None):
		if hwndParent:
			newItem.SetParent(hwndParent)
		else:
			newItem.SetParent(self)
		newItem.SetSize(self.itemWidth, self.itemHeight)

		pos=len(self.itemList)
		if self.__IsInViewRange(pos):
			(x, y)=self.GetItemViewCoord(pos, newItem.GetWidth())
			newItem.SetPosition(x + self.xPos, y + self.yPos)
			newItem.Show()
		else:
			newItem.Hide()

		self.itemList.append(newItem)

	def SetScrollBar(self, scrollBar):
		scrollBar.SetScrollEvent(__mem_func__(self.__OnScroll))
		self.scrollBar=scrollBar

	def __OnScroll(self):
		self.SetBasePos(int(self.scrollBar.GetPos()*self.__GetScrollLen()))

	def __GetScrollLen(self):
		scrollLen=self.__GetItemCount()-self.__GetViewItemCount()
		if scrollLen<0:
			return 0

		return scrollLen

	def __GetViewItemCount(self):
		return self.viewItemCount

	def GetCountItems(self):
		return len(self.itemList)
		
	def __GetItemCount(self):
		return len(self.itemList)

	def GetItemViewCoord(self, pos, itemWidth):
		if self.isHorizontal:
			return ((pos - self.basePos) * self.itemStep, 0)
		return (0, (pos - self.basePos) * self.itemStep)

	def __IsInViewRange(self, pos):
		if pos<self.basePos:
			return 0
		if pos>=self.basePos+self.viewItemCount:
			return 0
		return 1

if app.ENABLE_SEND_TARGET_INFO:
	class ListBoxExNew(Window):
		class Item(Window):
			def __init__(self):
				Window.__init__(self)

				self.fTimeChangeColor = 0
				self.ColorNum = 0
				self.SelectedColor = BLUE_COLOR
				self.realWidth = 0
				self.realHeight = 0

				self.removeTop = 0
				self.removeBottom = 0

				self.SetWindowName("NONAME_ListBoxExNew_Item")

			def __del__(self):
				Window.__del__(self)

			def SetParent(self, parent):
				Window.SetParent(self, parent)
				self.parent=proxy(parent)

			def SetSize(self, width, height):
				self.realWidth = width
				self.realHeight = height
				Window.SetSize(self, width, height)

			def SetRemoveTop(self, height):
				self.removeTop = height
				self.RefreshHeight()

			def SetRemoveBottom(self, height):
				self.removeBottom = height
				self.RefreshHeight()

			def SetCurrentHeight(self, height):
				Window.SetSize(self, self.GetWidth(), height)

			def GetCurrentHeight(self):
				return Window.GetHeight(self)

			def ResetCurrentHeight(self):
				self.removeTop = 0
				self.removeBottom = 0
				self.RefreshHeight()

			def RefreshHeight(self):
				self.SetCurrentHeight(self.GetHeight() - self.removeTop - self.removeBottom)

			def GetHeight(self):
				return self.realHeight

			def OnRender(self):
				if self.IsIn():
					x, y = self.GetGlobalPosition()
					grp.SetColor(self.SelectedColor)
					grp.RenderBar(x-11, y, self.GetWidth()+35, self.GetCurrentHeight())
					
					if app.GetTime() > self.fTimeChangeColor:
						self.fTimeChangeColor = float(app.GetTime()) + TIME_CHANGE_PER_COLOR
						
						if self.ColorNum == 1:
							self.SelectedColor = BLUE_COLOR_2
							self.ColorNum += 1

						elif self.ColorNum == 2:
							self.SelectedColor = BLUE_COLOR_3
							self.ColorNum += 1
							
						elif self.ColorNum == 3:
							self.SelectedColor = BLUE_COLOR_4
							self.ColorNum += 1
							
						elif self.ColorNum == 4:
							self.SelectedColor = BLUE_COLOR_5
							self.ColorNum += 1
						else:
							self.SelectedColor = BLUE_COLOR
							self.ColorNum = 1

		def __init__(self, stepSize, viewSteps):
			Window.__init__(self)

			self.viewItemCount=10
			self.basePos=0
			self.baseIndex=0
			self.maxSteps=0
			self.viewSteps = viewSteps
			self.stepSize = stepSize
			self.itemList=[]

			self.scrollBar=None

			self.SetWindowName("NONAME_ListBoxEx")

		def __del__(self):
			Window.__del__(self)

		def IsEmpty(self):
			if len(self.itemList)==0:
				return 1
			return 0

		def __CheckBasePos(self, pos):
			self.viewItemCount = 0

			start_pos = pos

			height = 0
			while height < self.GetHeight():
				if pos >= len(self.itemList):
					return start_pos == 0
				height += self.itemList[pos].GetHeight()
				pos += 1
				self.viewItemCount += 1
			return height == self.GetHeight()

		def SetBasePos(self, basePos, forceRefresh = TRUE):
			if forceRefresh == FALSE and self.basePos == basePos:
				return

			for oldItem in self.itemList[self.baseIndex:self.baseIndex+self.viewItemCount]:
				oldItem.ResetCurrentHeight()
				oldItem.Hide()

			self.basePos=basePos

			baseIndex = 0
			while basePos > 0:
				basePos -= self.itemList[baseIndex].GetHeight() / self.stepSize
				if basePos < 0:
					self.itemList[baseIndex].SetRemoveTop(self.stepSize * abs(basePos))
					break
				baseIndex += 1
			self.baseIndex = baseIndex

			stepCount = 0
			self.viewItemCount = 0
			while baseIndex < len(self.itemList):
				stepCount += self.itemList[baseIndex].GetCurrentHeight() / self.stepSize
				self.viewItemCount += 1
				if stepCount > self.viewSteps:
					self.itemList[baseIndex].SetRemoveBottom(self.stepSize * (stepCount - self.viewSteps))
					break
				elif stepCount == self.viewSteps:
					break
				baseIndex += 1

			y = 0
			for newItem in self.itemList[self.baseIndex:self.baseIndex+self.viewItemCount]:
				newItem.SetPosition(0, y)
				newItem.Show()
				y += newItem.GetCurrentHeight()

		def GetItemIndex(self, argItem):
			return self.itemList.index(argItem)

		def GetSelectedItem(self):
			return self.selItem

		def GetSelectedItemIndex(self):
			return self.selItemIdx

		def RemoveAllItems(self):
			self.itemList=[]
			self.maxSteps=0

			if self.scrollBar:
				self.scrollBar.SetPos(0)

		def RemoveItem(self, delItem):
			self.maxSteps -= delItem.GetHeight() / self.stepSize
			self.itemList.remove(delItem)

		def AppendItem(self, newItem):
			if newItem.GetHeight() % self.stepSize != 0:
				import dbg
				dbg.TraceError("Invalid AppendItem height %d stepSize %d" % (newItem.GetHeight(), self.stepSize))
				return

			self.maxSteps += newItem.GetHeight() / self.stepSize
			newItem.SetParent(self)
			self.itemList.append(newItem)

		def SetScrollBar(self, scrollBar):
			scrollBar.SetScrollEvent(__mem_func__(self.__OnScroll))
			self.scrollBar=scrollBar

		def __OnScroll(self):
			self.SetBasePos(int(self.scrollBar.GetPos()*self.__GetScrollLen()), FALSE)

		def __GetScrollLen(self):
			scrollLen=self.maxSteps-self.viewSteps
			if scrollLen<0:
				return 0

			return scrollLen

		def __GetViewItemCount(self):
			return self.viewItemCount

		def __GetItemCount(self):
			return len(self.itemList)

		def GetViewItemCount(self):
			return self.viewItemCount

		def GetItemCount(self):
			return len(self.itemList)

class CandidateListBox(ListBoxEx):

	HORIZONTAL_MODE = 0
	VERTICAL_MODE = 1

	class Item(ListBoxEx.Item):
		def __init__(self, text):
			ListBoxEx.Item.__init__(self)

			self.textBox=TextLine()
			self.textBox.SetParent(self)
			self.textBox.SetText(text)
			self.textBox.Show()

		def __del__(self):
			ListBoxEx.Item.__del__(self)

	def __init__(self, mode = HORIZONTAL_MODE):
		ListBoxEx.__init__(self)
		self.itemWidth=32
		self.itemHeight=32
		self.mode = mode

	def __del__(self):
		ListBoxEx.__del__(self)

	def SetMode(self, mode):
		self.mode = mode

	def AppendItem(self, newItem):
		ListBoxEx.AppendItem(self, newItem)

	def GetItemViewCoord(self, pos):
		if self.mode == self.HORIZONTAL_MODE:
			return ((pos-self.basePos)*self.itemStep, 0)
		elif self.mode == self.VERTICAL_MODE:
			return (0, (pos-self.basePos)*self.itemStep)

class InputField(Window):
	PATH = "d:/ymir work/ui/pattern/input_%s.tga"

	BORDER_SIZE = 1
	BASE_SIZE = 1

	L = 0
	R = 1
	T = 2
	B = 3

	def __init__(self, basePath = PATH):
		Window.__init__(self)

		self.onClickEvent = None

		self.MakeField(basePath)
		self.SetSize(0, 0)

		self.SetWindowName("NONAME_InputField")

	def __del__(self):
		Window.__del__(self)

	def MakeField(self, basePath):
		self.Lines = []
		for i in xrange(4):
			line = ExpandedImageBox()
			line.SetParent(self)
			line.LoadImage(basePath % "border")
			line.Show()
			self.Lines.append(line)

		self.Lines[self.T].SetPosition(self.BORDER_SIZE, 0)
		self.Lines[self.B].SetPosition(self.BORDER_SIZE, 0)

		self.Base = ExpandedImageBox()
		self.Base.SetParent(self)
		self.Base.SetPosition(self.BORDER_SIZE, self.BORDER_SIZE)
		self.Base.LoadImage(basePath % "base")
		self.Base.Show()

	def SetSize(self, width, height):
		minSize = self.BORDER_SIZE * 2 + self.BASE_SIZE
		width = max(minSize, width)
		height = max(minSize, height)
		Window.SetSize(self, width, height)

		scaleH = float(width - self.BORDER_SIZE * 2 - self.BORDER_SIZE) / float(self.BORDER_SIZE)
		scaleV = float(height - self.BORDER_SIZE) / float(self.BORDER_SIZE)
		self.Lines[self.L].SetRenderingRect(0, 0, 0, scaleV)
		self.Lines[self.R].SetRenderingRect(0, 0, 0, scaleV)
		self.Lines[self.T].SetRenderingRect(0, 0, scaleH, 0)
		self.Lines[self.B].SetRenderingRect(0, 0, scaleH, 0)
		self.Lines[self.R].SetPosition(width - self.BORDER_SIZE, self.Lines[self.R].GetTop())
		self.Lines[self.B].SetPosition(self.Lines[self.B].GetLeft(), height - self.BORDER_SIZE)

		scaleH = float(width - self.BORDER_SIZE * 2 - self.BASE_SIZE) / float(self.BASE_SIZE)
		scaleV = float(height - self.BORDER_SIZE * 2 - self.BASE_SIZE) / float(self.BASE_SIZE)
		self.Base.SetRenderingRect(0, 0, scaleH, scaleV)

	def SetAlpha(self, alpha):
		for line in self.Lines:
			line.SetAlpha(alpha)
		self.Base.SetAlpha(alpha)

	def SetEvent(self, event):
		self.onClickEvent = event

	def OnMouseLeftButtonDown(self):
		if self.onClickEvent:
			self.onClickEvent()

class TextLine(Window):
	def __init__(self):
		Window.__init__(self)
		self.max = 0
		self.BonusId = 0
		self.SetFontName(localeInfo.UI_DEF_FONT)

	def __del__(self):
		Window.__del__(self)

	def RegisterWindow(self, layer):
		self.hWnd = wndMgr.RegisterTextLine(self, layer)

	def GetRenderPos(self):
		return wndMgr.GetRenderPos(self.hWnd)

	def SetFixedRenderPos(self, startPos, endPos):
		wndMgr.SetFixedRenderPos(self.hWnd, startPos, endPos)

	def SetMax(self, max):
		wndMgr.SetMax(self.hWnd, max)

	def SetLimitWidth(self, width):
		wndMgr.SetLimitWidth(self.hWnd, width)

	def SetMultiLine(self):
		wndMgr.SetMultiLine(self.hWnd, True)

	def SetHorizontalAlignArabic(self):
		wndMgr.SetHorizontalAlign(self.hWnd, wndMgr.TEXT_HORIZONTAL_ALIGN_ARABIC)

	def SetHorizontalAlignLeft(self):
		wndMgr.SetHorizontalAlign(self.hWnd, wndMgr.TEXT_HORIZONTAL_ALIGN_LEFT)

	def SetHorizontalAlignRight(self):
		wndMgr.SetHorizontalAlign(self.hWnd, wndMgr.TEXT_HORIZONTAL_ALIGN_RIGHT)

	def SetHorizontalAlignCenter(self):
		wndMgr.SetHorizontalAlign(self.hWnd, wndMgr.TEXT_HORIZONTAL_ALIGN_CENTER)

	def SetVerticalAlignTop(self):
		wndMgr.SetVerticalAlign(self.hWnd, wndMgr.TEXT_VERTICAL_ALIGN_TOP)

	def SetVerticalAlignBottom(self):
		wndMgr.SetVerticalAlign(self.hWnd, wndMgr.TEXT_VERTICAL_ALIGN_BOTTOM)

	def SetVerticalAlignCenter(self):
		wndMgr.SetVerticalAlign(self.hWnd, wndMgr.TEXT_VERTICAL_ALIGN_CENTER)

	def SetSecret(self, Value=True):
		wndMgr.SetSecret(self.hWnd, Value)
		
	def SetTextColor(self, color):
		self.SetPackedFontColor(color)
		
	def SetBonusId(self, bnsId):
		self.BonusId = bnsId

	def GetBonusId(self):
		if self.BonusId != 0:
			return self.BonusId
			
	def SetOutline(self, Value=True):
		wndMgr.SetOutline(self.hWnd, Value)

	def SetFeather(self, value=True):
		wndMgr.SetFeather(self.hWnd, value)

	def SetFontName(self, fontName):
		wndMgr.SetFontName(self.hWnd, fontName)
		
	if app.WJ_MULTI_TEXTLINE:
		def SetEnterToken(self, bool):
			wndMgr.SetEnterToken(self.hWnd, bool)
			
	def SetDefaultFontName(self):
		wndMgr.SetFontName(self.hWnd, localeInfo.UI_DEF_FONT)

	def SetFontColor(self, red, green, blue):
		wndMgr.SetFontColor(self.hWnd, red, green, blue)

	def SetPackedFontColor(self, color):
		wndMgr.SetFontColor(self.hWnd, color)
		
	def SetOutLineColor(self, red, green, blue, alpha):
		wndMgr.SetOutLineColor(self.hWnd, red, green, blue, alpha)

	def SetPackedOutLineColor(self, color):
		wndMgr.SetOutLineColor(self.hWnd, color)
		
	def SetText(self, text):
		wndMgr.SetText(self.hWnd, text)

	def GetText(self):
		return wndMgr.GetText(self.hWnd)

	def GetTextSize(self):
		return wndMgr.GetTextSize(self.hWnd)

	def GetTextWidth(self):
		(w, h) = self.GetTextSize()
		return w

	def GetTextHeight(self):
		(w, h) = self.GetTextSize()
		return h
		
	def AdjustSize(self):
		x, y = self.GetTextSize()
		wndMgr.SetWindowSize(self.hWnd, x, y)

	def GetRight(self):
		return self.GetLeft() + self.GetTextWidth()

	def GetBottom(self):
		return self.GetTop() + self.GetTextHeight()

	def SetCenter(self):
		wndMgr.SetWindowPosition(self.hWnd, self.GetLeft() - self.GetTextWidth()/2, self.GetTop())
		
class EmptyCandidateWindow(Window):
	def __init__(self):
		Window.__init__(self)

	def __del__(self):
		Window.__del__(self)

	def Load(self):
		pass

	def SetCandidatePosition(self, x, y, textCount):
		pass

	def Clear(self):
		pass

	def Append(self, text):
		pass

	def Refresh(self):
		pass

	def Select(self):
		pass

class EditLine(TextLine):
	candidateWindowClassDict = {}

	def __init__(self):
		TextLine.__init__(self)

		self.eventReturn = Window.NoneMethod
		self.eventEscape = Window.NoneMethod
		self.eventTab = None
		self.numberMode = False
		self.useIME = True
		self.CanClick = None
		self.bCodePage = False
		self.userMax = 0
		
		self.candidateWindowClass = None
		self.candidateWindow = None
		self.SetCodePage(app.GetDefaultCodePage())

		self.readingWnd = ReadingWnd()
		self.readingWnd.Hide()

		self.SelectedItemVnum = 0

	def __del__(self):
		TextLine.__del__(self)

		self.eventReturn = Window.NoneMethod
		self.eventEscape = Window.NoneMethod
		self.eventTab = None
		self.CanClick = None

	def SetCodePage(self, codePage):
		candidateWindowClass=EditLine.candidateWindowClassDict.get(codePage, EmptyCandidateWindow)
		self.__SetCandidateClass(candidateWindowClass)

	def __SetCandidateClass(self, candidateWindowClass):
		if self.candidateWindowClass==candidateWindowClass:
			return

		self.candidateWindowClass = candidateWindowClass
		self.candidateWindow = self.candidateWindowClass()
		self.candidateWindow.Load()
		self.candidateWindow.Hide()

	def RegisterWindow(self, layer):
		self.hWnd = wndMgr.RegisterTextLine(self, layer)

	def SAFE_SetReturnEvent(self, event):
		self.eventReturn = __mem_func__(event)

	def SetReturnEvent(self, event):
		self.eventReturn = event

	def SetEscapeEvent(self, event):
		self.eventEscape = event

	def SetTabEvent(self, event):
		self.eventTab = event

	def SetMax(self, max):
		self.max = max
		wndMgr.SetMax(self.hWnd, self.max)
		ime.SetMax(self.max)
		self.SetUserMax(self.max)

	def SetUserMax(self, max):
		self.userMax = max
		ime.SetUserMax(self.userMax)

	def SetNumberMode(self):
		self.numberMode = True

	#def AddExceptKey(self, key):
	#	ime.AddExceptKey(key)

	#def ClearExceptKey(self):
	#	ime.ClearExceptKey()

	def SetIMEFlag(self, flag):
		self.useIME = flag

	def CanEdit(self, flag):
		self.CanClick = flag

	def SetText(self, text):
		wndMgr.SetText(self.hWnd, text)

		if self.IsFocus():
			ime.SetText(text)

	def Enable(self):
		wndMgr.ShowCursor(self.hWnd)

	def Disable(self):
		wndMgr.HideCursor(self.hWnd)

	def SetEndPosition(self):
		ime.MoveEnd()

	def OnSetFocus(self):
		Text = self.GetText()
		ime.SetText(Text)
		ime.SetMax(self.max)
		ime.SetUserMax(self.userMax)
		ime.SetCursorPosition(-1)
		if self.numberMode:
			ime.SetNumberMode()
		else:
			ime.SetStringMode()
		ime.EnableCaptureInput()
		if self.useIME:
			ime.EnableIME()
		else:
			ime.DisableIME()
		wndMgr.ShowCursor(self.hWnd, True)

	def OnKillFocus(self):
		self.SetText(ime.GetText(self.bCodePage))
		self.OnIMECloseCandidateList()
		self.OnIMECloseReadingWnd()
		ime.DisableIME()
		ime.DisableCaptureInput()
		wndMgr.HideCursor(self.hWnd)

	def OnIMEChangeCodePage(self):
		self.SetCodePage(ime.GetCodePage())

	def OnIMEOpenCandidateList(self):
		self.candidateWindow.Show()
		self.candidateWindow.Clear()
		self.candidateWindow.Refresh()

		gx, gy = self.GetGlobalPosition()
		self.candidateWindow.SetCandidatePosition(gx, gy, len(self.GetText()))

		return True

	def OnIMECloseCandidateList(self):
		self.candidateWindow.Hide()
		return True

	def OnIMEOpenReadingWnd(self):
		gx, gy = self.GetGlobalPosition()
		textlen = len(self.GetText())-2
		reading = ime.GetReading()
		readinglen = len(reading)
		self.readingWnd.SetReadingPosition( gx + textlen*6-24-readinglen*6, gy )
		self.readingWnd.SetText(reading)
		if ime.GetReadingError() == 0:
			self.readingWnd.SetTextColor(0xffffffff)
		else:
			self.readingWnd.SetTextColor(0xffff0000)
		self.readingWnd.SetSize(readinglen * 6 + 4, 19)
		self.readingWnd.Show()
		return True

	def OnIMECloseReadingWnd(self):
		self.readingWnd.Hide()
		return True

	def OnIMEUpdate(self):
		TextLine.SetText(self, ime.GetText(self.bCodePage))

	def OnIMETab(self):
		if self.eventTab:
			self.eventTab()
			return True

		return False

	def OnIMEReturn(self):
		self.eventReturn()

		return True

	def OnPressEscapeKey(self):
		self.eventEscape()
		return True

	def OnKeyDown(self, key):
		if app.DIK_F1 == key:
			return False
		if app.DIK_F2 == key:
			return False
		if app.DIK_F3 == key:
			return False
		if app.DIK_F4 == key:
			return False
		if app.DIK_LALT == key:
			return False
		if app.DIK_SYSRQ == key:
			return False
		if app.DIK_LCONTROL == key:
			return False
		if app.DIK_V == key:
			if app.IsPressed(app.DIK_LCONTROL):
				ime.PasteTextFromClipBoard()

		return True

	def OnKeyUp(self, key):
		if app.DIK_F1 == key:
			return False
		if app.DIK_F2 == key:
			return False
		if app.DIK_F3 == key:
			return False
		if app.DIK_F4 == key:
			return False
		if app.DIK_LALT == key:
			return False
		if app.DIK_SYSRQ == key:
			return False
		if app.DIK_LCONTROL == key:
			return False

		return True

	def OnIMEKeyDown(self, key):
		# Left
		if app.VK_LEFT == key:
			ime.MoveLeft()
			return True
		# Right
		if app.VK_RIGHT == key:
			ime.MoveRight()
			return True

		# Up
		if app.VK_UP == key:
			if self.eventUpArrow:
				self.eventUpArrow()
				return TRUE
		# Down
		if app.VK_DOWN == key:
			if self.eventDownArrow:
				self.eventDownArrow()
				return TRUE

		# Home
		if app.VK_HOME == key:
			ime.MoveHome()
			return True
		# End
		if app.VK_END == key:
			ime.MoveEnd()
			return True

		# Delete
		if app.VK_DELETE == key:
			ime.Delete()
			TextLine.SetText(self, ime.GetText(self.bCodePage))
			return True

		return True

	#def OnMouseLeftButtonDown(self):
	#	self.SetFocus()
	def OnMouseLeftButtonDown(self):
		if False == self.IsIn():
			return False

		self.SetFocus()
		PixelPosition = wndMgr.GetCursorPosition(self.hWnd)
		ime.SetCursorPosition(PixelPosition)

class MarkBox(Window):
	def __init__(self, layer = "UI"):
		Window.__init__(self, layer)

	def __del__(self):
		Window.__del__(self)

	def RegisterWindow(self, layer):
		self.hWnd = wndMgr.RegisterMarkBox(self, layer)

	def Load(self):
		wndMgr.MarkBox_Load(self.hWnd)

	def SetScale(self, scale):
		wndMgr.MarkBox_SetScale(self.hWnd, scale)

	def SetIndex(self, guildID):
		MarkID = guild.GuildIDToMarkID(guildID)
		wndMgr.MarkBox_SetImageFilename(self.hWnd, guild.GetMarkImageFilenameByMarkID(MarkID))
		wndMgr.MarkBox_SetIndex(self.hWnd, guild.GetMarkIndexByMarkID(MarkID))

	def SetAlpha(self, alpha):
		wndMgr.MarkBox_SetDiffuseColor(self.hWnd, 1.0, 1.0, 1.0, alpha)

class ImageBox(Window):
	def __init__(self, layer = "UI"):
		Window.__init__(self, layer)
		
		self.eventDict = {
			"MOUSE_LEFT_BUTTON_UP" : None, 
			"MOUSE_LEFT_BUTTON_DOWN" : None, 
			"MOUSE_RIGHT_BUTTON_UP" : None, 
			"MOUSE_RIGHT_BUTTON_DOWN" : None, 
			"MOUSE_OVER_IN" : None, 
			"MOUSE_OVER_OUT" : None
		}

		self.eventFunc = {
			"MOUSE_LEFT_BUTTON_UP" : None, 
			"MOUSE_LEFT_BUTTON_DOWN" : None, 
			"MOUSE_RIGHT_BUTTON_UP" : None, 
			"MOUSE_RIGHT_BUTTON_DOWN" : None, 
			"MOUSE_OVER_IN" : None, 
			"MOUSE_OVER_OUT" : None
		}
		self.eventArgs = {
			"MOUSE_LEFT_BUTTON_UP" : None, 
			"MOUSE_LEFT_BUTTON_DOWN" : None, 
			"MOUSE_RIGHT_BUTTON_UP" : None, 
			"MOUSE_RIGHT_BUTTON_DOWN" : None, 
			"MOUSE_OVER_IN" : None, 
			"MOUSE_OVER_OUT" : None
		}
		
	def __del__(self):
		Window.__del__(self)	
		self.eventFunc = None
		self.eventArgs = None

	def RegisterWindow(self, layer):
		self.hWnd = wndMgr.RegisterImageBox(self, layer)

	def LoadImage(self, imageName):
		self.name=imageName
		wndMgr.LoadImage(self.hWnd, imageName)

	def UnloadImage(self):
		wndMgr.UnloadImage(self.hWnd)
		
	def SetScale(self, xScale, yScale):
		wndMgr.SetScale(self.hWnd, xScale, yScale)
		
	def SetAlpha(self, alpha):
		wndMgr.SetDiffuseColor(self.hWnd, 1.0, 1.0, 1.0, alpha)
		
	def SetColor(self, r, g, b, a):
		wndMgr.SetDiffuseColor(self.hWnd, r, g, b, a)

	def SetImageSize(self,w,h):
		wndMgr.SetImageSize(self.hWnd,w,h)

	def GetWidth(self):
		return wndMgr.GetWidth(self.hWnd)
			
	def GetHeight(self):
		return wndMgr.GetHeight(self.hWnd)
		
	def SetEvent(self, func, *args) :
		result = self.eventFunc.has_key(args[0])		
		if result :
			self.eventFunc[args[0]] = func
			self.eventArgs[args[0]] = args
		else :
			print "[ERROR] ui.py SetEvent, Can`t Find has_key : %s" % args[0]
			
	def SAFE_SetEvent(self, func, *args):
		result = self.eventFunc.has_key(args[0])		
		if result :
			self.eventFunc[args[0]] = __mem_func__(func)
			self.eventArgs[args[0]] = args
		else :
			print "[ERROR] ui.py SAFE_SetEvent, Can`t Find has_key : %s" % args[0]

	def OnMouseLeftButtonUp(self):
		if self.eventFunc["MOUSE_LEFT_BUTTON_UP"] :
			apply(self.eventFunc["MOUSE_LEFT_BUTTON_UP"], self.eventArgs["MOUSE_LEFT_BUTTON_UP"])
		if self.eventDict["MOUSE_LEFT_BUTTON_UP"]:
			apply(self.eventDict["MOUSE_LEFT_BUTTON_UP"], self.eventArgs["MOUSE_LEFT_BUTTON_UP"])
			
	def OnMouseLeftButtonDown(self):
		if self.eventFunc["MOUSE_LEFT_BUTTON_DOWN"] :
			apply(self.eventFunc["MOUSE_LEFT_BUTTON_DOWN"], self.eventArgs["MOUSE_LEFT_BUTTON_DOWN"])
		if self.eventDict["MOUSE_LEFT_BUTTON_DOWN"]:
			apply(self.eventDict["MOUSE_LEFT_BUTTON_DOWN"], self.eventArgs["MOUSE_LEFT_BUTTON_DOWN"])

	def OnMouseRightButtonUp(self):
		if self.eventFunc["MOUSE_RIGHT_BUTTON_UP"] :
			apply(self.eventFunc["MOUSE_RIGHT_BUTTON_UP"], self.eventArgs["MOUSE_RIGHT_BUTTON_UP"])
		if self.eventDict["MOUSE_RIGHT_BUTTON_UP"]:
			apply(self.eventDict["MOUSE_RIGHT_BUTTON_UP"], self.eventArgs["MOUSE_RIGHT_BUTTON_UP"])
			
	def OnMouseRightButtonDown(self):
		if self.eventFunc["MOUSE_RIGHT_BUTTON_DOWN"] :
			apply(self.eventFunc["MOUSE_RIGHT_BUTTON_DOWN"], self.eventArgs["MOUSE_RIGHT_BUTTON_DOWN"])
		if self.eventDict["MOUSE_RIGHT_BUTTON_DOWN"]:
			apply(self.eventDict["MOUSE_RIGHT_BUTTON_DOWN"], self.eventArgs["MOUSE_RIGHT_BUTTON_DOWN"])
			
	def OnMouseOverIn(self) :
		if self.eventFunc["MOUSE_OVER_IN"] :
			apply(self.eventFunc["MOUSE_OVER_IN"], self.eventArgs["MOUSE_OVER_IN"])
		if self.eventDict["MOUSE_OVER_IN"]:
			apply(self.eventDict["MOUSE_OVER_IN"], self.eventArgs["MOUSE_OVER_IN"])

	def OnMouseOverOut(self) :
		if self.eventFunc["MOUSE_OVER_OUT"] :
			apply(self.eventFunc["MOUSE_OVER_OUT"], self.eventArgs["MOUSE_OVER_OUT"])
			
		if self.eventDict["MOUSE_OVER_OUT"]:
			apply(self.eventDict["MOUSE_OVER_OUT"], self.eventArgs["MOUSE_OVER_OUT"])
			
	def SAFE_SetStringEvent(self, event, func, *args):
		self.eventDict[event]=__mem_func__(func)
		self.eventArgs[event]=args


	def SetCoolTime(self, time):
		wndMgr.SetCoolTimeImageBox(self.hWnd, time)

	def SetStartCoolTime(self, time):
		wndMgr.SetStartCoolTimeImageBox(self.hWnd, time)
 # you can use this class, i think it should work
class ImageBox2(Window):
	def __init__(self, layer = "UI"):
		Window.__init__(self, layer)

		self.name=""
		self.eventDict={}
		self.eventFunc = {"mouse_click" : None, "mouse_over_in" : None, "mouse_over_out" : None}
		self.eventArgs = {"mouse_click" : None, "mouse_over_in" : None, "mouse_over_out" : None}
		self.argDict={}

	def __del__(self):
		Window.__del__(self)

	def RegisterWindow(self, layer):
		self.hWnd = wndMgr.RegisterImageBox(self, layer)

	def LoadImage(self, imageName):
		self.name=imageName
		return wndMgr.LoadImage(self.hWnd, imageName)

	def GetImageName(self):
		return self.name

	def SetAlpha(self, alpha):
		wndMgr.SetDiffuseColor(self.hWnd, 1.0, 1.0, 1.0, alpha)

	def GetWidth(self):
		return wndMgr.GetWidth(self.hWnd)

	def GetHeight(self):
		return wndMgr.GetHeight(self.hWnd)

	def ForceRender(self):
		wndMgr.ImageForceRender(self.hWnd)

	def OnMouseLeftButtonUp(self):
		try:
			apply(self.eventDict["MOUSE_LEFT_UP"], self.argDict["MOUSE_LEFT_UP"])
		except KeyError:
			pass

	def OnMouseLeftButtonDown(self):
		try:
			apply(self.eventDict["MOUSE_LEFT_DOWN"], self.argDict["MOUSE_LEFT_DOWN"])
		except KeyError:
			pass

	def SAFE_SetStringEvent(self, event, func, *args):
		self.eventDict[event]=__mem_func__(func)
		self.argDict[event]=args

	def SAFE_SetMouseClickEvent(self, func, *args):
		self.eventDict["MOUSE_LEFT_DOWN"]=__mem_func__(func)
		self.argDict["MOUSE_LEFT_DOWN"]=args
		
	def SetEvent(self, func, *args) :
		result = self.eventFunc.has_key(args[0])		
		if result :
			self.eventFunc[args[0]] = func
			self.eventArgs[args[0]] = args
		else :
			print "[ERROR] ui.py SetEvent, Can`t Find has_key : %s" % args[0]

	def OnMouseOverIn(self) :
		if self.eventFunc["mouse_over_in"] :
			apply(self.eventFunc["mouse_over_in"], self.eventArgs["mouse_over_in"])
		else:
			try:
				self.eventDict["MOUSE_OVER_IN"]()
			except KeyError:
				pass

	def OnMouseOverOut(self) :
		if self.eventFunc["mouse_over_out"] :
			apply(self.eventFunc["mouse_over_out"], self.eventArgs["mouse_over_out"])
		else :
			try:
				self.eventDict["MOUSE_OVER_OUT"]()
			except KeyError:
				pass

class ImageBoxSkillTree(Window):
	def __init__(self, layer = "UI"):
		Window.__init__(self, layer)

		self.r = 1.0
		self.g = 1.0
		self.b = 1.0
		self.alpha = 1.0

		self.eventDict = {}
		self.argsDict={}

	def __del__(self):
		Window.__del__(self)

	def RegisterWindow(self, layer):
		self.hWnd = wndMgr.RegisterImageBox(self, layer)

	def LoadImage(self, imageName):
		self.name=imageName
		wndMgr.LoadImage(self.hWnd, imageName)

		if len(self.eventDict)!=0:
			print "LOAD IMAGE", self, self.eventDict

	def SetAlpha(self, alpha):
		wndMgr.SetDiffuseColor(self.hWnd, 1.0, 1.0, 1.0, alpha)

	def SetRenderingRect(self, left, top, right, bottom):
		wndMgr.SetRenderingRect(self.hWnd, left, top, right, bottom)

	def SetPercentage(self, curValue, maxValue):
		if maxValue:
			self.SetRenderingRect(0.0, 0.0, -1.0 + float(curValue) / float(maxValue), 0.0)
		else:
			self.SetRenderingRect(0.0, 0.0, 0.0, 0.0)

	def SetRGB(self, r, g, b):
		self.r = float(r)
		self.g = float(g)
		self.b = float(b)
		wndMgr.SetDiffuseColor(self.hWnd, float(r), float(g), float(b), self.alpha)

	def GetWidth(self):
		return wndMgr.GetWidth(self.hWnd)

	def GetHeight(self):
		return wndMgr.GetHeight(self.hWnd)

	def OnMouseOverIn(self):
		try:
			if self.eventDict["MOUSE_OVER_IN"]:
				apply(self.eventDict["MOUSE_OVER_IN"], self.argsDict["MOUSE_OVER_IN"])
		except KeyError:
			pass

	def OnMouseOverOut(self):
		try:
			self.eventDict["MOUSE_OVER_OUT"]()
		except KeyError:
			pass

	def SAFE_SetStringEvent(self, event, func,isa=FALSE):
		if not isa:
			self.eventDict[event]=__mem_func__(func)
		else:
			self.eventDict[event]=func
			

	def SetMouseOverInEvent(self, func, *args):
		self.eventDict["MOUSE_OVER_IN"]=__mem_func__(func)
		self.argsDict["MOUSE_OVER_IN"]=args

	def SetMouseOverOutEvent(self, func, *args):
		self.eventDict["MOUSE_OVER_OUT"]=__mem_func__(func)
		self.argsDict["MOUSE_OVER_OUT"]=args

	def SetMouseClickEvent(self, event, *args):
		self.eventDict["MOUSE_BUTTON_DOWN"]=__mem_func__(event)
		self.argsDict["MOUSE_BUTTON_DOWN"]=args

	def SetMouseButtonUpEvent(self, event, *args):
		self.eventDict["MOUSE_BUTTON_UP"]=__mem_func__(event)
		self.argsDict["MOUSE_BUTTON_UP"]=args

	def SetMouseRightClickEvent(self, func, *args):
		self.eventDict["MOUSE_RIGHT_BUTTON_DOWN"]=__mem_func__(func)
		self.argsDict["MOUSE_RIGHT_BUTTON_DOWN"]=args

	def SetMouseLeftClickEvent(self, func, *args):
		self.eventDict["MOUSE_BUTTON_DOWN"]=__mem_func__(func)
		self.argsDict["MOUSE_BUTTON_DOWN"]=args

	def SetMouseDoubleClickEvent(self, func, *args):
		self.eventDict["MOUSE_DOUBLE_CLICK_EVENT"]=__mem_func__(func)
		self.argsDict["MOUSE_DOUBLE_CLICK_EVENT"]=args

	def OnMouseLeftButtonDown(self):
		try:
			if self.eventDict["MOUSE_BUTTON_DOWN"]:
				apply(self.eventDict["MOUSE_BUTTON_DOWN"], self.argsDict["MOUSE_BUTTON_DOWN"])
		except KeyError:
			pass

	def OnMouseLeftButtonUp(self):
		try:
			if self.eventDict["MOUSE_BUTTON_UP"]:
				apply(self.eventDict["MOUSE_BUTTON_UP"], self.argsDict["MOUSE_BUTTON_UP"])
		except KeyError:
			pass

	def OnMouseRightButtonDown(self):
		try:
			if self.eventDict["MOUSE_RIGHT_BUTTON_DOWN"]:
				apply(self.eventDict["MOUSE_RIGHT_BUTTON_DOWN"], self.argsDict["MOUSE_RIGHT_BUTTON_DOWN"])
		except KeyError:
			pass

	def GetText(self):
		return "a"

	def OnMouseLeftButtonDown(self):
		try:
			if self.eventDict["MOUSE_BUTTON_DOWN"]:
				apply(self.eventDict["MOUSE_BUTTON_DOWN"], self.argsDict["MOUSE_BUTTON_DOWN"])
		except KeyError:
			pass
			
	def OnMouseLeftButtonDoubleClick(self):
		try:
			if self.eventDict["MOUSE_DOUBLE_CLICK_EVENT"]:
				apply(self.eventDict["MOUSE_DOUBLE_CLICK_EVENT"], self.argsDict["MOUSE_DOUBLE_CLICK_EVENT"])
		except KeyError:
			pass

class ExpandedImageBox(ImageBox):
	def __init__(self, layer = "UI"):
		ImageBox.__init__(self, layer)
		self.xScaleImage = 0
		self.yScaleImage = 0

	def __del__(self):
		ImageBox.__del__(self)

	def RegisterWindow(self, layer):
		self.hWnd = wndMgr.RegisterExpandedImageBox(self, layer)

	def SetScale(self, xScale, yScale, IsTemporary = False):
		if not IsTemporary:
			self.xScaleImage = xScale
			self.yScaleImage = yScale
	
		wndMgr.SetScale(self.hWnd, xScale, yScale)

	def SetOrigin(self, x, y):
		wndMgr.SetOrigin(self.hWnd, x, y)

	def SetRotation(self, rotation):
		wndMgr.SetRotation(self.hWnd, rotation)

	def SetRenderingMode(self, mode):
		wndMgr.SetRenderingMode(self.hWnd, mode)

	# [0.0, 1.0] 사이의 값만큼 퍼센트로 그리지 않는다.
	def SetRenderingRect(self, left, top, right, bottom):
		wndMgr.SetRenderingRect(self.hWnd, left, top, right, bottom)

	# if app.ENABLE_IMAGE_CLIP_RECT:
	def SetClipRect(self, left, top, right, bottom, isVertical = False):
		wndMgr.SetClipRect(self.hWnd, left, top, right, bottom, isVertical)

	def SetPercentage(self, curValue, maxValue):
		if maxValue:
			self.SetRenderingRect(0.0, 0.0, -1.0 + float(curValue) / float(maxValue), 0.0)
		else:
			self.SetRenderingRect(0.0, 0.0, 0.0, 0.0)

	def GetWidth(self):
		return wndMgr.GetWindowWidth(self.hWnd)

	def GetHeight(self):
		return wndMgr.GetWindowHeight(self.hWnd)

class ExpandedImageBoxAnim(ImageBox):

	ANIMATION_DIRECTION_RIGHT = 0
	ANIMATION_DIRECTION_LEFT = 1

	def __init__(self, layer = "UI"):
		ImageBox.__init__(self, layer)

		self.isAnimated = False
		self.animationDuration = 0
		self.animationDurationCounter = 0
		self.animationIndex = 0
		self.animationDirection = self.ANIMATION_DIRECTION_RIGHT

		self.baseX = 0
		self.baseY = 0

		self.isScalingOverTime = False
		self.xScaleStart = 0
		self.xScaleEnd = 0
		self.yScaleStart = 0
		self.yScaleEnd = 0
		self.scaleTimeStart = 0
		self.scaleTimeDur = 0

		self.SetWindowName("NONAME_ExpandedImageBox")

	def __del__(self):
		ImageBox.__del__(self)

	def SetClipRect(self, left, top, right, bottom, isVertical = False):
		wndMgr.SetClipRect(self.hWnd, left, top, right, bottom, isVertical)

	def RegisterWindow(self, layer):
		self.hWnd = wndMgr.RegisterExpandedImageBox(self, layer)

	def SetAnimationDirectionRight(self):
		self.animationDirection = self.ANIMATION_DIRECTION_RIGHT

	def SetAnimationDirectionLeft(self):
		self.animationDirection = self.ANIMATION_DIRECTION_LEFT

	def SetPosition(self, x, y):
		ImageBox.SetPosition(self, x, y)

		self.baseX = x
		self.baseY = y

	def SetScale(self, xScale, yScale):
		wndMgr.SetScale(self.hWnd, xScale, yScale)

	def SetScaleOverTime(self, xScaleStart, xScaleEnd, yScaleStart, yScaleEnd, time):
		self.isScalingOverTime = True
		self.xScaleStart = xScaleStart
		self.xScaleEnd = xScaleEnd
		self.yScaleStart = yScaleStart
		self.yScaleEnd = yScaleEnd
		self.scaleTimeStart = app.GetTime()
		self.scaleTimeDur = float(time)
		self.SetScale(xScaleStart, yScaleStart)

	def SetOrigin(self, x, y):
		wndMgr.SetOrigin(self.hWnd, x, y)

	def SetRotation(self, rotation):
		wndMgr.SetRotation(self.hWnd, rotation)

	def SetRenderingMode(self, mode):
		wndMgr.SetRenderingMode(self.hWnd, mode)

	# [0.0, 1.0] 사이의 값만큼 퍼센트로 그리지 않는다.
	def SetRenderingRect(self, left, top, right, bottom):
		wndMgr.SetRenderingRect(self.hWnd, left, top, right, bottom)

	def SetExpandedRenderingRect(self, left_top, left_bottom, top_left, top_right, right_top, right_bottom, bottom_left, bottom_right):
		wndMgr.SetExpandedRenderingRect(self.hWnd, left_top, left_bottom, top_left, top_right, right_top, right_bottom, bottom_left, bottom_right)

	def SetTextureRenderingRect(self, left, top, right, bottom):
		wndMgr.SetRenderingRect(self.hWnd, left, top, right, bottom)

	def SetPercentage(self, curValue, maxValue):
		if maxValue:
			self.SetRenderingRect(0.0, 0.0, -1.0 + float(curValue) / float(maxValue), 0.0)
		else:
			self.SetRenderingRect(0.0, 0.0, 0.0, 0.0)

	def SetVPercentage(self, curValue, maxValue):
		if maxValue:
			self.SetRenderingRect(0.0, -1.0 + float(curValue) / float(maxValue), 0.0, 0.0)
		else:
			self.SetRenderingRect(0.0, 0.0, 0.0, 0.0)

	def SetAnimated(self, duration):
		if duration > 0:
			self.isAnimated = True
			self.animationDuration = duration
			self.animationDurationCounter = 0
			self.animationIndex = 0
			self.OnUpdate()
		else:
			self.isAnimated = False

	def OnUpdate(self):
		if self.isAnimated == True:
			aniIndex = self.animationIndex

			self.animationDurationCounter += 1
			if self.animationDurationCounter >= self.animationDuration:
				self.animationDurationCounter = 0

				self.animationIndex += 1
				if self.animationIndex >= self.GetWidth():
					self.animationIndex = 0

			if self.GetWidth() > 0:
				if self.animationDirection == self.ANIMATION_DIRECTION_RIGHT:
					self.SetTextureRenderingRect((float(aniIndex) / float(self.GetWidth())), 0.0, -(float(aniIndex) / float(self.GetWidth())), 0.0)
				else:
					self.SetTextureRenderingRect(-(float(aniIndex) / float(self.GetWidth())), 0.0, (float(aniIndex) / float(self.GetWidth())), 0.0)

		if self.isScalingOverTime:
			perc = (app.GetTime() - self.scaleTimeStart) / float(self.scaleTimeDur)
			if perc >= 1.0:
				self.SetScale(self.xScaleEnd, self.yScaleEnd)
				self.isScalingOverTime = False
			else:
				self.SetScale(self.xScaleStart + (self.xScaleEnd - self.xScaleStart) * perc, self.yScaleStart + (self.yScaleEnd - self.yScaleStart) * perc)
			self.UpdateRect()

class CheckBox(Window):
	def __init__(self):
		Window.__init__(self)

		self.backgroundImage = None
		self.checkImage = None

		self.eventFunc = { "ON_CHECK" : None, "ON_UNCKECK" : None, }
		self.eventArgs = { "ON_CHECK" : None, "ON_UNCKECK" : None, }

		self.CreateElements()

	def __del__(self):
		Window.__del__(self)

		self.backgroundImage = None
		self.checkImage = None

		self.eventFunc = { "ON_CHECK" : None, "ON_UNCKECK" : None, }
		self.eventArgs = { "ON_CHECK" : None, "ON_UNCKECK" : None, }
	
	def CreateElements(self):
		self.backgroundImage = ImageBox()
		self.backgroundImage.SetParent(self)
		self.backgroundImage.AddFlag("not_pick")
		self.backgroundImage.LoadImage("d:/ymir work/ui/game/stats_board/checkbox_new_unselected.tga")
		self.backgroundImage.Show()

		self.checkImage = ImageBox()
		self.checkImage.SetParent(self)
		self.checkImage.AddFlag("not_pick")
		self.checkImage.SetPosition(0, -4)
		self.checkImage.LoadImage("d:/ymir work/ui/game/stats_board/checkbox_new_selected.tga")
		self.checkImage.Hide()

		self.textInfo = TextLine()
		self.textInfo.SetParent(self)
		self.textInfo.SetPosition(20, -2)
		self.textInfo.Show()

		self.SetSize(self.backgroundImage.GetWidth() + self.textInfo.GetTextSize()[0], self.backgroundImage.GetHeight() + self.textInfo.GetTextSize()[1])

	def SetTextInfo(self, info):
		if self.textInfo:
			self.textInfo.SetText(info)

		self.SetSize(self.backgroundImage.GetWidth() + self.textInfo.GetTextSize()[0], self.backgroundImage.GetHeight() + self.textInfo.GetTextSize()[1])

	def SetCheckStatus(self, flag):
		if flag:
			self.checkImage.Show()
		else:
			self.checkImage.Hide()

	def GetCheckStatus(self):
		if self.checkImage:
			return self.checkImage.IsShow()

		return False

	def SetEvent(self, func, *args) :
		result = self.eventFunc.has_key(args[0])
		if result:
			self.eventFunc[args[0]] = func
			self.eventArgs[args[0]] = args
		else:
			print "[ERROR] ui.py SetEvent, Can`t Find has_key : %s" % args[0]

	def SetBaseCheckImage(self, image):
		if not self.backgroundImage:
			return
		
		self.backgroundImage.LoadImage(image)

	def OnMouseLeftButtonUp(self):
		if self.checkImage:
			if self.checkImage.IsShow():
				self.checkImage.Hide()

				if self.eventFunc["ON_UNCKECK"]:
					apply(self.eventFunc["ON_UNCKECK"], self.eventArgs["ON_UNCKECK"])
			else:
				self.checkImage.Show()

				if self.eventFunc["ON_CHECK"]:
					apply(self.eventFunc["ON_CHECK"], self.eventArgs["ON_CHECK"])
					
class CheckBoxOptions(Window):
	def __init__(self):
		Window.__init__(self)

		self.backgroundImage = None
		self.checkImage = None

		self.eventFunc = { "ON_CHECK" : None, "ON_UNCKECK" : None, }
		self.eventArgs = { "ON_CHECK" : None, "ON_UNCKECK" : None, }

		self.CreateElements()

	def __del__(self):
		Window.__del__(self)

		self.backgroundImage = None
		self.checkImage = None

		self.eventFunc = { "ON_CHECK" : None, "ON_UNCKECK" : None, }
		self.eventArgs = { "ON_CHECK" : None, "ON_UNCKECK" : None, }
	
	def CreateElements(self):
		self.backgroundImage = ImageBox()
		self.backgroundImage.SetParent(self)
		self.backgroundImage.AddFlag("not_pick")
		self.backgroundImage.LoadImage("d:/ymir work/ui/game/stats_board/checkbox_new_unselected.tga")
		self.backgroundImage.Show()

		self.checkImage = ImageBox()
		self.checkImage.SetParent(self)
		self.checkImage.AddFlag("not_pick")
		self.checkImage.SetPosition(0, -4)
		self.checkImage.LoadImage("d:/ymir work/ui/game/stats_board/checkbox_new_selected.tga")
		self.checkImage.Hide()

		self.textInfo = TextLine()
		self.textInfo.SetParent(self)
		self.textInfo.SetPosition(20, -2)
		self.textInfo.Show()

		self.SetSize(self.backgroundImage.GetWidth() + self.textInfo.GetTextSize()[0], self.backgroundImage.GetHeight() + self.textInfo.GetTextSize()[1])

	def SetTextInfo(self, info):
		if self.textInfo:
			self.textInfo.SetText(info)

		self.SetSize(self.backgroundImage.GetWidth() + self.textInfo.GetTextSize()[0], self.backgroundImage.GetHeight() + self.textInfo.GetTextSize()[1])

	def SetCheckStatus(self, flag):
		if flag:
			self.checkImage.Show()
		else:
			self.checkImage.Hide()

	def GetCheckStatus(self):
		if self.checkImage:
			return self.checkImage.IsShow()

		return False

	def SetEvent(self, func, *args) :
		result = self.eventFunc.has_key(args[0])
		if result:
			self.eventFunc[args[0]] = func
			self.eventArgs[args[0]] = args
		else:
			print "[ERROR] ui.py SetEvent, Can`t Find has_key : %s" % args[0]

	def SetBaseCheckImage(self, image):
		if not self.backgroundImage:
			return
		
		self.backgroundImage.LoadImage(image)

	def OnMouseLeftButtonUp(self):
		if self.checkImage:
			if self.checkImage.IsShow():
				self.checkImage.Hide()

				if self.eventFunc["ON_UNCKECK"]:
					apply(self.eventFunc["ON_UNCKECK"], self.eventArgs["ON_UNCKECK"])
			else:
				self.checkImage.Show()

				if self.eventFunc["ON_CHECK"]:
					apply(self.eventFunc["ON_CHECK"], self.eventArgs["ON_CHECK"])
					
class AniImageBox(Window):
	def __init__(self, layer = "UI"):
		Window.__init__(self, layer)
		self.eventEndFrame = None

		if app.ENABLE_FISH_EVENT:
			self.end_frame_event = None

	def __del__(self):
		Window.__del__(self)
		self.eventEndFrame = None

		if app.ENABLE_FISH_EVENT:
			self.end_frame_event = None

	def RegisterWindow(self, layer):
		self.hWnd = wndMgr.RegisterAniImageBox(self, layer)

	def SetDelay(self, delay):
		wndMgr.SetDelay(self.hWnd, delay)

	def AppendImage(self, filename):
		wndMgr.AppendImage(self.hWnd, filename)

	def AppendImageScale(self, filename, scale_x, scale_y):
		wndMgr.AppendImageScale(self.hWnd, filename, scale_x, scale_y)

	def SetPercentage(self, curValue, maxValue):
		wndMgr.SetRenderingRect(self.hWnd, 0.0, 0.0, -1.0 + float(curValue) / float(maxValue), 0.0)

	def SetOnEndFrame(self, event):
		self.eventEndFrame = event

	def SetScale(self, xScale, yScale):
		wndMgr.SetScale(self.hWnd, xScale, yScale)
		
	if app.ENABLE_FISH_EVENT:
		def ResetFrame(self):
			wndMgr.ResetFrame(self.hWnd)

		def SetEndFrameEvent(self, event):
			self.end_frame_event = event

		def OnEndFrame(self):
			if self.end_frame_event:
				self.end_frame_event()

			if self.eventEndFrame:
				self.eventEndFrame()

		def SetScale(self, xScale, yScale):
			wndMgr.SetSlotScale(self.hWnd, xScale, yScale)
	else:
		def OnEndFrame(self):
			pass

class Button(Window):
	def __init__(self, layer = "UI"):
		Window.__init__(self, layer)

		self.eventFunc = None
		self.eventArgs = None
		
		self.eventFuncList = []
		self.eventArgsList = []

		self.ButtonText = None
		self.ToolTipText = None
		self.TextChild = []
	
		self.overFunc = None
		self.overArgs = None
		self.overOutFunc = None
		self.overOutArgs = None
		
		self.showtooltipevent = None
		self.showtooltiparg = None
		self.hidetooltipevent = None
		self.hidetooltiparg = None

	def __del__(self):
		self.eventFunc = None
		self.eventArgs = None

		self.overFunc = None
		self.overArgs = None
		self.overOutFunc = None
		self.overOutArgs = None

		Window.__del__(self)

	def RegisterWindow(self, layer):
		self.hWnd = wndMgr.RegisterButton(self, layer)

	def SetUpVisual(self, filename):
		wndMgr.SetUpVisual(self.hWnd, filename)

	def SetOverVisual(self, filename):
		wndMgr.SetOverVisual(self.hWnd, filename)

	def SetDownVisual(self, filename):
		wndMgr.SetDownVisual(self.hWnd, filename)

	def SetDisableVisual(self, filename):
		wndMgr.SetDisableVisual(self.hWnd, filename)

	def SetPosition(self, x, y):
		wndMgr.SetWindowPosition(self.hWnd, x, y)

	def GetUpVisualFileName(self):
		return wndMgr.GetUpVisualFileName(self.hWnd)

	def GetOverVisualFileName(self):
		return wndMgr.GetOverVisualFileName(self.hWnd)

	def GetDownVisualFileName(self):
		return wndMgr.GetDownVisualFileName(self.hWnd)

	def GetText(self):
		if not self.ButtonText:
			return ""

		return self.ButtonText.GetText()

	def Flash(self):
		wndMgr.Flash(self.hWnd)

	def Enable(self):
		wndMgr.Enable(self.hWnd)

	def Disable(self):
		wndMgr.Disable(self.hWnd)

	def Down(self):
		wndMgr.Down(self.hWnd)

	def SetUp(self):
		wndMgr.SetUp(self.hWnd)
		
	def GetText(self):
		if not self.ButtonText:
			return# ""
		return self.ButtonText.GetText()

	def SAFE_SetEvent(self, func, *args):
		self.eventFunc = __mem_func__(func)
		self.eventArgs = args
		
		self.eventFuncList.append(__mem_func__(func))
		self.eventArgsList.append(args)
		
	def SetEvent(self, func, *args):
		if func == 0: # similar to the old behaviour of SetEvent(0)
			self.Hide()
			return

		self.eventFunc = func
		self.eventArgs = args
		
		self.eventFuncList.append(func)
		self.eventArgsList.append(args)

	def SetTextColor(self, color):
		if not self.ButtonText:
			return
		self.ButtonText.SetPackedFontColor(color)

	def SetTextAddPos(self, text, x_add = 0, y_add = 0, height = 4):
		if not self.ButtonText:
			textLine = TextLine()
			textLine.SetParent(self)
			textLine.SetPosition(self.GetWidth() / 2 + x_add, self.GetHeight() / 2 + y_add)
			textLine.SetVerticalAlignCenter()
			textLine.SetHorizontalAlignCenter()
			textLine.Show()
			self.ButtonText = textLine
		self.ButtonText.SetText(text)

	def SetText(self, text, height = 4, x = 0, y = 0):
		if not self.ButtonText:
			textLine = TextLine()
			textLine.SetParent(self)
			if height == 1:
				textLine.SetFontName(localeInfo.UI_DEF_FONT_LARGE)
			textLine.SetPosition(self.GetWidth()/2 - x, self.GetHeight()/2 - y)
			textLine.SetVerticalAlignCenter()
			textLine.SetHorizontalAlignCenter()
			textLine.Show()
			self.ButtonText = textLine

		self.ButtonText.SetText(text)
		if height == 1:
			self.ButtonText.SetFontName(localeInfo.UI_DEF_FONT_LARGE)	

	def OnMouseOverIn(self):
		if self.overFunc:
			apply(self.overFunc, self.overArgs )
			
	def OnMouseOverOut(self):
		if self.overOutFunc:
			apply(self.overOutFunc, self.overOutArgs )
			
	def SetOverEvent(self, func, *args):
		self.overFunc = func
		self.overArgs = args
		
	def SetOverOutEvent(self, func, *args):
		self.overOutFunc = func
		self.overOutArgs = args
		
	def SetButtonScale(self, xScale, yScale):
		wndMgr.SetButtonScale(self.hWnd, xScale, yScale)
		
	def SetButtonColor(self, diffuseColor = (1.0, 1.0, 1.0, 1.0)):
		wndMgr.SetButtonColor(self.hWnd, diffuseColor)

	def GetButtonImageWidth(self):
		return wndMgr.GetButtonImageWidth(self.hWnd)
	
	def GetButtonImageHeight(self):
		return wndMgr.GetButtonImageHeight(self.hWnd)
		
	def SetAutoSizeText(self, text):
		if not self.ButtonText:
			textLine = TextLine()
			textLine.SetParent(self)
			textLine.SetVerticalAlignCenter()
			textLine.SetHorizontalAlignCenter()
			textLine.Show()
			self.ButtonText = textLine
	
		self.ButtonText.SetText(text)
		
		imageWidth = self.GetButtonImageWidth()
		imageHeight = self.GetButtonImageHeight()
		
		if imageWidth==0 or imageHeight==0:
			return
		
		(textWidth, textHeight)=self.ButtonText.GetTextSize()
		textWidth += imageWidth/5
		textHeight += imageHeight/10
		
		curWidth = self.GetWidth()
		curHeight = self.GetHeight()
		
		if curWidth < textWidth:
			curWidth = textWidth
			
		if curHeight < textHeight:
			curHeight = textHeight
		
		self.SetSize(curWidth, curHeight)
		self.SetButtonScale(curWidth*1.0/imageWidth, curHeight*1.0/imageHeight)
		self.ButtonText.SetPosition(self.GetWidth()/2, self.GetHeight()/2)
		
	def SetTextAlignLeft(self, text, height = 4):
		if not self.ButtonText:
			textLine = TextLine()
			textLine.SetParent(self)
			textLine.SetPosition(27, self.GetHeight()/2)
			textLine.SetVerticalAlignCenter()
			textLine.SetHorizontalAlignLeft()
			textLine.Show()
			self.ButtonText = textLine

		self.ButtonText.SetText(text)
		self.ButtonText.SetPosition(27, self.GetHeight()/2)
		self.ButtonText.SetVerticalAlignCenter()
		self.ButtonText.SetHorizontalAlignLeft()

	def AppendTextLineAllClear(self) : 
		self.TextChild = []

	def SetAppendTextChangeText(self, idx, text):
		if not len(self.TextChild) :
			return

		self.TextChild[idx].SetText(text)

	def SetAppendTextColor(self, idx, color) :
		if not len(self.TextChild) :
			return

		self.TextChild[idx].SetPackedFontColor(color)

	def AppendTextLine(self, text, font_size = localeInfo.UI_DEF_FONT, font_color = grp.GenerateColor(0.7607, 0.7607, 0.7607, 1.0), text_sort = "center", pos_x = None, pos_y = None):
		textLine = TextLine()
		textLine.SetParent(self)
		textLine.SetFontName(font_size)
		textLine.SetPackedFontColor(font_color)
		textLine.SetText(text)
		textLine.Show()

		if not pos_x and not pos_y :
			textLine.SetPosition(self.GetWidth()/2, self.GetHeight()/2)
		else :
			textLine.SetPosition(pos_x, pos_y)

		textLine.SetVerticalAlignCenter()
		if "center" == text_sort :
			textLine.SetHorizontalAlignCenter()
		elif "right" == text_sort :
			textLine.SetHorizontalAlignRight()
		elif "left" == 	text_sort :
			textLine.SetHorizontalAlignLeft()

		self.TextChild.append(textLine)

	def SetFormToolTipText(self, type, text, x, y):
		if not self.ToolTipText:
			toolTip=createToolTipWindowDict[type]()
			toolTip.SetParent(self)
			toolTip.SetSize(0, 0)
			toolTip.SetHorizontalAlignCenter()
			toolTip.SetOutline()
			toolTip.Hide()
			toolTip.SetPosition(x + self.GetWidth()/2, y)
			self.ToolTipText=toolTip

		self.ToolTipText.SetText(text)

	def SetToolTipWindow(self, toolTip, parent = True):		
		self.ToolTipText=toolTip
		if parent == True:
			self.ToolTipText.SetParentProxy(self)

	def SetToolTipText(self, text, x=0, y = -19):
		self.SetFormToolTipText("TEXT", text, x, y)

	def CallEvent(self):
		if self.eventFunc:
			apply(self.eventFunc, self.eventArgs)

	def ShowToolTip(self):
		if self.ToolTipText:
			self.ToolTipText.Show()

		if self.showtooltipevent:
			apply(self.showtooltipevent, self.showtooltiparg)
			
	def HideToolTip(self):
		if self.ToolTipText:
			self.ToolTipText.Hide()
			
		if self.hidetooltipevent:
			apply(self.hidetooltipevent, self.hidetooltiparg)
			
	def SetShowToolTipEvent(self, func, *args):
		self.showtooltipevent = func
		self.showtooltiparg = args
		
	def SetHideToolTipEvent(self, func, *args):
		self.hidetooltipevent = func
		self.hidetooltiparg = args

	def IsDown(self):
		return wndMgr.IsDown(self.hWnd)

class RadioButton(Button):
	def __init__(self):
		Button.__init__(self)

	def __del__(self):
		Button.__del__(self)

	def RegisterWindow(self, layer):
		self.hWnd = wndMgr.RegisterRadioButton(self, layer)

class RadioButtonGroup:
	def __init__(self):
		self.buttonGroup = []
		self.selectedBtnIdx = -1

	def __del__(self):
		for button, ue, de in self.buttonGroup:
			button.__del__()

	def Show(self):
		for (button, selectEvent, unselectEvent) in self.buttonGroup:
			button.Show()

	def Hide(self):
		for (button, selectEvent, unselectEvent) in self.buttonGroup:
			button.Hide()

	def SetText(self, idx, text):
		if idx >= len(self.buttonGroup):
			return
		(button, selectEvent, unselectEvent) = self.buttonGroup[idx]
		button.SetText(text)

	def OnClick(self, btnIdx):
		if btnIdx == self.selectedBtnIdx:
			return
		(button, selectEvent, unselectEvent) = self.buttonGroup[self.selectedBtnIdx]
		if unselectEvent:
			unselectEvent()
		button.SetUp()

		self.selectedBtnIdx = btnIdx
		(button, selectEvent, unselectEvent) = self.buttonGroup[btnIdx]
		if selectEvent:
			selectEvent()

		button.Down()

	def AddButton(self, button, selectEvent, unselectEvent):
		i = len(self.buttonGroup)
		button.SetEvent(lambda : self.OnClick(i))
		self.buttonGroup.append([button, selectEvent, unselectEvent])
		button.SetUp()

	def Create(rawButtonGroup):
		radioGroup = RadioButtonGroup()
		for (button, selectEvent, unselectEvent) in rawButtonGroup:
			radioGroup.AddButton(button, selectEvent, unselectEvent)

		radioGroup.OnClick(0)

		return radioGroup

	Create=staticmethod(Create)

class ToggleButton(Button):
	def __init__(self):
		Button.__init__(self)

		self.eventUp = None
		self.eventDown = None

		self.eventUpArgs = None
		self.eventDownArgs = None

	def __del__(self):
		Button.__del__(self)

		self.eventUp = None
		self.eventDown = None

	def SetToggleUpEvent(self, event, *args):
		self.eventUp = event
		self.eventUpArgs = args

	def SetToggleDownEvent(self, event, *args):
		self.eventDown = event
		self.eventDownArgs = args

	def RegisterWindow(self, layer):
		self.hWnd = wndMgr.RegisterToggleButton(self, layer)

	def OnToggleUp(self):
		if self.eventUp:
			if self.eventUpArgs:
				apply(self.eventUp, self.eventUpArgs)
			else:
				self.eventUp()

	def OnToggleDown(self):
		if self.eventDown:
			if self.eventDownArgs:
				apply(self.eventDown, self.eventDownArgs)
			else:
				self.eventDown()

class DragButton(Button):
	def __init__(self):
		Button.__init__(self)
		self.AddFlag("movable")

		self.callbackEnable = True
		self.eventMove = lambda: None

	def __del__(self):
		Button.__del__(self)

		self.eventMove = lambda: None

	def RegisterWindow(self, layer):
		self.hWnd = wndMgr.RegisterDragButton(self, layer)

	def SetMoveEvent(self, event):
		self.eventMove = event

	def SetRestrictMovementArea(self, x, y, width, height):
		wndMgr.SetRestrictMovementArea(self.hWnd, x, y, width, height)

	def TurnOnCallBack(self):
		self.callbackEnable = True

	def TurnOffCallBack(self):
		self.callbackEnable = False

	def OnMove(self):
		if self.callbackEnable:
			self.eventMove()

class NumberLine(Window):

	def __init__(self, layer = "UI"):
		Window.__init__(self, layer)

	def __del__(self):
		Window.__del__(self)

	def RegisterWindow(self, layer):
		self.hWnd = wndMgr.RegisterNumberLine(self, layer)

	def SetHorizontalAlignCenter(self):
		wndMgr.SetNumberHorizontalAlignCenter(self.hWnd)

	def SetHorizontalAlignRight(self):
		wndMgr.SetNumberHorizontalAlignRight(self.hWnd)

	def SetPath(self, path):
		wndMgr.SetPath(self.hWnd, path)

	def SetNumber(self, number):
		wndMgr.SetNumber(self.hWnd, number)

###################################################################################################
## PythonScript Element
###################################################################################################

class Box(Window):

	def RegisterWindow(self, layer):
		self.hWnd = wndMgr.RegisterBox(self, layer)

	def SetColor(self, color):
		wndMgr.SetColor(self.hWnd, color)

class Bar(Window):

	def RegisterWindow(self, layer):
		self.hWnd = wndMgr.RegisterBar(self, layer)

	def SetColor(self, color):
		wndMgr.SetColor(self.hWnd, color)

class Line(Window):

	def RegisterWindow(self, layer):
		self.hWnd = wndMgr.RegisterLine(self, layer)

	def SetColor(self, color):
		wndMgr.SetColor(self.hWnd, color)

class SlotBar(Window):

	def __init__(self):
		Window.__init__(self)

	def RegisterWindow(self, layer):
		self.hWnd = wndMgr.RegisterBar3D(self, layer)

## Same with SlotBar
class Bar3D(Window):

	def __init__(self):
		Window.__init__(self)

	def RegisterWindow(self, layer):
		self.hWnd = wndMgr.RegisterBar3D(self, layer)

	def SetColor(self, left, right, center):
		wndMgr.SetColor(self.hWnd, left, right, center)
		
class TextLink(Window):
	NORMAL_COLOR =  0xffa08784
	OVER_COLOR = 0xffe6d0a2
	DOWN_COLOR = 0xffefe4cd
	
	def __init__(self):
		Window.__init__(self)
	
		self.eventFunc = None
		self.eventArgs = None
	
		self.text = TextLine()
		self.text.SetParent(self)
		self.text.SetPackedFontColor(self.NORMAL_COLOR)
		self.text.Show()
	
		self.underline = TextLine()
		self.underline.SetParent(self)
		self.underline.SetPackedFontColor(self.NORMAL_COLOR)
		self.underline.Hide()
	
	def __del__(self):
		Window.__del__(self)
	
	def SetText(self, text):
		self.text.SetText(text)
		self.SetSize(self.text.GetTextSize()[0], self.text.GetTextSize()[1])
		self.underline.SetPosition(-20, self.text.GetTextSize()[1])
		self.underline.SetWindowHorizontalAlignCenter()
		self.underline.SetSize(self.text.GetTextSize()[0], 0)
	
	def OnMouseOverIn(self):
		self.text.SetPackedFontColor(self.OVER_COLOR)
		self.underline.Show()
	
	def OnMouseOverOut(self):
		self.text.SetPackedFontColor(self.NORMAL_COLOR)
		self.underline.Hide()
	
	def OnMouseLeftButtonDown(self):
		self.text.SetPackedFontColor(self.DOWN_COLOR)
		self.underline.SetPackedFontColor(self.DOWN_COLOR)
		self.underline.Show()
	
	def OnMouseLeftButtonUp(self):
		if self.eventFunc:
			apply(self.eventFunc, self.eventArgs)
		self.OnMouseOverOut()
	
	def SetEvent(self, event, *args):
		self.eventFunc = event
		self.eventArgs = args

class SlotWindow(Window):

	def __init__(self):
		Window.__init__(self)

		self.StartIndex = 0
		self.ItemVnum = 0

		self.eventSelectEmptySlot = None
		self.eventSelectItemSlot = None
		self.eventUnselectEmptySlot = None
		self.eventUnselectItemSlot = None
		self.eventUseSlot = None
		self.eventOverInItem = None
		self.eventOverOutItem = None
		self.eventPressedSlotButton = None
		if app.ENABLE_FISH_EVENT:
			self.eventSelectEmptySlotWindow = None
			self.eventSelectItemSlotWindow = None
			self.eventUnselectItemSlotWindow = None
			self.eventOverInItemWindow = None

	def __del__(self):
		Window.__del__(self)

		self.eventSelectEmptySlot = None
		self.eventSelectItemSlot = None
		self.eventUnselectEmptySlot = None
		self.eventUnselectItemSlot = None
		self.eventUseSlot = None
		self.eventOverInItem = None
		self.eventOverOutItem = None
		self.eventPressedSlotButton = None
		if app.ENABLE_FISH_EVENT:
			self.eventSelectEmptySlotWindow = None
			self.eventSelectItemSlotWindow = None
			self.eventUnselectItemSlotWindow = None
			self.eventOverInItemWindow = None

	def RegisterWindow(self, layer):
		self.hWnd = wndMgr.RegisterSlotWindow(self, layer)

	def SetSlotStyle(self, style):
		wndMgr.SetSlotStyle(self.hWnd, style)

	def HasSlot(self, slotIndex):
		return wndMgr.HasSlot(self.hWnd, slotIndex)

	def SetSlotBaseImage(self, imageFileName, r, g, b, a):
		wndMgr.SetSlotBaseImage(self.hWnd, imageFileName, r, g, b, a)

	def SetSlotBaseImageScale(self, imageFileName, r, g, b, a, sx, sy):
		wndMgr.SetSlotBaseImageScale(self.hWnd, imageFileName, r, g, b, a, sx, sy)

	def SetCoverButton(self,\
						slotIndex,\
						upName="d:/ymir work/ui/public/slot_cover_button_01.sub",\
						overName="d:/ymir work/ui/public/slot_cover_button_02.sub",\
						downName="d:/ymir work/ui/public/slot_cover_button_03.sub",\
						disableName="d:/ymir work/ui/public/slot_cover_button_04.sub",\
						LeftButtonEnable = False,\
						RightButtonEnable = True):
		wndMgr.SetCoverButton(self.hWnd, slotIndex, upName, overName, downName, disableName, LeftButtonEnable, RightButtonEnable)

	def EnableCoverButton(self, slotIndex):
		wndMgr.EnableCoverButton(self.hWnd, slotIndex)

	def DisableCoverButton(self, slotIndex):
		wndMgr.DisableCoverButton(self.hWnd, slotIndex)
		
	if app.ENABLE_FISH_EVENT:
		def DeleteCoverButton(self, slotIndex):
			wndMgr.DeleteCoverButton(self.hWnd, slotIndex)
			
	def SetAlwaysRenderCoverButton(self, slotIndex, bAlwaysRender = True):
		wndMgr.SetAlwaysRenderCoverButton(self.hWnd, slotIndex, bAlwaysRender)

	def AppendSlotButton(self, upName, overName, downName):
		wndMgr.AppendSlotButton(self.hWnd, upName, overName, downName)

	def ShowSlotButton(self, slotNumber):
		wndMgr.ShowSlotButton(self.hWnd, slotNumber)

	def HideAllSlotButton(self):
		wndMgr.HideAllSlotButton(self.hWnd)

	def AppendRequirementSignImage(self, filename):
		wndMgr.AppendRequirementSignImage(self.hWnd, filename)

	def ShowRequirementSign(self, slotNumber):
		wndMgr.ShowRequirementSign(self.hWnd, slotNumber)

	def HideRequirementSign(self, slotNumber):
		wndMgr.HideRequirementSign(self.hWnd, slotNumber)

	def ActivateEffectClickSlot(self, slotNumber):
		wndMgr.ActivateEffectClickSlot(self.hWnd, slotNumber)

	def DeactivateEffectClickSlot(self, slotNumber):
		wndMgr.DeactivateEffectClickSlot(self.hWnd, slotNumber)

	def ActivateSlotInventory(self, slotNumber):
		wndMgr.ActivateSlot(self.hWnd, slotNumber)
		
	def DeactivateSlotInventory(self, slotNumber):
		wndMgr.DeactivateSlot(self.hWnd, slotNumber)
		self.DeactivateSlot(slotNumber)

	if app.ENABLE_CHANGELOOK_SYSTEM:
		def ActivateSlot(self, slotNumber, r = 1.0, g = 1.0, b = 1.0, a = 1.0):
			wndMgr.ActivateEffect(self.hWnd, slotNumber, r, g, b, a)

		def DeactivateSlot(self, slotNumber):
			wndMgr.DeactivateEffect(self.hWnd, slotNumber)

		def ActivateSlotOld(self, slotNumber):
			wndMgr.ActivateSlot(self.hWnd, slotNumber)

		def DeactivateSlotOld(self, slotNumber):
			wndMgr.DeactivateSlot(self.hWnd, slotNumber)
	else:
		def ActivateSlot(self, slotNumber):
			wndMgr.ActivateSlot(self.hWnd, slotNumber)

		def DeactivateSlot(self, slotNumber):
			wndMgr.DeactivateSlot(self.hWnd, slotNumber)

	def ShowSlotBaseImage(self, slotNumber):
		wndMgr.ShowSlotBaseImage(self.hWnd, slotNumber)

	def HideSlotBaseImage(self, slotNumber):
		wndMgr.HideSlotBaseImage(self.hWnd, slotNumber)

	def SAFE_SetButtonEvent(self, button, state, event):
		if "LEFT"==button:
			if "EMPTY"==state:
				self.eventSelectEmptySlot=__mem_func__(event)
			elif "EXIST"==state:
				self.eventSelectItemSlot=__mem_func__(event)
			elif "ALWAYS"==state:
				self.eventSelectEmptySlot=__mem_func__(event)
				self.eventSelectItemSlot=__mem_func__(event)
		elif "RIGHT"==button:
			if "EMPTY"==state:
				self.eventUnselectEmptySlot=__mem_func__(event)
			elif "EXIST"==state:
				self.eventUnselectItemSlot=__mem_func__(event)
			elif "ALWAYS"==state:
				self.eventUnselectEmptySlot=__mem_func__(event)
				self.eventUnselectItemSlot=__mem_func__(event)

	if app.ENABLE_FISH_EVENT:
		def SetSelectEmptySlotEvent(self, empty, window = None):
			self.eventSelectEmptySlot = empty
			self.eventSelectEmptySlotWindow = window
	
		def SetSelectItemSlotEvent(self, item, window = None):
			self.eventSelectItemSlot = item
			self.eventSelectItemSlotWindow = window
	else:
		def SetSelectEmptySlotEvent(self, empty):
			self.eventSelectEmptySlot = empty
	
		def SetSelectItemSlotEvent(self, item):
			self.eventSelectItemSlot = item

	def SetUnselectEmptySlotEvent(self, empty):
		self.eventUnselectEmptySlot = empty

	if app.ENABLE_FISH_EVENT:
		def SetUnselectItemSlotEvent(self, item, window = None):
			self.eventUnselectItemSlot = item
			self.eventUnselectItemSlotWindow = window
	else:	
		def SetUnselectItemSlotEvent(self, item):
			self.eventUnselectItemSlot = item

	def SetUseSlotEvent(self, use):
		self.eventUseSlot = use

	if app.ENABLE_FISH_EVENT:
		def SetOverInItemEvent(self, event, window = None):
			self.eventOverInItem = event
			self.eventOverInItemWindow = window
	else:
		def SetOverInItemEvent(self, event):
			self.eventOverInItem = event

	def SetOverOutItemEvent(self, event):
		self.eventOverOutItem = event

	def SetPressedSlotButtonEvent(self, event):
		self.eventPressedSlotButton = event

	def GetSlotCount(self):
		return wndMgr.GetSlotCount(self.hWnd)

	def SetUseMode(self, flag):
		"True일때만 ItemToItem 이 가능한지 보여준다"
		wndMgr.SetUseMode(self.hWnd, flag)

	def SetUsableItem(self, flag):
		"True면 현재 가리킨 아이템이 ItemToItem 적용 가능하다"
		wndMgr.SetUsableItem(self.hWnd, flag)
		
	def AppendHighLightImage(self, index, fileName, alphaSpeed = 0.0, rotationSpeed = 0.0, curAlpha = 1.0, diffuse = 0xFFFFFFFF):
		wndMgr.AppendHighLightImage(self.hWnd, index, fileName, alphaSpeed, rotationSpeed, curAlpha, diffuse)

	def EnableHighLightImage(self, slotIndex):
		wndMgr.EnableHighLightImage(self.hWnd, slotIndex)

	def DisableHighLightImage(self, slotIndex):
		wndMgr.DisableHighLightImage(self.hWnd, slotIndex)

	## Slot
	if app.WJ_ENABLE_TRADABLE_ICON:
		def SetCanMouseEventSlot(self, slotIndex):
			wndMgr.SetCanMouseEventSlot(self.hWnd, slotIndex)

		def SetCantMouseEventSlot(self, slotIndex):
			wndMgr.SetCantMouseEventSlot(self.hWnd, slotIndex)

		def SetUsableSlotOnTopWnd(self, slotIndex):
			wndMgr.SetUsableSlotOnTopWnd(self.hWnd, slotIndex)

		def SetUnusableSlotOnTopWnd(self, slotIndex):
			wndMgr.SetUnusableSlotOnTopWnd(self.hWnd, slotIndex)

	def SetSlotCoolTime(self, slotIndex, coolTime, elapsedTime = 0.0):
		wndMgr.SetSlotCoolTime(self.hWnd, slotIndex, coolTime, elapsedTime)

	def DisableSlot(self, slotIndex):
		wndMgr.DisableSlot(self.hWnd, slotIndex)

	def EnableSlot(self, slotIndex):
		wndMgr.EnableSlot(self.hWnd, slotIndex)

	def LockSlot(self, slotIndex):
		wndMgr.LockSlot(self.hWnd, slotIndex)

	def UnlockSlot(self, slotIndex):
		wndMgr.UnlockSlot(self.hWnd, slotIndex)

	def RefreshSlot(self):
		wndMgr.RefreshSlot(self.hWnd)

	def ClearSlot(self, slotNumber):
		wndMgr.ClearSlot(self.hWnd, slotNumber)

	def ClearAllSlot(self):
		wndMgr.ClearAllSlot(self.hWnd)

	def AppendSlot(self, index, x, y, width, height):
		wndMgr.AppendSlot(self.hWnd, index, x, y, width, height)

	def SetSlot(self, slotIndex, itemIndex, width, height, icon, diffuseColor = (1.0, 1.0, 1.0, 1.0)):
		wndMgr.SetSlot(self.hWnd, slotIndex, itemIndex, width, height, icon, diffuseColor)

	def SetSlotScale(self, slotIndex, itemIndex, width, height, icon, sx, sy, diffuseColor = (1.0, 1.0, 1.0, 1.0)):
		wndMgr.SetSlotScale(self.hWnd, slotIndex, itemIndex, width, height, icon, diffuseColor, sx, sy)

	def SetSlotCount(self, slotNumber, count):
		wndMgr.SetSlotCount(self.hWnd, slotNumber, count)

	def SetSlotCountNew(self, slotNumber, grade, count):
		wndMgr.SetSlotCountNew(self.hWnd, slotNumber, grade, count)

	def SetCardSlot(self, renderingSlotNumber, CardIndex, cardIcon, diffuseColor = (1.0, 1.0, 1.0, 1.0)):
		if 0 == CardIndex or None == CardIndex:
			wndMgr.ClearSlot(self.hWnd, renderingSlotNumber)
			return

		item.SelectItem(CardIndex)
		(width, height) = item.GetItemSize()

		wndMgr.SetCardSlot(self.hWnd, renderingSlotNumber, CardIndex, width, height, cardIcon, diffuseColor)

	def SetItemSlot(self, renderingSlotNumber, ItemIndex, ItemCount = 0, diffuseColor = (1.0, 1.0, 1.0, 1.0)):
		if 0 == ItemIndex or None == ItemIndex:
			wndMgr.ClearSlot(self.hWnd, renderingSlotNumber)
			return

		item.SelectItem(ItemIndex)
		itemIcon = item.GetIconImage()

		item.SelectItem(ItemIndex)
		(width, height) = item.GetItemSize()

		wndMgr.SetSlot(self.hWnd, renderingSlotNumber, ItemIndex, width, height, itemIcon, diffuseColor)
		wndMgr.SetSlotCount(self.hWnd, renderingSlotNumber, ItemCount)
		if app.ENABLE_CHANGELOOK_SYSTEM:
			wndMgr.SetCoverButton(self.hWnd, renderingSlotNumber, "d:/ymir work/ui/game/quest/slot_button_00.sub", "d:/ymir work/ui/game/quest/slot_button_00.sub", "d:/ymir work/ui/game/quest/slot_button_00.sub", "icon/item/ingame_convert_mark.tga", False, False)

	def SetItemSlotVnum(self, renderingSlotNumber, ItemIndex, ItemCount = 0, diffuseColor = (1.0, 1.0, 1.0, 1.0)):
		if 0 == ItemIndex or None == ItemIndex:
			wndMgr.ClearSlot(self.hWnd, renderingSlotNumber)
			return

		item.SelectItem(ItemIndex)
		itemIcon = item.GetIconImage()

		item.SelectItem(ItemIndex)
		(width, height) = item.GetItemSize()

		wndMgr.SetSlot(self.hWnd, renderingSlotNumber, ItemIndex, width, height, itemIcon, diffuseColor)
		wndMgr.SetSlotCount(self.hWnd, renderingSlotNumber, ItemCount)
		if app.ENABLE_CHANGELOOK_SYSTEM:
			wndMgr.SetCoverButton(self.hWnd, renderingSlotNumber, "d:/ymir work/ui/game/quest/slot_button_00.sub", "d:/ymir work/ui/game/quest/slot_button_00.sub", "d:/ymir work/ui/game/quest/slot_button_00.sub", "icon/item/ingame_convert_mark.tga", False, False)
			
		self.ItemVnum = ItemIndex

	def SetItemSlotScale(self, renderingSlotNumber, ItemIndex, ItemCount = 0, sx = 1.0, sy = 1.0):
		if 0 == ItemIndex or None == ItemIndex:
			wndMgr.ClearSlot(self.hWnd, renderingSlotNumber)
			return

		item.SelectItem(ItemIndex)
		itemIcon = item.GetIconImage()

		item.SelectItem(ItemIndex)
		(width, height) = item.GetItemSize()
	
		if sx != 1.0:
			wndMgr.SetSlotScale(self.hWnd, renderingSlotNumber, ItemIndex, width, height, itemIcon, (1.0, 1.0, 1.0, 1.0), sx, sy)
		else:
			wndMgr.SetSlot(self.hWnd, renderingSlotNumber, ItemIndex, width, height, itemIcon, (1.0, 1.0, 1.0, 1.0))
			wndMgr.SetSlotCount(self.hWnd, renderingSlotNumber, ItemCount)
			if app.ENABLE_CHANGELOOK_SYSTEM:
				wndMgr.SetCoverButton(self.hWnd, renderingSlotNumber, "d:/ymir work/ui/game/quest/slot_button_00.sub", "d:/ymir work/ui/game/quest/slot_button_00.sub", "d:/ymir work/ui/game/quest/slot_button_00.sub", "icon/item/ingame_convert_mark.tga", False, False)

	def SetItemSlotScaleWithColor(self, renderingSlotNumber, ItemIndex, ItemCount = 0, sx = 1.0, sy = 1.0, diffuseColor = (1.0, 1.0, 1.0, 1.0)):
		if 0 == ItemIndex or None == ItemIndex:
			wndMgr.ClearSlot(self.hWnd, renderingSlotNumber)
			return

		item.SelectItem(ItemIndex)
		itemIcon = item.GetIconImage()

		item.SelectItem(ItemIndex)
		(width, height) = item.GetItemSize()
	
		if sx != 1.0:
			wndMgr.SetSlotScale(self.hWnd, renderingSlotNumber, ItemIndex, width, height, itemIcon, diffuseColor, sx, sy)
		else:
			wndMgr.SetSlot(self.hWnd, renderingSlotNumber, ItemIndex, width, height, itemIcon, diffuseColor)
			wndMgr.SetSlotCount(self.hWnd, renderingSlotNumber, ItemCount)
			if app.ENABLE_CHANGELOOK_SYSTEM:
				wndMgr.SetCoverButton(self.hWnd, renderingSlotNumber, "d:/ymir work/ui/game/quest/slot_button_00.sub", "d:/ymir work/ui/game/quest/slot_button_00.sub", "d:/ymir work/ui/game/quest/slot_button_00.sub", "icon/item/ingame_convert_mark.tga", False, False)

	def SetSkillSlot(self, renderingSlotNumber, skillIndex, skillLevel):

		skillIcon = skill.GetIconImage(skillIndex)

		if 0 == skillIcon:
			wndMgr.ClearSlot(self.hWnd, renderingSlotNumber)
			return

		wndMgr.SetSlot(self.hWnd, renderingSlotNumber, skillIndex, 1, 1, skillIcon)
		wndMgr.SetSlotCount(self.hWnd, renderingSlotNumber, skillLevel)

	def SetSkillSlotNew(self, renderingSlotNumber, skillIndex, skillGrade, skillLevel):

		skillIcon = skill.GetIconImageNew(skillIndex, skillGrade)

		if 0 == skillIcon:
			wndMgr.ClearSlot(self.hWnd, renderingSlotNumber)
			return

		wndMgr.SetSlot(self.hWnd, renderingSlotNumber, skillIndex, 1, 1, skillIcon)

	def SetEmotionSlot(self, renderingSlotNumber, emotionIndex):
		import CacheEffect as player
		icon = player.GetEmotionIconImage(emotionIndex)

		if 0 == icon:
			wndMgr.ClearSlot(self.hWnd, renderingSlotNumber)
			return

		wndMgr.SetSlot(self.hWnd, renderingSlotNumber, emotionIndex, 1, 1, icon)

	## Event
	if app.ENABLE_FISH_EVENT:
		def OnSelectEmptySlot(self, slotNumber):
			if self.eventSelectEmptySlot:
				if self.eventSelectEmptySlotWindow:
					self.eventSelectEmptySlot(slotNumber, self.eventSelectEmptySlotWindow)
				else:
					self.eventSelectEmptySlot(slotNumber)

		def OnSelectItemSlot(self, slotNumber):
			if self.eventSelectItemSlot:
				if self.eventSelectItemSlotWindow:
					self.eventSelectItemSlot(slotNumber, self.eventSelectItemSlotWindow)
				else:
					self.eventSelectItemSlot(slotNumber)
	else:
		def OnSelectEmptySlot(self, slotNumber):
			if self.eventSelectEmptySlot:
				self.eventSelectEmptySlot(slotNumber)
	
		def OnSelectItemSlot(self, slotNumber):
			if self.eventSelectItemSlot:
				self.eventSelectItemSlot(slotNumber)

	def OnUnselectEmptySlot(self, slotNumber):
		if self.eventUnselectEmptySlot:
			self.eventUnselectEmptySlot(slotNumber)

	if app.ENABLE_FISH_EVENT:
		def OnUnselectItemSlot(self, slotNumber):
			if self.eventUnselectItemSlot:
				if self.eventUnselectItemSlotWindow:
					self.eventUnselectItemSlot(slotNumber, self.eventUnselectItemSlotWindow)
				else:
					self.eventUnselectItemSlot(slotNumber)
	else:
		def OnUnselectItemSlot(self, slotNumber):
			if self.eventUnselectItemSlot:
				self.eventUnselectItemSlot(slotNumber)

	def OnUseSlot(self, slotNumber):
		if self.eventUseSlot:
			self.eventUseSlot(slotNumber)

	if app.ENABLE_FISH_EVENT:
		def OnOverInItem(self, slotNumber):
			if self.eventOverInItem:
				if self.eventOverInItemWindow:
					self.eventOverInItem(slotNumber, self.eventOverInItemWindow)
				else:
					if self.ItemVnum:
						self.eventOverInItem(slotNumber, self.ItemVnum)
					else:
						self.eventOverInItem(slotNumber)
	else:
		def OnOverInItem(self, slotNumber):
			if self.eventOverInItem:
				if self.ItemVnum:
					self.eventOverInItem(slotNumber, self.ItemVnum)
				else:
					self.eventOverInItem(slotNumber)

	def OnOverOutItem(self):
		if self.eventOverOutItem:
			self.eventOverOutItem()

	def OnPressedSlotButton(self, slotNumber):
		if self.eventPressedSlotButton:
			self.eventPressedSlotButton(slotNumber)

	def GetStartIndex(self):
		return 0
		
	if app.ENABLE_FISH_EVENT:
		def SetPickedAreaRender(self, flag):
			wndMgr.SetPickedAreaRender(self.hWnd, flag)

	if app.ENABLE_CUBE_COLOR:
		def SetUsableSlotCube(self, slotIndex):
			wndMgr.SetUsableSlotCube(self.hWnd, slotIndex)

		def SetUnusableWorldSlotCube(self, slotIndex):
			wndMgr.SetUnusableWorldSlotCube(self.hWnd, slotIndex)

		def SetUsableWorldSlotCube(self, slotIndex):
			wndMgr.SetUsableWorldSlotCube(self.hWnd, slotIndex)

		def SetUnusableSlotCube(self, slotIndex):
			wndMgr.SetUnusableSlotCube(self.hWnd, slotIndex)

class GridSlotWindow(SlotWindow):

	def __init__(self):
		SlotWindow.__init__(self)

		self.startIndex = 0

	def __del__(self):
		SlotWindow.__del__(self)

	def RegisterWindow(self, layer):
		self.hWnd = wndMgr.RegisterGridSlotWindow(self, layer)

	def ArrangeSlot(self, StartIndex, xCount, yCount, xSize, ySize, xBlank, yBlank):

		self.startIndex = StartIndex

		wndMgr.ArrangeSlot(self.hWnd, StartIndex, xCount, yCount, xSize, ySize, xBlank, yBlank)
		self.startIndex = StartIndex

	def GetStartIndex(self):
		return self.startIndex

class TitleBar(Window):

	BLOCK_WIDTH = 32
	BLOCK_HEIGHT = 23


	IMAGES = {
		'TITLE' : {
			'PATH' : "d:/ymir work/ui/pattern",
			'LEFT' : 'titlebar_left.tga',
			'CENTER' : 'titlebar_center.tga',
			'RIGHT' : 'titlebar_right.tga',
			'RIGHT_SPECIAL' : 'titlebar_right_02.tga'
		},
		
		'CLOSE' : {
			'PATH' : "d:/ymir work/ui/public",
			'NORMAL' : 'close_button_01.sub',
			'OVER' : 'close_button_02.sub',
			'DOWN' : 'close_button_03.sub'
		},
		
		'INFO' : {
			'PATH' : "d:/ymir work/ui/pattern",
			'NORMAL' : 'q_mark_01.tga',
			'OVER' : 'q_mark_02.tga',
			'DOWN' : 'q_mark_02.tga'
		},
	}

	def __init__(self):
		Window.__init__(self)
		self.AddFlag("attach")

	def __del__(self):
		Window.__del__(self)

	def MakeTitleBar(self, width, color):
		width = max(64, width)

		imgLeft = ExpandedImageBox()
		imgCenter = ExpandedImageBox()
		imgRight = ExpandedImageBox()
		imgLeft.AddFlag("not_pick")
		imgCenter.AddFlag("not_pick")
		imgRight.AddFlag("not_pick")
		imgLeft.SetParent(self)
		imgCenter.SetParent(self)
		imgRight.SetParent(self)

		imgLeft.LoadImage("%s/%s" % (self.IMAGES['TITLE']['PATH'], self.IMAGES['TITLE']['LEFT']))
		imgCenter.LoadImage("%s/%s" % (self.IMAGES['TITLE']['PATH'], self.IMAGES['TITLE']['CENTER']))
		imgRight.LoadImage("%s/%s" % (self.IMAGES['TITLE']['PATH'], self.IMAGES['TITLE']['RIGHT']))

		imgLeft.Show()
		imgCenter.Show()
		imgRight.Show()

		imgLeftTitle = ExpandedImageBox()
		imgLeftTitle.AddFlag("not_pick")
		imgLeftTitle.SetParent(self)
		imgLeftTitle.SetPosition(-33, -25)
		imgLeftTitle.Hide()
		
		self.imgLeftTitle = imgLeftTitle

		btnClose = Button()
		btnClose.SetParent(self)
		btnClose.SetUpVisual("%s/%s" % (self.IMAGES['CLOSE']['PATH'], self.IMAGES['CLOSE']['NORMAL']))
		btnClose.SetOverVisual("%s/%s" % (self.IMAGES['CLOSE']['PATH'], self.IMAGES['CLOSE']['OVER']))
		btnClose.SetDownVisual("%s/%s" % (self.IMAGES['CLOSE']['PATH'], self.IMAGES['CLOSE']['DOWN']))
		btnClose.SetToolTipText(localeInfo.UI_CLOSE, 0, -23)
		btnClose.Show()

		self.imgLeft = imgLeft
		self.imgCenter = imgCenter
		self.imgRight = imgRight
		self.btnClose = btnClose

		self.SetWidth(width)

	def SetWidth(self, width):
		self.imgCenter.SetRenderingRect(0.0, 0.0, float((width - self.BLOCK_WIDTH*2) - self.BLOCK_WIDTH) / self.BLOCK_WIDTH, 0.0)
		self.imgCenter.SetPosition(self.BLOCK_WIDTH, 0)
		self.imgRight.SetPosition(width - self.BLOCK_WIDTH, 0)

		self.btnClose.SetPosition(width - self.btnClose.GetWidth() - 3, 3)

		self.SetSize(width, self.BLOCK_HEIGHT)
	
	def TitleInfo(self, bLionHead = True, bShow = True):
		if bLionHead:
			self.imgLeftTitle.LoadImage("d:/ymir work/ui/game/comp/bar.png")
		else:
			self.imgLeftTitle.LoadImage("d:/ymir work/ui/game/comp/bar2.png")
	
		if bShow:
			self.imgLeftTitle.Show()
		else:
			self.imgLeftTitle.Hide()
			
		self.imgLeftTitle.SetTop()
	
	def SetCloseEvent(self, event):
		self.btnClose.SetEvent(event)

	def CloseButton(self, command):
		if command == "hide":
			self.imgRight.LoadImage("%s/%s" % (self.IMAGES['TITLE']['PATH'], self.IMAGES['TITLE']['RIGHT_SPECIAL']))
			self.btnClose.Hide()
			
		elif command == "show":
			self.imgRight.LoadImage("%s/%s" % (self.IMAGES['TITLE']['PATH'], self.IMAGES['TITLE']['RIGHT']))
			self.btnClose.Show()
			
class SubTitleBar(Button):
	def __init__(self):
		Button.__init__(self)
		self.image_map = ["d:/ymir work/ui/quest_re/quest_down.tga", "d:/ymir work/ui/quest_re/quest_up.tga"]
	
	def __del__(self):
		Button.__del__(self)

	def MakeSubTitleBar(self, width, color):
		width = max(64, width)
		self.SetWidth(width)
		self.SetUpVisual("d:/ymir work/ui/quest_re/quest_tab_01.tga")
		self.SetOverVisual("d:/ymir work/ui/quest_re/quest_tab_01.tga")
		self.SetDownVisual("d:/ymir work/ui/quest_re/quest_tab_01.tga")
		self.Show()

		scrollImage = ImageBox()
		scrollImage.SetParent(self)
		scrollImage.LoadImage(self.image_map[0])
		scrollImage.SetPosition(5, 2.5)
		scrollImage.AddFlag("not_pick")
		scrollImage.Show()
		self.scrollImage = scrollImage

	def OpenCategory(self, qcount = 0):
		if qcount > 0:
			self.scrollImage.LoadImage(self.image_map[1])
		else:
			self.scrollImage.LoadImage(self.image_map[0])

	def CloseCategory(self, qcount = 0):
		self.scrollImage.LoadImage(self.image_map[0])
	
	def SetMiniImageNorm(self, image):
		self.image_map[0] = image
		self.scrollImage.LoadImage(self.image_map[0])
	
	def SetMiniImageOpen(self, image):
		self.image_map[1] = image

	def SetQuestLabel(self, filename, qcount):
		tabColor = ImageBox()
		tabColor.SetParent(self)
		tabColor.LoadImage(filename)
		tabColor.AddFlag("not_pick")
		tabColor.SetPosition(188, 12)
		if qcount > 0:
			tabColor.Show()
		else:
			tabColor.Hide()
		self.tabColor = tabColor

	def SetWidth(self, width):
		self.SetPosition(32, 0)
		self.SetSize(width, 23)

class ListBar(Button):
	def __init__(self):
		Button.__init__(self)

	def __del__(self):
		Button.__del__(self)

	def MakeListBar(self, width, color):
		width = max(64, width)
		self.SetWidth(width)
		self.Show()

		checkbox = ImageBox()
		checkbox.SetParent(self)
		checkbox.LoadImage("d:/ymir work/ui/quest_re/quest_new.tga")
		checkbox.SetPosition(10, 7)
		checkbox.AddFlag("not_pick")
		checkbox.Show()
		self.checkbox = checkbox
		self.isChecked = False

	def SetWidth(self, width):
		self.SetPosition(32, 0)
		self.SetSize(width, 23)

	def CallEvent(self):
		self.OnClickEvent()
		super(ListBar, self).CallEvent()

	def OnClickEvent(self):
		self.checkbox.Hide()
		self.isChecked = True

	def SetSlot(self, slotIndex, itemIndex, width, height, icon, diffuseColor = (1.0, 1.0, 1.0, 1.0)):
		wndMgr.SetSlot(self.hWnd, slotIndex, itemIndex, width, height, icon, diffuseColor)

class HorizontalBar(Window):

	BLOCK_WIDTH = 32
	BLOCK_HEIGHT = 17

	def __init__(self):
		Window.__init__(self)
		self.AddFlag("attach")
		self.ButtonText = None

	def __del__(self):
		Window.__del__(self)

	def Create(self, width):

		width = max(96, width)

		imgLeft = ImageBox()
		imgLeft.SetParent(self)
		imgLeft.AddFlag("not_pick")
		imgLeft.LoadImage("d:/ymir work/ui/pattern/horizontalbar_left.tga")
		imgLeft.Show()

		imgCenter = ExpandedImageBox()
		imgCenter.SetParent(self)
		imgCenter.AddFlag("not_pick")
		imgCenter.LoadImage("d:/ymir work/ui/pattern/horizontalbar_center.tga")
		imgCenter.Show()

		imgRight = ImageBox()
		imgRight.SetParent(self)
		imgRight.AddFlag("not_pick")
		imgRight.LoadImage("d:/ymir work/ui/pattern/horizontalbar_right.tga")
		imgRight.Show()

		self.imgLeft = imgLeft
		self.imgCenter = imgCenter
		self.imgRight = imgRight
		self.SetWidth(width)

	def SetText(self, text):
		if not self.ButtonText:
			textLine = TextLine()
			textLine.SetParent(self)
			textLine.SetPosition(self.GetWidth()/2, self.GetHeight()/2)
			textLine.SetVerticalAlignCenter()
			textLine.SetHorizontalAlignCenter()
			textLine.Show()
			self.ButtonText = textLine

		self.ButtonText.SetText(text)
	
	def IsInHorizontalBarPos(self):
		if self.IsInPosition() or self.imgLeft.IsInPosition() or self.imgCenter.IsInPosition() or self.imgRight.IsInPosition():
			return True
		
		return False
			
	def GetText(self):
		if not self.ButtonText:
			return ""
		return self.ButtonText.GetText()


	def SetWidth(self, width):
		self.imgCenter.SetRenderingRect(0.0, 0.0, float((width - self.BLOCK_WIDTH*2) - self.BLOCK_WIDTH) / self.BLOCK_WIDTH, 0.0)
		self.imgCenter.SetPosition(self.BLOCK_WIDTH, 0)
		self.imgRight.SetPosition(width - self.BLOCK_WIDTH, 0)
		self.SetSize(width, self.BLOCK_HEIGHT)

class Gauge(Window):

	SLOT_WIDTH = 16
	SLOT_HEIGHT = 7

	GAUGE_TEMPORARY_PLACE = 12
	GAUGE_WIDTH = 16

	def __init__(self):
		Window.__init__(self)
		self.width = 0
		
		self.showtooltipevent = None
		self.showtooltiparg = None
		self.hidetooltipevent = None
		self.hidetooltiparg = None
		self.ToolTipText = None
		
	def __del__(self):
		Window.__del__(self)
		self.showtooltipevent = None
		self.showtooltiparg = None
		self.hidetooltipevent = None
		self.hidetooltiparg = None

	def SetShowToolTipEvent(self, func, *args):
		self.showtooltipevent = func
		self.showtooltiparg = args

	def SetHideToolTipEvent(self, func, *args):
		self.hidetooltipevent = func
		self.hidetooltiparg = args
	
	def OnMouseOverIn(self):
		self.ShowToolTip()
	
	def OnMouseOverOut(self):
		self.HideToolTip()	
	
	def ShowToolTip(self):
		if self.ToolTipText:
			self.ToolTipText.Show()

	def HideToolTip(self):
		if self.ToolTipText:
			self.ToolTipText.Hide()

	def SetToolTipText(self, text, x=0, y = -19):
		self.SetFormToolTipText("TEXT", text, x, y)

	def SetFormToolTipText(self, type, text, x, y):
		if not self.ToolTipText: 
			toolTip = createToolTipWindowDict[type]()
			toolTip.SetParent(self)
			toolTip.SetSize(0, 0)
			toolTip.SetHorizontalAlignCenter()
			toolTip.SetOutline()
			toolTip.Hide()
			toolTip.SetPosition(x + self.GetWidth()/2, y)
		
			self.ToolTipText=toolTip

		self.ToolTipText.SetText(text)

	def MakeGauge(self, width, color, parentNew = None):

		self.width = max(48, width)

		imgSlotLeft = ExpandedImageBox()
		imgSlotLeft.SetParent(self, parentNew)
		imgSlotLeft.LoadImage("d:/ymir work/ui/pattern/gauge_slot_left.tga")
		imgSlotLeft.Show()

		imgSlotRight = ExpandedImageBox()
		imgSlotRight.SetParent(self, parentNew)
		imgSlotRight.LoadImage("d:/ymir work/ui/pattern/gauge_slot_right.tga")
		imgSlotRight.Show()
		imgSlotRight.SetPosition(width - self.SLOT_WIDTH, 0)

		imgSlotCenter = ExpandedImageBox()
		imgSlotCenter.SetParent(self, parentNew)
		imgSlotCenter.LoadImage("d:/ymir work/ui/pattern/gauge_slot_center.tga")
		imgSlotCenter.Show()
		imgSlotCenter.SetRenderingRect(0.0, 0.0, float((width - self.SLOT_WIDTH*2) - self.SLOT_WIDTH) / self.SLOT_WIDTH, 0.0)
		imgSlotCenter.SetPosition(self.SLOT_WIDTH, 0)

		imgGauge = ExpandedImageBox()
		imgGauge.SetParent(self, parentNew)
		imgGauge.LoadImage("d:/ymir work/ui/pattern/gauge_" + color + ".tga")
		imgGauge.Show()
		imgGauge.SetRenderingRect(0.0, 0.0, 0.0, 0.0)
		imgGauge.SetPosition(self.GAUGE_TEMPORARY_PLACE, 0)

		imgSlotLeft.AddFlag("attach")
		imgSlotCenter.AddFlag("attach")
		imgSlotRight.AddFlag("attach")

		self.imgLeft = imgSlotLeft
		self.imgCenter = imgSlotCenter
		self.imgRight = imgSlotRight
		self.imgGauge = imgGauge

		self.SetSize(width, self.SLOT_HEIGHT)

	def SetPercentage(self, curValue, maxValue):

		# PERCENTAGE_MAX_VALUE_ZERO_DIVISION_ERROR
		if maxValue > 0.0:
			percentage = min(1.0, float(curValue)/float(maxValue))
		else:
			percentage = 0.0
		# END_OF_PERCENTAGE_MAX_VALUE_ZERO_DIVISION_ERROR

		gaugeSize = -1.0 + float(self.width - self.GAUGE_TEMPORARY_PLACE*2) * percentage / self.GAUGE_WIDTH
		self.imgGauge.SetRenderingRect(0.0, 0.0, gaugeSize, 0.0)

class GaugeTarget(Window):

	SLOT_WIDTH = 16
	SLOT_HEIGHT = 7

	GAUGE_TEMPORARY_PLACE = 12
	GAUGE_WIDTH = 16

	def __init__(self):
		Window.__init__(self)
		self.width = 0
		self.lastCurValue = 0
		self.lastMaxValue = 0
		
		self.ToolTipText = None
		
	def __del__(self):
		Window.__del__(self)

	def MakeGauge(self, width, color):

		self.width = max(48, width)

		imgSlotLeft = ImageBox()
		imgSlotLeft.SetParent(self)
		imgSlotLeft.LoadImage("d:/ymir work/ui/pattern/gauge_slot_left.tga")
		imgSlotLeft.Show()

		imgSlotRight = ImageBox()
		imgSlotRight.SetParent(self)
		imgSlotRight.LoadImage("d:/ymir work/ui/pattern/gauge_slot_right.tga")
		imgSlotRight.Show()
		imgSlotRight.SetPosition(width - self.SLOT_WIDTH, 0)

		imgSlotCenter = ExpandedImageBox()
		imgSlotCenter.SetParent(self)
		imgSlotCenter.LoadImage("d:/ymir work/ui/pattern/gauge_slot_center.tga")
		imgSlotCenter.Show()
		imgSlotCenter.SetRenderingRect(0.0, 0.0, float((width - self.SLOT_WIDTH*2) - self.SLOT_WIDTH) / self.SLOT_WIDTH, 0.0)
		imgSlotCenter.SetPosition(self.SLOT_WIDTH, 0)

		imgGaugeBack = ExpandedImageBox()
		imgGaugeBack.SetParent(self)
		imgGaugeBack.LoadImage("d:/ymir work/ui/pattern/gauge_yellow.tga")
		imgGaugeBack.Hide()
		imgGaugeBack.SetRenderingRect(0.0, 0.0, 0.0, 0.0)
		imgGaugeBack.SetPosition(self.GAUGE_TEMPORARY_PLACE, 0)
		
		imgGauge = ExpandedImageBox()
		imgGauge.SetParent(self)
		imgGauge.LoadImage("d:/ymir work/ui/pattern/gauge_" + color + ".tga")
		imgGauge.Show()
		imgGauge.SetRenderingRect(0.0, 0.0, 0.0, 0.0)
		imgGauge.SetPosition(self.GAUGE_TEMPORARY_PLACE, 0)

		imgSlotLeft.AddFlag("attach")
		imgSlotCenter.AddFlag("attach")
		imgSlotRight.AddFlag("attach")

		self.imgLeft = imgSlotLeft
		self.imgCenter = imgSlotCenter
		self.imgRight = imgSlotRight
		self.imgGauge = imgGauge
		self.imgGaugeBack = imgGaugeBack

		self.SetSize(width, self.SLOT_HEIGHT)

	def ChangeColor(self, color):
		if self.imgGauge:
			self.imgGauge.LoadImage("d:/ymir work/ui/pattern/gauge_" + color + ".tga")

	def SetWidth(self, width):
		self.width = max(48, width)
		self.imgRight.SetPosition(width - self.SLOT_WIDTH, 0)
		self.imgCenter.SetRenderingRect(0.0, 0.0, float((width - self.SLOT_WIDTH*2) - self.SLOT_WIDTH) / self.SLOT_WIDTH, 0.0)
		
		self.SetSize(width, self.SLOT_HEIGHT)
		
		self.SetPercentage(self.lastCurValue, self.lastMaxValue)
		
	def SetPercentage(self, curValue, maxValue):
		if maxValue > 0.0:
			percentage = min(1.0, float(curValue)/float(maxValue))
		else:
			percentage = 0.0
			
		self.lastCurValue = curValue
		self.lastMaxValue = maxValue

		gaugeSize = -1.0 + float(self.width - self.GAUGE_TEMPORARY_PLACE*2) * percentage / self.GAUGE_WIDTH
		self.imgGauge.SetRenderingRect(0.0, 0.0, gaugeSize, 0.0)
		
	def SetPercentageBack(self, curValue, maxValue):
		if not self.imgGaugeBack.IsShow():
			self.imgGaugeBack.Show()
			
		if maxValue > 0.0:
			percentage = min(1.0, float(curValue)/float(maxValue))
		else:
			percentage = 0.0

		gaugeSize = -1.0 + float(self.width - self.GAUGE_TEMPORARY_PLACE*2) * percentage / self.GAUGE_WIDTH
		self.imgGaugeBack.SetRenderingRect(0.0, 0.0, gaugeSize, 0.0)
		
	def SetShowToolTipEvent(self, func, *args):
		self.showtooltipevent = func
		self.showtooltiparg = args

	def SetHideToolTipEvent(self, func, *args):
		self.hidetooltipevent = func
		self.hidetooltiparg = args

	def ShowToolTip(self):
		if self.ToolTipText:
			self.ToolTipText.Show()

	def HideToolTip(self):
		if self.ToolTipText:
			self.ToolTipText.Hide()

	def SetToolTipText(self, text, x=0, y = -19):
		self.SetFormToolTipText("TEXT", text, x, y)

	def SetFormToolTipText(self, type, text, x, y):
		if not self.ToolTipText: 
			toolTip = createToolTipWindowDict[type]()
			toolTip.SetParent(self)
			toolTip.SetSize(0, 0)
			toolTip.SetHorizontalAlignCenter()
			toolTip.SetOutline()
			toolTip.Hide()
			toolTip.SetPosition(x + self.GetWidth()/2, y)
			self.ToolTipText=toolTip

			self.ToolTipText.SetText(text)

class Board(Window):
	CORNER_WIDTH = 32
	CORNER_HEIGHT = 32
	LINE_WIDTH = 128
	LINE_HEIGHT = 128

	BASE_WIDTH = 128
	BASE_HEIGHT = 128

	LT = 0
	LB = 1
	RT = 2
	RB = 3
	L = 0
	R = 1
	T = 2
	B = 3

	BASE_PATH = "d:/ymir work/ui/pattern"
	
	IMAGES = {
		'CORNER' : {
			0 : "board_corner_lefttop_norm",
			1 : "board_corner_Leftbottom_norm",
			2 : "board_corner_righttop_norm",
			3 : "board_corner_rightbottom_norm"
		},
		'BAR' : {
			0 : "board_line_left_norm",
			1 : "board_line_right_norm",
			2 : "board_line_top_norm",
			3 : "board_line_bottom_norm"
		},
		'FILL' : "board_base_norm"
	}

	def __init__(self, layer = "UI"):
		Window.__init__(self, layer)

		self.MakeBoard()
		
	def SetAlpha(self, alpha):
		pass
		
	def MakeBoard(self):
		CornerFileNames = [ ]
		LineFileNames = [ ]
		
		for imageDictKey in (['CORNER', 'BAR']):
			for x in xrange(len(self.IMAGES[imageDictKey])):
				if imageDictKey == "CORNER":
					CornerFileNames.append("%s/%s.tga" % (self.BASE_PATH, self.IMAGES[imageDictKey][x]))
				elif imageDictKey == "BAR":
					LineFileNames.append("%s/%s.tga" % (self.BASE_PATH, self.IMAGES[imageDictKey][x]))
						
		self.Corners = []
		for fileName in CornerFileNames:
			Corner = ExpandedImageBoxAnim()
			Corner.AddFlag("not_pick")
			Corner.LoadImage(fileName)
			Corner.SetParent(self)
			Corner.SetPosition(0, 0)
			Corner.Show()
			self.Corners.append(Corner)

		self.Lines = []
		for fileName in LineFileNames:
			Line = ExpandedImageBoxAnim()
			Line.AddFlag("not_pick")
			Line.LoadImage(fileName)
			Line.SetParent(self)
			Line.SetPosition(0, 0)
			Line.Show()
			self.Lines.append(Line)

		self.Lines[self.L].SetPosition(0, self.CORNER_HEIGHT)
		self.Lines[self.T].SetPosition(self.CORNER_WIDTH, 0)

		self.Base = ExpandedImageBoxAnim()
		self.Base.AddFlag("not_pick")
		self.Base.LoadImage("%s/%s.tga" % (self.BASE_PATH, self.IMAGES['FILL']))
		self.Base.SetParent(self)
		self.Base.SetPosition(self.CORNER_WIDTH, self.CORNER_HEIGHT)
		self.Base.Show()

	def __del__(self):
		Window.__del__(self)

	def SetSize(self, width, height):
		width = max(self.CORNER_WIDTH*2, width)
		height = max(self.CORNER_HEIGHT*2, height)
		Window.SetSize(self, width, height)

		self.Corners[self.LB].SetPosition(0, height - self.CORNER_HEIGHT)
		self.Corners[self.RT].SetPosition(width - self.CORNER_WIDTH, 0)
		self.Corners[self.RB].SetPosition(width - self.CORNER_WIDTH, height - self.CORNER_HEIGHT)
		self.Lines[self.R].SetPosition(width - self.CORNER_WIDTH, self.CORNER_HEIGHT)
		self.Lines[self.B].SetPosition(self.CORNER_HEIGHT, height - self.CORNER_HEIGHT)

		verticalShowingPercentage = float((height - self.CORNER_HEIGHT*2) - self.LINE_HEIGHT) / self.LINE_HEIGHT
		horizontalShowingPercentage = float((width - self.CORNER_WIDTH*2) - self.LINE_WIDTH) / self.LINE_WIDTH
		
		verticalShowingPercentage2 = float((height - self.CORNER_HEIGHT*2) - self.BASE_HEIGHT) / self.BASE_HEIGHT
		horizontalShowingPercentage2 = float((width - self.CORNER_WIDTH*2) - self.BASE_WIDTH) / self.BASE_WIDTH
		
		self.Lines[self.L].SetRenderingRect(0, 0, 0, verticalShowingPercentage)
		self.Lines[self.R].SetRenderingRect(0, 0, 0, verticalShowingPercentage)
		self.Lines[self.T].SetRenderingRect(0, 0, horizontalShowingPercentage, 0)
		self.Lines[self.B].SetRenderingRect(0, 0, horizontalShowingPercentage, 0)

		if self.Base:
			self.Base.SetRenderingRect(0, 0, horizontalShowingPercentage2, verticalShowingPercentage2)

class BoardNorm(Window):
	CORNER_WIDTH = 32
	CORNER_HEIGHT = 32
	LINE_WIDTH = 128
	LINE_HEIGHT = 128

	LT = 0
	LB = 1
	RT = 2
	RB = 3
	L = 0
	R = 1
	T = 2
	B = 3
	
	BASE_PATH = "d:/ymir work/ui/pattern"
	IMAGES = {
		'CORNER' : {
			0 : "Board_Corner_LeftTop",
			1 : "Board_Corner_LeftBottom",
			2 : "Board_Corner_RightTop",
			3 : "Board_Corner_RightBottom"
		},
		'BAR' : {
			0 : "Board_Line_Left",
			1 : "Board_Line_Right",
			2 : "Board_Line_Top",
			3 : "Board_Line_Bottom"
		},
		'FILL' : "Board_Base"
	}

	def __init__(self, layer = "UI"):
		Window.__init__(self, layer)
		self.skipMaxCheck = False

		self.MakeBoard()
		
	def MakeBoard(self):
		CornerFileNames = [ ]
		LineFileNames = [ ]
		
		for imageDictKey in (['CORNER', 'BAR']):
			for x in xrange(len(self.IMAGES[imageDictKey])):
				if imageDictKey == "CORNER":
					CornerFileNames.append("%s/%s.tga" % (self.BASE_PATH, self.IMAGES[imageDictKey][x]))
				elif imageDictKey == "BAR":
					LineFileNames.append("%s/%s.tga" % (self.BASE_PATH, self.IMAGES[imageDictKey][x]))
		
		self.Corners = []
		for fileName in CornerFileNames:
			Corner = ExpandedImageBox()
			Corner.AddFlag("not_pick")
			Corner.LoadImage(fileName)
			Corner.SetParent(self)
			Corner.SetPosition(0, 0)
			Corner.Show()
			self.Corners.append(Corner)

		self.Lines = []
		for fileName in LineFileNames:
			Line = ExpandedImageBox()
			Line.AddFlag("not_pick")
			Line.LoadImage(fileName)
			Line.SetParent(self)
			Line.SetPosition(0, 0)
			Line.Show()
			self.Lines.append(Line)

		self.Lines[self.L].SetPosition(0, self.CORNER_HEIGHT)
		self.Lines[self.T].SetPosition(self.CORNER_WIDTH, 0)

		self.Base = ExpandedImageBox()
		self.Base.AddFlag("not_pick")
		self.Base.LoadImage("%s/%s.tga" % (self.BASE_PATH, self.IMAGES['FILL']))
		self.Base.SetParent(self)
		self.Base.SetPosition(self.CORNER_WIDTH, self.CORNER_HEIGHT)
		self.Base.Show()

	def __del__(self):
		Window.__del__(self)

	def SetSize(self, width, height):
		if not self.skipMaxCheck:
			width = max(self.CORNER_WIDTH*2, width)
			height = max(self.CORNER_HEIGHT*2, height)
			
		Window.SetSize(self, width, height)

		self.Corners[self.LB].SetPosition(0, height - self.CORNER_HEIGHT)
		self.Corners[self.RT].SetPosition(width - self.CORNER_WIDTH, 0)
		self.Corners[self.RB].SetPosition(width - self.CORNER_WIDTH, height - self.CORNER_HEIGHT)
		self.Lines[self.R].SetPosition(width - self.CORNER_WIDTH, self.CORNER_HEIGHT)
		self.Lines[self.B].SetPosition(self.CORNER_HEIGHT, height - self.CORNER_HEIGHT)

		verticalShowingPercentage = float((height - self.CORNER_HEIGHT*2) - self.LINE_HEIGHT) / self.LINE_HEIGHT
		horizontalShowingPercentage = float((width - self.CORNER_WIDTH*2) - self.LINE_WIDTH) / self.LINE_WIDTH
		self.Lines[self.L].SetRenderingRect(0, 0, 0, verticalShowingPercentage)
		self.Lines[self.R].SetRenderingRect(0, 0, 0, verticalShowingPercentage)
		self.Lines[self.T].SetRenderingRect(0, 0, horizontalShowingPercentage, 0)
		self.Lines[self.B].SetRenderingRect(0, 0, horizontalShowingPercentage, 0)

		if self.Base:
			self.Base.SetRenderingRect(0, 0, horizontalShowingPercentage, verticalShowingPercentage)
			
class BorderB(BoardNorm):
	CORNER_WIDTH = 16
	CORNER_HEIGHT = 16
	LINE_WIDTH = 16
	LINE_HEIGHT = 16

	BASE_PATH = "d:/ymir work/ui/pattern"

	IMAGES = {
		'CORNER' : {
			0 : "border_b_left_top",
			1 : "border_b_left_bottom",
			2 : "border_b_right_top",
			3 : "border_b_right_bottom"
		},
		'BAR' : {
			0 : "border_b_left",
			1 : "border_b_right",
			2 : "border_b_top",
			3 : "border_b_bottom"
		},
		'FILL' : "border_b_center"
	}

	def __init__(self):
		BoardNorm.__init__(self)
			
		self.eventFunc = {
			"MOUSE_LEFT_BUTTON_UP" : None, 
		}
		self.eventArgs = {
			"MOUSE_LEFT_BUTTON_UP" : None, 
		}

	def __del__(self):
		BoardNorm.__del__(self)
		self.eventFunc = None
		self.eventArgs = None

	def SetSize(self, width, height):
		BoardNorm.SetSize(self, width, height)

	def SetEvent(self, func, *args) :
		result = self.eventFunc.has_key(args[0])
		if result :
			self.eventFunc[args[0]] = func
			self.eventArgs[args[0]] = args
		else :
			print "[ERROR] ui.py SetEvent, Can`t Find has_key : %s" % args[0]

	def OnMouseLeftButtonUp(self):
		if self.eventFunc["MOUSE_LEFT_BUTTON_UP"] :
			apply(self.eventFunc["MOUSE_LEFT_BUTTON_UP"], self.eventArgs["MOUSE_LEFT_BUTTON_UP"])

class BorderC(BoardNorm):
	CORNER_WIDTH = 16
	CORNER_HEIGHT = 16
	LINE_WIDTH = 16
	LINE_HEIGHT = 16
	
	BASE_PATH = "d:/ymir work/ui/pattern/borderc"
	IMAGES = {
		'CORNER' : {
			0 : "border_c_left_top",
			1 : "border_c_left_bottom",
			2 : "border_c_right_top",
			3 : "border_c_right_bottom"
		},
		'BAR' : {
			0 : "border_c_left",
			1 : "border_c_right",
			2 : "border_c_top",
			3 : "border_c_bottom"
		},
		'FILL' : "border_c_center"
	}
	
	def __init__(self):
		BoardNorm.__init__(self)
			
		self.eventFunc = {
			"MOUSE_LEFT_BUTTON_UP" : None,
		}
		self.eventArgs = {
			"MOUSE_LEFT_BUTTON_UP" : None,
		}
		
	def __del__(self):
		BoardNorm.__del__(self)
		self.eventFunc = None
		self.eventArgs = None
	
	def SetSize(self, width, height):
		BoardNorm.SetSize(self, width, height)
		
	def SetEvent(self, func, *args) :
		result = self.eventFunc.has_key(args[0])
		if result :
			self.eventFunc[args[0]] = func
			self.eventArgs[args[0]] = args
		else :
			print "[ERROR] ui.py SetEvent, Can`t Find has_key : %s" % args[0]
			
	def OnMouseLeftButtonUp(self):
		if self.eventFunc["MOUSE_LEFT_BUTTON_UP"] :
			apply(self.eventFunc["MOUSE_LEFT_BUTTON_UP"], self.eventArgs["MOUSE_LEFT_BUTTON_UP"])

class BorderNew(BoardNorm):
	CORNER_WIDTH = 16
	CORNER_HEIGHT = 16
	LINE_WIDTH = 16
	LINE_HEIGHT = 16
	
	BASE_PATH = "d:/ymir work/ui/game/comp/mes/board"
	IMAGES = {
		'CORNER' : {
			0 : "border_a_left_top",
			1 : "border_a_left_bottom",
			2 : "border_a_right_top",
			3 : "border_a_right_bottom"
		},
		'BAR' : {
			0 : "border_a_left",
			1 : "border_a_right",
			2 : "border_a_top",
			3 : "border_a_bottom"
		},
		'FILL' : "border_a_center"
	}
	
	def __init__(self):
		BoardNorm.__init__(self)

	def __del__(self):
		BoardNorm.__del__(self)

	def SetSize(self, width, height):
		BoardNorm.SetSize(self, width, height)

class BrownBoard(Window):
	CORNER_WIDTH = 1
	CORNER_HEIGHT = 1

	LINE_WIDTH = 1
	LINE_HEIGHT = 1

	LT = 0
	LB = 1

	RT = 2
	RB = 3

	L = 0
	R = 1
	T = 2
	B = 3

	def __init__(self):
		Window.__init__(self)

		self.MakeBoard("d:/ymir work/ui/pattern/BrownBoard/BrownBoard_Corner_", "d:/ymir work/ui/pattern/BrownBoard/BrownBoard_Line_")
		self.MakeBase()

	def MakeBoard(self, cornerPath, linePath):
		CornerFileNames = [ cornerPath + dir + ".tga" for dir in ("LeftTop", "LeftBottom", "RightTop", "RightBottom", ) ]

		LineFileNames = [ linePath + dir + ".tga" for dir in ("Left", "Right", "Top", "Bottom", ) ]

		self.Corners = []

		for fileName in CornerFileNames:
			Corner = ExpandedImageBox()
			Corner.AddFlag("not_pick")
			Corner.LoadImage(fileName)
			Corner.SetParent(self)
			Corner.SetPosition(0, 0)
			Corner.Show()

			self.Corners.append(Corner)

		self.Lines = []

		for fileName in LineFileNames:
			Line = ExpandedImageBox()
			Line.AddFlag("not_pick")
			Line.LoadImage(fileName)
			Line.SetParent(self)
			Line.SetPosition(0, 0)
			Line.Show()

			self.Lines.append(Line)

		self.Lines[self.L].SetPosition(0, self.CORNER_HEIGHT)
		self.Lines[self.T].SetPosition(self.CORNER_WIDTH, 0)
		self.ButtonText = None

	def MakeBase(self):
		self.Base = ExpandedImageBox()
		self.Base.AddFlag("not_pick")
		self.Base.LoadImage("d:/ymir work/ui/pattern/BrownBoard/BrownBoard_Base.tga")
		self.Base.SetParent(self)
		self.Base.SetPosition(self.CORNER_WIDTH, self.CORNER_HEIGHT)
		self.Base.Show()

	def __del__(self):
		Window.__del__(self)

	def SetText(self, text):
		if not self.ButtonText:
			textLine = TextLine()
			textLine.SetParent(self)
			textLine.SetPosition(self.GetWidth()/2, self.GetHeight()/2)
			textLine.SetVerticalAlignCenter()
			textLine.SetHorizontalAlignCenter()
			textLine.Show()
			self.ButtonText = textLine

		self.ButtonText.SetText(text)

	def GetText(self):
		if not self.ButtonText:
			return ""
		return self.ButtonText.GetText()

	def SetClipMaster(self):
		pass
		# self.SetParent("Disabled")

	def SetSize(self, width, height):
		width = max(self.CORNER_WIDTH * 2, width)
		height = max(self.CORNER_HEIGHT * 2, height)

		Window.SetSize(self, width, height)

		self.Corners[self.LB].SetPosition(0, height - self.CORNER_HEIGHT)
		self.Corners[self.RT].SetPosition(width - self.CORNER_WIDTH, 0)
		self.Corners[self.RB].SetPosition(width - self.CORNER_WIDTH, height - self.CORNER_HEIGHT)

		self.Lines[self.R].SetPosition(width - self.CORNER_WIDTH, self.CORNER_HEIGHT)
		self.Lines[self.B].SetPosition(self.CORNER_HEIGHT, height - self.CORNER_HEIGHT)

		verticalShowingPercentage = float((height - self.CORNER_HEIGHT * 2) - self.LINE_HEIGHT) / self.LINE_HEIGHT
		horizontalShowingPercentage = float((width - self.CORNER_WIDTH * 2) - self.LINE_WIDTH) / self.LINE_WIDTH

		self.Lines[self.L].SetRenderingRect(0, 0, 0, verticalShowingPercentage)
		self.Lines[self.R].SetRenderingRect(0, 0, 0, verticalShowingPercentage)
		self.Lines[self.T].SetRenderingRect(0, 0, horizontalShowingPercentage, 0)
		self.Lines[self.B].SetRenderingRect(0, 0, horizontalShowingPercentage, 0)

		# if self.Base:
			# self.Base.SetRenderingRect(0, 0, horizontalShowingPercentage, verticalShowingPercentage)
			
class BrownBoard2(Window):
	CORNER_WIDTH = 1
	CORNER_HEIGHT = 1

	LINE_WIDTH = 1
	LINE_HEIGHT = 1

	LT = 0
	LB = 1

	RT = 2
	RB = 3

	L = 0
	R = 1
	T = 2
	B = 3

	def __init__(self):
		Window.__init__(self)

		self.MakeBoard("d:/ymir work/ui/pattern/BrownBoard2/BrownBoard2_Corner_", "d:/ymir work/ui/pattern/BrownBoard2/BrownBoard2_Line_")
		self.MakeBase()

	def MakeBoard(self, cornerPath, linePath):
		CornerFileNames = [ cornerPath + dir + ".tga" for dir in ("LeftTop", "LeftBottom", "RightTop", "RightBottom", ) ]

		LineFileNames = [ linePath + dir + ".tga" for dir in ("Left", "Right", "Top", "Bottom", ) ]

		self.Corners = []

		for fileName in CornerFileNames:
			Corner = ExpandedImageBox()
			Corner.AddFlag("not_pick")
			Corner.LoadImage(fileName)
			Corner.SetParent(self)
			Corner.SetPosition(0, 0)
			Corner.Show()

			self.Corners.append(Corner)

		self.Lines = []

		for fileName in LineFileNames:
			Line = ExpandedImageBox()
			Line.AddFlag("not_pick")
			Line.LoadImage(fileName)
			Line.SetParent(self)
			Line.SetPosition(0, 0)
			Line.Show()

			self.Lines.append(Line)

		self.Lines[self.L].SetPosition(0, self.CORNER_HEIGHT)
		self.Lines[self.T].SetPosition(self.CORNER_WIDTH, 0)
		self.ButtonText = None

	def MakeBase(self):
		self.Base = ExpandedImageBox()
		self.Base.AddFlag("not_pick")
		self.Base.LoadImage("d:/ymir work/ui/pattern/BrownBoard2/BrownBoard2_Base.tga")
		self.Base.SetParent(self)
		self.Base.SetPosition(self.CORNER_WIDTH, self.CORNER_HEIGHT)
		self.Base.Show()

	def __del__(self):
		Window.__del__(self)

	def SetClipMaster(self):
		pass
		# self.SetParent("Disabled")

	def SetText(self, text):
		if not self.ButtonText:
			textLine = TextLine()
			textLine.SetParent(self)
			textLine.SetPosition(self.GetWidth()/2, self.GetHeight()/2)
			textLine.SetVerticalAlignCenter()
			textLine.SetHorizontalAlignCenter()
			textLine.Show()
			self.ButtonText = textLine

		self.ButtonText.SetText(text)

	def GetText(self):
		if not self.ButtonText:
			return ""
		return self.ButtonText.GetText()

	def SetSize(self, width, height):
		width = max(self.CORNER_WIDTH * 2, width)
		height = max(self.CORNER_HEIGHT * 2, height)

		Window.SetSize(self, width, height)

		self.Corners[self.LB].SetPosition(0, height - self.CORNER_HEIGHT)
		self.Corners[self.RT].SetPosition(width - self.CORNER_WIDTH, 0)
		self.Corners[self.RB].SetPosition(width - self.CORNER_WIDTH, height - self.CORNER_HEIGHT)

		self.Lines[self.R].SetPosition(width - self.CORNER_WIDTH, self.CORNER_HEIGHT)
		self.Lines[self.B].SetPosition(self.CORNER_HEIGHT, height - self.CORNER_HEIGHT)

		verticalShowingPercentage = float((height - self.CORNER_HEIGHT * 2) - self.LINE_HEIGHT) / self.LINE_HEIGHT
		horizontalShowingPercentage = float((width - self.CORNER_WIDTH * 2) - self.LINE_WIDTH) / self.LINE_WIDTH

		self.Lines[self.L].SetRenderingRect(0, 0, 0, verticalShowingPercentage)
		self.Lines[self.R].SetRenderingRect(0, 0, 0, verticalShowingPercentage)
		self.Lines[self.T].SetRenderingRect(0, 0, horizontalShowingPercentage, 0)
		self.Lines[self.B].SetRenderingRect(0, 0, horizontalShowingPercentage, 0)

		# if self.Base:
			# self.Base.SetRenderingRect(0, 0, horizontalShowingPercentage, verticalShowingPercentage)

class BorderA(BoardNorm):
	CORNER_WIDTH = 16
	CORNER_HEIGHT = 16
	LINE_WIDTH = 16
	LINE_HEIGHT = 16
	
	BASE_PATH = "d:/ymir work/ui/pattern"
	IMAGES = {
		'CORNER' : {
			0 : "border_a_left_top",
			1 : "border_a_left_bottom",
			2 : "border_a_right_top",
			3 : "border_a_right_bottom"
		},
		'BAR' : {
			0 : "border_a_left",
			1 : "border_a_right",
			2 : "border_a_top",
			3 : "border_a_bottom"
		},
		'FILL' : "border_a_center"
	}
	
	def __init__(self, layer = "UI"):
		BoardNorm.__init__(self, layer)

	def __del__(self):
		BoardNorm.__del__(self)

	def SetSize(self, width, height):
		BoardNorm.SetSize(self, width, height)

class BoardWithTitleBar(Board):
	def __init__(self):
		Board.__init__(self)

		titleBar = TitleBar()
		titleBar.SetParent(self)
		titleBar.MakeTitleBar(0, "red")
		titleBar.SetPosition(8, 7)
		titleBar.Show()

		titleName = TextLine()
		titleName.SetParent(titleBar)
		titleName.SetPosition(0, 4)
		titleName.SetWindowHorizontalAlignCenter()
		titleName.SetHorizontalAlignCenter()
		titleName.Show()

		self.titleBar = titleBar
		self.titleName = titleName

		self.SetCloseEvent(self.Hide)

	def __del__(self):
		Board.__del__(self)
		self.titleBar = None
		self.titleName = None

	def SetSize(self, width, height):
		self.titleBar.SetWidth(width - 15)
		Board.SetSize(self, width, height)
		self.titleName.UpdateRect()

	def SetTitleColor(self, color):
		self.titleName.SetPackedFontColor(color)

	def SetTitleName(self, name):
		self.titleName.SetText(name)

	def SetCloseEvent(self, event):
		self.titleBar.SetCloseEvent(event)

class ThinBoard(Window):

	CORNER_WIDTH = 16
	CORNER_HEIGHT = 16
	LINE_WIDTH = 16
	LINE_HEIGHT = 16
	BOARD_COLOR = grp.GenerateColor(0.0, 0.0, 0.0, 0.46)

	LT = 0
	LB = 1
	RT = 2
	RB = 3
	L = 0
	R = 1
	T = 2
	B = 3

	def __init__(self, layer = "UI"):
		Window.__init__(self, layer)

		CornerFileNames = [ "d:/ymir work/ui/pattern/thinboardnew/thinboard_corner_"+dir+".tga" for dir in ["lefttop","leftbottom","righttop","rightbottom"] ]
		LineFileNames = [ "d:/ymir work/ui/pattern/thinboardnew/thinboard_line_"+dir+".tga" for dir in ["left","right","top","bottom"] ]

		self.Corners = []
		for fileName in CornerFileNames:
			Corner = ExpandedImageBox()
			Corner.AddFlag("attach")
			Corner.AddFlag("not_pick")
			Corner.LoadImage(fileName)
			Corner.SetParent(self)
			Corner.SetPosition(0, 0)
			Corner.Show()
			self.Corners.append(Corner)

		self.Lines = []
		for fileName in LineFileNames:
			Line = ExpandedImageBox()
			Line.AddFlag("attach")
			Line.AddFlag("not_pick")
			Line.LoadImage(fileName)
			Line.SetParent(self)
			Line.SetPosition(0, 0)
			Line.Show()
			self.Lines.append(Line)

		Base = Bar()
		Base.SetParent(self)
		Base.AddFlag("attach")
		Base.AddFlag("not_pick")
		Base.SetPosition(self.CORNER_WIDTH, self.CORNER_HEIGHT)
		Base.SetColor(self.BOARD_COLOR)
		Base.Show()
		self.Base = Base

		self.Lines[self.L].SetPosition(0, self.CORNER_HEIGHT)
		self.Lines[self.T].SetPosition(self.CORNER_WIDTH, 0)

	def __del__(self):
		Window.__del__(self)

	if app.ENABLE_SEND_TARGET_INFO:
		def ShowCorner(self, corner):
			self.Corners[corner].Show()
			self.SetSize(self.GetWidth(), self.GetHeight())

		def HideCorners(self, corner):
			self.Corners[corner].Hide()
			self.SetSize(self.GetWidth(), self.GetHeight())

		def ShowLine(self, line):
			self.Lines[line].Show()
			self.SetSize(self.GetWidth(), self.GetHeight())

		def HideLine(self, line):
			self.Lines[line].Hide()
			self.SetSize(self.GetWidth(), self.GetHeight())

	def SetSize(self, width, height):

		width = max(self.CORNER_WIDTH*2, width)
		height = max(self.CORNER_HEIGHT*2, height)
		Window.SetSize(self, width, height)

		self.Corners[self.LB].SetPosition(0, height - self.CORNER_HEIGHT)
		self.Corners[self.RT].SetPosition(width - self.CORNER_WIDTH, 0)
		self.Corners[self.RB].SetPosition(width - self.CORNER_WIDTH, height - self.CORNER_HEIGHT)
		self.Lines[self.R].SetPosition(width - self.CORNER_WIDTH, self.CORNER_HEIGHT)
		self.Lines[self.B].SetPosition(self.CORNER_HEIGHT, height - self.CORNER_HEIGHT)

		verticalShowingPercentage = float((height - self.CORNER_HEIGHT*2) - self.LINE_HEIGHT) / self.LINE_HEIGHT
		horizontalShowingPercentage = float((width - self.CORNER_WIDTH*2) - self.LINE_WIDTH) / self.LINE_WIDTH
		self.Lines[self.L].SetRenderingRect(0, 0, 0, verticalShowingPercentage)
		self.Lines[self.R].SetRenderingRect(0, 0, 0, verticalShowingPercentage)
		self.Lines[self.T].SetRenderingRect(0, 0, horizontalShowingPercentage, 0)
		self.Lines[self.B].SetRenderingRect(0, 0, horizontalShowingPercentage, 0)
		self.Base.SetSize(width - self.CORNER_WIDTH*2, height - self.CORNER_HEIGHT*2)

	def ShowInternal(self):
		self.Base.Show()
		for wnd in self.Lines:
			wnd.Show()
		for wnd in self.Corners:
			wnd.Show()

	def HideInternal(self):
		self.Base.Hide()
		for wnd in self.Lines:
			wnd.Hide()
		for wnd in self.Corners:
			wnd.Hide()

class ThinBoardGold(Window):
	CORNER_WIDTH = 16
	CORNER_HEIGHT = 16
	LINE_WIDTH = 16
	LINE_HEIGHT = 16
	BOARD_COLOR = grp.GenerateColor(0.0, 0.0, 0.0, 0.51)

	LT = 0
	LB = 1
	RT = 2
	RB = 3
	L = 0
	R = 1
	T = 2
	B = 3

	def __init__(self, layer = "UI"):
		Window.__init__(self, layer)
		CornerFileNames = [ "d:/ymir work/ui/pattern/thinboardgold/ThinBoard_Corner_"+dir+".tga" for dir in ["LeftTop_gold", "LeftBottom_gold","RightTop_gold", "RightBottom_gold"]]
		LineFileNames = [ "d:/ymir work/ui/pattern/thinboardgold/ThinBoard_Line_"+dir+".tga" for dir in ["Left_gold", "Right_gold", "Top_gold", "Bottom_gold"]]
		
		self.Corners = []
		for fileName in CornerFileNames:
			Corner = ExpandedImageBox()
			Corner.AddFlag("attach")
			Corner.AddFlag("not_pick")
			Corner.LoadImage(fileName)
			Corner.SetParent(self)
			Corner.SetPosition(0, 0)
			Corner.Show()
			self.Corners.append(Corner)

		self.Lines = []
		for fileName in LineFileNames:
			Line = ExpandedImageBox()
			Line.AddFlag("attach")
			Line.AddFlag("not_pick")
			Line.LoadImage(fileName)
			Line.SetParent(self)
			Line.SetPosition(0, 0)
			Line.Show()
			self.Lines.append(Line)

		Base = ExpandedImageBox()
		Base.SetParent(self)
		Base.AddFlag("attach")
		Base.AddFlag("not_pick")
		Base.LoadImage("d:/ymir work/ui/pattern/thinboardgold/thinboard_bg_gold.tga")
		Base.SetPosition(self.CORNER_WIDTH, self.CORNER_HEIGHT)
		Base.Show()
		self.Base = Base

		self.ButtonText = None
		self.BonusId = 0

		self.Lines[self.L].SetPosition(0, self.CORNER_HEIGHT)
		self.Lines[self.T].SetPosition(self.CORNER_WIDTH, 0)

	def __del__(self):
		Window.__del__(self)

	def SetSize(self, width, height):

		width = max(self.CORNER_WIDTH*2, width)
		height = max(self.CORNER_HEIGHT*2, height)
		Window.SetSize(self, width, height)

		self.Corners[self.LB].SetPosition(0, height - self.CORNER_HEIGHT)
		self.Corners[self.RT].SetPosition(width - self.CORNER_WIDTH, 0)
		self.Corners[self.RB].SetPosition(width - self.CORNER_WIDTH, height - self.CORNER_HEIGHT)
		self.Lines[self.R].SetPosition(width - self.CORNER_WIDTH, self.CORNER_HEIGHT)
		self.Lines[self.B].SetPosition(self.CORNER_HEIGHT, height - self.CORNER_HEIGHT)

		verticalShowingPercentage = float((height - self.CORNER_HEIGHT*2) - self.LINE_HEIGHT) / self.LINE_HEIGHT
		horizontalShowingPercentage = float((width - self.CORNER_WIDTH*2) - self.LINE_WIDTH) / self.LINE_WIDTH
		self.Lines[self.L].SetRenderingRect(0, 0, 0, verticalShowingPercentage)
		self.Lines[self.R].SetRenderingRect(0, 0, 0, verticalShowingPercentage)
		self.Lines[self.T].SetRenderingRect(0, 0, horizontalShowingPercentage, 0)
		self.Lines[self.B].SetRenderingRect(0, 0, horizontalShowingPercentage, 0)
		if self.Base:
			self.Base.SetRenderingRect(0, 0, horizontalShowingPercentage, verticalShowingPercentage)

	def SetText(self, text):
		if not self.ButtonText:
			textLine = TextLine()
			textLine.SetParent(self)
			textLine.SetPosition(self.GetWidth()/2, self.GetHeight()/2)
			textLine.SetVerticalAlignCenter()
			textLine.SetHorizontalAlignCenter()
			textLine.Show()
			self.ButtonText = textLine

		self.ButtonText.SetText(text)

	def GetText(self):
		if not self.ButtonText:
			return ""
		return self.ButtonText.GetText()

	def SetBonusId(self, bnsId):
		self.BonusId = bnsId

	def GetBonusId(self):
		if self.BonusId != 0:
			return self.BonusId

	def ShowInternal(self):
		self.Base.Show()
		for wnd in self.Lines:
			wnd.Show()
		for wnd in self.Corners:
			wnd.Show()

	def HideInternal(self):
		self.Base.Hide()
		for wnd in self.Lines:
			wnd.Hide()
		for wnd in self.Corners:
			wnd.Hide()

class ThinBoardCircle(Window):
	CORNER_WIDTH = 4
	CORNER_HEIGHT = 4
	LINE_WIDTH = 4
	LINE_HEIGHT = 4
	BOARD_COLOR = grp.GenerateColor(0.0, 0.0, 0.0, 1.0)

	LT = 0
	LB = 1
	RT = 2
	RB = 3
	L = 0
	R = 1
	T = 2
	B = 3

	def __init__(self, layer = "UI"):
		Window.__init__(self, layer)

		CornerFileNames = [ "d:/ymir work/ui/pattern/thinboardcircle/ThinBoard_Corner_"+dir+"_Circle.tga" for dir in ["LeftTop","LeftBottom","RightTop","RightBottom"] ]
		LineFileNames = [ "d:/ymir work/ui/pattern/thinboardcircle/ThinBoard_Line_"+dir+"_Circle.tga" for dir in ["Left","Right","Top","Bottom"] ]

		self.Corners = []
		for fileName in CornerFileNames:
			Corner = ExpandedImageBox()
			Corner.AddFlag("attach")
			Corner.AddFlag("not_pick")
			Corner.LoadImage(fileName)
			Corner.SetParent(self)
			Corner.SetPosition(0, 0)
			Corner.Show()
			self.Corners.append(Corner)

		self.Lines = []
		for fileName in LineFileNames:
			Line = ExpandedImageBox()
			Line.AddFlag("attach")
			Line.AddFlag("not_pick")
			Line.LoadImage(fileName)
			Line.SetParent(self)
			Line.SetPosition(0, 0)
			Line.Show()
			self.Lines.append(Line)

		Base = Bar()
		Base.SetParent(self)
		Base.AddFlag("attach")
		Base.AddFlag("not_pick")
		Base.SetPosition(self.CORNER_WIDTH, self.CORNER_HEIGHT)
		Base.SetColor(self.BOARD_COLOR)
		Base.Show()
		self.Base = Base

		self.ButtonText = None
		self.BonusId = 0

		self.Lines[self.L].SetPosition(0, self.CORNER_HEIGHT)
		self.Lines[self.T].SetPosition(self.CORNER_WIDTH, 0)

	def __del__(self):
		Window.__del__(self)

	def SetSize(self, width, height):

		width = max(self.CORNER_WIDTH*2, width)
		height = max(self.CORNER_HEIGHT*2, height)
		Window.SetSize(self, width, height)

		self.Corners[self.LB].SetPosition(0, height - self.CORNER_HEIGHT)
		self.Corners[self.RT].SetPosition(width - self.CORNER_WIDTH, 0)
		self.Corners[self.RB].SetPosition(width - self.CORNER_WIDTH, height - self.CORNER_HEIGHT)
		self.Lines[self.R].SetPosition(width - self.CORNER_WIDTH, self.CORNER_HEIGHT)
		self.Lines[self.B].SetPosition(self.CORNER_HEIGHT, height - self.CORNER_HEIGHT)

		verticalShowingPercentage = float((height - self.CORNER_HEIGHT*2) - self.LINE_HEIGHT) / self.LINE_HEIGHT
		horizontalShowingPercentage = float((width - self.CORNER_WIDTH*2) - self.LINE_WIDTH) / self.LINE_WIDTH
		self.Lines[self.L].SetRenderingRect(0, 0, 0, verticalShowingPercentage)
		self.Lines[self.R].SetRenderingRect(0, 0, 0, verticalShowingPercentage)
		self.Lines[self.T].SetRenderingRect(0, 0, horizontalShowingPercentage, 0)
		self.Lines[self.B].SetRenderingRect(0, 0, horizontalShowingPercentage, 0)
		self.Base.SetSize(width - self.CORNER_WIDTH*2, height - self.CORNER_HEIGHT*2)

	def SetText(self, text):
		if not self.ButtonText:
			textLine = TextLine()
			textLine.SetParent(self)
			textLine.SetPosition(self.GetWidth()/2, self.GetHeight()/2)
			textLine.SetVerticalAlignCenter()
			textLine.SetHorizontalAlignCenter()
			textLine.Show()
			self.ButtonText = textLine

		self.ButtonText.SetText(text)

	def GetText(self):
		if not self.ButtonText:
			return ""
		return self.ButtonText.GetText()

	def SetBonusId(self, bnsId):
		self.BonusId = bnsId

	def GetBonusId(self):
		if self.BonusId != 0:
			return self.BonusId

	def ShowInternal(self):
		self.Base.Show()
		for wnd in self.Lines:
			wnd.Show()
		for wnd in self.Corners:
			wnd.Show()

	def HideInternal(self):
		self.Base.Hide()
		for wnd in self.Lines:
			wnd.Hide()
		for wnd in self.Corners:
			wnd.Hide()

class ScrollBar(Window):

	SCROLLBAR_WIDTH = 13
	SCROLLBAR_MIDDLE_HEIGHT = 1
	SCROLLBAR_BUTTON_WIDTH = 17
	SCROLLBAR_BUTTON_HEIGHT = 17
	SCROLL_BTN_XDIST = 2
	SCROLL_BTN_YDIST = 2

	class MiddleBar(DragButton):
		def __init__(self):
			DragButton.__init__(self)
			self.AddFlag("movable")

			self.SetWindowName("scrollbar_middlebar")

		def MakeImage(self):
			top = ExpandedImageBox()
			top.SetParent(self)
			top.LoadImage("d:/ymir work/ui/wiki/scrollbar.tga")
			top.AddFlag("not_pick")
			top.Show()
			topScale = ExpandedImageBox()
			topScale.SetParent(self)
			topScale.SetPosition(0, top.GetHeight())
			topScale.LoadImage("d:/ymir work/ui/wiki/scroll_top.tga")
			topScale.AddFlag("not_pick")
			topScale.Show()

			bottom = ExpandedImageBox()
			bottom.SetParent(self)
			bottom.LoadImage("d:/ymir work/ui/wiki/scrollbar.tga")
			bottom.AddFlag("not_pick")
			bottom.Show()
			bottomScale = ExpandedImageBox()
			bottomScale.SetParent(self)
			bottomScale.LoadImage("d:/ymir work/ui/wiki/scroll_bottom.tga")
			bottomScale.AddFlag("not_pick")
			bottomScale.Show()

			middle = ExpandedImageBox()
			middle.SetParent(self)
			middle.LoadImage("d:/ymir work/ui/wiki/scrollbar.tga")
			middle.AddFlag("not_pick")
			middle.Show()

			self.top = top
			self.topScale = topScale
			self.bottom = bottom
			self.bottomScale = bottomScale
			self.middle = middle

		def Resize(self, height):
			height = max(12, height)
			DragButton.SetSize(self, 10, height)
			self.bottom.SetPosition(0, height-4)

			height -= 4*3
			self.middle.SetRenderingRect(0, 0, 0, float(height)/4.0)

		def SetSize(self, height):
			minHeight = self.top.GetHeight() + self.bottom.GetHeight() + self.middle.GetHeight()
			height = max(minHeight, height)
			DragButton.SetSize(self, 10, height)

			scale = (height - minHeight) / 2 
			extraScale = 0
			if (height - minHeight) % 2 == 1:
				extraScale = 1

			self.topScale.SetRenderingRect(0, 0, 0, scale - 1)
			self.middle.SetPosition(0, self.top.GetHeight() + scale)
			self.bottomScale.SetPosition(0, self.middle.GetBottom())
			self.bottomScale.SetRenderingRect(0, 0, 0, scale - 1 + extraScale)
			self.bottom.SetPosition(0, height - self.bottom.GetHeight())

	def __init__(self):
		Window.__init__(self)

		self.pageSize = 1
		self.curPos = 0.0
		self.eventScroll = None
		self.eventArgs = None
		self.lockFlag = False

		self.CreateScrollBar()
		self.SetScrollBarSize(0)

		self.scrollStep = 0.20
		self.SetWindowName("NONAME_ScrollBar")

	def __del__(self):
		Window.__del__(self)

	def CreateScrollBar(self):
		topImage = ExpandedImageBox()
		topImage.SetParent(self)
		topImage.AddFlag("not_pick")
		topImage.LoadImage("d:/ymir work/ui/wiki/scroll_top.tga")
		topImage.Show()
		
		middleImage = ExpandedImageBox()
		middleImage.SetParent(self)
		middleImage.AddFlag("not_pick")
		middleImage.SetPosition(0, topImage.GetHeight())
		middleImage.LoadImage("d:/ymir work/ui/wiki/scroll_center.tga")
		middleImage.Show()
		
		bottomImage = ExpandedImageBox()
		bottomImage.SetParent(self)
		bottomImage.AddFlag("not_pick")
		bottomImage.LoadImage("d:/ymir work/ui/wiki/scroll_bottom.tga")
		bottomImage.Show()
		
		self.topImage = topImage
		self.bottomImage = bottomImage
		self.middleImage = middleImage

		middleBar = self.MiddleBar()
		middleBar.SetParent(self)
		middleBar.SetMoveEvent(__mem_func__(self.OnMove))
		middleBar.Show()
		middleBar.MakeImage()
		middleBar.SetSize(0) # set min height
		self.middleBar = middleBar

	def Destroy(self):
		self.eventScroll = None
		self.eventArgs = None

	def SetScrollEvent(self, event, *args):
		self.eventScroll = event
		self.eventArgs = args

	def SetMiddleBarSize(self, pageScale):
		self.middleBar.Resize(int(pageScale * float(self.GetHeight() - self.SCROLL_BTN_YDIST*2)))
		realHeight = self.GetHeight() - self.SCROLL_BTN_YDIST*2 - self.middleBar.GetHeight()
		self.pageSize = realHeight

	def SetScrollBarSize(self, height):
		self.SetSize(self.SCROLLBAR_WIDTH, height)

		self.pageSize = height - self.SCROLL_BTN_YDIST*2 - self.middleBar.GetHeight()

		middleImageScale = float((height-3 - self.SCROLL_BTN_YDIST*2) - self.middleImage.GetHeight()) / float(self.middleImage.GetHeight())
		self.middleImage.SetRenderingRect(0, 0, 0, middleImageScale)
		self.bottomImage.SetPosition(0, height-6)

		self.middleBar.SetRestrictMovementArea(self.SCROLL_BTN_XDIST, self.SCROLL_BTN_YDIST, \
			self.middleBar.GetWidth(), height - self.SCROLL_BTN_YDIST * 2)
		self.middleBar.SetPosition(self.SCROLL_BTN_XDIST, self.SCROLL_BTN_YDIST)
		
	def SetScrollStep(self, step):
		self.scrollStep = step
	
	def GetScrollStep(self):
		return self.scrollStep
		
	def GetPos(self):
		return self.curPos

	def OnUp(self):
		self.SetPos(self.curPos-self.scrollStep)

	def OnDown(self):
		self.SetPos(self.curPos+self.scrollStep)

	def SetPos(self, pos, moveEvent = True):
		pos = max(0.0, pos)
		pos = min(1.0, pos)

		newPos = float(self.pageSize) * pos
		self.middleBar.SetPosition(self.SCROLL_BTN_XDIST, int(newPos) + self.SCROLL_BTN_YDIST)
		if moveEvent == True:
			self.OnMove()

	def OnMove(self):

		if self.lockFlag:
			return

		if 0 == self.pageSize:
			return

		(xLocal, yLocal) = self.middleBar.GetLocalPosition()
		self.curPos = float(yLocal - self.SCROLL_BTN_YDIST) / float(self.pageSize)

		if self.eventScroll:
			apply(self.eventScroll, self.eventArgs)

	def OnMouseLeftButtonDown(self):
		(xMouseLocalPosition, yMouseLocalPosition) = self.GetMouseLocalPosition()
		newPos = float(yMouseLocalPosition) / float(self.GetHeight())
		self.SetPos(newPos)

	def LockScroll(self):
		self.lockFlag = True

	def UnlockScroll(self):
		self.lockFlag = False
		
if app.ENABLE_SWITCHBOT_WORLDARD:
	class ScrollBarNew(Window):
		MIDDLE_BAR_POS = 4
		SCROLLBAR_BUTTON_HEIGHT = 0
		SCROLLBAR_WIDTH = 8
		SCROLLBAR_MIDDLE_HEIGHT = 33

		class MiddleBar(DragButton):
			def __init__(self):
				DragButton.__init__(self)
				self.AddFlag("movable")

			def MakeImage(self):
				bar = ImageBox()
				bar.SetParent(self)
				bar.LoadImage("Switchbot/design/scroll_button_1.tga")
				bar.SetPosition(0, 0)
				bar.AddFlag("not_pick")
				bar.Show()

				self.bar = bar

			def SetSize(self, height):
				height = max(12, height)
				DragButton.SetSize(self, 10, height)

				height -= 4*3

		def __init__(self):
			Window.__init__(self)

			self.pageSize = 1
			self.curPos = 0.0
			self.eventScroll = lambda *arg: None
			self.lockFlag = False
			self.scrollStep = 0.20


			self.CreateScrollBar()

		def __del__(self):
			Window.__del__(self)

		def CreateScrollBar(self):
			barSlot = ImageBox()
			barSlot.SetParent(self)
			barSlot.AddFlag("not_pick")
			barSlot.LoadImage("Switchbot/design/scroll_background.tga")
			barSlot.Show()

			middleBar = self.MiddleBar()
			middleBar.SetParent(self)
			middleBar.SetMoveEvent(__mem_func__(self.OnMove))
			middleBar.Show()
			middleBar.MakeImage()
			middleBar.SetSize(33)

			self.middleBar = middleBar
			self.barSlot = barSlot

			self.SCROLLBAR_MIDDLE_HEIGHT = self.middleBar.GetHeight()


		def Destroy(self):
			self.middleBar = None
			self.eventScroll = lambda *arg: None

		def SetScrollEvent(self, event):
			self.eventScroll = event

		def GetPos(self):
			return self.curPos

		def SetPos(self, pos):
			pos = max(0.0, pos)
			pos = min(1.0, pos)

			newPos = float(self.pageSize) * pos
			self.middleBar.SetPosition(self.MIDDLE_BAR_POS, int(newPos))
			self.OnMove()


		def SetScrollBarSize(self, height):
			self.pageSize = height- self.SCROLLBAR_MIDDLE_HEIGHT
			self.SetSize(self.SCROLLBAR_WIDTH, height)
			self.middleBar.SetRestrictMovementArea(self.MIDDLE_BAR_POS, 0, 8, 156)
			self.middleBar.SetPosition(self.MIDDLE_BAR_POS, 0)

			self.UpdateBarSlot()

		def UpdateBarSlot(self):
			self.barSlot.SetPosition(0, self.SCROLLBAR_BUTTON_HEIGHT)

		def SetScrollStep(self, step):
			self.scrollStep = step

		def GetScrollStep(self):
			return self.scrollStep

		def OnUp(self):
			self.SetPos(self.curPos-self.scrollStep)

		def OnDown(self):
			self.SetPos(self.curPos+self.scrollStep)

		def OnMove(self):

			if self.lockFlag:
				return

			if 0 == self.pageSize:
				return

			(xLocal, yLocal) = self.middleBar.GetLocalPosition()
			self.curPos = float(yLocal) / float(self.pageSize)

			self.eventScroll()

		def OnMouseLeftButtonDown(self):
			(xMouseLocalPosition, yMouseLocalPosition) = self.GetMouseLocalPosition()
			pickedPos = yMouseLocalPosition  - self.SCROLLBAR_MIDDLE_HEIGHT/2
			newPos = float(pickedPos) / float(self.pageSize)
			self.SetPos(newPos)

		def LockScroll(self):
			self.lockFlag = True

		def UnlockScroll(self):
			self.lockFlag = False
			
class HorizontalScrollBar(Window):
	WINDOW_HEIGHT = 15
	CORRECT_MIDDLE_BAR_Y = 1
	CORRECT_MIDDLE_BAR_WIDTH = 4
	CORRECT_Y_POS = 3

	class MiddleBar(DragButton):
		def __init__(self):
			DragButton.__init__(self)
			self.AddFlag("movable")

		def MakeImage(self):
			left = ImageBox()
			left.SetParent(self)
			left.LoadImage("d:/ymir work/ui/pattern/horizontal_scrollbar_left.tga")
			left.SetPosition(0, 0)
			left.AddFlag("not_pick")
			left.Show()

			right = ImageBox()
			right.SetParent(self)
			right.LoadImage("d:/ymir work/ui/pattern/horizontal_scrollbar_right.tga")
			right.AddFlag("not_pick")
			right.Show()

			middle = ExpandedImageBox()
			middle.SetParent(self)
			middle.LoadImage("d:/ymir work/ui/pattern/horizontal_scrollbar_middle.tga")
			middle.SetPosition(left.GetWidth() - 1, 0)
			middle.AddFlag("not_pick")
			middle.Show()

			self.left = left
			self.right = right
			self.middle = middle

		def SetSize(self, width):
			width = max(4, width)
			DragButton.SetSize(self, width, HorizontalScrollBar.WINDOW_HEIGHT)
			self.right.SetPosition(width, 0)

			width -= self.right.GetWidth()
			self.middle.SetRenderingRect(0, 0, float(width) / 4.0, 0.0)

	def __init__(self):
		Window.__init__(self)

		self.pageSize = 1
		self.curPos = 0.0
		self.eventScroll = lambda *arg: None
		self.lockFlag = False
		self.scrollStep = 0.20

		self.CreateScrollBar()

	def __del__(self):
		Window.__del__(self)

	def CreateScrollBar(self):
		barSlot = Bar3D()
		barSlot.SetParent(self)
		barSlot.AddFlag("not_pick")
		barSlot.Show()

		middleBar = self.MiddleBar()
		middleBar.SetParent(self)
		middleBar.SetMoveEvent(__mem_func__(self.OnMove))
		middleBar.Show()
		middleBar.MakeImage()
		middleBar.SetSize(12)

		leftButton = Button()
		leftButton.SetParent(self)
		leftButton.SetEvent(__mem_func__(self.OnUp))
		leftButton.SetUpVisual("d:/ymir work/ui/public/scrollbar_left_button_01.sub")
		leftButton.SetOverVisual("d:/ymir work/ui/public/scrollbar_left_button_02.sub")
		leftButton.SetDownVisual("d:/ymir work/ui/public/scrollbar_left_button_03.sub")
		leftButton.Show()

		rightButton = Button()
		rightButton.SetParent(self)
		rightButton.SetEvent(__mem_func__(self.OnDown))
		rightButton.SetUpVisual("d:/ymir work/ui/public/scrollbar_right_button_01.sub")
		rightButton.SetOverVisual("d:/ymir work/ui/public/scrollbar_right_button_02.sub")
		rightButton.SetDownVisual("d:/ymir work/ui/public/scrollbar_right_button_03.sub")
		rightButton.Show()

		self.leftButton = leftButton
		self.rightButton = rightButton
		self.middleBar = middleBar
		self.barSlot = barSlot

		self.LEFT_BUTTON_WIDTH = self.leftButton.GetWidth()
		self.LEFT_BUTTON_WIDTH += 1
		self.MID_SCROLLBAR_WIDTH = self.middleBar.GetWidth()

	def Destroy(self):
		self.barSlot = None
		self.middleBar = None
		self.leftButton = None
		self.rightButton = None

		self.eventScroll = lambda *arg: None

	def SetScrollEvent(self, event):
		self.eventScroll = event

	def SetMiddleBarSize(self, pageScale):
		realWidth = self.GetWidth() - self.LEFT_BUTTON_WIDTH * 2
		self.MID_SCROLLBAR_WIDTH = int(pageScale * float(realWidth))
		self.middleBar.SetSize(self.MID_SCROLLBAR_WIDTH)
		self.pageSize = (self.GetWidth() - self.LEFT_BUTTON_WIDTH * 2) - self.MID_SCROLLBAR_WIDTH - self.CORRECT_MIDDLE_BAR_WIDTH

	def SetScrollBarSize(self, width):
		self.pageSize = (width - self.LEFT_BUTTON_WIDTH * 2) - self.MID_SCROLLBAR_WIDTH - self.CORRECT_MIDDLE_BAR_WIDTH
		self.SetSize(width, self.WINDOW_HEIGHT)
		self.leftButton.SetPosition(0, self.CORRECT_MIDDLE_BAR_Y)
		self.rightButton.SetPosition(width - self.LEFT_BUTTON_WIDTH + 1, self.CORRECT_MIDDLE_BAR_Y)

		self.middleBar.SetRestrictMovementArea(
			self.LEFT_BUTTON_WIDTH,
			self.CORRECT_Y_POS,
			width - self.LEFT_BUTTON_WIDTH * 2 - self.CORRECT_MIDDLE_BAR_WIDTH,
			self.WINDOW_HEIGHT,
		)

		self.middleBar.SetPosition(self.LEFT_BUTTON_WIDTH, self.CORRECT_MIDDLE_BAR_Y)
		self.UpdateBarSlot()

	def UpdateBarSlot(self):
		self.barSlot.SetPosition(self.LEFT_BUTTON_WIDTH, 0)
		self.barSlot.SetSize(self.GetWidth() - self.LEFT_BUTTON_WIDTH * 2, self.GetHeight())

	def GetPos(self):
		return self.curPos

	def SetPos(self, pos):
		pos = max(0.0, pos)
		pos = min(1.0, pos)

		newPos = float(self.pageSize) * pos
		self.middleBar.SetPosition(self.LEFT_BUTTON_WIDTH + int(newPos), self.CORRECT_Y_POS)
		self.OnMove()

	def SetScrollStep(self, step):
		self.scrollStep = step
	
	def GetScrollStep(self):
		return self.scrollStep

	def OnUp(self):
		self.SetPos(self.curPos - self.scrollStep)

	def OnDown(self):
		self.SetPos(self.curPos + self.scrollStep)
	
	def OnMove(self):
		if self.lockFlag:
			return

		if 0 == self.pageSize:
			return

		(xLocal, yLocal) = self.middleBar.GetLocalPosition()
		self.curPos = float(xLocal - self.LEFT_BUTTON_WIDTH) / float(self.pageSize)

		if self.eventScroll:
			self.eventScroll()

	def OnMouseLeftButtonDown(self):
		(xMouseLocalPosition, yMouseLocalPosition) = self.GetMouseLocalPosition()
		pickedPos = xMouseLocalPosition - self.LEFT_BUTTON_WIDTH - self.MID_SCROLLBAR_WIDTH / 2
		newPos = float(pickedPos) / float(self.pageSize)

		self.SetPos(newPos)

	def LockScroll(self):
		self.lockFlag = True

	def UnlockScroll(self):
		self.lockFlag = False

class ThinScrollBar(ScrollBar):

	# def CreateScrollBar(self):
		# middleBar = self.MiddleBar()
		# middleBar.SetParent(self)
		# middleBar.SetMoveEvent(__mem_func__(self.OnMove))
		# middleBar.Show()
		# middleBar.SetUpVisual("d:/ymir work/ui/public/scrollbar_thin_middle_button_01.sub")
		# middleBar.SetOverVisual("d:/ymir work/ui/public/scrollbar_thin_middle_button_02.sub")
		# middleBar.SetDownVisual("d:/ymir work/ui/public/scrollbar_thin_middle_button_03.sub")

		# upButton = Button()
		# upButton.SetParent(self)
		# upButton.SetUpVisual("d:/ymir work/ui/public/scrollbar_thin_up_button_01.sub")
		# upButton.SetOverVisual("d:/ymir work/ui/public/scrollbar_thin_up_button_02.sub")
		# upButton.SetDownVisual("d:/ymir work/ui/public/scrollbar_thin_up_button_03.sub")
		# upButton.SetEvent(__mem_func__(self.OnUp))
		# upButton.Show()

		# downButton = Button()
		# downButton.SetParent(self)
		# downButton.SetUpVisual("d:/ymir work/ui/public/scrollbar_thin_down_button_01.sub")
		# downButton.SetOverVisual("d:/ymir work/ui/public/scrollbar_thin_down_button_02.sub")
		# downButton.SetDownVisual("d:/ymir work/ui/public/scrollbar_thin_down_button_03.sub")
		# downButton.SetEvent(__mem_func__(self.OnDown))
		# downButton.Show()

		# self.middleBar = middleBar
		# self.upButton = upButton
		# self.downButton = downButton

		# self.SCROLLBAR_WIDTH = self.upButton.GetWidth()
		# self.SCROLLBAR_MIDDLE_HEIGHT = self.middleBar.GetHeight()
		# self.SCROLLBAR_BUTTON_WIDTH = self.upButton.GetWidth()
		# self.SCROLLBAR_BUTTON_HEIGHT = self.upButton.GetHeight()
		# self.MIDDLE_BAR_POS = 0
		# self.MIDDLE_BAR_UPPER_PLACE = 0
		# self.MIDDLE_BAR_DOWNER_PLACE = 0
		# self.TEMP_SPACE = 0

	def UpdateBarSlot(self):
		pass

class SmallThinScrollBar(ScrollBar):

	# def CreateScrollBar(self):
		# middleBar = self.MiddleBar()
		# middleBar.SetParent(self)
		# middleBar.SetMoveEvent(__mem_func__(self.OnMove))
		# middleBar.Show()
		# middleBar.SetUpVisual("d:/ymir work/ui/public/scrollbar_small_thin_middle_button_01.sub")
		# middleBar.SetOverVisual("d:/ymir work/ui/public/scrollbar_small_thin_middle_button_01.sub")
		# middleBar.SetDownVisual("d:/ymir work/ui/public/scrollbar_small_thin_middle_button_01.sub")

		# upButton = Button()
		# upButton.SetParent(self)
		# upButton.SetUpVisual("d:/ymir work/ui/public/scrollbar_small_thin_up_button_01.sub")
		# upButton.SetOverVisual("d:/ymir work/ui/public/scrollbar_small_thin_up_button_02.sub")
		# upButton.SetDownVisual("d:/ymir work/ui/public/scrollbar_small_thin_up_button_03.sub")
		# upButton.SetEvent(__mem_func__(self.OnUp))
		# upButton.Show()

		# downButton = Button()
		# downButton.SetParent(self)
		# downButton.SetUpVisual("d:/ymir work/ui/public/scrollbar_small_thin_down_button_01.sub")
		# downButton.SetOverVisual("d:/ymir work/ui/public/scrollbar_small_thin_down_button_02.sub")
		# downButton.SetDownVisual("d:/ymir work/ui/public/scrollbar_small_thin_down_button_03.sub")
		# downButton.SetEvent(__mem_func__(self.OnDown))
		# downButton.Show()

		# self.middleBar = middleBar
		# self.upButton = upButton
		# self.downButton = downButton

		# self.SCROLLBAR_WIDTH = self.upButton.GetWidth()
		# self.SCROLLBAR_MIDDLE_HEIGHT = self.middleBar.GetHeight()
		# self.SCROLLBAR_BUTTON_WIDTH = self.upButton.GetWidth()
		# self.SCROLLBAR_BUTTON_HEIGHT = self.upButton.GetHeight()
		# self.MIDDLE_BAR_POS = 0
		# self.MIDDLE_BAR_UPPER_PLACE = 0
		# self.MIDDLE_BAR_DOWNER_PLACE = 0
		# self.TEMP_SPACE = 0

	def UpdateBarSlot(self):
		pass

class SliderBar(Window):

	def __init__(self):
		Window.__init__(self)

		self.curPos = 1.0
		self.pageSize = 1.0
		self.eventChange = None

		self.__CreateBackGroundImage()
		self.__CreateCursor()

	def __del__(self):
		Window.__del__(self)

	def __CreateBackGroundImage(self):
		img = ImageBox()
		img.SetParent(self)
		img.LoadImage("d:/ymir work/ui/game/windows/sliderbar.sub")
		img.Show()
		self.backGroundImage = img

		##
		self.SetSize(self.backGroundImage.GetWidth(), self.backGroundImage.GetHeight())

	def __CreateCursor(self):
		cursor = DragButton()
		cursor.AddFlag("movable")
		cursor.AddFlag("restrict_y")
		cursor.SetParent(self)
		cursor.SetMoveEvent(__mem_func__(self.__OnMove))
		cursor.SetUpVisual("d:/ymir work/ui/game/windows/sliderbar_cursor.sub")
		cursor.SetOverVisual("d:/ymir work/ui/game/windows/sliderbar_cursor.sub")
		cursor.SetDownVisual("d:/ymir work/ui/game/windows/sliderbar_cursor.sub")
		cursor.Show()
		self.cursor = cursor

		##
		self.cursor.SetRestrictMovementArea(0, 0, self.backGroundImage.GetWidth(), 0)
		self.pageSize = self.backGroundImage.GetWidth() - self.cursor.GetWidth()

	def __OnMove(self):
		(xLocal, yLocal) = self.cursor.GetLocalPosition()
		self.curPos = float(xLocal) / float(self.pageSize)

		if self.eventChange:
			self.eventChange()

	def SetSliderPos(self, pos):
		self.curPos = pos
		self.cursor.SetPosition(int(self.pageSize * pos), 0)

	def GetSliderPos(self):
		return self.curPos

	def SetEvent(self, event):
		self.eventChange = event

	def Enable(self):
		self.cursor.Show()

	def Disable(self):
		self.cursor.Hide()

class ListBox(Window):

	TEMPORARY_PLACE = 3

	def __init__(self, layer = "UI"):
		Window.__init__(self, layer)
		self.overLine = -1
		self.selectedLine = -1
		self.width = 0
		self.height = 0
		self.stepSize = 17
		self.basePos = 0
		self.showLineCount = 0
		self.itemCenterAlign = True
		self.itemList = []
		self.keyDict = {}
		self.textDict = {}
		self.event = lambda *arg: None
	def __del__(self):
		Window.__del__(self)

	def SetWidth(self, width):
		self.SetSize(width, self.height)

	def SetSize(self, width, height):
		Window.SetSize(self, width, height)
		self.width = width
		self.height = height

	def SetTextCenterAlign(self, flag):
		self.itemCenterAlign = flag

	def SetBasePos(self, pos):
		self.basePos = pos
		self._LocateItem()

	def ClearItem(self):
		self.keyDict = {}
		self.textDict = {}
		self.itemList = []
		self.overLine = -1
		self.selectedLine = -1

	def InsertItem(self, number, text):
		self.keyDict[len(self.itemList)] = number
		self.textDict[len(self.itemList)] = text

		textLine = TextLine()
		textLine.SetParent(self)
		textLine.SetText(text)
		textLine.Show()

		if self.itemCenterAlign:
			textLine.SetWindowHorizontalAlignCenter()
			textLine.SetHorizontalAlignCenter()

		self.itemList.append(textLine)

		self._LocateItem()

	def ChangeItem(self, number, text):
		for key, value in self.keyDict.items():
			if value == number:
				self.textDict[key] = text

				if number < len(self.itemList):
					self.itemList[key].SetText(text)

				return

	def LocateItem(self):
		self._LocateItem()

	def _LocateItem(self):

		skipCount = self.basePos
		yPos = 0
		self.showLineCount = 0

		for textLine in self.itemList:
			textLine.Hide()

			if skipCount > 0:
				skipCount -= 1
				continue

			textLine.SetPosition(0, yPos + 3)

			yPos += self.stepSize

			if yPos <= self.GetHeight():
				self.showLineCount += 1
				textLine.Show()

	def ArrangeItem(self):
		self.SetSize(self.width, len(self.itemList) * self.stepSize)
		self._LocateItem()

	def GetViewItemCount(self):
		return int(self.GetHeight() / self.stepSize)

	def GetItemCount(self):
		return len(self.itemList)

	def SetEvent(self, event):
		self.event = event

	def SelectItem(self, line):

		if not self.keyDict.has_key(line):
			return

		if line == self.selectedLine:
			return

		self.selectedLine = line
		self.event(self.keyDict.get(line, 0), self.textDict.get(line, "None"))

	def GetSelectedItem(self):
		return self.keyDict.get(self.selectedLine, 0)
		
	if app.ENABLE_SEARCH_SHOP:
		def GetSelectedItemText(self):
			return self.textDict.get(self.selectedLine, "")

	def OnMouseLeftButtonDown(self):
		if self.overLine < 0:
			return

	def OnMouseLeftButtonUp(self):
		if self.overLine >= 0:
			self.SelectItem(self.overLine+self.basePos)

	def OnUpdate(self):

		self.overLine = -1

		if self.IsIn():
			x, y = self.GetGlobalPosition()
			height = self.GetHeight()
			xMouse, yMouse = wndMgr.GetMousePosition()

			if yMouse - y < height - 1:
				self.overLine = (yMouse - y) / self.stepSize

				if self.overLine < 0:
					self.overLine = -1
				if self.overLine >= len(self.itemList):
					self.overLine = -1

	def OnRender(self):
		xRender, yRender = self.GetGlobalPosition()
		yRender -= self.TEMPORARY_PLACE
		widthRender = self.width
		heightRender = self.height + self.TEMPORARY_PLACE*2

		if -1 != self.overLine:
			grp.SetColor(HALF_WHITE_COLOR)
			grp.RenderBar(xRender + 2, yRender + self.overLine*self.stepSize + 4, self.width - 3, self.stepSize)

		if -1 != self.selectedLine:
			if self.selectedLine >= self.basePos:
				if self.selectedLine - self.basePos < self.showLineCount:
					grp.SetColor(SELECT_COLOR)
					grp.RenderBar(xRender + 2, yRender + (self.selectedLine-self.basePos)*self.stepSize + 4, self.width - 3, self.stepSize)



class ListBox2(ListBox):
	def __init__(self, *args, **kwargs):
		ListBox.__init__(self, *args, **kwargs)
		self.rowCount = 10
		self.barWidth = 0
		self.colCount = 0

	def SetRowCount(self, rowCount):
		self.rowCount = rowCount

	def SetSize(self, width, height):
		ListBox.SetSize(self, width, height)
		self._RefreshForm()

	def ClearItem(self):
		ListBox.ClearItem(self)
		self._RefreshForm()

	def InsertItem(self, *args, **kwargs):
		ListBox.InsertItem(self, *args, **kwargs)
		self._RefreshForm()

	def OnUpdate(self):
		mpos = wndMgr.GetMousePosition()
		self.overLine = self._CalcPointIndex(mpos)

	def OnRender(self):
		x, y = self.GetGlobalPosition()
		pos = (x + 2, y)

		if -1 != self.overLine:
			grp.SetColor(HALF_WHITE_COLOR)
			self._RenderBar(pos, self.overLine)

		if -1 != self.selectedLine:
			if self.selectedLine >= self.basePos:
				if self.selectedLine - self.basePos < self.showLineCount:
					grp.SetColor(SELECT_COLOR)
					self._RenderBar(pos, self.selectedLine-self.basePos)



	def _CalcPointIndex(self, mpos):
		if self.IsIn():
			px, py = mpos
			gx, gy = self.GetGlobalPosition()
			lx, ly = px - gx, py - gy

			col = lx / self.barWidth
			row = ly / self.stepSize
			idx = col * self.rowCount + row
			if col >= 0 and col < self.colCount:
				if row >= 0 and row < self.rowCount:
					if idx >= 0 and idx < len(self.itemList):
						return idx

		return -1

	def _CalcRenderPos(self, pos, idx):
		x, y = pos
		row = idx % self.rowCount
		col = idx / self.rowCount
		return (x + col * self.barWidth, y + row * self.stepSize)

	def _RenderBar(self, basePos, idx):
		x, y = self._CalcRenderPos(basePos, idx)
		grp.RenderBar(x, y, self.barWidth - 3, self.stepSize)

	def _LocateItem(self):
		pos = (0, self.TEMPORARY_PLACE)

		self.showLineCount = 0
		for textLine in self.itemList:
			x, y = self._CalcRenderPos(pos, self.showLineCount)
			textLine.SetPosition(x, y)
			textLine.Show()

			self.showLineCount += 1

	def _RefreshForm(self):
		if len(self.itemList) % self.rowCount:
			self.colCount = len(self.itemList) / self.rowCount + 1
		else:
			self.colCount = len(self.itemList) / self.rowCount

		if self.colCount:
			self.barWidth = self.width / self.colCount
		else:
			self.barWidth = self.width


class ComboBox(Window):

	class ListBoxWithBoard(ListBox):

		def __init__(self, layer):
			ListBox.__init__(self, layer)

		def OnRender(self):
			xRender, yRender = self.GetGlobalPosition()
			yRender -= self.TEMPORARY_PLACE
			widthRender = self.width
			heightRender = self.height + self.TEMPORARY_PLACE*2
			grp.SetColor(BACKGROUND_COLOR)
			grp.RenderBar(xRender, yRender, widthRender, heightRender)
			grp.SetColor(DARK_COLOR)
			grp.RenderLine(xRender, yRender, widthRender, 0)
			grp.RenderLine(xRender, yRender, 0, heightRender)
			grp.SetColor(BRIGHT_COLOR)
			grp.RenderLine(xRender, yRender+heightRender, widthRender, 0)
			grp.RenderLine(xRender+widthRender, yRender, 0, heightRender)

			ListBox.OnRender(self)

	def __init__(self):
		Window.__init__(self)
		self.x = 0
		self.y = 0
		self.width = 0
		self.height = 0
		self.isSelected = False
		self.isOver = False
		self.isListOpened = False
		self.event = lambda *arg: None
		self.clickevent = lambda *arg : None
		self.clickeventArgs = None
		self.enable = True

		self.textLine = MakeTextLine(self)
		self.textLine.SetText(localeInfo.UI_ITEM)

		self.listBox = self.ListBoxWithBoard("TOP_MOST")
		self.listBox.SetPickAlways()
		self.listBox.SetParent(self)
		self.listBox.SetEvent(__mem_func__(self.OnSelectItem))
		self.listBox.Hide()

	def __del__(self):
		Window.__del__(self)

	def Destroy(self):
		self.textLine = None
		self.listBox = None

	def SetPosition(self, x, y):
		Window.SetPosition(self, x, y)
		self.x = x
		self.y = y
		self.__ArrangeListBox()

	def SetSize(self, width, height):
		Window.SetSize(self, width, height)
		self.width = width
		self.height = height
		self.textLine.UpdateRect()
		self.__ArrangeListBox()

	def __ArrangeListBox(self):
		self.listBox.SetPosition(0, self.height + 5)
		self.listBox.SetWidth(self.width)

	def Enable(self):
		self.enable = True

	def Disable(self):
		self.enable = False
		self.textLine.SetText("")
		self.CloseListBox()

	def SetEvent(self, event):
		self.event = event
    
	def SetOnClickEvent(self, event, wnds):
		self.clickevent = event
		self.clickeventArgs = wnds
    
	def ClearItem(self):
		self.CloseListBox()
		self.listBox.ClearItem()

	def InsertItem(self, index, name):
		self.listBox.InsertItem(index, name)
		self.listBox.ArrangeItem()

	def SetCurrentItem(self, text):
		self.textLine.SetText(text)

	def SelectItem(self, key):
		self.listBox.SelectItem(key)

	def OnSelectItem(self, index, name):

		self.CloseListBox()
		self.event(index)

	def CloseListBox(self):
		self.isListOpened = False
		self.listBox.Hide()

	def OnMouseLeftButtonDown(self):

		if not self.enable:
			return

		self.isSelected = True
		if self.clickevent:
			self.clickevent(self.clickeventArgs)

	def OnMouseLeftButtonUp(self):

		if not self.enable:
			return

		self.isSelected = False

		if self.isListOpened:
			self.CloseListBox()
		else:
			if self.listBox.GetItemCount() > 0:
				self.isListOpened = True
				self.listBox.Show()
				self.__ArrangeListBox()

	def OnUpdate(self):

		if not self.enable:
			return

		if self.IsIn():
			self.isOver = True
		else:
			self.isOver = False

	def OnRender(self):
		self.x, self.y = self.GetGlobalPosition()
		xRender = self.x
		yRender = self.y
		widthRender = self.width
		heightRender = self.height
		grp.SetColor(BACKGROUND_COLOR)
		grp.RenderBar(xRender, yRender, widthRender, heightRender)
		grp.SetColor(DARK_COLOR)
		grp.RenderLine(xRender, yRender, widthRender, 0)
		grp.RenderLine(xRender, yRender, 0, heightRender)
		grp.SetColor(BRIGHT_COLOR)
		grp.RenderLine(xRender, yRender+heightRender, widthRender, 0)
		grp.RenderLine(xRender+widthRender, yRender, 0, heightRender)

		if self.isOver:
			grp.SetColor(HALF_WHITE_COLOR)
			grp.RenderBar(xRender + 2, yRender + 3, self.width - 3, heightRender - 5)

			if self.isSelected:
				grp.SetColor(WHITE_COLOR)
				grp.RenderBar(xRender + 2, yRender + 3, self.width - 3, heightRender - 5)

###################################################################################################
## Python Script Loader
###################################################################################################

class ScriptWindow(Window):
	def __init__(self, layer = "UI"):
		Window.__init__(self, layer)
		self.Children = []
		self.ElementDictionary = {}		
		
	def __del__(self):
		Window.__del__(self)

	def ClearDictionary(self):
		self.Children = []
		self.ElementDictionary = {}
		
	def InsertChild(self, name, child):
		self.ElementDictionary[name] = child

	def IsChild(self, name):
		return self.ElementDictionary.has_key(name)
	def GetChild(self, name):
		return self.ElementDictionary[name]

	def GetChild2(self, name):
		return self.ElementDictionary.get(name, None)

class PythonScriptLoader(object):

	BODY_KEY_LIST = ( "x", "y", "width", "height" )

	#####

	DEFAULT_KEY_LIST = ( "type", "x", "y", )
	WINDOW_KEY_LIST = ( "width", "height", )
	IMAGE_KEY_LIST = ( "image", )
	EXPANDED_IMAGE_KEY_LIST = ( "image", )
	ANI_IMAGE_KEY_LIST = ( "images", )
	SLOT_KEY_LIST = ( "width", "height", "slot", )
	CANDIDATE_LIST_KEY_LIST = ( "item_step", "item_xsize", "item_ysize", )
	GRID_TABLE_KEY_LIST = ( "start_index", "x_count", "y_count", "x_step", "y_step", )
	EDIT_LINE_KEY_LIST = ( "width", "height", "input_limit", )
	COMBO_BOX_KEY_LIST = ( "width", "height", "item", )
	TITLE_BAR_KEY_LIST = ( "width", )
	HORIZONTAL_BAR_KEY_LIST = ( "width", )
	BOARD_KEY_LIST = ( "width", "height", )
	BOARD_WITH_TITLEBAR_KEY_LIST = ( "width", "height", "title", )
	BOX_KEY_LIST = ( "width", "height", )
	BAR_KEY_LIST = ( "width", "height", )
	LINE_KEY_LIST = ( "width", "height", )
	SLOTBAR_KEY_LIST = ( "width", "height", )
	GAUGE_KEY_LIST = ( "width", "color", )
	SCROLLBAR_KEY_LIST = ( "size", )
	LIST_BOX_KEY_LIST = ( "width", "height", )
	RENDER_TARGET_KEY_LIST = ( "index", )

	def __init__(self):
		self.Clear()

	def Clear(self):
		self.ScriptDictionary = { "SCREEN_WIDTH" : wndMgr.GetScreenWidth(), "SCREEN_HEIGHT" : wndMgr.GetScreenHeight() }
		self.InsertFunction = 0

	def LoadScriptFile(self, window, FileName):
		import exception
		import exceptions
		import os
		import errno
		self.Clear()

		import sys
		from utils import Sandbox
		sandbox = Sandbox(True, ["uiScriptLocale", "localeInfo", "sys", "item", "app"])
		import Collision as chr
		import CacheEffect as player
		import app

		self.ScriptDictionary["PLAYER_NAME_MAX_LEN"] = chr.PLAYER_NAME_MAX_LEN
		self.ScriptDictionary["DRAGON_SOUL_EQUIPMENT_SLOT_START"] = player.DRAGON_SOUL_EQUIPMENT_SLOT_START
		# self.ScriptDictionary["LOCALE_PATH"] = app.GetLocalePath()

		if __USE_UISCRIPT_CYTHON__:
			import os
			from os.path import splitext as op_splitext, basename as op_basename, dirname as op_dirname
			def GetModName(filename):
				return op_splitext(op_basename(filename))[0]
			def IsInUiPath(filename):
				def ICmp(s1, s2):
					return s1.lower() == s2.lower()
				return ICmp(op_dirname(filename), "uiscript")

			modname = GetModName(FileName)

			import uiscriptlib

			# tpl2Main = ("SCREEN_WIDTH","SCREEN_HEIGHT")
			
			tpl2Main = (
				"SCREEN_WIDTH","SCREEN_HEIGHT",
				"PLAYER_NAME_MAX_LEN", "DRAGON_SOUL_EQUIPMENT_SLOT_START"
			)
			
			for idx in tpl2Main:
				tmpVal = self.ScriptDictionary[idx]
				try:
					exec "bt.%s = tmpVal"%idx in globals(), locals()
				except:
					continue

		try:
			if __USE_UISCRIPT_CYTHON__ and IsInUiPath(FileName) and uiscriptlib.isExist(modname):
				m1 = uiscriptlib.moduleImport(modname)
				self.ScriptDictionary["window"] = m1.window.copy()
				del m1
			else:
				sandbox.execfile(FileName, self.ScriptDictionary)
		except IOError, err:
			import dbg
			dbg.TraceError("Failed to load script file : %s" % FileName)
			dbg.TraceError("error  : %s" % err)
			exception.Abort("LoadScriptFile1")
		except RuntimeError,err:
			import dbg
			dbg.TraceError("Failed to load script file : %s" % FileName)
			dbg.TraceError("error  : %s" % err)
			exception.Abort("LoadScriptFile2")
		except:
			import dbg
			dbg.TraceError("Failed to load script file : %s" % FileName)
			dbg.TraceError("%s" % sys.exc_info()[0])
			dbg.TraceError("%s" % str(sys.exc_info()))
			exception.Abort("LoadScriptFile test !!!!!!!!!!!!!!")

		#####

		try:
			Body = self.ScriptDictionary["window"]
		except:
			import exception
			exception.Abort("Something went wrong at file: %s" % (str(FileName)))
		self.CheckKeyList("window", Body, self.BODY_KEY_LIST)

		window.ClearDictionary()
		self.InsertFunction = window.InsertChild

		window.SetPosition(int(Body["x"]), int(Body["y"]))
		window.SetSize(int(Body["width"]), int(Body["height"]))
		if True == Body.has_key("style"):
			for StyleList in Body["style"]:
				window.AddFlag(StyleList)
		
		#NEW_ANIMATION
		# if True == Body.has_key("animation"):
				# window.bAnim = True
		#NEW_ANIMATION

		self.LoadChildren(window, Body)

	def LoadChildren(self, parent, dicChildren):

		if True == dicChildren.has_key("style"):
			for style in dicChildren["style"]:
				parent.AddFlag(style)

		if False == dicChildren.has_key("children"):
			return False

		Index = 0

		ChildrenList = dicChildren["children"]
		parent.Children = range(len(ChildrenList))
		for ElementValue in ChildrenList:
			try:
				Name = ElementValue["name"]
			except KeyError:
				Name = ElementValue["name"] = "NONAME"

			try:
				Type = ElementValue["type"]
			except KeyError:
				Type = ElementValue["type"] = "window"

			if False == self.CheckKeyList(Name, ElementValue, self.DEFAULT_KEY_LIST):
				del parent.Children[Index]
				continue

			if Type == "window":
				parent.Children[Index] = ScriptWindow()
				parent.Children[Index].SetParent(parent)
				self.LoadElementWindow(parent.Children[Index], ElementValue, parent)
			elif Type == "render_target":	
				parent.Children[Index] = RenderTarget()
				parent.Children[Index].SetParent(parent)
				self.LoadElementRenderTarget(parent.Children[Index], ElementValue, parent)
			elif Type == "render_target_v2":	
				parent.Children[Index] = RenderTargetV2()
				parent.Children[Index].SetParent(parent)
				self.LoadElementRenderTarget(parent.Children[Index], ElementValue, parent)
			elif Type == "button":
				parent.Children[Index] = Button()
				parent.Children[Index].SetParent(parent)
				self.LoadElementButton(parent.Children[Index], ElementValue, parent)

			elif Type == "radio_button":
				parent.Children[Index] = RadioButton()
				parent.Children[Index].SetParent(parent)
				self.LoadElementButton(parent.Children[Index], ElementValue, parent)

			elif Type == "toggle_button":
				parent.Children[Index] = ToggleButton()
				parent.Children[Index].SetParent(parent)
				self.LoadElementButton(parent.Children[Index], ElementValue, parent)

			elif Type == "mark":
				parent.Children[Index] = MarkBox()
				parent.Children[Index].SetParent(parent)
				self.LoadElementMark(parent.Children[Index], ElementValue, parent)

			elif Type == "image":
				parent.Children[Index] = ImageBox()
				parent.Children[Index].SetParent(parent)
				self.LoadElementImage(parent.Children[Index], ElementValue, parent)

			elif Type == "image2":
				parent.Children[Index] = ImageBox2()
				parent.Children[Index].SetParent(parent)
				self.LoadElementImage(parent.Children[Index], ElementValue, parent)

			elif Type == "expanded_image":
				parent.Children[Index] = ExpandedImageBox()
				parent.Children[Index].SetParent(parent)
				self.LoadElementExpandedImage(parent.Children[Index], ElementValue, parent)

			elif Type == "ani_image":
				parent.Children[Index] = AniImageBox()
				parent.Children[Index].SetParent(parent)
				self.LoadElementAniImage(parent.Children[Index], ElementValue, parent)

			elif Type == "slot":
				parent.Children[Index] = SlotWindow()
				parent.Children[Index].SetParent(parent)
				self.LoadElementSlot(parent.Children[Index], ElementValue, parent)

			elif Type == "candidate_list":
				parent.Children[Index] = CandidateListBox()
				parent.Children[Index].SetParent(parent)
				self.LoadElementCandidateList(parent.Children[Index], ElementValue, parent)

			elif Type == "grid_table":
				parent.Children[Index] = GridSlotWindow()
				parent.Children[Index].SetParent(parent)
				self.LoadElementGridTable(parent.Children[Index], ElementValue, parent)

			elif Type == "text":
				parent.Children[Index] = TextLine()
				parent.Children[Index].SetParent(parent)
				self.LoadElementText(parent.Children[Index], ElementValue, parent)

			elif Type == "editline":
				parent.Children[Index] = EditLine()
				parent.Children[Index].SetParent(parent)
				self.LoadElementEditLine(parent.Children[Index], ElementValue, parent)
				
			elif Type == "editline_new":
				parent.Children[Index] = EditLineNew()
				parent.Children[Index].SetParent(parent)
				self.LoadElementEditLine(parent.Children[Index], ElementValue, parent)
				
			elif Type == "titlebar":
				parent.Children[Index] = TitleBar()
				parent.Children[Index].SetParent(parent)
				self.LoadElementTitleBar(parent.Children[Index], ElementValue, parent)

			elif Type == "horizontalbar":
				parent.Children[Index] = HorizontalBar()
				parent.Children[Index].SetParent(parent)
				self.LoadElementHorizontalBar(parent.Children[Index], ElementValue, parent)

			elif Type == "board":
				parent.Children[Index] = Board()
				parent.Children[Index].SetParent(parent)
				self.LoadElementBoard(parent.Children[Index], ElementValue, parent)

			elif Type == "board_with_titlebar":
				parent.Children[Index] = BoardWithTitleBar()
				parent.Children[Index].SetParent(parent)
				self.LoadElementBoardWithTitleBar(parent.Children[Index], ElementValue, parent)

			elif Type == "thinboard":
				parent.Children[Index] = ThinBoard()
				parent.Children[Index].SetParent(parent)
				self.LoadElementThinBoard(parent.Children[Index], ElementValue, parent)
			
			elif Type == "thinboard_gold":
				parent.Children[Index] = ThinBoardGold()
				parent.Children[Index].SetParent(parent)
				self.LoadElementThinBoardGold(parent.Children[Index], ElementValue, parent)
				
			elif Type == "thinboard_circle":
				parent.Children[Index] = ThinBoardCircle()
				parent.Children[Index].SetParent(parent)
				self.LoadElementThinBoardCircle(parent.Children[Index], ElementValue, parent)

			elif Type == "box":
				parent.Children[Index] = Box()
				parent.Children[Index].SetParent(parent)
				self.LoadElementBox(parent.Children[Index], ElementValue, parent)
				
			# elif Type == "thinboard_circle":
				# parent.Children[Index] = ThinBoardCircle()
				# parent.Children[Index].SetParent(parent)
				# self.LoadElementThinBoard(parent.Children[Index], ElementValue, parent)

			elif Type == "bar":
				parent.Children[Index] = Bar()
				parent.Children[Index].SetParent(parent)
				self.LoadElementBar(parent.Children[Index], ElementValue, parent)

			elif Type == "line":
				parent.Children[Index] = Line()
				parent.Children[Index].SetParent(parent)
				self.LoadElementLine(parent.Children[Index], ElementValue, parent)

			elif Type == "slotbar":
				parent.Children[Index] = SlotBar()
				parent.Children[Index].SetParent(parent)
				self.LoadElementSlotBar(parent.Children[Index], ElementValue, parent)

			elif Type == "gauge":
				parent.Children[Index] = Gauge()
				parent.Children[Index].SetParent(parent)
				self.LoadElementGauge(parent.Children[Index], ElementValue, parent)

			elif Type == "scrollbar":
				parent.Children[Index] = ScrollBar()
				parent.Children[Index].SetParent(parent)
				self.LoadElementScrollBar(parent.Children[Index], ElementValue, parent)

			elif Type == "thin_scrollbar":
				parent.Children[Index] = ThinScrollBar()
				parent.Children[Index].SetParent(parent)
				self.LoadElementScrollBar(parent.Children[Index], ElementValue, parent)

			elif Type == "small_thin_scrollbar":
				parent.Children[Index] = SmallThinScrollBar()
				parent.Children[Index].SetParent(parent)
				self.LoadElementScrollBar(parent.Children[Index], ElementValue, parent)

			elif Type == "sliderbar":
				parent.Children[Index] = SliderBar()
				parent.Children[Index].SetParent(parent)
				self.LoadElementSliderBar(parent.Children[Index], ElementValue, parent)

			elif Type == "listbox":
				parent.Children[Index] = ListBox()
				parent.Children[Index].SetParent(parent)
				self.LoadElementListBox(parent.Children[Index], ElementValue, parent)

			elif Type == "border_a":
				parent.Children[Index] = BorderA()
				parent.Children[Index].SetParent(parent)
				self.LoadElementBoard(parent.Children[Index], ElementValue, parent)
				
			elif Type == "border_new":
				parent.Children[Index] = BorderNew()
				parent.Children[Index].SetParent(parent)
				self.LoadElementBoard(parent.Children[Index], ElementValue, parent)
				
			elif Type == "listbox_scroll":  
				parent.Children[Index] = ListBoxScroll()
				parent.Children[Index].SetParent(parent)
				self.LoadElementListBox(parent.Children[Index], ElementValue, parent)

			elif Type == "listbox2":
				parent.Children[Index] = ListBox2()
				parent.Children[Index].SetParent(parent)
				self.LoadElementListBox2(parent.Children[Index], ElementValue, parent)
				
			elif Type == "listboxex":
				parent.Children[Index] = ListBoxEx()
				parent.Children[Index].SetParent(parent)
				self.LoadElementListBoxEx(parent.Children[Index], ElementValue, parent)
				
			elif Type == "extended_text":
				parent.Children[Index] = ExtendedTextLine()
				parent.Children[Index].SetParent(parent)
				self.LoadElementExtendedText(parent.Children[Index], ElementValue, parent)

			elif Type == "checkbox_biolog":
				parent.Children[Index] = CheckBox_Biolog()
				parent.Children[Index].SetParent(parent)
				self.LoadElementCheckBox(parent.Children[Index], ElementValue, parent)

			elif Type == "boxed_board":
				parent.Children[Index] = BoxedBoard()
				parent.Children[Index].SetParent(parent)
				self.LoadElementBoxedBoard(parent.Children[Index], ElementValue, parent)
				
			elif Type == "scrollbar_new" and app.ENABLE_SWITCHBOT_WORLDARD:
				parent.Children[Index] = ScrollBarNew()
				parent.Children[Index].SetParent(parent)
				self.LoadElementScrollBar(parent.Children[Index], ElementValue, parent)
				
			else:
				Index += 1
				continue

			parent.Children[Index].SetWindowName(Name)
			if 0 != self.InsertFunction:
				self.InsertFunction(Name, parent.Children[Index])

			self.LoadChildren(parent.Children[Index], ElementValue)
			Index += 1

	def CheckKeyList(self, name, value, key_list):

		for DataKey in key_list:
			if False == value.has_key(DataKey):
				print "Failed to find data key", "[" + name + "/" + DataKey + "]"
				return False

		return True

	def LoadDefaultData(self, window, value, parentWindow):
		loc_x = int(value["x"])
		loc_y = int(value["y"])
		if value.has_key("vertical_align"):
			if "center" == value["vertical_align"]:
				window.SetWindowVerticalAlignCenter()
			elif "bottom" == value["vertical_align"]:
				window.SetWindowVerticalAlignBottom()

		if parentWindow.IsRTL():
			loc_x = int(value["x"]) + window.GetWidth()
			if value.has_key("horizontal_align"):
				if "center" == value["horizontal_align"]:
					window.SetWindowHorizontalAlignCenter()
					loc_x = - int(value["x"])
				elif "right" == value["horizontal_align"]:
					window.SetWindowHorizontalAlignLeft()
					loc_x = int(value["x"]) - window.GetWidth()
					## loc_x = parentWindow.GetWidth() - int(value["x"]) + window.GetWidth()
			else:
				window.SetWindowHorizontalAlignRight()

			if value.has_key("all_align"):
				window.SetWindowVerticalAlignCenter()
				window.SetWindowHorizontalAlignCenter()
				loc_x = - int(value["x"])
		else:
			if value.has_key("horizontal_align"):
				if "center" == value["horizontal_align"]:
					window.SetWindowHorizontalAlignCenter()
				elif "right" == value["horizontal_align"]:
					window.SetWindowHorizontalAlignRight()

		window.SetPosition(loc_x, loc_y)
		window.Show()

	## Window
	def LoadElementWindow(self, window, value, parentWindow):

		if False == self.CheckKeyList(value["name"], value, self.WINDOW_KEY_LIST):
			return False

		window.SetSize(int(value["width"]), int(value["height"]))
		self.LoadDefaultData(window, value, parentWindow)

		return True

	## Button
	def LoadElementButton(self, window, value, parentWindow):

		if value.has_key("width") and value.has_key("height"):
			window.SetSize(int(value["width"]), int(value["height"]))

		if True == value.has_key("default_image"):
			window.SetUpVisual(value["default_image"])
		if True == value.has_key("over_image"):
			window.SetOverVisual(value["over_image"])
		if True == value.has_key("down_image"):
			window.SetDownVisual(value["down_image"])
		if True == value.has_key("disable_image"):
			window.SetDisableVisual(value["disable_image"])

		if True == value.has_key("text"):
			if True == value.has_key("text_height"):
				window.SetText(value["text"], value["text_height"])
			else:
				window.SetText(value["text"])

			if value.has_key("text_color"):
				window.SetTextColor(value["text_color"])

		if True == value.has_key("tooltip_text"):
			if True == value.has_key("tooltip_x") and True == value.has_key("tooltip_y"):
				window.SetToolTipText(value["tooltip_text"], int(value["tooltip_x"]), int(value["tooltip_y"]))
			else:
				window.SetToolTipText(value["tooltip_text"])

		self.LoadDefaultData(window, value, parentWindow)

		return True

	def LoadElementCheckBox(self, window, value, parentWindow):

		if value.has_key("text"):
			window.SetText(value["text"])

		if value.has_key("checked") and value["checked"] == True:
			window.SetChecked(window.STATE_SELECTED)

		if value.has_key("disabled") and value["disabled"] == True:
			window.Disable()

		self.LoadDefaultData(window, value, parentWindow)

	def LoadElementBoxedBoard(self, window, value, parentWindow):
		if not self.CheckKeyList(value["name"], value, self.WINDOW_KEY_LIST):
			return False
		
		window.SetSize(value["width"], value["height"])
		
		if value.has_key("border_color"):
			window.SetBorderColor(value["border_color"])
		
		if value.has_key("border_size"):
			window.SetBorderSize(value["border_size"])
		
		if value.has_key("base_color"):
			window.SetBaseColor(value["base_color"])
		
		self.LoadDefaultData(window, value, parentWindow)
		return True

	## Mark
	def LoadElementMark(self, window, value, parentWindow):

		#if False == self.CheckKeyList(value["name"], value, self.MARK_KEY_LIST):
		#	return False

		self.LoadDefaultData(window, value, parentWindow)

		return True

	## Image
	def LoadElementImage(self, window, value, parentWindow):

		if False == self.CheckKeyList(value["name"], value, self.IMAGE_KEY_LIST):
			return False

		window.LoadImage(value["image"])
		self.LoadDefaultData(window, value, parentWindow)

		return True

	## AniImage
	def LoadElementAniImage(self, window, value, parentWindow):

		if False == self.CheckKeyList(value["name"], value, self.ANI_IMAGE_KEY_LIST):
			return False

		if True == value.has_key("delay"):
			window.SetDelay(value["delay"])

		if True == value.has_key("x_scale") and True == value.has_key("y_scale"):
			for image in value["images"]:
				window.AppendImageScale(image, float(value["x_scale"]), float(value["y_scale"]))
		else:
			for image in value["images"]:
				window.AppendImage(image)

		if value.has_key("width") and value.has_key("height"):
			window.SetSize(value["width"], value["height"])

		self.LoadDefaultData(window, value, parentWindow)

		return True

	## Expanded Image
	def LoadElementExpandedImage(self, window, value, parentWindow):

		if False == self.CheckKeyList(value["name"], value, self.EXPANDED_IMAGE_KEY_LIST):
			return False

		window.LoadImage(value["image"])

		if True == value.has_key("x_origin") and True == value.has_key("y_origin"):
			window.SetOrigin(float(value["x_origin"]), float(value["y_origin"]))

		if True == value.has_key("x_scale") and True == value.has_key("y_scale"):
			window.SetScale(float(value["x_scale"]), float(value["y_scale"]))

		if True == value.has_key("rect"):
			RenderingRect = value["rect"]
			window.SetRenderingRect(RenderingRect[0], RenderingRect[1], RenderingRect[2], RenderingRect[3])

		if True == value.has_key("mode"):
			mode = value["mode"]
			if "MODULATE" == mode:
				window.SetRenderingMode(wndMgr.RENDERING_MODE_MODULATE)

		self.LoadDefaultData(window, value, parentWindow)

		return True

	## Slot
	def LoadElementSlot(self, window, value, parentWindow):

		if False == self.CheckKeyList(value["name"], value, self.SLOT_KEY_LIST):
			return False

		global_x = int(value["x"])
		global_y = int(value["y"])
		global_width = int(value["width"])
		global_height = int(value["height"])

		window.SetPosition(global_x, global_y)
		window.SetSize(global_width, global_height)
		window.Show()

		r = 1.0
		g = 1.0
		b = 1.0
		a = 1.0

		if True == value.has_key("image_r") and \
			True == value.has_key("image_g") and \
			True == value.has_key("image_b") and \
			True == value.has_key("image_a"):
			r = float(value["image_r"])
			g = float(value["image_g"])
			b = float(value["image_b"])
			a = float(value["image_a"])

		SLOT_ONE_KEY_LIST = ("index", "x", "y", "width", "height")

		for slot in value["slot"]:
			if True == self.CheckKeyList(value["name"] + " - one", slot, SLOT_ONE_KEY_LIST):
				wndMgr.AppendSlot(window.hWnd,
									int(slot["index"]),
									int(slot["x"]),
									int(slot["y"]),
									int(slot["width"]),
									int(slot["height"]))

		if True == value.has_key("image"):
			wndMgr.SetSlotBaseImage(window.hWnd,
									value["image"],
									r, g, b, a)

		return True

	def LoadElementCandidateList(self, window, value, parentWindow):
		if False == self.CheckKeyList(value["name"], value, self.CANDIDATE_LIST_KEY_LIST):
			return False

		window.SetPosition(int(value["x"]), int(value["y"]))
		window.SetItemSize(int(value["item_xsize"]), int(value["item_ysize"]))
		window.SetItemStep(int(value["item_step"]))
		window.Show()

		return True

	## Table
	def LoadElementGridTable(self, window, value, parentWindow):

		if False == self.CheckKeyList(value["name"], value, self.GRID_TABLE_KEY_LIST):
			return False

		xBlank = 0
		yBlank = 0
		if True == value.has_key("x_blank"):
			xBlank = int(value["x_blank"])
		if True == value.has_key("y_blank"):
			yBlank = int(value["y_blank"])

		window.SetPosition(int(value["x"]), int(value["y"]))

		window.ArrangeSlot(	int(value["start_index"]),
							int(value["x_count"]),
							int(value["y_count"]),
							int(value["x_step"]),
							int(value["y_step"]),
							xBlank,
							yBlank)
		if True == value.has_key("image"):
			r = 1.0
			g = 1.0
			b = 1.0
			a = 1.0
			if True == value.has_key("image_r") and \
				True == value.has_key("image_g") and \
				True == value.has_key("image_b") and \
				True == value.has_key("image_a"):
				r = float(value["image_r"])
				g = float(value["image_g"])
				b = float(value["image_b"])
				a = float(value["image_a"])
			wndMgr.SetSlotBaseImage(window.hWnd, value["image"], r, g, b, a)

		if True == value.has_key("style"):
			if "select" == value["style"]:
				wndMgr.SetSlotStyle(window.hWnd, wndMgr.SLOT_STYLE_SELECT)
		window.Show()

		return True

	## Text
	def LoadElementText(self, window, value, parentWindow):

		if value.has_key("fontsize"):
			fontSize = value["fontsize"]

			if "LARGE" == fontSize:
				window.SetFontName(localeInfo.UI_DEF_FONT_LARGE)

		elif value.has_key("fontname"):
			fontName = value["fontname"]
			window.SetFontName(fontName)

		if value.has_key("text_horizontal_align"):
			if "left" == value["text_horizontal_align"]:
				window.SetHorizontalAlignLeft()
			elif "center" == value["text_horizontal_align"]:
				window.SetHorizontalAlignCenter()
			elif "right" == value["text_horizontal_align"]:
				window.SetHorizontalAlignRight()

		if value.has_key("text_vertical_align"):
			if "top" == value["text_vertical_align"]:
				window.SetVerticalAlignTop()
			elif "center" == value["text_vertical_align"]:
				window.SetVerticalAlignCenter()
			elif "bottom" == value["text_vertical_align"]:
				window.SetVerticalAlignBottom()

		if value.has_key("all_align"):
			window.SetHorizontalAlignCenter()
			window.SetVerticalAlignCenter()
			window.SetWindowHorizontalAlignCenter()
			window.SetWindowVerticalAlignCenter()

		if value.has_key("r") and value.has_key("g") and value.has_key("b"):
			window.SetFontColor(float(value["r"]), float(value["g"]), float(value["b"]))
		elif value.has_key("color"):
			window.SetPackedFontColor(value["color"])
		else:
			window.SetFontColor(0.8549, 0.8549, 0.8549)

		if value.has_key("outline"):
			if value["outline"]:
				window.SetOutline()
		if True == value.has_key("text"):
			window.SetText(value["text"])

		self.LoadDefaultData(window, value, parentWindow)

		return True

	## EditLine
	def LoadElementEditLine(self, window, value, parentWindow):

		if False == self.CheckKeyList(value["name"], value, self.EDIT_LINE_KEY_LIST):
			return False


		if value.has_key("secret_flag"):
			window.SetSecret(value["secret_flag"])
		if value.has_key("info_msg"):
			window.SetInfoMessage(value["info_msg"])
		if value.has_key("with_codepage"):
			if value["with_codepage"]:
				window.bCodePage = True
		if value.has_key("only_number"):
			if value["only_number"]:
				window.SetNumberMode()
		if value.has_key("enable_codepage"):
			window.SetIMEFlag(value["enable_codepage"])
		if value.has_key("enable_ime"):
			window.SetIMEFlag(value["enable_ime"])
		if value.has_key("limit_width"):
			window.SetLimitWidth(value["limit_width"])
		if value.has_key("multi_line"):
			if value["multi_line"]:
				window.SetMultiLine()

		window.SetMax(int(value["input_limit"]))
		window.SetSize(int(value["width"]), int(value["height"]))
		self.LoadElementText(window, value, parentWindow)

		return True

	def LoadElementRenderTarget(self, window, value, parentWindow):

		if False == self.CheckKeyList(value["name"], value, self.RENDER_TARGET_KEY_LIST):
			return False

		window.SetSize(value["width"], value["height"])
		
		if True == value.has_key("style"):
			for style in value["style"]:
				window.AddFlag(style)
				
		self.LoadDefaultData(window, value, parentWindow)
		
		if value.has_key("index"):
			window.SetRenderTarget(int(value["index"]))

		return True


	## TitleBar
	def LoadElementTitleBar(self, window, value, parentWindow):

		if False == self.CheckKeyList(value["name"], value, self.TITLE_BAR_KEY_LIST):
			return False

		window.MakeTitleBar(int(value["width"]), value.get("color", "red"))
		
		if value.has_key("title_info"):
			window.TitleInfo(int(value["title_info"]), True)
			
			if value.has_key("title_info_x") and value.has_key("title_info_y"):
				window.imgLeftTitle.SetPosition(int(value["title_info_x"]), int(value["title_info_y"]))
				
			if value.has_key("title_info_xscale"):
				window.imgLeftTitle.SetScale(float(value["title_info_xscale"]), 1.0)
		
		self.LoadDefaultData(window, value, parentWindow)

		return True

	## HorizontalBar
	def LoadElementHorizontalBar(self, window, value, parentWindow):

		if False == self.CheckKeyList(value["name"], value, self.HORIZONTAL_BAR_KEY_LIST):
			return False

		window.Create(int(value["width"]))
		self.LoadDefaultData(window, value, parentWindow)

		return True

	## Board
	def LoadElementBoard(self, window, value, parentWindow):

		if False == self.CheckKeyList(value["name"], value, self.BOARD_KEY_LIST):
			return False

		window.SetSize(int(value["width"]), int(value["height"]))
		self.LoadDefaultData(window, value, parentWindow)

		return True

	## Board With TitleBar
	def LoadElementBoardWithTitleBar(self, window, value, parentWindow):

		if False == self.CheckKeyList(value["name"], value, self.BOARD_WITH_TITLEBAR_KEY_LIST):
			return False

		window.SetSize(int(value["width"]), int(value["height"]))
		window.SetTitleName(value["title"])
		self.LoadDefaultData(window, value, parentWindow)

		return True

	## ThinBoard
	def LoadElementThinBoard(self, window, value, parentWindow):

		if False == self.CheckKeyList(value["name"], value, self.BOARD_KEY_LIST):
			return False

		window.SetSize(int(value["width"]), int(value["height"]))
		self.LoadDefaultData(window, value, parentWindow)

		return True
		
	## ThinBoardGold
	def LoadElementThinBoardGold(self, window, value, parentWindow):

		if False == self.CheckKeyList(value["name"], value, self.BOARD_KEY_LIST):
			return False

		window.SetSize(int(value["width"]), int(value["height"]))
		self.LoadDefaultData(window, value, parentWindow)

		return True
		
		## ThinBoardCircle
	def LoadElementThinBoardCircle(self, window, value, parentWindow):

		if False == self.CheckKeyList(value["name"], value, self.BOARD_KEY_LIST):
			return False

		window.SetSize(int(value["width"]), int(value["height"]))
		self.LoadDefaultData(window, value, parentWindow)

		return True

	## Box
	def LoadElementBox(self, window, value, parentWindow):

		if False == self.CheckKeyList(value["name"], value, self.BOX_KEY_LIST):
			return False

		if True == value.has_key("color"):
			window.SetColor(value["color"])

		window.SetSize(int(value["width"]), int(value["height"]))
		self.LoadDefaultData(window, value, parentWindow)

		return True

	## Bar
	def LoadElementBar(self, window, value, parentWindow):

		if False == self.CheckKeyList(value["name"], value, self.BAR_KEY_LIST):
			return False

		if True == value.has_key("color"):
			window.SetColor(value["color"])

		window.SetSize(int(value["width"]), int(value["height"]))
		self.LoadDefaultData(window, value, parentWindow)

		return True

	## Line
	def LoadElementLine(self, window, value, parentWindow):

		if False == self.CheckKeyList(value["name"], value, self.LINE_KEY_LIST):
			return False

		if True == value.has_key("color"):
			window.SetColor(value["color"])

		window.SetSize(int(value["width"]), int(value["height"]))
		self.LoadDefaultData(window, value, parentWindow)

		return True

	## Slot
	def LoadElementSlotBar(self, window, value, parentWindow):

		if False == self.CheckKeyList(value["name"], value, self.SLOTBAR_KEY_LIST):
			return False

		window.SetSize(int(value["width"]), int(value["height"]))
		self.LoadDefaultData(window, value, parentWindow)

		return True
		
	def LoadElementSlotBar2(self, window, value, parentWindow):
		window.SetWidth(int(value["width"]))

		if value.has_key("text"):
			window.SetText(value["text"])

		self.LoadDefaultData(window, value, parentWindow)

		return True

	## Gauge
	def LoadElementGauge(self, window, value, parentWindow):

		if False == self.CheckKeyList(value["name"], value, self.GAUGE_KEY_LIST):
			return False

		window.MakeGauge(value["width"], value["color"])
		self.LoadDefaultData(window, value, parentWindow)

		if True == value.has_key("tooltip_text"):
			if True == value.has_key("tooltip_x") and True == value.has_key("tooltip_y"):
				window.SetToolTipText(value["tooltip_text"], int(value["tooltip_x"]), int(value["tooltip_y"]))
			else:
				window.SetToolTipText(value["tooltip_text"])

		return True

	## ScrollBar
	def LoadElementScrollBar(self, window, value, parentWindow):

		if False == self.CheckKeyList(value["name"], value, self.SCROLLBAR_KEY_LIST):
			return False

		window.SetScrollBarSize(value["size"])
		self.LoadDefaultData(window, value, parentWindow)

		return True

	## SliderBar
	def LoadElementSliderBar(self, window, value, parentWindow):

		self.LoadDefaultData(window, value, parentWindow)

		return True

	## ListBox
	def LoadElementListBox(self, window, value, parentWindow):

		if False == self.CheckKeyList(value["name"], value, self.LIST_BOX_KEY_LIST):
			return False

		if value.has_key("item_align"):
			window.SetTextCenterAlign(value["item_align"])

		window.SetSize(value["width"], value["height"])
		self.LoadDefaultData(window, value, parentWindow)

		return True

	## ListBox2
	def LoadElementListBox2(self, window, value, parentWindow):

		if False == self.CheckKeyList(value["name"], value, self.LIST_BOX_KEY_LIST):
			return False

		window.SetRowCount(value.get("row_count", 10))
		window.SetSize(value["width"], value["height"])
		self.LoadDefaultData(window, value, parentWindow)

		if value.has_key("item_align"):
			window.SetTextCenterAlign(value["item_align"])

		return True
	def LoadElementListBoxEx(self, window, value, parentWindow):

		if False == self.CheckKeyList(value["name"], value, self.LIST_BOX_KEY_LIST):
			return False

		window.SetSize(value["width"], value["height"])
		self.LoadDefaultData(window, value, parentWindow)

		if value.has_key("itemsize_x") and value.has_key("itemsize_y"):
			window.SetItemSize(int(value["itemsize_x"]), int(value["itemsize_y"]))

		if value.has_key("itemstep"):
			window.SetItemStep(int(value["itemstep"]))

		if value.has_key("viewcount"):
			window.SetViewItemCount(int(value["viewcount"]))

		return True
	def LoadElementExtendedText(self, window, value, parentWindow):

		if True == value.has_key("text"):
			window.SetText(value["text"])

		self.LoadDefaultData(window, value, parentWindow)

		return True

class ReadingWnd(Bar):

	def __init__(self):
		Bar.__init__(self,"TOP_MOST")

		self.__BuildText()
		self.SetSize(80, 19)
		self.Show()

	def __del__(self):
		Bar.__del__(self)

	def __BuildText(self):
		self.text = TextLine()
		self.text.SetParent(self)
		self.text.SetPosition(4, 3)
		self.text.Show()

	def SetText(self, text):
		self.text.SetText(text)

	def SetReadingPosition(self, x, y):
		xPos = x + 2
		yPos = y  - self.GetHeight() - 2
		self.SetPosition(xPos, yPos)

	def SetTextColor(self, color):
		self.text.SetPackedFontColor(color)

def MakeWindow(parent, x, y, width, height):
	wind = Window()
	wind.SetParent(parent)
	wind.SetSize(width, height)
	wind.SetPosition(x, y)
	wind.Show()
	return wind
	
class ExtendedTextLine(Window):

	OBJECT_TYPE_IMAGE = 0
	OBJECT_TYPE_TEXT = 1
	OBJECT_TYPE_HEIGHT = 2
	OBJECT_TYPE_WIDTH = 3

	OBJECT_TAGS = {
		OBJECT_TYPE_IMAGE : "IMAGE",
		OBJECT_TYPE_TEXT : "TEXT",
		OBJECT_TYPE_HEIGHT : "HEIGHT",
		OBJECT_TYPE_WIDTH : "WIDTH",
	}

	def __init__(self):
		Window.__init__(self)

		self.inputText = ""
		self.childrenList = []

		self.limitWidth = 0
		self.x = 0
		self.maxHeight = 0
		self.extraHeight = 0

		self.renderingRect = { "left" : 0, "right" : 0, "top" : 0, "bottom" : 0 }

		self.SetWindowName("NONAME_ExtendedTextLine")

	def __del__(self):
		Window.__del__(self)

	def SetLimitWidth(self, width):
		self.limitWidth = width
		if self.inputText != "":
			self.SetText(self.inputText)

	def IsText(self, text):
		return self.inputText == text

	def SetText(self, text):
		self.childrenList = []
		self.x = 0
		self.maxHeight = 0
		self.extraHeight = 0

		charIndex = 0
		currentWord = ""

		textLine = None

		while charIndex < len(text):
			c = text[charIndex:charIndex+1] 

			# tags
			if c == "<":
				if textLine:
					self.childrenList.append(textLine)
					self.x += textLine.GetTextWidth()
					self.maxHeight = max(self.maxHeight, textLine.GetTextHeight() + 2)
					textLine = None

				tagStart = charIndex
				tagEnd = text[tagStart:].find(">")
				if tagEnd == -1:
					tagEnd = len(text)
				else:
					tagEnd += tagStart

				tagNameStart = charIndex + 1
				tagNameEnd = text[tagNameStart:].find(" ")
				if tagNameEnd == -1 or tagNameEnd > tagEnd:
					tagNameEnd = tagEnd
				else:
					tagNameEnd += tagNameStart
				tag = text[tagNameStart:tagNameEnd]

				content = {}
				tagContentPos = tagNameEnd + 1
				while tagContentPos < tagEnd:
					tagContentStart = -1
					for i in xrange(tagContentPos, tagEnd):
						if text[i:i+1] != " " and text[i:i+1] != "\t":
							tagContentStart = i
							break
					if tagContentStart == -1:
						break

					tagContentPos = text[tagContentStart:].find("=") + tagContentStart
					tagKey = text[tagContentStart:tagContentPos]

					tagContentPos += 1

					tagContentEnd = -1
					isBreakAtSpace = True
					for i in xrange(tagContentPos, tagEnd+1):
						if isBreakAtSpace == True and (text[i:i+1] == " " or text[i:i+1] == "\t" or text[i:i+1] == ">"):
							tagContentEnd = i
							break
						elif text[i:i+1] == "\"":
							if isBreakAtSpace == True:
								isBreakAtSpace = False
								tagContentPos = i + 1
							else:
								tagContentEnd = i
								break
					if tagContentEnd == -1:
						break

					tagValue = text[tagContentPos:tagContentEnd]
					content[tagKey] = tagValue

					tagContentPos = text[tagContentEnd:].find(" ")
					if tagContentPos == -1:
						tagContentPos = tagContentEnd
					else:
						tagContentPos += tagContentEnd

				bRet = True
				for key in self.OBJECT_TAGS:
					if self.OBJECT_TAGS[key] == tag.upper():
						bRet = self.__ComputeTag(key, content)
						break

				if bRet == False:
					break

				charIndex = tagEnd + 1
				continue

			# text
			if not textLine:
				textLine = TextLine()
				textLine.SetParent(self)
				textLine.SetPosition(self.x, 0)
				textLine.SetWindowVerticalAlignCenter()
				textLine.SetVerticalAlignCenter()
				textLine.Show()
			subtext = textLine.GetText()
			textLine.SetText(subtext + c)
			if textLine.GetTextWidth() + self.x >= self.limitWidth and self.limitWidth != 0:
				if subtext != "":
					textLine.SetText(subtext)
					self.childrenList.append(textLine)
					self.x += textLine.GetTextWidth()
					self.maxHeight = max(self.maxHeight, textLine.GetTextHeight() + 2)
					textLine = None
				else:
					textLine = None
				break

			# increase char index
			charIndex += 1

		if textLine:
			self.childrenList.append(textLine)
			self.x += textLine.GetTextWidth()
			self.maxHeight = max(self.maxHeight, textLine.GetTextHeight() + 2)
			textLine = None

		self.inputText = text[:charIndex]
		self.SetSize(self.x, self.maxHeight + self.extraHeight)
		self.UpdateRect()

		return charIndex

	def __ComputeTag(self, index, content):
		# tag <IMAGE []>
		if index == self.OBJECT_TYPE_IMAGE:
			if not content.has_key("path"):
				import dbg
				dbg.TraceError("Cannot read image tag : no path given")
				return False

			image = ImageBox()
			image.SetParent(self)
			image.SetPosition(self.x, 0)
			image.SetWindowVerticalAlignCenter()
			image.LoadImage(content["path"])
			image.Show()

			if content.has_key("y"):
				image.SetPosition(image.GetLeft(), int(content["y"]))

			if content.has_key("align") and content["align"].lower() == "center":
				image.SetPosition(self.limitWidth / 2 - image.GetWidth() / 2, 0)
			else:
				if self.x + image.GetWidth() >= self.limitWidth and self.limitWidth != 0:
					return False
				self.x += image.GetWidth()

			self.childrenList.append(image)
			self.maxHeight = max(self.maxHeight, image.GetHeight())

			return True

		# tag <TEXT []>
		elif index == self.OBJECT_TYPE_TEXT:
			if not content.has_key("text"):
				import dbg
				dbg.TraceError("Cannot read text tag : no text given")
				return False

			textLine = TextLine()
			textLine.SetParent(self)
			textLine.SetPosition(self.x, 0)
			textLine.SetWindowVerticalAlignCenter()
			textLine.SetVerticalAlignCenter()
			if content.has_key("r") and content.has_key("g") and content.has_key("b"):
				textLine.SetFontColor(int(content["r"]) / 255.0, int(content["g"]) / 255.0, int(content["b"]) / 255.0)
			elif content.has_key("color"):
				textLine.SetPackedFontColor(int(content["color"], 0))
			isLarge = False
			if content.has_key("font_size"):
				if content["font_size"].lower() == "large":
					isLarge = True
					textLine.SetFontName(localeInfo.UI_DEF_FONT_LARGE)
			if content.has_key("bold"):
				if content["bold"] == "1" or content["bold"].lower() == "true":
					if isLarge:
						textLine.SetFontName(localeInfo.UI_DEF_FONT_LARGE_BOLD)
					else:
						textLine.SetFontName(localeInfo.UI_DEF_FONT_BOLD)
			if content.has_key("outline") and content["outline"] == "1":
				textLine.SetOutline()
			textLine.SetText(content["text"])
			textLine.Show()

			if self.x + textLine.GetTextWidth() >= self.limitWidth and self.limitWidth != 0:
				return False

			self.childrenList.append(textLine)
			self.x += textLine.GetTextWidth()
			self.maxHeight = max(self.maxHeight, textLine.GetTextHeight() + 2)

			return True

		# tag <HEIGHT []>
		elif index == self.OBJECT_TYPE_HEIGHT:
			if not content.has_key("size"):
				import dbg
				dbg.TraceError("Cannot read height tag : no size given")
				return False

			self.extraHeight += int(content["size"])

			return True

		# tag <WIDTH []>
		elif index == self.OBJECT_TYPE_WIDTH:
			if not content.has_key("size"):
				import dbg
				dbg.TraceError("Cannot read width tag : no size given")
				return False

			self.x += int(content["size"])

			return True

		return False

	def SetRenderingRect(self, left, top, right, bottom):
		self.renderingRect = {
			"left" : max(0, min(self.GetWidth(), int(-left * self.GetWidth()))),
			"top" : max(0, min(self.GetHeight(), int(-top * self.GetHeight()))),
			"right" : max(0, min(self.GetWidth(), int(-right * self.GetWidth()))),
			"bottom" : max(0, min(self.GetHeight(), int(-bottom * self.GetHeight()))),
		}

		self.__ApplyRenderingRect()

	def __ApplyRenderingRect(self):
		for child in self.childrenList:
			(x, y) = child.GetLocalPosition()
			childHeight = child.GetHeight()
			if isinstance(child, TextLine):
				childHeight = child.GetTextHeight()
			yEnd = y + childHeight

			renderTop = max(0, self.renderingRect["top"] - y)
			renderBottom = max(0, self.renderingRect["bottom"] - (self.GetHeight() - yEnd))

			child.SetRenderingRect(0, -float(renderTop) / childHeight, 0, -float(renderBottom) / childHeight)


def MakeSlotBar(parent, x, y, width, height):
	slotBar = SlotBar()
	slotBar.SetParent(parent)
	slotBar.SetSize(width, height)
	slotBar.SetPosition(x, y)
	slotBar.Show()
	return slotBar

def MakeImageBox(parent, name, x, y):
	image = ImageBox()
	image.SetParent(parent)
	image.LoadImage(name)
	image.SetPosition(x, y)
	image.Show()
	return image

def MakeText(parent, textlineText, x, y, color = None):
	textline = TextLine()
	if parent != None:
		textline.SetParent(parent)
	textline.SetPosition(x, y)
	if color != None:
		textline.SetFontColor(color[0], color[1], color[2])
	textline.SetText(textlineText)
	textline.Show()
	return textline
	
def MakeImageBoxNew(parent, name, x, y, xScale, yScale):
	image = ImageBox()
	image.SetParent(parent)
	image.LoadImage(name)
	image.SetPosition(x, y)
	image.SetScale(xScale, yScale)
	image.Show()
	return image
	
def MakeTextV3(parent, textlineText, x, y, color=False, font = False):
	if font:
		textline = TextLine(font)
	else:
		textline = TextLine()
	if parent != None:
		textline.SetParent(parent)
	textline.SetPosition(x, y)
	if color:
		textline.SetPackedFontColor(grp.GenerateColor(0.659,0.475,0.388,1.0))
	textline.SetText(textlineText)
	textline.Show()
	return textline
	
def MakeTextForBP(parent, x, y, textlineText, bnsId = 0):
	textline = TextLine()
	if parent != None:
		textline.SetParent(parent)
	textline.SetPosition(x, y)
	textline.SetText(textlineText)
	textline.SetBonusId(bnsId)
	textline.Show()
	return textline

def MakeTextLine(parent):
	textLine = TextLine()
	textLine.SetParent(parent)
	textLine.SetWindowHorizontalAlignCenter()
	textLine.SetWindowVerticalAlignCenter()
	textLine.SetHorizontalAlignCenter()
	textLine.SetVerticalAlignCenter()
	textLine.Show()
	return textLine
	
def MakeTextLineBP(parent, horizontalAlign = True, verticalAlgin = True, x = 0, y = 0):
	textLine = TextLine()
	textLine.SetParent(parent)
	
	if horizontalAlign == True:
		textLine.SetWindowHorizontalAlignCenter()
		
	if verticalAlgin == True:
		textLine.SetWindowVerticalAlignCenter()
		
	textLine.SetHorizontalAlignCenter()
	textLine.SetVerticalAlignCenter()
	
	if x != 0 and y != 0:
		textLine.SetPosition(x, y)
		
	textLine.Show()
	return textLine
	
def MakeTextLineNew(parent, x, y, text):
	textLine = TextLine()
	textLine.SetParent(parent)
	textLine.SetPosition(x, y)
	textLine.SetText(text)
	textLine.Show()
	return textLine

def MakeExpandedImageBox(parent, name, x, y, flag = ""):
	image = ExpandedImageBox()
	image.SetParent(parent)
	image.LoadImage(name)
	image.SetPosition(x, y)
	if flag != "":
		image.AddFlag(flag)
	image.Show()
	return image

def MakeOptionsCheckBox(parent, text, x, y):
	checkBox = CheckBoxOptions()
	checkBox.SetParent(parent)
	checkBox.SetPosition(x, y)
	checkBox.SetTextInfo(text)
	checkBox.SetBaseCheckImage("d:/ymir work/ui/new_options/options_checkbox.tga")
	checkBox.Show()
	return checkBox
	
def MakeTextLineWithouAlign(parent, text, x, y):
	textLine = TextLine()
	textLine.SetParent(parent)
	textLine.SetPosition(x, y)
	textLine.SetText(text)
	# if app.WJ_MULTI_TEXTLINE:
		# textLine.DisableEnterToken()
	textLine.Show()
	return textLine
	
def MakeBoardWithTitleBar(parent, flag, title, closeEvent, width, height):
	board = BoardWithTitleBar()
	board.SetParent(parent)
	board.SetSize(width, height)
	board.AddFlag(flag)
	board.SetTitleName(title)
	board.SetCloseEvent(closeEvent)
	board.Show()
	return board

def MakeButton(parent, x, y, tooltipText, path, up, over, down, CanShow = True):
	button = Button()
	button.SetParent(parent)
	button.SetPosition(x, y)
	button.SetUpVisual(path + up)
	button.SetOverVisual(path + over)
	button.SetDownVisual(path + down)
	button.SetToolTipText(tooltipText)
	if CanShow == True:
		button.Show()
	return button

def MakeRadioButton(parent, x, y, path, up, over, down):
	button = RadioButton()
	button.SetParent(parent)
	button.SetPosition(x, y)
	button.SetUpVisual(path + up)
	button.SetOverVisual(path + over)
	button.SetDownVisual(path + down)
	button.Show()
	return button
	
def MakeRadioButtonV2(parent, x, y, buttonText, path, up, over, down, tooltip = ""):
	button = RadioButton()
	button.SetParent(parent)
	button.SetPosition(x, y)
	button.SetUpVisual(path + up)
	button.SetOverVisual(path + over)
	button.SetDownVisual(path + down)
	button.SetText(buttonText)
	button.SetToolTipText(tooltip)
	button.Show()
	return button

def RenderRoundBox(x, y, width, height, color):
	grp.SetColor(color)
	grp.RenderLine(x+2, y, width-3, 0)
	grp.RenderLine(x+2, y+height, width-3, 0)
	grp.RenderLine(x, y+2, 0, height-4)
	grp.RenderLine(x+width, y+1, 0, height-3)
	grp.RenderLine(x, y+2, 2, -2)
	grp.RenderLine(x, y+height-2, 2, 2)
	grp.RenderLine(x+width-2, y, 2, 2)
	grp.RenderLine(x+width-2, y+height, 2, -2)

def MakeButtonNew(parent, x, y, text, path, up, over, down):
	button = Button()
	button.SetParent(parent)
	button.SetPosition(x, y)
	button.SetUpVisual(path + up)
	button.SetOverVisual(path + over)
	button.SetDownVisual(path + down)
	button.SetText(text)
	button.UpdateRect()
	button.Show()
	return button

def MakeHorizontalBar(parent, x, y, width, text):
	horizontalBar = HorizontalBar()
	horizontalBar.Create(width)
	horizontalBar.SetParent(parent)
	horizontalBar.SetPosition(x, y)
	horizontalBar.SetWidth(width)
	horizontalBar.SetText(text)
	horizontalBar.Show()
	return horizontalBar

def MakeThinBoardCircle(parent, x, y, width, heigh, text, bnsId = 0):
	thin = ThinBoardCircle()
	thin.SetParent(parent)
	thin.SetSize(width, heigh)
	thin.SetPosition(x, y)
	thin.SetText(text)
	thin.SetBonusId(bnsId)
	thin.Show()
	return thin
	
def MakeBrownBoard(parent, x, y, width, heigh, text, bnsId = 0):
	thin = BrownBoard2()
	thin.SetParent(parent)
	thin.SetSize(width, heigh)
	thin.SetPosition(x, y)
	thin.SetText(text)
	# thin.SetBonusId(bnsId)
	thin.Show()
	return thin

def MakeThinBoardGold(parent, x, y, width, heigh, text, bnsId = 0):
	thin = ThinBoardGold()
	thin.SetParent(parent)
	thin.SetSize(width, heigh)
	thin.SetPosition(x, y)
	thin.SetText(text)
	thin.SetBonusId(bnsId)
	thin.Show()
	return thin

def GenerateColor(r, g, b):
	r = float(r) / 255.0
	g = float(g) / 255.0
	b = float(b) / 255.0
	return grp.GenerateColor(r, g, b, 1.0)

def EnablePaste(flag):
	ime.EnablePaste(flag)

def GetHyperlink():
	return wndMgr.GetHyperlink()

class WikiRenderTarget(Window):
	def __init__(self):
		Window.__init__(self)
	
	def __del__(self):
		Window.__del__(self)
	
	def RegisterWindow(self, layer):
		self.hWnd = wndMgr.RegisterWikiRenderTarget(self, layer)

class InGameWikiCheckBox(Window):
	def __init__(self):
		Window.__init__(self)
		
		self.backgroundImage = None
		self.checkImage = None
		
		self.eventFunc = { "ON_CHECK" : None, "ON_UNCKECK" : None, }
		self.eventArgs = { "ON_CHECK" : None, "ON_UNCKECK" : None, }
		
		self.CreateElements()
	
	def __del__(self):
		Window.__del__(self)
		
		self.backgroundImage = None
		self.checkImage = None
		
		self.eventFunc = { "ON_CHECK" : None, "ON_UNCKECK" : None, }
		self.eventArgs = { "ON_CHECK" : None, "ON_UNCKECK" : None, }
	
	def CreateElements(self):
		self.backgroundImage = ImageBox()
		self.backgroundImage.SetParent(self)
		self.backgroundImage.AddFlag("not_pick")
		self.backgroundImage.LoadImage("d:/ymir work/ui/wiki/wiki_check_box_clean.tga")
		self.backgroundImage.Show()
		
		self.checkImage = ImageBox()
		self.checkImage.SetParent(self)
		self.checkImage.AddFlag("not_pick")
		self.checkImage.LoadImage("d:/ymir work/ui/wiki/wiki_check_box_checked.tga")
		self.checkImage.Hide()
		
		self.textInfo = TextLine()
		self.textInfo.SetParent(self)
		self.textInfo.SetPosition(20, 0)
		self.textInfo.Show()
		
		self.SetSize(self.backgroundImage.GetWidth() + self.textInfo.GetTextSize()[0], self.backgroundImage.GetHeight() + self.textInfo.GetTextSize()[1])
	
	def SetTextInfo(self, info):
		if self.textInfo:
			self.textInfo.SetText(info)
		
		self.SetSize(self.backgroundImage.GetWidth() + self.textInfo.GetTextSize()[0], self.backgroundImage.GetHeight() + self.textInfo.GetTextSize()[1])
	
	def SetCheckStatus(self, flag):
		if flag:
			self.checkImage.Show()
		else:
			self.checkImage.Hide()
	
	def GetCheckStatus(self):
		if self.checkImage:
			return self.checkImage.IsShow()
		
		return False
	
	def SetEvent(self, func, *args) :
		result = self.eventFunc.has_key(args[0])
		if result:
			self.eventFunc[args[0]] = func
			self.eventArgs[args[0]] = args
		else:
			print "[ERROR] ui.py SetEvent, Can`t Find has_key : %s" % args[0]
	
	def SetBaseCheckImage(self, image):
		if not self.backgroundImage:
			return
		
		self.backgroundImage.LoadImage(image)
	
	def OnMouseLeftButtonUp(self):
		if self.checkImage:
			if self.checkImage.IsShow():
				self.checkImage.Hide()
				
				if self.eventFunc["ON_UNCKECK"]:
					apply(self.eventFunc["ON_UNCKECK"], self.eventArgs["ON_UNCKECK"])
			else:
				self.checkImage.Show()
				
				if self.eventFunc["ON_CHECK"]:
					apply(self.eventFunc["ON_CHECK"], self.eventArgs["ON_CHECK"])

class EditLineNew(EditLine):
	def __init__(self):
		EditLine.__init__(self)

		self.backText = TextLine()
		self.backText.SetParent(self)
		self.backText.SetPosition(0,0)
		self.backText.SetFontColor(128,128,128)

	def __del__(self):
		EditLine.__del__(self)

	def SetInfoMessage(self, msg):
		self.backText.SetText(msg)

		if len(self.GetText()) > 0:
			self.backText.Hide()
		else:
			self.backText.Show()

	def OnIMEUpdate(self):
		EditLine.OnIMEUpdate(self)
		if len(self.GetText()) > 0:
			self.backText.Hide()
		else:
			self.backText.Show()

class RenderTarget(Window):

	def __init__(self, layer = "UI"):
		Window.__init__(self, layer)
		
		self.number = -1

	def __del__(self):
		Window.__del__(self)

	def RegisterWindow(self, layer):
		self.hWnd = wndMgr.RegisterRenderTarget(self, layer)
		
	def SetRenderTarget(self, number):
		self.number = number
		wndMgr.SetRenderTarget(self.hWnd, self.number)


class RenderTargetV2(Window):

	def __init__(self, layer = "UI"):
		Window.__init__(self, layer)
		
		self.index = -1
		self.isHolding = False
		self.mouseLastXPos = 0
		
	def __del__(self):
		Window.__del__(self)

	def RegisterWindow(self, layer):
		self.hWnd = wndMgr.RegisterRenderTarget(self, layer)
		
	def SetRenderTarget(self, index):
		self.index = index
		wndMgr.SetRenderTarget(self.hWnd, self.index)

	def GetRenderTargetIndex(self):
		return self.index

	def SetAutoRotate(self, value):
		renderTarget.SetAutoRotate(self.index, value)

	def OnUpdate(self):
		if self.isHolding == True:
			mouseCurrentPos = self.GetMouseLocalPosition()
			
			difference = mouseCurrentPos[0] - self.mouseLastXPos
			self.mouseLastXPos = mouseCurrentPos[0]
			renderTarget.SetModelRotation(self.index, difference)

	def OnMouseLeftButtonUp(self):
		self.isHolding = False
		app.SetCursor(app.NORMAL)

	def OnMouseLeftButtonDown(self):
		self.isHolding = True
		self.mouseLastXPos = self.GetMouseLocalPosition()[0]
		app.SetCursor(app.CAMERA_ROTATE)

	# def RenderCharacterModel(self):
		# if self.index == -1:
			# return

		# renderTarget.SetBackground(self.index, "d:/ymir work/ui/game/newcharacterui/characterbackground.sub")
		# renderTarget.SetVisibility(self.index, True)
		# renderTarget.RenderPlayer(self.index)
		# self.canUpdateCharacterRender = True

	def OnMouseMiddleScroll(self, len):
		if (len == 0):
			return
		
		renderTarget.ZoomCamera(self.index, len)

RegisterToolTipWindow("TEXT", TextLine)
