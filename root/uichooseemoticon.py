import uiCommon, chat, app, net, item, wndMgr, mouseModule, localeInfo, constInfo
import ui
import CacheEffect as player
import uiScriptLocale
import cfg
import Collision as chr

NEW_EMOTICON_DICT = {
	0 : {
		"PRICE" : "Price: Free",
		"INDEX" : 0,
		"ID_EMOTICON" : 0,
		"IMAGE" : "sweat",
		"X_SCALE" : 1,
		"Y_SCALE" : 1,
	},
	1 : {
		"PRICE" : "Price: Free",
		"INDEX" : 1,
		"ID_EMOTICON" : 1,
		"IMAGE" : "money",
		"X_SCALE" : 1,
		"Y_SCALE" : 1,
	},
	2 : {
		"PRICE" : "Price: Free",
		"INDEX" : 2,
		"ID_EMOTICON" : 2,
		"IMAGE" : "trumpet",
		"X_SCALE" : 1,
		"Y_SCALE" : 1,
	},
	3 : {
		"PRICE" : "Price: Free",
		"INDEX" : 3,
		"ID_EMOTICON" : 3,
		"IMAGE" : "hearts1",
		"X_SCALE" : 1,
		"Y_SCALE" : 1,
	},
	4 : {
		"PRICE" : "Price: Free",
		"INDEX" : 4,
		"ID_EMOTICON" : 4,
		"IMAGE" : "hearts",
		"X_SCALE" : 1,
		"Y_SCALE" : 1,
	},
	5 : {
		"PRICE" : "Price: Free",
		"INDEX" : 5,
		"ID_EMOTICON" : 5,
		"IMAGE" : "bomb",
		"X_SCALE" : 1,
		"Y_SCALE" : 1,
	},
	6 : {
		"PRICE" : "Price: Free",
		"INDEX" : 6,
		"ID_EMOTICON" : 6,
		"IMAGE" : "light",
		"X_SCALE" : 1,
		"Y_SCALE" : 1,
	},
	7 : {
		"PRICE" : "Price: Free",
		"INDEX" : 7,
		"ID_EMOTICON" : 7,
		"IMAGE" : "thunder",
		"X_SCALE" : 1,
		"Y_SCALE" : 1,
	},
	8 : {
		"PRICE" : "Price: Free",
		"INDEX" : 8,
		"ID_EMOTICON" : 8,
		"IMAGE" : "sorry",
		"X_SCALE" : 1,
		"Y_SCALE" : 1,
	},
	9 : {
		"PRICE" : "Price: 100 Points",
		"INDEX" : 9,
		"ID_EMOTICON" : 12,
		"IMAGE" : "smartpepe",
		"X_SCALE" : 0.5,
		"Y_SCALE" : 0.5,
	},
	10 : {
		"PRICE" : "Price: 100 Points",
		"INDEX" : 10,
		"ID_EMOTICON" : 13,
		"IMAGE" : "inlovepepe",
		"X_SCALE" : 0.5,
		"Y_SCALE" : 0.5,
	},
	11 : {
		"PRICE" : "Price: 100 Points",
		"INDEX" : 11,
		"ID_EMOTICON" : 14,
		"IMAGE" : "devilpepe",
		"X_SCALE" : 0.5,
		"Y_SCALE" : 0.5,
	},
	12 : {
		"PRICE" : "Pret 1kkkk",
		"INDEX" : 12,
		"ID_EMOTICON" : 15,
		"IMAGE" : "fatpepe",
		"X_SCALE" : 0.5,
		"Y_SCALE" : 0.5,
	},
	13 : {
		"PRICE" : "Pret 1kkkk",
		"INDEX" : 13,
		"ID_EMOTICON" : 16,
		"IMAGE" : "painpepe",
		"X_SCALE" : 0.5,
		"Y_SCALE" : 0.5,
	},
	14 : {
		"PRICE" : "Pret 1kkkk",
		"INDEX" : 14,
		"ID_EMOTICON" : 17,
		"IMAGE" : "giftheartpepe",
		"X_SCALE" : 0.5,
		"Y_SCALE" : 0.5,
	},
	15 : {
		"PRICE" : "Pret 1kkkk",
		"INDEX" : 15,
		"ID_EMOTICON" : 18,
		"IMAGE" : "bearhugpepe",
		"X_SCALE" : 0.5,
		"Y_SCALE" : 0.5,
	},
	16 : {
		"PRICE" : "Pret 1kkkk",
		"INDEX" : 16,
		"ID_EMOTICON" : 19,
		"IMAGE" : "depressedpepe",
		"X_SCALE" : 1,
		"Y_SCALE" : 1,
	},
	17 : {
		"PRICE" : "Pret 1kkkk",
		"INDEX" : 17,
		"ID_EMOTICON" : 20,
		"IMAGE" : "simppepe",
		"X_SCALE" : 0.5,
		"Y_SCALE" : 0.5,
	},
	18 : {
		"PRICE" : "Pret 1kkkk",
		"INDEX" : 18,
		"ID_EMOTICON" : 21,
		"IMAGE" : "hypepepe",
		"X_SCALE" : 0.5,
		"Y_SCALE" : 0.5,
	},
	19 : {
		"PRICE" : "Pret 1kkkk",
		"INDEX" : 19,
		"ID_EMOTICON" : 22,
		"IMAGE" : "hearteyespepe",
		"X_SCALE" : 0.5,
		"Y_SCALE" : 0.5,
	},
	20 : {
		"PRICE" : "Pret 1kkkk",
		"INDEX" : 20,
		"ID_EMOTICON" : 23,
		"IMAGE" : "happypepe",
		"X_SCALE" : 0.5,
		"Y_SCALE" : 0.5,
	},
	21 : {
		"PRICE" : "Pret 1kkkk",
		"INDEX" : 21,
		"ID_EMOTICON" : 24,
		"IMAGE" : "grinpepe",
		"X_SCALE" : 0.5,
		"Y_SCALE" : 0.5,
	},
	22 : {
		"PRICE" : "Pret 1kkkk",
		"INDEX" : 22,
		"ID_EMOTICON" : 25,
		"IMAGE" : "ewpepe",
		"X_SCALE" : 0.5,
		"Y_SCALE" : 0.5,
	},
	23 : {
		"PRICE" : "Pret 1kkkk",
		"INDEX" : 23,
		"ID_EMOTICON" : 26,
		"IMAGE" : "eyerollpepe",
		"X_SCALE" : 0.5,
		"Y_SCALE" : 0.5,
	},
	24 : {
		"PRICE" : "Pret 1kkkk",
		"INDEX" : 24,
		"ID_EMOTICON" : 27,
		"IMAGE" : "cryingpepe",
		"X_SCALE" : 0.5,
		"Y_SCALE" : 0.5,
	},
	25 : {
		"PRICE" : "Pret 1kkkk",
		"INDEX" : 25,
		"ID_EMOTICON" : 28,
		"IMAGE" : "cringepepe",
		"X_SCALE" : 0.5,
		"Y_SCALE" : 0.5,
	},
	26 : {
		"PRICE" : "Pret 1kkkk",
		"INDEX" : 26,
		"ID_EMOTICON" : 29,
		"IMAGE" : "coolpepe",
		"X_SCALE" : 0.5,
		"Y_SCALE" : 0.5,
	},
	27 : {
		"PRICE" : "Pret 1kkkk",
		"INDEX" : 27,
		"ID_EMOTICON" : 30,
		"IMAGE" : "blushpepe",
		"X_SCALE" : 0.5,
		"Y_SCALE" : 0.5,
	},
	28 : {
		"PRICE" : "Pret 1kkkk",
		"INDEX" : 28,
		"ID_EMOTICON" : 31,
		"IMAGE" : "angelpepe",
		"X_SCALE" : 0.5,
		"Y_SCALE" : 0.5,
	},
	29 : {
		"PRICE" : "Pret 1kkkk",
		"INDEX" : 29,
		"ID_EMOTICON" : 32,
		"IMAGE" : "hehepepe",
		"X_SCALE" : 0.5,
		"Y_SCALE" : 0.5,
	},
	30 : {
		"PRICE" : "Pret 1kkkk",
		"INDEX" : 30,
		"ID_EMOTICON" : 33,
		"IMAGE" : "kisspepe",
		"X_SCALE" : 0.5,
		"Y_SCALE" : 0.5,
	},
	31 : {
		"PRICE" : "Pret 1kkkk",
		"INDEX" : 31,
		"ID_EMOTICON" : 34,
		"IMAGE" : "nerdpepe",
		"X_SCALE" : 0.5,
		"Y_SCALE" : 0.5,
	},
	32 : {
		"PRICE" : "Pret 1kkkk",
		"INDEX" : 32,
		"ID_EMOTICON" : 35,
		"IMAGE" : "monkapepe",
		"X_SCALE" : 0.5,
		"Y_SCALE" : 0.5,
	},
	33 : {
		"PRICE" : "Pret 1kkkk",
		"INDEX" : 33,
		"ID_EMOTICON" : 36,
		"IMAGE" : "okaypepe",
		"X_SCALE" : 0.5,
		"Y_SCALE" : 0.5,
	},
	34 : {
		"PRICE" : "Pret 1kkkk",
		"INDEX" : 34,
		"ID_EMOTICON" : 37,
		"IMAGE" : "heartstruckpepe",
		"X_SCALE" : 0.5,
		"Y_SCALE" : 0.5,
	},
	35 : {
		"PRICE" : "Pret 1kkkk",
		"INDEX" : 35,
		"ID_EMOTICON" : 38,
		"IMAGE" : "tonguepepe",
		"X_SCALE" : 0.5,
		"Y_SCALE" : 0.5,
	},
	36 : {
		"PRICE" : "Pret 1kkkk",
		"INDEX" : 36,
		"ID_EMOTICON" : 39,
		"IMAGE" : "ughpepe",
		"X_SCALE" : 0.5,
		"Y_SCALE" : 0.5,
	},
	37 : {
		"PRICE" : "Pret 1kkkk",
		"INDEX" : 37,
		"ID_EMOTICON" : 40,
		"IMAGE" : "uwupepe",
		"X_SCALE" : 0.5,
		"Y_SCALE" : 0.5,
	},
	38 : {
		"PRICE" : "Pret 1kkkk",
		"INDEX" : 38,
		"ID_EMOTICON" : 41,
		"IMAGE" : "thinkingpepe",
		"X_SCALE" : 0.5,
		"Y_SCALE" : 0.5,
	},
	39 : {
		"PRICE" : "Pret 1kkkk",
		"INDEX" : 39,
		"ID_EMOTICON" : 42,
		"IMAGE" : "smilepepe",
		"X_SCALE" : 0.5,
		"Y_SCALE" : 0.5,
	},
	40 : {
		"PRICE" : "Pret 1kkkk",
		"INDEX" : 40,
		"ID_EMOTICON" : 43,
		"IMAGE" : "surrenderpepe",
		"X_SCALE" : 0.5,
		"Y_SCALE" : 0.5,
	},
	41 : {
		"PRICE" : "Pret 1kkkk",
		"INDEX" : 41,
		"ID_EMOTICON" : 44,
		"IMAGE" : "whatifpepe",
		"X_SCALE" : 0.5,
		"Y_SCALE" : 0.5,
	},
	42 : {
		"PRICE" : "Pret 1kkkk",
		"INDEX" : 42,
		"ID_EMOTICON" : 45,
		"IMAGE" : "sadpepe",
		"X_SCALE" : 0.5,
		"Y_SCALE" : 0.5,
	},
	43 : {
		"PRICE" : "Pret 1kkkk",
		"INDEX" : 43,
		"ID_EMOTICON" : 46,
		"IMAGE" : "peekpepe",
		"X_SCALE" : 0.5,
		"Y_SCALE" : 0.5,
	},
	44 : {
		"PRICE" : "Pret 1kkkk",
		"INDEX" : 44,
		"ID_EMOTICON" : 47,
		"IMAGE" : "angrypepe",
		"X_SCALE" : 0.5,
		"Y_SCALE" : 0.5,
	},
	45 : {
		"PRICE" : "Pret 1kkkk",
		"INDEX" : 45,
		"ID_EMOTICON" : 48,
		"IMAGE" : "leyemoticon",
		"X_SCALE" : 0.8,
		"Y_SCALE" : 0.8,
	},
	46 : {
		"PRICE" : "Pret 1kkkk",
		"INDEX" : 46,
		"ID_EMOTICON" : 49,
		"IMAGE" : "dollar",
		"X_SCALE" : 0.5,
		"Y_SCALE" : 0.5,
	},
	47 : {
		"PRICE" : "Pret 1kkkk",
		"INDEX" : 47,
		"ID_EMOTICON" : 50,
		"IMAGE" : "begone",
		"X_SCALE" : 0.8,
		"Y_SCALE" : 0.8,
	},
	48 : {
		"PRICE" : "Pret 1kkkk",
		"INDEX" : 48,
		"ID_EMOTICON" : 51,
		"IMAGE" : "laughpepeanim",
		"X_SCALE" : 0.5,
		"Y_SCALE" : 0.5,
	},
	49 : {
		"PRICE" : "Pret 1kkkk",
		"INDEX" : 49,
		"ID_EMOTICON" : 52,
		"IMAGE" : "pepeblushanim",
		"X_SCALE" : 0.5,
		"Y_SCALE" : 0.5,
	},
	50 : {
		"PRICE" : "Pret 1kkkk",
		"INDEX" : 50,
		"ID_EMOTICON" : 53,
		"IMAGE" : "suspiciouspepe",
		"X_SCALE" : 0.5,
		"Y_SCALE" : 0.5,
	},
	51 : {
		"PRICE" : "Pret 1kkkk",
		"INDEX" : 51,
		"ID_EMOTICON" : 54,
		"IMAGE" : "haha",
		"X_SCALE" : 0.8,
		"Y_SCALE" : 0.8,
	},
	52 : {
		"PRICE" : "Pret 1kkkk",
		"INDEX" : 51,
		"ID_EMOTICON" : 55,
		"IMAGE" : "catawkward",
		"X_SCALE" : 0.8,
		"Y_SCALE" : 0.8,
	},
}

