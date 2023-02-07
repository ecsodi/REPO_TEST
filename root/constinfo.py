import app
import ShapeSkin as chrmgr
import CacheEffect as player
import item
import chat
import localeInfo
import net
# Showing description of item in refine window.
ENABLE_REFINE_ITEM_DESCRIPTION = 1
NEW_NAME_DISTRIBUTION_PER_LINE = 1
TOOLTIP_KEYS_COLOR_HEX = 0xffffcc99
TOOLTIP_KEYS_COLOR_RGB = (92,122,234)

STORED_WHISPERS = []
STORED_WHISPERS_FOR = "" #playerName

BOT_DATA_LIST_INFO = []
BOT_DATA_LIST_GENERAL = []
BOT_NAME = "Deimos Helper"
QUESTION = ""
QUESTION_INFO = {}
ANSWER = {}

ENABLE_PASSIVE_SKILLS_HELPER = True
PASSIVE_SKILLS_DATA = {}

auto_shout_status = 0
auto_shout_text = ""
	
DEIMOS_INTERFACE = 0
END_TIME_BIO = 0
ENABLE_BIO_NOTIF = 0
IS_OPENED_OFFLINESHOP = 0
PY_LIVE = 0
DEIMOS_TITLEBAR = 1
WOLF_MAN = "ENABLED"	# ENABLED/DISABLED
WOLF_WOMEN = "DISABLED"	# ENABLED/DISABLED
FILTER_EMOJI_NOTICE = True # Filter emojis on tip notice or big notice to chat line

AUTO_HIDE_OPTION = False

FAST_INTERACTION_DELETE = True # Enable fast DELETE item
FAST_INTERACTION_SAFEBOX = True # Enable from inventar <-> safebox
FAST_INTERACTION_TRADE = True # Enable from inventar <-> exchange
FAST_INTERACTION_DICE = True # Enable from inventar <-> dice
FAST_INTERACTION_TRADE_X = 6 # How much lines in

if app.ENABLE_SELL_ITEM:
	def IsSellItems(itemVnum):
		item.SelectItem(itemVnum)
		itemPrice = item.GetISellItemPrice()
	
		if item.GetItemType() == item.ITEM_TYPE_METIN:
			return True
			
		# if itemPrice > 1:
			# return True
		
		LIST_DICT = [8633, 8634, 8635, 8636, 8637, 8638, 8639, 8640, 8641, 8642, 8643, 8644]
		
		for i in xrange(len(LIST_DICT)):
			if itemVnum == LIST_DICT[i]:
				return True

		return False

is_Safe = 1
ENABLE_COLOR_SCROLL = 0
ENABLE_NEW_LEVELSKILL_SYSTEM = 0
ENABLE_RANDOM_CHANNEL_SEL = 0
ENABLE_CLEAN_DATA_IF_FAIL_LOGIN = 0
ENABLE_PASTE_FEATURE = 1
ENABLE_FULLSTONE_DETAILS = 1
ENABLE_REFINE_PCT = 1
EXTRA_UI_FEATURE = 1
ALL_WINDOWS_HIDE_STATE = 1
NEW_678TH_SKILL_ENABLE = 0
ENABLE_EXPANDED_MONEY_TASKBAR = 1
ANTI_EXP_STATUS = 0
OPEN_GAME = None
CLICK_MISSIONS = 0
SET_MISSIONS = 0
BIG_BOARD = 0
AUTO_PICK_UP = 0

BLOCK_PVP_MAPS = ["metin2_map_guild_01", "metin2_map_t2", "metin2_map_t1", "metin2_map_guild_02", "metin2_map_guild_03", "gm_guild_build"]

## NEW_SKILL_PASSIVE
PASSIVE_SKILL_LV = [0,0,0,0,0,0,0,0,0,0,0,0]

