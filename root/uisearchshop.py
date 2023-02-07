import thenewui as ui
import item
import skill
import grp
import localeInfo
import uiScriptLocale
import net
import shop
import uiCommon
import collections
import CacheEffect as player
import app
import chat
from uiguild import CheckBox

ITEM_DICT = collections.OrderedDict(sorted(item.GetItemsInfo().items()))
SKILL_DICT = skill.GetSkillInfo()

RACE_DICT = {
	localeInfo.SEARCH_SHOP_ALL : -1,
	localeInfo.JOB_WARRIOR : 0,
	localeInfo.JOB_ASSASSIN : 1,
	localeInfo.JOB_SURA : 2,
	localeInfo.JOB_SHAMAN : 3,
}

SUB_TYPE_IGNORE = {
    0 : [1, 2, 4, 5, 9],
    1 : [3, 4, 5],
    2 : [1, 2, 3, 4, 5, 9],
    3 : [0, 1, 2, 3, 9],
}

ITEM_TYPE_DICT = {
	localeInfo.SEARCH_SHOP_ALL : {"typeID" : -1, "subtypes" : {}},
	localeInfo.SEARCH_SHOP_ITEM_USE : 
    {
		"typeID" : 3, 
		"subtypes" : 
        {
			localeInfo.SEARCH_SHOP_ITEM_USE_POTION : item.USE_POTION,
			localeInfo.SEARCH_SHOP_ITEM_USE_TUNING : item.USE_TUNING,
			localeInfo.SEARCH_SHOP_ITEM_USE_ABILITY_UP : item.USE_ABILITY_UP,
			localeInfo.SEARCH_SHOP_ITEM_USE_POTION_NODELAY : item.USE_POTION_NODELAY,
			localeInfo.SEARCH_SHOP_ITEM_USE_CLEAR : item.USE_CLEAR,
			localeInfo.SEARCH_SHOP_ITEM_USE_DETACHMENT : item.USE_DETACHMENT,
			localeInfo.SEARCH_SHOP_ITEM_USE_SPECIAL : item.USE_SPECIAL,
        }
    },
	localeInfo.SEARCH_SHOP_ITEM_MATERIAL : {"typeID" : 5, "subtypes" : {0}},
	localeInfo.SEARCH_SHOP_ITEM_METIN : 
    {
		"typeID" : 10, 
		"subtypes" : 
        {
            localeInfo.SEARCH_SHOP_ITEM_METIN_NORMAL : item.METIN_NORMAL,
        }
    },
	localeInfo.SEARCH_SHOP_ITEM_RESOURCES : {"typeID" : 14, "subtypes" : {0}},
	localeInfo.SEARCH_SHOP_ITEM_SKILLBOOK : {"typeID" : 17, "subtypes" : {0}},
	localeInfo.SEARCH_SHOP_ITEM_GIFTBOX : {"typeID" : 23, "subtypes" : {0}},
	localeInfo.SEARCH_SHOP_ITEM_BLEND : {"typeID" : 27, "subtypes" : {0}},
	localeInfo.SEARCH_SHOP_ITEM_DS : 
    {
		"typeID" : 29, 
		"subtypes" : 
        {
            localeInfo.SEARCH_SHOP_ITEM_DS_1 : item.DRAGON_STONE_DRAGON_DIAMOND,
            localeInfo.SEARCH_SHOP_ITEM_DS_2 : item.DRAGON_STONE_DRAGON_RUBY,
            localeInfo.SEARCH_SHOP_ITEM_DS_3 : item.DRAGON_STONE_DRAGON_JADE,
            localeInfo.SEARCH_SHOP_ITEM_DS_4 : item.DRAGON_STONE_DRAGON_SAPPHIRE,
            localeInfo.SEARCH_SHOP_ITEM_DS_5 : item.DRAGON_STONE_DRAGON_GARNET,
            localeInfo.SEARCH_SHOP_ITEM_DS_6 : item.DRAGON_STONE_DRAGON_ONYX,
        }
    },
	localeInfo.SEARCH_SHOP_ITEM_RING : {"typeID" : 33, "subtypes" : {0}},
	localeInfo.SEARCH_SHOP_ITEM_BELT : {"typeID" : 34, "subtypes" : {0}},
    localeInfo.SEARCH_SHOP_ITEM_QUEST : {"typeID" : 18, "subtypes" : {0}},

	localeInfo.SEARCH_SHOP_ITEM_WEAPON : 
    {
		"typeID" : 1,
		"subtypes" : 
        {
			localeInfo.SEARCH_SHOP_ITEM_WEAPON_SWORD : item.WEAPON_SWORD,
			localeInfo.SEARCH_SHOP_ITEM_WEAPON_DAGGER : item.WEAPON_DAGGER,
			localeInfo.SEARCH_SHOP_ITEM_WEAPON_BOW : item.WEAPON_BOW,
			localeInfo.SEARCH_SHOP_ITEM_WEAPON_TWO_HANDED : item.WEAPON_TWO_HANDED,
			localeInfo.SEARCH_SHOP_ITEM_WEAPON_BELL : item.WEAPON_BELL,
			localeInfo.SEARCH_SHOP_ITEM_WEAPON_FAN : item.WEAPON_FAN,
		}
	},

	localeInfo.SEARCH_OBJECT_EQUIP : 
    {
		"typeID" : 2,
		"subtypes" : 
        {
			localeInfo.SEARCH_OBJECT_ARMOR : item.ARMOR_BODY,
			localeInfo.SEARCH_OBJECT_HEAD : item.ARMOR_HEAD,
			localeInfo.SEARCH_OBJECT_SHIELD : item.ARMOR_SHIELD,
			localeInfo.SEARCH_OBJECT_WRIST : item.ARMOR_WRIST,
			localeInfo.SEARCH_OBJECT_SHOES : item.ARMOR_FOOTS,
			localeInfo.SEARCH_OBJECT_NECK : item.ARMOR_NECK,
			localeInfo.SEARCH_OBJECT_EAR : item.ARMOR_EAR,
			localeInfo.SEARCH_OBJECT_PENDANT : item.ARMOR_PENDANT,
		}
	},
	
	# localeInfo.SEARCH_SHOP_ITEM_INFINITE : 
    # {
		# "typeID" : 37,
		# "subtypes" : 
        # {
			# localeInfo.SEARCH_SHOP_ITEM_INFINITE_POTIONS : item.INFINITE_TYPE_POTION,
			# localeInfo.SEARCH_SHOP_ITEM_INFINITE_MALL : item.INFINITE_TYPE_MALL,
		# }
	# },
    
	# localeInfo.SEARCH_SHOP_ITEM_PENDANT : 
    # {
		# "typeID" : 38,
		# "subtypes" : 
        # {
			# localeInfo.SEARCH_SHOP_ITEM_PENDANT_FIRE : 0,
			# localeInfo.SEARCH_SHOP_ITEM_PENDANT_ICE : 1,
			# localeInfo.SEARCH_SHOP_ITEM_PENDANT_EARTH : 2,
			# localeInfo.SEARCH_SHOP_ITEM_PENDANT_DARK : 3,
			# localeInfo.SEARCH_SHOP_ITEM_PENDANT_WIND : 4,
			# localeInfo.SEARCH_SHOP_ITEM_PENDANT_LIGHTNING : 5,
		# }
	# },

	# localeInfo.SEARCH_SHOP_ITEM_PET : 
    # {
		# "typeID" : 36,
		# "subtypes" : 
        # {
			# localeInfo.SEARCH_SHOP_ITEM_PET_LEVELABLE : item.PET_LEVELABLE,
			# localeInfo.SEARCH_SHOP_ITEM_PET_EGG : item.PET_EGG,
			# localeInfo.SEARCH_SHOP_ITEM_PET_TRANSPORTBOX : item.PET_TRANSPORTBOX,
			# localeInfo.SEARCH_SHOP_ITEM_PET_BOOK : item.PET_BOOK,
			# localeInfo.SEARCH_SHOP_ITEM_PET_PROTEIN : item.PET_PROTEIN,
			# localeInfo.SEARCH_SHOP_ITEM_PET_CHANGE_NAME : item.PET_CHANGE_NAME_ITEM,
			# localeInfo.SEARCH_SHOP_ITEM_PET_REVIVE : item.PET_REVIVE_ITEM,
		# }
	# },

	localeInfo.SEARCH_SHOP_ITEM_COSTUME : 
    {
		"typeID" : 28,
		"subtypes" : 
        {
			localeInfo.SEARCH_OBJECT_COSTUME : item.COSTUME_TYPE_BODY,
			localeInfo.SEARCH_OBJECT_HAIR : item.COSTUME_TYPE_HAIR,
			localeInfo.SEARCH_OBJECT_SASH : item.COSTUME_TYPE_SASH,
			localeInfo.SEARCH_OBJECT_SASHSKIN : item.COSTUME_SKIN_SASH,
			localeInfo.SEARCH_OBJECT_COSTUMEWEAP : item.COSTUME_TYPE_WEAPON,
			localeInfo.SEARCH_OBJECT_MOUNT : item.COSTUME_TYPE_MOUNT,
			localeInfo.SEARCH_OBJECT_PET : item.COSTUME_TYPE_PET,
			localeInfo.SEARCH_OBJECT_COSTUMEACC : item.COSTUME_TYPE_CROWN,
		}
	},

	# localeInfo.SEARCH_SHOP_ITEM_SHINING : 
    # {
		# "typeID" : 35,
		# "subtypes" : 
        # {
			# localeInfo.SEARCH_SHOP_ITEM_SHINING_WEAPON : item.SHINING_WEAPON,
			# localeInfo.SEARCH_SHOP_ITEM_SHINING_ARMOR : item.SHINING_ARMOR,
			# localeInfo.SEARCH_SHOP_ITEM_SHINING_SPECIAL : item.SHINING_SPECIAL,
			# localeInfo.SEARCH_SHOP_ITEM_SHINING_WING : item.SHINING_WING,
		# }
	# },

}

