import ui
import app
import wndMgr
import grp
import chat
import uiToolTip
import item
import mouseModule
import player
import net
import localeInfo
import uiCommon
import cPickle as pickle

WORLDARD_PATCH = "Switchbot/design/"
MAX_BONUS = 5
MAX_SAVE  = 8
VNUM_ITEM_CHANGE = 71084
MAX_CHANGE = 5000

class SwitchBotListElements(ui.Window):
	def __init__(self,wndSwitchBot,wndThinBoard,wndIndex):
		ui.Window.__init__(self,"TOP_MOST")
		self.wndSwitchBot = wndSwitchBot
		self.wndThinBoard = wndThinBoard
		self.wndIndex = wndIndex
		self.wndIsOpen = False
		self.id = -1
		self.name = ""

		self.__LoadWindow()

	def __del__(self): 
		ui.Window.__del__(self)

	def Show(self):
		ui.Window.Show(self)

		self.SetOpen(True)
		self.AdjustPositionAndSize()
		
	def __LoadWindow(self):
		self.listBox = ui.ComboBox.ListBoxWithBoard("TOP_MOST")
		self.listBox.SetPickAlways()
		self.listBox.SetParent(self)
		self.listBox.SetPosition(0,0)
		self.listBox.SetEvent(self.OnSelectItem)
		self.listBox.Show()

	def InsertBonus(self,index,name):
		self.listBox.InsertItem(index, name)
		self.listBox.ArrangeItem()

	def GetBasePosition(self):
		x, y = self.wndThinBoard.GetGlobalPosition()
		return x-1, y+23

	def AdjustPositionAndSize(self):
		bx, by = self.GetBasePosition()
		self.SetPosition(bx, by)

	def GetName(self):
		return self.name

	def GetId(self):
		return self.id

	def GetIndex(self):
		return self.wndIndex

	def ResetAll(self):
		self.id = -1
		self.name = ""

	def OnSelectItem(self,id,name):
		self.id = id
		self.name = name
		self.wndSwitchBot.SwitchBotListSelect(self)
		self.Close()

	def SetId(self,id):
		self.id = id

	def SetOpen(self,value):
		self.wndIsOpen = value

	def IsOpen(self):
		return	self.wndIsOpen

	def Close(self):
		self.listBox.ClearItem()
		self.SetOpen(False)
		wndMgr.Hide(self.hWnd)

class SwitchBotListBonus(SwitchBotListElements):
	def __init__(self,wndSwitchBot,wndThinBoard,wndIndex):
		SwitchBotListElements.__init__(self,wndSwitchBot,wndThinBoard,wndIndex)
		self.listBox.SetSize(205,20)

	def __del__(self): 
		SwitchBotListElements.__del__(self)

	def Select(self):
		self.wndSwitchBot.SetNameBonusSlot(self.GetIndex(),self.GetId(),self.GetName())
		self.wndSwitchBot.ResetValueBonus(self.GetIndex())

class SwitchBotListValue(SwitchBotListElements):
	def __init__(self,wndSwitchBot,wndThinBoard,wndIndex):
		SwitchBotListElements.__init__(self,wndSwitchBot,wndThinBoard,wndIndex)
		self.listBox.SetSize(39,20)

	def __del__(self): 
		SwitchBotListElements.__del__(self)

	def Select(self):
		self.wndSwitchBot.SetValueBonusSlot(self.GetIndex(),self.GetId(),self.GetName())