DETECT_LEAKING_WINDOWS = False # turne this to false to disable leaking windows checking
if DETECT_LEAKING_WINDOWS:
	WINDOW_COUNT_OBJ = False # we only want to check leaking while we are in the game phase
	WINDOW_OBJ_COUNT = 0 # number of leaking window (only counting this if window_count_obj is true)
	WINDOW_OBJ_LIST = {} # here we store the init-ed but not del-ed (so currently allocated) windows
	WINDOW_OBJ_TRACE = [] # we store the curent stackstrace here
	WINDOW_TOTAL_OBJ_COUNT = 0 # number of total allocated windows

if app.ENABLE_SEND_TARGET_INFO:
	MONSTER_INFO_DATA = {}

IS_AUTO_REFINE = False
AUTO_REFINE_TYPE = 0
AUTO_REFINE_DATA = {
	"ITEM" : [-1, -1],
	"NPC" : [0, -1, -1, 0]
}

#COMPANION
COMPANION_ACTIVE_POS = -1
COMPANION_EVOLVE_ITEMS = {
	0 : { # EVOLVE FIRST
		0 :	[71124, 1],
		1 :	[71138, 200],
		2 :	[71138, 25],
		3 :	[71138, 35],
		4 :	[71138, 45],
	},
	
	1 : { # EVOLVE SECOND
		0 :	[711256, 32423],
		1 :	[711764,1325],
	},
	
	2 : { # EVOLVE THIRD
		0 :	[711256, 32423],
		1 :	[711764,1325],
	},
}

SelectJob = {
	'QID' : 0,
	'QCMD' : '',
}

USE_MONEY_K_FORMAT = True
import re
def ConvertMoneyText(text, powers = dict(k = 10**3, m = 10**6, b = 10**9)):
	match = re.search(r'(\d+)({:s}+)?'.format('+|'.join(powers.keys())), text, re.I)
	if match:
		moneyValue, suffixName = match.groups()
		moneyValue = int(moneyValue)
		if not suffixName:
			return moneyValue

		return moneyValue * (powers[suffixName[0]] ** len(suffixName))

	return 0

INPUT_IGNORE = 0
PVPMODE_ENABLE = 1
PVPMODE_TEST_ENABLE = 0
PVPMODE_ACCELKEY_ENABLE = 1
PVPMODE_ACCELKEY_DELAY = 0.5
PVPMODE_PROTECTED_LEVEL = 30
FOG_LEVEL0 = 3800.0
FOG_LEVEL1 = 12600.0
FOG_LEVEL2 = 20800.0
FOG_LEVEL = FOG_LEVEL2
FOG_LEVEL_LIST=[FOG_LEVEL0, FOG_LEVEL1, FOG_LEVEL2]
CAMERA_MAX_DISTANCE_SHORT = 2300.0
CAMERA_MAX_DISTANCE_LONG = 3500.0
CAMERA_MAX_DISTANCE_LIST=[CAMERA_MAX_DISTANCE_SHORT, CAMERA_MAX_DISTANCE_LONG]
CAMERA_MAX_DISTANCE = CAMERA_MAX_DISTANCE_LONG
CHRNAME_COLOR_INDEX = 0
ENVIRONMENT_NIGHT="d:/ymir work/environment/moonlight04.msenv"
Night = 0
HIGH_PRICE = 500000
MIDDLE_PRICE = 50000
ERROR_METIN_STONE = 28960
SUB2_LOADING_ENABLE = 1
EXPANDED_COMBO_ENABLE = 1
CONVERT_EMPIRE_LANGUAGE_ENABLE = 1
USE_ITEM_WEAPON_TABLE_ATTACK_BONUS = 0
ADD_DEF_BONUS_ENABLE = 1
LOGIN_COUNT_LIMIT_ENABLE = 0
USE_SKILL_EFFECT_UPGRADE_ENABLE = 1
VIEW_OTHER_EMPIRE_PLAYER_TARGET_BOARD = 1
GUILD_MONEY_PER_GSP = 100
GUILD_WAR_TYPE_SELECT_ENABLE = 1
TWO_HANDED_WEAPON_ATT_SPEED_DECREASE_VALUE = 0
HAIR_COLOR_ENABLE = 1
ARMOR_SPECULAR_ENABLE = 1
WEAPON_SPECULAR_ENABLE = 1
SEQUENCE_PACKET_ENABLE = 1
KEEP_ACCOUNT_CONNETION_ENABLE = 1
MINIMAP_POSITIONINFO_ENABLE = 1
MINIMAP_CLOCK_ENABLE = 1
CONVERT_EMPIRE_LANGUAGE_ENABLE = 0
USE_ITEM_WEAPON_TABLE_ATTACK_BONUS = 0
ADD_DEF_BONUS_ENABLE = 0
LOGIN_COUNT_LIMIT_ENABLE = 0
PVPMODE_PROTECTED_LEVEL = 15
TWO_HANDED_WEAPON_ATT_SPEED_DECREASE_VALUE = 10

