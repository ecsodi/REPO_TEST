import ui
import chat
import item
import localeInfo
import uiToolTip
import player
import grp
import app
import net

def FReturnInfo(func,index):
	(vnum_reward,count_reward,item_reward_stackable,vnum_material_1,count_material_1,vnum_material_2,count_material_2,vnum_material_3,count_material_3,vnum_material_4,count_material_4,vnum_material_5,count_material_5,gold, gaya_green, gaya_blue, percent,category) = player.GetCubeInfo(index)
	info = {
			"vnum_reward" : vnum_reward,
			"count_reward" : count_reward,
			"item_reward_stackable" : item_reward_stackable,
			"vnum_material_1" : vnum_material_1,
			"count_material_1" : count_material_1,
			"vnum_material_2" : vnum_material_2,
			"count_material_2" : count_material_2,
			"vnum_material_3" : vnum_material_3,
			"count_material_3" : count_material_3,
			"vnum_material_4" : vnum_material_4,
			"count_material_4" : count_material_4,
			"vnum_material_5" : vnum_material_5,
			"count_material_5" : count_material_5,
			"gold" : gold,
			"gaya_green" : gaya_green,
			"gaya_blue" : gaya_blue,
			"percent" : percent,
			"category" : category,
	}

	return info[func]

class CubeRenewalItem(ui.Window):

	def __init__(self, getParentEvent):
		ui.Window.__init__(self)
		self.SetParent(getParentEvent().GetBoard())

		self.index = -1
		self.type = -1

		self.count_all = -1

		self.date_cube = None

		self.index = -1

		self.button = ui.Button()
		self.button.SetParent(self)
		self.button.SetEvent(ui.__mem_func__(self.Select))
		self.button.Show()

		self.image = ui.ImageBox()
		self.image.SetParent(self)
		self.image.SetPosition(7,3)
		self.image.Show()

		self.text = ui.TextLine()
		self.text.SetParent(self)
		self.text.SetPosition(40,2)
		self.text.Show()

		self.count_total = ui.TextLine()
		self.count_total.SetParent(self)
		self.count_total.SetPosition(16,2)
		self.count_total.Hide()

		self.getParentEvent = getParentEvent

		self.SetSize(280, 17)

	def __del__(self):
		ui.Window.__del__(self)

	def SetName(self, name):
		self.name = name
		self.text.SetText(name)

	def SetCountTotal(self, count):

		self.count_all = count

		if count <= 0:
			self.count_total.Hide()
			self.text.SetPosition(17,2)
			return

		self.count_total.SetText("[%d]"%(count*self.GetCountReward()))
		self.count_total.SetPackedFontColor(grp.GenerateColor(0.5411, 0.7254, 0.5568, 1.0))
		self.count_total.Show()

		w, h = self.count_total.GetTextSize()
		self.text.SetPosition(w+20,2)

	def GetCount(self):
		return self.count_all

	def SetType(self,type):
		self.type = type

	def AppendIndex(self,index):
		self.index = index

	def GetIndex(self):
		return self.index

	def GetDates(self,func):
		return FReturnInfo(func,self.GetIndex())

	def GetVnumReward(self):
		return self.GetDates("vnum_reward")

	def GetCountReward(self):
		return self.GetDates("count_reward")

	def GetItemStackable(self):
		return self.GetDates("item_reward_stackable")

	def GetVnumMaterial(self,index):
		return self.GetDates("vnum_material_%d"%index)

	def GetCountMaterial(self,index):
		return self.GetDates("count_material_%d"%index)

	def GetGold(self):
		return self.GetDates("gold")

	def GetGayaGreen(self):
		return self.GetDates("gaya_green")

	def GetGayaBlue(self):
		return self.GetDates("gaya_blue")

	def GetPorcentaje(self):
		return self.GetDates("percent")

	def GetName(self):
		return self.name

	def GetType(self):
		return self.type

	def GetStepWidth(self):
		return 0

	def Select(self):
		self.getParentEvent().OnSelectItem(self)

