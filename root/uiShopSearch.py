import ui
import localeInfo
import item
import grp
import shopsearch
import net
import uiToolTip
import uiCommon
import player
import app
import constInfo
import cfg
import time
import chat

ROOT_PATH = "d:/ymir work/ui/game/shopsearchmgr/"

#######################################################
## CATEGORY_PROTO STRUCTURE:
## [ <-- proto list start
##   { <-- category start
##	 "icon" : <icon_path_name>,
##	 "name" : <display_name>,
##	 "itemvnum" : 139 OR (129, 139, 149) OR (129, "130~139", 149), <-- accepts the specific vnum 139 OR the vnums 129, 139, 149 OR the vnums 129, 130, 131, 132, ..., 139, 149 as well as the item types (optional)
########################## ITEM_TYPE:
############# OPTION 1:
##	 "itemtype" : item.ITEM_TYPE_WEAPON, <-- accepts all items with item type = weapon
############# OPTION 2:
##	 "itemtype" : (item.ITEM_TYPE_WEAPON, item.WEAPON_ARROW, item.WEAPON_FAN), <-- accepts all items with item type = weapon and sub type = arrow or fan (add as many subtypes as you want)
############# OPTION 3:
##	 "itemtype" : [
##	   (item.ITEM_TYPE_WEAPON, item.WEAPON_SWORD, item.WEAPON_TWO_HANDED), <-- accepts all items with item type = weapon and sub type = sword or two handed
##	   item.ITEM_TYPE_ARMOR, <-- AND accepts all items with item type = armor
##	   <-- you could add any more item types to be accepted by this category
##	 ],
########################## END OF ITEM_TYPE
##   }, <-- category end
## ]  <-- proto list end
#######################################################

CATEGORY_PROTO = [
	### e.g sub-category
	# {
		# "icon" : "all",
		# "name" : localeInfo.SHOP_SEARCH_CAT_ALL,
		# "itemtype" : item.ITEM_TYPE_WEAPON,
		# "sub_category" : [
			# {
				# "name" : localeInfo.SHOP_SEARCH_CAT_ALL,
				# "itemtype" : (item.ITEM_TYPE_WEAPON, item.WEAPON_SWORD),
			# },
			# {
				# "name" : localeInfo.SHOP_SEARCH_CAT_ALL,
				# "itemtype" : (item.ITEM_TYPE_WEAPON, item.WEAPON_TWO_HANDED),
			# },
			# {
				# "name" : localeInfo.SHOP_SEARCH_CAT_ALL,
				# "itemtype" : (item.ITEM_TYPE_WEAPON, item.WEAPON_DAGGER),
			# },
			# {
				# "name" : localeInfo.SHOP_SEARCH_CAT_ALL,
				# "itemtype" : (item.ITEM_TYPE_WEAPON, item.WEAPON_BOW),
			# },
		# ],
	# },

	{
		"icon" : "all",
		"name" : localeInfo.SHOP_SEARCH_CAT_ALL,
		"itemtype" : range(item.ITEM_TYPE_MAX_NUM),
	},
	{
		"icon" : "weapons",
		"name" : localeInfo.CATEGORY_EQUIPMENT_WEAPON,
		"itemtype" : item.ITEM_TYPE_WEAPON,
	},
	{
		"icon" : "armors",
		"name" : localeInfo.CATEGORY_ARMOR_ARMOR_BODY,
		"itemtype" : (item.ITEM_TYPE_ARMOR, item.ARMOR_BODY),
	},
	{
		"icon" : "jewelry",
		"name" : localeInfo.CATEGORY_EQUIPMENT_JEWELRY,
		"itemtype" : (item.ITEM_TYPE_ARMOR, item.ARMOR_SHIELD, item.ARMOR_EAR, item.ARMOR_NECK, item.ARMOR_WRIST, item.ARMOR_FOOTS, item.ARMOR_HEAD),
	},
	{
		"icon" : "talismans",
		"name" : localeInfo.CATEGORY_JEWELRY_ARMOR_PENDANT,
		"itemtype" : range(item.ITEM_TYPE_MAX_NUM),
	},
	{
		"icon" : "alchemy",
		"name" : localeInfo.CATEGORY_DRAGON_STONE,
		"itemtype" : range(item.ITEM_TYPE_MAX_NUM),
	},
	{
		"icon" : "costumes",
		"name" : localeInfo.CATEGORY_COSTUMES_COSTUME_BODY,
		"itemtype" : (item.ITEM_TYPE_COSTUME, item.COSTUME_TYPE_BODY, item.COSTUME_TYPE_HAIR),
	},
	{
		"icon" : "acce",
		"name" : localeInfo.CATEGORY_COSTUMES_SASH,
		"itemtype" : range(item.ITEM_TYPE_MAX_NUM),
	},
	{
		"icon" : "weapons",
		"name" : localeInfo.CATEGORY_COSTUMES_COSTUME_WEAPON,
		"itemtype" : (item.ITEM_TYPE_COSTUME, item.COSTUME_TYPE_WEAPON),
	},
	{
		"icon" : "aura",
		"name" : "Aura Outfit",
		"itemtype" : range(item.ITEM_TYPE_MAX_NUM),
	},
	{
		"icon" : "skills",
		"name" : localeInfo.CATEGORY_SKILL,
		"itemtype" : range(item.ITEM_TYPE_MAX_NUM),
	},
	{
		"icon" : "potions",
		"name" : localeInfo.CATEGORY_POTION,
		"itemtype" : range(item.ITEM_TYPE_MAX_NUM),
	},
	{
		"icon" : "fish",
		"name" : localeInfo.CATEGORY_FISHING_PICK,
		"itemtype" : range(item.ITEM_TYPE_MAX_NUM),
	},
	{
		"icon" : "belts",
		"name" : localeInfo.CATEGORY_JEWELRY_ITEM_BELT,
		"itemtype" : item.ITEM_TYPE_BELT,
	},
	{
		"icon" : "pets",
		"name" : localeInfo.CATEGORY_MOUNT_PET_CHARGED_PET,
		"itemtype" : range(item.ITEM_TYPE_MAX_NUM),
	},
	{
		"icon" : "mounts",
		"name" : localeInfo.CATEGORY_MOUNT_PET_MOUNT,
		"itemtype" : range(item.ITEM_TYPE_MAX_NUM),
	},
	{
		"icon" : "ores",
		"name" : localeInfo.CATEGORY_FISHING_PICK_STONE,
		"itemtype" : range(item.ITEM_TYPE_MAX_NUM),
	},
	{
		"icon" : "stones",
		"name" : localeInfo.CATEGORY_TUNING_STONE,
		"itemtype" : range(item.ITEM_TYPE_MAX_NUM),
	},
	{
		"icon" : "rings",
		"name" : "Rings",
		"itemtype" : range(item.ITEM_TYPE_MAX_NUM),
	},
	{
		"icon" : "chests",
		"name" : localeInfo.CATEGORY_ETC_GIFTBOX,
		"itemtype" : range(item.ITEM_TYPE_MAX_NUM),
	},
]

