import thenewui as ui
import CacheEffect as player
import grp, wndMgr, item, constInfo, net, localeInfo, chat, cfg

IMG_DIR = "d:/ymir work/ui/game/reward_info/"
IMG_ICON_DIR = "d:/ymir work/ui/game/reward_info/icons/"

REWORK_DIR = "rewards/"

reward_info = {
	# eventName, eventImgFolder, [items]
	player.REWARD_NINJA_105 : [localeInfo.REWARD_NINJA_105, "ninja_105",[ [91111,1] ] ],
	player.REWARD_WAR_105 : [localeInfo.REWARD_WAR_105, "warrior_105",[ [91112,1] ] ],
	player.REWARD_SURA_105 : [localeInfo.REWARD_SURA_105, "sura_105",[ [91113,1] ] ],
	player.REWARD_SHAMAN_105 : [localeInfo.REWARD_SHAMAN_105, "saman_105",[ [91114,1] ] ],
	player.REWARD_LYCAN_105 : [localeInfo.REWARD_LYCAN_105, "lycan_105",[ [91115,1] ] ],
	player.REWARD_AVERAGE : [localeInfo.REWARD_AVERAGE, "prima_arma_75",[ [61024,1] ] ],
	player.REWARD_FIRST_CRAFT : [localeInfo.REWARD_FIRST_CRAFT, "primul_craft",[ [80017,10] ] ],
	player.REWARD_FIRST_TRANSMUTATIO : [localeInfo.REWARD_FIRST_TRANSMUTATIO, "prima_transmutare",[ [80017,10] ] ],
	# player.REWARD_FIRST_DSS_LEGENDARY : [localeInfo.REWARD_FIRST_DSS_LEGENDARY, "prima_alchimie",[ [80017,20] ] ],
	player.REWARD_FIRST_FINISHED_BIOLOG : [localeInfo.REWARD_FIRST_FINISHED_BIOLOG, "primul_biolog_terminat",[ [8779,1] ] ],
	player.REWARD_FIRST_MAX_PET : [localeInfo.REWARD_FIRST_MAX_PET, "primul_insotitor",[ [8780,1] ] ],
	player.REWARD_FIRST_LV100_ARMOR : [localeInfo.REWARD_FIRST_LV100_ARMOR, "prima_armura_beta",[ [8776,1] ] ],
	player.REWARD_FIRST_LV100_WEAPON : [localeInfo.REWARD_FIRST_LV100_WEAPON, "prima_arma_beta",[ [8775,1] ] ],
	player.REWARD_FIRST_FULL_REFINED : [localeInfo.REWARD_FIRST_FULL_REFINED, "primul_obiect_9",[ [80017,10] ] ],
	player.REWARD_FIRST_MONKEY_DUNG : [localeInfo.REWARD_FIRST_MONKEY_DUNG, "maimuta_lord",[ [80017,10] ] ],
	player.REWARD_FIRST_ORK_DUNG : [localeInfo.REWARD_FIRST_ORK_DUNG, "primul_orc",[ [80017,10] ] ],
	player.REWARD_FIRST_SPIDER_DUNG : [localeInfo.REWARD_FIRST_SPIDER_DUNG, "prima_baroneasa",[ [80017,10] ] ],
	player.REWARD_FIRST_DT_DUNG : [localeInfo.REWARD_FIRST_DT_DUNG, "primul_reaper",[ [80017,10] ] ],
	player.REWARD_FIRST_AZRAEL_DUNG : [localeInfo.REWARD_FIRST_AZRAEL_DUNG, "primul_azrael",[ [80017,10] ] ],
	player.REWARD_FIRST_DRAGON_DUNG : [localeInfo.REWARD_FIRST_DRAGON_DUNG, "primul_dragon",[ [80017,10] ] ],
	player.REWARD_FIRST_RAZADOR_DUNG : [localeInfo.REWARD_FIRST_RAZADOR_DUNG, "primul_razador",[ [80017,20] ] ],
	player.REWARD_FIRST_NEMERE_DUNG : [localeInfo.REWARD_FIRST_NEMERE_DUNG, "primul_nemere",[ [80017,20] ] ],
	player.REWARD_FIRST_METIN_LV100 : [localeInfo.REWARD_FIRST_METIN_LV100, "primul_metin_de_105",[ [80017,5] ] ],
	player.REWARD_FIRST_BOSS_LV100 : [localeInfo.REWARD_FIRST_BOSS_LV100, "primul_boss_beta",[ [80017,10] ] ],
	player.REWARD_FIRST_CALL_SERVER : [localeInfo.REWARD_FIRST_CALL_SERVER, "primul_striga",[ [80017,1] ] ],
	player.REWARD_FIRST_LV99 : [localeInfo.REWARD_FIRST_LV99, "level_99",[ [80017,20] ] ],
	player.REWARD_FIRST_ABSORBTION : [localeInfo.REWARD_FIRST_ABSORBTION, "prima_absorbtie",[ [80017,20] ] ],
	player.REWARD_FIRST_BATTLEPASS : [localeInfo.REWARD_FIRST_BATTLEPASS, "primul_emperor",[ [80017,20] ] ],
	player.REWARD_FIRST_CUSTOM_SASH : [localeInfo.REWARD_FIRST_CUSTOM_SASH, "esarfa_25",[ [61025,1] ] ],

	# player.REWARD_PET_115 : [localeInfo.REWARD_PET_115, "pet_115",[ [4399,1] ] ],
	# player.REWARD_120 : [localeInfo.REWARD_120, "lvl_120",[ [4399,1] ] ],
	# player.REWARD_LEGENDARY_SKILL : [localeInfo.REWARD_LEGENDARY_SKILL, "legendary_skill",[ [4399,1] ] ],
	# player.REWARD_LEGENDARY_SKILL_SET : [localeInfo.REWARD_LEGENDARY_SKILL_SET, "legendary_skill_set",[ [4399,1] ] ],
	# player.REWARD_THANDRUIL : [localeInfo.REWARD_THANDRUIL, "thranduil",[ [4399,1] ] ],
	# player.REWARD_HYDRA : [localeInfo.REWARD_HYDRA, "hydra",[ [4399,1] ] ],
	# player.REWARD_CRYSTAL_DRAGON : [localeInfo.REWARD_CRYSTAL_DRAGON, "crystal_dragon",[ [4399,1] ] ],
	# player.REWARD_OFFLINESHOP_SLOT : [localeInfo.REWARD_OFFLINESHOP_SLOT, "offlineshop_slot",[ [4399,1] ] ],
	# player.REWARD_INVENTORY_SLOT : [localeInfo.REWARD_INVENTORY_SLOT, "inventory_slot",[ [4399,1] ] ],
	# player.REWARD_AVERAGE : [localeInfo.REWARD_AVERAGE, "average",[ [4399,1] ] ],
	# player.REWARD_ELEMENT : [localeInfo.REWARD_ELEMENT, "element",[ [4399,1] ] ],
	# player.REWARD_BATTLEPASS : [localeInfo.REWARD_BATTLEPASS, "battlepass",[ [4399,1] ] ],
	# player.REWARD_CUSTOM_SASH : [localeInfo.REWARD_CUSTOM_SASH, "self_sash",[ [4399,1] ] ],
	# player.REWARD_AURA : [localeInfo.REWARD_AURA, "aura",[ [4399,1] ] ],
	# player.REWARD_ENERGY : [localeInfo.REWARD_ENERGY, "energy_crystal",[ [4399,1] ] ],
	# player.REWARD_112_BIO : [localeInfo.REWARD_112_BIO, "112_bio",[ [4399,1] ] ],
	# player.REWARD_120_BIO : [localeInfo.REWARD_120_BIO, "120_bio",[ [4399,1] ] ],
	# player.REWARD_LEADER_SHIP : [localeInfo.REWARD_LEADER_SHIP, "leadership",[ [4399,1] ] ],
	# player.REWARD_BUFFI_LEGENDARY_SKILL : [localeInfo.REWARD_BUFFI_LEGENDARY_SKILL, "buffi_shaman",[ [4399,1] ] ],
}