class CubeRenewalCategoriaItem(CubeRenewalItem):

	def __init__(self, getParentEvent):
		self.OpenFunc = False
		self.SubCategorias = []
		self.index = -1

		CubeRenewalItem.__init__(self, getParentEvent)

		self.button.SetUpVisual("d:/ymir work/ui/game/cube/cube_menu_tab1.sub")
		self.button.SetOverVisual("d:/ymir work/ui/game/cube/cube_menu_tab1.sub")
		self.button.SetDownVisual("d:/ymir work/ui/game/cube/cube_menu_tab1.sub")

		self.SetType(1)

	def __del__(self):
		CubeRenewalItem.__del__(self)

	def SetCategoria(self,index,name):
		self.SetName(name)
		self.IndexCategoria(index)

	def AppendSubCategorias(self, date_cube):
		subcategorias = CubeRenewalSubCategoriaItem(self.getParentEvent)
		subcategorias.AppendIndex(date_cube)
		subcategorias.LoadInfo()
		subcategorias.Select()
		self.SubCategorias.append(subcategorias)

	def GetListSubCategorias(self):
		return self.SubCategorias

	def IndexCategoria(self,index):
		self.index = index

	def GetIndexCategoria(self):
		return self.index

	def FindVnumSubCategoria(self, key):
		list = filter(lambda argMember, argKey=key: argMember.IsSameVnum(argKey), self.SubCategorias)
		if list:
			return list[0]

		return None

	def Open(self):
		self.image.LoadImage("d:/ymir work/ui/game/cube/cube_menu_tab1_minus.sub")
		self.OpenFunc = True

	def Close(self):
		self.image.LoadImage("d:/ymir work/ui/game/cube/cube_menu_tab1_plus.sub")
		self.OpenFunc = False
		map(ui.Window.Hide, self.SubCategorias)

	def IsOpen(self):
		return self.OpenFunc

	def Select(self):
		if self.OpenFunc:
			self.Close()
		else:
			self.Open()

		for x in self.GetListSubCategorias():
			x.Select()

		self.getParentEvent().OnRefresh()
		
class CubeRenewalSubCategoriaItem(CubeRenewalItem):

	def __init__(self, getParentEvent):

		self.OpenFunc = False
		self.SubCategoriaObjects = []

		CubeRenewalItem.__init__(self, getParentEvent)

		self.button.SetUpVisual("d:/ymir work/ui/game/cube/cube_menu_tab2.sub")
		self.button.SetOverVisual("d:/ymir work/ui/game/cube/cube_menu_tab2.sub")
		self.button.SetDownVisual("d:/ymir work/ui/game/cube/cube_menu_tab2.sub")

		self.image.SetPosition(7,4)
		self.text.SetPosition(25,2)
		self.text.SetPackedFontColor(0xffa28b5f)

		self.SetType(2)

	def __del__(self):
		CubeRenewalItem.__del__(self)

	def LoadInfo(self):
		item.SelectItem(self.GetVnumReward())
		self.SetName(item.GetItemName())

	def AppendSubCategoriaObjects(self, date_cube):
		subcategoriaobj = CubeRenewalSubCategoriaObjects(self.getParentEvent)
		subcategoriaobj.AppendIndex(date_cube)
		subcategoriaobj.LoadInfo()
		self.SubCategoriaObjects.append(subcategoriaobj)

	def IsSameVnum(self, vnum):
		return self.GetVnumReward() == vnum

	def Open(self):
		self.image.LoadImage("d:/ymir work/ui/game/cube/cube_menu_tab2_minus.sub")
		self.OpenFunc = True

	def Close(self):
		self.image.LoadImage("d:/ymir work/ui/game/cube/cube_menu_tab2_plus.sub")
		self.OpenFunc = False
		map(ui.Window.Hide, self.SubCategoriaObjects)

	def IsOpen(self):
		return self.OpenFunc

	def GetListSubCategoriasObjects(self):
		return self.SubCategoriaObjects

	def Select(self):
		if self.OpenFunc:
			self.Close()
		else:
			self.Open()

		self.getParentEvent().OnRefresh()

