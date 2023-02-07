import uiScriptLocale
import localeInfo

ROOT_PATH = "d:/ymir work/ui/game/statistics/"

WINDOW_WIDTH = 500
WINDOW_HEIGHT = 445

window = {
	"name" : "GameStatisticsWindow",
	"style" : ("movable", "float", "animation", ),

	"x" : SCREEN_WIDTH / 2 - WINDOW_WIDTH / 2 - 125,
	"y" : SCREEN_HEIGHT / 2 - WINDOW_HEIGHT / 2,
	
	"width" : WINDOW_WIDTH,
	"height" : WINDOW_HEIGHT,
	
	"children" :
	(
		{
			"name" : "board",
			"type" : "board",
			"style" : ("attach",),

			"x" : 0,
			"y" : 0,

			"width" : WINDOW_WIDTH,
			"height" : WINDOW_HEIGHT - 64,

			"children" :
			(
				{
					"name" : "TitleBar",
					"type" : "titlebar",
					"style" : ("attach",),

					"x" : 8,
					"y" : 7,

					"width" : WINDOW_WIDTH - 15,
					"children" :
					(
						{ "name" : "TitleName", "type" : "text", "x" : WINDOW_WIDTH / 2, "y" : 3, "text" : uiScriptLocale.GAME_STATISTICS_TITLE, "text_horizontal_align" : "center" },
					),
				},
			),
		},
		{
			"name" : "tab_control",
			"type" : "window",

			"x" : 0,
			"y" : WINDOW_HEIGHT - 77,

			"width" : 500,
			"height" : 64,

			"children":
			(
				{
					"name" : "tab_image",
					"type" : "image",

					"x" : 0,
					"y" : 0,

					"width" : 500,
					"height" : 64,

					"image" : ROOT_PATH + "tab_01.png",
				},
				{
					"name" : "tab_button_01",
					"type" : "button",

					"x" : 11,
					"y" : 22,

					"width" : 100,
					"height" : 34,
				},
				{
					"name" : "tab_button_02",
					"type" : "button",

					"x" : 125,
					"y" : 22,

					"width" : 100,
					"height" : 34,
				},
				{
					"name" : "tab_button_03",
					"type" : "button",

					"x" : 235,
					"y" : 22,

					"width" : 100,
					"height" : 34,
				},
			),
		},

		{
			"name" : "InfoBoard",
			"type" : "border_a",

			"x" : 40,
			"y" : 35,

			"width" : WINDOW_WIDTH - 80,
			"height" : 35,
			
			"children":
			(
				{
					"name" : "InfoText", 
					"type" : "text", 
					
					"x" : 0, 
					"y" : 4, 
					
					"text" : "Test Info Text", 
					
					"horizontal_align" : "center",
					"text_horizontal_align" : "center",
				},
			),
		},
		
		{
			"name" : "InfoButton", 
			"type" : "button", 
			
			"x" : 435, 
			"y" : 36, 
			
			"default_image" : ROOT_PATH + "last_week_winners_btn_01.png",
			"over_image" : ROOT_PATH + "last_week_winners_btn_02.png",
			"down_image" : ROOT_PATH + "last_week_winners_btn_03.png",
		},
		
		# Why here and not on the board ? Why not ? :)))
		# PS: it overlaps with the tabs
		{
			"name" : "MainBoard",
			"type" : "border_a",

			"x" : 15,
			"y" : 55,

			"width" : WINDOW_WIDTH - 30,
			"height" : 315,
			
			"children":
			(
				{
					"name" : "PersonalInfoPage",
					"type" : "window",
		
					"x" : 0,
					"y" : 0,
		
					"width" : WINDOW_WIDTH - 30,
					"height" : 315,
		
					"children":
					(
						{
							"name" : "pi_btn_type_0",
							"type" : "button",
		
							"x" : 1,	# 1/226
							"y" : 1,	# 1 / 1 + (i * 102)
		
							"default_image" : ROOT_PATH + "personal/00_normal.png",
							"over_image" : ROOT_PATH + "personal/00_over.png",
							"down_image" : ROOT_PATH + "personal/00_over.png",
							
							"children":
							(
								{
									"name" : "pi_text_name_1_type_0", 
									"type" : "text", 
									
									"x" : 0,
									"y" : 70,
									
									"text" : uiScriptLocale.GAME_STATISTICS_STONES_DMG.split("\n")[0], 
									
									"horizontal_align" : "center",
									"text_horizontal_align" : "center",
									
									"outline" : True,
									"r" : 1.0, "g" : 1.0, "b" : 1.0, "a" : 0.7, 
								},
								{
									"name" : "pi_text_name_2_type_0", 
									"type" : "text", 
									
									"x" : 0,
									"y" : 70+12,
									
									"text" : uiScriptLocale.GAME_STATISTICS_STONES_DMG.split("\n")[1], 
									
									"horizontal_align" : "center",
									"text_horizontal_align" : "center",
									
									"outline" : True,
									"r" : 1.0, "g" : 1.0, "b" : 1.0, "a" : 0.7, 
								},
								{
									"name" : "pi_text_value_type_0", 
									"type" : "text", 
									
									"fontname" : "Tahoma:14b",
									
									"x" : 0, 
									"y" : 27, 
									
									"text" : "69.000.000", 
									
									"horizontal_align" : "center",
									"text_horizontal_align" : "center",

									"r" : 1.0, "g" : 1.0, "b" : 1.0, "a" : 0.7,
								},
								{
									"name" : "pi_text_value_w_type_0", 
									"type" : "text", 
									
									"fontname" : "Tahoma:14b",
									
									"x" : 0, 
									"y" : 27-7, 
									
									"text" : localeInfo.GAME_STATISTICS_PERSONAL_THIS_WEEK.split("\n")[0], 
									
									"horizontal_align" : "center",
									"text_horizontal_align" : "center",

									"r" : 1.0, "g" : 1.0, "b" : 1.0, "a" : 0.7,
								},
							),
						},
						{
							"name" : "pi_btn_type_1",
							"type" : "button",
		
							"x" : 226,
							"y" : 1,
		
							"default_image" : ROOT_PATH + "personal/01_normal.png",
							"over_image" : ROOT_PATH + "personal/01_over.png",
							"down_image" : ROOT_PATH + "personal/01_over.png",
							
							"children":
							(
								{
									"name" : "pi_text_name_1_type_1", 
									"type" : "text", 
									
									"x" : 0,
									"y" : 70,
									
									"text" : uiScriptLocale.GAME_STATISTICS_STONES_KILL.split("\n")[0],
									
									"horizontal_align" : "center",
									"text_horizontal_align" : "center",
									
									"outline" : True,
									"r" : 1.0, "g" : 1.0, "b" : 1.0, "a" : 0.7, 
								},
								{
									"name" : "pi_text_name_2_type_1", 
									"type" : "text", 
									
									"x" : 0,
									"y" : 70+12,
									
									"text" : uiScriptLocale.GAME_STATISTICS_STONES_KILL.split("\n")[1],
									
									"horizontal_align" : "center",
									"text_horizontal_align" : "center",
									
									"outline" : True,
									"r" : 1.0, "g" : 1.0, "b" : 1.0, "a" : 0.7, 
								},
								{
									"name" : "pi_text_value_type_1", 
									"type" : "text", 
									
									"fontname" : "Tahoma:14b",
									
									"x" : 0, 
									"y" : 27, 
									
									"text" : "69.000.000", 
									
									"horizontal_align" : "center",
									"text_horizontal_align" : "center",
									
									"r" : 1.0, "g" : 1.0, "b" : 1.0, "a" : 0.7,
								},
								{
									"name" : "pi_text_value_w_type_1", 
									"type" : "text", 
									
									"fontname" : "Tahoma:14b",
									
									"x" : 0, 
									"y" : 27-7, 
									
									"text" : localeInfo.GAME_STATISTICS_PERSONAL_THIS_WEEK.split("\n")[0], 
									
									"horizontal_align" : "center",
									"text_horizontal_align" : "center",
									
									"r" : 1.0, "g" : 1.0, "b" : 1.0, "a" : 0.7,
								},	
							),
						},
						{
							"name" : "pi_btn_type_2",
							"type" : "button",
		
							"x" : 1,
							"y" : 1 + 102,
		
							"default_image" : ROOT_PATH + "personal/02_normal.png",
							"over_image" : ROOT_PATH + "personal/02_over.png",
							"down_image" : ROOT_PATH + "personal/02_over.png",
							
							"children":
							(
								{
									"name" : "pi_text_name_1_type_2", 
									"type" : "text", 
									
									"x" : 0,
									"y" : 70,
									
									"text" : uiScriptLocale.GAME_STATISTICS_LEADERS_DMG.split("\n")[0],
									
									"horizontal_align" : "center",
									"text_horizontal_align" : "center",
									
									"outline" : True,
									"r" : 1.0, "g" : 1.0, "b" : 1.0, "a" : 0.7, 
								},
								{
									"name" : "pi_text_name_2_type_2", 
									"type" : "text", 
									
									"x" : 0,
									"y" : 70+12,
									
									"text" : uiScriptLocale.GAME_STATISTICS_LEADERS_DMG.split("\n")[1],
									
									"horizontal_align" : "center",
									"text_horizontal_align" : "center",
									
									"outline" : True,
									"r" : 1.0, "g" : 1.0, "b" : 1.0, "a" : 0.7, 
								},
								{
									"name" : "pi_text_value_type_2", 
									"type" : "text", 
									
									"fontname" : "Tahoma:14b",
									
									"x" : 0, 
									"y" : 27, 
									
									"text" : "69.000.000", 
									
									"horizontal_align" : "center",
									"text_horizontal_align" : "center",
									
									"r" : 1.0, "g" : 1.0, "b" : 1.0, "a" : 0.7,
								},
								{
									"name" : "pi_text_value_w_type_2", 
									"type" : "text", 
									
									"fontname" : "Tahoma:14b",
									
									"x" : 0, 
									"y" : 27-7, 
									
									"text" : localeInfo.GAME_STATISTICS_PERSONAL_THIS_WEEK.split("\n")[0], 
									
									"horizontal_align" : "center",
									"text_horizontal_align" : "center",
									
									"r" : 1.0, "g" : 1.0, "b" : 1.0, "a" : 0.7,
								},
							),
						},
						{
							"name" : "pi_btn_type_3",
							"type" : "button",
		
							"x" : 226,
							"y" : 1 + 102,
		
							"default_image" : ROOT_PATH + "personal/03_normal.png",
							"over_image" : ROOT_PATH + "personal/03_over.png",
							"down_image" : ROOT_PATH + "personal/03_over.png",
							
							"children":
							(
								{
									"name" : "pi_text_name_1_type_3", 
									"type" : "text", 
									
									"x" : 0,
									"y" : 70,
									
									"text" : uiScriptLocale.GAME_STATISTICS_LEADERS_KILL.split("\n")[0],
									
									"horizontal_align" : "center",
									"text_horizontal_align" : "center",
									
									"outline" : True,
									"r" : 1.0, "g" : 1.0, "b" : 1.0, "a" : 0.7, 
								},
								{
									"name" : "pi_text_name_2_type_3", 
									"type" : "text", 
									
									"x" : 0,
									"y" : 70+12,
									
									"text" : uiScriptLocale.GAME_STATISTICS_LEADERS_KILL.split("\n")[1],
									
									"horizontal_align" : "center",
									"text_horizontal_align" : "center",
									
									"outline" : True,
									"r" : 1.0, "g" : 1.0, "b" : 1.0, "a" : 0.7, 
								},
								{
									"name" : "pi_text_value_type_3", 
									"type" : "text", 
									
									"fontname" : "Tahoma:14b",
									
									"x" : 0, 
									"y" : 27, 
									
									"text" : "69.000.000", 
									
									"horizontal_align" : "center",
									"text_horizontal_align" : "center",
									
									"r" : 1.0, "g" : 1.0, "b" : 1.0, "a" : 0.7,
								},
								{
									"name" : "pi_text_value_w_type_3", 
									"type" : "text", 
									
									"fontname" : "Tahoma:14b",
									
									"x" : 0, 
									"y" : 27-7, 
									
									"text" : localeInfo.GAME_STATISTICS_PERSONAL_THIS_WEEK.split("\n")[0], 
									
									"horizontal_align" : "center",
									"text_horizontal_align" : "center",
									
									"r" : 1.0, "g" : 1.0, "b" : 1.0, "a" : 0.7,
								},
							),
						},
						{
							"name" : "pi_btn_type_4",
							"type" : "button",
		
							"x" : 1,
							"y" : 1 + 102 + 102,
		
							"default_image" : ROOT_PATH + "personal/04_normal.png",
							"over_image" : ROOT_PATH + "personal/04_over.png",
							"down_image" : ROOT_PATH + "personal/04_over.png",
							
							"children":
							(
								{
									"name" : "pi_text_name_1_type_4", 
									"type" : "text", 
									
									"x" : 0,
									"y" : 70,
									
									"text" : uiScriptLocale.GAME_STATISTICS_FISHES_CAUGHT.split("\n")[0],
									
									"horizontal_align" : "center",
									"text_horizontal_align" : "center",
									
									"outline" : True,
									"r" : 1.0, "g" : 1.0, "b" : 1.0, "a" : 0.7, 
								},
								{
									"name" : "pi_text_name_2_type_4", 
									"type" : "text", 
									
									"x" : 0,
									"y" : 70+12,
									
									"text" : uiScriptLocale.GAME_STATISTICS_FISHES_CAUGHT.split("\n")[1],
									
									"horizontal_align" : "center",
									"text_horizontal_align" : "center",
									
									"outline" : True,
									"r" : 1.0, "g" : 1.0, "b" : 1.0, "a" : 0.7, 
								},
								{
									"name" : "pi_text_value_type_4", 
									"type" : "text", 
									
									"fontname" : "Tahoma:14b",
									
									"x" : 0, 
									"y" : 27, 
									
									"text" : "69.000.000", 
									
									"horizontal_align" : "center",
									"text_horizontal_align" : "center",
									
									"r" : 1.0, "g" : 1.0, "b" : 1.0, "a" : 0.7,
								},
								{
									"name" : "pi_text_value_w_type_4", 
									"type" : "text", 
									
									"fontname" : "Tahoma:14b",
									
									"x" : 0, 
									"y" : 27-7, 
									
									"text" : localeInfo.GAME_STATISTICS_PERSONAL_THIS_WEEK.split("\n")[0], 
									
									"horizontal_align" : "center",
									"text_horizontal_align" : "center",
									
									"r" : 1.0, "g" : 1.0, "b" : 1.0, "a" : 0.7,
								},
							),
						},
						{
							"name" : "pi_btn_type_5",
							"type" : "button",
		
							"x" : 226,
							"y" : 1 + 102 + 102,
		
							"default_image" : ROOT_PATH + "personal/05_normal.png",
							"over_image" : ROOT_PATH + "personal/05_over.png",
							"down_image" : ROOT_PATH + "personal/05_over.png",
							
							"children":
							(
								{
									"name" : "pi_text_name_1_type_5", 
									"type" : "text", 
									
									"x" : 0,
									"y" : 70,
									
									"text" : uiScriptLocale.GAME_STATISTICS_REFINE_ITEMS.split("\n")[0],
									
									"horizontal_align" : "center",
									"text_horizontal_align" : "center",
									
									"outline" : True,
									"r" : 1.0, "g" : 1.0, "b" : 1.0, "a" : 0.7, 
								},
								{
									"name" : "pi_text_name_2_type_5", 
									"type" : "text", 
									
									"x" : 0,
									"y" : 70+12,
									
									"text" : uiScriptLocale.GAME_STATISTICS_REFINE_ITEMS.split("\n")[1],
									
									"horizontal_align" : "center",
									"text_horizontal_align" : "center",
									
									"outline" : True,
									"r" : 1.0, "g" : 1.0, "b" : 1.0, "a" : 0.7, 
								},
								{
									"name" : "pi_text_value_type_5", 
									"type" : "text", 
									
									"fontname" : "Tahoma:14b",
									
									"x" : 0, 
									"y" : 27, 
									
									"text" : "69.000.000", 
									
									"horizontal_align" : "center",
									"text_horizontal_align" : "center",
									
									"r" : 1.0, "g" : 1.0, "b" : 1.0, "a" : 0.7,
								},
								{
									"name" : "pi_text_value_w_type_5", 
									"type" : "text", 
									
									"fontname" : "Tahoma:14b",
									
									"x" : 0, 
									"y" : 27-7, 
									
									"text" : localeInfo.GAME_STATISTICS_PERSONAL_THIS_WEEK.split("\n")[0], 
									
									"horizontal_align" : "center",
									"text_horizontal_align" : "center",
									
									"r" : 1.0, "g" : 1.0, "b" : 1.0, "a" : 0.7,
								},
							),
						},
						{
							"name" : "pi_btn_type_6",
							"type" : "button",
		
							"x" : 1,
							"y" : 1 + 102 + 102 + 102,
		
							"default_image" : ROOT_PATH + "personal/06_normal.png",
							"over_image" : ROOT_PATH + "personal/06_over.png",
							"down_image" : ROOT_PATH + "personal/06_over.png",
							
							"children":
							(
								{
									"name" : "pi_text_name_1_type_6", 
									"type" : "text", 
									
									"x" : 0,
									"y" : 70,
									
									"text" : uiScriptLocale.GAME_STATISTICS_COMPLETED_DUNGEONS.split("\n")[0],
									
									"horizontal_align" : "center",
									"text_horizontal_align" : "center",
									
									"outline" : True,
									"r" : 1.0, "g" : 1.0, "b" : 1.0, "a" : 0.7, 
								},
								{
									"name" : "pi_text_name_2_type_6", 
									"type" : "text", 
									
									"x" : 0,
									"y" : 70+12,
									
									"text" : uiScriptLocale.GAME_STATISTICS_COMPLETED_DUNGEONS.split("\n")[1],
									
									"horizontal_align" : "center",
									"text_horizontal_align" : "center",
									
									"outline" : True,
									"r" : 1.0, "g" : 1.0, "b" : 1.0, "a" : 0.7, 
								},
								{
									"name" : "pi_text_value_type_6", 
									"type" : "text", 
									
									"fontname" : "Tahoma:14b",
									
									"x" : 0, 
									"y" : 27, 
									
									"text" : "69.000.000", 
									
									"horizontal_align" : "center",
									"text_horizontal_align" : "center",
									
									"r" : 1.0, "g" : 1.0, "b" : 1.0, "a" : 0.7,
								},
								{
									"name" : "pi_text_value_w_type_6", 
									"type" : "text", 
									
									"fontname" : "Tahoma:14b",
									
									"x" : 0, 
									"y" : 27-7, 
									
									"text" : localeInfo.GAME_STATISTICS_PERSONAL_THIS_WEEK.split("\n")[0], 
									
									"horizontal_align" : "center",
									"text_horizontal_align" : "center",
									
									"r" : 1.0, "g" : 1.0, "b" : 1.0, "a" : 0.7,
								},
							),
						},
						{
							"name" : "pi_btn_type_7",
							"type" : "button",
		
							"x" : 226,
							"y" : 1 + 102 + 102 + 102,
		
							"default_image" : ROOT_PATH + "personal/07_normal.png",
							"over_image" : ROOT_PATH + "personal/07_over.png",
							"down_image" : ROOT_PATH + "personal/07_over.png",
							
							"children":
							(
								{
									"name" : "pi_text_name_1_type_7", 
									"type" : "text", 
									
									"x" : 0,
									"y" : 70,
									
									"text" : uiScriptLocale.GAME_STATISTICS_PLAYER_DMG_SKILL.split("\n")[0],
									
									"horizontal_align" : "center",
									"text_horizontal_align" : "center",
									
									"outline" : True,
									"r" : 1.0, "g" : 1.0, "b" : 1.0, "a" : 0.7, 
								},
								{
									"name" : "pi_text_name_2_type_7", 
									"type" : "text", 
									
									"x" : 0,
									"y" : 70+12,
									
									"text" : uiScriptLocale.GAME_STATISTICS_PLAYER_DMG_SKILL.split("\n")[1],
									
									"horizontal_align" : "center",
									"text_horizontal_align" : "center",
									
									"outline" : True,
									"r" : 1.0, "g" : 1.0, "b" : 1.0, "a" : 0.7, 
								},
								{
									"name" : "pi_text_value_type_7", 
									"type" : "text", 
									
									"fontname" : "Tahoma:14b",
									
									"x" : 0, 
									"y" : 27, 
									
									"text" : "69.000.000", 
									
									"horizontal_align" : "center",
									"text_horizontal_align" : "center",
									
									"r" : 1.0, "g" : 1.0, "b" : 1.0, "a" : 0.7,
								},
								{
									"name" : "pi_text_value_w_type_7", 
									"type" : "text", 
									
									"fontname" : "Tahoma:14b",
									
									"x" : 0, 
									"y" : 27-7, 
									
									"text" : localeInfo.GAME_STATISTICS_PERSONAL_THIS_WEEK.split("\n")[0], 
									
									"horizontal_align" : "center",
									"text_horizontal_align" : "center",
									
									"r" : 1.0, "g" : 1.0, "b" : 1.0, "a" : 0.7,
								},
							),
						},
						{
							"name" : "pi_btn_type_8",
							"type" : "button",
		
							"x" : 1,
							"y" : 1 + 102 + 102 + 102 + 102,
		
							"default_image" : ROOT_PATH + "personal/08_normal.png",
							"over_image" : ROOT_PATH + "personal/08_over.png",
							"down_image" : ROOT_PATH + "personal/08_over.png",
							
							"children":
							(
								{
									"name" : "pi_text_name_1_type_8", 
									"type" : "text", 
									
									"x" : 0,
									"y" : 70,
									
									"text" : uiScriptLocale.GAME_STATISTICS_PLAYER_DMG_HIT.split("\n")[0],
									
									"horizontal_align" : "center",
									"text_horizontal_align" : "center",
									
									"outline" : True,
									"r" : 1.0, "g" : 1.0, "b" : 1.0, "a" : 0.7, 
								},
								{
									"name" : "pi_text_name_2_type_8", 
									"type" : "text", 
									
									"x" : 0,
									"y" : 70+12,
									
									"text" : uiScriptLocale.GAME_STATISTICS_PLAYER_DMG_HIT.split("\n")[1],
									
									"horizontal_align" : "center",
									"text_horizontal_align" : "center",
									
									"outline" : True,
									"r" : 1.0, "g" : 1.0, "b" : 1.0, "a" : 0.7, 
								},
								{
									"name" : "pi_text_value_type_8", 
									"type" : "text", 
									
									"fontname" : "Tahoma:14b",
									
									"x" : 0, 
									"y" : 27, 
									
									"text" : "69.000.000", 
									
									"horizontal_align" : "center",
									"text_horizontal_align" : "center",
									
									"r" : 1.0, "g" : 1.0, "b" : 1.0, "a" : 0.7,
								},
								{
									"name" : "pi_text_value_w_type_8", 
									"type" : "text", 
									
									"fontname" : "Tahoma:14b",
									
									"x" : 0, 
									"y" : 27-7, 
									
									"text" : localeInfo.GAME_STATISTICS_PERSONAL_THIS_WEEK.split("\n")[0], 
									
									"horizontal_align" : "center",
									"text_horizontal_align" : "center",
									
									"r" : 1.0, "g" : 1.0, "b" : 1.0, "a" : 0.7,
								},
							),
						},
						{
							"name" : "pi_btn_type_9",
							"type" : "button",
		
							"x" : 226,
							"y" : 1 + 102 + 102 + 102 + 102,
		
							"default_image" : ROOT_PATH + "personal/09_normal.png",
							"over_image" : ROOT_PATH + "personal/09_over.png",
							"down_image" : ROOT_PATH + "personal/09_over.png",
							
							"children":
							(
								{
									"name" : "pi_text_name_1_type_9", 
									"type" : "text", 
									
									"x" : 0,
									"y" : 70,
									
									"text" : uiScriptLocale.GAME_STATISTICS_PLAYER_KILL.split("\n")[0],
									
									"horizontal_align" : "center",
									"text_horizontal_align" : "center",
									
									"outline" : True,
									"r" : 1.0, "g" : 1.0, "b" : 1.0, "a" : 0.7, 
								},
								{
									"name" : "pi_text_name_2_type_9", 
									"type" : "text", 
									
									"x" : 0,
									"y" : 70+12,
									
									"text" : uiScriptLocale.GAME_STATISTICS_PLAYER_KILL.split("\n")[1],
									
									"horizontal_align" : "center",
									"text_horizontal_align" : "center",
									
									"outline" : True,
									"r" : 1.0, "g" : 1.0, "b" : 1.0, "a" : 0.7, 
								},
								{
									"name" : "pi_text_value_type_9", 
									"type" : "text", 
									
									"fontname" : "Tahoma:14b",
									
									"x" : 0, 
									"y" : 27, 
									
									"text" : "69.000.000", 
									
									"horizontal_align" : "center",
									"text_horizontal_align" : "center",
									
									"r" : 1.0, "g" : 1.0, "b" : 1.0, "a" : 0.7,
								},
								{
									"name" : "pi_text_value_w_type_9", 
									"type" : "text", 
									
									"fontname" : "Tahoma:14b",
									
									"x" : 0, 
									"y" : 27-7, 
									
									"text" : localeInfo.GAME_STATISTICS_PERSONAL_THIS_WEEK.split("\n")[0], 
									
									"horizontal_align" : "center",
									"text_horizontal_align" : "center",
									
									"r" : 1.0, "g" : 1.0, "b" : 1.0, "a" : 0.7,
								},
							),
						},
						{
							"name" : "pi_btn_type_10",
							"type" : "button",
		
							"x" : 1,
							"y" : 1 + 102 + 102 + 102 + 102 + 102,
		
							"default_image" : ROOT_PATH + "personal/10_normal.png",
							"over_image" : ROOT_PATH + "personal/10_over.png",
							"down_image" : ROOT_PATH + "personal/10_over.png",
							
							"children":
							(
								{
									"name" : "pi_text_name_1_type_10", 
									"type" : "text", 
									
									"x" : 0,
									"y" : 70,
									
									"text" : uiScriptLocale.GAME_STATISTICS_PLAYER_DUELS.split("\n")[0],
									
									"horizontal_align" : "center",
									"text_horizontal_align" : "center",
									
									"outline" : True,
									"r" : 1.0, "g" : 1.0, "b" : 1.0, "a" : 0.7, 
								},
								{
									"name" : "pi_text_name_2_type_10", 
									"type" : "text", 
									
									"x" : 0,
									"y" : 70+12,
									
									"text" : uiScriptLocale.GAME_STATISTICS_PLAYER_DUELS.split("\n")[1],
									
									"horizontal_align" : "center",
									"text_horizontal_align" : "center",
									
									"outline" : True,
									"r" : 1.0, "g" : 1.0, "b" : 1.0, "a" : 0.7, 
								},
								{
									"name" : "pi_text_value_type_10", 
									"type" : "text", 
									
									"fontname" : "Tahoma:14b",
									
									"x" : 0, 
									"y" : 27, 
									
									"text" : "69.000.000", 
									
									"horizontal_align" : "center",
									"text_horizontal_align" : "center",
									
									"r" : 1.0, "g" : 1.0, "b" : 1.0, "a" : 0.7,
								},
								{
									"name" : "pi_text_value_w_type_10", 
									"type" : "text", 
									
									"fontname" : "Tahoma:14b",
									
									"x" : 0, 
									"y" : 27-7, 
									
									"text" : localeInfo.GAME_STATISTICS_PERSONAL_THIS_WEEK.split("\n")[0], 
									
									"horizontal_align" : "center",
									"text_horizontal_align" : "center",
									
									"r" : 1.0, "g" : 1.0, "b" : 1.0, "a" : 0.7,
								},
							),
						},
						{
							"name" : "pi_btn_type_11",
							"type" : "button",
		
							"x" : 226,
							"y" : 1 + 102 + 102 + 102 + 102 + 102,
		
							"default_image" : ROOT_PATH + "personal/11_normal.png",
							"over_image" : ROOT_PATH + "personal/11_over.png",
							"down_image" : ROOT_PATH + "personal/11_over.png",
							
							"children":
							(
								{
									"name" : "pi_text_name_1_type_11", 
									"type" : "text", 
									
									"x" : 0,
									"y" : 70,
									
									"text" : uiScriptLocale.GAME_STATISTICS_PLAYER_KILLED.split("\n")[0],
									
									"horizontal_align" : "center",
									"text_horizontal_align" : "center",
									
									"outline" : True,
									"r" : 1.0, "g" : 1.0, "b" : 1.0, "a" : 0.7, 
								},
								{
									"name" : "pi_text_name_2_type_11", 
									"type" : "text", 
									
									"x" : 0,
									"y" : 70+12,
									
									"text" : uiScriptLocale.GAME_STATISTICS_PLAYER_KILLED.split("\n")[1],
									
									"horizontal_align" : "center",
									"text_horizontal_align" : "center",
									
									"outline" : True,
									"r" : 1.0, "g" : 1.0, "b" : 1.0, "a" : 0.7, 
								},
								{
									"name" : "pi_text_value_type_11", 
									"type" : "text", 
									
									"fontname" : "Tahoma:14b",
									
									"x" : 0, 
									"y" : 27, 
									
									"text" : "69.000.000", 
									
									"horizontal_align" : "center",
									"text_horizontal_align" : "center",
									
									"r" : 1.0, "g" : 1.0, "b" : 1.0, "a" : 0.7,
								},
								{
									"name" : "pi_text_value_w_type_11", 
									"type" : "text", 
									
									"fontname" : "Tahoma:14b",
									
									"x" : 0, 
									"y" : 27-7, 
									
									"text" : localeInfo.GAME_STATISTICS_PERSONAL_THIS_WEEK.split("\n")[0], 
									
									"horizontal_align" : "center",
									"text_horizontal_align" : "center",
									
									"r" : 1.0, "g" : 1.0, "b" : 1.0, "a" : 0.7,
								},
							),
						},
					),
				},
				
				{
					"name" : "RankingPage",
					"type" : "window",
		
					"x" : 0,
					"y" : 0,
		
					"width" : WINDOW_WIDTH - 30,
					"height" : 315,
		
					"children":
					(
						{
							"name" : "ScrollBarWindow", 
							"type" : "window", 
							
							"x" : 225,
							"y" : 35,
							
							"width" : 16,
							"height" : 270,
						},
					
						{
							"name" : "PvmText", 
							"type" : "text", 
							
							"x" : 20,
							"y" : 8,
							
							"text" : uiScriptLocale.GAME_STATISTICS_PVM_TEXT, 
						},
						{
							"name" : "PvmSeparator", 
							"type" : "image", 
							
							"x" : 5,
							"y" : 23,
							
							"image" : ROOT_PATH + "ranking_type_separator.png",
						},
						{
							"name" : "PvpText", 
							"type" : "text", 
							
							"x" : 20,
							"y" : 8,
							
							"text" : uiScriptLocale.GAME_STATISTICS_PVP_TEXT, 
							
							"horizontal_align" : "right",
							"text_horizontal_align" : "right",
						},
						{
							"name" : "PvpSeparator", 
							"type" : "image", 
							
							"x" : 5 + 110,
							"y" : 23,
							
							"image" : ROOT_PATH + "ranking_type_separator.png",
							
							"horizontal_align" : "right",
						},
						
						{
							"name" : "ranking_btn_type_0",
							"type" : "button",
		
							"x" : 8,
							"y" : 35,
		
							"default_image" : ROOT_PATH + "category_btn_01.png",
							"over_image" : ROOT_PATH + "category_btn_02.png",
							"down_image" : ROOT_PATH + "category_btn_03.png",
							
							"text" : uiScriptLocale.GAME_STATISTICS_RANKING_BTN_0,
							"text_align_left" : True,
							"text_height" : 4,
							"text_x_left" : 48,
							"text_y_left" : 21,
							
							"children":
							(
								{
									"name" : "ranking_icon_type_0", 
									"type" : "image",
									"style" : ("not_pick",),
									
									"x" : 4,
									"y" : 3,
									
									"image" : ROOT_PATH + "icon/type_00.png", 
								},
							),
						},
						
						{
							"name" : "ranking_btn_type_1",
							"type" : "button",
		
							"x" : 8,
							"y" : 35 + (1 * 46),
		
							"default_image" : ROOT_PATH + "category_btn_01.png",
							"over_image" : ROOT_PATH + "category_btn_02.png",
							"down_image" : ROOT_PATH + "category_btn_03.png",
							
							"text" : uiScriptLocale.GAME_STATISTICS_RANKING_BTN_1,
							"text_align_left" : True,
							"text_height" : 4,
							"text_x_left" : 48,
							"text_y_left" : 21,
							
							"children":
							(
								{
									"name" : "ranking_icon_type_1", 
									"type" : "image",
									"style" : ("not_pick",),
									
									"x" : 4,
									"y" : 3,
									
									"image" : ROOT_PATH + "icon/type_01.png", 
								},
							),
						},
						
						{
							"name" : "ranking_btn_type_2",
							"type" : "button",
		
							"x" : 8,
							"y" : 35 + (2 * 46),
		
							"default_image" : ROOT_PATH + "category_btn_01.png",
							"over_image" : ROOT_PATH + "category_btn_02.png",
							"down_image" : ROOT_PATH + "category_btn_03.png",
							
							"text" : uiScriptLocale.GAME_STATISTICS_RANKING_BTN_2,
							"text_align_left" : True,
							"text_height" : 4,
							"text_x_left" : 48,
							"text_y_left" : 21,
							
							"children":
							(
								{
									"name" : "ranking_icon_type_2", 
									"type" : "image",
									"style" : ("not_pick",),
									
									"x" : 4,
									"y" : 3,
									
									"image" : ROOT_PATH + "icon/type_02.png", 
								},
							),
						},
						
						{
							"name" : "ranking_btn_type_3",
							"type" : "button",
		
							"x" : 8,
							"y" : 35 + (3 * 46),
		
							"default_image" : ROOT_PATH + "category_btn_01.png",
							"over_image" : ROOT_PATH + "category_btn_02.png",
							"down_image" : ROOT_PATH + "category_btn_03.png",
							
							"text" : uiScriptLocale.GAME_STATISTICS_RANKING_BTN_3,
							"text_align_left" : True,
							"text_height" : 4,
							"text_x_left" : 48,
							"text_y_left" : 21,
							
							"children":
							(
								{
									"name" : "ranking_icon_type_3", 
									"type" : "image",
									"style" : ("not_pick",),
									
									"x" : 4,
									"y" : 3,
									
									"image" : ROOT_PATH + "icon/type_03.png", 
								},
							),
						},
						
						{
							"name" : "ranking_btn_type_4",
							"type" : "button",
		
							"x" : 8,
							"y" : 35 + (4 * 46),
		
							"default_image" : ROOT_PATH + "category_btn_01.png",
							"over_image" : ROOT_PATH + "category_btn_02.png",
							"down_image" : ROOT_PATH + "category_btn_03.png",
							
							"text" : uiScriptLocale.GAME_STATISTICS_RANKING_BTN_4,
							"text_align_left" : True,
							"text_height" : 4,
							"text_x_left" : 48,
							"text_y_left" : 21,
							
							"children":
							(
								{
									"name" : "ranking_icon_type_4", 
									"type" : "image",
									"style" : ("not_pick",),
									
									"x" : 4,
									"y" : 3,
									
									"image" : ROOT_PATH + "icon/type_04.png", 
								},
							),
						},
						
						{
							"name" : "ranking_btn_type_5",
							"type" : "button",
		
							"x" : 8,
							"y" : 35 + (5 * 46),
		
							"default_image" : ROOT_PATH + "category_btn_01.png",
							"over_image" : ROOT_PATH + "category_btn_02.png",
							"down_image" : ROOT_PATH + "category_btn_03.png",
							
							"text" : uiScriptLocale.GAME_STATISTICS_RANKING_BTN_5,
							"text_align_left" : True,
							"text_height" : 4,
							"text_x_left" : 48,
							"text_y_left" : 21,
							
							"children":
							(
								{
									"name" : "ranking_icon_type_5", 
									"type" : "image",
									"style" : ("not_pick",),
									
									"x" : 4,
									"y" : 3,
									
									"image" : ROOT_PATH + "icon/type_05.png", 
								},
							),
						},
						
						{
							"name" : "ranking_btn_type_6",
							"type" : "button",
		
							"x" : 8,
							"y" : 35 + (6 * 46),
		
							"default_image" : ROOT_PATH + "category_btn_01.png",
							"over_image" : ROOT_PATH + "category_btn_02.png",
							"down_image" : ROOT_PATH + "category_btn_03.png",
							
							"text" : uiScriptLocale.GAME_STATISTICS_RANKING_BTN_6,
							"text_align_left" : True,
							"text_height" : 4,
							"text_x_left" : 48,
							"text_y_left" : 21,
							
							"children":
							(
								{
									"name" : "ranking_icon_type_6", 
									"type" : "image",
									"style" : ("not_pick",),
									
									"x" : 4,
									"y" : 3,
									
									"image" : ROOT_PATH + "icon/type_06.png", 
								},
							),
						},
						
						{
							"name" : "ranking_btn_type_7",
							"type" : "button",
		
							"x" : 252,
							"y" : 35 + (0 * 46),
		
							"default_image" : ROOT_PATH + "category_btn_01.png",
							"over_image" : ROOT_PATH + "category_btn_02.png",
							"down_image" : ROOT_PATH + "category_btn_03.png",
							
							"text" : uiScriptLocale.GAME_STATISTICS_RANKING_BTN_7,
							"text_align_left" : True,
							"text_height" : 4,
							"text_x_left" : 48,
							"text_y_left" : 21,
							
							"children":
							(
								{
									"name" : "ranking_icon_type_7", 
									"type" : "image",
									"style" : ("not_pick",),
									
									"x" : 4,
									"y" : 3,
									
									"image" : ROOT_PATH + "icon/type_07.png", 
								},
							),
						},
						
						{
							"name" : "ranking_btn_type_8",
							"type" : "button",
		
							"x" : 252,
							"y" : 35 + (1 * 46),
		
							"default_image" : ROOT_PATH + "category_btn_01.png",
							"over_image" : ROOT_PATH + "category_btn_02.png",
							"down_image" : ROOT_PATH + "category_btn_03.png",
							
							"text" : uiScriptLocale.GAME_STATISTICS_RANKING_BTN_8,
							"text_align_left" : True,
							"text_height" : 4,
							"text_x_left" : 48,
							"text_y_left" : 21,
							
							"children":
							(
								{
									"name" : "ranking_icon_type_8", 
									"type" : "image",
									"style" : ("not_pick",),
									
									"x" : 4,
									"y" : 3,
									
									"image" : ROOT_PATH + "icon/type_08.png", 
								},
							),
						},
						
						{
							"name" : "ranking_btn_type_9",
							"type" : "button",
		
							"x" : 252,
							"y" : 35 + (2 * 46),
		
							"default_image" : ROOT_PATH + "category_btn_01.png",
							"over_image" : ROOT_PATH + "category_btn_02.png",
							"down_image" : ROOT_PATH + "category_btn_03.png",
							
							"text" : uiScriptLocale.GAME_STATISTICS_RANKING_BTN_9,
							"text_align_left" : True,
							"text_height" : 4,
							"text_x_left" : 48,
							"text_y_left" : 21,
							
							"children":
							(
								{
									"name" : "ranking_icon_type_9", 
									"type" : "image",
									"style" : ("not_pick",),
									
									"x" : 4,
									"y" : 3,
									
									"image" : ROOT_PATH + "icon/type_09.png", 
								},
							),
						},
						
						{
							"name" : "ranking_btn_type_10",
							"type" : "button",
		
							"x" : 252,
							"y" : 35 + (3 * 46),
		
							"default_image" : ROOT_PATH + "category_btn_01.png",
							"over_image" : ROOT_PATH + "category_btn_02.png",
							"down_image" : ROOT_PATH + "category_btn_03.png",
							
							"text" : uiScriptLocale.GAME_STATISTICS_RANKING_BTN_10,
							"text_align_left" : True,
							"text_height" : 4,
							"text_x_left" : 48,
							"text_y_left" : 21,
							
							"children":
							(
								{
									"name" : "ranking_icon_type_10", 
									"type" : "image",
									"style" : ("not_pick",),
									
									"x" : 4,
									"y" : 3,
									
									"image" : ROOT_PATH + "icon/type_10.png", 
								},
							),
						},
						
						{
							"name" : "ranking_btn_type_11",
							"type" : "button",
		
							"x" : 252,
							"y" : 35 + (4 * 46),
		
							"default_image" : ROOT_PATH + "category_btn_01.png",
							"over_image" : ROOT_PATH + "category_btn_02.png",
							"down_image" : ROOT_PATH + "category_btn_03.png",
							
							"text" : uiScriptLocale.GAME_STATISTICS_RANKING_BTN_11,
							"text_align_left" : True,
							"text_height" : 4,
							"text_x_left" : 48,
							"text_y_left" : 21,
							
							"children":
							(
								{
									"name" : "ranking_icon_type_11", 
									"type" : "image",
									"style" : ("not_pick",),
									
									"x" : 4,
									"y" : 3,
									
									"image" : ROOT_PATH + "icon/type_11.png", 
								},
							),
						},
						
						{
							"name" : "ranking_btn_type_12",
							"type" : "button",
		
							"x" : 252,
							"y" : 35 + (5 * 46),
		
							"default_image" : ROOT_PATH + "category_btn_01.png",
							"over_image" : ROOT_PATH + "category_btn_02.png",
							"down_image" : ROOT_PATH + "category_btn_03.png",
							
							"text" : uiScriptLocale.GAME_STATISTICS_RANKING_BTN_12,
							"text_align_left" : True,
							"text_height" : 4,
							"text_x_left" : 48,
							"text_y_left" : 21,
							
							"children":
							(
								{
									"name" : "ranking_icon_type_12", 
									"type" : "image",
									"style" : ("not_pick",),
									
									"x" : 4,
									"y" : 3,
									
									"image" : ROOT_PATH + "icon/type_12.png", 
								},
							),
						},
					),
				},
				
				{
					"name" : "RankingOpenPage",
					"type" : "window",
		
					"x" : 0,
					"y" : 0,
		
					"width" : WINDOW_WIDTH - 30,
					"height" : 315,
		
					"children":
					(
						{
							"name" : "TopBar", 
							"type" : "image", 
							
							"x" : 3,
							"y" : 3,
							
							"image" : ROOT_PATH + "top_bar.png",
							
							"children":
							(
								{
									"name" : "TopBarPosText", 
									"type" : "text",

									"x" : 20,
									"y" : 2,
									
									"text" : "#", 
								},
								{
									"name" : "TopBarNameText", 
									"type" : "text",

									"x" : 112,
									"y" : 2,
									
									"text" : uiScriptLocale.GAME_STATISTICS_RANKING_NAME, 
								},
								{
									"name" : "TopBarLevelText", 
									"type" : "text",

									"x" : 243,
									"y" : 2,
									
									"text" : uiScriptLocale.GAME_STATISTICS_RANKING_LEVEL, 
								},
								{
									"name" : "TopBarValueText", 
									"type" : "text",

									"x" : 365,
									"y" : 2,
									
									"text" : uiScriptLocale.GAME_STATISTICS_RANKING_VALUE, 
								},
							),
						},
						
						{
							"name" : "ranking_item_0",
							"type" : "image",
		
							"x" : 3,
							"y" : 25 + (0 * 26),
		
							"image" : ROOT_PATH + "ranking_item.png",

							"children":
							(
								{ "name" : "ranking_item_0_pos", "type" : "image", "x" : 12, "y" : 3, "image" : ROOT_PATH + "ranking_pos_1.png", },
								{ "name" : "ranking_item_0_name", "type" : "text", "x" : 125, "y" : 5, "text" : "", "text_horizontal_align" : "center", "r" : 1.0, "g" : 1.0, "b" : 1.0, "a" : 0.7, },
								{ "name" : "ranking_item_0_level", "type" : "text", "x" : 255, "y" : 5, "text" : "", "text_horizontal_align" : "center", "r" : 1.0, "g" : 1.0, "b" : 1.0, "a" : 0.7, },
								{ "name" : "ranking_item_0_value", "type" : "text", "x" : 375, "y" : 5, "text" : "", "text_horizontal_align" : "center", "r" : 1.0, "g" : 1.0, "b" : 1.0, "a" : 0.7, },
							),
						},
						
						{
							"name" : "ranking_item_1",
							"type" : "image",
		
							"x" : 3,
							"y" : 25 + (1 * 26),
		
							"image" : ROOT_PATH + "ranking_item.png",

							"children":
							(
								{ "name" : "ranking_item_1_pos", "type" : "image", "x" : 10, "y" : 3, "image" : ROOT_PATH + "ranking_pos_2.png", },
								{ "name" : "ranking_item_1_name", "type" : "text", "x" : 125, "y" : 5, "text" : "", "text_horizontal_align" : "center", "r" : 1.0, "g" : 1.0, "b" : 1.0, "a" : 0.7, },
								{ "name" : "ranking_item_1_level", "type" : "text", "x" : 255, "y" : 5, "text" : "", "text_horizontal_align" : "center", "r" : 1.0, "g" : 1.0, "b" : 1.0, "a" : 0.7, },
								{ "name" : "ranking_item_1_value", "type" : "text", "x" : 375, "y" : 5, "text" : "", "text_horizontal_align" : "center", "r" : 1.0, "g" : 1.0, "b" : 1.0, "a" : 0.7, },
							),
						},
						
						{
							"name" : "ranking_item_2",
							"type" : "image",
		
							"x" : 3,
							"y" : 25 + (2 * 26),
		
							"image" : ROOT_PATH + "ranking_item.png",

							"children":
							(
								{ "name" : "ranking_item_2_pos", "type" : "image", "x" : 10, "y" : 3, "image" : ROOT_PATH + "ranking_pos_3.png", },
								{ "name" : "ranking_item_2_name", "type" : "text", "x" : 125, "y" : 5, "text" : "", "text_horizontal_align" : "center", "r" : 1.0, "g" : 1.0, "b" : 1.0, "a" : 0.7, },
								{ "name" : "ranking_item_2_level", "type" : "text", "x" : 255, "y" : 5, "text" : "", "text_horizontal_align" : "center", "r" : 1.0, "g" : 1.0, "b" : 1.0, "a" : 0.7, },
								{ "name" : "ranking_item_2_value", "type" : "text", "x" : 375, "y" : 5, "text" : "", "text_horizontal_align" : "center", "r" : 1.0, "g" : 1.0, "b" : 1.0, "a" : 0.7, },
							),
						},
						
						{
							"name" : "ranking_item_3",
							"type" : "image",
		
							"x" : 3,
							"y" : 25 + (3 * 26),
		
							"image" : ROOT_PATH + "ranking_item.png",

							"children":
							(
								{ "name" : "ranking_item_3_pos", "type" : "text", "x" : 24, "y" : 5, "text" : "4", "fontname" : "Tahoma:14b", "text_horizontal_align" : "center", "r" : 1.0, "g" : 1.0, "b" : 1.0, "a" : 0.7, },
								{ "name" : "ranking_item_3_name", "type" : "text", "x" : 125, "y" : 5, "text" : "", "text_horizontal_align" : "center", "r" : 1.0, "g" : 1.0, "b" : 1.0, "a" : 0.7, },
								{ "name" : "ranking_item_3_level", "type" : "text", "x" : 255, "y" : 5, "text" : "", "text_horizontal_align" : "center", "r" : 1.0, "g" : 1.0, "b" : 1.0, "a" : 0.7, },
								{ "name" : "ranking_item_3_value", "type" : "text", "x" : 375, "y" : 5, "text" : "", "text_horizontal_align" : "center", "r" : 1.0, "g" : 1.0, "b" : 1.0, "a" : 0.7, },
							),
						},
						
						{
							"name" : "ranking_item_4",
							"type" : "image",
		
							"x" : 3,
							"y" : 25 + (4 * 26),
		
							"image" : ROOT_PATH + "ranking_item.png",

							"children":
							(
								{ "name" : "ranking_item_4_pos", "type" : "text", "x" : 24, "y" : 5, "text" : "5", "fontname" : "Tahoma:14b", "text_horizontal_align" : "center", "r" : 1.0, "g" : 1.0, "b" : 1.0, "a" : 0.7, },
								{ "name" : "ranking_item_4_name", "type" : "text", "x" : 125, "y" : 5, "text" : "", "text_horizontal_align" : "center", "r" : 1.0, "g" : 1.0, "b" : 1.0, "a" : 0.7, },
								{ "name" : "ranking_item_4_level", "type" : "text", "x" : 255, "y" : 5, "text" : "", "text_horizontal_align" : "center", "r" : 1.0, "g" : 1.0, "b" : 1.0, "a" : 0.7, },
								{ "name" : "ranking_item_4_value", "type" : "text", "x" : 375, "y" : 5, "text" : "", "text_horizontal_align" : "center", "r" : 1.0, "g" : 1.0, "b" : 1.0, "a" : 0.7, },
							),
						},
						
						{
							"name" : "ranking_item_5",
							"type" : "image",
		
							"x" : 3,
							"y" : 25 + (5 * 26),
		
							"image" : ROOT_PATH + "ranking_item.png",

							"children":
							(
								{ "name" : "ranking_item_5_pos", "type" : "text", "x" : 24, "y" : 5, "text" : "6", "fontname" : "Tahoma:14b", "text_horizontal_align" : "center", "r" : 1.0, "g" : 1.0, "b" : 1.0, "a" : 0.7, },
								{ "name" : "ranking_item_5_name", "type" : "text", "x" : 125, "y" : 5, "text" : "", "text_horizontal_align" : "center", "r" : 1.0, "g" : 1.0, "b" : 1.0, "a" : 0.7, },
								{ "name" : "ranking_item_5_level", "type" : "text", "x" : 255, "y" : 5, "text" : "", "text_horizontal_align" : "center", "r" : 1.0, "g" : 1.0, "b" : 1.0, "a" : 0.7, },
								{ "name" : "ranking_item_5_value", "type" : "text", "x" : 375, "y" : 5, "text" : "", "text_horizontal_align" : "center", "r" : 1.0, "g" : 1.0, "b" : 1.0, "a" : 0.7, },
							),
						},
						
						{
							"name" : "ranking_item_6",
							"type" : "image",
		
							"x" : 3,
							"y" : 25 + (6 * 26),
		
							"image" : ROOT_PATH + "ranking_item.png",

							"children":
							(
								{ "name" : "ranking_item_6_pos", "type" : "text", "x" : 24, "y" : 5, "text" : "7", "fontname" : "Tahoma:14b", "text_horizontal_align" : "center", "r" : 1.0, "g" : 1.0, "b" : 1.0, "a" : 0.7, },
								{ "name" : "ranking_item_6_name", "type" : "text", "x" : 125, "y" : 5, "text" : "", "text_horizontal_align" : "center", "r" : 1.0, "g" : 1.0, "b" : 1.0, "a" : 0.7, },
								{ "name" : "ranking_item_6_level", "type" : "text", "x" : 255, "y" : 5, "text" : "", "text_horizontal_align" : "center", "r" : 1.0, "g" : 1.0, "b" : 1.0, "a" : 0.7, },
								{ "name" : "ranking_item_6_value", "type" : "text", "x" : 375, "y" : 5, "text" : "", "text_horizontal_align" : "center", "r" : 1.0, "g" : 1.0, "b" : 1.0, "a" : 0.7, },
							),
						},
						
						{
							"name" : "ranking_item_7",
							"type" : "image",
		
							"x" : 3,
							"y" : 25 + (7 * 26),
		
							"image" : ROOT_PATH + "ranking_item.png",

							"children":
							(
								{ "name" : "ranking_item_7_pos", "type" : "text", "x" : 24, "y" : 5, "text" : "8", "fontname" : "Tahoma:14b", "text_horizontal_align" : "center", "r" : 1.0, "g" : 1.0, "b" : 1.0, "a" : 0.7, },
								{ "name" : "ranking_item_7_name", "type" : "text", "x" : 125, "y" : 5, "text" : "", "text_horizontal_align" : "center", "r" : 1.0, "g" : 1.0, "b" : 1.0, "a" : 0.7, },
								{ "name" : "ranking_item_7_level", "type" : "text", "x" : 255, "y" : 5, "text" : "", "text_horizontal_align" : "center", "r" : 1.0, "g" : 1.0, "b" : 1.0, "a" : 0.7, },
								{ "name" : "ranking_item_7_value", "type" : "text", "x" : 375, "y" : 5, "text" : "", "text_horizontal_align" : "center", "r" : 1.0, "g" : 1.0, "b" : 1.0, "a" : 0.7, },
							),
						},
						
						{
							"name" : "ranking_item_8",
							"type" : "image",
		
							"x" : 3,
							"y" : 25 + (8 * 26),
		
							"image" : ROOT_PATH + "ranking_item.png",

							"children":
							(
								{ "name" : "ranking_item_8_pos", "type" : "text", "x" : 24, "y" : 5, "text" : "9", "fontname" : "Tahoma:14b", "text_horizontal_align" : "center", "r" : 1.0, "g" : 1.0, "b" : 1.0, "a" : 0.7, },
								{ "name" : "ranking_item_8_name", "type" : "text", "x" : 125, "y" : 5, "text" : "", "text_horizontal_align" : "center", "r" : 1.0, "g" : 1.0, "b" : 1.0, "a" : 0.7, },
								{ "name" : "ranking_item_8_level", "type" : "text", "x" : 255, "y" : 5, "text" : "", "text_horizontal_align" : "center", "r" : 1.0, "g" : 1.0, "b" : 1.0, "a" : 0.7, },
								{ "name" : "ranking_item_8_value", "type" : "text", "x" : 375, "y" : 5, "text" : "", "text_horizontal_align" : "center", "r" : 1.0, "g" : 1.0, "b" : 1.0, "a" : 0.7, },
							),
						},
						
						{
							"name" : "ranking_item_9",
							"type" : "image",
		
							"x" : 3,
							"y" : 25 + (9 * 26),
		
							"image" : ROOT_PATH + "ranking_item.png",

							"children":
							(
								{ "name" : "ranking_item_9_pos", "type" : "text", "x" : 24, "y" : 5, "text" : "10", "fontname" : "Tahoma:14b", "text_horizontal_align" : "center", "r" : 1.0, "g" : 1.0, "b" : 1.0, "a" : 0.7, },
								{ "name" : "ranking_item_9_name", "type" : "text", "x" : 125, "y" : 5, "text" : "", "text_horizontal_align" : "center", "r" : 1.0, "g" : 1.0, "b" : 1.0, "a" : 0.7, },
								{ "name" : "ranking_item_9_level", "type" : "text", "x" : 255, "y" : 5, "text" : "", "text_horizontal_align" : "center", "r" : 1.0, "g" : 1.0, "b" : 1.0, "a" : 0.7, },
								{ "name" : "ranking_item_9_value", "type" : "text", "x" : 375, "y" : 5, "text" : "", "text_horizontal_align" : "center", "r" : 1.0, "g" : 1.0, "b" : 1.0, "a" : 0.7, },
							),
						},
						
						{
							"name" : "ranking_item_10",
							"type" : "image",
		
							"x" : 3,
							"y" : 25 + (10 * 26),
		
							"image" : ROOT_PATH + "ranking_item_personal.png",

							"children":
							(
								{ "name" : "ranking_item_10_pos", "type" : "text", "x" : 24, "y" : 5, "text" : "-", "fontname" : "Tahoma:14b", "text_horizontal_align" : "center", "r" : 1.0, "g" : 1.0, "b" : 1.0, "a" : 0.7, },
								{ "name" : "ranking_item_10_name", "type" : "text", "x" : 125, "y" : 5, "text" : "", "text_horizontal_align" : "center", "r" : 1.0, "g" : 1.0, "b" : 1.0, "a" : 0.7, },
								{ "name" : "ranking_item_10_level", "type" : "text", "x" : 255, "y" : 5, "text" : "", "text_horizontal_align" : "center", "r" : 1.0, "g" : 1.0, "b" : 1.0, "a" : 0.7, },
								{ "name" : "ranking_item_10_value", "type" : "text", "x" : 375, "y" : 5, "text" : "", "text_horizontal_align" : "center", "r" : 1.0, "g" : 1.0, "b" : 1.0, "a" : 0.7, },
							),
						},
					),
				},
				
				{
					"name" : "LoadingOverlay",
					"type" : "bar",
		
					"x" : 2,
					"y" : 2,
		
					"width" : WINDOW_WIDTH - 30 - 4,
					"height" : 315 - 4,
					
					"color" : 0x4C000000,
		
					"children":
					(
						{
							"name" : "LoadingAnimation",
							"type" : "ani_image",
		
							"x" : 0,
							"y" : 0,
							
							"width" : 100,
							"height" : 100,
							
							"horizontal_align" : "center",
							"vertical_align" : "center",

							"delay" : 4,
							
							"images" :
							(
								ROOT_PATH + "loading/1.png",
								ROOT_PATH + "loading/2.png",
								ROOT_PATH + "loading/3.png",
								ROOT_PATH + "loading/4.png",
								ROOT_PATH + "loading/5.png",
								ROOT_PATH + "loading/6.png",
								ROOT_PATH + "loading/7.png",
								ROOT_PATH + "loading/8.png",
								ROOT_PATH + "loading/9.png",
								ROOT_PATH + "loading/10.png",
								ROOT_PATH + "loading/11.png",
								ROOT_PATH + "loading/12.png",
								ROOT_PATH + "loading/13.png",
								ROOT_PATH + "loading/14.png",
								ROOT_PATH + "loading/15.png",
								ROOT_PATH + "loading/16.png",
							),
						},
					),
				},
			),
		},
	),	
}