ALREADY_NOTIFY_LIST = []
if app.ENABLE_INVENTORY_VIEWER:
	INVENTORY_VIEW_GM_LIST = []

isItemQuestionDialog = 0

def GET_ITEM_QUESTION_DIALOG_STATUS():
	global isItemQuestionDialog
	return isItemQuestionDialog

def SET_ITEM_QUESTION_DIALOG_STATUS(flag):
	global isItemQuestionDialog
	isItemQuestionDialog = flag

def GET_ITEM_DROP_QUESTION_DIALOG_STATUS():
	global isItemQuestionDialog
	return isItemQuestionDialog

def SET_ITEM_DROP_QUESTION_DIALOG_STATUS(flag):
	global isItemQuestionDialog
	isItemQuestionDialog = flag

def SET_DEFAULT_FOG_LEVEL():
	global FOG_LEVEL
	app.SetMinFog(FOG_LEVEL)

def SET_FOG_LEVEL_INDEX(index):
	global FOG_LEVEL
	global FOG_LEVEL_LIST
	try:
		FOG_LEVEL=FOG_LEVEL_LIST[index]
	except IndexError:
		FOG_LEVEL=FOG_LEVEL_LIST[0]
	app.SetMinFog(FOG_LEVEL)

def GET_FOG_LEVEL_INDEX():
	global FOG_LEVEL
	global FOG_LEVEL_LIST
	return FOG_LEVEL_LIST.index(FOG_LEVEL)

def SET_DEFAULT_CAMERA_MAX_DISTANCE():
	global CAMERA_MAX_DISTANCE
	app.SetCameraMaxDistance(CAMERA_MAX_DISTANCE)

def SET_CAMERA_MAX_DISTANCE_INDEX(index):
	global CAMERA_MAX_DISTANCE
	global CAMERA_MAX_DISTANCE_LIST
	try:
		CAMERA_MAX_DISTANCE=CAMERA_MAX_DISTANCE_LIST[index]
	except:
		CAMERA_MAX_DISTANCE=CAMERA_MAX_DISTANCE_LIST[0]

	app.SetCameraMaxDistance(CAMERA_MAX_DISTANCE)

def GET_CAMERA_MAX_DISTANCE_INDEX():
	global CAMERA_MAX_DISTANCE
	global CAMERA_MAX_DISTANCE_LIST
	return CAMERA_MAX_DISTANCE_LIST.index(CAMERA_MAX_DISTANCE)

def SET_DEFAULT_CHRNAME_COLOR():
	global CHRNAME_COLOR_INDEX
	chrmgr.SetEmpireNameMode(CHRNAME_COLOR_INDEX)

def SET_CHRNAME_COLOR_INDEX(index):
	global CHRNAME_COLOR_INDEX
	CHRNAME_COLOR_INDEX=index
	chrmgr.SetEmpireNameMode(index)

def GET_CHRNAME_COLOR_INDEX():
	global CHRNAME_COLOR_INDEX
	return CHRNAME_COLOR_INDEX

def SET_VIEW_OTHER_EMPIRE_PLAYER_TARGET_BOARD(index):
	global VIEW_OTHER_EMPIRE_PLAYER_TARGET_BOARD
	VIEW_OTHER_EMPIRE_PLAYER_TARGET_BOARD = index

def GET_VIEW_OTHER_EMPIRE_PLAYER_TARGET_BOARD():
	global VIEW_OTHER_EMPIRE_PLAYER_TARGET_BOARD
	return VIEW_OTHER_EMPIRE_PLAYER_TARGET_BOARD

