import app
import uiScriptLocale
import localeInfo

QUEST_ICON_BACKGROUND = 'd:/ymir work/ui/game/quest/slot_base.sub'

SMALL_VALUE_FILE = "d:/ymir work/ui/public/Parameter_Slot_00.sub"
MIDDLE_VALUE_FILE = "d:/ymir work/ui/public/Parameter_Slot_01.sub"
LARGE_VALUE_FILE = "d:/ymir work/ui/public/Parameter_Slot_03.sub"
ICON_SLOT_FILE = "d:/ymir work/ui/public/Slot_Base.sub"
FACE_SLOT_FILE = "d:/ymir work/ui/game/windows/box_face.sub"
ROOT_PATH = "d:/ymir work/ui/game/windows/"

LOCALE_PATH = "locale/ui/windows/"

window = {
	"name" : "CharacterWindow",
	"style" : ("movable", "float","animation",),

	"x" : 24,
	"y" : (SCREEN_HEIGHT - 37 - 361) / 2,

	"width" : 253,
	"height" : 405,

	"children" :
	(
		{
			"name" : "board",
			"type" : "board",
			"style" : ("attach",),

			"x" : 0,
			"y" : 0,

			"width" : 253,
			"height" : 405,

			"children" :
			(
				{
					"name" : "Skill_TitleBar",
					"type" : "titlebar",
					"style" : ("attach",),

					"x" : 8,
					"y" : 7,

					"width" : 238,
					"color" : "red",

					"children" :
					(
						{ "name":"TitleName", "type":"text", "x":0, "y":-1, "text":uiScriptLocale.CHARACTER_SKILL, "all_align":"center" },
					),
				},
				{
					"name" : "Emoticon_TitleBar",
					"type" : "titlebar",
					"style" : ("attach",),

					"x" : 8,
					"y" : 7,

					"width" : 238,
					"color" : "red",

					"children" :
					(
						{ "name":"TitleName", "type":"text", "x":0, "y":-1, "text":uiScriptLocale.CHARACTER_ACTION, "all_align":"center" },
					),
				},
				{
					"name" : "Quest_TitleBar",
					"type" : "titlebar",
					"style" : ("attach",),

					"x" : 8,
					"y" : 7,

					"width" : 238,
					"color" : "red",

					"children" :
					(
						{ "name":"TitleName", "type":"text", "x":0, "y":-1, "text":uiScriptLocale.CHARACTER_QUEST, "all_align":"center" },
					),
				},

				## Tab Area
				{
					"name" : "TabControl",
					"type" : "window",

					"x" : 0,
					"y" : 371,

					"width" : 250,
					"height" : 31,

					"children" :
					(
						## Tab
						{
							"name" : "Tab_01",
							"type" : "image",

							"x" : 0,
							"y" : 0,

							"width" : 250,
							"height" : 31,

							"image" : ROOT_PATH+"char_tab_01_norm.sub",
						},
						{
							"name" : "Tab_02",
							"type" : "image",

							"x" : 0,
							"y" : 0,

							"width" : 250,
							"height" : 31,

							"image" : ROOT_PATH+"char_tab_02_norm.sub",
						},
						{
							"name" : "Tab_03",
							"type" : "image",

							"x" : 0,
							"y" : 0,

							"width" : 250,
							"height" : 31,

							"image" : ROOT_PATH+"char_tab_03_norm.sub",
						},
						{
							"name" : "Tab_04",
							"type" : "image",

							"x" : 0,
							"y" : 0,

							"width" : 250,
							"height" : 31,

							"image" : ROOT_PATH+"char_tab_04_norm.sub",
						},
						## RadioButton
						{
							"name" : "Tab_Button_01",
							"type" : "radio_button",

							"x" : 6,
							"y" : 5,

							"width" : 53,
							"height" : 27,
						},
						{
							"name" : "Tab_Button_02",
							"type" : "radio_button",

							"x" : 61,
							"y" : 5,

							"width" : 67,
							"height" : 27,
						},
						{
							"name" : "Tab_Button_03",
							"type" : "radio_button",

							"x" : 130,
							"y" : 5,

							"width" : 61,
							"height" : 27,
						},
						{
							"name" : "Tab_Button_04",
							"type" : "radio_button",

							"x" : 192,
							"y" : 5,

							"width" : 55,
							"height" : 27,
						},
					),
				},

				## Page Area
				{
					"name" : "Character_Page",
					"type" : "window",
					"style" : ("attach",),

					"x" : 0,
					"y" : 0,

					"width" : 253,
					"height" : 371,

					"children" :
					(
						{
							"name" : "status_window",
							"type" : "window",
							"style" : ("attach",),
							"x" : 0,
							"y" : 0,
							"width" : 253,
							"height" : 371,
							"children" :
							(
								{
									"name":"Status_Standard", "type":"window", "x":3, "y":125, "width":250, "height":250,
									"children" :
									(
										{ "name":"Base_Info_bar", "type":"image", "x":6, "y":12-7, "image":ROOT_PATH+"base_info_bar.sub" },
										{ "name":"Char_Info_Status_img", "type" : "button", "x" : 12, "y" : 14-7, "default_image" : ROOT_PATH+"char_info_status_img.sub", "over_image" : ROOT_PATH+"char_info_status_img.sub", "down_image" : ROOT_PATH+"char_info_status_img.sub", },
										
										{ 
											"name":"Status_Plus_Label", 
											"type":"button", 
											
											"x":191, 
											"y":15-7,
											
											"default_image" : ROOT_PATH+"char_info_status_plus_img.sub",
											"over_image" : ROOT_PATH+"char_info_status_plus_img.sub",
											"down_image" : ROOT_PATH+"char_info_status_plus_img.sub",

											
											"children" :
											(
												{ "name":"Status_Plus_Btn_Img", "type":"image", "x":19, "y":0, "default_image" : ROOT_PATH+"char_info_status_value_img.sub", "over_image" : ROOT_PATH+"char_info_status_value_img.sub", "down_image" : ROOT_PATH+"char_info_status_value_img.sub", },
												{ "name":"Status_Plus_Value", "type":"text", "x":30, "y":-1, "text":"270", "r":1.0, "g":1.0, "b":1.0, "a":1.0, "text_horizontal_align":"center" },
											),
										},

										{
											"name":"base_info", "type":"window", "x":0, "y":26, "width":150, "height":150,
											"children" :
											(
												## HTH
												{ "name":"HTH_Slot", "type":"image", "x":50, "y":0, "image":SMALL_VALUE_FILE },
												{ "name":"HTH_Value", "type":"text", "x":70, "y":3, "text":"999", "r":1.0, "g":1.0, "b":1.0, "a":1.0, "text_horizontal_align":"center" },
												{ "name":"HTH_Plus", "type" : "button", "x":91, "y":3, "default_image" : ROOT_PATH+"btn_plus_up.sub", "over_image" : ROOT_PATH+"btn_plus_over.sub", "down_image" : ROOT_PATH+"btn_plus_down.sub", },

												## INT
												{ "name":"INT_Slot", "type":"image", "x":50, "y":31, "image":SMALL_VALUE_FILE },
												{ "name":"INT_Value", "type":"text", "x":70, "y":34, "text":"999", "r":1.0, "g":1.0, "b":1.0, "a":1.0, "text_horizontal_align":"center" },
												{ "name":"INT_Plus", "type" : "button", "x" : 91, "y" : 34, "default_image" : ROOT_PATH+"btn_plus_up.sub", "over_image" : ROOT_PATH+"btn_plus_over.sub", "down_image" : ROOT_PATH+"btn_plus_down.sub", },

												## STR
												{ "name":"STR_Slot", "type":"image", "x":50, "y":62, "image":SMALL_VALUE_FILE },
												{ "name":"STR_Value", "type":"text", "x":70, "y":65, "text":"999", "r":1.0, "g":1.0, "b":1.0, "a":1.0, "text_horizontal_align":"center" },
												{ "name":"STR_Plus", "type" : "button", "x" : 91, "y" : 65, "default_image" : ROOT_PATH+"btn_plus_up.sub", "over_image" : ROOT_PATH+"btn_plus_over.sub", "down_image" : ROOT_PATH+"btn_plus_down.sub", },

												## DEX
												{ "name":"DEX_Slot", "type":"image", "x":50, "y":93, "image":SMALL_VALUE_FILE },
												{ "name":"DEX_Value", "type":"text", "x":70, "y":96, "text":"999", "r":1.0, "g":1.0, "b":1.0, "a":1.0, "text_horizontal_align":"center" },
												{ "name":"DEX_Plus", "type" : "button", "x" : 91, "y" : 96, "default_image" : ROOT_PATH+"btn_plus_up.sub", "over_image" : ROOT_PATH+"btn_plus_over.sub", "down_image" : ROOT_PATH+"btn_plus_down.sub", },


												{ "name":"HTH_IMG", "type":"button",	"x":20, "y":-2, "default_image" : ROOT_PATH+"char_info_con.sub", "over_image" : ROOT_PATH+"char_info_con.sub", "down_image" : ROOT_PATH+"char_info_con.sub", },
												{ "name":"INT_IMG", "type":"button",	"x":20, "y":29, "default_image" : ROOT_PATH+"char_info_int.sub", "over_image" : ROOT_PATH+"char_info_int.sub", "down_image" : ROOT_PATH+"char_info_int.sub", },
												{ "name":"STR_IMG", "type":"button",	"x":20, "y":60, "default_image" : ROOT_PATH+"char_info_str.sub", "over_image" : ROOT_PATH+"char_info_str.sub", "down_image" : ROOT_PATH+"char_info_str.sub", },
												{ "name":"DEX_IMG", "type":"button",	"x":20, "y":91, "default_image" : ROOT_PATH+"char_info_dex.sub", "over_image" : ROOT_PATH+"char_info_dex.sub", "down_image" : ROOT_PATH+"char_info_dex.sub", },
						
											),
										},
										{ "name":"HTH_Minus", "type" : "button", "x":7, "y":36-7, "default_image" : ROOT_PATH+"btn_minus_up.sub", "over_image" : ROOT_PATH+"btn_minus_over.sub", "down_image" : ROOT_PATH+"btn_minus_down.sub", },
										{ "name":"INT_Minus", "type" : "button", "x":7, "y":67-7, "default_image" : ROOT_PATH+"btn_minus_up.sub", "over_image" : ROOT_PATH+"btn_minus_over.sub", "down_image" : ROOT_PATH+"btn_minus_down.sub", },
										{ "name":"STR_Minus", "type" : "button", "x":7, "y":98-7, "default_image" : ROOT_PATH+"btn_minus_up.sub", "over_image" : ROOT_PATH+"btn_minus_over.sub", "down_image" : ROOT_PATH+"btn_minus_down.sub", },
										{ "name":"DEX_Minus", "type" : "button", "x":7, "y":129-7, "default_image" : ROOT_PATH+"btn_minus_up.sub", "over_image" : ROOT_PATH+"btn_minus_over.sub", "down_image" : ROOT_PATH+"btn_minus_down.sub", },

										{ "name":"HEL_IMG",	"type":"button",	"x":118, "y":31-7, "default_image" : ROOT_PATH+"char_info_hp.sub", "over_image" : ROOT_PATH+"char_info_hp.sub", "down_image" : ROOT_PATH+"char_info_hp.sub", },
										{ "name":"SP_IMG",	"type":"button",	"x":118, "y":62-7, "default_image" : ROOT_PATH+"char_info_sp.sub", "over_image" : ROOT_PATH+"char_info_sp.sub", "down_image" : ROOT_PATH+"char_info_sp.sub", },
										{ "name":"ATT_IMG",	"type":"button",	"x":118, "y":93-7, "default_image" : ROOT_PATH+"char_info_att.sub", "over_image" : ROOT_PATH+"char_info_att.sub", "down_image" : ROOT_PATH+"char_info_att.sub", },
										{ "name":"DEF_IMG",	"type":"button",	"x":118, "y":124-7, "default_image" : ROOT_PATH+"char_info_def.sub", "over_image" : ROOT_PATH+"char_info_def.sub", "down_image" : ROOT_PATH+"char_info_def.sub", },

										####

										## HP
										{
											"name":"HEL_Label", "type":"window", "x":145, "y":33-7, "width":50, "height":20,
											"children" :
											(
												{ "name":"HP_Slot", "type":"image", "x":0, "y":0, "image":LARGE_VALUE_FILE },
												{ "name":"HP_Value", "type":"text", "x":45, "y":3, "text":"9999/9999", "r":1.0, "g":1.0, "b":1.0, "a":1.0, "text_horizontal_align":"center" },
											)
										},
										## SP
										{
											"name":"SP_Label", "type":"window", "x":145, "y":64-7, "width":50, "height":20, 
											"children" :
											(
												{ "name":"SP_Slot", "type":"image", "x":0, "y":0, "image":LARGE_VALUE_FILE },
												{ "name":"SP_Value", "type":"text", "x":45, "y":3, "text":"9999/9999", "r":1.0, "g":1.0, "b":1.0, "a":1.0, "text_horizontal_align":"center" },
											)
										},
										## ATT
										{
											"name":"ATT_Label", "type":"window", "x":145, "y":95-7, "width":50, "height":20, 
											"children" :
											(
												{ "name":"ATT_Slot", "type":"image", "x":0, "y":0, "image":LARGE_VALUE_FILE },
												{ "name":"ATT_Value", "type":"text", "x":45, "y":3, "text":"999", "r":1.0, "g":1.0, "b":1.0, "a":1.0, "text_horizontal_align":"center" },
											)
										},
										## DEF
										{
											"name":"DEF_Label", "type":"window", "x":145, "y":126-7, "width":50, "height":20, 
											"children" :
											(
												{ "name":"DEF_Slot", "type":"image", "x":0, "y":0, "image":LARGE_VALUE_FILE },
												{ "name":"DEF_Value", "type":"text", "x":45, "y":3, "text":"999", "r":1.0, "g":1.0, "b":1.0, "a":1.0, "text_horizontal_align":"center" },
											)
										},
									),
								},
								
								{ 
									"name":"Status_Extent", "type":"window", "x":3, "y":270, "width":253, "height":125, 
									"children" :
									(

										{ "name":"Status_Extent_Label", "type" : "image", "x" : 13, "y" : 0, "image" : ROOT_PATH+"status_extent_bar.sub", },

										{ "name":"MSPD_IMG", "type":"button", "x":20, "y":31 - 25,  "default_image" : ROOT_PATH+"char_info_movespeed.sub", "over_image" : ROOT_PATH+"char_info_movespeed.sub", "down_image" : ROOT_PATH+"char_info_movespeed.sub",  },
										{ "name":"ASPD_IMG", "type":"button", "x":20, "y":62 - 25,  "default_image" : ROOT_PATH+"char_info_attspeed.sub", "over_image" : ROOT_PATH+"char_info_attspeed.sub", "down_image" : ROOT_PATH+"char_info_attspeed.sub",  },
										{ "name":"CSPD_IMG", "type":"button", "x":20, "y":93 - 25,  "default_image" : ROOT_PATH+"char_info_magspeed.sub", "over_image" : ROOT_PATH+"char_info_magspeed.sub", "down_image" : ROOT_PATH+"char_info_magspeed.sub",  },
										{ "name":"MATT_IMG", "type":"button", "x":118, "y":31 - 25, "default_image" : ROOT_PATH+"char_info_magatt.sub", "over_image" : ROOT_PATH+"char_info_magatt.sub", "down_image" : ROOT_PATH+"char_info_magatt.sub", },
										{ "name":"MDEF_IMG", "type":"button", "x":118, "y":62 - 25, "default_image" : ROOT_PATH+"char_info_magdef.sub", "over_image" : ROOT_PATH+"char_info_magdef.sub", "down_image" : ROOT_PATH+"char_info_magdef.sub", },
										{ "name":"ER_IMG", "type":"button", "x":118, "y":93 - 25, "default_image" : ROOT_PATH+"char_info_hitpct.sub", "over_image" : ROOT_PATH+"char_info_hitpct.sub", "down_image" : ROOT_PATH+"char_info_hitpct.sub", },
									
										{
											"name":"MOV_Label", "type":"window", "x":50, "y":33 - 25, "width":50, "height":20, 
											"children" :
											(
												{ "name":"MSPD_Slot", "type":"image", "x":0, "y":0, "image":MIDDLE_VALUE_FILE },
												{ "name":"MSPD_Value", "type":"text", "x":26, "y":3, "text":"999", "r":1.0, "g":1.0, "b":1.0, "a":1.0, "text_horizontal_align":"center" },
											)
										},

										{
											"name":"ASPD_Label", "type":"window", "x":50, "y":64 - 25, "width":50, "height":20, 
											"children" :
											(
												{ "name":"ASPD_Slot", "type":"image", "x":0, "y":0, "image":MIDDLE_VALUE_FILE },
												{ "name":"ASPD_Value", "type":"text", "x":26, "y":3, "text":"999", "r":1.0, "g":1.0, "b":1.0, "a":1.0, "text_horizontal_align":"center" },
											)
										},

										{
											"name":"CSPD_Label", "type":"window", "x":50, "y":95 - 25, "width":50, "height":20, 
											"children" :
											(
												{ "name":"CSPD_Slot", "type":"image", "x":0, "y":0, "image":MIDDLE_VALUE_FILE },
												{ "name":"CSPD_Value", "type":"text", "x":26, "y":3, "text":"999", "r":1.0, "g":1.0, "b":1.0, "a":1.0, "text_horizontal_align":"center" },
											)
										},

										{
											"name":"MATT_Label", "type":"window", "x":145, "y":33 - 25, "width":50, "height":20, 
											"children" :
											(
												{ "name":"MATT_Slot", "type":"image", "x":0, "y":0, "image":LARGE_VALUE_FILE },
												{ "name":"MATT_Value", "type":"text", "x":45, "y":3, "text":"999-999", "r":1.0, "g":1.0, "b":1.0, "a":1.0, "text_horizontal_align":"center" },
											)
										},

										{
											"name":"MDEF_Label", "type":"window", "x":145, "y":64 - 25, "width":50, "height":20, 
											"children" :
											(
												{ "name":"MDEF_Slot", "type":"image", "x":0, "y":0, "image":LARGE_VALUE_FILE },
												{ "name":"MDEF_Value", "type":"text", "x":45, "y":3, "text":"999", "r":1.0, "g":1.0, "b":1.0, "a":1.0, "text_horizontal_align":"center" },
											)
										},

										{
											"name":"ER_Label", "type":"window", "x":145, "y":95 - 25, "width":50, "height":20, 
											"children" :
											(
												{ "name":"ER_Slot", "type":"image", "x":0, "y":0, "image":LARGE_VALUE_FILE },
												{ "name":"ER_Value", "type":"text", "x":45, "y":3, "text":"999", "r":1.0, "g":1.0, "b":1.0, "a":1.0, "text_horizontal_align":"center" },
											)
										},
									),
								},
							),
						},
						{
							"name" : "bonus_window",
							"type" : "window",
							"style" : ("attach",),
							"x" : 0,
							"y" : 0,
							"width" : 253,
							"height" : 371,
							"children" :
							(
								{ "name":"bonus_base_bar", "type":"image", "x":9, "y":12-7+125, "image":ROOT_PATH+"base_info_bar.sub" },
								{ "name":"bonus_base_tooltip_image", "type" : "image", "x" : 12+3, "y" : 14-7+125, "image" : ROOT_PATH+"bonus_icon_tooltip.sub", },
								{ "name":"bonus_base_image", "type" : "image", "x" : 11, "y" : 14-7+145, "image" : "d:/ymir work/ui/board_image_base_other.tga", },
								{
									"name" : "bonus_scrollbar",
									"type" : "scrollbar",
									
									"x" : 30,
									"y" : 14-7+150,
									"size" : 210,
									"horizontal_align" : "right",
								},
							),
						},
						# {
							# "name" : "special_other_window",
							# "type" : "window",
							# "style" : ("attach",),
							# "x" : 0,
							# "y" : 0,
							# "width" : 253,
							# "height" : 371,
							# "children" :
							# (
								# { "name":"special_base_bar", "type":"image", "x":9, "y":12-7+125, "image":ROOT_PATH+"base_info_bar.sub" },
								# { "name":"special_base_tooltip_image", "type" : "image", "x" : 12+3, "y" : 14-7+125, "image" : ROOT_PATH+"other_icon_tooltip.sub", },
								# { "name":"special_base_image", "type" : "image", "x" : 11, "y" : 14-7+145, "image" : "d:/ymir work/ui/board_image_base_other.tga", },
								# {
									# "name" : "special_scrollbar",
									# "type" : "scrollbar",
									
									# "x" : 30,
									# "y" : 14-7+150,
									# "size" : 210,
									# "horizontal_align" : "right",
								# },
							# ),
						# },
						## Title Area
						{
							"name" : "Character_TitleBar", "type" : "titlebar", "style" : ("attach",), "x" : 61, "y" : 7, "width" : 185, "color" : "red",
							"children" :
							(
								{ "name" : "TitleName", "type":"text", "x":0, "y":-1, "text":uiScriptLocale.CHARACTER_MAIN, "all_align":"center" },
							),
						},

						## Guild Name Slot
						{
							"name" : "Guild_Name_Slot",
							"type" : "image",
							"x" : 60,
							"y" :27+7,
							"image" : LARGE_VALUE_FILE,

							"children" :
							(
								{
									"name" : "Guild_Name",
									"type":"text",
									"text":"?? ??",
									"x":0,
									"y":0,
									"r":1.0,
									"g":1.0,
									"b":1.0,
									"a":1.0,
									"all_align" : "center",
								},
							),
						},

						## Character Name Slot
						{
							"name" : "Character_Name_Slot",
							"type" : "image",
							"x" : 153,
							"y" :27+7,
							"image" : LARGE_VALUE_FILE,

							"children" :
							(
								{
									"name" : "Character_Name",
									"type":"text",
									"text":"??? ??",
									"x":0,
									"y":0,
									"r":1.0,
									"g":1.0,
									"b":1.0,
									"a":1.0,
									"all_align" : "center",
								},
							),
						},
						{ "name":"Lv_Exp_BackImg", "type":"image", "x":9, "y":60, "image":ROOT_PATH+"level_exp_info.sub" },
						{ "name":"Level_Value", "type":"text", "x":35, "y":84, "fontsize":"LARGE", "text":"999", "r":1.0, "g":1.0, "b":1.0, "a":1.0, "text_horizontal_align":"center" },

						## EXP
						{
							"name":"Status_CurExp", "type":"window", "x":53+8, "y":84, "width":87, "height":42,
							"children" :
							(
								{ "name":"Exp_Value", "type":"text", "x":46, "y":0, "fontsize":"LARGE", "text":"2500000000", "r":1.0, "g":1.0, "b":1.0, "a":1.0, "text_horizontal_align":"center" },		
							),
						},
						{ "name" : "slash", "type":"text", "text":"/", "x":152, "y":87, "text_horizontal_align" : "center", },

						## REXP
						{
							"name":"Status_RestExp", "type":"window", "x":152, "y":84, "width":50, "height":20, 
							"children" :
							(
								{ "name":"RestExp_Value", "type":"text", "x":46, "y":0, "fontsize":"LARGE", "text":"2500000000", "r":1.0, "g":1.0, "b":1.0, "a":1.0, "text_horizontal_align":"center" },
							),
						},

						## Face Slot
						{ "name" : "Face_Image", "type" : "image", "x" : 11, "y" : 11, "image" : "d:/ymir work/ui/game/windows/face_warrior.sub" },
						{ "name" : "Face_Slot", "type" : "image", "x" : 7, "y" : 7, "image" : FACE_SLOT_FILE, },
						
						## Passive Expanded Button
						{ "name":"change_status_button", "type" : "radio_button", "x":8, "y":107, "default_image" : ROOT_PATH+"button_status_see_down.sub", "over_image" : ROOT_PATH+"button_status_see_hover.sub", "down_image" : ROOT_PATH+"button_status_see_norm.sub", },
						{ "name":"change_bonus_button",		"type" : "radio_button",	"x":87, "y":107, "default_image" : ROOT_PATH+"old_level_btn_03.sub", "over_image" : ROOT_PATH+"old_level_btn_03.sub", "down_image" : ROOT_PATH+"old_level_btn_01.sub", },
						# { "name":"change_other_button",	"type" : "radio_button",	"x":166, "y":107, "default_image" : ROOT_PATH+"new_level_btn_03.sub", "over_image" : ROOT_PATH+"new_level_btn_03.sub", "down_image" : ROOT_PATH+"new_level_btn_01.sub", },
					),
				},
				{
					"name" : "Skill_Page",
					"type" : "window",
					"style" : ("attach",),

					"x" : 0,
					"y" : 24,

					"width" : 250,
					"height" : 350,

					"children" :
					(

						{
							"name":"Skill_Active_Title_Bar", "type":"horizontalbar", "x":15, "y":9, "width":223,

							"children" :
							(
								{ 
									"name":"Active_Skill_Point_Label", 
									"type":"button", 
									"x":180, 
									"y":3, 

									"default_image" : ROOT_PATH+"char_info_status_plus_img.sub",
									"over_image" : ROOT_PATH+"char_info_status_plus_img.sub",
									"down_image" : ROOT_PATH+"char_info_status_plus_img.sub",
									
									"children" :
									(
										{ "name":"Active_Skill_Plus_Img", "type":"image", "x":13, "y":0, "image":ROOT_PATH+"char_info_status_value_img.sub", },
										{ "name":"Active_Skill_Point_Value", "type":"text", "x":25, "y":0, "text":"99", "r":1.0, "g":1.0, "b":1.0, "a":1.0, "text_horizontal_align":"center" },
									),
								},

								## Group Button
								{
									"name" : "Skill_Group_Button_1",
									"type" : "radio_button",

									"x" : 5,
									"y" : 2,

									"text" : "Group1",
									"text_color" : 0xFFFFE3AD,

									"default_image" : "d:/ymir work/ui/game/windows/skill_tab_button_01.sub",
									"over_image" : "d:/ymir work/ui/game/windows/skill_tab_button_02.sub",
									"down_image" : "d:/ymir work/ui/game/windows/skill_tab_button_03.sub",
								},

								{
									"name" : "Skill_Group_Button_2",
									"type" : "radio_button",

									"x" : 50,
									"y" : 2,

									"text" : "Group2",
									"text_color" : 0xFFFFE3AD,

									"default_image" : "d:/ymir work/ui/game/windows/skill_tab_button_01.sub",
									"over_image" : "d:/ymir work/ui/game/windows/skill_tab_button_02.sub",
									"down_image" : "d:/ymir work/ui/game/windows/skill_tab_button_03.sub",
								},

								{
									"name" : "Active_Skill_Group_Name",
									"type" : "text",

									"x" : 7,
									"y" : 0,
									"text" : "Active",

									"vertical_align" : "center",
									"text_vertical_align" : "center",
									"color" : 0xFFFFE3AD,
								},

							),
						},
						{
							"name":"Skill_ETC_Title_Bar", "type":"horizontalbar", "x":15, "y":200 - 34, "width":223,
							"children" :
							(
								{
									"name" : "Support_Skill_Group_Name",
									"type" : "text",

									"x" : 7,
									"y" : 1,
									"text" : uiScriptLocale.SKILL_SUPPORT_TITLE,

									"vertical_align" : "center",
									"text_vertical_align" : "center",
									"color" : 0xFFFFE3AD,
								},

								{ 
									"name":"Support_Skill_Point_Label", "type":"image", "x":145, "y":3, "image":LOCALE_PATH+"label_uppt.sub",
									"children" :
									(
										{ "name":"Support_Skill_Point_Value", "type":"text", "x":62, "y":0, "text":"99", "r":1.0, "g":1.0, "b":1.0, "a":1.0, "text_horizontal_align":"center" },
									),
								},
							),
						},
						
						# {
							# "name":"Skill_ETC_Title_Bar2", "type":"horizontalbar", "x":15, "y":235, "width":223,

							# "children" :
							# (
								# {
									# "name" : "Support_Skill_Group_Name",
									# "type" : "text",

									# "x" : 7,
									# "y" : 1,
									# "text" : localeInfo.UNIQUE_COMP,

									# "vertical_align" : "center",
									# "text_vertical_align" : "center",
									# "color" : 0xFFFFE3AD,
								# },
							# ),
						# },
						
						{ "name":"Skill_Board", "type":"image", "x":13, "y":38, "image":"d:/ymir work/ui/game/comp/skill_board.png", },

						## Active Slot
						{
							"name" : "Skill_Active_Slot",
							"type" : "slot",

							"x" : 0 + 16,
							"y" : 0 + 15 + 23,

							"width" : 223,
							"height" : 150,
							"image" : ICON_SLOT_FILE,

							"slot" :	(
											{"index": 1, "x": 1, "y":  4, "width":32, "height":32},
											{"index":21, "x":38, "y":  4, "width":32, "height":32},
											{"index":41, "x":75, "y":  4, "width":32, "height":32},

											{"index": 3, "x": 1, "y": 40, "width":32, "height":32},
											{"index":23, "x":38, "y": 40, "width":32, "height":32},
											{"index":43, "x":75, "y": 40, "width":32, "height":32},

											{"index": 5, "x": 1, "y": 76, "width":32, "height":32},
											{"index":25, "x":38, "y": 76, "width":32, "height":32},
											{"index":45, "x":75, "y": 76, "width":32, "height":32},

											# {"index": 7, "x": 1, "y":112, "width":32, "height":32},
											# {"index":27, "x":38, "y":112, "width":32, "height":32},
											# {"index":47, "x":75, "y":112, "width":32, "height":32},

											####

											{"index": 2, "x":113, "y":  4, "width":32, "height":32},
											{"index":22, "x":150, "y":  4, "width":32, "height":32},
											{"index":42, "x":187, "y":  4, "width":32, "height":32},

											{"index": 4, "x":113, "y": 40, "width":32, "height":32},
											{"index":24, "x":150, "y": 40, "width":32, "height":32},
											{"index":44, "x":187, "y": 40, "width":32, "height":32},

											{"index": 6, "x":113, "y": 76, "width":32, "height":32},
											{"index":26, "x":150, "y": 76, "width":32, "height":32},
											{"index":46, "x":187, "y": 76, "width":32, "height":32},

											# {"index": 8, "x":113, "y":112, "width":32, "height":32},
											# {"index":28, "x":150, "y":112, "width":32, "height":32},
											# {"index":48, "x":187, "y":112, "width":32, "height":32},
										),
						},

						{
							"name" : "Skill_ETC_Slot",
							"type" : "slot",
							"x" : 18,
							"y" : 189,
							"width" : 223,
							"height" : 150,
							"image" : ICON_SLOT_FILE,
							
							"slot" :	(
											{"index": 101, "x": 1, "y":  4, "width":32, "height":32},
											{"index": 110, "x":38, "y":  4, "width":32, "height":32},
											{"index": 102, "x":75, "y":  4, "width":32, "height":32},
											
											{"index": 106, "x":113, "y":  4, "width":32, "height":32},
											{"index": 103, "x":150, "y":  4, "width":32, "height":32},
											{"index": 104, "x":187, "y":  4, "width":32, "height":32},
											
											# {"index": 300, "x": 1, "y": 74, "width":32, "height":32},
											# {"index": 301, "x": 38, "y": 74, "width":32, "height":32},
											# {"index": 302, "x": 75, "y": 74, "width":32, "height":32},
											# {"index": 303, "x": 113, "y": 74, "width":32, "height":32},
											# {"index": 304, "x": 150, "y": 74, "width":32, "height":32},
											# {"index": 305, "x": 187, "y": 74, "width":32, "height":32},
											
								
											# {"index": 306, "x": 1, "y": 110, "width":32, "height":32},
											# {"index": 307, "x": 38, "y": 110, "width":32, "height":32},
											# {"index": 308, "x": 75, "y": 110, "width":32, "height":32},
											# {"index": 309, "x": 113, "y": 110, "width":32, "height":32},
											# {"index": 310, "x": 150, "y": 110, "width":32, "height":32},
											# {"index": 311, "x": 187, "y": 110, "width":32, "height":32},
											
										),
							
						},
						# ETC Slot
						# {
							# "name" : "Skill_ETC_Slot",
							# "type" : "grid_table",
							# "x" : 18,
							# "y" : 189,
							# "start_index" : 101,
							# "x_count" : 6,
							# "y_count" : 3,
							# "x_step" : 32,
							# "y_step" : 32,
							# "x_blank" : 5,
							# "y_blank" : 4,
							# "image" : ICON_SLOT_FILE,
						# },

					),
				},
				{
					"name" : "Emoticon_Page",
					"type" : "window",
					"style" : ("attach",),

					"x" : 0,
					"y" : 24,

					"width" : 250,
					"height" : 304,

					"children" :
					(
						## ?? ?? ??
						{ "name":"Action_Bar", "type":"horizontalbar", "x":12, "y":11, "width":223, },
						{ "name":"Action_Bar_Text", "type":"text", "x":15, "y":13, "text":uiScriptLocale.CHARACTER_NORMAL_ACTION },

						## Basis Action Slot
						{
							"name" : "SoloEmotionSlot",
							"type" : "grid_table",
							"x" : 27,
							"y" : 33,
							"horizontal_align" : "center",
							"start_index" : 1,
							"x_count" : 6,
							"y_count" : 3,
							"x_step" : 32,
							"y_step" : 32,
							"x_blank" : 0,
							"y_blank" : 0,
							"image" : ICON_SLOT_FILE,
						},

						## ?? ?? ??
						{ "name":"Reaction_Bar", "type":"horizontalbar", "x":12, "y":8+150 - 10, "width":223, },
						{ "name":"Reaction_Bar_Text", "type":"text", "x":15, "y":10+150 - 10, "text":uiScriptLocale.CHARACTER_MUTUAL_ACTION },

						## Reaction Slot
						{
							"name" : "DualEmotionSlot",
							"type" : "grid_table",
							"x" : 27,
							"y" : 180 - 10,
							"start_index" : 51,
							"x_count" : 6,
							"y_count" : 1,
							"x_step" : 32,
							"y_step" : 32,
							"x_blank" : 0,
							"y_blank" : 0,
							"image" : ICON_SLOT_FILE,
						},
						
						{ "name":"Emotic_Bar", "type":"horizontalbar", "x":12, "y":8+150 + 58 - 10, "width":223, },
						{ "name":"Emotic_Bar_Text", "type":"text", "x":15, "y":10+150 + 58 - 10, "text":localeInfo.STAT_TOOLTIP_SPECIAL_ACTION },

						{
							"name" : "PremiumEmotionSlot",
							"type" : "grid_table",
							"x" : 27,
							"y" : 180 + 58 - 10,
							"start_index" : 60,
							"x_count" : 6,
							"y_count" : 2,
							"x_step" : 32,
							"y_step" : 32,
							"x_blank" : 0,
							"y_blank" : 0,
							"image" : ICON_SLOT_FILE,
						},


						## Slot
						# {
							# "name" : "EmotionSlot",
							# "type" : "grid_table",
							# "x" : 27,
							# "y" : 180 + 58 - 10,
							# "start_index" : 70,
							# "x_count" : 6,
							# "y_count" : 3,
							# "x_step" : 32,
							# "y_step" : 32,
							# "x_blank" : 0,
							# "y_blank" : 0,
							# "image" : ICON_SLOT_FILE,
						# },
					),
				},
				{
					"name" : "Quest_Page",
					"type" : "window",
					"style" : ("attach",),

					"x" : 0,
					"y" : 24,

					"width" : 250,
					"height" : 304,

					"children" :
					(
						{
							"name" : "Quest_Slot",
							"type" : "grid_table",
							"x" : 18,
							"y" : 20,
							"start_index" : 0,
							"x_count" : 1,
							"y_count" : 5,
							"x_step" : 32,
							"y_step" : 32,
							"y_blank" : 28,
							"image" : QUEST_ICON_BACKGROUND,
						},

						{
							"name" : "Quest_ScrollBar",
							"type" : "scrollbar",

							"x" : 25,
							"y" : 12,
							"size" : 290,
							"horizontal_align" : "right",
						},

						{ "name" : "Quest_Name_00", "type" : "text", "text" : "?????", "x" : 60, "y" : 14 },
						{ "name" : "Quest_LastTime_00", "type" : "text", "text" : "?? ?? ???", "x" : 60, "y" : 30 },
						{ "name" : "Quest_LastCount_00", "type" : "text", "text" : "?? ?? ???", "x" : 60, "y" : 46 },

						{ "name" : "Quest_Name_01", "type" : "text", "text" : "?????", "x" : 60, "y" : 74 },
						{ "name" : "Quest_LastTime_01", "type" : "text", "text" : "?? ?? ???", "x" : 60, "y" : 90 },
						{ "name" : "Quest_LastCount_01", "type" : "text", "text" : "?? ?? ???", "x" : 60, "y" : 106 },

						{ "name" : "Quest_Name_02", "type" : "text", "text" : "?????", "x" : 60, "y" : 134 },
						{ "name" : "Quest_LastTime_02", "type" : "text", "text" : "?? ?? ???", "x" : 60, "y" : 150 },
						{ "name" : "Quest_LastCount_02", "type" : "text", "text" : "?? ?? ???", "x" : 60, "y" : 166 },

						{ "name" : "Quest_Name_03", "type" : "text", "text" : "?????", "x" : 60, "y" : 194 },
						{ "name" : "Quest_LastTime_03", "type" : "text", "text" : "?? ?? ???", "x" : 60, "y" : 210 },
						{ "name" : "Quest_LastCount_03", "type" : "text", "text" : "?? ?? ???", "x" : 60, "y" : 226 },

						{ "name" : "Quest_Name_04", "type" : "text", "text" : "?????", "x" : 60, "y" : 254 },
						{ "name" : "Quest_LastTime_04", "type" : "text", "text" : "?? ?? ???", "x" : 60, "y" : 270 },
						{ "name" : "Quest_LastCount_04", "type" : "text", "text" : "?? ?? ???", "x" : 60, "y" : 286 },

					),
				},
			),
		},
	),
}
