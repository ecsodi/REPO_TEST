import thenewui as ui
import item
import net
import constInfo
import localeInfo
import uiCommon
import wndMgr
import app
import grp
import chat
import CacheEffect as player
import skill
import nonplayer
import shop
import chr
import math
from _weakref import proxy
import uiToolTip
import ime
import renderTarget
RENDER_TARGET_INDEX = 222

class RemoteShopWindow(ui.ScriptWindow):
	def __init__(self):
		ui.ScriptWindow.__init__(self)
		self.bLoaded = 0
		self.npcVnum = 0
		self.LoadWindow()

	def __del__(self):
		ui.ScriptWindow.__del__(self)
		
		self.BorderInfo = None
		self.BannerImage = None
		self.TitleImage = None
		self.ShopInfo = None
		self.BorderRender = None
		self.comboBox = None
		self.npcVnum = 0
		
		if self.ModelPreview:
			self.ModelPreview.Hide()
			renderTarget.SetVisibility(RENDER_TARGET_INDEX, False)
			self.ModelPreview = None
			
	def Show(self):
		self.SetCenterPosition()
		ui.ScriptWindow.Show(self)

	def LoadWindow(self):
		if self.bLoaded == 1:
			return

		self.bLoaded = 1
		
		self.AddFlag("float")
		self.AddFlag("movable")
		self.AddFlag("animation")
		
		BOARD_WIDTH = 320
		BOARD_HEIGHT = 420
		
		self.Board = ui.BoardWithTitleBar()
		self.Board.SetParent(self)
		self.Board.SetSize(BOARD_WIDTH, BOARD_HEIGHT)
		self.Board.AddFlag("not_pick")
		self.Board.SetTitleName("Deschide Magazin")
		self.Board.SetCloseEvent(ui.__mem_func__(self.Close))
		self.Board.Show()
		
		self.BorderInfo = ui.BorderB()
		self.BorderInfo.SetParent(self.Board)
		self.BorderInfo.SetPosition(10, 30)
		self.BorderInfo.SetSize(BOARD_WIDTH - 20, BOARD_HEIGHT - 40)
		self.BorderInfo.Show()

		self.BannerImage = ui.ImageBox()
		self.BannerImage.SetParent(self.BorderInfo)
		self.BannerImage.SetPosition(5, 3)
		self.BannerImage.LoadImage("d:/ymir work/ui/game/distance_shop/banner.png")
		self.BannerImage.Show()
		
		self.TitleImage = ui.ImageBox()
		self.TitleImage.SetParent(self.BorderInfo)
		self.TitleImage.SetPosition(5, 73)
		self.TitleImage.LoadImage("d:/ymir work/ui/game/distance_shop/titlebar.png")
		self.TitleImage.SetScale(0.96, 1.0)
		self.TitleImage.Show()

		self.ShopInfo = ui.TextLine()
		self.ShopInfo.SetParent(self.TitleImage)
		self.ShopInfo.SetPosition(66, 2)
		self.ShopInfo.SetText("Alege un magazin din lista de mai jos!")
		self.ShopInfo.Show()

		self.BorderRender = ui.BorderB()
		self.BorderRender.SetParent(self.BorderInfo)
		self.BorderRender.SetPosition(10, 95)
		self.BorderRender.SetSize(BOARD_WIDTH - 40, BOARD_HEIGHT - 145)
		self.BorderRender.Show()

		self.npcVnum = 0

		self.btnOpenShop = ui.MakeButton(self.BorderRender, 0, 275-35, False, "d:/ymir work/ui/public/", "AcceptButton00.sub", "AcceptButton01.sub", "AcceptButton02.sub")
		self.btnOpenShop.SetWindowHorizontalAlignCenter()
		self.btnOpenShop.SetEvent(ui.__mem_func__(self.OpenShop))

		self.comboBox = ui.ComboBox()
		self.comboBox.SetParent(self.BorderRender)
		self.comboBox.SetPosition(0, 210)
		self.comboBox.SetSize(120, 14)
		self.comboBox.ClearItem()
		self.comboBox.SetWindowHorizontalAlignCenter()
		self.comboBox.SetEvent(self.OnSelectItem)
		
		self.comboBox.SetCurrentItem("Alege Magazin")
		
		self.categories = (["Magazinul general", 0, 9003],["Negustorul de arme", 1, 20094],["Negustorul de armuri", 2, 20094],["Negustor permise", 3, 30307],["Consumabile", 4, 20010],["Alchimie", 5, 20001],["Biolog", 6, 20084],["Curele", 7, 20090],["Magazin accesorii", 8, 20094],["Theowahdan", 9, 20406],["Finisaje", 10, 9003],["Pescar", 11, 9009])
		for category in self.categories:
			self.comboBox.InsertItem(category[1], category[0])
		
		self.comboBox.Show()

		self.ModelPreview = ui.RenderTarget()
		self.ModelPreview.SetParent(self.BorderRender)
		self.ModelPreview.SetSize(170, 200)
		self.ModelPreview.SetPosition(0, 5)
		self.ModelPreview.SetWindowHorizontalAlignCenter()
		self.ModelPreview.SetRenderTarget(RENDER_TARGET_INDEX)
		self.ModelPreview.Show()

		renderTarget.SetBackground(RENDER_TARGET_INDEX, "d:/ymir work/ui/game/myshop_deco/model_view_bg.sub")
		renderTarget.SetVisibility(RENDER_TARGET_INDEX, True)

		self.SetSize(self.Board.GetWidth(), self.Board.GetHeight())
		
	def OnSelectItem(self, id):
		category = self.categories[id]
		self.comboBox.SetCurrentItem("%s" % category[0])
		renderTarget.SelectModel(RENDER_TARGET_INDEX, category[2])
		if id > 7:
			self.npcVnum = int(category[1]) + 1
		else:
			self.npcVnum = category[1]
			
	def OpenShop(self):
		net.SendRemoteShopPacket(self.npcVnum)
		
	def Destroy(self):
		self.ClearDictionary()
		self.BorderInfo = None
		self.BannerImage = None
		self.TitleImage = None
		self.ShopInfo = None
		self.BorderRender = None
		self.comboBox = None
		
	def Close(self):
		self.Hide()
	
	def OnPressEscapeKey(self):		
		self.Close()
		return True	
