import constInfo
import systemSetting
import wndMgr
import chat
import app
import CacheEffect as player
import Collision as chr
import uiTaskBar
import uiCharacter
import uiInventory
import uiChat
import uiMessenger
import guild
import thenewui as ui
import uiWhisper
import uiPointReset
import uiShop
import uiExchange
import uiSystem
import uiRestart
import uiToolTip
import uiMiniMap
import uiParty
import uiSafebox
import net
import uiGuild
import uiQuest
import uiPrivateShopBuilder
import uiCommon
import uiRefine
import uiRefineRenewal
import uiEquipmentDialog
import uiGameButton
import uiTip
import grp
import uicuberenewal
import miniMap
import background
import uiselectitem
import uiScriptLocale
import event
import localeInfo
import uiMiniGame
import uichestview
import uiextendinventory
import uiDragonSoul
import uibiolog
import uigaya
import uiwiky_ful
import uidungeoninfo
import uirankinfo
import operator
import uiChooseEmoticon
import uiTabMap
import uiRemoteShop
import uiBattlePass
import uiwheeloffright
import uiletterevent_g
import uiPremiumPanel
# import uinewnotifs
import uishout

if app.ENABLE_MINIGAME_RUMI_EVENT:
	import uiCards
if app.ENABLE_SASH_SYSTEM:
	import uisash
if app.ENABLE_COSTUME_SYSTEM:
	import renderTargetExtension
if app.ENABLE_INVENTORY_VIEWER:
	import uiInventoryViewer
if app.ENABLE_CHANGELOOK_SYSTEM:
	import uichangelook
if app.ENABLE_SEARCH_SHOP:
	import uiSearchShop
if app.ENABLE_REWARD_SYSTEM:
	import uiReward
if app.ENABLE_EVENT_MANAGER:
	import uiEventCalendar
if app.ENABLE_MAINTENANCE_SYSTEM:
	import uiMaintenance
if app.ENABLE_SWITCHBOT_WORLDARD:
	import uiswtichbot
IsQBHide = 0
IsWisperHide = 0

