import uiScriptLocale
import localeInfo
ROOT_PATH = "d:/ymir work/ui/public/"
ROOT_PATH_NEW = "d:/ymir work/ui/game/select_interface/"
ROOT_PATH_NEW_CHR = "d:/ymir work/ui/game/select_interface/create/"
LOCALE_PATH = uiScriptLocale.SELECT_PATH	#uiScriptLocale.SELECT_PATH  D:\ymir work\ui\intro\949_select\

BOARD_X = SCREEN_WIDTH * (25) / 800
BOARD_Y = SCREEN_HEIGHT * (156) / 600

X_GAP = 11
Y_GAP = 12

NAME_X = 18
NAME_Y = 95
NAME_SCALE_X = 0.65
NAME_SCALE_Y = 0.65
FACE_X = 7
FACE_Y = 4
SELECT_BTN_X = X_GAP#12
SELECT_BTN_Y = 6
SELECT_BTN_GAP = 72#49


SMALL_NAME_X = 150 - 65
SMALL_NAME_Y = 6
SMALL_NAME_SCALE_X = 1.0
SMALL_NAME_SCALE_Y = 1.0

FLAG_SCALE_X = 0.45
FLAG_SCALE_Y = 0.45

SHADOW_SCALE_X = 3.0 * SCREEN_WIDTH  / 800.0
SHADOW_SCALE_Y = 2.0 * SCREEN_HEIGHT / 600.0

STAT_GAUGE_X = X_GAP + 15
STAT_GAUGE_Y = 286
STAT_GAUGE_BAR_X = 40
STAT_GAUGE_BAR_WIDTH = 195
STAT_GAUGE_GAP = 18
STAT_GAUGE_TEXT_WIDTH = 21
STAT_GAUGE_TEXT_HEIGHT = 13

#THINBOARD_GOLD_WIDTH = 198#194
THINBOARD_GOLD_HEIGHT = 364#359

THINBOARD_CIRCLE_LEFT_WIDTH = 175

#SELECT_Y = BOARD_Y + 312 + 7

THINBOARD_CIRCLE_RIGHT_WIDTH = 180
THINBOARD_CIRCLE_RIGHT_HEIGHT = 270
###################