class CubeRenewalSubCategoriaObjects(CubeRenewalItem):
	def __init__(self, getParentEvent):
		CubeRenewalItem.__init__(self, getParentEvent)

		self.button.SetUpVisual("d:/ymir work/ui/game/cube/cube_menu_tab3_default.sub")
		self.button.SetOverVisual("d:/ymir work/ui/game/cube/cube_menu_tab3_select.sub")
		self.button.SetDownVisual("d:/ymir work/ui/game/cube/cube_menu_tab3_select.sub")
		self.SetType(3)
		self.text.SetPosition(17,2)

	def __del__(self):
		CubeRenewalItem.__del__(self)

	def LoadInfo(self):
		item.SelectItem(self.GetVnumReward())
		self.SetName(item.GetItemName()+' (%d%%)'%(self.GetPorcentaje()))
		self.CountTotal()

	def CountTotal(self):
		count_items = []
		count_all_items = 0

		for i in xrange(1,6):
			if self.GetVnumMaterial(i) != 0:
				if player.GetItemCountByVnum(self.GetVnumMaterial(i)) >= self.GetCountMaterial(i):
					number = player.GetItemCountByVnum(self.GetVnumMaterial(i)) / (self.GetCountMaterial(i))
					count_items.append(number)
				count_all_items += 1

		if len(count_items) >= count_all_items:
			self.SetCountTotal(min(count_items))
		else:
			self.SetCountTotal(0)

	def UnSelect(self):
		self.button.SetUp()
		self.button.Enable()

	def SetSelect(self):
		self.button.Down()
		self.button.Disable()

	def Select(self):
		self.getParentEvent().SelectObject(self)