class ChooseEmoticonBuy(ui.ScriptWindow):
	def __init__(self):
		ui.ScriptWindow.__init__(self)
		self.wndEmoticon = None
		self.isLoaded = 0
		self.__LoadWindow()

	def __del__(self):
		ui.ScriptWindow.__del__(self)

	def BindEmoticon(self, wnd):
		self.wndEmoticon = wnd

	def __LoadWindow(self):
		if self.isLoaded == 1:
			return

		self.isLoaded = 1
		self.AddFlag("float")
		self.AddFlag("movable")
		self.AddFlag("animation")
		
		self.board = ui.BoardWithTitleBar()
		self.board.SetParent(self)
		self.board.AddFlag("not_pick")
		self.board.SetPosition(0,0)
		self.board.SetSize(340,390)
		self.board.SetTitleName("Schimbare emoticoane")
		self.board.SetCloseEvent(ui.__mem_func__(self.OnPressEscapeKey))
		self.board.Show()
		self.borderClear = ui.BorderA()
		self.borderClear.SetParent(self.board)
		self.borderClear.SetPosition(15,35)
		self.borderClear.SetSize(370 - 61, 390 - 50)
		self.borderClear.Show()
		
		self.ScrollBar = ui.ScrollBar()
		self.ScrollBar.SetParent(self.board)
		self.ScrollBar.SetPosition(324, 35)
		self.ScrollBar.SetScrollBarSize(339)
		self.ScrollBar.Show()
	
		self.wndListBox = ui.ListBoxExLey()
		self.wndListBox.SetSize(500, 660)
		self.wndListBox.SetParent(self.board)
		self.wndListBox.SetNewPos(25, 45)
		self.wndListBox.SetViewItemCount(3)
		self.wndListBox.SetItemStep(110)
		self.wndListBox.SetItemSize(260, 150)
		self.wndListBox.SetScrollBar(self.ScrollBar)
		self.wndListBox.Show()
		
		self.index = 0
		
		self.dictButtons = {}
		self.dictButtons2 = {}
		self.dictButtons3 = {}
		
		self.elemente = {}
		
		index = 0
		for i in xrange(len(NEW_EMOTICON_DICT) - 1):
			if index >= len(NEW_EMOTICON_DICT):
				break
			
			self.dictButtons[i] = ui.MakeButton(self.board, 0, 0, False, "d:/ymir work/ui/game/emoticon_renewal/", "detail_item_small.png","detail_item_over.png","detail_item_down.png")
			# self.dictButtons[i].SetButtonColor((1.0, 1.0, 0.0, 1.0))
			self.dictButtons[i].SetButtonScale(0.7, 0.7)
			self.dictButtons[i].SetEvent(ui.__mem_func__(self.Select), index)
			self.dictButtons[i].Show()

			self.elemente[i] = {}

			self.elemente[i]["text_3"] = ui.MakeTextV3(self.dictButtons[i], "Emoticon %s" % NEW_EMOTICON_DICT[index]["INDEX"], -86, 1, False)
			self.elemente[i]["text_3"].SetWindowHorizontalAlignCenter()
			self.elemente[i]["text_3"].SetHorizontalAlignCenter()
			self.elemente[i]["text_3"].Show()
			
			self.elemente[i]["text_1"] = ui.MakeTextV3(self.dictButtons[i], "%s " % NEW_EMOTICON_DICT[index]["IMAGE"], -84, 80, False)
			self.elemente[i]["text_1"].SetWindowHorizontalAlignCenter()
			self.elemente[i]["text_1"].SetHorizontalAlignCenter()
			self.elemente[i]["text_1"].Show()
		
			self.elemente[i]["poza_1"] = ui.MakeImageBoxNew(self.dictButtons[i], "d:/ymir work/ui/game/emoticon_renewal/emotes/%s.png" % (NEW_EMOTICON_DICT[index]["IMAGE"]), -85, -25, 0.6, 0.6)
			self.elemente[i]["poza_1"].SetWindowHorizontalAlignCenter()
			self.elemente[i]["poza_1"].SetWindowVerticalAlignCenter()
			self.elemente[i]["poza_1"].AddFlag('attach')
			self.elemente[i]["poza_1"].AddFlag('not_pick')
			
			self.elemente[i]["poza_1"].SetScale(NEW_EMOTICON_DICT[index]["X_SCALE"], NEW_EMOTICON_DICT[index]["Y_SCALE"])

			if index + 1 < len(NEW_EMOTICON_DICT):
				self.dictButtons2[i] = ui.MakeButton(self.dictButtons[i], 100, 0, False ,"d:/ymir work/ui/game/emoticon_renewal/", "detail_item_small.png","detail_item_over.png","detail_item_down.png")
				self.dictButtons2[i].SetEvent(ui.__mem_func__(self.Select), index + 1)
				self.dictButtons2[i].SetButtonScale(0.7, 0.7)

				self.dictButtons2[i].Show()

				self.elemente[i]["poza_2"] = ui.MakeImageBoxNew(self.dictButtons2[i], "d:/ymir work/ui/game/emoticon_renewal/emotes/%s.png" % (NEW_EMOTICON_DICT[index + 1]["IMAGE"]), 0, -3, 0.8, 0.8)
				self.elemente[i]["poza_2"].SetWindowHorizontalAlignCenter()
				self.elemente[i]["poza_2"].SetWindowVerticalAlignCenter()
				self.elemente[i]["poza_2"].AddFlag('attach')
				self.elemente[i]["poza_2"].AddFlag('not_pick')
				
				self.elemente[i]["poza_2"].SetScale(NEW_EMOTICON_DICT[index + 1]["X_SCALE"], NEW_EMOTICON_DICT[index + 1]["Y_SCALE"])
				
				self.elemente[i]["text_2"] = ui.MakeTextV3(self.dictButtons2[i], "%s " % NEW_EMOTICON_DICT[index + 1]["IMAGE"], 2, 80, False)
				self.elemente[i]["text_2"].SetWindowHorizontalAlignCenter()
				self.elemente[i]["text_2"].SetHorizontalAlignCenter()
				self.elemente[i]["text_2"].Show()
				
				self.elemente[i]["text_4"] = ui.MakeTextV3(self.dictButtons2[i], "Emoticon %s" % NEW_EMOTICON_DICT[index + 1]["INDEX"], 0, 1, False)
				self.elemente[i]["text_4"].SetWindowHorizontalAlignCenter()
				self.elemente[i]["text_4"].SetHorizontalAlignCenter()
				self.elemente[i]["text_4"].Show()
			
			if index + 2 < len(NEW_EMOTICON_DICT):
				self.dictButtons3[i] = ui.MakeButton(self.dictButtons[i], 200, 0, False ,"d:/ymir work/ui/game/emoticon_renewal/", "detail_item_small.png","detail_item_over.png","detail_item_down.png")
				self.dictButtons3[i].SetEvent(ui.__mem_func__(self.Select), index + 2)
				self.dictButtons3[i].SetButtonScale(0.7, 0.7)

				self.dictButtons3[i].Show()

				self.elemente[i]["poza_3"] = ui.MakeImageBoxNew(self.dictButtons3[i], "d:/ymir work/ui/game/emoticon_renewal/emotes/%s.png" % (NEW_EMOTICON_DICT[index + 2]["IMAGE"]), 0, -3, 0.8, 0.8)
				self.elemente[i]["poza_3"].SetWindowHorizontalAlignCenter()
				self.elemente[i]["poza_3"].SetWindowVerticalAlignCenter()
				self.elemente[i]["poza_3"].AddFlag('attach')
				self.elemente[i]["poza_3"].AddFlag('not_pick')
				
				self.elemente[i]["poza_3"].SetScale(NEW_EMOTICON_DICT[index + 2]["X_SCALE"], NEW_EMOTICON_DICT[index + 2]["Y_SCALE"])
				
				self.elemente[i]["text_5"] = ui.MakeTextV3(self.dictButtons3[i], "%s " % NEW_EMOTICON_DICT[index + 2]["IMAGE"], 2, 80, False)
				self.elemente[i]["text_5"].SetWindowHorizontalAlignCenter()
				self.elemente[i]["text_5"].SetHorizontalAlignCenter()
				self.elemente[i]["text_5"].Show()
				
				self.elemente[i]["text_6"] = ui.MakeTextV3(self.dictButtons3[i], "Emoticon %s" % NEW_EMOTICON_DICT[index + 2]["INDEX"], 0, 1, False)
				self.elemente[i]["text_6"].SetWindowHorizontalAlignCenter()
				self.elemente[i]["text_6"].SetHorizontalAlignCenter()
				self.elemente[i]["text_6"].Show()
			
			self.wndListBox.AppendItem(self.dictButtons[i], self.board)
			
			index += 3
		self.ScrollBar.SetScrollStep(float(2) / float(self.wndListBox.GetCountItems()+1))
		self.ScrollBar.SetMiddleBarSize(float(6) / float(self.wndListBox.GetCountItems()+1))

		self.wndListBox.SetBasePos(0)
		self.SetSize(self.board.GetWidth(), self.board.GetHeight())

	def SetIndex(self, index):
		self.index = index

	def OnRunMouseWheel(self, nLen):
		if nLen > 0:
			self.ScrollBar.OnUp()
		else:
			self.ScrollBar.OnDown()
			
	def SaveEmoticonSettings(self, index, emoticon_id):
		cfg.Set(cfg.SAVE_GENERAL, "EMOTICON_%d" % int(index), int(emoticon_id))
		
	def Select(self, index):
		if player.IsPremiumUser() == 1 or player.IsPremiumUser() == 2 or player.IsPremiumUser() == 3:
			self.SaveEmoticonSettings(self.index, NEW_EMOTICON_DICT[index]["ID_EMOTICON"])
	
			self.emoticonCfg = cfg.Get(cfg.SAVE_GENERAL, "EMOTICON_%s" % self.index)
	
			player.SetEmoticonForNum(self.index, int(self.emoticonCfg))
	
			if self.wndEmoticon:
				self.wndEmoticon.AppendEmoticon(self.index, index)
				self.Hide()
				
			self.OnPressEscapeKey()
		else:
			chat.AppendChat(1, "Nu esti utilizator premium.")

	def Show(self):
		self.SetCenterPosition()
		self.SetTop()
		ui.ScriptWindow.Show(self)
		
	# def OnUpdate(self):
		# if chr.IsDeimosPremium(player.GetMainCharacterIndex()) == False or chr.IsDeimosPremiumV2(player.GetMainCharacterIndex()) == False:
			# self.Hide()
		
	def OnPressEscapeKey(self):
		self.Hide()
		return True