for sk in SKILL_DICT.iteritems():
	ITEM_DICT.update({"%s %s" % (sk[0], localeInfo.TOOLTIP_SKILLBOOK_NAME) : [50300, sk[1]]})
	ITEM_DICT.update({"%s %s" % (sk[0], localeInfo.TOOLTIP_SKILL_FORGET_BOOK_NAME) : [70037, sk[1]]})

class SearchShopWindow(ui.ScriptWindow):
	def __init__(self):
		ui.ScriptWindow.__init__(self)
		self.lastSearchTime = 0
		self.FilterInfo = {
			"Race" : -1,
			"ItemType" : -1,
			"ItemSubType" : -1,
		}
		
	def __del__(self):
		ui.ScriptWindow.__del__(self)
	
	def LoadWindow(self):
		try:
			PythonScriptLoader = ui.PythonScriptLoader()
			PythonScriptLoader.LoadScriptFile(self, "uiscript/searchshop.py")
		except:
			import exception
			exception.Abort("SearchShopWindow.LoadWindow.LoadObject")
	
		try:
			GetObject = self.GetChild
			self.board = self.GetChild("Board")
			self.titleBar = self.GetChild("TitleBar")
			self.inputName = GetObject("InputName")
			self.searchButton = GetObject("SearchButton")
			self.inputPrice = GetObject("InputPrice")
			self.sortButton = GetObject("SortButton")
			self.saveButton = GetObject("SaveButton")
			self.listButton = GetObject("ListButton")
			self.itemsBox = GetObject("ItemsBox")
			self.itemBarList = GetObject("ItemBarList")
			self.scrollBar = GetObject("ScrollBar")
			self.firstPage = GetObject("FirstButton")
			self.prevPage = GetObject("PrevButton")
			self.nextPage = GetObject("NextButton")
			self.lastPage = GetObject("LastButton")
			self.pageText = GetObject("PageText")
		except:
			import exception
			exception.Abort("SearchShopWindow.LoadWindow.BindObject")
		
		self.titleBar.SetCloseEvent(ui.__mem_func__(self.Close))
		
		self.inputName.OnIMEUpdate = ui.__mem_func__(self.__OnNameUpdate)
		self.inputName.OnKillFocus = ui.__mem_func__(self.__HideResults)
		self.inputName.SAFE_SetReturnEvent(self.__SearchItem)
		self.searchButton.SetEvent(ui.__mem_func__(self.__SearchItem))
		self.inputPrice.SAFE_SetReturnEvent(self.__SearchItem)
		self.resultList = ListBoxWithBoard("TOP_MOST")
		self.resultList.SetPickAlways()
		self.resultList.SetParent(self)
		self.resultList.SetPosition(25, 74)
		self.resultList.SetEvent(ui.__mem_func__(self.__OnSelectResult))
		self.sortButton.SetToggleDownEvent(lambda: self.__SortItems(-3))
		self.sortButton.SetToggleUpEvent(lambda: self.__SortItems(-2))
		self.bookmarkWnd = SearchBookmarks(self)
		self.saveButton.SetEvent(ui.__mem_func__(self.__SaveSearch))
		self.listButton.SetEvent(ui.__mem_func__(self.__OpenSavedList))
		self.itemsBox.Hide()
		self.itemBarList.SetItemSize(460, 30)
		self.itemBarList.SetScrollBar(self.scrollBar)
		
		self.Races = ui.ComboBox()
		self.Races.SetParent(self.board)
		self.Races.SetPosition(15, 100)
		self.Races.SetSize(100, 15)
		self.Races.Show()
		self.Races.SetEvent(ui.__mem_func__(self.ClickRace))

		self.ItemType = ui.ComboBox()
		self.ItemType.SetParent(self.board)
		self.ItemType.SetPosition(135, 100)
		self.ItemType.SetSize(100, 15)
		self.ItemType.Show()
		self.ItemType.SetEvent(ui.__mem_func__(self.ClickItemType))

		self.ItemSubType = ui.ComboBox()
		self.ItemSubType.SetParent(self.board)
		self.ItemSubType.SetPosition(255, 100)
		self.ItemSubType.SetSize(100, 15)
		self.ItemSubType.Hide()
		self.ItemSubType.SetEvent(ui.__mem_func__(self.ClickItemSubType))
        
		self.Races.SetOnClickEvent(ui.__mem_func__(self.HideBoxes), [self.ItemType, self.ItemSubType])
		self.ItemType.SetOnClickEvent(ui.__mem_func__(self.HideBoxes), [self.Races, self.ItemSubType])
		self.ItemSubType.SetOnClickEvent(ui.__mem_func__(self.HideBoxes), [self.Races, self.ItemType])
        
		self.Races.SetCurrentItem("-")
		for race, _ in sorted(RACE_DICT.iteritems(), key=lambda item: item[1]):
			self.Races.InsertItem(_, race)
		
		self.ItemType.SetCurrentItem("-")
		for typeName, vals in sorted(ITEM_TYPE_DICT.iteritems(), key=lambda item: item[1]["typeID"]):
			self.ItemType.InsertItem(vals["typeID"], typeName)
		
		self.firstPage.SetEvent(lambda: self.RefreshItems(0))
		self.prevPage.SetEvent(lambda: self.RefreshItems(1))
		self.nextPage.SetEvent(lambda: self.RefreshItems(2))
		self.lastPage.SetEvent(lambda: self.RefreshItems(3))
		self.__SetPageButtons(False)
		
		self.currentPage = 0
		self.searchResults = None
		self.tooltip = None
		self.isDown = False
	
	def ClickItemSubType(self, subtype):
		if subtype == -1:
			self.ItemSubType.SetCurrentItem(localeInfo.SEARCH_SHOP_ALL)
			self.FilterInfo["ItemSubType"] = -1
			return

		for itemType, vals in ITEM_TYPE_DICT.iteritems():
			if vals["typeID"] == self.FilterInfo["ItemType"]:
				for subType, id in sorted(vals["subtypes"].iteritems(), key=lambda item: item[1]):
					if id == subtype:
						self.FilterInfo["ItemSubType"] = subtype
						self.ItemSubType.SetCurrentItem(subType)

	def ClickItemType(self, type):
		for itemType, vals in ITEM_TYPE_DICT.iteritems():
			if vals["typeID"] == type:
				self.ItemType.SetCurrentItem(itemType)
				self.FilterInfo["ItemType"] = type
				if len(vals["subtypes"]):
					self.ItemSubType.ClearItem()
					self.ItemSubType.Show()
					self.ItemSubType.SetCurrentItem("-")
					self.ItemSubType.InsertItem(-1, localeInfo.SEARCH_SHOP_ALL)
					for subType, id in sorted(vals["subtypes"].iteritems(), key=lambda item: item[1]):
						if self.FilterInfo["Race"] in SUB_TYPE_IGNORE and id in SUB_TYPE_IGNORE[self.FilterInfo["Race"]]:#try
							continue

						self.ItemSubType.InsertItem(id, subType)
				else:
					self.ItemSubType.Hide()

	def ClickRace(self, race):
		self.FilterInfo["Race"] = race
		self.Races.SetCurrentItem(RACE_DICT.keys()[RACE_DICT.values().index(race)])
		self.RefreshSubTypes()

     
	def HideBoxes(self, wnds):
		for wnd in wnds:
			wnd.CloseListBox()

	def RefreshSubTypes(self):
		for itemType, vals in ITEM_TYPE_DICT.iteritems():
			if vals["typeID"] == self.FilterInfo["ItemType"]:
				self.ItemType.SetCurrentItem(itemType)
				if len(vals["subtypes"]):
					self.ItemSubType.ClearItem()
					self.ItemSubType.Show()
					self.ItemSubType.SetCurrentItem("-")
					self.ItemSubType.InsertItem(-1, localeInfo.SEARCH_SHOP_ALL)
					for subType, id in sorted(vals["subtypes"].iteritems(), key=lambda item: item[1]):
						if self.FilterInfo["Race"] in SUB_TYPE_IGNORE and id in SUB_TYPE_IGNORE[self.FilterInfo["Race"]]:#try
							continue

						self.ItemSubType.InsertItem(id, subType)
				else:
					self.ItemSubType.Hide()
	def Open(self):
		self.__ClearItems()
		self.__SetSize(0)
		self.__SetPageButtons(False)
		self.Show()
		self.inputName.SetFocus()
		self.inputPrice.SetText("0")
	
	def SetToolTip(self, tooltip):
		self.tooltip = tooltip
		self.tooltip.Hide()
	
	def __OnNameUpdate(self):
		ui.EditLine.OnIMEUpdate(self.inputName)
		
		if len(self.inputName.GetText()) >= 3:
			self.__FindResults()
		else:
			self.resultList.Hide()
	
	def __FindResults(self):
		self.resultList.ClearItem()
		str = self.inputName.GetText().lower()
		
		count = 0
		for item in ITEM_DICT.iteritems():
			if str in item[0].lower():
				self.resultList.InsertItem(item[1], item[0])
				count += 1
				if count == 10:
					break
					
		self.resultList.SetSize(150 + 60, 18 * count)
		self.resultList.SetSize(150 + 60, 18 * count)
		self.resultList.LocateItem()
		self.resultList.Show() if count else self.resultList.Hide()
		
	def __HideResults(self):
		ui.EditLine.OnKillFocus(self.inputName)
		self.resultList.Hide()
		
	def __OnSelectResult(self):
		self.inputName.SetText(self.resultList.GetSelectedItemText())
		self.inputName.SetEndPosition()
		self.resultList.Hide()
		
	def __SearchItem(self):
		if self.lastSearchTime + 5 > app.GetTime():
			chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.SEARCH_SHOP_WAIT)
			return
		
		self.sortButton.SetUp()
		shop.ClearSearchResults()
		self.resultList.Hide()
		
		if self.inputPrice.GetText() == "":
			chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.SEARCH_SHOP_PRICE_MIN)
			return
		
		self.inputName.KillFocus()
		self.lastSearchTime = app.GetTime()
		
		if len(self.inputName.GetText()):
			item = ITEM_DICT.get(self.inputName.GetText(), 0)

			if isinstance(item, list):
				net.SendSearchShopPacket(item[0], int(self.inputPrice.GetText()), item[1], self.FilterInfo["Race"], self.FilterInfo["ItemType"], self.FilterInfo["ItemSubType"])
			else:
				net.SendSearchShopPacket(item, int(self.inputPrice.GetText()), 0, self.FilterInfo["Race"], self.FilterInfo["ItemType"], self.FilterInfo["ItemSubType"])
		else:
			net.SendSearchShopPacket(0, int(self.inputPrice.GetText()), 0, self.FilterInfo["Race"], self.FilterInfo["ItemType"], self.FilterInfo["ItemSubType"])
        
		self.FilterInfo["Race"] = -1 
		self.FilterInfo["ItemType"] = -1
		self.FilterInfo["ItemSubType"] = -1
        
		self.__SetSize(0)
		self.__SetPageButtons(False)
		
	def RefreshItems(self, arg = -1):
		self.__ClearItems()
		if arg == -1:
			self.searchResults = shop.GetSearchResults()
			self.searchResults.sort(key = lambda x: x[3])
		elif arg == -2:
			self.searchResults.sort(key = lambda x: x[3])
		elif arg == -3:
			self.searchResults.sort(key = lambda x: x[3], reverse = True)
		
		mod = len(self.searchResults) / 15.0
		maxPages = int(mod + 1) if mod > int(mod) else mod
		
		if arg == 0 or arg == -1:
			self.currentPage = 0
		elif arg == 1:
			if self.currentPage > 0:
				self.currentPage -= 1
		elif arg == 2:
			if self.currentPage < maxPages - 1:
				self.currentPage += 1
		elif arg == 3:
			self.currentPage = int(maxPages - 1)
		
		for item, x in zip(self.searchResults[15 * self.currentPage:], xrange(15)):
			itemBar = ItemBar(self.itemsBox)
			itemBar.SetItemInfo(item)
			itemBar.SetToolTip(self.tooltip)
			itemBar.SetBarColor(x % 2 == 0)
			
			self.itemBarList.AppendItem(itemBar)
		
		count = len(self.itemBarList.itemList)
		self.__SetSize(min(count, 10))
		self.__SetPageButtons(count > 0)
		self.pageText.SetText(str(self.currentPage + 1))
		
	def __SortItems(self, arg):
		if self.isDown:
			self.RefreshItems(arg)
		elif arg == -2:
			self.sortButton.Down()
		else:
			self.sortButton.SetUp()
	
	def __SaveSearch(self):
		if self.inputName.GetText() in ITEM_DICT and self.inputName.GetText() != "":
			self.bookmarkWnd.Save(self.inputName.GetText())
		else:
			chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.SEARCH_SHOP_WRONG_NAME)
			
	def __OpenSavedList(self):
		self.bookmarkWnd.Open()
	
	def __SetSize(self, count):
		self.SetSize(522 - 2, 30 * count + (170 if count else 150))
		self.board.SetSize(522 - 2, 30 * count + (170 if count else 150))
		self.itemsBox.SetSize(471 + 20 - 3, 30 * count + (11 if count else 0))
		self.scrollBar.SetScrollBarSize(30 * count + 5)
		self.itemsBox.Show() if count else self.itemsBox.Hide()
		self.isDown = count > 0
		if self.isDown:
			self.Races.SetPosition(15, (30 * count) + 120)
			self.ItemSubType.SetPosition(255, (30 * count) + 120)
			self.ItemType.SetPosition(135, (30 * count) + 120)
		else:
			self.Races.SetPosition(15, 100)
			self.ItemSubType.SetPosition(255, 100)
			self.ItemType.SetPosition(135, 100)

	def __ClearItems(self):
		for item in self.itemBarList.itemList:
			item.Destroy()
			item = None
			
		self.itemBarList.RemoveAllItems()
	
	def __SetPageButtons(self, show):
		self.firstPage.Hide() if not show else self.firstPage.Show()
		self.firstPage.SetWindowVerticalAlignBottom()
		self.prevPage.Hide() if not show else self.prevPage.Show()
		self.prevPage.SetWindowVerticalAlignBottom()
		self.nextPage.Hide() if not show else self.nextPage.Show()
		self.nextPage.SetWindowVerticalAlignBottom()
		self.lastPage.Hide() if not show else self.lastPage.Show()
		self.lastPage.SetWindowVerticalAlignBottom()
		self.pageText.Hide() if not show else self.pageText.Show()
		self.pageText.SetWindowVerticalAlignBottom()
		
	def OnPressEscapeKey(self):
		self.Close()
		return True
	
	def OnMouseWheel(self, len):
		if len >= 0:
			self.scrollBar.OnUp()
		else:
			self.scrollBar.OnDown()
		return True
	
	def OnMoveWindow(self, x, y):
		self.bookmarkWnd.SetPosition(x + 520, y)
		self.bookmarkWnd.SetTop()
		
	def Close(self):
		self.inputName.KillFocus()
		self.inputPrice.KillFocus()
		self.bookmarkWnd.Hide()
		self.Hide()
	
	def Destroy(self):
		self.ClearDictionary()
		self.board = None
		self.itemsBox = None
		self.inputName = None
		self.searchButton = None
		self.inputPrice = None
		self.sortButton = None
		self.bookmarkWnd.Destroy()
		self.bookmarkWnd = None
		self.saveButton = None
		self.listButton = None
		self.resultList = None
		self.__ClearItems()
		self.tooltip = None
		self.itemBarList = None
		self.scrollBar = None
		self.firstPage = None
		self.prevPage = None
		self.nextPage = None
		self.lastPage = None
		self.pageText = None