class Interface(object):
	CHARACTER_STATUS_TAB = 1
	CHARACTER_SKILL_TAB = 2

	def __init__(self):
		systemSetting.SetInterfaceHandler(self)
		self.windowOpenPosition = 0
		if app.WJ_ENABLE_TRADABLE_ICON:
			self.onTopWindow = player.ON_TOP_WND_NONE
		self.dlgWhisperWithoutTarget = None
		self.inputDialog = None
		self.tipBoard = None
		self.bigBoard = None
		self.mallPageDlg = None
		self.wndTaskBar = None
		self.wndCharacter = None
		self.wndInventory = None
		self.wndExpandedTaskBar = None
		self.wndChat = None
		self.wndMessenger = None
		self.wndMiniMap = None
		self.wndGuild = None
		self.wndCube = None
		self.wndGuildBuilding = None
		self.wndChangeEmoticon = None
		self.wndTabMap = None
		self.wndRemoteShop = None
		self.lefttipboard = None
		self.wndWheelOfFright = None
		self.wndLetterEvent = None
		if app.ENABLE_COSTUME_SYSTEM: 
			self.wndTargetRender = None
		if app.ENABLE_SHOW_CHEST_DROP:
			self.dlgChestDrop = None
		if app.ENABLE_INVENTORY_VIEWER:
			self.wndInventory = None
		self.wndCustomInventory = None
		if app.ENABLE_SEARCH_SHOP:
			self.wndSearchShop = None
		if app.ENABLE_REWARD_SYSTEM:
			self.wndReward = None
		if app.ENABLE_EVENT_MANAGER:
			self.wndEventManager = None
			self.wndEventIcon = None
		if app.ENABLE_MAINTENANCE_SYSTEM:
			self.wndMaintenance = None
			
		self.listGMName = {}
		self.wndQuestWindow = {}
		self.wndQuestWindowNewKey = 0
		self.privateShopAdvertisementBoardDict = {}
		self.guildScoreBoardDict = {}
		self.equipmentDialogDict = {}
		
		self.wndBattlePass = None
		self.wndMiniGame = None
		self.miniGameList = []
		self.wndExpandedMoneyTaskBar = None

		self.wndDragonSoul = None
		self.wndDragonSoulRefine = None
			
		event.SetInterfaceWindow(self)

	def __del__(self):
		systemSetting.DestroyInterfaceHandler()
		event.SetInterfaceWindow(None)
		
	def __MakeShoutWindow(self):
		self.wndShout = uishout.ShoutManager()
		self.wndShout.LoadWindow()
		self.wndShout.Hide()
		
	if app.ENABLE_SWITCHBOT_WORLDARD:
		def __MakeSwitchBot(self):
			self.wndSwitchBot = uiswtichbot.UiSwitchBot()
			self.wndSwitchBot.Hide()
			
	################################
	## Make Windows & Dialogs
	def __MakeUICurtain(self):
		wndUICurtain = ui.Bar("TOP_MOST")
		wndUICurtain.SetSize(wndMgr.GetScreenWidth(), wndMgr.GetScreenHeight())
		wndUICurtain.SetColor(0x77000000)
		wndUICurtain.Hide()
		self.wndUICurtain = wndUICurtain

	def __MakeMessengerWindow(self):
		self.wndMessenger = uiMessenger.MessengerWindow()
		self.wndMessenger.BindInterface(self)

		from _weakref import proxy
		self.wndMessenger.SetWhisperButtonEvent(lambda n,i=proxy(self):i.OpenWhisperDialog(n))
		self.wndMessenger.SetGuildButtonEvent(ui.__mem_func__(self.ToggleGuildWindow))

	def __MakeGuildWindow(self):
		self.wndGuild = uiGuild.GuildWindow()

	def __MakeChatWindow(self):

		wndChat = uiChat.ChatWindow()

		wndChat.SetSize(wndChat.CHAT_WINDOW_WIDTH, 0)
		wndChat.SetPosition(wndMgr.GetScreenWidth()/2 - wndChat.CHAT_WINDOW_WIDTH/2, wndMgr.GetScreenHeight() - wndChat.EDIT_LINE_HEIGHT - 37)
		wndChat.SetHeight(200)
		wndChat.Refresh()
		wndChat.Show()

		self.wndChat = wndChat
		self.wndChat.BindInterface(self)
		self.wndChat.SetSendWhisperEvent(ui.__mem_func__(self.OpenWhisperDialogWithoutTarget))
		self.wndChat.SetOpenChatLogEvent(ui.__mem_func__(self.ToggleChatLogWindow))

	def __MakeTaskBar(self):
		wndTaskBar = uiTaskBar.TaskBar()
		wndTaskBar.LoadWindow()
		self.wndTaskBar = wndTaskBar
		self.wndTaskBar.SetToggleButtonEvent(uiTaskBar.TaskBar.BUTTON_CHARACTER, ui.__mem_func__(self.ToggleCharacterWindowStatusPage))
		self.wndTaskBar.SetToggleButtonEvent(uiTaskBar.TaskBar.BUTTON_INVENTORY, ui.__mem_func__(self.ToggleInventoryWindow))
		self.wndTaskBar.SetToggleButtonEvent(uiTaskBar.TaskBar.BUTTON_MESSENGER, ui.__mem_func__(self.ToggleMessenger))
		self.wndTaskBar.SetToggleButtonEvent(uiTaskBar.TaskBar.BUTTON_SYSTEM, ui.__mem_func__(self.ToggleSystemDialog))
		
		self.wndTaskBar.SetToggleButtonEvent(uiTaskBar.TaskBar.BUTTON_OFFLINE_SHOP, ui.__mem_func__(self.OpenMyShop))

		if uiTaskBar.TaskBar.IS_EXPANDED:
			self.wndTaskBar.SetToggleButtonEvent(uiTaskBar.TaskBar.BUTTON_EXPAND, ui.__mem_func__(self.ToggleExpandedButton))
			self.wndExpandedTaskBar = uiTaskBar.ExpandedTaskBar()
			self.wndExpandedTaskBar.LoadWindow()
			self.wndExpandedTaskBar.SetToggleButtonEvent(uiTaskBar.ExpandedTaskBar.BUTTON_DRAGON_SOUL, ui.__mem_func__(self.ToggleDragonSoulWindow))
		else:
			self.wndTaskBar.SetToggleButtonEvent(uiTaskBar.TaskBar.BUTTON_CHAT, ui.__mem_func__(self.ToggleChat))

		self.wndEnergyBar = None
		import app
		if app.ENABLE_ENERGY_SYSTEM:
			wndEnergyBar = uiTaskBar.EnergyBar()
			wndEnergyBar.LoadWindow()
			self.wndEnergyBar = wndEnergyBar
			
		if constInfo.ENABLE_EXPANDED_MONEY_TASKBAR:
			self.wndTaskBar.SetToggleButtonEvent(uiTaskBar.TaskBar.BUTTON_EXPAND_MONEY, ui.__mem_func__(self.ToggleExpandedMoneyButton))
			self.wndExpandedMoneyTaskBar = uiTaskBar.ExpandedMoneyTaskBar()
			self.wndExpandedMoneyTaskBar.LoadWindow()
			if self.wndInventory:
				self.wndInventory.SetExpandedMoneyBar(self.wndExpandedMoneyTaskBar)

	def __MakeParty(self):
		wndParty = uiParty.PartyWindow()
		wndParty.Hide()
		self.wndParty = wndParty

	def __MakeGameButtonWindow(self):
		wndGameButton = uiGameButton.GameButtonWindow()
		wndGameButton.SetTop()
		wndGameButton.Show()
		wndGameButton.SetButtonEvent("STATUS", ui.__mem_func__(self.__OnClickStatusPlusButton))
		wndGameButton.SetButtonEvent("SKILL", ui.__mem_func__(self.__OnClickSkillPlusButton))
		wndGameButton.SetButtonEvent("QUEST", ui.__mem_func__(self.__OnClickQuestButton))
		wndGameButton.SetButtonEvent("BUILD", ui.__mem_func__(self.__OnClickBuildButton))

		self.wndGameButton = wndGameButton

	def __IsChatOpen(self):
		return True

	def __MakeWindows(self):
		wndCharacter = uiCharacter.CharacterWindow()
		wndInventory = uiInventory.InventoryWindow()
		wndInventory.BindInterfaceClass(self)
		if app.ENABLE_INVENTORY_VIEWER:
			wndInventoryViewer = uiInventoryViewer.InventoryWindow()
			wndInventoryViewer.BindInterfaceClass(self)

		wndDragonSoul = uiDragonSoul.DragonSoulWindow()	
		wndDragonSoulRefine = uiDragonSoul.DragonSoulRefineWindow()

		self.wndCustomInventory = uiextendinventory.CustomInventoryWindow()
		self.wndCustomInventory.BindInterfaceClass(self)

		wndMiniMap = uiMiniMap.MiniMap()
		wndSafebox = uiSafebox.SafeboxWindow()
		if app.WJ_ENABLE_TRADABLE_ICON:
			wndSafebox.BindInterface(self)

		wndMall = uiSafebox.MallWindow()
		self.wndMall = wndMall

		wndChatLog = uiChat.ChatLogWindow()
		wndChatLog.BindInterface(self)
	
		self.wndCharacter = wndCharacter
		self.wndInventory = wndInventory
		self.wndDragonSoul = wndDragonSoul
		self.wndDragonSoulRefine = wndDragonSoulRefine
		if app.ENABLE_INVENTORY_VIEWER:
			self.wndInventoryViewer = wndInventoryViewer
		self.wndMiniMap = wndMiniMap
		self.wndSafebox = wndSafebox
		self.wndChatLog = wndChatLog
		self.dlgChestDrop = uichestview.ChestViewWindow()
		if app.ENABLE_COSTUME_SYSTEM: 
			self.wndTargetRender = renderTargetExtension.RenderTarget.Get()
			self.wndTargetRender.BindInterface(self)
			self.wndTargetRender.Hide()
		self.wndChangeEmoticon = uiChooseEmoticon.ChooseEmoticon()
		self.wndTabMap = uiTabMap.TabMapWindow()
		self.wndRemoteShop = uiRemoteShop.RemoteShopWindow()
		
		self.wndMiniGame = uiMiniGame.MiniGameWindow()
		self.wndMiniGame.BindInterface(self)
		
		self.wndDragonSoul.SetDragonSoulRefineWindow(self.wndDragonSoulRefine)
		self.wndDragonSoulRefine.SetInventoryWindows(self.wndInventory, self.wndDragonSoul)
		self.wndDragonSoul.BindInterfaceClass(self)

		self.wndInventory.SetDragonSoulRefineWindow(self.wndDragonSoulRefine)
		if self.wndMiniMap:
			self.wndMiniMap.BindInterface(self)
			
		self.wndWheelOfFright = uiwheeloffright.WheelOfFrightWindow()
		self.wndLetterEvent = uiletterevent_g.LetterEventWindow()

		self.wndGaya = uigaya.GayaWindow()
		self.wndWiki = uiwiky_ful.WikiNewWindow()
		self.wndDungeonInfo = uidungeoninfo.DungeonInfoWindow()
		self.wndRankInfo = uirankinfo.RankInfo()
		self.wndBattlePass = uiBattlePass.BattlePass()

	def __MakeDialogs(self):
		self.dlgExchange = uiExchange.ExchangeDialog()
		if app.WJ_ENABLE_TRADABLE_ICON:
			self.dlgExchange.BindInterface(self)
			self.dlgExchange.SetInven(self.wndInventory)
			self.wndInventory.BindWindow(self.dlgExchange)
		self.dlgExchange.LoadDialog()
		self.dlgExchange.SetCenterPosition()
		self.dlgExchange.Hide()
		self.dlgPointReset = uiPointReset.PointResetDialog()
		self.dlgPointReset.LoadDialog()
		self.dlgPointReset.Hide()

		self.dlgShop = uiShop.ShopDialog()
		if app.WJ_ENABLE_TRADABLE_ICON:
			self.dlgShop.BindInterface(self)
		self.dlgShop.LoadDialog()
		self.dlgShop.Hide()

		self.dlgRestart = uiRestart.RestartDialog()
		self.dlgRestart.LoadDialog()
		self.dlgRestart.Hide()

		self.dlgSystem = uiSystem.SystemDialog()
		self.dlgSystem.BindInterface(self)
		self.dlgSystem.LoadDialog()

		self.dlgSystem.Hide()

		self.dlgPassword = uiSafebox.PasswordDialog()
		self.dlgPassword.Hide()

		self.hyperlinkItemTooltip = uiToolTip.HyperlinkItemToolTip()
		self.hyperlinkItemTooltip.BindInterface(self)
		self.hyperlinkItemTooltip.Hide()

		self.tooltipItem = uiToolTip.ItemToolTip()
		self.tooltipItem.BindInterface(self)
		self.tooltipItem.Hide()

		self.tooltipSkill = uiToolTip.SkillToolTip()
		self.tooltipSkill.Hide()

		self.privateShopBuilder = uiPrivateShopBuilder.PrivateShopBuilder()
		# if app.WJ_ENABLE_TRADABLE_ICON:
			# self.privateShopBuilder.BindInterface(self)
			# self.privateShopBuilder.SetInven(self.wndInventory)
			# self.wndInventory.BindWindow(self.privateShopBuilder)
		self.privateShopBuilder.Hide()

		# self.dlgRefineNew = uiRefine.RefineDialogNew()
		self.dlgRefineNew = uiRefineRenewal.RefineDialogNew()
		
		if app.WJ_ENABLE_TRADABLE_ICON:
			self.dlgRefineNew.SetInven(self.wndInventory)
			self.wndInventory.BindWindow(self.dlgRefineNew)
		self.dlgRefineNew.Hide()

	def __MakeTipBoard(self):
		self.tipBoard = uiTip.TipBoard()
		self.tipBoard.Hide()

		self.bigBoard = uiTip.BigBoard()
		self.bigBoard.Hide()
		
		self.lefttipboard = uiTip.LeftTipBoard()
		self.lefttipboard.BindInterface(self)
		self.lefttipboard.Hide()
		
	def __MakeCubeWindow(self):
		self.wndCube = uicuberenewal.CubeRenewalWindows()
		self.wndCube.Hide()

	if app.ENABLE_SASH_SYSTEM:
		def __MakeSashWindow(self):
			self.wndSashCombine = uisash.CombineWindow()
			self.wndSashCombine.LoadWindow()
			self.wndSashCombine.Hide()
			
			self.wndSashAbsorption = uisash.AbsorbWindow()
			self.wndSashAbsorption.LoadWindow()
			self.wndSashAbsorption.Hide()
			
			if self.wndInventory:
				self.wndInventory.SetSashWindow(self.wndSashCombine, self.wndSashAbsorption)
		
	if app.ENABLE_CHANGELOOK_SYSTEM:
		def __MakeChangeLookWindow(self):
			self.wndChangeLook = uichangelook.Window()
			self.wndChangeLook.LoadWindow()
			self.wndChangeLook.Hide()
			
			if self.wndInventory:
				self.wndInventory.SetChangeLookWindow(self.wndChangeLook)

	if app.ENABLE_MINIGAME_RUMI_EVENT:
		def __MakeCardsInfoWindow(self):
			self.wndCardsInfo = uiCards.CardsInfoWindow()
			self.wndCardsInfo.LoadWindow()
			self.wndCardsInfo.Hide()

		def __MakeCardsWindow(self):
			self.wndCards = uiCards.CardsWindow()
			self.wndCards.LoadWindow()
			self.wndCards.Hide()

		def __MakeCardsIconWindow(self):
			self.wndCardsIcon = uiCards.IngameWindow()
			self.wndCardsIcon.LoadWindow()
			self.wndCardsIcon.Hide()

	# ACCESSORY_REFINE_ADD_METIN_STONE
	def __MakeItemSelectWindow(self):
		self.wndItemSelect = uiselectitem.SelectItemWindow()
		self.wndItemSelect.Hide()
	# END_OF_ACCESSORY_REFINE_ADD_METIN_STONE

	def __BoardBiolog(self):
		self.wndBiolog = uibiolog.BiologWindow()
		self.wndBiolog.BindInterface(self)
		self.wndBiolog.Hide()

	def __BoardPanelChar(self):
		self.wndPanelChar = uiPremiumPanel.PremiumWindow()
		self.wndPanelChar.BindInterface(self)
		self.wndPanelChar.Hide()

	def OpenMyShop(self):
		net.SendChatPacket("/open_shop")
		
	if app.ENABLE_SEARCH_SHOP:
		def __MakeSearchShopWindow(self):
			self.wndSearchShop = uiSearchShop.SearchShopWindow()
			self.wndSearchShop.LoadWindow()

	def MakeInterface(self):
		self.__MakeMessengerWindow()
		self.__MakeGuildWindow()
		self.__MakeChatWindow()
		self.__MakeParty()
		self.__MakeWindows()
		self.__MakeDialogs()

		self.__MakeUICurtain()
		self.__MakeTaskBar()
		self.__MakeGameButtonWindow()
		self.__MakeTipBoard()
		if app.ENABLE_CHANGELOOK_SYSTEM:
			self.__MakeChangeLookWindow()
		if app.ENABLE_SASH_SYSTEM:
			self.__MakeSashWindow()
		self.__MakeCubeWindow()
		if app.ENABLE_MINIGAME_RUMI_EVENT:
			self.__MakeCardsInfoWindow()
			self.__MakeCardsWindow()
			self.__MakeCardsIconWindow()
		self.__MakeShoutWindow()
		if app.ENABLE_SWITCHBOT_WORLDARD:
			self.__MakeSwitchBot()
		# ACCESSORY_REFINE_ADD_METIN_STONE
		self.__MakeItemSelectWindow()
		# END_OF_ACCESSORY_REFINE_ADD_METIN_STONE		
		self.__BoardBiolog()
		self.__BoardPanelChar()
		if app.ENABLE_SEARCH_SHOP:
			self.__MakeSearchShopWindow()
		self.questButtonList = []
		self.whisperButtonList = []
		self.whisperDialogDict = {}
		self.privateShopAdvertisementBoardDict = {}

		self.wndInventory.SetItemToolTip(self.tooltipItem)
		self.wndCustomInventory.SetItemToolTip(self.tooltipItem)
		
		self.wndDragonSoul.SetItemToolTip(self.tooltipItem)
		self.wndDragonSoulRefine.SetItemToolTip(self.tooltipItem)
		if app.ENABLE_BATTLE_PASS:
			self.wndBattlePass.SetItemToolTip(self.tooltipItem)

		if app.ENABLE_INVENTORY_VIEWER:
			self.wndInventoryViewer.SetItemToolTip(self.tooltipItem)
		self.wndSafebox.SetItemToolTip(self.tooltipItem)
		if app.ENABLE_CHANGELOOK_SYSTEM:
			self.wndChangeLook.SetItemToolTip(self.tooltipItem)
		if app.ENABLE_SASH_SYSTEM:
			self.wndSashCombine.SetItemToolTip(self.tooltipItem)
			self.wndSashAbsorption.SetItemToolTip(self.tooltipItem)

		self.wndMall.SetItemToolTip(self.tooltipItem)
		self.wndCharacter.SetSkillToolTip(self.tooltipSkill)
		self.wndTaskBar.SetItemToolTip(self.tooltipItem)
		self.wndTaskBar.SetSkillToolTip(self.tooltipSkill)
		self.wndGuild.SetSkillToolTip(self.tooltipSkill)
		self.wndItemSelect.SetItemToolTip(self.tooltipItem)
		self.dlgShop.SetItemToolTip(self.tooltipItem)
		self.dlgExchange.SetItemToolTip(self.tooltipItem)
		self.privateShopBuilder.SetItemToolTip(self.tooltipItem)
		self.wndBiolog.SetItemToolTip(self.tooltipItem)
		self.wndGaya.SetItemToolTip(self.tooltipItem)
		self.wndWheelOfFright.SetItemToolTip(self.tooltipItem)
		self.wndLetterEvent.SetItemToolTip(self.tooltipItem)
		self.wndDungeonInfo.SetInterface(self)
		self.wndDungeonInfo.SetItemToolTip(self.tooltipItem)
		self.dlgChestDrop.SetItemToolTip(self.tooltipItem)
		if app.ENABLE_SEARCH_SHOP:
			self.wndSearchShop.SetToolTip(self.tooltipItem)

		if constInfo.STORED_WHISPERS_FOR == "":
			self.__InitWhisper()

		self.DRAGON_SOUL_IS_QUALIFIED = False

	def CancelQuestionDialog(self):
		self.OpenLinkQuestionDialog.Close()
		self.OpenLinkQuestionDialog = None
		
	def MakeHyperlinkTooltip(self, hyperlink):
		tokens = hyperlink.split(":")

		if tokens and len(tokens):
			type = tokens[0]
			if "item" == type:
				self.hyperlinkItemTooltip.SetHyperlinkItem(tokens)
			elif "web" == type:
					OpenLinkQuestionDialog = uiCommon.QuestionDialog2()
					OpenLinkQuestionDialog.SetText1(localeInfo.CHAT_OPEN_LINK_DANGER)
					OpenLinkQuestionDialog.SetText2(localeInfo.CHAT_OPEN_LINK)
					OpenLinkQuestionDialog.SetAcceptEvent(lambda arg = tokens: self.ExecuteLink(arg))
					OpenLinkQuestionDialog.SetCancelEvent(ui.__mem_func__(self.CancelQuestionDialog))
					OpenLinkQuestionDialog.Open()
					self.OpenLinkQuestionDialog = OpenLinkQuestionDialog
			elif "msg" == type:
				self.OpenWhisperDialog(str(tokens[1]))

	def ExecuteLink(self, tokens):
		app.ExecuteShell(tokens[1].replace("w<?", "://"))
		self.OpenLinkQuestionDialog.Close()
		self.OpenLinkQuestionDialog = None

	## Make Windows & Dialogs
	################################

	def Close(self):
		if self.dlgWhisperWithoutTarget:
			self.dlgWhisperWithoutTarget.Destroy()
			del self.dlgWhisperWithoutTarget

		for name in self.whisperDialogDict:
			self.__MakeWhisperButton(name)
			
		if uiQuest.QuestDialog.__dict__.has_key("QuestCurtain"):
			uiQuest.QuestDialog.QuestCurtain.Close()

		if self.wndQuestWindow:
			for key, eachQuestWindow in self.wndQuestWindow.items():
				eachQuestWindow.nextCurtainMode = -1
				eachQuestWindow.CloseSelf()
				eachQuestWindow = None
		self.wndQuestWindow = {}

		if self.wndChat:
			self.wndChat.Destroy()

		if self.wndBiolog:
			self.wndBiolog.Hide()
			self.wndBiolog.Destroy()

		if self.wndPanelChar:
			self.wndPanelChar.Hide()
			self.wndPanelChar.Destroy()

		if self.wndTaskBar:
			self.wndTaskBar.Destroy()

		if self.wndExpandedTaskBar:
			self.wndExpandedTaskBar.Destroy()
			
		if self.wndEnergyBar:
			self.wndEnergyBar.Destroy()

		if self.wndCharacter:
			self.wndCharacter.Hide()
			self.wndCharacter.Destroy()

		if self.wndInventory:
			self.wndInventory.Hide()
			self.wndInventory.Destroy()

		if self.wndCustomInventory:
			self.wndCustomInventory.Hide()
			self.wndCustomInventory.Destroy()

		if self.wndDragonSoul:
			self.wndDragonSoul.Hide()
			self.wndDragonSoul.Destroy()

		if self.wndDragonSoulRefine:
			self.wndDragonSoulRefine.Hide()
			self.wndDragonSoulRefine.Destroy()

		if self.dlgExchange:
			self.dlgExchange.Destroy()

		if self.dlgPointReset:
			self.dlgPointReset.Destroy()

		if self.dlgShop:
			self.dlgShop.Destroy()

		if self.dlgRestart:
			self.dlgRestart.Destroy()

		if self.dlgSystem:
			self.dlgSystem.Destroy()

		if self.dlgPassword:
			self.dlgPassword.Destroy()

		if self.wndMiniMap:
			self.wndMiniMap.Destroy()

		if self.wndSafebox:
			self.wndSafebox.Destroy()

		if self.wndGaya:
			self.wndGaya.Destroy()
			del self.wndGaya

		if self.wndWiki:
			self.wndWiki.Hide()
			self.wndWiki.Destroy()
			del self.wndWiki

		if self.wndDungeonInfo:
			self.wndDungeonInfo.Hide()
			self.wndDungeonInfo.Destroy()
			del self.wndDungeonInfo
			
		if self.wndRankInfo:
			self.wndRankInfo.Hide()
			self.wndRankInfo.Destroy()
			del self.wndRankInfo

		if self.wndMall:
			self.wndMall.Destroy()

		if self.wndParty:
			self.wndParty.Destroy()

		if app.ENABLE_CHANGELOOK_SYSTEM:
			if self.wndChangeLook:
				self.wndChangeLook.Destroy()
				
		if self.wndCube:
			self.wndCube.Destroy()

		# if self.wndNotifSys:
			# self.wndNotifSys.Destroy()
			
		if app.ENABLE_COSTUME_SYSTEM:
			if self.wndTargetRender:
				self.wndTargetRender.Destroy()

		if app.ENABLE_SASH_SYSTEM:
			if self.wndSashCombine:
				self.wndSashCombine.Destroy()
			
			if self.wndSashAbsorption:
				self.wndSashAbsorption.Destroy()

		if app.ENABLE_MINIGAME_RUMI_EVENT:
			if self.wndCardsInfo:
				self.wndCardsInfo.Destroy()

			if self.wndCards:
				self.wndCards.Destroy()

			if self.wndCardsIcon:
				self.wndCardsIcon.Destroy()

		if self.wndMessenger:
			self.wndMessenger.Destroy()

		if self.wndGuild:
			self.wndGuild.Destroy()
			
		if self.wndShout:
			self.wndShout.Destroy()
			
		if self.privateShopBuilder:
			self.privateShopBuilder.Destroy()

		if self.dlgRefineNew:
			self.dlgRefineNew.Destroy()

		if self.wndGuildBuilding:
			self.wndGuildBuilding.Destroy()

		if self.wndGameButton:
			self.wndGameButton.Destroy()

		if app.ENABLE_INVENTORY_VIEWER:
			if self.wndInventoryViewer:
				self.wndInventoryViewer.Hide()
				self.wndInventoryViewer.Destroy()

		# ITEM_MALL
		if self.mallPageDlg:
			self.mallPageDlg.Destroy()
			
		if self.wndChangeEmoticon:
			self.wndChangeEmoticon.Destroy()	
			
		if self.wndTabMap:
			self.wndTabMap.Destroy()	
			
		if self.wndRemoteShop:
			self.wndRemoteShop.Destroy()	
			
		if self.wndBattlePass:
			self.wndBattlePass.Hide()
			self.wndBattlePass.Destroy()

		if self.dlgChestDrop:
			self.dlgChestDrop.Destroy()

		if self.wndItemSelect:
			self.wndItemSelect.Destroy()

		if constInfo.ENABLE_EXPANDED_MONEY_TASKBAR:
			if self.wndExpandedMoneyTaskBar:
				self.wndExpandedMoneyTaskBar.Destroy()
				
		if app.ENABLE_REWARD_SYSTEM:
			if self.wndReward:
				self.wndReward.Hide()
				self.wndReward.Destroy()
				self.wndReward = None
				
		if app.ENABLE_EVENT_MANAGER:
			if self.wndEventManager:
				self.wndEventManager.Hide()
				self.wndEventManager.Destroy()
				self.wndEventManager = None

			if self.wndEventIcon:
				self.wndEventIcon.Hide()
				self.wndEventIcon.Destroy()
				self.wndEventIcon = None
				
		if self.wndWheelOfFright:
			self.wndWheelOfFright.Destroy()

		if self.wndLetterEvent:
			self.wndLetterEvent.Destroy()
		if app.ENABLE_SEARCH_SHOP:
			if self.wndSearchShop:
				self.wndSearchShop.Destroy()
		if app.ENABLE_SWITCHBOT_WORLDARD:
			if self.wndSwitchBot:
				self.wndSwitchBot.Close()
				self.wndSwitchBot.Destroy()
				del self.wndSwitchBot
		self.wndChatLog.Destroy()
		if app.ENABLE_INVENTORY_VIEWER:
			if self.wndInventoryViewer:
				del self.wndInventoryViewer
		for btn in self.questButtonList:
			btn.SetEvent(0)
		for btn in self.whisperButtonList:
			btn.SetEvent(0)
		for dlg in self.whisperDialogDict.itervalues():
			dlg.Destroy()
		for brd in self.guildScoreBoardDict.itervalues():
			brd.Destroy()
		for dlg in self.equipmentDialogDict.itervalues():
			dlg.Destroy()

		# ITEM_MALL
		del self.mallPageDlg
		# END_OF_ITEM_MALL

		del self.wndGuild
		del self.wndMessenger
		del self.wndUICurtain
		del self.wndChat
		del self.wndTaskBar
		if self.wndExpandedTaskBar:
			del self.wndExpandedTaskBar
		del self.wndEnergyBar
		del self.wndCharacter
		del self.wndInventory
		
		if self.wndDragonSoul:
			del self.wndDragonSoul
		if self.wndDragonSoulRefine:
			del self.wndDragonSoulRefine
		del self.wndCustomInventory
		del self.dlgExchange
		del self.dlgPointReset
		del self.dlgShop
		del self.dlgRestart
		del self.dlgSystem
		if self.wndMiniGame:
			self.wndMiniGame.Destroy()
			del self.wndMiniGame
		del self.dlgPassword
		del self.hyperlinkItemTooltip
		del self.tooltipItem
		del self.tooltipSkill
		del self.wndMiniMap
		del self.wndSafebox
		del self.wndMall
		del self.wndParty
		if app.ENABLE_CHANGELOOK_SYSTEM:
			del self.wndChangeLook
		if app.ENABLE_SASH_SYSTEM:
			del self.wndSashCombine
			del self.wndSashAbsorption
		# del self.wndNotifSys
		del self.wndCube
		if app.ENABLE_MINIGAME_RUMI_EVENT:
			del self.wndCardsInfo
			del self.wndCards
			del self.wndCardsIcon
		del self.privateShopBuilder
		del self.inputDialog
		del self.wndBiolog
		del self.wndPanelChar
		del self.wndChatLog
		del self.dlgRefineNew
		del self.wndGuildBuilding
		del self.wndGameButton
		del self.tipBoard
		del self.bigBoard
		del self.lefttipboard
		del self.wndItemSelect
		del self.wndShout

		if app.ENABLE_COSTUME_SYSTEM:
			del self.wndTargetRender
		del self.wndWheelOfFright
		del self.wndLetterEvent
		if self.dlgChestDrop:
			del self.dlgChestDrop

		if self.wndBattlePass:
			del self.wndBattlePass
			
		if self.wndChangeEmoticon:
			del self.wndChangeEmoticon		

		if self.wndTabMap:
			del self.wndTabMap
			
		if self.wndRemoteShop:
			del self.wndRemoteShop		

		if app.ENABLE_MAINTENANCE_SYSTEM:
			if self.wndMaintenance:
				self.wndMaintenance.Hide()
				self.wndMaintenance.Destroy()
				del self.wndMaintenance
				
		if constInfo.ENABLE_EXPANDED_MONEY_TASKBAR:
			if self.wndExpandedMoneyTaskBar:
				del self.wndExpandedMoneyTaskBar
				
		if app.ENABLE_SEARCH_SHOP:
			del self.wndSearchShop
			
		self.questButtonList = []

		# Store whispers after logout
		if len(self.whisperButtonList) > 0:
			constInfo.STORED_WHISPERS_FOR = player.GetName()
			for btn in self.whisperButtonList:
				constInfo.STORED_WHISPERS.append(btn.name)
		# End store whispers

		self.whisperButtonList = []
		self.whisperDialogDict = {}
		self.privateShopAdvertisementBoardDict = {}
		self.guildScoreBoardDict = {}
		self.equipmentDialogDict = {}

		uiChat.DestroyChatInputSetWindow()

	## Skill
	def OnUseSkill(self, slotIndex, coolTime):
		self.wndCharacter.OnUseSkill(slotIndex, coolTime)
		self.wndTaskBar.OnUseSkill(slotIndex, coolTime)
		self.wndGuild.OnUseSkill(slotIndex, coolTime)

	def OnActivateSkill(self, slotIndex):
		self.wndCharacter.OnActivateSkill(slotIndex)
		self.wndTaskBar.OnActivateSkill(slotIndex)

	def OnDeactivateSkill(self, slotIndex):
		self.wndCharacter.OnDeactivateSkill(slotIndex)
		self.wndTaskBar.OnDeactivateSkill(slotIndex)

	def OnChangeCurrentSkill(self, skillSlotNumber):
		self.wndTaskBar.OnChangeCurrentSkill(skillSlotNumber)

	def SelectMouseButtonEvent(self, dir, event):
		self.wndTaskBar.SelectMouseButtonEvent(dir, event)

	# HIDE_COSTUME
	def SetHideCostumePart(self, index, status):
		if self.wndInventory:
			self.wndInventory.SetHideCostumePart(index, status)
	# END_OF_HIDE_COSTUME
	
	## Refresh
	def RefreshAlignment(self):
		self.wndCharacter.RefreshAlignment()

	def RefreshStatus(self):
		self.wndTaskBar.RefreshStatus()
		self.wndCharacter.RefreshStatus()
		self.wndInventory.RefreshStatus()
		if self.wndEnergyBar:
			self.wndEnergyBar.RefreshStatus()
			
		self.wndDragonSoul.RefreshStatus()
		self.wndCustomInventory.RefreshItemSlot()
		
		if self.wndExpandedMoneyTaskBar:
			self.wndExpandedMoneyTaskBar.RefreshStatus()

	def RefreshStamina(self):
		self.wndTaskBar.RefreshStamina()

	def RefreshSkill(self):
		self.wndCharacter.RefreshSkill()
		self.wndTaskBar.RefreshSkill()
		
	def RefreshInventory(self):
		self.wndTaskBar.RefreshQuickSlot()
		self.wndInventory.RefreshItemSlot()
		self.wndDragonSoul.RefreshItemSlot()
		self.wndCustomInventory.RefreshItemSlot()
		if app.ENABLE_SWITCHBOT_WORLDARD:
			if self.wndSwitchBot:
				self.wndSwitchBot.RefreshItemSlot()

	def RefreshCharacter(self):
		self.wndCharacter.RefreshCharacter()
		self.wndTaskBar.RefreshQuickSlot()

	if app.ENABLE_REWARD_SYSTEM:
		def MakeRewardWindow(self):
			if self.wndReward == None:
				self.wndReward = uiReward.RewardWindow()
				
		def SetRewardPlayers(self, data):
			self.MakeRewardWindow()
			self.wndReward.SetRewardPlayers(data)
			
		def OpenRewardWindow(self):
			self.MakeRewardWindow()
			if self.wndReward.IsShow():
				self.wndReward.Close()
			else:
				self.wndReward.Open()

	if app.ENABLE_EVENT_MANAGER:
		def MakeEventIcon(self):
			if self.wndEventIcon == None:
				self.wndEventIcon = uiEventCalendar.MovableImage()
				self.wndEventIcon.Show()
				
		def MakeEventCalendar(self):
			if self.wndEventManager == None:
				self.wndEventManager = uiEventCalendar.EventCalendarWindow()
				
		def OpenEventCalendar(self):
			self.MakeEventCalendar()
			if self.wndEventManager.IsShow():
				self.wndEventManager.Close()
			else:
				self.wndEventManager.Open()
				
		def RefreshEventStatus(self, eventID, eventStatus, eventendTime, eventEndTimeText):
			if eventendTime != 0:
				eventendTime =+ app.GetGlobalTimeStamp()
			uiEventCalendar.SetEventStatus(eventID, eventStatus, eventendTime, eventEndTimeText)
			self.RefreshEventManager()
			
		def ClearEventManager(self):
			uiEventCalendar.server_event_data={}
			
		def RefreshEventManager(self):
			if self.wndEventManager:
				self.wndEventManager.Refresh()
			if self.wndEventIcon:
				self.wndEventIcon.Refresh()
				
		def AppendEvent(self, dayIndex, eventID, eventIndex, startTime, endTime, empireFlag, channelFlag, value0, value1, value2, value3, startRealTime, endRealTime, isAlreadyStart):
			self.MakeEventCalendar()
			self.MakeEventIcon()
						
			if startRealTime != 0:
				startRealTime += app.GetGlobalTimeStamp()
			if endRealTime != 0:
				endRealTime += app.GetGlobalTimeStamp()
			uiEventCalendar.SetServerData(dayIndex, eventID, eventIndex, startTime, endTime, empireFlag, channelFlag, value0, value1, value2, value3, startRealTime, endRealTime, isAlreadyStart)

	def RefreshQuest(self):
		self.wndCharacter.RefreshQuest()

	def RefreshSafebox(self):
		self.wndSafebox.RefreshSafebox()

	if app.ENABLE_SWITCHBOT_WORLDARD:
		def BINARY_SWITCHBOT_OPEN(self):
			self.wndSwitchBot.Show()
			
		def BINARY_SWITCHBOT_CLEAR_INFO(self):
			self.wndSwitchBot.func_clear_bonus_item()

		def BINARY_SWITCHBOT_INFO_BONUS(self,id_bonus,bonus_value_0,bonus_value_1,bonus_value_2,bonus_value_3,bonus_value_4):
			self.wndSwitchBot.func_set_bonus_items(id_bonus,bonus_value_0,bonus_value_1,bonus_value_2,bonus_value_3,bonus_value_4)

		def BINARY_SWITCHBOT_INFO_EXTRA(self):
			self.wndSwitchBot.func_add_mh()
			
	# ITEM_MALL
	def RefreshMall(self):
		self.wndMall.RefreshMall()

	def OpenItemMall(self):
		if not self.mallPageDlg:
			self.mallPageDlg = uiShop.MallPageDialog()

		self.mallPageDlg.Open()
	# END_OF_ITEM_MALL
	
	if app.ENABLE_SEARCH_SHOP:
		def OpenSearchShop(self):
			self.wndSearchShop.Open()
			
		def RefreshSearchShop(self):
			self.wndSearchShop.RefreshItems()

	def OpenChangeEmoticon(self):
		if False == player.IsObserverMode() and player.IsPremiumUser() == 1 or player.IsPremiumUser() == 2 or player.IsPremiumUser() == 3:
			if not self.wndChangeEmoticon.IsShow():
				self.wndChangeEmoticon.Show()
			else:
				self.wndChangeEmoticon.Close()	

	def OpenBattlePass(self):
		if False == player.IsObserverMode():
			if not self.wndBattlePass.IsShow():
				self.wndBattlePass.Show()
			else:
				self.wndBattlePass.Close()	
				
	def BattlePassMission(self, iType, iVnum, pCount, iCount):
		self.wndBattlePass.BattlePassMission(iType, iVnum, pCount, iCount)
		
	def BattlePassReward(self, iType, iVnum, iVnumReward, iCountReward):
		self.wndBattlePass.BattlePassMissionReward(iType, iVnum, iVnumReward, iCountReward)
		
	def BattlePassFinal(self, iVnum, iCount):
		self.wndBattlePass.BattlePassFinal(iVnum, iCount)

	def OpenTabMap(self):
		if False == player.IsObserverMode():
			if not self.wndTabMap.IsShow():
				self.wndTabMap.Open()
			else:
				self.wndTabMap.Close()	
				
	def OpenRemoteShop(self):
		if False == player.IsObserverMode() and player.IsPremiumUser() == 1 or player.IsPremiumUser() == 2 or player.IsPremiumUser() == 3:
			if not self.wndRemoteShop.IsShow():
				self.wndRemoteShop.Show()
			else:
				self.wndRemoteShop.Close()	
				
	def RefreshMessenger(self):
		# pass
		self.wndMessenger.RefreshMessenger()

	def RefreshGuildInfoPage(self):
		self.wndGuild.RefreshGuildInfoPage()

	def RefreshGuildBoardPage(self):
		self.wndGuild.RefreshGuildBoardPage()

	def RefreshGuildMemberPage(self):
		self.wndGuild.RefreshGuildMemberPage()

	def RefreshGuildMemberPageGradeComboBox(self):
		self.wndGuild.RefreshGuildMemberPageGradeComboBox()

	def RefreshGuildSkillPage(self):
		self.wndGuild.RefreshGuildSkillPage()

	def RefreshGuildGradePage(self):
		self.wndGuild.RefreshGuildGradePage()

	def DeleteGuild(self):
		self.wndMessenger.ClearGuildMember()
		self.wndGuild.DeleteGuild()

	def RefreshMobile(self):
		self.dlgSystem.RefreshMobile()

	def OnMobileAuthority(self):
		self.dlgSystem.OnMobileAuthority()

	def OnBlockMode(self, mode):
		self.dlgSystem.OnBlockMode(mode)

	## Calling Functions
	# PointReset
	def OpenPointResetDialog(self):
		self.dlgPointReset.Show()
		self.dlgPointReset.SetTop()

	def ClosePointResetDialog(self):
		self.dlgPointReset.Close()

	# Shop
	def OpenShopDialog(self, vid):
		self.wndInventory.Show()
		self.wndInventory.SetTop()
		self.dlgShop.Open(vid)
		self.dlgShop.SetTop()
		
	if app.ENABLE_OFFLINE_SHOP:
		def UpdateShopGold(self, gold):
			self.dlgShop.UpdateGold(gold)
		
		def UpdateShopLock(self, lock):
			self.dlgShop.UpdateLock(lock)
		
		def UpdateShopTime(self, time):
			self.dlgShop.UpdateTime(time)
		
		def UpdateShopSign(self, sign):
			self.dlgShop.UpdateSign(sign)
		
		def OpenOfflineShop(self, sign, channel, index, x, y, time, update):
			self.dlgShop.OpenOfflineShop(sign, channel, index, x, y, time, update)
			
	def CloseShopDialog(self):
		self.dlgShop.Close()

	def RefreshShopDialog(self):
		self.dlgShop.Refresh()

	def AddChestDropInfo(self, chestVnum, dropChance, slotIndex, itemVnum, itemCount):
		self.dlgChestDrop.AddChestDropItem(int(chestVnum), int(slotIndex), int(dropChance), int(itemVnum), int(itemCount))

	def RefreshChestDropInfo(self, chestVnum):
		self.dlgChestDrop.RefreshItems(chestVnum)

	## Quest
	def OpenCharacterWindowQuestPage(self):
		self.wndCharacter.Show()
		self.wndCharacter.SetState("QUEST")

	def OpenQuestWindow(self, skin, idx):

		wnds = ()

		q = uiQuest.QuestDialog(skin, idx)
		q.SetWindowName("QuestWindow" + str(idx))
		q.Show()
		if skin:
			q.Lock()
			wnds = self.__HideWindows()

			# UNKNOWN_UPDATE
			q.AddOnDoneEvent(lambda tmp_self, args=wnds: self.__ShowWindows(args))
			# END_OF_UNKNOWN_UPDATE

		if skin:
			q.AddOnCloseEvent(q.Unlock)
		q.AddOnCloseEvent(lambda key = self.wndQuestWindowNewKey:ui.__mem_func__(self.RemoveQuestDialog)(key))
		self.wndQuestWindow[self.wndQuestWindowNewKey] = q

		self.wndQuestWindowNewKey = self.wndQuestWindowNewKey + 1

		# END_OF_UNKNOWN_UPDATE

	def HideAllQuestWindow(self):
		tempList = []
		for i,v in self.wndQuestWindow.iteritems():
			tempList.append(v)

		for i in tempList:
			i.OnCancel()

	def RemoveQuestDialog(self, key):
		del self.wndQuestWindow[key]

	## Exchange
	def StartExchange(self):
		self.dlgExchange.OpenDialog()
		self.dlgExchange.Refresh()

	def EndExchange(self):
		self.dlgExchange.CloseDialog()

	def RefreshExchange(self):
		self.dlgExchange.Refresh()
	
	if app.WJ_ENABLE_TRADABLE_ICON:
		def CantTradableItemExchange(self, dstSlotIndex, srcSlotIndex):
			onTopWnd = self.GetOnTopWindow()
			if onTopWnd == player.ON_TOP_WND_EXCHANGE:
				self.dlgExchange.CantTradableItem(dstSlotIndex, srcSlotIndex)

	## Party
	def AddPartyMember(self, pid, name):
		self.wndParty.AddPartyMember(pid, name)

		self.__ArrangeQuestButton()

	def UpdatePartyMemberInfo(self, pid):
		self.wndParty.UpdatePartyMemberInfo(pid)

	def RemovePartyMember(self, pid):
		self.wndParty.RemovePartyMember(pid)
		self.__ArrangeQuestButton()

	def LinkPartyMember(self, pid, vid):
		self.wndParty.LinkPartyMember(pid, vid)

	def UnlinkPartyMember(self, pid):
		self.wndParty.UnlinkPartyMember(pid)

	def UnlinkAllPartyMember(self):
		self.wndParty.UnlinkAllPartyMember()

	def ExitParty(self):
		self.wndParty.ExitParty()
		self.__ArrangeQuestButton()

	def PartyHealReady(self):
		self.wndParty.PartyHealReady()

	def ChangePartyParameter(self, distributionMode):
		self.wndParty.ChangePartyParameter(distributionMode)

	# GAYA
	def ClearGaya(self):
		self.wndGaya.Clear()
		
	def AddGayaItem(self, pos, dwVnumReward, bCountReward, dwVnumPrice, iCountNeed, bType):
		self.wndGaya.AddItem(pos, dwVnumReward, bCountReward, dwVnumPrice, iCountNeed, bType)
	
	def SetGaya(self, race):
		self.wndGaya.Set(race)	
	# END_OF_GAYA

	def ShowWiki(self):
		if self.wndWiki.IsShow():
			self.wndWiki.Close()
		else:
			self.wndWiki.SetTop()
			self.wndWiki.Show()

	def SetMobInfo(self, page, index, mob, vnum, count):
		self.wndWiki.SetMobInfo(page, index, mob, vnum, count)

	def SearchInWiki(self, Type, iVnum):
		self.wndWiki.SearchByInfo(Type, iVnum)

	def ShowDungeonInfo(self):
		if self.wndDungeonInfo.IsShow() == FALSE:
			self.wndDungeonInfo.Show()
		else:
			self.wndDungeonInfo.Close()
	
	# Rank Info
	def ShowRankInfo(self):
		if self.wndRankInfo.IsShow() == FALSE:
			self.wndRankInfo.Show()
		else:
			self.wndRankInfo.Close()

	def AppendInfoRankGlobal(self, mode, my_pos, pos, name, value, empire):
		self.wndRankInfo.AppendInfo(mode, my_pos, pos, name, value, empire)

	## Safebox
	def AskSafeboxPassword(self):
		if self.wndSafebox.IsShow():
			return

		# SAFEBOX_PASSWORD
		self.dlgPassword.SetTitle(localeInfo.PASSWORD_TITLE)
		self.dlgPassword.SetSendMessage("/safebox_password ")
		# END_OF_SAFEBOX_PASSWORD

		self.dlgPassword.ShowDialog()

	def OpenSafeboxWindow(self, size):
		self.dlgPassword.CloseDialog()
		self.wndSafebox.ShowWindow(size)
		# self.wndCustomInventory.SetTableSize(size)

	def RefreshSafeboxMoney(self):
		self.wndSafebox.RefreshSafeboxMoney()

	def CommandCloseSafebox(self):
		self.wndSafebox.CommandCloseSafebox()

	# ITEM_MALL
	def AskMallPassword(self):
		if self.wndMall.IsShow():
			return
			
		# Grimm
		if self.dlgPassword.IsShow():
			self.dlgPassword.CloseDialog()
			return
			
		self.dlgPassword.SetTitle(localeInfo.MALL_PASSWORD_TITLE)
		self.dlgPassword.SetSendMessage("/mall_password ")
		self.dlgPassword.ShowDialog()

	def OpenMallWindow(self, size):
		self.dlgPassword.CloseDialog()
		self.wndMall.ShowWindow(size)

	def CommandCloseMall(self):
		self.wndMall.CommandCloseMall()
	# END_OF_ITEM_MALL
	
	# def SendNotification(self, szString):
		# self.wndNotifSys.RecieveInfo(szString)
		# self.wndNotifSys.DisplayNotification(szString)

	## Guild
	def OnStartGuildWar(self, guildSelf, guildOpp):
		self.wndGuild.OnStartGuildWar(guildSelf, guildOpp)

		guildWarScoreBoard = uiGuild.GuildWarScoreBoard()
		guildWarScoreBoard.Open(guildSelf, guildOpp)
		guildWarScoreBoard.Show()
		self.guildScoreBoardDict[uiGuild.GetGVGKey(guildSelf, guildOpp)] = guildWarScoreBoard

	def OnEndGuildWar(self, guildSelf, guildOpp):
		self.wndGuild.OnEndGuildWar(guildSelf, guildOpp)

		key = uiGuild.GetGVGKey(guildSelf, guildOpp)

		if not self.guildScoreBoardDict.has_key(key):
			return

		self.guildScoreBoardDict[key].Destroy()
		del self.guildScoreBoardDict[key]

	# GUILDWAR_MEMBER_COUNT
	def UpdateMemberCount(self, gulidID1, memberCount1, guildID2, memberCount2):
		key = uiGuild.GetGVGKey(gulidID1, guildID2)

		if not self.guildScoreBoardDict.has_key(key):
			return

		self.guildScoreBoardDict[key].UpdateMemberCount(gulidID1, memberCount1, guildID2, memberCount2)
	# END_OF_GUILDWAR_MEMBER_COUNT

	def OnRecvGuildWarPoint(self, gainGuildID, opponentGuildID, point):
		key = uiGuild.GetGVGKey(gainGuildID, opponentGuildID)
		if not self.guildScoreBoardDict.has_key(key):
			return

		guildBoard = self.guildScoreBoardDict[key]
		guildBoard.SetScore(gainGuildID, opponentGuildID, point)

	## PK Mode
	def OnChangePKMode(self):
		self.wndCharacter.RefreshAlignment()
		self.dlgSystem.OnChangePKMode()

	## Refine
	def OpenRefineDialog(self, targetItemPos, nextGradeItemVnum, cost, prob, type):
		self.dlgRefineNew.Open(targetItemPos, nextGradeItemVnum, cost, prob, type)

	def AppendMaterialToRefineDialog(self, vnum, count):
		self.dlgRefineNew.AppendMaterial(vnum, count)

	# if app.ENABLE_REFINE_RENEWAL:
	def CheckRefineDialog(self, isFail):
		self.dlgRefineNew.CheckRefine(isFail)	

		## Show & Hide
	def ShowMainWIndows(self):
		self.wndTaskBar.Show()
		#self.wndAffect.Show()
		self.wndMiniMap.Show()
		self.wndMiniMap.ShowMiniMap()

		if self.wndChat:
			self.wndChat.Show()

		if self.wndParty:
			if player.IsPartyMember(net.GetMainActorVID()):
				self.wndParty.Show()

	## Show & Hide
	def ShowDefaultWindows(self):
		self.wndTaskBar.Show()
		self.wndMiniMap.Show()
		self.wndMiniMap.ShowMiniMap()
		if self.wndEnergyBar:
			self.wndEnergyBar.Show()
		if self.wndMiniGame:
			self.wndMiniGame.ShowMiniGameDialog()

	def ShowAllWindows(self):
		self.wndTaskBar.Show()
		self.wndCharacter.Show()
		self.wndInventory.Show()
		self.wndDragonSoul.Show()
		self.wndDragonSoulRefine.Show()
		self.wndCustomInventory.Show()
		self.wndChat.Show()
		self.wndMiniMap.Show()
		if self.wndEnergyBar:
			self.wndEnergyBar.Show()
		if self.wndExpandedTaskBar:
			self.wndExpandedTaskBar.Show()
			self.wndExpandedTaskBar.SetTop()
		if constInfo.ENABLE_EXPANDED_MONEY_TASKBAR:
			if self.wndExpandedMoneyTaskBar:
				self.wndExpandedMoneyTaskBar.Show()
				self.wndExpandedMoneyTaskBar.SetTop()

	def HideAllWindows(self):
		if self.wndTaskBar:
			self.wndTaskBar.Hide()

		if self.wndEnergyBar:
			self.wndEnergyBar.Hide()

		if self.wndCharacter:
			self.wndCharacter.Close()

		if self.wndInventory:
			self.wndInventory.Hide()

		if self.wndDragonSoul:
			self.wndDragonSoul.Hide()
		if self.wndDragonSoulRefine:
			self.wndDragonSoulRefine.Hide()

		if constInfo.ENABLE_EXPANDED_MONEY_TASKBAR:
			if self.wndExpandedMoneyTaskBar:
				self.wndExpandedMoneyTaskBar.Hide()

		if app.ENABLE_INVENTORY_VIEWER:
			if self.wndInventoryViewer:
				self.wndInventoryViewer.Hide()

		if self.wndChat:
			self.wndChat.Hide()

		if self.wndMiniMap:
			self.wndMiniMap.Hide()

		if self.wndMessenger:
			self.wndMessenger.Hide()

		if self.wndGuild:
			self.wndGuild.Hide()

		if self.wndExpandedTaskBar:
			self.wndExpandedTaskBar.Hide()
			
		if app.ENABLE_COSTUME_SYSTEM:
			if self.wndTargetRender:
				self.wndTargetRender.Hide()

		if self.wndMiniGame:
			self.wndMiniGame.HideMiniGameDialog()

	def ShowMouseImage(self):
		self.wndTaskBar.ShowMouseImage()

	def HideMouseImage(self):
		self.wndTaskBar.HideMouseImage()
		
	def LoadAppLeftTip(self, message, type):
		self.lefttipboard.SetTip(message, type)

	def ToggleChat(self):
		if True == self.wndChat.IsEditMode():
			self.wndChat.CloseChat()
		else:
			self.wndChat.OpenChat()

	def IsOpenChat(self):
		return self.wndChat.IsEditMode()

	def SetChatFocus(self):
		self.wndChat.SetChatFocus()

	def CheckMap(self):
		mapcontrol = [
			"summonersrift",
		]

		if str(background.GetCurrentMapName()) in mapcontrol:
			return True

		return False

	def OpenRestartDialog(self):
		if self.CheckMap():
			pass
		else:
			self.dlgRestart.OpenDialog()
			self.dlgRestart.SetTop()

	def CloseRestartDialog(self):
		if self.CheckMap():
			pass
		else:
			self.dlgRestart.Close()

	def ToggleSystemDialog(self):
		if False == self.dlgSystem.IsShow():
			self.dlgSystem.OpenDialog()
			self.dlgSystem.SetTop()
		else:
			self.dlgSystem.Close()

	def OpenSystemDialog(self):
		self.dlgSystem.OpenDialog()
		self.dlgSystem.SetTop()

	def ToggleMessenger(self):
		if self.wndMessenger.IsShow():
			self.wndMessenger.Hide()
		else:
			self.wndMessenger.SetTop()
			self.wndMessenger.Show()

	def ToggleMiniMap(self):
		if app.IsPressed(app.DIK_LSHIFT) or app.IsPressed(app.DIK_RSHIFT):
			if False == self.wndMiniMap.isShowMiniMap():
				self.wndMiniMap.ShowMiniMap()
				self.wndMiniMap.SetTop()
				if self.wndMiniGame:
					self.wndMiniGame.ShowMiniGameDialog()
			else:
				self.wndMiniMap.HideMiniMap()
				if self.wndMiniGame:
					self.wndMiniGame.HideMiniGameDialog()
		else:
			self.wndMiniMap.ToggleAtlasWindow()

	def DoMiniGameAction(self, mode):
		if mode == 0:
			if self.wndMiniGame:
				self.wndMiniGame.HideMiniGameDialog()
		else:
			if self.wndMiniGame:
				self.wndMiniGame.ShowMiniGameDialog()

	def PressMKey(self):
		if app.IsPressed(app.DIK_LALT) or app.IsPressed(app.DIK_RALT):
			self.ToggleMessenger()

		else:
			self.ToggleMiniMap()

	def SetMapName(self, mapName):
		self.wndMiniMap.SetMapName(mapName)

	def MiniMapScaleUp(self):
		self.wndMiniMap.ScaleUp()

	def MiniMapScaleDown(self):
		self.wndMiniMap.ScaleDown()

	def ToggleCharacterWindow(self, state):
		if False == player.IsObserverMode():
			if False == self.wndCharacter.IsShow():
				self.OpenCharacterWindowWithState(state)
			else:
				if state == self.wndCharacter.GetState():
					self.wndCharacter.OverOutItem()
					self.wndCharacter.Close()
				else:
					self.wndCharacter.SetState(state)

	def OpenCharacterWindowWithState(self, state):
		if False == player.IsObserverMode():
			self.wndCharacter.SetState(state)
			self.wndCharacter.Show()
			self.wndCharacter.SetTop()

	def ToggleCharacterWindowStatusPage(self):
		self.ToggleCharacterWindow("STATUS")

	def ToggleInventoryWindow(self):
		if False == player.IsObserverMode():
			if False == self.wndInventory.IsShow():
				self.wndInventory.Show()
				self.wndInventory.SetTop()
			else:
				self.wndInventory.OverOutItem()
				self.wndInventory.Close()

	def ToggleCustomInventoryWindow(self):
		if False == player.IsObserverMode():
			if False == self.wndCustomInventory.IsShow():
				self.wndCustomInventory.Show()
				self.wndCustomInventory.SetTop()
			else:
				self.wndCustomInventory.OverOutItem()
				self.wndCustomInventory.CloseFromTitleBar()

	if app.ENABLE_INVENTORY_VIEWER:
		def InventoryViewerAddItem(self, pageIndex, slotIndex, itemVnum, itemCount):
			if self.wndInventoryViewer:
				self.wndInventoryViewer.AddItemInInventory(pageIndex, slotIndex, itemVnum, itemCount)
				
		def InventoryViewerAddSocket(self, pageIndex, slotIndex, socketIndex, socketValue):
			if self.wndInventoryViewer:
				self.wndInventoryViewer.InventoryItemAddSocket(pageIndex, slotIndex, socketIndex, socketValue)
				
		def InventoryViewerAddAttr(self, pageIndex, slotIndex, attrIndex, attrType, attrValue):
			if self.wndInventoryViewer:
				self.wndInventoryViewer.InventoryItemAddAttr(pageIndex, slotIndex, attrIndex, attrType, attrValue)
				
		if app.ENABLE_CHANGELOOK_SYSTEM:
			def InventoryViewerAddTransmutation(self, pageIndex, slotIndex, transmutation):
				if self.wndInventoryViewer:
					self.wndInventoryViewer.InventoryItemAddTransmutation(pageIndex, slotIndex, transmutation)
				
		def OpenInventoryViewerWindow(self, chrVid):
			if self.wndInventoryViewer:
				self.wndInventoryViewer.Open(chrVid)
			
	def ToggleExpandedButton(self):
		if False == player.IsObserverMode():
			if False == self.wndExpandedTaskBar.IsShow():
				self.wndExpandedTaskBar.Show()
				self.wndExpandedTaskBar.SetTop()
			else:
				self.wndExpandedTaskBar.Close()
				
	if constInfo.ENABLE_EXPANDED_MONEY_TASKBAR:
		def ToggleExpandedMoneyButton(self):
			if False == self.wndExpandedMoneyTaskBar.IsShow():
				self.wndExpandedMoneyTaskBar.Show()
				self.wndExpandedMoneyTaskBar.SetTop()
			else:
				self.wndExpandedMoneyTaskBar.Close()

	def ToggleGuildWindow(self):
		if not self.wndGuild.IsShow():
			if self.wndGuild.CanOpen():
				self.wndGuild.Open()
			else:
				chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.GUILD_YOU_DO_NOT_JOIN)
		else:
			self.wndGuild.OverOutItem()
			self.wndGuild.Hide()

	def ToggleChatLogWindow(self):
		if self.wndChatLog.IsShow():
			self.wndChatLog.Hide()
		else:
			self.wndChatLog.Show()

	def ToggleWheelOfFright(self):
		if self.wndWheelOfFright.IsShow():
			self.wndWheelOfFright.Close()
		else:
			self.wndWheelOfFright.Open()
	
	def SpinWheelOfFright(self, spin, prizes):
		self.wndWheelOfFright.Spin(spin, prizes)

	def ToggleLetterEvent(self):
		if self.wndLetterEvent.IsShow():
			self.wndLetterEvent.Close()
		else:
			self.wndLetterEvent.Show()

	def SetLetterItem(self, index, vnum, count):
		self.wndLetterEvent.SetLetter(index, vnum, count)

	def SetLetterDropItem(self, index, vnum, count):
		self.wndLetterEvent.SetReward(index, vnum, count)
		
	def DragonSoulActivate(self, deck):
		self.wndDragonSoul.ActivateDragonSoulByExtern(deck)

	def DragonSoulDeactivate(self):
		self.wndDragonSoul.DeactivateDragonSoul()
		
	def UseDSSButtonEffect(self, enable):
		if self.wndInventory:
			self.wndInventory.UseDSSButtonEffect(enable)
				
	def Highligt_Item(self, inven_type, inven_pos):
		if player.DRAGON_SOUL_INVENTORY == inven_type:
			self.wndDragonSoul.HighlightSlot(inven_pos)
				
		if player.INVENTORY == inven_type:
			if inven_pos <= 180: # grimm @@@
				self.wndInventory.HighlightSlot(inven_pos)
			else:
				self.wndCustomInventory.HighlightSlot(inven_pos)
	
	def DragonSoulGiveQuilification(self):
		self.DRAGON_SOUL_IS_QUALIFIED = True

	def ToggleDragonSoulWindow(self):
		if False == player.IsObserverMode():
			# if app.ENABLE_DRAGON_SOUL_SYSTEM:
			if False == self.wndDragonSoul.IsShow():
				if self.DRAGON_SOUL_IS_QUALIFIED:
					self.wndDragonSoul.Show()
				else:
					try:
						self.wndPopupDialog.SetText(localeInfo.DRAGON_SOUL_UNQUALIFIED)
						self.wndPopupDialog.Open()
					except:
						self.wndPopupDialog = uiCommon.PopupDialog()
						self.wndPopupDialog.SetText(localeInfo.DRAGON_SOUL_UNQUALIFIED)
						self.wndPopupDialog.Open()
			else:
				self.wndDragonSoul.Close()
		
	def ToggleDragonSoulWindowWithNoInfo(self):
		if False == player.IsObserverMode():
			# if app.ENABLE_DRAGON_SOUL_SYSTEM:
			if False == self.wndDragonSoul.IsShow():
				# if self.DRAGON_SOUL_IS_QUALIFIED:
				self.wndDragonSoul.Show()
			else:
				self.wndDragonSoul.Close()

	def FailDragonSoulRefine(self, reason, inven_type, inven_pos):
		if False == player.IsObserverMode():
			# if app.ENABLE_DRAGON_SOUL_SYSTEM:
			if True == self.wndDragonSoulRefine.IsShow():
				self.wndDragonSoulRefine.RefineFail(reason, inven_type, inven_pos)
 
	def SucceedDragonSoulRefine(self, inven_type, inven_pos):
		if False == player.IsObserverMode():
			# if app.ENABLE_DRAGON_SOUL_SYSTEM:
			if True == self.wndDragonSoulRefine.IsShow():
				self.wndDragonSoulRefine.RefineSucceed(inven_type, inven_pos)
 
	def OpenDragonSoulRefineWindow(self):
		if False == player.IsObserverMode():
			# if app.ENABLE_DRAGON_SOUL_SYSTEM:
			if False == self.wndDragonSoulRefine.IsShow():
				self.wndDragonSoulRefine.Show()
				if None != self.wndDragonSoul:
					if False == self.wndDragonSoul.IsShow():
						self.wndDragonSoul.Show()

	def CloseDragonSoulRefineWindow(self):
		if False == player.IsObserverMode():
			# if app.ENABLE_DRAGON_SOUL_SYSTEM:
			if True == self.wndDragonSoulRefine.IsShow():
				self.wndDragonSoulRefine.Close()

	def CheckGameButton(self):
		if self.wndGameButton:
			self.wndGameButton.CheckGameButton()

	def __OnClickStatusPlusButton(self):
		self.ToggleCharacterWindow("STATUS")

	def __OnClickSkillPlusButton(self):
		self.ToggleCharacterWindow("SKILL")

	def __OnClickQuestButton(self):
		self.ToggleCharacterWindow("QUEST")

	def __OnClickBuildButton(self):
		self.BUILD_OpenWindow()
		self.wndChat.CloseChat()

	def BINARY_CUBE_RENEWAL_OPEN(self):
		self.wndCube.Openz()
		
	def BINARY_CUBE_RENEWAL_LOADING(self):
		self.wndCube.BINARY_CUBE_RENEWAL_LOADING()

	def ShowBiolog(self):
		if self.wndBiolog.IsShow() == FALSE:
			self.wndBiolog.Show()
		else:
			self.wndBiolog.Close()
			
	def OpenCharPanel(self):
		if self.wndPanelChar.IsShow() == FALSE:
			self.wndPanelChar.Show()
		else:
			self.wndPanelChar.Close()

	def AppendInfoBiologBonus(self, Index, Type, Value):
		self.wndBiolog.SetInfoBonus(Index, Type, Value)
	
	def AppendInfoBiologTime(self, timeLeft, maxTime):
		self.wndBiolog.SetInfoTime(timeLeft, maxTime)
	
	def AppendInfoBiolog(self, iRewardVnum, vnum, actualCount, needCount):
		self.wndBiolog.SetInfoMission(iRewardVnum, vnum, actualCount, needCount)

	if app.ENABLE_MINIGAME_RUMI_EVENT:
		def OpenCardsInfoWindow(self):
			self.wndCardsInfo.Open()

		def OpenCardsWindow(self, safemode):
			self.wndCards.Open(safemode)

		def UpdateCardsInfo(self, hand_1, hand_1_v, hand_2, hand_2_v, hand_3, hand_3_v, hand_4, hand_4_v, hand_5, hand_5_v, cards_left, points):
			self.wndCards.UpdateCardsInfo(hand_1, hand_1_v, hand_2, hand_2_v, hand_3, hand_3_v, hand_4, hand_4_v, hand_5, hand_5_v, cards_left, points)

		def UpdateCardsFieldInfo(self, hand_1, hand_1_v, hand_2, hand_2_v, hand_3, hand_3_v, points):
			self.wndCards.UpdateCardsFieldInfo(hand_1, hand_1_v, hand_2, hand_2_v, hand_3, hand_3_v, points)

		def CardsPutReward(self, hand_1, hand_1_v, hand_2, hand_2_v, hand_3, hand_3_v, points):
			self.wndCards.CardsPutReward(hand_1, hand_1_v, hand_2, hand_2_v, hand_3, hand_3_v, points)

		def CardsShowIcon(self):
			self.wndCardsIcon.Show()

	# show GIFT
	def ShowGift(self):
		self.wndTaskBar.ShowGift()

	if app.ENABLE_CHANGELOOK_SYSTEM:
		def ActChangeLook(self, iAct):
			if iAct == 1:
				if not self.wndChangeLook.IsOpened():
					self.wndChangeLook.Open()
				
				if not self.wndInventory.IsShow():
					self.wndInventory.Show()
				
				self.wndInventory.RefreshBagSlotWindow()
			elif iAct == 2:
				if self.wndChangeLook.IsOpened():
					self.wndChangeLook.Close()
				
				self.wndInventory.RefreshBagSlotWindow()
			elif iAct == 3 or iAct == 4:
				if self.wndChangeLook.IsOpened():
					self.wndChangeLook.Refresh()
				
				self.wndInventory.RefreshBagSlotWindow()

	if app.ENABLE_SASH_SYSTEM:
		def ActSash(self, iAct, bWindow):
			if iAct == 1:
				if bWindow == True:
					if not self.wndSashCombine.IsOpened():
						self.wndSashCombine.Open()
					
					if not self.wndInventory.IsShow():
						self.wndInventory.Show()
				else:
					if not self.wndSashAbsorption.IsOpened():
						self.wndSashAbsorption.Open()
					
					if not self.wndInventory.IsShow():
						self.wndInventory.Show()
				
				self.wndInventory.RefreshBagSlotWindow()
			elif iAct == 2:
				if bWindow == True:
					if self.wndSashCombine.IsOpened():
						self.wndSashCombine.Close()
				else:
					if self.wndSashAbsorption.IsOpened():
						self.wndSashAbsorption.Close()
				
				self.wndInventory.RefreshBagSlotWindow()
			elif iAct == 3 or iAct == 4:
				if bWindow == True:
					if self.wndSashCombine.IsOpened():
						self.wndSashCombine.Refresh(iAct)
				else:
					if self.wndSashAbsorption.IsOpened():
						self.wndSashAbsorption.Refresh(iAct)
				
				self.wndInventory.RefreshBagSlotWindow()
				
	def __HideWindows(self):
		hideWindows = self.wndTaskBar,\
						self.wndCharacter,\
						self.wndInventory,\
						self.wndMiniMap,\
						self.wndGuild,\
						self.wndMessenger,\
						self.wndChat,\
						self.wndParty,\
						self.wndGameButton,

		if self.wndEnergyBar:
			hideWindows += self.wndEnergyBar,

		if self.wndChangeEmoticon:
			hideWindows += self.wndChangeEmoticon,

		if self.wndTabMap:
			hideWindows += self.wndTabMap,
			
		if self.wndRemoteShop:
			hideWindows += self.wndRemoteShop,
			
		if self.wndMiniGame:
			hideWindows += self.wndMiniGame,
			
		if self.wndExpandedTaskBar:
			hideWindows += self.wndExpandedTaskBar,

		if constInfo.ENABLE_EXPANDED_MONEY_TASKBAR:
			if self.wndExpandedMoneyTaskBar:
				hideWindows += self.wndExpandedMoneyTaskBar,
				
		if app.ENABLE_COSTUME_SYSTEM:
			hideWindows += self.wndTargetRender,

		if self.wndDragonSoul:
			hideWindows += self.wndDragonSoul,\
						self.wndDragonSoulRefine,

		if self.wndBattlePass:
			hideWindows += self.wndBattlePass,

		hideWindows = filter(lambda x:x.IsShow(), hideWindows)
		map(lambda x:x.Hide(), hideWindows)
		import sys

		self.HideAllQuestButton()
		self.HideAllWhisperButton()

		if self.wndChat.IsEditMode():
			self.wndChat.CloseChat()

		return hideWindows

	def __ShowWindows(self, wnds):
		import sys
		map(lambda x:x.Show(), wnds)
		global IsQBHide
		if not IsQBHide:
			self.ShowAllQuestButton()
		else:
			self.HideAllQuestButton()

		self.ShowAllWhisperButton()

	def BINARY_OpenAtlasWindow(self):
		if self.wndMiniMap:
			self.wndMiniMap.ShowAtlas()

	def BINARY_SetObserverMode(self, flag):
		self.wndGameButton.SetObserverMode(flag)

	def BINARY_OpenSelectItemWindow(self):
		self.wndItemSelect.Open()
	
	if app.ENABLE_MAINTENANCE_SYSTEM:
		def ShowMaintenanceSign(self, timeLeft, duration):
			if not self.wndMaintenance:
				self.wndMaintenance = uiMaintenance.MaintenanceBoard()
			self.wndMaintenance.Open(timeLeft, duration)

		def HideMaintenanceSign(self):
			if self.wndMaintenance:
				self.wndMaintenance.Close()

	def OpenPrivateShopBuilderNoDialog(self):
		if self.privateShopBuilder.IsShow() == FALSE:
			self.privateShopBuilder.Open(" ")
		else:
			self.privateShopBuilder.Close()

	def OpenPrivateShopInputNameDialog(self):
		#if player.IsInSafeArea():
		#	chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.CANNOT_OPEN_PRIVATE_SHOP_IN_SAFE_AREA)
		#	return

		inputDialog = uiCommon.InputDialog()
		inputDialog.SetTitle(localeInfo.PRIVATE_SHOP_INPUT_NAME_DIALOG_TITLE)
		inputDialog.SetMaxLength(32)
		inputDialog.SetAcceptEvent(ui.__mem_func__(self.OpenPrivateShopBuilder))
		inputDialog.SetCancelEvent(ui.__mem_func__(self.ClosePrivateShopInputNameDialog))
		inputDialog.Open()
		self.inputDialog = inputDialog

	def ClosePrivateShopInputNameDialog(self):
		self.inputDialog = None
		return True

	def OpenPrivateShopBuilder(self):

		if not self.inputDialog:
			return True

		if not len(self.inputDialog.GetText()):
			return True

		self.privateShopBuilder.Open(self.inputDialog.GetText())
		self.ClosePrivateShopInputNameDialog()
		return True

	def AppearPrivateShop(self, vid, text):
		board = uiPrivateShopBuilder.PrivateShopAdvertisementBoard()
		board.Open(vid, text)

		self.privateShopAdvertisementBoardDict[vid] = board

	def DisappearPrivateShop(self, vid):
		if not self.privateShopAdvertisementBoardDict.has_key(vid):
			return

		del self.privateShopAdvertisementBoardDict[vid]
		uiPrivateShopBuilder.DeleteADBoard(vid)

	#####################################################################################
	### Equipment ###

	def OpenEquipmentDialog(self, vid):
		dlg = uiEquipmentDialog.EquipmentDialog()
		dlg.SetItemToolTip(self.tooltipItem)
		dlg.SetCloseEvent(ui.__mem_func__(self.CloseEquipmentDialog))
		dlg.Open(vid)

		self.equipmentDialogDict[vid] = dlg

	def SetEquipmentDialogItem(self, vid, slotIndex, vnum, count):
		if not vid in self.equipmentDialogDict:
			return
		self.equipmentDialogDict[vid].SetEquipmentDialogItem(slotIndex, vnum, count)

	def SetEquipmentDialogSocket(self, vid, slotIndex, socketIndex, value):
		if not vid in self.equipmentDialogDict:
			return
		self.equipmentDialogDict[vid].SetEquipmentDialogSocket(slotIndex, socketIndex, value)

	def SetEquipmentDialogAttr(self, vid, slotIndex, attrIndex, type, value):
		if not vid in self.equipmentDialogDict:
			return
		self.equipmentDialogDict[vid].SetEquipmentDialogAttr(slotIndex, attrIndex, type, value)

	def CloseEquipmentDialog(self, vid):
		if not vid in self.equipmentDialogDict:
			return
		del self.equipmentDialogDict[vid]

	#####################################################################################

	#####################################################################################
	### Quest ###
	def BINARY_ClearQuest(self, index):
		btn = self.__FindQuestButton(index)
		if 0 != btn:
			self.__DestroyQuestButton(btn)

	def RecvQuest(self, index, name):
		# QUEST_LETTER_IMAGE
		self.BINARY_RecvQuest(index, name, "file", localeInfo.GetLetterImageName())
		# END_OF_QUEST_LETTER_IMAGE

	def BINARY_RecvQuest(self, index, name, iconType, iconName):

		btn = self.__FindQuestButton(index)
		if 0 != btn:
			self.__DestroyQuestButton(btn)

		btn = uiWhisper.WhisperButton()

		# QUEST_LETTER_IMAGE
		##!! 20061026.levites.퀘스트_이미지_교체
		import item
		if "item"==iconType:
			item.SelectItem(int(iconName))
			buttonImageFileName=item.GetIconImageFileName()
		else:
			buttonImageFileName=iconName
		if constInfo.ENABLE_COLOR_SCROLL and ('#' in name):
			for s_color in ("green","blue","purple"):
				if name.endswith(s_color):
					btn.SetUpVisual("icon/scroll_close_%s.tga"%s_color)
					btn.SetOverVisual("icon/scroll_open_%s.tga"%s_color)
					btn.SetDownVisual("icon/scroll_open_%s.tga"%s_color)
					name = name[:-1-len(s_color)]
					break
		else:
			#if localeInfo.IsEUROPE():
			#	btn.SetUpVisual(localeInfo.GetLetterCloseImageName())
			#	btn.SetOverVisual(localeInfo.GetLetterOpenImageName())
			#	btn.SetDownVisual(localeInfo.GetLetterOpenImageName())
			#else:
			btn.SetUpVisual(buttonImageFileName)
			btn.SetOverVisual(buttonImageFileName)
			btn.SetDownVisual(buttonImageFileName)

		# END_OF_QUEST_LETTER_IMAGE
		btn.SetToolTipText(name, -20, 35)
		btn.ToolTipText.SetHorizontalAlignLeft()

		btn.SetEvent(ui.__mem_func__(self.__StartQuest), btn)
		btn.Show()

		btn.index = index
		btn.name = name

		self.questButtonList.insert(0, btn)
		self.__ArrangeQuestButton()

		#chat.AppendChat(chat.CHAT_TYPE_NOTICE, localeInfo.QUEST_APPEND)

	def __ArrangeQuestButton(self):

		screenWidth = wndMgr.GetScreenWidth()
		screenHeight = wndMgr.GetScreenHeight()

		##!! 20061026.levites.퀘스트_위치_보정
		if self.wndParty.IsShow():
			xPos = 100 + 30
		else:
			xPos = 20

		yPos = 170 * screenHeight / 600
		yCount = (screenHeight - 330) / 63

		count = 0
		for btn in self.questButtonList:

			btn.SetPosition(xPos + (int(count/yCount) * 100), yPos + (count%yCount * 63))
			count += 1
			global IsQBHide
			if IsQBHide:
				btn.Hide()
			else:
				btn.Show()

	def __StartQuest(self, btn):
		event.QuestButtonClick(btn.index)
		self.__DestroyQuestButton(btn)

	def __FindQuestButton(self, index):
		for btn in self.questButtonList:
			if btn.index == index:
				return btn

		return 0

	def __DestroyQuestButton(self, btn):
		btn.SetEvent(0)
		self.questButtonList.remove(btn)
		self.__ArrangeQuestButton()

	def HideAllQuestButton(self):
		for btn in self.questButtonList:
			btn.Hide()

	def ShowAllQuestButton(self):
		for btn in self.questButtonList:
			btn.Show()

	def __InitWhisper(self):
		chat.InitFloatingBoxes(self)

	def OpenWhisperDialogWithoutTarget(self):
		if not self.dlgWhisperWithoutTarget:
			dlgWhisper = uiWhisper.WhisperDialog(self.MinimizeWhisperDialog, self.CloseWhisperDialog)
			dlgWhisper.BindInterface(self)
			dlgWhisper.LoadDialog()
			dlgWhisper.OpenWithoutTarget(self.RegisterTemporaryWhisperDialog)
			dlgWhisper.SetPosition(self.windowOpenPosition*30,self.windowOpenPosition*30)
			dlgWhisper.Show()
			self.dlgWhisperWithoutTarget = dlgWhisper

			self.windowOpenPosition = (self.windowOpenPosition+1) % 5

		else:
			self.dlgWhisperWithoutTarget.SetTop()
			self.dlgWhisperWithoutTarget.OpenWithoutTarget(self.RegisterTemporaryWhisperDialog)

	def RegisterTemporaryWhisperDialog(self, name):
		if not self.dlgWhisperWithoutTarget:
			return

		btn = self.__FindWhisperButton(name)
		if 0 != btn:
			self.__DestroyWhisperButton(btn)

		elif self.whisperDialogDict.has_key(name):
			oldDialog = self.whisperDialogDict[name]
			oldDialog.Destroy()
			del self.whisperDialogDict[name]

		self.whisperDialogDict[name] = self.dlgWhisperWithoutTarget
		self.dlgWhisperWithoutTarget.OpenWithTarget(name)
		self.dlgWhisperWithoutTarget = None
		self.__CheckGameMaster(name)

	def OpenWhisperDialog(self, name):
		if not self.whisperDialogDict.has_key(name):
			dlg = self.__MakeWhisperDialog(name)
			dlg.OpenWithTarget(name)
			dlg.chatLine.SetFocus()
			dlg.Show()

			self.__CheckGameMaster(name)
			btn = self.__FindWhisperButton(name)
			if 0 != btn:
				self.__DestroyWhisperButton(btn)

	def RecvWhisper(self, name):
		if not self.whisperDialogDict.has_key(name):
			btn = self.__FindWhisperButton(name)
			if 0 == btn:
				btn = self.__MakeWhisperButton(name)
				btn.Flash()
				if app.ENABLE_RECV_WHISPER_WINDOW_FLASH:
					app.StartFlashApplication()
				chat.AppendChat(chat.CHAT_TYPE_NOTICE, localeInfo.RECEIVE_MESSAGE % (name))
			else:
				btn.Flash()
				if app.ENABLE_RECV_WHISPER_WINDOW_FLASH:
					app.StartFlashApplication()
		elif self.IsGameMasterName(name):
			dlg = self.whisperDialogDict[name]

	def MakeWhisperButton(self, name):
		self.__MakeWhisperButton(name)

	def ShowWhisperDialog(self, btn):
		import app
		if app.IsPressed(app.DIK_LSHIFT) or app.IsPressed(app.DIK_RSHIFT):
			self.__DestroyWhisperButton(btn)
			chat.ClearBox(btn.name)
		else:
			try:
				self.__MakeWhisperDialog(btn.name)
				dlgWhisper = self.whisperDialogDict[btn.name]
				dlgWhisper.OpenWithTarget(btn.name)
				dlgWhisper.Show()
				self.__CheckGameMaster(btn.name)
			except:
				import dbg
				dbg.TraceError("interface.ShowWhisperDialog - Failed to find key")

			self.__DestroyWhisperButton(btn)

	def MinimizeWhisperDialog(self, name):

		if 0 != name:
			self.__MakeWhisperButton(name)

		self.CloseWhisperDialog(name)

	def CloseWhisperDialog(self, name):

		if 0 == name:

			if self.dlgWhisperWithoutTarget:
				self.dlgWhisperWithoutTarget.Destroy()
				self.dlgWhisperWithoutTarget = None

			return

		try:
			dlgWhisper = self.whisperDialogDict[name]
			dlgWhisper.Destroy()
			del self.whisperDialogDict[name]
		except:
			import dbg
			dbg.TraceError("interface.CloseWhisperDialog - Failed to find key")

	def __ArrangeWhisperButton(self):

		screenWidth = wndMgr.GetScreenWidth()
		screenHeight = wndMgr.GetScreenHeight()

		xPos = screenWidth - 70
		yPos = 170 * screenHeight / 600
		yCount = (screenHeight - 330) / 63
		#yCount = (screenHeight - 285) / 63

		count = 0
		for button in self.whisperButtonList:

			button.SetPosition(xPos + (int(count/yCount) * -50), yPos + (count%yCount * 63))
			count += 1

	def __FindWhisperButton(self, name):
		for button in self.whisperButtonList:
			if button.name == name:
				return button

		return 0

	def __MakeWhisperDialog(self, name):
		dlgWhisper = uiWhisper.WhisperDialog(self.MinimizeWhisperDialog, self.CloseWhisperDialog)
		dlgWhisper.BindInterface(self)
		dlgWhisper.LoadDialog()
		dlgWhisper.SetPosition(self.windowOpenPosition*30,self.windowOpenPosition*30)
		self.whisperDialogDict[name] = dlgWhisper

		self.windowOpenPosition = (self.windowOpenPosition+1) % 5

		return dlgWhisper

	def __MakeWhisperButton(self, name):
		whisperButton = uiWhisper.WhisperButton()
		
		if name == "[SwitchBot]": # ICON SWITCHBOT (Grimm)
			whisperButton.SetUpVisual("icon/item/71084.png")
			whisperButton.SetOverVisual("icon/item/71084.png")
			whisperButton.SetDownVisual("icon/item/71084.png")
		# elif self.IsGameMasterName(name):
			# whisperButton.SetUpVisual("locale/effect/gm_icon.png")
			# whisperButton.SetOverVisual("locale/effect/gm_icon.png")
			# whisperButton.SetDownVisual("locale/effect/gm_icon.png")
		else:
			whisperButton.SetUpVisual("d:/ymir work/ui/game/windows/btn_mail_up.sub")
			whisperButton.SetOverVisual("d:/ymir work/ui/game/windows/btn_mail_up.sub")
			whisperButton.SetDownVisual("d:/ymir work/ui/game/windows/btn_mail_up.sub")
		
		if self.IsGameMasterName(name):
			whisperButton.SetToolTipTextWithColor(name, 0xffffa200)
		else:
			whisperButton.SetToolTipText(name)
		whisperButton.ToolTipText.SetHorizontalAlignCenter()
		whisperButton.SetEvent(ui.__mem_func__(self.ShowWhisperDialog), whisperButton)
		whisperButton.Show()
		whisperButton.name = name

		self.whisperButtonList.insert(0, whisperButton)
		self.__ArrangeWhisperButton()

		return whisperButton

	def __DestroyWhisperButton(self, button):
		button.SetEvent(0)
		self.whisperButtonList.remove(button)
		self.__ArrangeWhisperButton()

	def HideAllWhisperButton(self):
		for btn in self.whisperButtonList:
			btn.Hide()

	def ShowAllWhisperButton(self):
		for btn in self.whisperButtonList:
			btn.Show()

	def __CheckGameMaster(self, name):
		if not self.listGMName.has_key(name):
			return
		if self.whisperDialogDict.has_key(name):
			dlg = self.whisperDialogDict[name]
			# dlg.SetGameMasterLook()

	def RegisterGameMasterName(self, name):
		if self.listGMName.has_key(name):
			return
		self.listGMName[name] = "GM"

	def IsGameMasterName(self, name):
		if self.listGMName.has_key(name):
			return True
		else:
			return False

	def RecoverWhispers(self):
		if constInfo.STORED_WHISPERS_FOR == player.GetName():
			for playerName in constInfo.STORED_WHISPERS:
				self.__MakeWhisperButton(playerName)

			self.ShowAllWhisperButton()
		else:
			chat.DestroyWhisper()
			
		# Reset (recovery was ok: already used - recovery was not ok: drop them anyway)
		constInfo.STORED_WHISPERS = []
		constInfo.STORED_WHISPERS_FOR = ""

	#####################################################################################

	#####################################################################################
	### Guild Building ###

	def BUILD_OpenWindow(self):
		self.wndGuildBuilding = uiGuild.BuildGuildBuildingWindow()
		self.wndGuildBuilding.Open()
		self.wndGuildBuilding.wnds = self.__HideWindows()
		self.wndGuildBuilding.SetCloseEvent(ui.__mem_func__(self.BUILD_CloseWindow))

	def BUILD_CloseWindow(self):
		self.__ShowWindows(self.wndGuildBuilding.wnds)
		self.wndGuildBuilding = None

	def BUILD_OnUpdate(self):
		if not self.wndGuildBuilding:
			return

		if self.wndGuildBuilding.IsPositioningMode():
			import background
			x, y, z = background.GetPickingPoint()
			self.wndGuildBuilding.SetBuildingPosition(x, y, z)
			
	def BUILD_OnMouseLeftButtonDown(self):
		if not self.wndGuildBuilding:
			return

		# GUILD_BUILDING
		if self.wndGuildBuilding.IsPositioningMode():
			self.wndGuildBuilding.SettleCurrentPosition()
			return True
		elif self.wndGuildBuilding.IsPreviewMode():
			pass
		else:
			return True
		# END_OF_GUILD_BUILDING
		return False

	def BUILD_OnMouseLeftButtonUp(self):
		if not self.wndGuildBuilding:
			return

		if not self.wndGuildBuilding.IsPreviewMode():
			return True

		return False

	def BULID_EnterGuildArea(self, areaID):
		# GUILD_BUILDING
		mainCharacterName = player.GetMainCharacterName()
		masterName = guild.GetGuildMasterName()

		if mainCharacterName != masterName:
			return

		if areaID != player.GetGuildID():
			return
		# END_OF_GUILD_BUILDING

		self.wndGameButton.ShowBuildButton()

	def BULID_ExitGuildArea(self, areaID):
		self.wndGameButton.HideBuildButton()

	#####################################################################################

	# if app.ENABLE_DEFENSE_WAVE:
	def BINARY_Update_Mast_HP(self, hp):
		self.wndMiniMap.SetMastHP(hp)

	def BINARY_Update_Mast_Window(self, i):
		self.wndMiniMap.SetMastWindow(i)
		
	def OpenShoutWindow(self):
		if self.wndShout.IsShow():
			self.wndShout.Hide()
		else:
			self.wndShout.Open()
			
	def IsEditLineFocus(self):
		if self.ChatWindow.chatLine.IsFocus():
			return 1

		if self.ChatWindow.chatToLine.IsFocus():
			return 1

		return 0

	def EmptyFunction(self):
		pass

	if app.WJ_ENABLE_TRADABLE_ICON:
		def SetOnTopWindow(self, onTopWnd):
			self.onTopWindow = onTopWnd

		def GetOnTopWindow(self):
			return self.onTopWindow

		def RefreshMarkInventoryBag(self):
			self.wndInventory.RefreshMarkSlots()
			self.wndCustomInventory.RefreshMarkSlots()
			
	if constInfo.FAST_INTERACTION_SAFEBOX == True:
		def GetInventoryPageIndex(self):
			if self.wndInventory:
				return self.wndInventory.GetInventoryPageIndex()
			else:
				return -1

		def AttachItemFromSafebox(self, slotIndex, itemIndex):
			if self.wndInventory and self.wndInventory.IsShow():
				self.wndInventory.AttachItemFromSafebox(slotIndex, itemIndex)

			return True

		def AttachInvenItemToOtherWindowSlot(self, slotWindow, slotIndex):
			if self.wndSafebox and self.wndSafebox.IsShow():
				return self.wndSafebox.AttachItemFromInventory(slotWindow, slotIndex)

			if self.dlgExchange and self.dlgExchange.IsShow():
				return self.dlgExchange.AttachItemFromInventory(slotWindow, slotIndex)

			return False
			