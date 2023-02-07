import uiScriptLocale

# ROOT_PATH_NEW = "d:/ymir work/ui/public/"
ROOT_PATH_NEW = "d:/ymir work/ui/game/stats_board/"

TEXT_TEMPORARY_X = -10

window = {
	"name" : "GameOptionDialog",
	"style" : ("movable", "float", "not_pick", "animation",),

	"x" : 0,
	"y" : 0,

	"width" : 497,
	"height" : 400,

	"children" :
	(
		{
			"name" : "board",
			"type" : "board",

			"x" : 0,
			"y" : 0,

			"width" : 497,
			"height" : 400,
			"children" :
			(
				## Title
				{
					"name" : "titlebar",
					"type" : "titlebar",
					"style" : ("attach",),

					"x" : 8,
					"y" : 8,

					"width" : 497 - 15,
					"color" : "gray",

					"children" :
					(
						{ "name":"titlename", "type":"text", "x":0, "y":3, 
						"text" : uiScriptLocale.GAME_OPTIONS_TITLE, 
						"horizontal_align":"center", "text_horizontal_align":"center" },
					),
				},
				# Background
				{
					"name" : "bg", 
					"type" : "image",

					"x" : 10, 
					"y" : 66,

					"image" : ROOT_PATH_NEW + "bg_board.png",
				},
				
				{
					"name" : "background_game", 
					
					"x" : 10, 
					"y" : 66,

					"width" : 450,
					"height" : 320,
					
					"children" :
					(
						{
							"name" : "character",
							"type" : "radio_button",

							"x" : 10,
							"y" : 17,

							"text" : uiScriptLocale.CHARACTER_MAIN,

							"default_image" : ROOT_PATH_NEW + "button_norm.png",
							"over_image" : ROOT_PATH_NEW + "button_over.png",
							"down_image" : ROOT_PATH_NEW + "button_down.png",
						},
						# Character Options Board
						{
							"name" : "char_opt_board",
							
							"x" : 170,
							"y" : 5,
							
							"width" : 400,
							"height" : 320,
							
							"children" : 
							(

								{
									"name" : "TitleCategoryImage",
									"type" : "image",

									"x" : 1,
									"y" : 0,
									
									"image" : ROOT_PATH_NEW + "bonus/title.png",
									"children" : 
									(
										{
											"name" : "TitleBlock",
											"type" : "text",

											"x" : 5,
											"y" : 3,

											"outline" : 1,
											
											"text" : uiScriptLocale.OPTION_PVPMODE,
										},	
									),
								},		

								
								{
									"name" : "pvp_peace",
									"type" : "radio_button",

									"x" : 20,
									"y" : 32,

									"children" : ({"name":"desc", "type":"text", "x":20, "y":0, "text": uiScriptLocale.OPTION_PVPMODE_PEACE,},),
									"tooltip_text" : uiScriptLocale.OPTION_PVPMODE_PEACE_TOOLTIP,

									"default_image" : ROOT_PATH_NEW + "check_empty.png",
									"over_image" : ROOT_PATH_NEW + "check_box.png",
									"down_image" : ROOT_PATH_NEW + "check_box.png",
								},
								{
									"name" : "pvp_revenge",
									"type" : "radio_button",

									"x" : 20*4,
									"y" : 32,

									"children" : ({"name":"desc", "type":"text", "x":20, "y":0, "text": uiScriptLocale.OPTION_PVPMODE_REVENGE,},),
									"tooltip_text" : uiScriptLocale.OPTION_PVPMODE_REVENGE_TOOLTIP,

									"default_image" : ROOT_PATH_NEW + "check_empty.png",
									"over_image" : ROOT_PATH_NEW + "check_box.png",
									"down_image" : ROOT_PATH_NEW + "check_box.png",
								},
								{
									"name" : "pvp_guild",
									"type" : "radio_button",

									"x" : 20*8,
									"y" : 32,

									"children" : ({"name":"desc", "type":"text", "x":20, "y":0, "text": uiScriptLocale.OPTION_PVPMODE_GUILD,},),
									"tooltip_text" : uiScriptLocale.OPTION_PVPMODE_GUILD_TOOLTIP,

									"default_image" : ROOT_PATH_NEW + "check_empty.png",
									"over_image" : ROOT_PATH_NEW + "check_box.png",
									"down_image" : ROOT_PATH_NEW + "check_box.png",
								},
								{
									"name" : "pvp_free",
									"type" : "radio_button",

									"x" : 20*12,
									"y" : 32,

									"children" : ({"name":"desc", "type":"text", "x":20, "y":0, "text": uiScriptLocale.OPTION_PVPMODE_FREE,},),
									"tooltip_text" : uiScriptLocale.OPTION_PVPMODE_FREE_TOOLTIP,

									"default_image" : ROOT_PATH_NEW + "check_empty.png",
									"over_image" : ROOT_PATH_NEW + "check_box.png",
									"down_image" : ROOT_PATH_NEW + "check_box.png",
								},		
								
								{
									"name" : "TitleCategoryImage",
									"type" : "image",

									"x" : 1,
									"y" : 55,
									
									"image" : ROOT_PATH_NEW + "bonus/title.png",
									"children" : 
									(
										{
											"name" : "TitleBlock",
											"type" : "text",

											"x" : 5,
											"y" : 3,

											"outline" : 1,
											
											"text" : uiScriptLocale.GAME_OPTIONS_BLOCK,
										},	
									),
								},		

								{
									"name" : "block_exchange_button",
									"type" : "toggle_button",

									"x" : 20,
									"y" : 87,

									"default_image" : ROOT_PATH_NEW + "checkbox_new_unselected.tga",
									"over_image" : ROOT_PATH_NEW + "checkbox_new_unselected.tga",
									"down_image" : ROOT_PATH_NEW + "checkbox_new_selected.tga",
									"children" : ({"name":"desc", "type":"text", "x":20, "y":-1, "text": uiScriptLocale.OPTION_BLOCK_EXCHANGE,},),
								},
								{
									"name" : "block_party_button",
									"type" : "toggle_button",

									"x" : 20,
									"y" : 87 + 25,
									"default_image" : ROOT_PATH_NEW + "checkbox_new_unselected.tga",
									"over_image" : ROOT_PATH_NEW + "checkbox_new_unselected.tga",
									"down_image" : ROOT_PATH_NEW + "checkbox_new_selected.tga",
									"children" : ({"name":"desc", "type":"text", "x":20, "y":-1, "text": uiScriptLocale.OPTION_BLOCK_PARTY,},),
								},
								{
									"name" : "block_guild_button",
									"type" : "toggle_button",

									"x" : 20 + 70,
									"y" : 87,
									"default_image" : ROOT_PATH_NEW + "checkbox_new_unselected.tga",
									"over_image" : ROOT_PATH_NEW + "checkbox_new_unselected.tga",
									"down_image" : ROOT_PATH_NEW + "checkbox_new_selected.tga",
									"children" : ({"name":"desc", "type":"text", "x":20, "y":-1, "text": uiScriptLocale.OPTION_BLOCK_GUILD,},),

								},
								{
									"name" : "block_whisper_button",
									"type" : "toggle_button",

									"x" : 20 + 70,
									"y" : 87 + 25,

									"default_image" : ROOT_PATH_NEW + "checkbox_new_unselected.tga",
									"over_image" : ROOT_PATH_NEW + "checkbox_new_unselected.tga",
									"down_image" : ROOT_PATH_NEW + "checkbox_new_selected.tga",
									"children" : ({"name":"desc", "type":"text", "x":20, "y":-1, "text": uiScriptLocale.OPTION_BLOCK_WHISPER,},),

								},
								{
									"name" : "block_friend_button",
									"type" : "toggle_button",

									"x" : 20 + 70 + 70,
									"y" : 87,

									"default_image" : ROOT_PATH_NEW + "checkbox_new_unselected.tga",
									"over_image" : ROOT_PATH_NEW + "checkbox_new_unselected.tga",
									"down_image" : ROOT_PATH_NEW + "checkbox_new_selected.tga",
									"children" : ({"name":"desc", "type":"text", "x":20, "y":-1, "text": uiScriptLocale.OPTION_BLOCK_FRIEND,},),

								},
								{
									"name" : "block_party_request_button",
									"type" : "toggle_button",

									"x" : 20 + 70 + 70,
									"y" : 87 + 25,

									"default_image" : ROOT_PATH_NEW + "checkbox_new_unselected.tga",
									"over_image" : ROOT_PATH_NEW + "checkbox_new_unselected.tga",
									"down_image" : ROOT_PATH_NEW + "checkbox_new_selected.tga",
									"children" : ({"name":"desc", "type":"text", "x":20, "y":-1, "text": uiScriptLocale.OPTION_BLOCK_PARTY_REQUEST,},),
								},
								
							
								{
									"name" : "TitleCategoryImage",
									"type" : "image",

									"x" : 1,
									"y" : 135,
									
									"image" : ROOT_PATH_NEW + "bonus/title.png",
									"children" : 
									(
										{
											"name" : "TitleCategory",
											"type" : "text",

											"x" : 5,
											"y" : 3,

											"outline" : 1,
											
											"text" : uiScriptLocale.GAME_OPTIONS_NAME_VISIBILITY,
										},	
									),
								},		
								{
									"name" : "name_color",
									"type" : "toggle_button",

									"x" : 20,
									"y" : 167,

									"default_image" : ROOT_PATH_NEW + "checkbox_new_unselected.tga",
									"over_image" : ROOT_PATH_NEW + "checkbox_new_unselected.tga",
									"down_image" : ROOT_PATH_NEW + "checkbox_new_selected.tga",
									"children" : ({"name":"desc", "type":"text", "x":20, "y":-1, "text": uiScriptLocale.SHOW_NAME_COLOR,},),

								},
								{
									"name" : "always_show_name",
									"type" : "toggle_button",

									"x" : 20,
									"y" : 187,

									"default_image" : ROOT_PATH_NEW + "checkbox_new_unselected.tga",
									"over_image" : ROOT_PATH_NEW + "checkbox_new_unselected.tga",
									"down_image" : ROOT_PATH_NEW + "checkbox_new_selected.tga",
									
									"children" : ({"name":"desc", "type":"text", "x":20, "y":-1, "text": uiScriptLocale.SHOW_NAME,},),
								},
							
								{
									"name" : "TitleCategoryImage",
									"type" : "image",

									"x" : 1,
									"y" : 215,
									
									"image" : ROOT_PATH_NEW + "bonus/title.png",
									"children" : 
									(
										{
											"name" : "TitleCategory",
											"type" : "text",

											"x" : 5,
											"y" : 3,

											"outline" : 1,
											
											"text" : "Mod Noapte",
										},	
									),
								},	
								# {
									# "name" : "always_show_name_partial",
									# "type" : "toggle_button",

									# "x" : 20,
									# "y" : 207,

									# "default_image" : ROOT_PATH_NEW + "checkbox_new_unselected.tga",
									# "over_image" : ROOT_PATH_NEW + "checkbox_new_unselected.tga",
									# "down_image" : ROOT_PATH_NEW + "checkbox_new_selected.tga",
									
									# "children" : ({"name":"desc", "type":"text", "x":20, "y":-1, "text": "Partial Name",},),
								# },
								{
									"name" : "night_on",
									"type" : "radio_button",
				
									"x" : 20,
									"y" : 207 + 40,
								
									"default_image" : ROOT_PATH_NEW + "check_empty.png",
									"over_image" : ROOT_PATH_NEW + "check_box.png",
									"down_image" : ROOT_PATH_NEW + "check_box.png",
									"children" : ({"name":"desc", "type":"text", "x":20, "y":0, "text": "Pornit",},),

								},
								{
									"name" : "night_off",
									"type" : "radio_button",
				
									"x" : 20+110,
									"y" : 207 + 40,
								
									"default_image" : ROOT_PATH_NEW + "check_empty.png",
									"over_image" : ROOT_PATH_NEW + "check_box.png",
									"down_image" : ROOT_PATH_NEW + "check_box.png",
									"children" : ({"name":"desc", "type":"text", "x":20, "y":0, "text": "Oprit",},),
								},

							),
						},
						
						# UI Board
						{
							"name" : "ui_opt_board",
							
							"x" : 170,
							"y" : 5,
							
							"width" : 400,
							"height" : 320,
							
							"children" : 
							(
								{
									"name" : "TitleCategoryImage",
									"type" : "image",

									"x" : 1,
									"y" : 0,
									
									"image" : ROOT_PATH_NEW + "bonus/title.png",
									"children" : 
									(
										{
											"name" : "TitleCategory",
											"type" : "text",

											"x" : 5,
											"y" : 3,

											"outline" : 1,
											
											"text" : uiScriptLocale.OPTION_TARGET_BOARD,
										},	
									),
								},		

								{
									"name" : "target_board_off",
									"type" : "radio_button",
				
									"x" : 20,
									"y" : 32,
								
									"default_image" : ROOT_PATH_NEW + "check_empty.png",
									"over_image" : ROOT_PATH_NEW + "check_box.png",
									"down_image" : ROOT_PATH_NEW + "check_box.png",
									"children" : ({"name":"desc", "type":"text", "x":20, "y":0, "text": uiScriptLocale.OPTION_COUNTRYFLAG_ON,},),

								},
								{
									"name" : "target_board_on",
									"type" : "radio_button",
				
									"x" : 20+110,
									"y" : 32,
								
									"default_image" : ROOT_PATH_NEW + "check_empty.png",
									"over_image" : ROOT_PATH_NEW + "check_box.png",
									"down_image" : ROOT_PATH_NEW + "check_box.png",
									"children" : ({"name":"desc", "type":"text", "x":20, "y":0, "text": uiScriptLocale.OPTION_COUNTRYFLAG_OFF,},),
								},

								{
									"name" : "TitleCategoryImage",
									"type" : "image",

									"x" : 1,
									"y" : 55,
									
									"image" : ROOT_PATH_NEW + "bonus/title.png",
									"children" : 
									(
										{
											"name" : "TitleCategory",
											"type" : "text",

											"x" : 5,
											"y" : 3,

											"outline" : 1,
											
											"text" : uiScriptLocale.OPTION_VIEW_CHAT,
										},	
									),
								},		

								{
									"name" : "chat_mode_on",
									"type" : "radio_button",
				
									"x" : 20 + 110,
									"y" : 87,
								
									"default_image" : ROOT_PATH_NEW + "check_empty.png",
									"over_image" : ROOT_PATH_NEW + "check_box.png",
									"down_image" : ROOT_PATH_NEW + "check_box.png",
									"children" : ({"name":"desc", "type":"text", "x":20, "y":0, "text": uiScriptLocale.OPTION_COUNTRYFLAG_OFF,},),

								},
								{
									"name" : "chat_mode_off",
									"type" : "radio_button",
				
									"x" : 20,
									"y" : 87,
								
									"default_image" : ROOT_PATH_NEW + "check_empty.png",
									"over_image" : ROOT_PATH_NEW + "check_box.png",
									"down_image" : ROOT_PATH_NEW + "check_box.png",
									"children" : ({"name":"desc", "type":"text", "x":20, "y":0, "text": uiScriptLocale.OPTION_COUNTRYFLAG_ON,},),
								},

								{
									"name" : "TitleCategoryImage",
									"type" : "image",

									"x" : 1,
									"y" : 107,
									
									"image" : ROOT_PATH_NEW + "bonus/title.png",
									"children" : 
									(
										{
											"name" : "TitleCategory",
											"type" : "text",

											"x" : 5,
											"y" : 3,

											"outline" : 1,
											
											"text" : uiScriptLocale.GAME_OPTIONS_EFFECTS_NAME,
										},	
									),
								},		

								{
									"name" : "damage_mode_on",
									"type" : "radio_button",
				
									"x" : 20,
									"y" : 139,
								
									"default_image" : ROOT_PATH_NEW + "check_empty.png",
									"over_image" : ROOT_PATH_NEW + "check_box.png",
									"down_image" : ROOT_PATH_NEW + "check_box.png",
									"children" : ({"name":"desc", "type":"text", "x":20, "y":0, "text": uiScriptLocale.OPTION_COUNTRYFLAG_ON,},),

								},
								{
									"name" : "damage_mode_off",
									"type" : "radio_button",
				
									"x" : 20+110,
									"y" : 139,
								
									"default_image" : ROOT_PATH_NEW + "check_empty.png",
									"over_image" : ROOT_PATH_NEW + "check_box.png",
									"down_image" : ROOT_PATH_NEW + "check_box.png",
									"children" : ({"name":"desc", "type":"text", "x":20, "y":0, "text": uiScriptLocale.OPTION_COUNTRYFLAG_OFF,},),
								},
								
								{
									"name" : "TitleCategoryImage",
									"type" : "image",

									"x" : 1,
									"y" : 159,
									
									"image" : ROOT_PATH_NEW + "bonus/title.png",
									"children" : 
									(
										{
											"name" : "TitleCategory",
											"type" : "text",

											"x" : 5,
											"y" : 3,

											"outline" : 1,
											
											"text" : uiScriptLocale.OPTION_SALESTEXT,
										},	
									),
								},		

								{
									"name" : "shopname_mode_on",
									"type" : "radio_button",
				
									"x" : 20+110,
									"y" : 191,
								
									"default_image" : ROOT_PATH_NEW + "check_empty.png",
									"over_image" : ROOT_PATH_NEW + "check_box.png",
									"down_image" : ROOT_PATH_NEW + "check_box.png",
									"children" : ({"name":"desc", "type":"text", "x":20, "y":0, "text": uiScriptLocale.OPTION_COUNTRYFLAG_OFF,},),

								},
								{
									"name" : "shopname_mode_off",
									"type" : "radio_button",
				
									"x" : 20,
									"y" : 191,
								
									"default_image" : ROOT_PATH_NEW + "check_empty.png",
									"over_image" : ROOT_PATH_NEW + "check_box.png",
									"down_image" : ROOT_PATH_NEW + "check_box.png",
									"children" : ({"name":"desc", "type":"text", "x":20, "y":0, "text": uiScriptLocale.OPTION_COUNTRYFLAG_ON,},),
								},
								
								{
									"name" : "TitleCategoryImage",
									"type" : "image",

									"x" : 1,
									"y" : 211,
									
									"image" : ROOT_PATH_NEW + "bonus/title.png",
									"children" : 
									(
										{
											"name" : "TitleCategory",
											"type" : "text",

											"x" : 5,
											"y" : 3,

											"outline" : 1,
											
											"text" : uiScriptLocale.GLOBAL_ANNOUNCE,
										},	
									),
								},		

								{
									"name" : "notice_mode_on",
									"type" : "radio_button",
				
									"x" : 20,
									"y" : 243,
								
									"default_image" : ROOT_PATH_NEW + "check_empty.png",
									"over_image" : ROOT_PATH_NEW + "check_box.png",
									"down_image" : ROOT_PATH_NEW + "check_box.png",
									"children" : ({"name":"desc", "type":"text", "x":20, "y":0, "text": uiScriptLocale.OPTION_COUNTRYFLAG_ON,},),

								},
								{
									"name" : "notice_mode_off",
									"type" : "radio_button",
				
									"x" : 20+110,
									"y" : 243,
								
									"default_image" : ROOT_PATH_NEW + "check_empty.png",
									"over_image" : ROOT_PATH_NEW + "check_box.png",
									"down_image" : ROOT_PATH_NEW + "check_box.png",
									"children" : ({"name":"desc", "type":"text", "x":20, "y":0, "text": uiScriptLocale.OPTION_COUNTRYFLAG_OFF,},),
								},

								
								{
									"name" : "TitleCategoryImage",
									"type" : "image",

									"x" : 1,
									"y" : 263,
									
									"image" : ROOT_PATH_NEW + "bonus/title.png",
									"children" : 
									(
										{
											"name" : "TitleCategory",
											"type" : "text",

											"x" : 5,
											"y" : 3,

											"outline" : 1,
											
											"text" : uiScriptLocale.QUEST_SCROLLS,
										},	
									),
								},	
								
								{
									"name" : "missions_off",
									"type" : "radio_button",
				
									"x" : 20+110,
									"y" : 295,
								
									"default_image" : ROOT_PATH_NEW + "check_empty.png",
									"over_image" : ROOT_PATH_NEW + "check_box.png",
									"down_image" : ROOT_PATH_NEW + "check_box.png",
									"children" : ({"name":"desc", "type":"text", "x":20, "y":0, "text": uiScriptLocale.OPTION_COUNTRYFLAG_OFF,},),

								},
								{
									"name" : "missions_on",
									"type" : "radio_button",
				
									"x" : 20,
									"y" : 295,
								
									"default_image" : ROOT_PATH_NEW + "check_empty.png",
									"over_image" : ROOT_PATH_NEW + "check_box.png",
									"down_image" : ROOT_PATH_NEW + "check_box.png",
									"children" : ({"name":"desc", "type":"text", "x":20, "y":0, "text": uiScriptLocale.OPTION_COUNTRYFLAG_ON,},),
								},

							),
						},
						# Ambient Board
						# {
							# "name" : "ambient_opt_board",
							
							# "x" : 170,
							# "y" : 5,
							
							# "width" : 400,
							# "height" : 320,
							
							# "children" : 
							# (
								# {
									# "name" : "TitleCategoryImage",
									# "type" : "image",

									# "x" : 1,
									# "y" : 0,
									
									# "image" : ROOT_PATH_NEW + "bonus/title.png",
									# "children" : 
									# (
										# {
											# "name" : "TitleCategory",
											# "type" : "text",

											# "x" : 5,
											# "y" : 3,

											# "outline" : 1,
											
											# "text" : uiScriptLocale.GAME_OPTIONS_ENVIRONMENT,
										# },	
									# ),
								# },	
								# {
									# "name" : "env_01",
									# "type" : "radio_button",

									# "x" : 20,
									# "y" : 20+30,

									# "default_image" : ROOT_PATH_NEW + "check_empty.png",
									# "over_image" : ROOT_PATH_NEW + "check_box.png",
									# "down_image" : ROOT_PATH_NEW + "check_box.png",
									# "children" : ({"name":"desc", "type":"text", "x":20, "y":0, "text": "Normal Sky",},),
								# },
								
								# {
									# "name" : "env_02",
									# "type" : "radio_button",

									# "x" : 20+120+50,
									# "y" : 20+30,

									# "default_image" : ROOT_PATH_NEW + "check_empty.png",
									# "over_image" : ROOT_PATH_NEW + "check_box.png",
									# "down_image" : ROOT_PATH_NEW + "check_box.png",
									# "children" : ({"name":"desc", "type":"text", "x":20, "y":0, "text": "Night Sky",},),
								# },
								# {
									# "name" : "env_03",
									# "type" : "radio_button",

									# "x" : 20,
									# "y" : 20+30+30,

									# "default_image" : ROOT_PATH_NEW + "check_empty.png",
									# "over_image" : ROOT_PATH_NEW + "check_box.png",
									# "down_image" : ROOT_PATH_NEW + "check_box.png",
									# "children" : ({"name":"desc", "type":"text", "x":20, "y":0, "text": "Moody Sky",},),
								# },
								
								# {
									# "name" : "env_04",
									# "type" : "radio_button",

									# "x" : 20+120+50,
									# "y" : 20+30+30,

									# "default_image" : ROOT_PATH_NEW + "check_empty.png",
									# "over_image" : ROOT_PATH_NEW + "check_box.png",
									# "down_image" : ROOT_PATH_NEW + "check_box.png",
									# "children" : ({"name":"desc", "type":"text", "x":20, "y":0, "text": "Red Sky",},),
								# },
								# {
									# "name" : "env_05",
									# "type" : "radio_button",

									# "x" : 20,
									# "y" : 20+30+30+30,

									# "default_image" : ROOT_PATH_NEW + "check_empty.png",
									# "over_image" : ROOT_PATH_NEW + "check_box.png",
									# "down_image" : ROOT_PATH_NEW + "check_box.png",
									# "children" : ({"name":"desc", "type":"text", "x":20, "y":0, "text": "Bright Red Sky",},),
								# },
								
								# {
									# "name" : "env_06",
									# "type" : "radio_button",

									# "x" : 20+120+50,
									# "y" : 20+30+30+30,

									# "default_image" : ROOT_PATH_NEW + "check_empty.png",
									# "over_image" : ROOT_PATH_NEW + "check_box.png",
									# "down_image" : ROOT_PATH_NEW + "check_box.png",
									# "children" : ({"name":"desc", "type":"text", "x":20, "y":0, "text": "Green Sky",},),
								# },	
								# {
									# "name" : "env_07",
									# "type" : "radio_button",

									# "x" : 20,
									# "y" : 20+30+30+30+30,

									# "default_image" : ROOT_PATH_NEW + "check_empty.png",
									# "over_image" : ROOT_PATH_NEW + "check_box.png",
									# "down_image" : ROOT_PATH_NEW + "check_box.png",
									# "children" : ({"name":"desc", "type":"text", "x":20, "y":0, "text": "Gray Sky",},),
								# },
							# ),
						# },
						
						{
							"name" : "character1",
							"type" : "radio_button",

							"x" : 10,
							"y" : 17+28,

							"text" : uiScriptLocale.GAME_OPTIONS_INTERFACE,
							
							"default_image" : ROOT_PATH_NEW + "button_norm.png",
							"over_image" : ROOT_PATH_NEW + "button_over.png",
							"down_image" : ROOT_PATH_NEW + "button_down.png",
						},
						# {
							# "name" : "character2",
							# "type" : "radio_button",

							# "x" : 10,
							# "y" : 17+28*2,

							# "text" : uiScriptLocale.GAME_OPTIONS_ENVIRONMENT,

							# "default_image" : ROOT_PATH_NEW + "button_norm.png",
							# "over_image" : ROOT_PATH_NEW + "button_over.png",
							# "down_image" : ROOT_PATH_NEW + "button_down.png",
						# },
					),
				},
				{
					"name" : "background_graphics", 
					
					"x" : 10, 
					"y" : 66,

					"width" : 451,
					"height" : 320,
					
					"children" : 
					(
						{
							"name" : "display_settings_option_board",
							
							"x" : 170,
							"y" : 5,
							
							"width" : 400,
							"height" : 320,
							
							"children" : 
							(
								{
									"name" : "TitleCategoryImage",
									"type" : "image",

									"x" : 1,
									"y" : 0,
									
									"image" : ROOT_PATH_NEW + "bonus/title.png",
									"children" : 
									(
										{
											"name" : "TitleCategory",
											"type" : "text",

											"x" : 5,
											"y" : 3,

											"outline" : 1,
											
											"text" : uiScriptLocale.GAME_OPTIONS_HIDE_ELEMENTS,
										},	
									),
								},	
								{
									"name" : "hide_pets",
									"type" : "toggle_button",

									"x" : 20,
									"y" : 32,

									"default_image" : ROOT_PATH_NEW + "checkbox_new_unselected.tga",
									"over_image" : ROOT_PATH_NEW + "checkbox_new_unselected.tga",
									"down_image" : ROOT_PATH_NEW + "checkbox_new_selected.tga",
									"children" : ({"name":"desc", "type":"text", "x":20, "y":-1, "text": uiScriptLocale.GAME_OPTIONS_HIDE_PETS,},),

								},
								{
									"name" : "hide_mounts",
									"type" : "toggle_button",

									"x" : 20 + 70,
									"y" : 32,

									"default_image" : ROOT_PATH_NEW + "checkbox_new_unselected.tga",
									"over_image" : ROOT_PATH_NEW + "checkbox_new_unselected.tga",
									"down_image" : ROOT_PATH_NEW + "checkbox_new_selected.tga",
									
									"children" : ({"name":"desc", "type":"text", "x":20, "y":-1, "text": uiScriptLocale.GAME_OPTIONS_HIDE_MOUNTS,},),
								},
								{
									"name" : "hide_shops",
									"type" : "toggle_button",

									"x" : 20 + 70 + 70,
									"y" : 32,

									"default_image" : ROOT_PATH_NEW + "checkbox_new_unselected.tga",
									"over_image" : ROOT_PATH_NEW + "checkbox_new_unselected.tga",
									"down_image" : ROOT_PATH_NEW + "checkbox_new_selected.tga",
									
									"children" : ({"name":"desc", "type":"text", "x":20, "y":-1, "text": uiScriptLocale.GAME_OPTIONS_HIDE_SHOPS,},),
								},
								{
									"name" : "TitleCategoryImage",
									"type" : "image",

									"x" : 1,
									"y" : 55,
									
									"image" : ROOT_PATH_NEW + "bonus/title.png",
									"children" : 
									(
										{
											"name" : "TitleCategory",
											"type" : "text",

											"x" : 5,
											"y" : 3,

											"outline" : 1,
											
											"text" : uiScriptLocale.METIN_SCALE,
										},	
									),
								},	
								{
									"name" : "scale_bar",
									"type" : "sliderbar",

									"x" : 5,
									"y" : 87,
								},
								{
									"name" : "TitleCategoryImage",
									"type" : "image",

									"x" : 1,
									"y" : 110,
									
									"image" : ROOT_PATH_NEW + "bonus/title.png",
									"children" : 
									(
										{
											"name" : "TitleCategory",
											"type" : "text",

											"x" : 5,
											"y" : 3,

											"outline" : 1,
											
											"text" : uiScriptLocale.FOV_SETTING,
										},	
									),
								},	
								{
									"name" : "fov_bar",
									"type" : "sliderbar",

									"x" : 5,
									"y" : 142,
								},
								
								{
									"name" : "TitleCategoryImage",
									"type" : "image",

									"x" : 1,
									"y" : 165,
									
									"image" : ROOT_PATH_NEW + "bonus/title.png",
									"children" : 
									(
										{
											"name" : "TitleCategory",
											"type" : "text",

											"x" : 5,
											"y" : 3,

											"outline" : 1,
											
											"text" : uiScriptLocale.MODEL_DOG_MODE_STATUS,
										},	
									),
								},	
								
								{
									"name" : "dog_mode_off",
									"type" : "radio_button",
				
									"x" : 20+110,
									"y" : 197,
								
									"default_image" : ROOT_PATH_NEW + "check_empty.png",
									"over_image" : ROOT_PATH_NEW + "check_box.png",
									"down_image" : ROOT_PATH_NEW + "check_box.png",
									"children" : ({"name":"desc", "type":"text", "x":20, "y":0, "text": uiScriptLocale.OPTION_COUNTRYFLAG_OFF,},),

								},
								{
									"name" : "dog_mode_on",
									"type" : "radio_button",
				
									"x" : 20,
									"y" : 197,
								
									"default_image" : ROOT_PATH_NEW + "check_empty.png",
									"over_image" : ROOT_PATH_NEW + "check_box.png",
									"down_image" : ROOT_PATH_NEW + "check_box.png",
									"children" : ({"name":"desc", "type":"text", "x":20, "y":0, "text": uiScriptLocale.OPTION_COUNTRYFLAG_ON,},),
								},
								
								{
									"name" : "TitleCategoryImage",
									"type" : "image",

									"x" : 1,
									"y" : 217,
									
									"image" : ROOT_PATH_NEW + "bonus/title.png",
									"children" : 
									(
										{
											"name" : "TitleCategory",
											"type" : "text",

											"x" : 5,
											"y" : 3,

											"outline" : 1,
											
											"text" : uiScriptLocale.AFFECT_ICONS,
										},	
									),
								},	
								
								{
									"name" : "affects_off",
									"type" : "radio_button",
				
									"x" : 20+110,
									"y" : 249,
								
									"default_image" : ROOT_PATH_NEW + "check_empty.png",
									"over_image" : ROOT_PATH_NEW + "check_box.png",
									"down_image" : ROOT_PATH_NEW + "check_box.png",
									"children" : ({"name":"desc", "type":"text", "x":20, "y":0, "text": uiScriptLocale.OPTION_COUNTRYFLAG_OFF,},),

								},
								{
									"name" : "affects_on",
									"type" : "radio_button",
				
									"x" : 20,
									"y" : 249,
								
									"default_image" : ROOT_PATH_NEW + "check_empty.png",
									"over_image" : ROOT_PATH_NEW + "check_box.png",
									"down_image" : ROOT_PATH_NEW + "check_box.png",
									"children" : ({"name":"desc", "type":"text", "x":20, "y":0, "text": uiScriptLocale.OPTION_COUNTRYFLAG_ON,},),
								},
								
								# {
									# "name" : "TitleCategoryImage",
									# "type" : "image",

									# "x" : 1,
									# "y" : 269,
									
									# "image" : ROOT_PATH_NEW + "bonus/title.png",
									# "children" : 
									# (
										# {
											# "name" : "TitleCategory",
											# "type" : "text",

											# "x" : 5,
											# "y" : 3,

											# "outline" : 1,
											
											# "text" : uiScriptLocale.INTERFACE_OPTIONS,
										# },	
									# ),
								# },		
								
								# {
									# "name" : "interface_off",
									# "type" : "radio_button",
				
									# "x" : 20+110,
									# "y" : 301,
								
									# "default_image" : ROOT_PATH_NEW + "check_empty.png",
									# "over_image" : ROOT_PATH_NEW + "check_box.png",
									# "down_image" : ROOT_PATH_NEW + "check_box.png",
									# "children" : ({"name":"desc", "type":"text", "x":20, "y":0, "text": uiScriptLocale.INTERFACE_OPTIONS_1,},),

								# },
								# {
									# "name" : "interface_on",
									# "type" : "radio_button",
				
									# "x" : 20,
									# "y" : 301,
								
									# "default_image" : ROOT_PATH_NEW + "check_empty.png",
									# "over_image" : ROOT_PATH_NEW + "check_box.png",
									# "down_image" : ROOT_PATH_NEW + "check_box.png",
									# "children" : ({"name":"desc", "type":"text", "x":20, "y":0, "text": uiScriptLocale.INTERFACE_OPTIONS_2,},),
								# },
								
							),
						},
						{
							"name" : "advanced_option_board",
							
							"x" : 170,
							"y" : 5,
							
							"width" : 400,
							"height" : 320,
							
							"children" : 
							(
								{
									"name" : "TitleCategoryImage",
									"type" : "image",

									"x" : 1,
									"y" : 0,
									
									"image" : ROOT_PATH_NEW + "bonus/title.png",
									"children" : 
									(
										{
											"name" : "TitleCategory",
											"type" : "text",

											"x" : 5,
											"y" : 3,

											"outline" : 1,
											
											"text" : uiScriptLocale.GAME_OPTIONS_CAMERA_DISTANCE,
										},	
									),
								},		
								
								{
									"name" : "camera_mode_1",
									"type" : "radio_button",

									"x" : 20,
									"y" : 32,

									"default_image" : ROOT_PATH_NEW + "check_empty.png",
									"over_image" : ROOT_PATH_NEW + "check_box.png",
									"down_image" : ROOT_PATH_NEW + "check_box.png",
									
									"children" : 
									(
										{"name":"desc", "type":"text", "x":20, "y":0, "text": uiScriptLocale.OPTION_CAMERA_DISTANCE_SHORT,},
									),
								},
								{
									"name" : "camera_mode_2",
									"type" : "radio_button",

									"x" : 20+70,
									"y" : 32,

									"default_image" : ROOT_PATH_NEW + "check_empty.png",
									"over_image" : ROOT_PATH_NEW + "check_box.png",
									"down_image" : ROOT_PATH_NEW + "check_box.png",
									
									"children" : ({"name":"desc", "type":"text", "x":20, "y":0, "text": uiScriptLocale.OPTION_CAMERA_DISTANCE_LONG,},),
									
								},
								{
									"name" : "TitleCategoryImage",
									"type" : "image",

									"x" : 1,
									"y" : 55,
									
									"image" : ROOT_PATH_NEW + "bonus/title.png",
									"children" : 
									(
										{
											"name" : "TitleCategory",
											"type" : "text",

											"x" : 5,
											"y" : 3,

											"outline" : 1,
											
											"text" : uiScriptLocale.OPTION_FOG,
										},	
									),
								},		
								
								{
									"name" : "fog_level0",
									"type" : "radio_button",

									"x" : 20,
									"y" : 87,

									"default_image" : ROOT_PATH_NEW + "check_empty.png",
									"over_image" : ROOT_PATH_NEW + "check_box.png",
									"down_image" : ROOT_PATH_NEW + "check_box.png",
									
									"children" : 
									(
										{"name":"desc", "type":"text", "x":20, "y":0, "text": uiScriptLocale.OPTION_FOG_DENSE,},
									),
								},
								
								{
									"name" : "fog_level1",
									"type" : "radio_button",

									"x" : 20+70,
									"y" : 87,
									
									"default_image" : ROOT_PATH_NEW + "check_empty.png",
									"over_image" : ROOT_PATH_NEW + "check_box.png",
									"down_image" : ROOT_PATH_NEW + "check_box.png",
									"children" : ({"name":"desc", "type":"text", "x":20, "y":0, "text": uiScriptLocale.OPTION_FOG_MIDDLE,},),
								},
								
								{
									"name" : "fog_level2",
									"type" : "radio_button",

									"x" : 20+70+70,
									"y" : 87,
									
									"default_image" : ROOT_PATH_NEW + "check_empty.png",
									"over_image" : ROOT_PATH_NEW + "check_box.png",
									"down_image" : ROOT_PATH_NEW + "check_box.png",
									"children" : ({"name":"desc", "type":"text", "x":20, "y":0, "text": uiScriptLocale.OPTION_FOG_LIGHT,},),
								},
								
								{
									"name" : "TitleCategoryImage",
									"type" : "image",

									"x" : 1,
									"y" : 110,
									
									"image" : ROOT_PATH_NEW + "bonus/title.png",
									"children" : 
									(
										{
											"name" : "TitleCategory",
											"type" : "text",

											"x" : 5,
											"y" : 3,

											"outline" : 1,
											
											"text" : uiScriptLocale.OPTION_TILING,
										},	
									),
								},		
								
								
								{
									"name" : "tiling_cpu",
									"type" : "radio_button",

									"x" : 20,
									"y" : 142,
									
									"default_image" : ROOT_PATH_NEW + "check_empty.png",
									"over_image" : ROOT_PATH_NEW + "check_box.png",
									"down_image" : ROOT_PATH_NEW + "check_box.png",
									"children" : 
									(
										{"name":"desc", "type":"text", "x":20, "y":0, "text": "CPU",},
									),
								},
								
								{
									"name" : "tiling_gpu",
									"type" : "radio_button",

									"x" : 20+70,
									"y" : 142,
									
									"default_image" : ROOT_PATH_NEW + "check_empty.png",
									"over_image" : ROOT_PATH_NEW + "check_box.png",
									"down_image" : ROOT_PATH_NEW + "check_box.png",
									"children" : ({"name":"desc", "type":"text", "x":20, "y":0, "text": "GPU",},),
								},
								
								{
									"name" : "TitleCategoryImage",
									"type" : "image",

									"x" : 1,
									"y" : 165,
									
									"image" : ROOT_PATH_NEW + "bonus/title.png",
									"children" : 
									(
										{
											"name" : "TitleCategory",
											"type" : "text",

											"x" : 5,
											"y" : 3,

											"outline" : 1,
											
											"text" : uiScriptLocale.GAME_OPTIONS_EFFECTS_NAME,
										},	
									),
								},			
								
								{
									"name" : "hide_effects_off",
									"type" : "radio_button",
				
									"x" : 20,
									"y" : 197,
								
									"default_image" : ROOT_PATH_NEW + "check_empty.png",
									"over_image" : ROOT_PATH_NEW + "check_box.png",
									"down_image" : ROOT_PATH_NEW + "check_box.png",
									"children" : ({"name":"desc", "type":"text", "x":20, "y":0, "text": uiScriptLocale.OPTION_COUNTRYFLAG_ON,},),

								},
								{
									"name" : "hide_effects_on",
									"type" : "radio_button",
				
									"x" : 20+110,
									"y" : 197,
								
									"default_image" : ROOT_PATH_NEW + "check_empty.png",
									"over_image" : ROOT_PATH_NEW + "check_box.png",
									"down_image" : ROOT_PATH_NEW + "check_box.png",
									"children" : ({"name":"desc", "type":"text", "x":20, "y":0, "text": uiScriptLocale.OPTION_COUNTRYFLAG_OFF,},),
								},

								{
									"name" : "TitleCategoryImage",
									"type" : "image",

									"x" : 1,
									"y" : 220,
									
									"image" : ROOT_PATH_NEW + "bonus/title.png",
									"children" : 
									(
										{
											"name" : "TitleCategory",
											"type" : "text",

											"x" : 5,
											"y" : 3,

											"outline" : 1,
											
											"text" : uiScriptLocale.GRAPHIC_MODE,
										},	
									),
								},		
								
								{
									"name" : "anim_off",
									"type" : "radio_button",
				
									"x" : 20+110,
									"y" : 252,
								
									"default_image" : ROOT_PATH_NEW + "check_empty.png",
									"over_image" : ROOT_PATH_NEW + "check_box.png",
									"down_image" : ROOT_PATH_NEW + "check_box.png",
									"children" : ({"name":"desc", "type":"text", "x":20, "y":0, "text": uiScriptLocale.OPTION_COUNTRYFLAG_OFF,},),

								},
								{
									"name" : "anim_on",
									"type" : "radio_button",
				
									"x" : 20,
									"y" : 252,
								
									"default_image" : ROOT_PATH_NEW + "check_empty.png",
									"over_image" : ROOT_PATH_NEW + "check_box.png",
									"down_image" : ROOT_PATH_NEW + "check_box.png",
									"children" : ({"name":"desc", "type":"text", "x":20, "y":0, "text": uiScriptLocale.OPTION_COUNTRYFLAG_ON,},),
								},

								
							),
						},
						{
							"name" : "display_settings_graphics",
							"type" : "radio_button",

							"x" : 10,
							"y" : 17,

							"text" : uiScriptLocale.GAME_OPTIONS_ACCOUNT_SETTINGS,
							
							"default_image" : ROOT_PATH_NEW + "button_norm.png",
							"over_image" : ROOT_PATH_NEW + "button_over.png",
							"down_image" : ROOT_PATH_NEW + "button_down.png",
						},
						{
							"name" : "advanced_settings_graphics",
							"type" : "radio_button",

							"x" : 10,
							"y" : 17+28,

							"text" : uiScriptLocale.DISPLAY_SETTINGS,

							"default_image" : ROOT_PATH_NEW + "button_norm.png",
							"over_image" : ROOT_PATH_NEW + "button_over.png",
							"down_image" : ROOT_PATH_NEW + "button_down.png",
						},
					),
				},
				{
					"name" : "category_game_option",
					"type" : "radio_button",
					
					"x" : 20,
					"y" : 40,
					"text" : uiScriptLocale.GAME_SETTINGS,
					"default_image" : ROOT_PATH_NEW + "btn_select_1.png",
					"over_image" : ROOT_PATH_NEW + "btn_select_2.png",
					"down_image" : ROOT_PATH_NEW + "btn_select_3.png",
				},
				{
					"name" : "category_graphics_option",
					"type" : "radio_button",
					
					"x" : 20 + 105,
					"y" : 40,
					"text" : uiScriptLocale.GRAPHIC_SETTINGS,
					"default_image" : ROOT_PATH_NEW + "btn_select_1.png",
					"over_image" : ROOT_PATH_NEW + "btn_select_2.png",
					"down_image" : ROOT_PATH_NEW + "btn_select_3.png",
				},
			),
		},
	),
}