class ListBoxWithBoard(ui.ListBox):
	def __init__(self, layer):
		ui.ListBox.__init__(self, layer)
		self.BACKGROUND_COLOR = grp.GenerateColor(0.0, 0.0, 0.0, 1.0)
		self.DARK_COLOR = grp.GenerateColor(0.2, 0.2, 0.2, 1.0)
		
	def __del__(self):
		ui.ListBox.__del__(self)
		
	def OnRender(self):
		xRender, yRender = self.GetGlobalPosition()
		yRender -= self.TEMPORARY_PLACE
		widthRender = self.width
		heightRender = self.height + self.TEMPORARY_PLACE
		grp.SetColor(self.BACKGROUND_COLOR)
		grp.RenderBar(xRender, yRender, widthRender, heightRender)
		grp.SetColor(self.DARK_COLOR)
		grp.RenderLine(xRender, yRender, widthRender, 0)
		grp.RenderLine(xRender, yRender, 0, heightRender)
		grp.RenderLine(xRender, yRender+heightRender, widthRender, 0)
		grp.RenderLine(xRender+widthRender, yRender, 0, heightRender)

		ui.ListBox.OnRender(self)

COLORS_DICT = {
	0 : [ 0x4c616161, 0xb2616161 ], # odd
	1 : [ 0x4ce2e2e2, 0x99e2e2e2 ], # even
	2 : [ 0x7f9f6f6f, 0xb29f6f6f ], # sold
}