class CubeRenewalWindows(ui.ScriptWindow):

	def __init__(self):
		ui.ScriptWindow.__init__(self)

		self.categoria = [
			[1,"Arme","Arme"],
			[2,"Armuri","Armuri"],
			[3,"Echipament","Echipament"],
			[4,"Armuri-Beta","Armuri Beta"],
			[5,"Arme-Beta","Arme Beta"],
			[6,"Colier", localeInfo.SEARCH_OBJECT_NECK],
			[7,"Bratara",localeInfo.SEARCH_OBJECT_WRIST],
			[8,"Papuci", localeInfo.SEARCH_OBJECT_SHOES],
			[9,"Cercei", localeInfo.SEARCH_OBJECT_EAR],
			[10,"Mount", localeInfo.CUBE_MOUNT_CAT],
			[11,"Scut", localeInfo.SEARCH_OBJECT_SHIELD],
			[40,"Coif",localeInfo.SEARCH_OBJECT_HEAD],
			[12,"GURTEL3","End-PvM-Gurtel"],
			[13,"TALISMAN","Talisman"],
			[14,"ERZE1","Ores"],
			[15,"ERZE2"," Perm. Ores"],
			[16,"BRACLETTE2","Braclette"],
			[17,"EARRINGS2","Earrings"],
			[18,"NECKLACE2","Necklace"],
			[19,"ARMOR4","Warrior-Armor"],
			[20,"ARMOR5","Ninja-Armor"],
			[21,"ARMOR6","Sura-Armor"],
			[22,"ARMOR7","Shaman-Armor"],
			[23,"DEWS","Refill-Dews"],
			[24,"Pet","Animal de companie"],
			[25,"ArmaWar","Weapon"],
			[26,"PVPWAFFENKRIEGER","Krieger"],
			[27,"PVPWAFFENNINJA","Ninja"],
			[28,"PVPWAFFENSURA","Sura"],
			[29,"PVPWAFFENSCHAMANE","Schamane"],
			[30,"PVPHELM","Helmets"],
			[31,"PVMHELM","Helmets"],
			[32,"KRISTALL","Energiecrystal"],
			[33,"Manni","Manni"],
			[34,"Manu","Manu"],
			[35,"PVPSHOES","PvP-Shoes"],
			[36,"PVMSHOES","PvM-Shoes"],
			[37,"KOSIS", localeInfo.CUBE_COSTUMES],
			[38,"KOSIS2", localeInfo.CUBE_HAIRSTYLES],
			[39,"KOSIS3", localeInfo.CUBE_WEAPON_COSTUMES],

			[999,"DEFAULT", "Obiecte"]
		]

		self.showingItemList = []
		self.categoria_list = []
		self.startLine = 0
		self.MaxElements = 12
		self.cube_elements = {}
		self.selectedItem = None
		self.count_item_reward = 0
		self.bLoaded = False

		self.toolTip = uiToolTip.ItemToolTip()
		self.toolTip.Hide()

		self.__LoadWindow()

	def __del__(self):
		ui.ScriptWindow.__del__(self)

	def Openz(self):
		ui.ScriptWindow.Show(self)

	def Destroy(self):
		self.ClearDictionary()
		if len(self.showingItemList) > 0:
			for item in self.showingItemList:
				item.Destroy()
				del item
	
			self.showingItemList = []

		if len(self.categoria_list) > 0:
			for item in self.categoria_list:
				item.Destroy()
				del item
	
			self.categoria_list = []
			
		self.categoria = []

		if self.toolTip:
			self.toolTip.Hide()
			self.toolTip = None

	def __LoadWindow(self):
		if self.bLoaded:
			return
	
		self.bLoaded = True
		try:
			pyScrLoader = ui.PythonScriptLoader()
			pyScrLoader.LoadScriptFile(self, "uiscript/cuberenewalwindow.py")
		except:
			import exception
			exception.Abort("CubeRenewalWindows.__LoadWindow.LoadObject")

		try:
			self.board = self.GetChild("item_list_board")
			self.item_slot = self.GetChild("item_slot")
			self.cube_list_scroll_bar = self.GetChild("cube_list_scroll_bar")
			self.yang_text = self.GetChild("yang_text")
			self.wndGayaBlue = self.GetChild("gaya_blue_text")
			# self.wndGayaGreen = self.GetChild("gaya_green_text")
			self.result_qty = self.GetChild("result_qty")
			self.button_ok = self.GetChild("button_ok")
			self.button_cancel = self.GetChild("button_cancel")

			self.qty_sub_button = self.GetChild("qty_sub_button")
			self.qty_add_button = self.GetChild("qty_add_button")

			self.GetChild("board").SetCloseEvent(ui.__mem_func__(self.Close))

			for i in xrange(1,6):
				self.cube_elements["count_elements_%d"%i] = self.GetChild("material_qty_text_%d"%i)

		except:
			import exception
			exception.Abort("CubeRenewalWindows.__LoadWindow.LoadElements")

		self.button_cancel.SetEvent(ui.__mem_func__(self.Close))

		self.button_ok.SetEvent(ui.__mem_func__(self.AceptCube))
		self.result_qty.SetReturnEvent(ui.__mem_func__(self.AceptInputItem))
		self.result_qty.CanEdit(False)

		self.qty_sub_button.SetEvent(ui.__mem_func__(self.QtySubButton))
		self.qty_add_button.SetEvent(ui.__mem_func__(self.QtyAddButton))

		self.cube_list_scroll_bar.SetScrollEvent(ui.__mem_func__(self.OnScroll))

		self.icons_items = ui.SlotWindow()
		self.icons_items.SetParent(self.item_slot)
		self.icons_items.SetPosition(25,13)
		self.icons_items.SetSize((32*9),32*3)
		self.icons_items.SetOverInItemEvent(ui.__mem_func__(self.OverInItem))
		self.icons_items.SetOverOutItemEvent(ui.__mem_func__(self.OverOutItem))
		self.icons_items.AppendSlot(0,0,0,32,32*3)

		for i in xrange(0,6):
			self.icons_items.AppendSlot(i+1,46*i+62,0,32,32*3)

		self.icons_items.Show()

	def BINARY_CUBE_RENEWAL_LOADING(self):
		self.ClearElements()
		self.LoadCategoria()
		self.LoadSubCategoria()
		self.LoadSubObjects()
		self.OnRefresh()
		self.SetCenterPosition()

	def BINARY_CUBE_RENEWAL_UPDATE(self):
		if self.selectedItem:
			self.UpdateCountSubCategoria()
			self.UpdateMaterialCount()

	def ClearElements(self):
		if len(self.showingItemList) > 0:
			map(ui.Window.Hide, self.showingItemList)

		for group in self.categoria_list:
			group.Close()

			for categorias in group.GetListSubCategorias():
				categorias.Close()

		for i in xrange(0,6):
			self.icons_items.ClearSlot(i)
			if i > 0:
				self.cube_elements["count_elements_%d"%i].Hide()

		self.yang_text.Hide()
		self.wndGayaBlue.Hide()
		# self.wndGayaGreen.Hide()
		self.result_qty.Hide()

		self.categoria_list = []
		self.startLine = 0

		self.cube_list_scroll_bar.SetPos(0)

	def CheckListCategoriasTotal(self):
		list1 = []
		list2 = []
		
		lala = player.GetCubeSize()

		for i2 in xrange(lala):
			list1.append(self.CheckCategoryIndex(FReturnInfo("category",i2)))

		for ia in list1:
			if ia not in list2:
				list2.append(ia)

		return list2

	def LoadCategoria(self):
		world = self.CheckListCategoriasTotal()
		for i in world:
			for i1 in xrange(len(self.categoria)):
				if self.categoria[i1][0] == i:
					member = CubeRenewalCategoriaItem(ui.__mem_func__(self.GetSelf))
					member.SetCategoria(self.categoria[i1][0],self.categoria[i1][2])
					member.Close()
					member.Show()
					self.categoria_list.append(member)

	def CheckCategoryIndex(self,name):
		vnum_default = 0
		for i in xrange(len(self.categoria)):
			if name == self.categoria[i][1]:
				return self.categoria[i][0]
		for i in xrange(len(self.categoria)):		
			if "DEFAULT" == self.categoria[i][1]:
				return self.categoria[i][0]

	def LoadSubCategoria(self):
		lala = player.GetCubeSize()
		for group in self.categoria_list:
			for i in xrange(int(lala)):
				if self.CheckCategoryIndex(FReturnInfo("category",i)) == group.GetIndexCategoria():
					if not group.FindVnumSubCategoria(FReturnInfo("vnum_reward",i)):
						group.AppendSubCategorias(i)

	def LoadSubObjects(self):
		for group in self.categoria_list:
			for i in xrange(player.GetCubeSize()):
				if self.CheckCategoryIndex(FReturnInfo("category",i)) == group.GetIndexCategoria():
					for categorias in group.GetListSubCategorias():
						if FReturnInfo("vnum_reward",i) == categorias.GetVnumReward():
							categorias.AppendSubCategoriaObjects(i)

	# if app.ENABLE_MOUSEWHEEL_EVENT:
	def OnRunMouseWheel(self, nLen):
		if nLen > 0:
			self.cube_list_scroll_bar.OnUp()
		else:
			self.cube_list_scroll_bar.OnDown()

	def OnScroll(self):
		scrollLineCount = len(self.showingItemList) - (self.MaxElements)
		startLine = int(scrollLineCount * self.cube_list_scroll_bar.GetPos())


		if startLine != self.startLine:
			self.startLine = startLine
			self.SetExtraInfo()

	def OnRefresh(self):
		self.showingItemList = []

		for group in self.categoria_list:
			self.showingItemList.append(group)

			if group.IsOpen():
				for categorias in group.GetListSubCategorias():
					self.showingItemList.append(categorias)

					if categorias.IsOpen():
						for a in categorias.GetListSubCategoriasObjects():
							self.showingItemList.append(a)

		self.SetExtraInfo()

	def SetExtraInfo(self):
		if self.MaxElements >= len(self.showingItemList):
			self.cube_list_scroll_bar.Hide()
			self.startLine = 0
		else:
			if self.showingItemList:
				self.cube_list_scroll_bar.SetMiddleBarSize(float(self.MaxElements) / float(len(self.showingItemList)))
			self.cube_list_scroll_bar.Show()

		map(ui.Window.Hide, self.showingItemList)

		yPos = 11
		heightLimit = 240

		for item in self.showingItemList[self.startLine:]:
			XPos = 0
			if item.GetType() == 2:
				XPos += 15
			if item.GetType() == 3:
				XPos += 35
			item.SetPosition(6 + XPos, yPos)
			item.SetTop()
			item.Show()

			yPos += 20

			if yPos > heightLimit:
				break

	def SelectObject(self,item):
		self.selectedItem = item
		if self.selectedItem:	
			self.UpdateInfoSelect()
			self.UpdateSelectSubCategoria()

	def UpdateInfoSelect(self):

		self.icons_items.ClearSlot(0)
		self.icons_items.SetItemSlot(0,self.selectedItem.GetVnumReward(),self.selectedItem.GetCountReward())

		for i in xrange(1,6):
			self.icons_items.ClearSlot(i)
			self.icons_items.SetItemSlot(i, self.selectedItem.GetVnumMaterial(i), self.selectedItem.GetCountMaterial(i))


		self.result_qty.KillFocus()
		self.result_qty.CanEdit(self.selectedItem.GetItemStackable())
		self.result_qty.SetText("%s"%(self.selectedItem.GetCountReward()))
		self.result_qty.Show()

		self.count_item_reward = self.selectedItem.GetCountReward()
	
		self.UpdateMaterialCount()
		

	def UpdateMaterialCount(self):
		count = (self.count_item_reward/(self.selectedItem.GetCountReward()))

		for i in xrange(1,6):
			if self.selectedItem.GetVnumMaterial(i) != 0:
				if player.GetItemCountByVnum(self.selectedItem.GetVnumMaterial(i)) >= (self.selectedItem.GetCountMaterial(i)*count):
					self.cube_elements["count_elements_%d"%i].SetPackedFontColor(grp.GenerateColor(0.5411, 0.7254, 0.5568, 1.0))
				else:
					self.cube_elements["count_elements_%d"%i].SetPackedFontColor(grp.GenerateColor(0.9, 0.4745, 0.4627, 1.0))

				self.cube_elements["count_elements_%d"%i].SetText("%d/%d"%(player.GetItemCountByVnum(self.selectedItem.GetVnumMaterial(i)),self.selectedItem.GetCountMaterial(i)*count))
				self.cube_elements["count_elements_%d"%i].Show()
			else:
				self.cube_elements["count_elements_%d"%i].Hide()

		self.yang_text.SetText(localeInfo.NumberToMoneyString(self.selectedItem.GetGold()*count))
		self.yang_text.Show()
		
		self.wndGayaBlue.SetText(localeInfo.AddPointToNumberString(self.selectedItem.GetGayaBlue()*count))
		self.wndGayaBlue.Show()

		# self.wndGayaGreen.SetText(localeInfo.AddPointToNumberString(self.selectedItem.GetGayaGreen()*count))
		# self.wndGayaGreen.Show()

	def ConvertInputResult(self):
		edit = int(self.result_qty.GetText())
		total = self.selectedItem.GetCountReward()
		convert = edit % total
		return convert

	def AceptInputItem(self):
		self.result_qty.KillFocus()

		result_total = int(self.result_qty.GetText())

		if int(self.result_qty.GetText()) < self.selectedItem.GetCountReward():
			result_total = self.selectedItem.GetCountReward()
		elif result_total > 200:
			result_total = 200
		else:
			result = self.ConvertInputResult()
			if result != 0:
				result_total = result_total-result

		self.count_item_reward = result_total
		self.result_qty.SetText("%d"%(result_total))

		self.icons_items.ClearSlot(0)
		self.icons_items.SetItemSlot(0,self.selectedItem.GetVnumReward(),self.count_item_reward)
		
	def AceptCube(self):
		if self.selectedItem:
			index = self.selectedItem.GetIndex()
			self.CheckInputFocus()
			count = (self.count_item_reward/(self.selectedItem.GetCountReward()))
			net.SendChatPacket("/cube m %d %d" % (index, count))

	def QtyAddButton(self):
		if self.selectedItem and self.selectedItem.GetItemStackable():
			self.result_qty.SetText("%d"%(self.selectedItem.GetCountReward()*self.selectedItem.GetCount()))
			self.AceptInputItem()

	def QtySubButton(self):
		if self.selectedItem and self.selectedItem.GetItemStackable():
			self.result_qty.SetText("%d"%(self.selectedItem.GetCountReward()))
			self.AceptInputItem()

	def CheckInputFocus(self):
		if self.result_qty.IsFocus():
			self.result_qty.SetText("%d"%(self.selectedItem.GetCountReward()))
			self.AceptInputItem()

	def OnSelectItem(self, item):
		self.selectedItem = item

		if self.selectedItem:
			self.selectedItem.Select()

	def OnRender(self):
		if len(self.showingItemList) > 0:
			self.UpdateCountSubCategoria()
		if self.selectedItem:
			self.UpdateMaterialCount()

	def UpdateCountSubCategoria(self):
		for group in self.categoria_list:
			if group.IsOpen():
				for categorias in group.GetListSubCategorias():
					if categorias.IsOpen():
						for a in categorias.GetListSubCategoriasObjects():
							a.CountTotal()

	def UpdateSelectSubCategoria(self):
		for group in self.categoria_list:
			for categorias in group.GetListSubCategorias():
				for a in categorias.GetListSubCategoriasObjects():
					a.UnSelect()
		self.selectedItem.SetSelect()

	def GetBoard(self):
		return self.board

	def GetSelf(self):
		return self		

	def OverInItem(self, index):
		self.toolTip.ClearToolTip()
		
		if self.selectedItem:
			if index == 0:
				vnum = self.selectedItem.GetVnumReward()
			else:
				vnum = self.selectedItem.GetVnumMaterial(index)

		metinSlot = []
		for i in xrange(player.METIN_SOCKET_MAX_NUM):
			metinSlot.append(0)

		self.toolTip.AddItemData(vnum,metinSlot)

	def OverOutItem(self):
		self.toolTip.Hide()

	def Close(self):
		net.SendChatPacket("/cube c")
		
		self.Hide()
		if self.selectedItem:
			del self.selectedItem
		
		self.selectedItem = None

	def OnPressEscapeKey(self):
		self.Close()
		return True