class RewardWindow(ui.BoardWithTitleBar):
	class RewardItem(ui.Window):
		def Destroy(self):
			self.children = {}
			self.rewardIndex = 0
			self.IsPlayerTrue = None
			self.rewardPlayer = None

		def __del__(self):
			ui.Window.__del__(self)
			
		def __init__(self):
			ui.Window.__init__(self)
			self.background = None
			
			self.background = ui.ExpandedImageBox()
			self.background.SetParent(self)
			self.background.LoadImage(REWORK_DIR+"finished.png")
			self.background.Show()
			
			self.SetSize(self.background.GetWidth(), self.background.GetHeight())

			self.Destroy()

		def LoadReward(self, rewardIndex, rewardData):
			self.rewardIndex = rewardIndex

			rewardImage = ui.ImageBox()
			rewardImage.SetParent(self)
			rewardImage.LoadImage(IMG_ICON_DIR+rewardData[1]+".tga")
			rewardImage.SetPosition(8,10)
			rewardImage.Show()
			self.children["rewardImage"] = rewardImage

			rewardName = ui.TextLine()
			rewardName.SetParent(self)
			rewardName.SetHorizontalAlignLeft()
			rewardName.SetText(rewardData[0])
			rewardName.SetPosition(130,58)
			rewardName.SetPackedFontColor(grp.GenerateColor(0.471,0.471,0.471, 1.0))
			rewardName.Show()
			self.children["rewardName"] = rewardName

			self.GridRewardImage = ui.ImageBox()
			self.GridRewardImage.SetParent(self)
			self.GridRewardImage.LoadImage(REWORK_DIR + "not_finish_slot.png")
			self.GridRewardImage.SetPosition(430, 18)
			self.GridRewardImage.Show()
			
			self.rewardPlayer = ui.TextLine()
			self.rewardPlayer.SetParent(self)
			self.rewardPlayer.SetHorizontalAlignLeft()
			self.rewardPlayer.SetPosition(130,27)
			self.rewardPlayer.Show()

			rewardItems = ui.GridSlotWindow()
			rewardItems.SetParent(self.GridRewardImage)
			rewardItems.SetPosition(50, 12)
			rewardItems.SetSlotStyle(wndMgr.SLOT_STYLE_NONE)
			rewardItems.SetOverInItemEvent(ui.__mem_func__(self.OverInItem))
			rewardItems.SetOverOutItemEvent(ui.__mem_func__(self.OverOutItem))
			rewardItems.ArrangeSlot(0, 1, 1, 32, 32, 0, 0)
			for rewardItem in rewardData[2]:
				(itemVnum,itemCount) = (rewardItem[0],rewardItem[1])
				item.SelectItem(itemVnum)
				(width,height) = item.GetItemSize()
				rewardItems.SetItemSlot(0, itemVnum, itemCount)
			rewardItems.RefreshSlot()
			rewardItems.Show()
			self.children["rewardItems"] = rewardItems
						
		def OverInItem(self, index):
			interface = constInfo.GetInterfaceInstance()
			if interface:
				if interface.tooltipItem:
					interface.tooltipItem.SetItemToolTip(reward_info[self.rewardIndex][2][index][0])

		def OverOutItem(self):
			interface = constInfo.GetInterfaceInstance()
			if interface:
				if interface.tooltipItem:
					interface.tooltipItem.HideToolTip()

		def SetRewardPlayer(self, playerName):
			self.IsPlayerTrue = playerName

		def OnUpdate(self):
			if self.IsPlayerTrue == None:
				self.background.LoadImage(REWORK_DIR+"not_finished.png")
				self.GridRewardImage.LoadImage(REWORK_DIR+"not_finish_slot.png")
				self.rewardPlayer.SetPackedFontColor(grp.GenerateColor(0.584,0.153,0.153, 1.0))
				self.rewardPlayer.SetText("Nu a fost completat.")
			else:
				self.background.LoadImage(REWORK_DIR+"finished.png")
				self.GridRewardImage.LoadImage(REWORK_DIR+"finish_slot.png")
				self.rewardPlayer.SetText(self.IsPlayerTrue)
				self.rewardPlayer.SetPackedFontColor(grp.GenerateColor(0.369,0.698,0.208, 1.0))

	def Destroy(self):
		self.ListBox = None
		self.boardImage = None
		self.isFirstOpen = False
		
	def __del__(self):
		ui.BoardWithTitleBar.__del__(self)
		
	def __init__(self):
		ui.BoardWithTitleBar.__init__(self)
		self.Destroy()
		self.LoadWindow()
		
	def LoadWindow(self):
		self.SetSize(630, 560)
		self.AddFlag("animation")
		self.AddFlag("movable")
		self.AddFlag("attach")
		self.AddFlag("float")
		self.SetTitleName(localeInfo.REWARD_WINDOW_TITLE)
		self.SetCloseEvent(self.Close)
		self.SetCenterPosition()
		
		bannerImage = ui.ImageBox()
		bannerImage.SetParent(self)
		bannerImage.SetPosition(8, 30)
		bannerImage.AddFlag("not_pick")
		bannerImage.LoadImage(REWORK_DIR + "banner.png")
		bannerImage.Show()
		self.bannerImage = bannerImage
		
		boardImage = ui.ImageBox()
		boardImage.SetParent(self)
		boardImage.SetPosition(8, 135)
		boardImage.AddFlag("not_pick")
		boardImage.LoadImage(REWORK_DIR + "border.png")
		boardImage.Show()
		self.boardImage = boardImage

		ListBox = ui.ListBoxEx()
		ListBox.SetParent(boardImage)
		ListBox.SetPosition(10,4)
		ListBox.SetSize(boardImage.GetWidth(), boardImage.GetHeight())
		ListBox.AddFlag("not_pick")
		ListBox.SetViewItemCount(4)
		ListBox.SetItemSize(520, 81)
		ListBox.SetItemStep(102)
		ListBox.Show()
		self.ListBox = ListBox

		scrollBar = ui.ScrollBar()
		scrollBar.SetParent(boardImage)
		scrollBar.SetPosition(598, 5)
		scrollBar.SetScrollBarSize(boardImage.GetHeight() - 10)
		scrollBar.SetScrollStep(0.05)
		scrollBar.Show()
		self.scrollBar = scrollBar

		ListBox.SetScrollBar(scrollBar)
		self.LoadRewards()

	def SetRewardPlayers(self, data):
		if len(data) > 0:
			splitRewards = data[:len(data)-1].split("#")
			for reward in splitRewards:
				rewardList = reward.split("|")
				if len(rewardList) == 2:
					listBoxData = self.ListBox.itemList
					for listboxItem in listBoxData:
						(rewardIndex,playerName) = (int(rewardList[0]),str(rewardList[1]))
						if playerName.isspace() or playerName == "" or playerName== " ":
							playerName = ""
						if listboxItem.rewardIndex == rewardIndex:
							listboxItem.SetRewardPlayer(playerName)
							break
	def LoadRewards(self):
		for key, data in reward_info.items():
			rewardItem = self.RewardItem()
			rewardItem.LoadReward(key, data)
			self.ListBox.AppendItem(rewardItem)
	
	def OnRunMouseWheel(self, nLen):
		if nLen > 0:
			self.scrollBar.OnUp()
		else:
			self.scrollBar.OnDown()

	def Close(self):
		self.Hide()
		
	def Open(self):
		if self.isFirstOpen == False:
			net.SendChatPacket("/update_reward_data")
			self.isFirstOpen = True
		self.Show()
		
	def OnPressEscapeKey(self):
		self.Close()
		return True