class ItemBar(ui.Bar):
	def __init__(self, parent):
		ui.Bar.__init__(self)

		self.SetParent(parent)
		self.SetColor(COLORS_DICT[1][0])
		self.SetSize(460, 30)
		self.__Build()

		self.item = None
		self.isEven = True
		
	def __del__(self):
		ui.Bar.__del__(self)

	def __Build(self):
		self.itemName = ui.TextLine()
		self.itemName.SetParent(self)
		self.itemName.SetPosition(5, 9)
		self.itemName.Show()

		self.itemOwner = ui.MakeTextLine(self)
		self.itemOwner.SetPosition(11, 0)

		self.mailbox = ui.MakeButton(self, 0, 0, "", "d:/ymir work/ui/shop/search/", "mailbox.tga", "mailbox_hov.tga", "mailbox_hov.tga")
		self.mailbox.SetEvent(lambda: player.OpenPrivateMessage(self.itemOwner.GetText()))

		self.itemPrice = ui.MakeTextLine(self)
		self.itemPrice.SetWindowHorizontalAlignRight()
		self.itemPrice.SetHorizontalAlignRight()
		self.itemPrice.SetPosition(4, 0)

		self.tooltip = None

		self.buyQuestionDlg = uiCommon.QuestionDialog()
		self.buyQuestionDlg.SetText(uiScriptLocale.SEARCH_SHOP_BUY_CONFIGM)
		self.buyQuestionDlg.SetAcceptEvent(lambda: self.__BuyItem(True))
		self.buyQuestionDlg.SetCancelEvent(lambda: self.__BuyItem(False))
		
	def SetToolTip(self, tooltip):
		self.tooltip = tooltip
		self.tooltip.Hide()
	
	def SetItemInfo(self, Item):
		self.item = Item

		self.__SetItemName(Item[2], Item[6][0], Item[4])

		self.itemOwner.SetText(Item[1])
		w, h = self.itemOwner.GetTextSize()
		x, y = self.itemOwner.GetGlobalPosition()
		self.mailbox.SetPosition(x - 20 - w / 2, 10)
		self.itemPrice.SetText(localeInfo.NumberToMoneyString(Item[3]))
		self.Show()

	def __SetItemName(self, vnum, index, count):
		skillName = ""
		itemName = ""
		
		if vnum == 50300 or vnum == 70037:
			skillName = skill.GetSkillName(index) + " "
			itemName = localeInfo.TOOLTIP_SKILLBOOK_NAME if vnum == 50300 else localeInfo.TOOLTIP_SKILL_FORGET_BOOK_NAME
		else:
			item.SelectItem(vnum)
			itemName = item.GetItemName()
			
		name = skillName + itemName
		if len(name) > 23:
			name = name[:20] + "..."
		self.itemName.SetText(("%dx " % count) + name)

	def __BuyItem(self, buy):
		self.buyQuestionDlg.Hide()

		if buy:
			net.SendSearchShopBuyPacket(self.item[0], self.item[9], self.item[3], self.item[5])
			self.item[8] = 1
			self.SetColor(COLORS_DICT[2][0])

	def SetBarColor(self, isEven):
		if self.item[8]:
			self.SetColor(COLORS_DICT[2][0])
		else:
			self.isEven = isEven
			self.SetColor(COLORS_DICT[isEven][0])

	def OnMouseOverIn(self):
		if self.item[8]:
			self.SetColor(COLORS_DICT[2][1])
		else:
			# self.SetColor(COLORS_DICT[self.isEven][1])
			self.SetColor(COLORS_DICT[1][1])
		if not self.tooltip.IsShow():
			self.tooltip.ClearToolTip()
			self.tooltip.AddItemData(self.item[2], self.item[6], self.item[7])
			self.tooltip.Show()

	def OnMouseOverOut(self):
		if self.item[8]:
			self.SetColor(COLORS_DICT[2][0])
		else:
			self.SetColor(COLORS_DICT[self.isEven][0])
		self.tooltip.Hide()

	def OnMouseLeftButtonUp(self):
		self.buyQuestionDlg.Show()
		self.buyQuestionDlg.SetTop()

	def OnMouseRightButtonUp(self):
		net.SendSearchShopTargetPacket(self.item[0])

	def Destroy(self):
		self.itemName = None
		self.itemOwner = None
		self.itemPrice = None
		self.tooltip = None
		self.buyQuestionDlg = None
		self.mailbox = None