window = {
	"name" : "New_CreateCharacterWindow",
	"x" : 0,
	"y" : 0,
	"width" : SCREEN_WIDTH,
	"height" : SCREEN_HEIGHT,
	"children"	:
	(
		## BackGround##
		{
			"name" : "Background", "type" : "expanded_image", "x" : 0, "y" : 0, "x_scale" : float(SCREEN_WIDTH) / 1920.0, "y_scale" : float(SCREEN_HEIGHT) / 1080.0,
			"image" : ROOT_PATH_NEW + "background.png",
		},

		{
			"name" : "character_board", 
			"type" : "image",

			"x" : BOARD_X,
			"y" : BOARD_Y,
			

			"image" : ROOT_PATH_NEW + "create/select_character_window.png",
			
			
			"children" :
			(
				{	
					"name" : "WARRIOR",	"type" : "radio_button", 
					"x" : SELECT_BTN_X+5, "y" : SELECT_BTN_Y + SELECT_BTN_GAP+10,
					"default_image" : ROOT_PATH_NEW_CHR + "warrior.png",
					"over_image"	: ROOT_PATH_NEW_CHR + "warrior_over.png",
					"down_image"	: ROOT_PATH_NEW_CHR + "warrior_selected.png",
				},
				{
					"name" : "ASSASSIN", "type" : "radio_button",
					"x" : SELECT_BTN_X+5, "y" : SELECT_BTN_Y + SELECT_BTN_GAP*2+10,
					"default_image" : ROOT_PATH_NEW_CHR + "ninja.png",
					"over_image"	: ROOT_PATH_NEW_CHR + "ninja_over.png",
					"down_image"	: ROOT_PATH_NEW_CHR + "ninja_selected.png",
				},
				{
					"name" : "SURA", "type" : "radio_button",
					"x" : SELECT_BTN_X+5, "y" : SELECT_BTN_Y + SELECT_BTN_GAP*3+10,
					"default_image" : ROOT_PATH_NEW_CHR + "sura.png",
					"over_image"	: ROOT_PATH_NEW_CHR + "sura_over.png",
					"down_image"	: ROOT_PATH_NEW_CHR + "sura_selected.png",
				},
				{
					"name" : "SHAMAN", "type" : "radio_button",
					"x" : SELECT_BTN_X+5, "y" : SELECT_BTN_Y + SELECT_BTN_GAP*4+10,
					"default_image" : ROOT_PATH_NEW_CHR + "shaman.png",
					"over_image"	: ROOT_PATH_NEW_CHR + "shaman_over.png",
					"down_image"	: ROOT_PATH_NEW_CHR + "shaman_selected.png",
				},
				{
					"name" : "WOLF", "type" : "radio_button",
					"x" : SELECT_BTN_X+5, "y" : SELECT_BTN_Y + SELECT_BTN_GAP*5+10,
					"default_image" : ROOT_PATH_NEW_CHR + "lycan.png",
					"over_image"	: ROOT_PATH_NEW_CHR + "lycan_over.png",
					"down_image"	: ROOT_PATH_NEW_CHR + "lycan_selected.png",
				},
				
				{ "name" : "CharacterFace_0", "type" : "image", "x" : SELECT_BTN_X - FACE_X+19, "y" : SELECT_BTN_Y + SELECT_BTN_GAP+15 				   - FACE_Y, "image" : "D:/ymir work/ui/game/select_interface/faces/icon_mwarrior.png"},
				{ "name" : "CharacterFace_1", "type" : "image", "x" : SELECT_BTN_X - FACE_X+19, "y" : SELECT_BTN_Y + SELECT_BTN_GAP*2+15   - FACE_Y, "image" : "D:/ymir work/ui/game/select_interface/faces/icon_mninja.png"},
				{ "name" : "CharacterFace_2", "type" : "image", "x" : SELECT_BTN_X - FACE_X+19, "y" : SELECT_BTN_Y + SELECT_BTN_GAP*3+15 - FACE_Y, "image" : "D:/ymir work/ui/game/select_interface/faces/icon_msura.png"},
				{ "name" : "CharacterFace_3", "type" : "image", "x" : SELECT_BTN_X - FACE_X+19, "y" : SELECT_BTN_Y + SELECT_BTN_GAP*4+15 - FACE_Y, "image" : "D:/ymir work/ui/game/select_interface/faces/icon_mshaman.png"},
				{ "name" : "CharacterFace_4", "type" : "image", "x" : SELECT_BTN_X - FACE_X+19, "y" : SELECT_BTN_Y + SELECT_BTN_GAP*5+15 - FACE_Y, "image" : "D:/ymir work/ui/game/select_interface/faces/icon_mlykaner.png"},
				
				{
					"name" : "EmpireFlag_B", "type" : "expanded_image",
					"x" : 25, "y" : 12,
					"image" : "d:/ymir work/ui/game/select_interface/yellow_kingdom.png"
				},
				{
					"name" : "EmpireFlag_C", "type" : "expanded_image",
					"x" : 25, "y" : 12,
					"image" : "d:/ymir work/ui/game/select_interface/blue_king.png"
				},
				{
					"name" : "EmpireFlag_A", "type" : "expanded_image",
					"x" : 25, "y" : 12,
					"image" : "d:/ymir work/ui/game/select_interface/red_kingdom.png"
				},
				{
					"name" : "gender_button_01", "type" : "radio_button",
					"x" : X_GAP + 4 + 6, "y" : 14 + SELECT_BTN_GAP*5 +21 + 67,

					"default_image" : ROOT_PATH_NEW_CHR + "male.png",
					"over_image"	: ROOT_PATH_NEW_CHR + "male_over.png",
					"down_image"	: ROOT_PATH_NEW_CHR + "male_selected.png",
				},
				{
					"name" : "gender_button_02", "type" : "radio_button",
					"x" : X_GAP + 4 + 6 + 45, "y" : 14 + SELECT_BTN_GAP*5 +21 + 67,
									
					"default_image" : ROOT_PATH_NEW_CHR + "female.png",
					"over_image"	: ROOT_PATH_NEW_CHR + "female_over.png",
					"down_image"	: ROOT_PATH_NEW_CHR + "female_selected.png",
				},

				{
					"name" : "shape_button_01", "type" : "radio_button",
					"x" : 153 + X_GAP + 4 + 6 + 100, "y" : 14 + SELECT_BTN_GAP*5 +21 + 67,

					"default_image" : ROOT_PATH_NEW_CHR + "1.png",
					"over_image"	: ROOT_PATH_NEW_CHR + "1_over.png",
					"down_image"	: ROOT_PATH_NEW_CHR + "1_selected.png",
				},
				{
					"name" : "shape_button_02", "type" : "radio_button",
					"x" : 153 + X_GAP + 4 + 6 + 100 + 45, "y" : 14 + SELECT_BTN_GAP*5 +21 + 67,

					"default_image" : ROOT_PATH_NEW_CHR + "2.png",
					"over_image"	: ROOT_PATH_NEW_CHR + "2_over.png",
					"down_image"	: ROOT_PATH_NEW_CHR + "2_selected.png",
				},
				
			), #Character children
		},##Character Board(Left)##

		{
			"name" : "character_discriptionboard",
			"type" : "image",

			"x" : SCREEN_WIDTH - BOARD_X - (290 + (X_GAP * 2)),
			"y" : SCREEN_HEIGHT * (256) / 600,

			"image" : ROOT_PATH_NEW + "create/character_stats.png",
			
			"children"	:
			(
				## stat Images
				{	"name":"hth_img",			"type" : "image",	"x" : STAT_GAUGE_X+4, "y" : 48+15, "image":"d:/ymir work/ui/game/windows/char_info_con.sub",			},
				{	"name":"int_img",			"type" : "image",	"x" : STAT_GAUGE_X+4,	"y" : 50 + 20+15, "image":"d:/ymir work/ui/game/windows/char_info_int.sub",			},
				{	"name":"str_img",			"type" : "image",	"x" : STAT_GAUGE_X+4, "y" : 52 + 20 + 20+15, "image":"d:/ymir work/ui/game/windows/char_info_str.sub",			},
				{	"name":"dex_img",			"type" : "image",	"x" : STAT_GAUGE_X+4, "y" : 54 + 20 + 20 +20+15, "image":"d:/ymir work/ui/game/windows/char_info_dex.sub",			},
				{
					"name" : "hth",
					"type" : "text",
					"x" : STAT_GAUGE_X,
					"y" : 53+15,
					"children" :
					(
						{
							"name" : "hth_gauge",
							"type" : "gauge",
							"x" : STAT_GAUGE_BAR_X,
							"y" : 4,
							"width" : STAT_GAUGE_BAR_WIDTH,
							"color" : "red",
						},
						{
							"name" : "hth_slot",
							
							"x" : STAT_GAUGE_BAR_WIDTH + STAT_GAUGE_BAR_X + 7,
							"y" : -1,
							
							"width" : STAT_GAUGE_TEXT_WIDTH,
							"height" : STAT_GAUGE_TEXT_HEIGHT,
							
							
							"children" :
							(
								{
									"name" : "hth_value",
									"type" : "text",
									"x" : 0,
									"y" : 1,
									"all_align" : "center",
									"text" : "0",
								},
							),
						},
					),
				},
				{
					"name" : "int",
					"type" : "text",
					"x" : STAT_GAUGE_X,
					"y" : 56+18+15,
					"children" :
					(
						{
							"name" : "int_gauge",
							"type" : "gauge",
							"x" : STAT_GAUGE_BAR_X,
							"y" : 4,
							"width" : STAT_GAUGE_BAR_WIDTH,
							"color" : "pink",
						},
						{
							"name" : "int_slot",
							
							"x" : STAT_GAUGE_BAR_WIDTH + STAT_GAUGE_BAR_X + 7,
							"y" : -1,
							
							"width" : STAT_GAUGE_TEXT_WIDTH,
							"height" : STAT_GAUGE_TEXT_HEIGHT,
							
							"children" :
							(
								{
									"name" : "int_value",
									"type" : "text",
									"x" : 0,
									"y" : 1,
									"all_align" : "center",
									"text" : "0",
								},
							),
						},
					),
				},
				{
					"name" : "str",
					"type" : "text",
					"x" : STAT_GAUGE_X,
					"y" : 60+18+18+15,
					"children" :
					(
						{
							"name" : "str_gauge",
							"type" : "gauge",
							"x" : STAT_GAUGE_BAR_X,
							"y" : 4,
							"width" : STAT_GAUGE_BAR_WIDTH,
							"color" : "purple",
						},
						{
							"name" : "str_slot",
							"x" : STAT_GAUGE_BAR_WIDTH + STAT_GAUGE_BAR_X + 7,
							"y" : -1,
							
							"width" : STAT_GAUGE_TEXT_WIDTH,
							"height" : STAT_GAUGE_TEXT_HEIGHT,
							"children" :
							(
								{
									"name" : "str_value",
									"type" : "text",
									"x" : 0,
									"y" : 1,
									"all_align" : "center",
									"text" : "0",
								},
							),
						},
					),
				},
				{
					"name" : "dex",
					"type" : "text",
					"x" : STAT_GAUGE_X,
					"y" : 64+18+18+18+15,
					"children" :
					(
						{
							"name" : "dex_gauge",
							"type" : "gauge",
							"x" : STAT_GAUGE_BAR_X,
							"y" : 4,
							"width" : STAT_GAUGE_BAR_WIDTH,
							"color" : "blue",
						},
						{
							"name" : "dex_slot",
							"x" : STAT_GAUGE_BAR_WIDTH + STAT_GAUGE_BAR_X + 7,
							"y" : -1,
							
							"width" : STAT_GAUGE_TEXT_WIDTH,
							"height" : STAT_GAUGE_TEXT_HEIGHT,
							"children" :
							(
								{
									"name" : "dex_value",
									"type" : "text",
									"x" : 0,
									"y" : 1,
									"all_align" : "center",
									"text" : "0",
								},
							),
						},
					),
				},

				{
					"name" : "character_name_slot", "type" : "image",
					"x" : 39, "y" : 190,

					"image" : ROOT_PATH_NEW_CHR + "character_name.png",
					
					"children" :
					(
						{
							"name" : "character_name_value", "type" : "editline",
							"x" : 7, "y" : 9,
							"input_limit" : 12,
							"width" : 90, "height" : 20,
						},
					),
				},
			), 
		},

		## Buttons - Start, Exit ##
		{
			"name" : "create_button", "type" : "button",
			"x" : SCREEN_WIDTH/2 - 117, "y" : SCREEN_HEIGHT - SCREEN_HEIGHT*(60)/600.0,

			"default_image" : ROOT_PATH_NEW + "play.png",
			"over_image"	: ROOT_PATH_NEW + "play_over.png",
			"down_image"	: ROOT_PATH_NEW + "play_down.png",
		},
		{
			"name" : "cancel_button","type" : "button",
			"x" : SCREEN_WIDTH/2 + 140, "y" : SCREEN_HEIGHT - SCREEN_HEIGHT*(55)/600.0,

			"default_image" : ROOT_PATH_NEW + "exit.png",
			"over_image"	: ROOT_PATH_NEW + "exit_over.png",
			"down_image"	: ROOT_PATH_NEW + "exit_down.png",
		},
		# {
			# "name" : "exit_game_button","type" : "button",
			# "x" : SCREEN_WIDTH/2 + 140, "y" : SCREEN_HEIGHT - SCREEN_HEIGHT*(55)/600.0,

			# "default_image" : ROOT_PATH_NEW_CHR + "exit.png",
			# "over_image"	: ROOT_PATH_NEW_CHR + "exit_over.png",
			# "down_image"	: ROOT_PATH_NEW_CHR + "exit_down.png",
		# },
		
	), #New_CreateCharacterWindow children
}