def SET_DEFAULT_CONVERT_EMPIRE_LANGUAGE_ENABLE():
	global CONVERT_EMPIRE_LANGUAGE_ENABLE
	net.SetEmpireLanguageMode(CONVERT_EMPIRE_LANGUAGE_ENABLE)

def SET_DEFAULT_USE_ITEM_WEAPON_TABLE_ATTACK_BONUS():
	global USE_ITEM_WEAPON_TABLE_ATTACK_BONUS
	player.SetWeaponAttackBonusFlag(USE_ITEM_WEAPON_TABLE_ATTACK_BONUS)

def SET_DEFAULT_USE_SKILL_EFFECT_ENABLE():
	global USE_SKILL_EFFECT_UPGRADE_ENABLE
	app.SetSkillEffectUpgradeEnable(USE_SKILL_EFFECT_UPGRADE_ENABLE)

def SET_TWO_HANDED_WEAPON_ATT_SPEED_DECREASE_VALUE():
	global TWO_HANDED_WEAPON_ATT_SPEED_DECREASE_VALUE
	app.SetTwoHandedWeaponAttSpeedDecreaseValue(TWO_HANDED_WEAPON_ATT_SPEED_DECREASE_VALUE)


ACCESSORY_MATERIAL_LIST = [50623, 50624, 50625, 50626, 50627, 50628, 50629, 50630, 50631, 50632, 50633, 50634, 50635, 50636, 50637, 50638, 50639]
JewelAccessoryInfos = [
		# jewel		wrist	neck	ear
		[ 50634,	14420,	16220,	17220 ],
		[ 50635,	14500,	16500,	17500 ],
		[ 50636,	14520,	16520,	17520 ],
		[ 50637,	14540,	16540,	17540 ],
		[ 50638,	14560,	16560,	17560 ],
		[ 50639,	14570,	16570,	17570 ],
	]
	
def GET_ACCESSORY_MATERIAL_VNUM(vnum, subType):
	ret = vnum
	item_base = (vnum / 10) * 10
	for info in JewelAccessoryInfos:
		if item.ARMOR_WRIST == subType:
			if info[1] == item_base:
				return info[0]
		elif item.ARMOR_NECK == subType:
			if info[2] == item_base:
				return info[0]
		elif item.ARMOR_EAR == subType:
			if info[3] == item_base:
				return info[0]

	if vnum >= 16210 and vnum <= 16219:
		return 50625

	if item.ARMOR_WRIST == subType:
		WRIST_ITEM_VNUM_BASE = 14000
		ret -= WRIST_ITEM_VNUM_BASE
	elif item.ARMOR_NECK == subType:
		NECK_ITEM_VNUM_BASE = 16000
		ret -= NECK_ITEM_VNUM_BASE
	elif item.ARMOR_EAR == subType:
		EAR_ITEM_VNUM_BASE = 17000
		ret -= EAR_ITEM_VNUM_BASE

	type = ret/20

	if type<0 or type>=len(ACCESSORY_MATERIAL_LIST):
		type = (ret-170) / 20
		if type<0 or type>=len(ACCESSORY_MATERIAL_LIST):
			return 0

	return ACCESSORY_MATERIAL_LIST[type]

def GET_BELT_MATERIAL_VNUM(vnum, subType = 0):
	return 18900

def IS_AUTO_POTION(itemVnum):
	return IS_AUTO_POTION_HP(itemVnum) or IS_AUTO_POTION_SP(itemVnum)

def IS_AUTO_POTION_HP(itemVnum):
	if 72723 <= itemVnum and 72726 >= itemVnum:
		return 1
	# elif itemVnum >= 61020 and itemVnum <= 61026:
		# return 1
	elif itemVnum >= 76021 and itemVnum <= 76022:
		return 1
	elif itemVnum == 79012:
		return 1

	return 0

def IS_AUTO_POTION_SP(itemVnum):
	if 72727 <= itemVnum and 72730 >= itemVnum:
		return 1
	elif itemVnum >= 76004 and itemVnum <= 76005:
		return 1
	elif itemVnum == 79013:
		return 1
	elif itemVnum >= 55701 and itemVnum <= 55708:
		return 1
				
	return 0