class Bookmark(ui.Bar):
	def __init__(self, parent, x, y, name, index):
		ui.Bar.__init__(self)
		self.SetParent(parent)
		self.parent = parent
		self.__Build(x, y, name, index)
		
	def __del__(self):
		ui.Bar.__del__(self)
	
	def __Build(self, x, y, name, index):
		self.SetSize(210, 20)
		self.SetPosition(x, y)
		self.SetColor(COLORS_DICT[index % 2 == 0][0])
		
		self.text = ui.TextLine()
		self.text.SetParent(self)
		self.text.SetText(name)
		self.text.SetPosition(5, 3)
		self.text.Show()
		
		self.removeBtn = ui.MakeButton(self, 192, 3, "", "d:/ymir work/ui/shop/search/", "delete.tga", "delete.tga", "delete.tga")
		self.removeBtn.SetEvent(lambda: self.text.SetText(uiScriptLocale.SEARCH_SHOP_BOOKMARK_EMPTY))
		self.removeBtn.Show()
		
		self.Show()

	def OnMouseLeftButtonUp(self):
		if self.text.GetText() != uiScriptLocale.SEARCH_SHOP_BOOKMARK_EMPTY:
			self.parent.mainWnd.inputName.SetText(self.text.GetText())
			self.parent.mainWnd.inputName.SetEndPosition()
		
	def Destroy(self):
		self.text = None
		self.removeBtn = None
	
