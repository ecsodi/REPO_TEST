import localeInfo
import CacheEffect as player
import ShapeSkin as chrmgr
import Collision as chr

NamePoint = "Points"
EMOTION_VERSION = 2

if EMOTION_VERSION == 2:
	EMOTION_CLAP = 1
	EMOTION_CONGRATULATION = 2
	EMOTION_FORGIVE = 3
	EMOTION_ANGRY = 4
	EMOTION_ATTRACTIVE = 5
	EMOTION_SAD = 6
	EMOTION_SHY = 7
	EMOTION_CHEERUP = 8
	EMOTION_BANTER = 9
	EMOTION_JOY = 10
	EMOTION_CHEERS_1 = 11
	EMOTION_CHEERS_2 = 12
	EMOTION_DANCE_1 = 13
	EMOTION_DANCE_2 = 14
	EMOTION_DANCE_3 = 15
	EMOTION_DANCE_4 = 16
	EMOTION_DANCE_5 = 17
	EMOTION_DANCE_6 = 18
	EMOTION_KISS = 51
	EMOTION_FRENCH_KISS = 52
	EMOTION_SLAP = 53
	NAME_ACTION_NEW1 = 60
	NAME_ACTION_NEW2 = 61
	NAME_ACTION_NEW3 = 62
	NAME_ACTION_NEW4 = 63
	NAME_ACTION_NEW5 = 64
	NAME_ACTION_NEW6 = 65
	NAME_ACTION_NEW7 = 66
	NAME_ACTION_NEW8 = 67
	NAME_ACTION_NEW9 = 68
	NAME_ACTION_NEW10 = 69
	NAME_ACTION_NEW11 = 70
	NAME_ACTION_NEW12 = 71

	EMOTION_DICT = {
		
		EMOTION_CLAP :				{"emotion_key" : chr.MOTION_CLAP ,"name": localeInfo.EMOTION_CLAP, 		"command":"/clap"},
		EMOTION_CHEERS_1 :			{"emotion_key" : chr.MOTION_CHEERS_1 ,"name": localeInfo.EMOTION_CHEERS_1, 	"command":"/cheer1"},
		EMOTION_CHEERS_2 :			{"emotion_key" : chr.MOTION_CHEERS_2 ,"name": localeInfo.EMOTION_CHEERS_2, 	"command":"/cheer2"},
		EMOTION_DANCE_1 :			{"emotion_key" : chr.MOTION_DANCE_1 ,"name": localeInfo.EMOTION_DANCE_1, 	"command":"/dance1"},
		EMOTION_DANCE_2 :			{"emotion_key" : chr.MOTION_DANCE_2 ,"name": localeInfo.EMOTION_DANCE_2, 	"command":"/dance2"},
		EMOTION_DANCE_3 :			{"emotion_key" : chr.MOTION_DANCE_3 ,"name": localeInfo.EMOTION_DANCE_3, 	"command":"/dance3"},
		EMOTION_DANCE_4 :			{"emotion_key" : chr.MOTION_DANCE_4 ,"name": localeInfo.EMOTION_DANCE_4, 	"command":"/dance4"},
		EMOTION_DANCE_5 :			{"emotion_key" : chr.MOTION_DANCE_5 ,"name": localeInfo.EMOTION_DANCE_5, 	"command":"/dance5"},
		EMOTION_DANCE_6 :			{"emotion_key" : chr.MOTION_DANCE_6 ,"name": "Dans 6", 	"command":"/dance6"},

		EMOTION_CONGRATULATION :	{"emotion_key" : chr.MOTION_CONGRATULATION ,"name": localeInfo.EMOTION_CONGRATULATION,	"command":"/congratulation"},
		EMOTION_FORGIVE :			{"emotion_key" : chr.MOTION_FORGIVE ,"name": localeInfo.EMOTION_FORGIVE, 	"command":"/forgive"},
		EMOTION_ANGRY :				{"emotion_key" : chr.MOTION_ANGRY ,"name": localeInfo.EMOTION_ANGRY, 		"command":"/angry"},
		EMOTION_ATTRACTIVE :		{"emotion_key" : chr.MOTION_ATTRACTIVE ,"name": localeInfo.EMOTION_ATTRACTIVE, 	"command":"/attractive"},
		EMOTION_SAD :				{"emotion_key" : chr.MOTION_SAD ,"name": localeInfo.EMOTION_SAD, 		"command":"/sad"},
		EMOTION_SHY :				{"emotion_key" : chr.MOTION_SHY ,"name": localeInfo.EMOTION_SHY, 		"command":"/shy"},
		EMOTION_CHEERUP :			{"emotion_key" : chr.MOTION_CHEERUP ,"name": localeInfo.EMOTION_CHEERUP, 	"command":"/cheerup"},
		EMOTION_BANTER :			{"emotion_key" : chr.MOTION_BANTER ,"name": localeInfo.EMOTION_BANTER, 	"command":"/banter"},
		EMOTION_JOY :				{"emotion_key" : chr.MOTION_JOY ,"name": localeInfo.EMOTION_JOY, 		"command":"/joy"},
		EMOTION_KISS :				{"emotion_key" : 255 ,"name": localeInfo.EMOTION_CLAP_KISS, 	"command":"/kiss"},
		EMOTION_FRENCH_KISS :		{"emotion_key" : 255 ,"name": localeInfo.EMOTION_FRENCH_KISS, 	"command":"/french_kiss"},
		EMOTION_SLAP :				{"emotion_key" : 255 ,"name": localeInfo.EMOTION_SLAP, 		"command":"/slap"},
			
		NAME_ACTION_NEW1 :			{"emotion_key" : chr.NAME_ACTION_NEW1 ,"name": "VIP Emotion", 		"command":"/new_action1"},
		NAME_ACTION_NEW2 :			{"emotion_key" : chr.NAME_ACTION_NEW2 ,"name": "VIP Emotion", 		"command":"/new_action2"},
		NAME_ACTION_NEW3 :			{"emotion_key" : chr.NAME_ACTION_NEW3 ,"name": "VIP Emotion", 		"command":"/new_action3"},
		NAME_ACTION_NEW4 :			{"emotion_key" : chr.NAME_ACTION_NEW4 ,"name": "VIP Emotion", 		"command":"/new_action4"},
		NAME_ACTION_NEW5 :			{"emotion_key" : chr.NAME_ACTION_NEW5 ,"name": "VIP Emotion", 		"command":"/new_action5"},
		NAME_ACTION_NEW6 :			{"emotion_key" : chr.NAME_ACTION_NEW6 ,"name": "VIP Emotion", 		"command":"/new_action6"},
		NAME_ACTION_NEW7 :			{"emotion_key" : chr.NAME_ACTION_NEW7 ,"name": "VIP Emotion", 		"command":"/new_action7"},
		NAME_ACTION_NEW8 :			{"emotion_key" : chr.NAME_ACTION_NEW8 ,"name": "VIP Emotion", 		"command":"/new_action8"},
		NAME_ACTION_NEW9 :			{"emotion_key" : chr.NAME_ACTION_NEW9 ,"name": "VIP Emotion", 		"command":"/new_action9"},
		NAME_ACTION_NEW10 :			{"emotion_key" : chr.NAME_ACTION_NEW10 ,"name": "VIP Emotion", 		"command":"/new_action10"},
		NAME_ACTION_NEW11 :			{"emotion_key" : chr.NAME_ACTION_NEW11 ,"name": "VIP Emotion", 		"command":"/new_action11"},
		NAME_ACTION_NEW12 :			{"emotion_key" : chr.NAME_ACTION_NEW12 ,"name": "VIP Emotion", 		"command":"/new_action12"},
	}

	ICON_DICT = {
		EMOTION_CLAP 				: 	"d:/ymir work/ui/game/windows/emotion_clap.sub",
		EMOTION_CHEERS_1			:	"d:/ymir work/ui/game/windows/emotion_cheers_1.sub",
		EMOTION_CHEERS_2			:	"d:/ymir work/ui/game/windows/emotion_cheers_2.sub",
		EMOTION_DANCE_1				:	"icon/action/dance1.tga",
		EMOTION_DANCE_2				:	"icon/action/dance2.tga",
		EMOTION_CONGRATULATION		:	"icon/action/congratulation.tga",
		EMOTION_FORGIVE				:	"icon/action/forgive.tga",
		EMOTION_ANGRY				:	"icon/action/angry.tga",
		EMOTION_ATTRACTIVE			:	"icon/action/attractive.tga",
		EMOTION_SAD					:	"icon/action/sad.tga",
		EMOTION_SHY					:	"icon/action/shy.tga",
		EMOTION_CHEERUP				:	"icon/action/cheerup.tga",
		EMOTION_BANTER				:	"icon/action/banter.tga",
		EMOTION_JOY					:	"icon/action/joy.tga",
		EMOTION_DANCE_1				:	"icon/action/dance1.tga",
		EMOTION_DANCE_2				:	"icon/action/dance2.tga",
		EMOTION_DANCE_3				:	"icon/action/dance3.tga",
		EMOTION_DANCE_4				:	"icon/action/dance4.tga",
		EMOTION_DANCE_5				:	"icon/action/dance5.tga",
		EMOTION_DANCE_6				:	"icon/action/dance6.tga",
		EMOTION_KISS				:	"d:/ymir work/ui/game/windows/emotion_kiss.sub",
		EMOTION_FRENCH_KISS			:	"d:/ymir work/ui/game/windows/emotion_french_kiss.sub",
		EMOTION_SLAP				:	"d:/ymir work/ui/game/windows/emotion_slap.sub",
		NAME_ACTION_NEW1 			:	"icon/action/charging.tga",
		NAME_ACTION_NEW2 			:	"icon/action/charging.tga",
		NAME_ACTION_NEW3 			:	"icon/action/charging.tga",
		NAME_ACTION_NEW4 			:	"icon/action/charging.tga",
		NAME_ACTION_NEW5 			:	"icon/action/charging.tga",
		NAME_ACTION_NEW6 			:	"icon/action/charging.tga",
		NAME_ACTION_NEW7 			:	"icon/action/charging.tga",
		NAME_ACTION_NEW8 			:	"icon/action/charging.tga",
		NAME_ACTION_NEW9 			:	"icon/action/charging.tga",
		NAME_ACTION_NEW10 			:	"icon/action/charging.tga",
		NAME_ACTION_NEW11 			:	"icon/action/charging.tga",
		NAME_ACTION_NEW12 			:	"icon/action/charging.tga",
	}

	ANI_DICT = {
		# chr.MOTION_CLAP : "clap.msa",
		chr.MOTION_CHEERS_1 : "cheers_1.msa",
		chr.MOTION_CHEERS_2 : "cheers_2.msa",
		chr.MOTION_DANCE_1 : "dance_1.msa",
		chr.MOTION_DANCE_2 : "dance_2.msa",
		chr.MOTION_DANCE_3 : "dance_3.msa",
		chr.MOTION_DANCE_4 : "dance_4.msa",
		chr.MOTION_DANCE_5 : "dance_5.msa",
		chr.MOTION_CONGRATULATION : "congratulation.msa",
		chr.MOTION_FORGIVE : "forgive.msa",
		chr.MOTION_ANGRY : "angry.msa",
		chr.MOTION_ATTRACTIVE : "attractive.msa",
		chr.MOTION_SAD : "sad.msa",
		chr.MOTION_SHY : "shy.msa",
		chr.MOTION_CHEERUP : "cheerup.msa",
		chr.MOTION_BANTER : "banter.msa",
		chr.MOTION_JOY : "joy.msa",
		chr.MOTION_FRENCH_KISS_WITH_WARRIOR : "french_kiss_with_warrior.msa",
		chr.MOTION_FRENCH_KISS_WITH_ASSASSIN : "french_kiss_with_assassin.msa",
		chr.MOTION_FRENCH_KISS_WITH_SURA : "french_kiss_with_sura.msa",
		chr.MOTION_FRENCH_KISS_WITH_SHAMAN : "french_kiss_with_shaman.msa",
		chr.MOTION_KISS_WITH_WARRIOR : "kiss_with_warrior.msa",
		chr.MOTION_KISS_WITH_ASSASSIN : "kiss_with_assassin.msa",
		chr.MOTION_KISS_WITH_SURA : "kiss_with_sura.msa",
		chr.MOTION_KISS_WITH_SHAMAN : "kiss_with_shaman.msa",
		chr.MOTION_SLAP_HIT_WITH_WARRIOR : "slap_hit.msa",
		chr.MOTION_SLAP_HIT_WITH_ASSASSIN :	"slap_hit.msa",
		chr.MOTION_SLAP_HIT_WITH_SURA : "slap_hit.msa",
		chr.MOTION_SLAP_HIT_WITH_SHAMAN : "slap_hit.msa",
		chr.MOTION_SLAP_HURT_WITH_WARRIOR : "slap_hurt.msa",
		chr.MOTION_SLAP_HURT_WITH_ASSASSIN : "slap_hurt.msa",
		chr.MOTION_SLAP_HURT_WITH_SURA : "slap_hurt.msa",
		chr.MOTION_SLAP_HURT_WITH_SHAMAN : "slap_hurt.msa",
		
		chr.NAME_ACTION_NEW1 :  "breakdance_freeze_var_3.msa",
		chr.NAME_ACTION_NEW2 :  "drop_kick.msa",
		chr.NAME_ACTION_NEW3 :  "entry.msa",
		chr.NAME_ACTION_NEW4 :  "flying_knee_punch_combo.msa",
		chr.NAME_ACTION_NEW5 :  "hip_hop_dancing.msa",
		chr.NAME_ACTION_NEW6 :  "joyful_jump.msa",
		chr.NAME_ACTION_NEW7 :  "kick_to_the_groin.msa",
		chr.NAME_ACTION_NEW8 :  "martelo_2.msa",
		chr.NAME_ACTION_NEW9 :  "offensive_idle.msa",
		chr.NAME_ACTION_NEW10 :  "salute.msa",
		chr.NAME_ACTION_NEW11 :  "soccer_trip.msa",
		chr.NAME_ACTION_NEW12 :  "swing_dancing.msa",
		
	
	}