def IS_BLEND_ITEM(itemVnum):
	if itemVnum == 0:
		return 0
		
	item.SelectItem(itemVnum)
	itemType = item.GetItemType()
	
	if itemType == item.ITEM_TYPE_BLEND:
		return 1
		
	return 0

# NEW_INVENTORY

def IsItemMovable(ItemVnum):
	if IsItemBook(ItemVnum) or IsItemStone(ItemVnum) or IsItemUpgrade(ItemVnum) or IsItemChest(ItemVnum):
		return True
		
	return False

def IsItemBook(ItemVnum):
	if ItemVnum == 0:
		return False
	
	item.SelectItem(ItemVnum)
		
	LIST_DICT = [50300, 25100, 76028, 71094, 70102, 98928, 98929, 98930, 98931, 98932, 98933, 98934, 98935, 98936, 98937, 98938, 98939, 98940, 98941, 98942, 98943]
	
	for i in xrange(len(LIST_DICT)):
		if ItemVnum == LIST_DICT[i]:
			return True

		
	return False
	
def IsItemStone(ItemVnum):
	if ItemVnum == 0:
		return False
	
	item.SelectItem(ItemVnum)
	
	if item.GetItemType() == item.ITEM_TYPE_METIN:
		return True
		
	return False
	
def IsItemUpgrade(ItemVnum):
	if ItemVnum == 0:
		return False
	
	item.SelectItem(ItemVnum)
	
	if item.GetItemType() == item.ITEM_TYPE_MATERIAL:
		return True
		
	return False
	
def IsItemChest(ItemVnum):
	if ItemVnum == 0:
		return False
	
	item.SelectItem(ItemVnum)
	
	if item.GetItemType() == item.ITEM_TYPE_GIFTBOX:
		return True
		
	if item.GetUseType(ItemVnum) == "USE_CHANGE_ATTRIBUTE":
		return True

	if item.GetUseType(ItemVnum) == "USE_ADD_ATTRIBUTE":
		return True
	
	if item.GetUseType(ItemVnum) == "USE_ADD_ATTRIBUTE_COSTUME":
		return True
		
	if item.GetUseType(ItemVnum) == "USE_CHANGE_ATTRIBUTE_COSTUME":
		return True
		
	LIST_DICT = [8633, 8634, 8635, 8636, 8637, 8638, 8639, 8640, 8641, 8642, 8643, 8644, 39030, 71001, 50513, 32323, 32322]
	
	for i in xrange(len(LIST_DICT)):
		if ItemVnum == LIST_DICT[i]:
			return True
		
	return False


LW = {}
LW["a"] = 8
LW["b"] = 7
LW["c"] = 7
LW["d"] = 7
LW["e"] = 7
LW["f"] = 5
LW["g"] = 7
LW["h"] = 7
LW["i"] = 5
LW["j"] = 5
LW["k"] = 6
LW["l"] = 5
LW["m"] = 11
LW["n"] = 7
LW["o"] = 6
LW["p"] = 7
LW["q"] = 7
LW["r"] = 5
LW["s"] = 7
LW["t"] = 5
LW["u"] = 7
LW["v"] = 7
LW["w"] = 9
LW["x"] = 7
LW["y"] = 7
LW["z"] = 7
LW["A"] = 9
LW["B"] = 8
LW["C"] = 8
LW["D"] = 9
LW["E"] = 8
LW["F"] = 8
LW["G"] = 9
LW["H"] = 9
LW["I"] = 6
LW["J"] = 7
LW["K"] = 9
LW["L"] = 8
LW["M"] = 11
LW["N"] = 9
LW["O"] = 9
LW["P"] = 9
LW["Q"] = 9
LW["R"] = 9
LW["S"] = 8
LW["T"] = 7
LW["U"] = 9
LW["V"] = 9
LW["W"] = 11
LW["X"] = 9
LW["Y"] = 9
LW["Z"] = 8
LW["0"] = 7
LW["1"] = 5
LW["2"] = 7
LW["3"] = 7
LW["4"] = 7
LW["5"] = 7
LW["6"] = 7
LW["7"] = 7
LW["8"] = 7
LW["9"] = 7
LW[" "] = 3
LW["!"] = 3
LW["?"] = 6
LW["("] = 4
LW[")"] = 4
LW["\\"] = 5
LW["/"] = 5
LW["\""] = 3
LW["'"] = 3
LW[":"] = 4
LW[";"] = 4
LW["|"] = 3
LW["&gt;"] = 7
LW["&lt;"] = 7
LW["."] = 4
LW[","] = 4
LW["*"] = 8
LW["-"] = 11
LW["+"] = 8
LW["="] = 8
LW["@"] = 13
LW["#"] = 10
LW["$"] = 9
LW["%"] = 12
LW["^"] = 7
LW["&"] = 11
LW["~"] = 8
LW["`"] = 5
LW["_"] = 8
LW["{"] = 5
LW["}"] = 5
LW[""] = 0
LW["	"] = 16

