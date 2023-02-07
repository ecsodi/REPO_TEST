import thenewui as ui
import wndMgr
import renderTarget
import player
import item
import app
import constInfo
import chat

class RenderTarget(ui.ScriptWindow):
	RENDER_TARGET_INDEX = 66
	Window = None

	def __init__(self):
		ui.ScriptWindow.__init__(self)

		self.curRot = 0.0
		self.max_pos_x = wndMgr.GetScreenWidth()
		self.max_pos_y = wndMgr.GetScreenHeight()

		self.emotionTime = 0
		self.refreshTime = 0

		self.Initialize()
		self.Init()

	def Initialize(self):
		self.interface = None

	@staticmethod
	def Get():
		if RenderTarget.Window == None:
			RenderTarget.Window = RenderTarget()

		return RenderTarget.Window

	def __del__(self):
		ui.ScriptWindow.__del__(self)
		self.Initialize()

	def DisplayUser(self, vRace=0, refresh=False, vItemWeapon=0, vItemArmor=0, vItemHair=0, vItemSash=0, vItemCrown = 0):
		if refresh:
			self.refreshTime = app.GetTime()
			return

		renderTarget.SetVisibility(self.RENDER_TARGET_INDEX, True)
		renderTarget.SelectModel(self.RENDER_TARGET_INDEX, vRace)
		renderTarget.ChangeEffect(self.RENDER_TARGET_INDEX)
		
		if vRace > 8:
			return

		playerRace = player.GetRace() # Get player race

		########## IF SELECTED FROM INVENTORY ELSE GET EQUIPPED ITEM DATA ##########
		# Weapon / Costume
		if vItemWeapon != 0:
			renderTarget.SetWeapon(self.RENDER_TARGET_INDEX, vItemWeapon)
		else:
			if playerRace == vRace:
				if app.ENABLE_COSTUME_WEAPON_SYSTEM and player.GetItemIndex(item.COSTUME_SLOT_WEAPON) != 0:
					weaponVnum = player.GetItemIndex(item.COSTUME_SLOT_WEAPON)
				else:
					weaponVnum = player.GetItemIndex(item.EQUIPMENT_WEAPON)

				renderTarget.SetWeapon(self.RENDER_TARGET_INDEX, weaponVnum)

		# Armor / Costume
		if vItemArmor != 0:
			renderTarget.SetArmor(self.RENDER_TARGET_INDEX, vItemArmor)
		else:
			if playerRace == vRace:
				if player.GetItemIndex(item.COSTUME_SLOT_BODY) != 0:
					armorVnum = player.GetItemIndex(item.COSTUME_SLOT_BODY)
				else:
					armorVnum = player.GetItemIndex(item.EQUIPMENT_BODY)

				renderTarget.SetArmor(self.RENDER_TARGET_INDEX, armorVnum)

		# Hair
		if vItemHair != 0:
			renderTarget.SetHair(self.RENDER_TARGET_INDEX, vItemHair)
		else:
			if playerRace == vRace:
				if player.GetItemIndex(item.COSTUME_SLOT_HAIR) != 0:
					item.SelectItem(player.GetItemIndex(item.COSTUME_SLOT_HAIR))
					renderTarget.SetHair(self.RENDER_TARGET_INDEX, item.GetValue(3))

		if app.ENABLE_SASH_SYSTEM:
			if vItemSash != 0:
				renderTarget.SetSash(self.RENDER_TARGET_INDEX, vItemSash - 85000)
			else:
				if playerRace == vRace:
					if player.GetItemIndex(1028) != 0:
					# if player.GetItemIndex(item.COSTUME_SLOT_SASH) != 0:
						renderTarget.SetSash(self.RENDER_TARGET_INDEX, player.GetItemIndex(1028)  - 85000)
					# elif player.GetItemIndex(1028) != 0:
					else:
						renderTarget.SetSash(self.RENDER_TARGET_INDEX, player.GetItemIndex(item.COSTUME_SLOT_SASH)  - 85000)

		if vItemCrown != 0:
			renderTarget.SetCrown(self.RENDER_TARGET_INDEX, vItemCrown)
		else:
			if playerRace == vRace:
				if player.GetItemIndex(1024) != 0:
					item.SelectItem(player.GetItemIndex(1024))
					renderTarget.SetCrown(self.RENDER_TARGET_INDEX, item.GetValue(2))

	def Init(self):
		try:
			pyScrLoader = ui.PythonScriptLoader()
			pyScrLoader.LoadScriptFile(self, "uiscript/ModelPreviewWindow.py")
		except:
			import exception
			exception.Abort("RenderTargetWindow.LoadDialog.LoadScript")

		try:
			self.titleBar = self.GetChild("TitleBar")
			self.titleBar.CloseButton("show")
			self.titleBar.SetCloseEvent(self.Close)

			self.board = self.GetChild("Board")

			self.RenderTarget = self.GetChild("RenderTarget")
			self.SetCenterPosition()

		except:
			import exception
			exception.Abort("RenderTargetWindow.LoadDialog.BindObject")

		renderTarget.SetBackground(self.RENDER_TARGET_INDEX, "d:/ymir work/ui/game/myshop_deco/model_view_bg.sub")

	def BindInterface(self, interface):
		self.interface = interface

	def Destroy(self):
		self.Close()
		self.Initialize()

	def Close(self):
		self.Hide()

	def Open(self):
		self.Show()
		self.SetTop()
		renderTarget.SetAutoRotate(self.RENDER_TARGET_INDEX, False)

	def OnPressEscapeKey(self):
		self.Close()
		return True

	def MINMAX(self, min, value, max):
		if value < min:
			return min
		elif value > max:
			return max
		else:
			return value

	def UpdateEquipment(self):
		# renderTarget.RefreshRender(self.RENDER_TARGET_INDEX, 0)
		self.DisplayUser(player.GetRace())

	def OnUpdate(self):
		x, y = self.GetGlobalPosition()
		pos_x = self.MINMAX(0, x, self.max_pos_x)
		pos_y = self.MINMAX(0, y, self.max_pos_y)
		self.SetPosition(pos_x, pos_y)

		if self.refreshTime != 0 and app.GetTime() - self.refreshTime > 0.2:
			self.UpdateEquipment()
			self.refreshTime = 0

		if self.emotionTime != 0 and app.GetTime() - self.emotionTime > 5.0:
			self.UpdateEquipment()
			self.emotionTime = 0

	def __ResetSettings(self):
		self.curRot = 0.0
		renderTarget.ResetSettings(self.RENDER_TARGET_INDEX)

	def AdjustPosition(self):
		if self.interface and self.interface.wndInventory and self.interface.wndInventory.GetGlobalPosition():
			x, y = self.interface.wndInventory.GetGlobalPosition()
			self.SetPosition(x - 210, y + 210)