class ShopSearchWindow(ui.ScriptWindow):

	CAT_NAME_COLOR_NORMAL = ui.GenerateColor(218, 218, 218)
	CAT_NAME_COLOR_FOCUSED = ui.GenerateColor(255, 199, 0)

	PRICE_COLOR_BY_LEVEL = {
		shopsearch.AVG_PRICE_GOOD : ui.GenerateColor(134, 206, 140),
		shopsearch.AVG_PRICE_NORMAL : ui.GenerateColor(255, 255, 255),
		shopsearch.AVG_PRICE_BAD : ui.GenerateColor(255, 199, 0),
		shopsearch.AVG_PRICE_WORST : ui.GenerateColor(232, 80, 16),
	}

	ENTRYCOUNT_BUTTON_COUNT = 3
	PAGE_BUTTON_COUNT = 5

	STATE_NONE = 0
	STATE_LOADING = 1
	STATE_RESULT = 2

	BUY_RESULT_LOCALE = {
		shopsearch.BUY_SUCCESS : localeInfo.SHOP_SEARCH_BUY_SUCCESS,
		shopsearch.BUY_NOT_EXIST : localeInfo.SHOP_SEARCH_BUY_NOT_EXIST,
		shopsearch.BUY_PRICE_CHANGE : localeInfo.SHOP_SEARCH_BUY_PRICE_CHANGE,
		shopsearch.BUY_TIMEOUT : localeInfo.SHOP_SEARCH_BUY_TIMEOUT,
		shopsearch.BUY_NO_PEER : localeInfo.SHOP_SEARCH_BUY_NO_PEER,
		shopsearch.BUY_UNKNOWN_ERROR : localeInfo.SHOP_SEARCH_BUY_UNKNOWN,
	}

	SORT_BUTTON_BASE_PATH = ROOT_PATH + "sort_button_%s%%s.tga"

	GRAPH_X_DESC_WEEKLY_MAX_NUM = 7
	GRAPH_X_DESC_MONTHLY_MAX_NUM = 15
	GRAPH_COUNT_Y_DESC_MAX_NUM = 5
	GRAPH_PRICE_Y_DESC_MAX_NUM = 3

	GRAPH_PRICE_STEP = 10000
	GRAPH_COUNT_STEP = 5

	class SubCategory(ui.ListBoxEx.Item):
		FOCUSED_BG_COLOR = grp.GenerateColor(1.0, 1.0, 1.0, 0.05)

		def __init__(self, data):
			ui.ListBoxEx.Item.__init__(self)
			self.data = data
			self.SetSelectedRenderColor(self.FOCUSED_BG_COLOR)
			self.__BuildObjects()

		def Destroy(self):
			self.data = None
			self.Hide()

		def __BuildObjects(self):
			name = ui.TextLine()
			name.SetParent(self)
			name.SetPosition(0, 0)
			name.SetWindowVerticalAlignCenter()
			name.SetVerticalAlignCenter()
			name.SetText(self.data["name"])
			name.Show()
			self.name = name

		def GetData(self):
			return self.data

		def OnSelect(self):
			self.name.SetPackedFontColor(ShopSearchWindow.CAT_NAME_COLOR_FOCUSED)

		def OnUnselect(self):
			self.name.SetPackedFontColor(ShopSearchWindow.CAT_NAME_COLOR_NORMAL)

	class Category(ui.ListBoxEx.Item):
		def __init__(self, data):
			ui.ListBoxEx.Item.__init__(self)
			self.eventFoldIn = lambda: None
			self.eventFoldOut = lambda: None
			self.isFoldOut = False
			self.data = data
			self.__BuildObjects()
			self.__BuildSubCategories()
			self.__RefreshState()

		def Destroy(self):
			self.subCategories = None
			self.data = None
			self.eventFoldIn = None
			self.eventFoldOut = None
			self.Hide()

		def __BuildObjects(self):
			mainBtn = ui.ToggleButton()
			mainBtn.SetParent(self)
			mainBtn.SetUpVisual(ROOT_PATH + "cat_btn_up.tga")
			mainBtn.SetOverVisual(ROOT_PATH + "cat_btn_over.tga")
			mainBtn.SetDownVisual(ROOT_PATH + "cat_btn_down.tga")
			mainBtn.SetToggleUpEvent(self.__OnFoldTrigger)
			mainBtn.SetToggleDownEvent(self.__OnFoldTrigger)
			mainBtn.SetPosition(15-4, 12)
			mainBtn.Show()
			self.mainBtn = mainBtn
			self.SetSize(mainBtn.GetWidth(), mainBtn.GetHeight())

			icon = ui.ImageBox()
			icon.SetParent(mainBtn)
			icon.AddFlag("not_pick")
			icon.LoadImage(ROOT_PATH + "cat_icon/" + self.data["icon"] + ".tga")
			icon.SetPosition(6, 0)
			icon.SetWindowVerticalAlignCenter()
			icon.Show()
			self.icon = icon

			name = ui.TextLine()
			name.SetParent(mainBtn)
			name.SetPosition(40, 0)
			name.SetWindowVerticalAlignCenter()
			name.SetVerticalAlignCenter()
			name.SetText(self.data["name"])
			name.Show()
			self.name = name

			if self.data.has_key("sub_category"):
				arrow = ui.ImageBox()
				arrow.SetParent(mainBtn)
				arrow.AddFlag("not_pick")
				arrow.SetPosition(self.GetWidth() - 14, 1)
				arrow.SetWindowVerticalAlignCenter()
				arrow.Show()
				self.arrow = arrow
			else:
				self.arrow = None

		def __BuildSubCategories(self):
			subCategories = []
			if self.data.has_key("sub_category"):
				for cat in self.data["sub_category"]:
					subCategory = ShopSearchWindow.SubCategory(cat)
					subCategory.Hide()
					subCategories.append(subCategory)
			self.subCategories = subCategories

		def __RefreshState(self):
			self.__RefreshArrow()
			self.__RefreshText()

		def __RefreshText(self):
			if self.mainBtn.IsDown():
				self.name.SetPackedFontColor(ShopSearchWindow.CAT_NAME_COLOR_FOCUSED)
			else:
				self.name.SetPackedFontColor(ShopSearchWindow.CAT_NAME_COLOR_NORMAL)

		def __RefreshArrow(self):
			if not self.arrow:
				return

			if self.isFoldOut:
				self.arrow.LoadImage(ROOT_PATH + "cat_arrow_up.tga")
			else:
				self.arrow.LoadImage(ROOT_PATH + "cat_arrow_down.tga")

		def __OnFoldTrigger(self):
			self.isFoldOut = not self.isFoldOut
			self.OnMouseLeftButtonDown()

			if self.isFoldOut:
				self.eventFoldOut()
			else:
				self.eventFoldIn()
			self.mainBtn.Down()
			self.__RefreshState()

		def SetUp(self):
			self.isFoldOut = False
			self.mainBtn.SetUp()
			self.__RefreshState()

		def Down(self):
			self.isFoldOut = True
			self.mainBtn.Down()
			self.__RefreshState()

		def GetData(self):
			return self.data

		def IsFoldOut(self):
			return self.isFoldOut

		def GetSubCategories(self):
			return self.subCategories

		def HideSubCategories(self):
			for subCat in self.subCategories:
				subCat.Hide()

		def SetFoldInEvent(self, eventFoldIn):
			self.eventFoldIn = eventFoldIn

		def SetFoldOutEvent(self, eventFoldOut):
			self.eventFoldOut = eventFoldOut

		def OnRender(self):
			pass

	class ItemDropDownMenu(ui.ImageBox):
		SHOW_SPACE_Y = 5
		START_Y = 4
		START_X = 5
		SPACE_Y = 4
		ELEM_WIDTH = 118
		ELEM_HEIGHT = 14

		def __init__(self):
			ui.ImageBox.__init__(self)
			self.AddFlag("float")
			self.LoadImage(ROOT_PATH + "drop_down_menu.tga")
			self.childs = []
			yPos = self.START_Y
			for data in self.__GetContent():
				textLine = ui.SelectableTextLine(False)
				textLine.SetParent(self)
				textLine.SetSize(self.ELEM_WIDTH, self.ELEM_HEIGHT)
				textLine.SetPosition(self.START_X, yPos)
				textLine.SetText(data[0])
				textLine.SetEvent(data[1])
				textLine.Show()
				self.childs.append(textLine)
				yPos += self.ELEM_HEIGHT + self.SPACE_Y

			self.currentItemIndex = -1
			self.parent = None
			self.eventShowAveragePrice = None
			self.eventAddFavourite = None

		def Destroy(self):
			ui.ImageBox.Destroy(self)
			self.parent = None
			self.eventShowAveragePrice = None
			self.eventAddFavourite = None

		def __GetContent(self):
			return [
				(localeInfo.SHOP_SEARCH_DROPDOWN_ADD_FAVOURITE, self.__AddFavourite),
				(localeInfo.SHOP_SEARCH_DROPDOWN_AVERAGE_PRICE, self.__ShowAveragePrice),
			]

		def SetParent(self, parent):
			ui.ImageBox.SetParent(self, parent)
			self.parent = parent

		def Open(self, parentObj, itemIndex):
			if self.currentItemIndex == itemIndex:
				self.Close()
				return

			self.currentItemIndex = itemIndex
			(parent_x, parent_y) = parentObj.GetLocalPosition(self.parent)
			self.SetPosition(parent_x + parentObj.GetWidth() - self.GetWidth(), parent_y + parentObj.GetHeight() + self.SHOW_SPACE_Y)
			self.Show()
			self.SetTop()

		def Close(self):
			self.currentItemIndex = -1
			self.Hide()

		def SetAveragePriceEvent(self, event):
			self.eventShowAveragePrice = event

		def SetFavouriteEvent(self, event):
			self.eventAddFavourite = event

		def __AddFavourite(self):
			if self.eventAddFavourite:
				self.eventAddFavourite(self.currentItemIndex)
			self.Close()

		def __ShowAveragePrice(self):
			if self.eventShowAveragePrice:
				self.eventShowAveragePrice(self.currentItemIndex)

			self.Close()

	class ItemObject(ui.PixelScrollListBox.Item):
		def __init__(self, index, dropDownMenu, itemToolTip, buyQuestionDlg, buyErrorDlg):
			ui.PixelScrollListBox.Item.__init__(self, 0)

			self.itemIndex = index
			self.itemPriceColor = ShopSearchWindow.PRICE_COLOR_BY_LEVEL[1]
			self.endTime = shopsearch.GetResultItemEndTime(index)
			self.lastLeftSec = -1
			self.dropDownMenu = dropDownMenu
			self.itemToolTip = itemToolTip

			itemVnum = shopsearch.GetResultItemVnum(index)
			item.SelectItem(itemVnum)
			_, itemSize = item.GetItemSize()

			bgImage = self._AddElement(ui.Button())
			bgImage.SetRMBMode()
			bgImage.SetUpVisual(ROOT_PATH + "content_bg_%d_up.png" % itemSize)
			bgImage.SetOverVisual(ROOT_PATH + "content_bg_%d_over.png" % itemSize)
			bgImage.SetDownVisual(ROOT_PATH + "content_bg_%d_up.png" % itemSize)
			bgImage.SetTooltipEvent(lambda: None, itemToolTip.HideToolTip)
			bgImage.SetEvent(lambda dlg=buyQuestionDlg, errDlg=buyErrorDlg: self.AskBuyItem(dlg, errDlg))
			self.SetSize(bgImage.GetWidth(), bgImage.GetHeight())

			itemIcon = self._AddElement(ui.ExpandedImageBox(), True)
			itemIcon.AddFlag("not_pick")
			itemIcon.SetPosition(24, 0)
			itemIcon.LoadImage(item.GetIconImageFileName())
			self.itemIcon = itemIcon

			itemName = self._AddElement(ui.ExtendedTextLine(), True)
			itemName.AddFlag("not_pick")
			itemName.SetPosition(76, 0)
			itemName.SetText("%dx <TEXT color=%d text=\"%s\">" % (shopsearch.GetResultItemCount(index), self.__GetItemNameColor(), self.__GetItemNameString()))

			timeText = self._AddElement(ui.TextLine())
			timeText.SetPosition(40, 0)
			timeText.SetWindowHorizontalAlignCenter()
			timeText.SetHorizontalAlignCenter()
			timeText.SetWindowVerticalAlignCenter()
			timeText.SetVerticalAlignCenter()
			self.timeText = timeText

			if self.endTime == 0:
				timeText.SetText("Online")
			else:
				self.__RefreshTimeText()

			submenuBtn = self._AddElement(ui.Button(), True)
			submenuBtn.SetToolTipText(localeInfo.SHOP_SEARCH_ITEM_SUBMENU_TOOLTIP)
			submenuBtn.SetUpVisual(ROOT_PATH + "content_submenu_button.tga")
			submenuBtn.SetOverVisual(ROOT_PATH + "content_submenu_button.tga")
			submenuBtn.SetDownVisual(ROOT_PATH + "content_submenu_button.tga")
			submenuBtn.SetWindowHorizontalAlignRight()
			submenuBtn.SetPosition(15 + submenuBtn.GetWidth(), 2)
			submenuBtn.SetEvent(self.__OnSubmenuBtnClick)
			self.submenuBtn = submenuBtn

			messageBtn = self._AddElement(ui.Button(), True)
			messageBtn.SetToolTipText(localeInfo.SHOP_SEARCH_ITEM_MESSAGE_OWNER_TOOLTIP)
			messageBtn.SetUpVisual(ROOT_PATH + "message_icon.tga")
			messageBtn.SetOverVisual(ROOT_PATH + "message_icon.tga")
			messageBtn.SetDownVisual(ROOT_PATH + "message_icon.tga")
			messageBtn.SetWindowHorizontalAlignRight()
			messageBtn.SetPosition(submenuBtn.GetLeft() + messageBtn.GetWidth() + 5, 2)
			messageBtn.SetEvent(self.__SendMessage)

			goldIcon = self._AddElement(ui.ExpandedImageBox(), True)
			goldIcon.AddFlag("not_pick")
			goldIcon.LoadImage(ROOT_PATH + "gold_icon.tga")
			goldIcon.SetWindowHorizontalAlignRight()
			goldIcon.SetPosition(messageBtn.GetLeft() + goldIcon.GetWidth() + 1, 1)

			goldText = self._AddElement(ui.TextLine())
			goldText.SetWindowHorizontalAlignRight()
			goldText.SetHorizontalAlignRight()
			goldText.SetWindowVerticalAlignCenter()
			goldText.SetVerticalAlignCenter()
			goldText.SetPosition(goldIcon.GetLeft() + 5, 0)
			goldText.SetText(localeInfo.NumberToString(shopsearch.GetResultItemPrice(index)))
			goldText.SetPackedFontColor(self.itemPriceColor)

		def Destroy(self):
			ui.PixelScrollListBox.Item.Destroy(self)
			self.timeText = None
			self.dropDownMenu = None
			self.itemIcon = None
			self.itemToolTip = None
			self.submenuBtn = None
			self.Hide()

		def __OnSubmenuBtnClick(self):
			self.dropDownMenu.Open(self.submenuBtn, self.itemIndex)

		def __GetItemNameData(self):
			itemVnum = shopsearch.GetResultItemVnum(self.itemIndex)
			itemName = item.GetItemName()
			if len(itemName) > 25:
				itemName = itemName[:25] + "..."

			(title, specialColor) = constInfo.GetItemSpecialColor(itemVnum)
			if title != None and specialColor != None:
				return (title, specialColor)

			titleColor = constInfo.GetItemTitleColor(itemVnum)
			if titleColor != None:
				return (itemName, titleColor)

			for i in xrange(player.ATTRIBUTE_SLOT_MAX_NUM):
				attrType, attrValue = shopsearch.GetResultItemAttribute(self.itemIndex, i)
				if attrType != 0:
					return (itemName, uiToolTip.ToolTip.SPECIAL_TITLE_COLOR)

			return (itemName, uiToolTip.ToolTip.TITLE_COLOR)

		def __GetItemNameString(self):
			return self.__GetItemNameData()[0]

		def __GetItemNameColor(self):
			return self.__GetItemNameData()[1]

		def __RefreshTimeText(self):
			leftSec = max(0, self.endTime - app.GetGlobalTimeStamp())
			if leftSec != self.lastLeftSec:
				self.lastLeftSec = leftSec
				self.timeText.SetText(localeInfo.SecondToDHM(leftSec))

		def OnUpdate(self):
			if self.IsInPosition() and not self.itemToolTip.disabled:
				if self.itemIcon.IsInPosition():
					self.itemToolTip.SetShopSearchItem(self.itemIndex, self.itemPriceColor)
				else:
					self.itemToolTip.HideToolTip()

			if self.endTime > 0:
				self.__RefreshTimeText()

		def AskBuyItem(self, dlg, errDlg):
			itemID = shopsearch.GetResultItemID(self.itemIndex)
			itemVnum = shopsearch.GetResultItemVnum(self.itemIndex)
			itemPrice = shopsearch.GetResultItemPrice(self.itemIndex)

			if player.GetElk() < itemPrice:
				errDlg.SetText(localeInfo.SHOP_SEARCH_CANNOT_BUY_NO_MONEY)
				errDlg.Open()
				return

			item.SelectItem(itemVnum)
			dlg.SetText(localeInfo.SHOP_SEARCH_ITEM_BUY_QUESTION % (item.GetItemName(), localeInfo.NumberToMoneyString(itemPrice)))
			dlg.SetAcceptEvent(lambda argDlg=dlg, argItemID=itemID, argItemVnum=itemVnum, argItemPrice=itemPrice: self.__BuyItem(argDlg, argItemID, argItemVnum, argItemPrice))
			dlg.Open()

			self.dropDownMenu.Close()

		def __BuyItem(self, dlg, itemID, itemVnum, itemPrice):
			net.SendShopSearchBuy(itemID, itemVnum, itemPrice)
			dlg.Close()

			self.dropDownMenu.Close()

		def __SendMessage(self):
			net.SendShopSearchOwnerMessage(shopsearch.GetResultItemOwnerID(self.itemIndex))

	class FavouriteBoard(ui.BoardWithTitleBar):
		X_BORDER = 20
		TOP_BORDER = 40
		BOT_BORDER = 17
		BOARD_WIDTH = 241 + 13
		BOARD_HEIGHT = 400 + 64
		ITEM_X_POS = 3
		ITEM_Y_START = 74
		ITEM_Y_SPACE = 1
		ITEM_MAX_COUNT = 10

		def __init__(self, searchFunc):
			ui.BoardWithTitleBar.__init__(self)
			self.searchFunc = searchFunc
			self.SetSize(self.BOARD_WIDTH, self.BOARD_HEIGHT)
			self.SetCenterPosition()

			self.AddFlag("float")
			self.AddFlag("movable")
			self.SetTitleName(localeInfo.SHOP_SEARCH_FAV_TITLE)
			self.SetCloseEvent(self.Close)

			bg = ui.ImageBox()
			bg.SetParent(self)
			bg.SetPosition(6, 30)
			bg.LoadImage(ROOT_PATH + "fav/fav_bg.tga")
			bg.Show()
			self.bg = bg

			desc = ui.MultiTextLine()
			desc.SetParent(bg)
			desc.SetPosition(5, 5)
			desc.SetWidth(bg.GetWidth() - 5 * 2)
			desc.SetText(localeInfo.SHOP_SEARCH_FAV_DESCRIPTION)
			desc.Show()
			bg.desc = desc

			self.items = []

		def Destroy(self):
			ui.BoardWithTitleBar.Destroy(self)
			self.searchFunc = None

		def __AppendFavElem(self, favName):
			elemIdx = len(self.items)

			elem = ui.ImageBox()
			elem.SetParent(self.bg)
			elem.LoadImage(ROOT_PATH + "fav/fav_item.tga")
			elem.SetPosition(self.ITEM_X_POS, self.ITEM_Y_START + (elem.GetHeight() + self.ITEM_Y_SPACE) * elemIdx)
			elem.Show()
			self.items.append(elem)

			textLine = ui.TextLine()
			textLine.SetParent(elem)
			textLine.SetPosition(10, 0)
			textLine.SetVerticalAlignCenter()
			textLine.SetWindowVerticalAlignCenter()
			textLine.SetText(favName)
			textLine.Show()
			elem.textLine = textLine

			deleteBtn = ui.Button()
			deleteBtn.SetParent(elem)
			deleteBtn.SetUpVisual(ROOT_PATH + "fav/delete_btn.tga")
			deleteBtn.SetOverVisual(ROOT_PATH + "fav/delete_btn_over.tga")
			deleteBtn.SetDownVisual(ROOT_PATH + "fav/delete_btn_down.tga")
			deleteBtn.SetPosition(elem.GetWidth() - 10 - deleteBtn.GetWidth(), (elem.GetHeight() - deleteBtn.GetHeight()) / 2)
			deleteBtn.SetEvent(lambda idx=elemIdx: self.__DeleteFavourite(idx))
			deleteBtn.Show()
			elem.deleteBtn = deleteBtn

			searchBtn = ui.Button()
			searchBtn.SetParent(elem)
			searchBtn.SetUpVisual(ROOT_PATH + "search_btn_up.png")
			searchBtn.SetOverVisual(ROOT_PATH + "search_btn_over.png")
			searchBtn.SetDownVisual(ROOT_PATH + "search_btn_down.png")
			searchBtn.SetPosition(deleteBtn.GetLeft() - 3 - searchBtn.GetWidth(), (elem.GetHeight() - searchBtn.GetHeight()) / 2)
			searchBtn.SetEvent(lambda name=favName: self.searchFunc(name))
			searchBtn.Show()
			elem.searchBtn = searchBtn

		def RefreshFavourites(self):
			self.items = []

			for i in xrange(self.ITEM_MAX_COUNT):
				favName = cfg.Get(cfg.SAVE_SHOPSEARCH, "fav_%d" % i, "")
				if not favName:
					break

				self.__AppendFavElem(favName)

		def __DeleteFavourite(self, index):
			cfg.Set(cfg.SAVE_SHOPSEARCH, "fav_%d" % index, "")
			for i in xrange(index + 1, self.ITEM_MAX_COUNT):
				favName = cfg.Get(cfg.SAVE_SHOPSEARCH, "fav_%d" % i, "")
				cfg.Set(cfg.SAVE_SHOPSEARCH, "fav_%d" % (i - 1), favName)
				cfg.Set(cfg.SAVE_SHOPSEARCH, "fav_%d" % i, "")

			self.RefreshFavourites()

		def Open(self, x, y):
			self.RefreshFavourites()
			self.SetPosition(x, y)
			self.Show()
			self.SetTop()

		def Close(self):
			self.Hide()

		def OnPressEscapeKey(self):
			self.Close()
			return True

	class SearchDropdownList(ui.Window):
		BORDER_SCALE_SIZE = 10
		BASE_SCALE_SIZE = 10
		BASE_TOP_SPACE = 3
		MAX_DISPLAY_ITEMS = 5

		def __init__(self, selectNameEvent):
			ui.Window.__init__(self)
			self.AddFlag("float")

			leftBorder = ui.ExpandedImageBox()
			leftBorder.AddFlag("not_pick")
			leftBorder.SetParent(self)
			leftBorder.LoadImage(ROOT_PATH + "search_dropdown_border_x.tga")
			leftBorder.Show()
			self.leftBorder = leftBorder

			rightBorder = ui.ExpandedImageBox()
			rightBorder.SetParent(self)
			rightBorder.LoadImage(ROOT_PATH + "search_dropdown_border_x.tga")
			rightBorder.SetWindowHorizontalAlignRight()
			rightBorder.SetPosition(rightBorder.GetWidth(), 0)
			rightBorder.Show()
			self.rightBorder = rightBorder

			bottomBorder = ui.ExpandedImageBox()
			bottomBorder.AddFlag("not_pick")
			bottomBorder.SetParent(self)
			bottomBorder.LoadImage(ROOT_PATH + "search_dropdown_border_y.tga")
			bottomBorder.SetWindowVerticalAlignBottom()
			bottomBorder.SetPosition(0, bottomBorder.GetHeight())
			bottomBorder.Show()
			self.bottomBorder = bottomBorder

			base = ui.ExpandedImageBox()
			base.AddFlag("not_pick")
			base.SetParent(self)
			base.LoadImage(ROOT_PATH + "search_dropdown_base.tga")
			base.SetPosition(leftBorder.GetWidth(), self.BASE_TOP_SPACE)
			base.Show()
			self.base = base

			itemList = ui.ListBox()
			itemList.SetParent(self)
			itemList.SetPosition(leftBorder.GetWidth(), self.BASE_TOP_SPACE)
			itemList.SetEvent(lambda key, name: selectNameEvent(name))
			itemList.Show()
			self.itemList = itemList

		def Destroy(self):
			ui.Window.Destroy(self)

			self.itemList = None

		def SetSize(self, width, height):
			ui.Window.SetSize(self, width, height)

			xBorderHeight = height - self.bottomBorder.GetHeight()
			xBorderScale = -1.0 + xBorderHeight / float(self.BORDER_SCALE_SIZE)
			self.leftBorder.SetRenderingRect(0.0, 0.0, 0.0, xBorderScale)
			self.rightBorder.SetRenderingRect(0.0, 0.0, 0.0, xBorderScale)

			yBorderScale = -1.0 + width / float(self.BORDER_SCALE_SIZE)
			self.bottomBorder.SetRenderingRect(0.0, 0.0, yBorderScale, 0.0)
			self.bottomBorder.UpdateRect()

			xBaseScale = -1.0 + (width - self.leftBorder.GetWidth() - self.rightBorder.GetWidth()) / float(self.BASE_SCALE_SIZE)
			yBaseScale = -1.0 + (height - self.BASE_TOP_SPACE - self.bottomBorder.GetHeight()) / float(self.BASE_SCALE_SIZE)
			self.base.SetRenderingRect(0.0, 0.0, xBaseScale, yBaseScale)

			self.itemList.SetSize(width - self.leftBorder.GetWidth() - self.rightBorder.GetWidth(), height - self.BASE_TOP_SPACE - self.bottomBorder.GetHeight() - 2)

		def SetWidth(self, width):
			self.SetSize(width, max(self.GetHeight(), 10))

		def Open(self, itemNames):
			self.SetSize(self.GetWidth(), min(self.MAX_DISPLAY_ITEMS, len(itemNames)) * self.itemList.GetStepSize() + self.BASE_TOP_SPACE + self.bottomBorder.GetHeight() + 2)
			self.itemList.ClearItem()
			i = 0
			for name in itemNames:
				self.itemList.InsertItem(i, name)
				i += 1

				if i >= self.MAX_DISPLAY_ITEMS:
					break

			self.Show()
			self.SetTop()

		def Close(self):
			self.Hide()

		def SelectPrevElement(self):
			curOverLine = self.itemList.GetOverLineIdx()
			if curOverLine <= 0:
				curOverLine = self.itemList.GetItemCount() - 1
			else:
				curOverLine -= 1

			self.itemList.SetOverLineIdx(curOverLine)

		def SelectNextElement(self):
			curOverLine = self.itemList.GetOverLineIdx()
			if curOverLine >= self.itemList.GetItemCount() - 1:
				curOverLine = 0
			else:
				curOverLine += 1

			self.itemList.SetOverLineIdx(curOverLine)

		def SelectCurrentElement(self):
			curOverLine = self.itemList.GetOverLineIdx()
			if curOverLine == -1:
				return False

			self.itemList.SelectItem(curOverLine)
			return True

	def __init__(self):
		ui.ScriptWindow.__init__(self)
		self.__Initialize()
		self.__LoadDialog()
		self.SetCenterPosition()

	def __del__(self):
		ui.ScriptWindow.__del__(self)

	def Destroy(self):
		ui.ScriptWindow.Destroy(self)

		self.Close()

		for cat in self.categories:
			cat.Destroy()
		self.categories = []

		self.main["item_list"].ClearItem()
		self.main = None

		self.dropDownMenu.Destroy()
		self.favBoard.Destroy()
		self.searchDropdown.Destroy()

	def __Initialize(self):
		self.categories = []
		for catData in CATEGORY_PROTO:
			cat = self.Category(catData)
			cat.SetFoldInEvent(self.__RefreshCategories)
			cat.SetFoldOutEvent(lambda arg=cat: self.__OnCategoryFoldOut(arg))
			cat.Hide()

			self.categories.append(cat)

		self.state = self.STATE_NONE
		self.entryCount = -1
		self.page = 0
		self.sortType = shopsearch.SORT_RANDOM
		self.currentGraphItem = 0
		self.currentGraphRefresh = False

		self.lastSelectedCategory = None
		self.lastInputSearch = None
		self.lastSearchFunc = None

	def __LoadDialog(self):
		PythonScriptLoader = ui.PythonScriptLoader()
		PythonScriptLoader.LoadScriptFile(self, "UIScript/shopsearchwindow.py")

		GetObj = self.GetChild
		self.board = GetObj("board")
		self.main = {
			"wnd" : GetObj("main"),
			"cat_list" : GetObj("category_list"),
			"cat_scroll" : GetObj("category_scroll"),
			"fav_btn" : GetObj("fav_button"),
			"sort_btn" : GetObj("sort_button"),
			"search_bg" : GetObj("search_bg"),
			"search" : GetObj("search_line"),
			"search_btn" : GetObj("search_button"),
			"item_list" : GetObj("item_list"),
			"item_scroll" : GetObj("item_scrollbar"),
			"item_loading" : GetObj("loading_image"),
			"no_search_info" : GetObj("item_no_search_info"),
			"no_result_info" : GetObj("item_no_result_info"),
			"entry_count" : [GetObj("entry_count_%d" % (i + 1)) for i in xrange(self.ENTRYCOUNT_BUTTON_COUNT)],
			"page_wnd" : GetObj("item_page_wnd"),
			"page_first" : GetObj("item_first_page_btn"),
			"page_back" : GetObj("item_previous_page_btn"),
			"page_next" : GetObj("item_next_page_btn"),
			"page_last" : GetObj("item_last_page_btn"),
			"page_btn" : [GetObj("item_page_btn%d" % (i + 1)) for i in xrange(self.PAGE_BUTTON_COUNT)],

			"graph" : {
				"wnd" : GetObj("graph"),
				"close" : GetObj("graph_close"),
				"item_name" : GetObj("graph_item_name"),
				"weekly_btn" : GetObj("graph_time_weekly_button"),
				"monthly_btn" : GetObj("graph_time_monthly_button"),
				"refresh_btn" : GetObj("graph_refresh_button"),
				"last_updated" : GetObj("graph_last_updated"),
				"graph_price" : GetObj("graph_average_price"),
				"price_cursor" : GetObj("graph_average_price_cursor"),
				"price_cursor_money" : GetObj("graph_average_price_money"),
				"graph_count" : GetObj("graph_sold_items"),
				"x_desc_weekly" : {
					"wnd" : GetObj("graph_sold_weekly_x_description"),
				},
				"x_desc_monthly" : {
					"wnd" : GetObj("graph_sold_monthly_x_description"),
				},
				"y_desc_price" : [GetObj("graph_price_y_desc_%d" % (i + 1)) for i in xrange(self.GRAPH_PRICE_Y_DESC_MAX_NUM)],
				"y_desc_count" : [GetObj("graph_sold_y_desc_%d" % (i + 1)) for i in xrange(self.GRAPH_COUNT_Y_DESC_MAX_NUM)],
			},
		}

		for i in xrange(self.GRAPH_X_DESC_WEEKLY_MAX_NUM):
			self.main["graph"]["x_desc_weekly"][i] = GetObj("graph_sold_weekly_desc_%d" % i)
		for i in xrange(self.GRAPH_X_DESC_MONTHLY_MAX_NUM):
			self.main["graph"]["x_desc_monthly"][i] = GetObj("graph_sold_monthly_x_desc_%d" % i)

		self.board.SetCloseEvent(self.Close)

		self.main["cat_list"].SetSelectEvent(self.__OnCategoryListSelect)
		self.main["cat_scroll"].SetScrollEvent(self.__OnCategoryScroll)
		self.main["fav_btn"].SetEvent(self.__OnClickFavButton)
		self.main["sort_btn"].SetEvent(self.__OnClickSortButton)
		self.main["search"].SetReturnEvent(self.__OnSearchByNameReturn)
		self.main["search"].SetEscapeEvent(self.OnPressEscapeKey)
		self.main["search"].SetUpdateEvent(self.__OnUpdateSearchSuggestions)
		self.main["search"].SetTabEvent(self.__AutoSearchCompletion)
		self.main["search"].SetKillFocusEvent(self.__OnSearchUnfocusEdit)
		self.main["search"].SetUpArrowEvent(self.__OnSearchUpArrow)
		self.main["search"].SetDownArrowEvent(self.__OnSearchDownArrow)
		self.main["search_btn"].SetEvent(self.__OnSearchByName)
		self.main["item_scroll"].SetScrollEvent(self.__OnResultItemScroll)

		for i in xrange(self.ENTRYCOUNT_BUTTON_COUNT):
			self.main["entry_count"][i].SetEvent(lambda arg=i: self.__OnSelectEntryCount(arg))

		self.main["page_first"].SetEvent(lambda: self.__SelectPage(0))
		self.main["page_back"].SetEvent(lambda: self.__ChangePage(-1))
		self.main["page_next"].SetEvent(lambda: self.__ChangePage(1))
		self.main["page_last"].SetEvent(lambda: self.__OnSelectLastPageBtn(1))

		for i in xrange(self.PAGE_BUTTON_COUNT):
			self.main["page_btn"][i].SetEvent(lambda arg=i: self.__OnSelectPageBtn(arg))

		self.main["graph"]["close"].SetEvent(self.OnPressEscapeKey)
		self.main["graph"]["weekly_btn"].SetEvent(self.__GraphOnSelectWeekly)
		self.main["graph"]["monthly_btn"].SetEvent(self.__GraphOnSelectMonthly)
		self.main["graph"]["refresh_btn"].SetEvent(self.__GraphOnClickRefresh)
		self.main["graph"]["graph_price"].SetOverLineEvent(self.__GraphPriceOnOver)
		self.main["graph"]["graph_price"].SetOutLineEvent(self.__GraphPriceOnOut)
		self.main["graph"]["price_cursor"].Hide()

		searchDropdown = self.SearchDropdownList(self.__StartSearchByNameDropdown)
		searchDropdown.SetParent(self.main["wnd"])
		searchDropdown.SetPosition(self.main["search_bg"].GetLeft(), self.main["search_bg"].GetBottom() - self.SearchDropdownList.BASE_TOP_SPACE)
		searchDropdown.SetWidth(self.main["search_bg"].GetWidth())
		searchDropdown.Close()
		self.searchDropdown = searchDropdown

		dropDownMenu = self.ItemDropDownMenu()
		dropDownMenu.SetParent(self)
		dropDownMenu.SetFavouriteEvent(self.__OnAddToFavourite)
		dropDownMenu.SetAveragePriceEvent(self.__OnRequestAveragePrice)
		dropDownMenu.Close()
		self.dropDownMenu = dropDownMenu

		favBoard = self.FavouriteBoard(self.__StartSearchByName)
		favBoard.Close()
		self.favBoard = favBoard

		itemToolTip = uiToolTip.ItemToolTip()
		itemToolTip.HideToolTip()
		self.itemToolTip = itemToolTip

		buyQuestionDlg = uiCommon.QuestionDialog()
		buyQuestionDlg.SetCancelEvent(buyQuestionDlg.Close)
		buyQuestionDlg.Close()
		self.buyQuestionDlg = buyQuestionDlg

		popupDlg = uiCommon.PopupDialog()
		popupDlg.Close()
		self.popupDlg = popupDlg

		self.__OnSelectEntryCount(0)
		self.__RefreshCategories()
		self.Refresh()

		self.main["graph"]["wnd"].Hide()
		self.__EnableItemTooltip()
		self.__GraphOnSelectWeekly()

	def Open(self):
		self.Show()
		self.SetTop()

	def CloseDialogs(self):
		self.itemToolTip.HideToolTip()
		self.buyQuestionDlg.Close()
		self.dropDownMenu.Close()
		self.favBoard.Close()
		self.searchDropdown.Close()

	def Close(self):
		self.Hide()
		self.main["search"].KillFocus()
		self.CloseDialogs()

	def OnPressEscapeKey(self):
		if self.main["graph"]["wnd"].IsShow():
			self.main["graph"]["wnd"].Hide()
			self.__EnableItemTooltip()
			return True

		if self.main["search"].IsFocus() and self.main["search"].GetText():
			self.main["search"].SetText("")
			return True

		self.Close()
		return True

	def OnRunMouseWheel(self, len):
		if self.main["cat_list"].IsInPosition():
			curBasePos = self.main["cat_list"].GetBasePos()
			maxBasePos = self.main["cat_list"].GetScrollLen()

			pos = min(1, max(0, self.main["cat_scroll"].GetPos() - len * self.main["cat_scroll"].GetPageScale() * 0.002))
			self.main["cat_scroll"].SetPos(pos)

			return True

		elif self.main["item_list"].IsInPosition():
			curBasePos = self.main["item_list"].GetBasePos()
			maxBasePos = self.main["item_list"].GetMaxBasePos()

			pos = min(1, max(0, self.main["item_scroll"].GetPos() - len * self.main["item_scroll"].GetPageScale() * 0.002))
			self.main["item_scroll"].SetPos(pos)

			return True

		return False

	def Refresh(self):
		self.main["item_list"].ClearItem()
		self.main["item_loading"].Hide()
		self.main["item_scroll"].Hide()
		self.main["no_search_info"].Hide()
		self.main["no_result_info"].Hide()
		self.main["page_wnd"].Hide()
		self.CloseDialogs()

		self.__RefreshSortButton()

		if self.state == self.STATE_NONE:
			self.main["no_search_info"].Show()

		elif self.state == self.STATE_LOADING:
			self.main["item_loading"].Show()

		elif self.state == self.STATE_RESULT:
			if shopsearch.GetResultItemMaxNum() > 0:
				self.main["page_wnd"].Show()

			self.__RefreshItems()
			self.__RefreshPageButtons()

	def RefreshResult(self):
		self.state = self.STATE_RESULT
		self.Refresh()

	def ShowBuyResult(self, result):
		if result in self.BUY_RESULT_LOCALE:
			self.popupDlg.SetText(self.BUY_RESULT_LOCALE[result])
		else:
			self.popupDlg.SetText(localeInfo.SHOP_SEARCH_BUY_UNKNOWN)
		self.popupDlg.Open()

	def __DisableItemTooltip(self):
		self.itemToolTip.disabled = True
		self.itemToolTip.HideToolTip()

	def __EnableItemTooltip(self):
		self.itemToolTip.disabled = False

	def __SearchItems(self, func = None):
		if func:
			self.lastSearchFunc = func
		if self.lastSearchFunc:
			self.main["search"].KillFocus()

			self.lastSearchFunc(self.page, self.entryCount, self.sortType)

			self.state = self.STATE_LOADING
			self.Refresh()

			return True

		return False

	def __OnClickFavButton(self):
		if self.favBoard.IsShow():
			self.favBoard.Close()
		else:
			(x, y) = self.GetGlobalPosition()
			self.favBoard.Open(x + self.GetWidth() - 7, y)

	def __OnClickSortButton(self):
		self.sortType += 1
		if self.sortType >= shopsearch.SORT_MAX_NUM:
			self.sortType = 0

		self.__RefreshSortButton()
		self.__SearchItems()

	def __RefreshSortButton(self):
		btn = self.main["sort_btn"]

		imageTypeDict = {
			shopsearch.SORT_RANDOM : "random",
			shopsearch.SORT_ASC : "asc",
			shopsearch.SORT_DESC : "desc",
		}
		tooltipDict = {
			shopsearch.SORT_RANDOM : localeInfo.SHOP_SEARCH_SORT_TOOLTIP_RANDOM,
			shopsearch.SORT_ASC : localeInfo.SHOP_SEARCH_SORT_TOOLTIP_ASC,
			shopsearch.SORT_DESC : localeInfo.SHOP_SEARCH_SORT_TOOLTIP_DESC,
		}
		basePath = self.SORT_BUTTON_BASE_PATH % imageTypeDict[self.sortType]

		btn.SetUpVisual(basePath % "")
		btn.SetOverVisual(basePath % "_over")
		btn.SetDownVisual(basePath % "_down")
		btn.SetToolTipText(tooltipDict[self.sortType])

	def __OnSearchByNameReturn(self):
		if self.searchDropdown.IsShow():
			if self.searchDropdown.SelectCurrentElement():
				return

		self.__OnSearchByName()

	def __OnSearchByName(self):
		name = self.main["search"].GetText()
		self.__StartSearchByName(name)

	def __StartSearchByNameDropdown(self, name):
		self.__StartSearchByName(name)
		self.searchDropdown.Close()

	def __StartSearchByName(self, name):
		if not name or self.lastInputSearch == name:
			return

		self.lastSelectedCategory = None
		self.lastInputSearch = name

		self.main["search"].SetText(name)

		for cat in self.categories:
			cat.SetUp()
		self.__RefreshCategories()

		if name.find("(") >= 0:
			name = name[:name.find("(")]

		self.__SearchItems(lambda page, entryCount, sortType, itemName=name: net.SendShopSearchByName(page, entryCount, sortType, itemName))
		# chat.AppendChat(1, "Not done yet. @func1")
		
	def __OnUpdateSearchSuggestions(self):
		name = self.main["search"].GetText()
		if not name:
			self.main["search"].SetEditOverlayText(localeInfo.SHOP_SEARCH_SEARCH_OVERLAY)
			return

		itemNames = item.GetItemNamesByName(name)
		self.main["search"].SetEditOverlayText(localeInfo.GetBestMatchingName(name, itemNames))

	def __AutoSearchCompletion(self):
		self.main["search"].SetText(self.main["search"].GetEditOverlayText())
		self.main["search"].SetEndPosition()

	def __OnSearchUnfocusEdit(self):
		self.searchDropdown.Close()

	def __OnSearchUpArrow(self):
		if self.searchDropdown.IsShow():
			self.searchDropdown.SelectPrevElement()

	def __OnSearchDownArrow(self):
		if self.searchDropdown.IsShow():
			self.searchDropdown.SelectNextElement()

	def __OnCategoryListSelect(self, catObj):
		data = catObj.GetData()
		if self.lastSelectedCategory == data:
			return

		self.lastSelectedCategory = data
		self.lastInputSearch = None

		itemTypeList = []
		if data.has_key("itemtype"):
			itemTypeList = data["itemtype"]
		vnumTuple = ()
		if data.has_key("itemvnum"):
			vnumTuple = data["itemvnum"]

		self.__SearchItems(lambda page, entryCount, sortType, itemTypes=itemTypeList, vnums=vnumTuple: net.SendShopSearchByOptions(page, entryCount, sortType, itemTypes, vnums))
		# chat.AppendChat(1, "Not done yet. @func2")

	def __OnCategoryScroll(self):
		scrollPos = self.main["cat_scroll"].GetPos()
		basePos = int(scrollPos * self.main["cat_list"].GetScrollLen())
		if basePos != self.main["cat_list"].basePos:
			self.main["cat_list"].SetBasePos(basePos)

	def __OnCategoryFoldOut(self, foldOutCat):
		for cat in self.categories:
			if cat != foldOutCat:
				cat.SetUp()

		self.__RefreshCategories()

	def __RefreshCategories(self):
		catList = self.main["cat_list"]
		catList.RemoveAllItems()

		for cat in self.categories:
			catList.AppendItem(cat)
			if cat.IsFoldOut():
				for subCat in cat.GetSubCategories():
					catList.AppendItem(subCat)
			else:
				cat.HideSubCategories()

		if catList.GetScrollLen() > 0:
			oldScrollPos = self.main["cat_scroll"].GetPos()

			viewItemCount = catList.GetViewItemCount()
			itemCount = catList.GetItemCount()
			self.main["cat_scroll"].SetMiddleBarSize(float(viewItemCount) / itemCount)
			self.main["cat_scroll"].Show()

			self.main["cat_scroll"].SetPos(oldScrollPos)

		else:
			self.main["cat_scroll"].Hide()

	def __RefreshItems(self):
		itemList = self.main["item_list"]
		itemList.ClearItem()

		for i in xrange(shopsearch.GetResultItemMaxNum()):
			curItem = self.ItemObject(i, self.dropDownMenu, self.itemToolTip, self.buyQuestionDlg, self.popupDlg)
			itemList.AppendItem(curItem)

		itemList.LocateItem()

		if itemList.GetMaxBasePos() > 0:
			oldScrollPos = self.main["item_scroll"].GetPos()

			viewItemSize = itemList.GetHeight()
			maxItemSize = itemList.GetMaxHeight()
			self.main["item_scroll"].SetMiddleBarSize(float(viewItemSize) / maxItemSize)
			self.main["item_scroll"].Show()
			self.main["item_scroll"].SetPos(oldScrollPos)

		else:
			self.main["item_scroll"].Hide()

			if shopsearch.GetResultItemMaxNum() == 0:
				self.main["no_result_info"].Show()

	def __OnResultItemScroll(self):
		itemList = self.main["item_list"]
		self.dropDownMenu.Close()

		pos = self.main["item_scroll"].GetPos()
		basePos = int(itemList.GetMaxBasePos() * pos)
		itemList.SetBasePos(basePos)

	def __RefreshPageButtons(self):
		maxPageNum = self.__GetMaxPage()
		if self.page >= maxPageNum:
			self.page = maxPageNum - 1

		for btn in self.main["page_btn"]:
			btn.Hide()

		minBtnIdx = max(0, self.PAGE_BUTTON_COUNT / 2 - maxPageNum / 2)
		maxBtnIdx = min(self.PAGE_BUTTON_COUNT - 1, self.PAGE_BUTTON_COUNT / 2 + (maxPageNum - 1) / 2)

		minPageIdx = self.page
		maxPageIdx = self.page
		for i in xrange(1, (maxBtnIdx + 1) - minBtnIdx):
			if i % 2 == 1:
				if minPageIdx > 0:
					minPageIdx -= 1
				else:
					maxPageIdx += 1
			else:
				if maxPageIdx < maxPageNum-1:
					maxPageIdx += 1
				else:
					minPageIdx -= 1

		for i in xrange(minBtnIdx, maxBtnIdx + 1):
			btn = self.main["page_btn"][i]
			btn.pageIdx = minPageIdx + i - minBtnIdx
			btn.SetText(str(btn.pageIdx + 1))
			if btn.pageIdx == self.page:
				btn.Down()
			else:
				btn.SetUp()
			btn.Show()

	def __OnSelectEntryCount(self, index):
		if self.entryCount == index:
			return

		for i in xrange(self.ENTRYCOUNT_BUTTON_COUNT):
			if i != index:
				self.main["entry_count"][i].SetUp()
			else:
				self.main["entry_count"][i].Down()

		self.entryCount = index
		self.__SearchItems()

	def __OnSelectPageBtn(self, index):
		btn = self.main["page_btn"][index]
		self.SelectPage(btn.pageIdx)

	def __GetMaxPage(self):
		return max(1, shopsearch.GetResultPageMaxNum())

	def __OnSelectLastPageBtn(self):
		self.__SelectPage( - 1)

	def __ChangePage(self, amount):
		self.page += amount
		if self.page < 0:
			self.page = 0
		if self.page >= self.__GetMaxPage():
			self.page = self.__GetMaxPage() - 1

		self.__SearchItems()

	def __SelectPage(self, pageIdx):
		self.page = pageIdx
		self.__SearchItems()

	def __OnAddToFavourite(self, itemIndex):
		itemVnum = shopsearch.GetResultItemVnum(itemIndex)
		item.SelectItem(itemVnum)
		itemName = item.GetItemName(False)

		emptyIdx = -1
		for i in xrange(self.FavouriteBoard.ITEM_MAX_COUNT):
			favName = cfg.Get(cfg.SAVE_SHOPSEARCH, "fav_%d" % i, "")
			if not favName:
				emptyIdx = i
				break

			if favName == itemName:
				self.popupDlg.SetText(localeInfo.SHOP_SEARCH_FAV_SAVE_ALREADY)
				self.popupDlg.Open()
				return

		if emptyIdx == -1:
			self.popupDlg.SetText(localeInfo.SHOP_SEARCH_FAV_SAVE_NO_EMPTY)
			self.popupDlg.Open()
			return

		cfg.Set(cfg.SAVE_SHOPSEARCH, "fav_%d" % emptyIdx, itemName)

		if self.favBoard.IsShow():
			self.favBoard.RefreshFavourites()

		self.popupDlg.SetText(localeInfo.SHOP_SEARCH_FAV_SAVE_SUCCESS)
		self.popupDlg.Open()

	def __OnRequestAveragePrice(self, itemIndex):
		itemVnum = shopsearch.GetResultItemVnum(itemIndex)
		net.SendShopSearchRequestSoldInfo(itemVnum)

		self.currentGraphItem = itemVnum
		self.currentGraphRefresh = False

	##################
	## GRAPH WINDOW
	##################

	def __GraphOnSelectWeekly(self):
		self.main["graph"]["wnd"].LoadImage(ROOT_PATH + "graph/bg_weekly.tga")
		self.main["graph"]["wnd"].SetPosition(8, 32)

		self.main["graph"]["x_desc_weekly"]["wnd"].Show()
		self.main["graph"]["x_desc_monthly"]["wnd"].Hide()

		self.main["graph"]["weekly_btn"].Down()
		self.main["graph"]["monthly_btn"].SetUp()

		self.__GraphRefresh()

	def __GraphOnSelectMonthly(self):
		self.main["graph"]["wnd"].LoadImage(ROOT_PATH + "graph/bg_monthly.tga")
		self.main["graph"]["wnd"].SetPosition(8, 32)

		self.main["graph"]["x_desc_weekly"]["wnd"].Hide()
		self.main["graph"]["x_desc_monthly"]["wnd"].Show()

		self.main["graph"]["weekly_btn"].SetUp()
		self.main["graph"]["monthly_btn"].Down()

		self.__GraphRefresh()

	def __GraphOnClickRefresh(self):
		net.SendShopSearchRequestSoldInfo(self.currentGraphItem)
		self.currentGraphRefresh = True

	def __GraphPriceOnOver(self, x, y, value):
		cursor = self.main["graph"]["price_cursor"]
		cursor.SetPosition(x - cursor.GetWidth() / 2, y - cursor.GetHeight() / 2)
		cursor.Show()

		moneyText = self.main["graph"]["price_cursor_money"]
		moneyText.SetText(localeInfo.SHOP_SEARCH_GRAPH_AVERAGE_PRICE_TOOLTIP % (localeInfo.NumberToString(int(value)), str(ui.GenerateColor(255, 0, 0))))
		moneyText.SetPosition(-4 - moneyText.GetWidth(), 0)

	def __GraphPriceOnOut(self):
		self.main["graph"]["price_cursor"].Hide()

	def __GraphGetXAxisCount(self):
		if self.main["graph"]["x_desc_weekly"]["wnd"].IsShow():
			return 7
		else:
			return shopsearch.SOLD_ITEM_INFO_COUNT

	def __GraphRefreshPrice(self):
		xAxisLimitCount = self.__GraphGetXAxisCount()

		maxPrice = shopsearch.GetSoldPriceAverage(0)
		for i in xrange(1, xAxisLimitCount):
			price = shopsearch.GetSoldPriceAverage(i)
			if price > maxPrice:
				maxPrice = price

		stepValue = (1 + maxPrice / (self.GRAPH_PRICE_STEP * self.GRAPH_PRICE_Y_DESC_MAX_NUM)) * self.GRAPH_PRICE_STEP
		for i in xrange(self.GRAPH_PRICE_Y_DESC_MAX_NUM):
			self.main["graph"]["y_desc_price"][i].SetText(localeInfo.NumberToString((i + 1) * stepValue))

		graph = self.main["graph"]["graph_price"]
		graph.SetYAxisLimitValue(0, stepValue * self.GRAPH_PRICE_Y_DESC_MAX_NUM)
		graph.SetXAxisLimitValue(0, xAxisLimitCount)

		graph.Clear()
		for i in xrange(xAxisLimitCount):
			graph.AddValue(xAxisLimitCount - (i + 1), shopsearch.GetSoldPriceAverage(i))
		graph.AddValue(xAxisLimitCount, shopsearch.GetSoldPriceAverage(0))

		graph.Refresh()

	def __GraphRefreshCount(self):
		xAxisLimitCount = self.__GraphGetXAxisCount()

		maxCount = shopsearch.GetSoldItemCount(0)
		for i in xrange(1, xAxisLimitCount):
			count = shopsearch.GetSoldItemCount(i)
			if count > maxCount:
				maxCount = count

		stepValue = (1 + max(0, (maxCount - 1)) / (self.GRAPH_COUNT_STEP * self.GRAPH_COUNT_Y_DESC_MAX_NUM)) * self.GRAPH_COUNT_STEP
		for i in xrange(self.GRAPH_COUNT_Y_DESC_MAX_NUM):
			self.main["graph"]["y_desc_count"][i].SetText(localeInfo.NumberToString((i + 1) * stepValue))

		graph = self.main["graph"]["graph_count"]
		graph.SetYAxisLimitValue(0, stepValue * self.GRAPH_COUNT_Y_DESC_MAX_NUM)
		graph.SetXAxisLimitValue(0, xAxisLimitCount)

		graph.Clear()
		for i in xrange(xAxisLimitCount):
			graph.AddValue(xAxisLimitCount - (i + 1), shopsearch.GetSoldItemCount(i))

		graph.Refresh()

	def __GraphRefreshXAxisDesc(self):
		xAxisLimitCount = self.__GraphGetXAxisCount()

		if xAxisLimitCount == 7:
			objCount = self.GRAPH_X_DESC_WEEKLY_MAX_NUM
			objList = self.main["graph"]["x_desc_weekly"]
		else:
			objCount = self.GRAPH_X_DESC_MONTHLY_MAX_NUM
			objList = self.main["graph"]["x_desc_monthly"]

		dayChange = 0
		for i in xrange(objCount):
			objList[objCount - i - 1].SetText("%02d/%02d" % (1 + app.GetLocalMonth(int(dayChange)), app.GetLocalDay(int(dayChange))))
			dayChange -= float(xAxisLimitCount) / objCount

	def __GraphRefresh(self):
		item.SelectItem(self.currentGraphItem)
		self.main["graph"]["item_name"].SetText(item.GetItemName())

		self.__GraphRefreshPrice()
		self.__GraphRefreshCount()
		self.__GraphRefreshXAxisDesc()

	def ShowSoldInfoResult(self, hasResults):
		if not hasResults:
			self.popupDlg.SetText(localeInfo.SHOP_SEARCH_GRAPH_NO_HISTORY)
			self.popupDlg.Open()
			return

		self.main["graph"]["last_updated"].SetText(localeInfo.SHOP_SEARCH_GRAPH_LAST_UPDATED % time.strftime("%Y.%m.%d  %H:%M"))

		self.__GraphRefresh()
		self.main["graph"]["wnd"].Show()

		self.__DisableItemTooltip()

		if self.currentGraphRefresh:
			self.popupDlg.SetText(localeInfo.SHOP_SEARCH_GRAPH_REFRESH_SUCCESS)
			self.popupDlg.Open()