class UiSwitchBot(ui.ScriptWindow):
	def __init__(self):
		ui.ScriptWindow.__init__(self)

		self.get_affect 	= uiToolTip.AFFECT_DICT
		self.toolTip 		= uiToolTip.ItemToolTip()

		self.accept_message = uiCommon.QuestionDialog2()
		
		self.elements = {}
		self.elements["list_bonus"] = []
		self.elements["save_bonus"] = {}
		self.elements["select_presets"] = -1
		self.list_get_bonus_id_m_h = [[72,5,55],[71,5,25]] #Media - Habilidad [id,give_value,max_value]

		self.ScollPos = 0

		for i in xrange(0,MAX_BONUS):
			self.elements["id_select_bonus_%d"%i] = -1
			self.elements["id_select_value_%d"%i] = -1

		self.LoadWindow()

	def __del__(self):
		ui.ScriptWindow.__del__(self)

	def Show(self):
		ui.ScriptWindow.Show(self)
		self.AdjustPositionAndSize()

	def LoadWindow(self):
		try:
			pyScrLoader = ui.PythonScriptLoader()
			pyScrLoader.LoadScriptFile(self, "Switchbot/script/switchbot_windows.py")
		except:
			import exception
			exception.Abort("UiSwitchBot.LoadWindow.LoadObject")
		try:
			self.board 			= self.GetChild("board")
			self.base_save		= self.GetChild("base_save")
			self.scrollbar 		= self.GetChild("scrollbar")
			self.slot_item 		= self.GetChild("slot_item")
			self.change_button 	= self.GetChild("change_button")
			self.save_button 	= self.GetChild("save_button")
			self.titleBar 	= self.GetChild("TitleBar")
		except:
			import exception
			exception.Abort("UiSwitchBot.LoadWindow.LoadElements")
			
		self.titleBar.SetCloseEvent(ui.__mem_func__(self.Close))
		self.slot_item.LockSlot(1)
		self.slot_item.SetSelectEmptySlotEvent(ui.__mem_func__(self.__OnSelectEmptySlot))
		self.slot_item.SetSelectItemSlotEvent(ui.__mem_func__(self.__OnSelectItemSlot))
		self.slot_item.SetOverInItemEvent(ui.__mem_func__(self.OverInItem))
		self.slot_item.SetOverOutItemEvent(ui.__mem_func__(self.OverOutItem))

		self.save_button.SetEvent(self.SavePresets)
		self.change_button.SetEvent(self.ChangeBonus)

		self.BonusElements()
		self.SaveElements()
		self.LoadPresets()
		self.RefreshPresets()


		self.scrollbar.SetScrollEvent(ui.__mem_func__(self.RefreshPresets))

	def LoadPresets(self):
		try:
			with old_open('switchbot.wa', 'rb') as f:
				self.elements["save_bonus"] = pickle.load(f)
		except IOError:
			self.elements["save_bonus"] = {}


		self.scrollbar.SetPos(0.0)
		self.Diff = len(self.elements["save_bonus"]) - (MAX_SAVE)
		if self.Diff > 0:
			stepSize = 1.0 / self.Diff
			self.scrollbar.SetScrollStep( stepSize )
		self.ScollPos = 0

	def BonusElements(self):
		for i in xrange(0,MAX_BONUS):
			self.elements["slot_bonus_%d"%i] = ui.Button()
			self.elements["slot_bonus_%d"%i].SetParent(self.board)
			self.elements["slot_bonus_%d"%i].SetUpVisual(WORLDARD_PATCH+"slot_bonus_new.tga")
			self.elements["slot_bonus_%d"%i].SetOverVisual(WORLDARD_PATCH+"slot_bonus_new.tga")
			self.elements["slot_bonus_%d"%i].SetDownVisual(WORLDARD_PATCH+"slot_bonus_new.tga")
			self.elements["slot_bonus_%d"%i].SetPosition(87,58+i*24)
			self.elements["slot_bonus_%d"%i].SetEvent(self.SelectBonus,i)
			self.elements["slot_bonus_%d"%i].Show()

			self.elements["bonus_text_%d"%i] = ui.TextLine()
			self.elements["bonus_text_%d"%i].SetParent(self.elements["slot_bonus_%d"%i])
			self.elements["bonus_text_%d"%i].SetPosition(7,4)
			self.elements["bonus_text_%d"%i].SetText(".")
			self.elements["bonus_text_%d"%i].Show()

			self.elements["slot_value_%d"%i] = ui.Button()
			self.elements["slot_value_%d"%i].SetParent(self.board)
			self.elements["slot_value_%d"%i].SetUpVisual(WORLDARD_PATCH+"slot_valor.tga")
			self.elements["slot_value_%d"%i].SetOverVisual(WORLDARD_PATCH+"slot_valor.tga")
			self.elements["slot_value_%d"%i].SetDownVisual(WORLDARD_PATCH+"slot_valor.tga")
			self.elements["slot_value_%d"%i].SetPosition(295,58+i*24)
			self.elements["slot_value_%d"%i].SetEvent(self.SelectValue,i)
			self.elements["slot_value_%d"%i].Show()

			self.elements["value_text_%d"%i] = ui.TextLine()
			self.elements["value_text_%d"%i].SetParent(self.elements["slot_value_%d"%i])
			self.elements["value_text_%d"%i].SetPosition(20,3)
			self.elements["value_text_%d"%i].SetText("0")
			self.elements["value_text_%d"%i].SetHorizontalAlignCenter()
			self.elements["value_text_%d"%i].Show()

			self.elements["button_reset_bonus_%d"%i] = ui.Button()
			self.elements["button_reset_bonus_%d"%i].SetParent(self.board)
			self.elements["button_reset_bonus_%d"%i].SetUpVisual(WORLDARD_PATCH+"elim_bonus_1.tga")
			self.elements["button_reset_bonus_%d"%i].SetOverVisual(WORLDARD_PATCH+"elim_bonus_2.tga")
			self.elements["button_reset_bonus_%d"%i].SetDownVisual(WORLDARD_PATCH+"elim_bonus_3.tga")
			self.elements["button_reset_bonus_%d"%i].SetPosition(337,58+i*24)
			self.elements["button_reset_bonus_%d"%i].SetEvent(self.ResetBonus,i)
			self.elements["button_reset_bonus_%d"%i].Show()

			self.elements["list_bonus_%d"%i] = SwitchBotListBonus(self,self.elements["slot_bonus_%d"%i],i)
			self.elements["list_value_%d"%i] = SwitchBotListValue(self,self.elements["slot_value_%d"%i],i)

	def SaveElements(self):
		for i in xrange(0,MAX_SAVE):
			self.elements["slot_save_%d"%i] = ui.RadioButton()
			self.elements["slot_save_%d"%i].SetParent(self.base_save)
			self.elements["slot_save_%d"%i].SetUpVisual(WORLDARD_PATCH+"boton_lista_1.tga")
			self.elements["slot_save_%d"%i].SetOverVisual(WORLDARD_PATCH+"boton_lista_2.tga")
			self.elements["slot_save_%d"%i].SetDownVisual(WORLDARD_PATCH+"boton_lista_2.tga")
			self.elements["slot_save_%d"%i].SetPosition(4,7+i*18)
			
			self.elements["slot_save_%d"%i].Show()

			self.elements["bonus_save_text_%d"%i] = ui.TextLine()
			self.elements["bonus_save_text_%d"%i].SetParent(self.elements["slot_save_%d"%i])
			self.elements["bonus_save_text_%d"%i].SetPosition(7,1)
			self.elements["bonus_save_text_%d"%i].SetText("")
			self.elements["bonus_save_text_%d"%i].Show()


			self.elements["button_delete_save_%d"%i] = ui.Button()
			self.elements["button_delete_save_%d"%i].SetParent(self.base_save)
			self.elements["button_delete_save_%d"%i].SetUpVisual(WORLDARD_PATCH+"elim_lista_1.tga")
			self.elements["button_delete_save_%d"%i].SetOverVisual(WORLDARD_PATCH+"elim_lista_2.tga")
			self.elements["button_delete_save_%d"%i].SetDownVisual(WORLDARD_PATCH+"elim_lista_3.tga")
			self.elements["button_delete_save_%d"%i].SetPosition(142,7+i*18)
			
			self.elements["button_delete_save_%d"%i].Show()

	def func_clear_bonus_item(self):
		self.elements["select_presets"] = -1
		self.elements["list_bonus"] = []
		self.CloseListBonusAll()
		for i in xrange(0,MAX_BONUS):
			self.ResetBonus(i)

	def func_set_bonus_items(self,id_bonus,bonus_value_0,bonus_value_1,bonus_value_2,bonus_value_3,bonus_value_4):
		self.elements["list_bonus"].append([id_bonus,self.func_get_repeat_bonus(bonus_value_0,bonus_value_1,bonus_value_2,bonus_value_3,bonus_value_4)])

	def func_get_repeat_bonus(self,valor1,valor2,valor3,valor4,valor5):
		get_bonus = [valor1,valor2,valor3,valor4,valor5]
		list_new_bonus = []

		for key in get_bonus:
			if key not in list_new_bonus:
				list_new_bonus.append(key)	

		return  list_new_bonus

	def func_add_mh(self):
		for j in xrange(0,len(self.list_get_bonus_id_m_h)):
			list_value = []
			value_i = (self.list_get_bonus_id_m_h[j][2] / self.list_get_bonus_id_m_h[j][1])
			for i in xrange(1,value_i+1):
				list_value.append((self.list_get_bonus_id_m_h[j][1]*i))
			self.elements["list_bonus"].append([self.list_get_bonus_id_m_h[j][0],list_value])

	def func_add_change_item(self):
		count = 0
		vnum_item_change = VNUM_ITEM_CHANGE

		self.slot_item.ClearSlot(1)

		for i in xrange(player.INVENTORY_PAGE_SIZE*player.INVENTORY_PAGE_COUNT +1000):
			itemVNum = player.GetItemIndex(i)
			itemCount = player.GetItemCount(i)
			if itemVNum == vnum_item_change:
				count+=itemCount

		if count <= 0:
			self.slot_item.ClearSlot(1)
		else:
			if count <= MAX_CHANGE:
				self.slot_item.SetItemSlot(1,vnum_item_change,count)
			else:
				self.slot_item.SetItemSlot(1,vnum_item_change,MAX_CHANGE)

	def func_count_bonus_item(self):
		count = 0
		for i in xrange(0,MAX_BONUS):
			(type,value) = player.GetItemAttribute(player.SWITCHBOT,0, i)
			if type != 0:
				count += 1
		return count

	def func_count_select_bonus(self):
		count = 0
		for i in xrange(0,MAX_BONUS):
			if self.elements["id_select_bonus_%d"%i] >= 0:
				count+=1

		return count


	def func_max_select_bonus(self):
		if self.func_count_bonus_item() > 0:
			if self.func_count_select_bonus() >= self.func_count_bonus_item():
				return True
			else:
				return False
		else:
			return True

		return False

	def func_count_select_value(self):
		count = 0
		for i in xrange(0,MAX_BONUS):
			if self.elements["id_select_value_%d"%i] >= 0:
				count+=1

		return count

	def func_repeat_bonus(self):
		list_bonus_total = []
		list_bonus_new = []
		for i in xrange(0,MAX_BONUS):
			if self.elements["id_select_bonus_%d"%i] >= 0:
				list_bonus_total.append([self.elements["id_select_bonus_%d"%i]])

		count = 0
		count_bonus_repeat = 0

		for i in list_bonus_total:
			if i not in list_bonus_new:
				list_bonus_new.append(list_bonus_total[count])
			else:
				count_bonus_repeat = 1
			count += 1

		return  count_bonus_repeat


	def func_check_change(self):
		if player.GetItemIndex(player.SWITCHBOT, 0) <= 0:
			chat.AppendChat(1, localeInfo.SWITCHBOT_TEXT_01)
			return False

		if self.func_count_select_bonus() <= 0:
			chat.AppendChat(1, localeInfo.SWITCHBOT_TEXT_02)
			return False

		if self.func_count_select_bonus() != self.func_count_select_value():
			chat.AppendChat(1, localeInfo.SWITCHBOT_TEXT_03)
			return False

		if self.func_repeat_bonus() == 1:
			chat.AppendChat(1, localeInfo.SWITCHBOT_TEXT_04)
			return False

		return True

	def func_get_list_bonus(self):
		return self.elements["list_bonus"]

	def func_get_id_select_bonus(self,index):
		return self.elements["id_select_bonus_%d"%index]

	def func_get_id_select_value(self,index):
		return self.elements["id_select_value_%d"%index]

	def func_get_list_bonus_select(self):
		list_bonus = []
		for i in xrange(0,MAX_BONUS):
			get_list_bonus = self.func_get_list_bonus()
			get_select_bonus_id = self.func_get_id_select_bonus(i)
			get_select_value_id = self.func_get_id_select_value(i)
				
			if get_select_bonus_id >= 0:
				type = get_list_bonus[get_select_bonus_id][0]
				value = get_list_bonus[get_select_bonus_id][1][get_select_value_id]
				list_bonus.append([type,value])
			else:
				list_bonus.append([0,0])

		return list_bonus

	def func_get_list_bonus_id_select(self):
		list_id = []
		for i in xrange(0,MAX_BONUS):
			get_list_bonus = self.func_get_list_bonus()
			get_select_bonus_id = self.func_get_id_select_bonus(i)
			get_select_value_id = self.func_get_id_select_value(i)
				
			if get_select_bonus_id >= 0:
				type = get_list_bonus[get_select_bonus_id][0]
				list_id.append([get_select_bonus_id,get_select_value_id])
			else:
				list_id.append([-1,-1])

		return list_id

	def SetNameBonusSlot(self,index,id_select,name):
		self.elements["bonus_text_%d"%index].SetText(name)
		self.elements["id_select_bonus_%d"%index] = id_select

	def ResetNameBonus(self,index):
		self.elements["bonus_text_%d"%index].SetText(".")
		self.elements["id_select_bonus_%d"%index] = -1

	def ResetValueBonus(self,index):
		self.elements["value_text_%d"%index].SetText("0")
		self.elements["id_select_value_%d"%index] = -1
	
	def SetValueBonusSlot(self,index,id_select,value):

		name = self.get_affect[self.elements["list_bonus"][self.elements["id_select_bonus_%d"%index]][0]](int(value))
		self.SetNameBonusSlot(index,self.elements["id_select_bonus_%d"%index],name)

		self.elements["value_text_%d"%index].SetText(value)
		self.elements["id_select_value_%d"%index] = id_select

	def __OnSelectEmptySlot(self, selectedSlotPos):
		isAttached = mouseModule.mouseController.isAttached()
		if isAttached:
			attachedSlotType = mouseModule.mouseController.GetAttachedType()
			attachedSlotPos = mouseModule.mouseController.GetAttachedSlotNumber()
			mouseModule.mouseController.DeattachObject()
			itemIndex = player.GetItemIndex(attachedSlotPos)
			itemCount = player.GetItemCount(attachedSlotPos)

			item.SelectItem(itemIndex)
			itemType = item.GetItemType()

			if item.ITEM_TYPE_WEAPON == itemType or item.ITEM_TYPE_ARMOR == itemType :
				if player.SLOT_TYPE_INVENTORY == attachedSlotType:
					attachedCount = mouseModule.mouseController.GetAttachedItemCount()
					net.SendItemMovePacket(player.INVENTORY, attachedSlotPos, player.SWITCHBOT, 0, attachedCount)

	def __OnSelectItemSlot(self, selectedSlotPos):
		isAttached = mouseModule.mouseController.isAttached()
		if isAttached:
			attachedSlotType = mouseModule.mouseController.GetAttachedType()
			attachedSlotPos = mouseModule.mouseController.GetAttachedSlotNumber()
			mouseModule.mouseController.DeattachObject()
			itemIndex = player.GetItemIndex(attachedSlotPos)
			itemCount = player.GetItemCount(attachedSlotPos)

			item.SelectItem(itemIndex)
			itemType = item.GetItemType()

			if item.ITEM_TYPE_WEAPON == itemType or item.ITEM_TYPE_ARMOR == itemType :
				if player.SLOT_TYPE_INVENTORY == attachedSlotType:
					attachedCount = mouseModule.mouseController.GetAttachedItemCount()
					net.SendItemMovePacket(player.INVENTORY, attachedSlotPos, player.SWITCHBOT, 0, attachedCount)

		else:
			if selectedSlotPos > 0:
				return

			itemVnum = player.GetItemIndex(player.SWITCHBOT, 0)
			itemCount = player.GetItemCount(player.SWITCHBOT, 0)
			mouseModule.mouseController.AttachObject(self, player.SLOT_TYPE_SWITCHBOT, 0, itemVnum, itemCount)


	def SelectBonus(self,index):
		list_bonus_element = self.elements["list_bonus_%d"%index]
			

		if list_bonus_element:
			if list_bonus_element.IsOpen():
				list_bonus_element.Close()
			else:
				self.CloseListBonusAll()

				if len(self.elements["list_bonus"]) <= 0:
					return

				if self.func_max_select_bonus() and list_bonus_element.GetId() == -1:
					return

				list_bonus_element.Show()

				for i in xrange(0,len(self.elements["list_bonus"])):
					name = self.get_affect[self.elements["list_bonus"][i][0]](0)
					#replace = ["+","0","%"]
					#for x in replace:
						#name = name.replace(x,"")
					list_bonus_element.InsertBonus(i,name)

	def SelectValue(self,index):
		list_value_element = self.elements["list_value_%d"%index]
		list_bonus_element = self.elements["list_bonus_%d"%index]

		if list_value_element:
			if list_value_element.IsOpen():
				list_value_element.Close()
			else:
				self.CloseListBonusAll()

				if list_bonus_element.GetId() == -1:
					return

				list_value_element.Show()

				for i in xrange(0,len(self.elements["list_bonus"][list_bonus_element.GetId()][1])):
					list_value_element.InsertBonus(i,str(self.elements["list_bonus"][list_bonus_element.GetId()][1][i]))

	def SwitchBotListSelect(self, item):
		self.selectedItem = item

		if self.selectedItem:
			self.selectedItem.Select()


	def ResetBonus(self,index):
		self.ResetValueBonus(index)
		self.ResetNameBonus(index)

		list_bonus_element = self.elements["list_bonus_%d"%index]
		list_value_element = self.elements["list_value_%d"%index]

		if list_bonus_element:
			list_bonus_element.ResetAll()

		if list_value_element:
			list_value_element.ResetAll()

	def CloseListBonusAll(self):
		for i in xrange(0,MAX_BONUS):
			list_bonus_element = self.elements["list_bonus_%d"%i]
			list_value_element = self.elements["list_value_%d"%i]

			if list_bonus_element:
				list_bonus_element.Close()

			if list_value_element:
				list_value_element.Close()


	def ChangeBonus(self):

		if self.func_check_change():
			list_bonus = self.func_get_list_bonus_select()

			self.accept_message.SetText1(localeInfo.SWITCHBOT_TEXT_06)
			self.accept_message.SetText2(localeInfo.SWITCHBOT_TEXT_07)
			self.accept_message.SetAcceptEvent(lambda arg=TRUE,  bonus  = list_bonus: self.AcceptChangeBonus(arg,bonus))
			self.accept_message.SetCancelEvent(lambda arg=FALSE, bonus  = list_bonus: self.AcceptChangeBonus(arg,bonus))
			self.accept_message.Open()		

	def AcceptChangeBonus(self,arg,list_bonus):
		self.accept_message.Close()
		if arg:
			net.SBChange(list_bonus)

	def RefreshItemSlot(self):
		itemIndex = player.GetItemIndex(player.SWITCHBOT, 0)
		itemCount = player.GetItemCount(player.SWITCHBOT, 0)

		self.slot_item.SetItemSlot(0, itemIndex, itemCount)

		if itemIndex > 0:
			self.func_add_change_item()
		else:
			self.slot_item.ClearSlot(1)

		self.slot_item.RefreshSlot()

	def SelectPresets(self,index,index1,name):
		if player.GetItemIndex(player.SWITCHBOT, 0) <= 0:
			return

		for i in xrange(0,MAX_BONUS):
			self.ResetBonus(i)

		dict = self.elements["save_bonus"].get(index1, None)
		for bonus_dict in xrange(0,len(dict["bonus"])):
			(type,value) 				 = dict["bonus"][bonus_dict]
			(id_select_b,id_select_v)    = dict["id"][bonus_dict]
			if type > 0:
				list_bonus_element = self.elements["list_bonus_%d"%bonus_dict]

				self.SetNameBonusSlot(bonus_dict,id_select_b,self.get_affect[type](0))
				list_bonus_element.SetId(id_select_b)

				self.SetValueBonusSlot(bonus_dict,id_select_v,str(value))

		self.elements["select_presets"] = index1

		for i in xrange(MAX_SAVE):
			self.elements["slot_save_%d"%i].SetUp()

		self.ClickRadioButton(index,index1)

	def ClickRadioButton(self,index,index1):
		if self.elements["select_presets"] == index1:
			self.elements["slot_save_%d"%index].Down()
		else:
			self.elements["slot_save_%d"%index].SetUp()

	def RefreshPresets(self):
		self.ScollPos = int(self.scrollbar.GetPos() * self.Diff)

		if self.ScollPos < 0:
			return

		for i in xrange(MAX_SAVE):
			idx = i + self.ScollPos
			if idx < len(self.elements["save_bonus"]):
				count = 0
				for index_s in self.elements["save_bonus"].iterkeys():
					dict = self.elements["save_bonus"].get(index_s, None)
					if not dict:
						continue
					name = dict["name"]
					if idx == count:
						self.ShowPresets(i,index_s,name)
						self.ClickRadioButton(i,index_s)
					count +=1
			else:
				self.EmptyPresets(i)


	def ShowPresets(self, index, index1, name):
		if(index < MAX_SAVE):
			self.elements["slot_save_%d"%index].Show()
			self.elements["button_delete_save_%d"%index].Show()
			self.elements["bonus_save_text_%d"%index].SetText(name)


			self.elements["button_delete_save_%d"%index].SetEvent(self.DeletePresets,index1)
			self.elements["slot_save_%d"%index].SetEvent(self.SelectPresets,index,index1,name)

	def EmptyPresets(self, index):
		if(index < MAX_SAVE):
			self.elements["slot_save_%d"%index].Hide()
			self.elements["button_delete_save_%d"%index].Hide()

	def GetCountListSave(self):
		count = 0
		while self.elements["save_bonus"].has_key(count):
			count += 1
			
		return count

	def SavePresets(self):
		if player.GetItemIndex(player.SWITCHBOT, 0) <= 0:
			return

		name_presets = uiCommon.InputDialog()
		name_presets.SetTitle(localeInfo.SWITCHBOT_TEXT_05)
		name_presets.SetAcceptEvent(ui.__mem_func__(self.OnAddPresets))
		name_presets.SetCancelEvent(ui.__mem_func__(self.OnCancelAddPresets))
		name_presets.Open()
		self.name_presets = name_presets

	def OnAddPresets(self):
		text = self.name_presets.GetText()
		if text:
			bonus = self.func_get_list_bonus_select()
			get_id = self.func_get_list_bonus_id_select()
			new_dict = {
				"name" 	: text,
				"bonus" : bonus,
				"id"	: get_id,
			}

			self.elements["save_bonus"][self.GetCountListSave()] = new_dict
			self.SaveDictPresets()

		self.OnCancelAddPresets()

	def DeletePresets(self,index):
		dict = self.elements["save_bonus"].get(index, None)
		if not dict:
			return

		del self.elements["save_bonus"][index]

		self.elements["select_presets"] = -1

		self.SaveDictPresets()


	def SaveDictPresets(self):
		with old_open('switchbot.wa', 'wb') as f:
			pickle.dump(self.elements["save_bonus"], f)

		self.LoadPresets()
		self.RefreshPresets()

	def OnCancelAddPresets(self):
		self.name_presets.Close()
		self.name_presets = None
		return True

	def AdjustPositionAndSize(self):

		for i in xrange(0,MAX_BONUS):
			list_bonus_element = self.elements["list_bonus_%d"%i]
			list_value_element = self.elements["list_value_%d"%i]

			if list_bonus_element:
				list_bonus_element.AdjustPositionAndSize()

			if list_value_element:
				list_value_element.AdjustPositionAndSize()


	def OverInItem(self,index):
		if index == 0:
			self.toolTip.ClearToolTip()
			self.toolTip.SetInventoryItem(index,player.SWITCHBOT)

	def OverOutItem(self):
		self.toolTip.HideToolTip()


	def OnMoveWindow(self, x, y):
		self.AdjustPositionAndSize()

	def Close(self):
		self.func_clear_bonus_item()
		net.SBClose()
		wndMgr.Hide(self.hWnd)
		
	def OnPressEscapeKey(self):
		self.Close()
		return TRUE