def GetLengthOfString(string):
	global LW
	len = 0
	for s in string:
		try:
			len += LW[s]
		except:
			len += 0
	return len
	
_interface_instance = None
def GetInterfaceInstance():
	global _interface_instance
	return _interface_instance
def SetInterfaceInstance(instance):
	global _interface_instance
	if _interface_instance:
		del _interface_instance
	_interface_instance = instance

def StripColor(text):
	import re

	regex = '\|c([a-zA-Z0-9]){0,8}|'
	search = re.search(regex, text)
	if search:
		text = re.sub(regex, '', text)

	return text
	
def StripHyperlink(text):
	import re

	regex = '\|H.*\|h'
	search = re.search(regex, text)
	if search:
		# return True
		text = re.sub(regex, '', text)

	return text
	
def EmojiFilter(text):
	import re

	EMOJI_DIC = {
		'<1>' : 'icon/emoji/chat/1',
		'<2>' : 'icon/emoji/chat/2',
		'<3>' : 'icon/emoji/chat/3',
		'<4>' : 'icon/emoji/chat/4',
		'<5>' : 'icon/emoji/chat/5',
		'<6>' : 'icon/emoji/chat/6',
		'<7>' : 'icon/emoji/chat/7',
		'<8>' : 'icon/emoji/chat/8',
		'<9>' : 'icon/emoji/chat/9',
		'<10>' : 'icon/emoji/chat/10',
		'<11>' : 'icon/emoji/chat/11',
		'<12>' : 'icon/emoji/chat/12',
		'<13>' : 'icon/emoji/chat/13',
		'<14>' : 'icon/emoji/chat/14',
		'<15>' : 'icon/emoji/chat/15',
		'<16>' : 'icon/emoji/chat/16',
		'<17>' : 'icon/emoji/chat/17',
		'<18>' : 'icon/emoji/chat/18',
		'<19>' : 'icon/emoji/chat/19',
		'<20>' : 'icon/emoji/chat/20',
		'<21>' : 'icon/emoji/chat/21',
		'<22>' : 'icon/emoji/chat/22',
		'<23>' : 'icon/emoji/chat/23',
		'<24>' : 'icon/emoji/chat/24',
		'<25>' : 'icon/emoji/chat/25',
		'<26>' : 'icon/emoji/chat/26',
		'<27>' : 'icon/emoji/chat/27',
		'<28>' : 'icon/emoji/chat/28',
		'<29>' : 'icon/emoji/chat/29',
		'<30>' : 'icon/emoji/chat/30',
		'<31>' : 'icon/emoji/chat/31',
		'<32>' : 'icon/emoji/chat/32',
		'<33>' : 'icon/emoji/chat/33',
		'<34>' : 'icon/emoji/chat/34',
		'<35>' : 'icon/emoji/chat/35',
		'<36>' : 'icon/emoji/chat/36',
	}

	for emoji_str, emoji_img in EMOJI_DIC.iteritems():
		text = text.replace(emoji_str, "|E" + emoji_img + ".png|e")

	return text