class SearchBookmarks(ui.ScriptWindow):
	def __init__(self, wnd):
		ui.ScriptWindow.__init__(self)
		self.mainWnd = wnd
		self.__Build()
		
	def __del__(self):
		ui.ScriptWindow.__del__(self)
		
	def __Build(self):
		try:
			PythonScriptLoader = ui.PythonScriptLoader()
			PythonScriptLoader.LoadScriptFile(self, "uiscript/searchbookmarks.py")
		except:
			import exception
			exception.Abort("SearchBookmarks.LoadWindow.LoadObject")
		
		try:
			GetObject = self.GetChild
			self.titleBar = self.GetChild("TitleBar")
		except:
			import exception
			exception.Abort("SearchBookmarks.LoadWindow.BindObject")
		
		self.titleBar.SetCloseEvent(ui.__mem_func__(self.Close))
		
		self.bookmarks = []
		
		for x in xrange(10):
			bookmark = Bookmark(self, 10, 21 * x + 31, uiScriptLocale.SEARCH_SHOP_BOOKMARK_EMPTY, x)
			self.bookmarks.append(bookmark)
		
		self.__SetBookmarks()
		
	def Open(self):
		self.Show()
	
	def __SetBookmarks(self):
		file = "shop/bookmark_list.txt"

		import os
		if not os.path.exists(os.path.dirname(file)):
			os.makedirs(os.path.dirname(file))

		try:
			f = old_open(file, "r")
		except IOError:
			f = old_open(file, "w+")

		lines = [line.rstrip('\n') for line in f]
		
		f.close()
		
		for line, bookmark in zip(lines, self.bookmarks):
			if bookmark.text.GetText() == uiScriptLocale.SEARCH_SHOP_BOOKMARK_EMPTY:
				bookmark.text.SetText(line)
		
	def Save(self, itemName):
		empty = False
		for bookmark in self.bookmarks:
			if bookmark.text.GetText() == uiScriptLocale.SEARCH_SHOP_BOOKMARK_EMPTY:
				bookmark.text.SetText(itemName)
				empty = True
				break
		
		if not empty:
			chat.AppendChat(chat.CHAT_TYPE_INFO, uiScriptLocale.SEARCH_SHOP_BOOKMARK_FULL)
		
	def __WriteBookmarks(self):
		file = "shop/bookmark_list.txt"
		f = old_open(file, "w")
		
		for bookmark in self.bookmarks:
			f.write("%s\n" % bookmark.text.GetText())
		
		f.close()
		
	def Close(self):
		self.Hide()
		
	def Destroy(self):
		self.ClearDictionary()
		self.__WriteBookmarks()
		self.titleBar = None
		for bookmark in self.bookmarks:
			bookmark.Destroy()
			bookmark = None
		self.bookmarks = None
		