def __RegisterSharedEmotionAnis(mode, path):
	chrmgr.SetPathName(path)
	chrmgr.RegisterMotionMode(mode)

	for key, val in ANI_DICT.items():
		chrmgr.Character(NamePoint, mode, key, val)

def RegisterEmotionAnis(path):
	actionPath = path + "action/"
	weddingPath = path + "wedding/"

	__RegisterSharedEmotionAnis(chr.NEW_678TH_SKILL_ENABLE, actionPath)
	__RegisterSharedEmotionAnis(chr.MOTION_MODE_WEDDING_DRESS, actionPath)

	chrmgr.SetPathName(weddingPath)
	chrmgr.RegisterMotionMode(chr.MOTION_MODE_WEDDING_DRESS)
	chrmgr.Character(NamePoint, chr.MOTION_MODE_WEDDING_DRESS, chr.MOTION_WAIT, "wait.msa")
	chrmgr.Character(NamePoint, chr.MOTION_MODE_WEDDING_DRESS, chr.MOTION_WALK, "walk.msa")
	chrmgr.Character(NamePoint, chr.MOTION_MODE_WEDDING_DRESS, chr.MOTION_RUN, "walk.msa")

def RegisterEmotionIcons():
	for key, val in ICON_DICT.items():
		player.RegisterEmotionIcon(key, val)