class ChooseEmoticon(ui.ScriptWindow):
	def __init__(self):
		ui.ScriptWindow.__init__(self)
		self.isLoaded = 0

		self.__LoadWindow()

	def __del__(self):
		ui.ScriptWindow.__del__(self)

	def __LoadWindow(self):
		if self.isLoaded == 1:
			return

		self.isLoaded = 1
		self.AddFlag("float")
		self.AddFlag("movable")
		self.AddFlag("animation")
		
		self.board = ui.BoardWithTitleBar()
		self.board.SetParent(self)
		self.board.AddFlag("not_pick")
		self.board.SetPosition(0,0)
		self.board.SetSize(340,390)
		self.board.SetTitleName("Schimbare emoticoane")
		self.board.SetCloseEvent(ui.__mem_func__(self.Close))
		self.board.Show()
		
		self.borderClear = ui.BorderA()
		self.borderClear.SetParent(self.board)
		self.borderClear.SetPosition(15,35)
		self.borderClear.SetSize(370 - 61, 390 - 50)
		self.borderClear.Show()
		
		self.EmoticonShop = ChooseEmoticonBuy()
		self.EmoticonShop.BindEmoticon(self)
		self.EmoticonShop.Hide()

		self.FirstControlTexts = {}
		self.SecondControlTexts = {}
		self.ThirdControlTexts = {}
		
		self.FirstNameButtons = {}
		self.SecondNameButtons = {}
		self.ThirdNameButtons = {}
	
		self.EmoticonNames = {}

		self.FirstRound = {}
		self.SecondRound = {}
		self.ThirdRound = {}

		self.BuildSlots()
		self.BuildButtons()
		
		self.LoadEmoticonSettings()
		self.SetSize(self.board.GetWidth(), self.board.GetHeight())

	def Show(self):
		self.SetCenterPosition()
		ui.ScriptWindow.Show(self)
		
	def LoadEmoticonSettings(self):
		for x in xrange(9):
			self.emoticonCfg = cfg.Get(cfg.SAVE_GENERAL, "EMOTICON_%s" % x)

	def BuildSlots(self):
		for i in xrange(3):
			self.FirstRound[i] = ui.MakeImageBoxNew(self.board, "d:/ymir work/ui/wiki/detail_item_small.tga", 25+100*i, 45, 0.7, 0.7)
			self.FirstRound[i].Show()
			
			self.SecondRound[i] = ui.MakeImageBoxNew(self.board, "d:/ymir work/ui/wiki/detail_item_small.tga", 25+100*i, 155, 0.7, 0.7)
			self.SecondRound[i].Show()
			
			self.ThirdRound[i] = ui.MakeImageBoxNew(self.board, "d:/ymir work/ui/wiki/detail_item_small.tga", 25+100*i, 265, 0.7, 0.7)
			self.ThirdRound[i].Show()
			
		self.dictPhotos = {}
		
		for i in xrange(9):
			if i < 3:
				parent = self.FirstRound[i]
			
			if i >= 3 and i < 6:
				parent = self.SecondRound[i - 3]
				
			if i >= 6:
				parent = self.ThirdRound[i - 6]
			self.emoticonCfg = cfg.Get(cfg.SAVE_GENERAL, "EMOTICON_%s" % i)
			
			self.dictPhotos[i] = ui.MakeImageBoxNew(parent, "d:/ymir work/ui/wiki/detail_item_small.tga", 11, 16, 0.7, 0.7)
			if int(self.emoticonCfg) < 9:
				self.dictPhotos[i].LoadImage("d:/ymir work/ui/game/emoticon_renewal/emotes/%s.png" % (NEW_EMOTICON_DICT[int(self.emoticonCfg)]["IMAGE"]))
				self.dictPhotos[i].SetScale(NEW_EMOTICON_DICT[int(self.emoticonCfg)]["X_SCALE"], NEW_EMOTICON_DICT[int(self.emoticonCfg)]["X_SCALE"])
			else:
				self.dictPhotos[i].LoadImage("d:/ymir work/ui/game/emoticon_renewal/emotes/%s.png" % (NEW_EMOTICON_DICT[int(self.emoticonCfg) - 3]["IMAGE"]))
				self.dictPhotos[i].SetScale(NEW_EMOTICON_DICT[int(self.emoticonCfg) - 3]["X_SCALE"], NEW_EMOTICON_DICT[int(self.emoticonCfg) - 3]["X_SCALE"])

	def BuildButtons(self):
		for i in xrange(3):
			self.FirstNameButtons[i] = ui.MakeButton(self.FirstRound[i], 0, 80, False ,"d:/ymir work/ui/game/questtimer/", "btn_normal.png","btn_hover.png","btn_down.png")
			self.FirstNameButtons[i].SetEvent(ui.__mem_func__(self.OpenShop), i)
			self.FirstNameButtons[i].SetButtonScale(0.9, 0.8)
			self.FirstNameButtons[i].Show()
			
			self.SecondNameButtons[i] = ui.MakeButton(self.SecondRound[i], 0, 80, False ,"d:/ymir work/ui/game/questtimer/", "btn_normal.png","btn_hover.png","btn_down.png")
			self.SecondNameButtons[i].SetEvent(ui.__mem_func__(self.OpenShop), i + 3)
			self.SecondNameButtons[i].SetButtonScale(0.9, 0.8)
			self.SecondNameButtons[i].Show()

			self.ThirdNameButtons[i] = ui.MakeButton(self.ThirdRound[i], 0, 80, False ,"d:/ymir work/ui/game/questtimer/", "btn_normal.png","btn_hover.png","btn_down.png")
			self.ThirdNameButtons[i].SetEvent(ui.__mem_func__(self.OpenShop), i + 6)
			self.ThirdNameButtons[i].SetButtonScale(0.9, 0.8)
			self.ThirdNameButtons[i].Show()

			FirstControlText = [1, 2, 3]
			SecondControlText = [4, 5, 6]
			ThirdControlText = [7, 8, 9]

			self.FirstControlTexts[i] = ui.MakeTextV3(self.FirstRound[i], "CTRL+%s " % FirstControlText[i], 0, 1, False)
			self.FirstControlTexts[i].SetWindowHorizontalAlignCenter()
			self.FirstControlTexts[i].SetHorizontalAlignCenter()
			self.FirstControlTexts[i].Show()
			
			self.SecondControlTexts[i] = ui.MakeTextV3(self.SecondRound[i], "CTRL+%s " % SecondControlText[i], 0, 1, False)
			self.SecondControlTexts[i].SetWindowHorizontalAlignCenter()
			self.SecondControlTexts[i].SetHorizontalAlignCenter()
			self.SecondControlTexts[i].Show()
			
			self.ThirdControlTexts[i] = ui.MakeTextV3(self.ThirdRound[i], "CTRL+%s " % ThirdControlText[i], 0, 1, False)
			self.ThirdControlTexts[i].SetWindowHorizontalAlignCenter()
			self.ThirdControlTexts[i].SetHorizontalAlignCenter()
			self.ThirdControlTexts[i].Show()
	
			self.emoticonCfg = cfg.Get(cfg.SAVE_GENERAL, "EMOTICON_%s" % i)

		for i in xrange(9):
			if i < 3:
				parent = self.FirstNameButtons[i]
			
			if i >= 3 and i < 6:
				parent = self.SecondNameButtons[i - 3]
				
			if i >= 6:
				parent = self.ThirdNameButtons[i - 6]
				
			self.emoticonCfg = cfg.Get(cfg.SAVE_GENERAL, "EMOTICON_%s" % i)

			if int(self.emoticonCfg) < 9:
				self.EmoticonNames[i] = ui.MakeTextV3(parent, "%s" % (NEW_EMOTICON_DICT[int(self.emoticonCfg)]["IMAGE"]), 0, 2, False)
			else:
				self.EmoticonNames[i] = ui.MakeTextV3(parent, "%s" % (NEW_EMOTICON_DICT[int(self.emoticonCfg) - 3]["IMAGE"]), 0, 2, False)

			self.EmoticonNames[i].SetWindowHorizontalAlignCenter()
			self.EmoticonNames[i].SetHorizontalAlignCenter()
			self.EmoticonNames[i].Show()
			
	def OpenShop(self, arg):
		if player.IsPremiumUser() == 1 or player.IsPremiumUser() == 2 or player.IsPremiumUser() == 3:
			self.EmoticonShop.SetIndex(arg)
			self.EmoticonShop.Show()
		else:
			chat.AppendChat(1, "Nu esti utilizator premium.")

	def AppendEmoticon(self, index, index_load):
		self.dictPhotos[index].LoadImage("d:/ymir work/ui/game/emoticon_renewal/emotes/%s.png" % (NEW_EMOTICON_DICT[index_load]["IMAGE"]))
		self.dictPhotos[index].SetScale(NEW_EMOTICON_DICT[index_load]["X_SCALE"], NEW_EMOTICON_DICT[index_load]["X_SCALE"])
		
		if index < 3:
			parent = self.FirstNameButtons[index]
		
		if index >= 3 and index < 6:
			parent = self.SecondNameButtons[index - 3]
			
		if index >= 6:
			parent = self.ThirdNameButtons[index - 6]

		self.EmoticonNames[index] = ui.MakeTextV3(parent, "%s" % (NEW_EMOTICON_DICT[index_load]["IMAGE"]), 0, 2, False)
		self.EmoticonNames[index].SetWindowHorizontalAlignCenter()
		self.EmoticonNames[index].SetHorizontalAlignCenter()
		self.EmoticonNames[index].Show()
		
	# def OnUpdate(self):
		# if chr.IsDeimosPremium(player.GetMainCharacterIndex()) == False or chr.IsDeimosPremiumV2(player.GetMainCharacterIndex()) == False:
			# self.Close()
			
	def Close(self):
		self.Hide()

	def Destroy(self):
		self.board = None
		self.EmoticonShop = None
		self.ClearDictionary()
		
	def Open(self):
		self.SetTop()
		self.Show()

	def OnPressEscapeKey(self):
		self.Close()
		return True
