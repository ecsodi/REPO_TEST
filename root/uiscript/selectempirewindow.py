import uiScriptLocale

ROOT_PATH = "d:/ymir work/ui/public/"
LOCALE_PATH = uiScriptLocale.EMPIRE_PATH
ROOT_PATH_NEW = "d:/ymir work/ui/game/select_interface/"

ATALS_X = SCREEN_WIDTH * (282) / 800
ATALS_Y = SCREEN_HEIGHT * (170) / 600

window = {
	"name" : "SelectCharacterWindow",

	"x" : 0,
	"y" : 0,

	"width" : SCREEN_WIDTH,
	"height" : SCREEN_HEIGHT,

	"children" :
	(
		## Board
		{
			"name" : "Background", "type" : "expanded_image", "x" : 0, "y" : 0, "x_scale" : float(SCREEN_WIDTH) / 1920.0, "y_scale" : float(SCREEN_HEIGHT) / 1080.0,
			"image" : ROOT_PATH_NEW + "background.png",
		},

		## Title
		{
			"name" : "Title",
			"type" : "expanded_image",

			"x" : SCREEN_WIDTH * (410 - 346/2) / 800,
			"y" : SCREEN_HEIGHT * (114 - 136/2) / 600,
			"x_scale" : float(SCREEN_WIDTH) / 800.0,
			"y_scale" : float(SCREEN_HEIGHT) / 600.0,

			"image" : LOCALE_PATH+"title.sub"
		},

		## Atlas
		{
			"name" : "Atlas",
			"type" : "image",

			"x" : ATALS_X,
			"y" : ATALS_Y,

			"image" : "d:/ymir work/ui/intro/empire/atlas.sub",

			"children" :
			(
				## Empire Image
				{
					"name" : "EmpireArea_A",
					"type" : "expanded_image",

					"x" : 43,
					"y" : 201,

					"image" : "d:/ymir work/ui/intro/empire/empirearea_a.sub"
				},
				{
					"name" : "EmpireArea_B",
					"type" : "expanded_image",

					"x" : 17,
					"y" : 16,

					"image" : "d:/ymir work/ui/intro/empire/empirearea_b.sub"
				},
				{
					"name" : "EmpireArea_C",
					"type" : "expanded_image",

					"x" : 314,
					"y" : 33,

					"image" : "d:/ymir work/ui/intro/empire/empirearea_c.sub"
				},

				## Empire Flag
				{
					"name" : "EmpireAreaFlag_A",
					"type" : "expanded_image",

					"x" : 167,
					"y" : 235,

					"image" : "d:/ymir work/ui/intro/empire/empireareaflag_a.sub"
				},
				{
					"name" : "EmpireAreaFlag_B",
					"type" : "expanded_image",

					"x" : 70,
					"y" : 42,

					"image" : "d:/ymir work/ui/intro/empire/empireareaflag_b.sub"
				},
				{
					"name" : "EmpireAreaFlag_C",
					"type" : "expanded_image",

					"x" : 357,
					"y" : 78,

					"image" : "d:/ymir work/ui/intro/empire/empireareaflag_c.sub"
				},
			),
		},

		## Buttons
		{
			"name" : "left_button",
			"type" : "button",

			"x" : ATALS_X + 160,
			"y" : ATALS_Y + 340,

			"default_image" : "d:/ymir work/ui/intro/select/left_button_01.sub",
			"over_image" : "d:/ymir work/ui/intro/select/left_button_02.sub",
			"down_image" : "d:/ymir work/ui/intro/select/left_button_03.sub",
		},
		{
			"name" : "right_button",
			"type" : "button",

			"x" : ATALS_X + 160 + 130,
			"y" : ATALS_Y + 340,

			"default_image" : "d:/ymir work/ui/intro/select/right_button_01.sub",
			"over_image" : "d:/ymir work/ui/intro/select/right_button_02.sub",
			"down_image" : "d:/ymir work/ui/intro/select/right_button_03.sub",
		},

		## Character Board
		{
			"name" : "empire_board",
			"type" : "thinboard",

			"x" : SCREEN_WIDTH * (40) / 800,
			"y" : SCREEN_HEIGHT * (211) / 600,

			"width" : 208,
			"height" : 314,

			"children" :
			(
				## Bar
				{
					"name" : "flag_board",
					"type" : "window",

					"x" : 24,
					"y" : 17,
					"width" : 159,
					"height" : 119,

					"children" :
					(
						## Empire Flag
						{
							"name" : "EmpireFlag_A",
							"type" : "expanded_image",

							"x" : 0,
							"y" : 0,
							
							"x_scale" : 1.3,
							"y_scale" : 1.3,
							
							"horizontal_align" : "center",
							"vertical_align" : "center",

							"image" : "d:/ymir work/effect/etc/empire/vermelhos_bandeira.tga"
						},
						{
							"name" : "EmpireFlag_B",
							"type" : "expanded_image",

							"x" : 0,
							"y" : 0,
							
							"x_scale" : 1.3,
							"y_scale" : 1.3,
							
							"horizontal_align" : "center",
							"vertical_align" : "center",

							"image" : "d:/ymir work/effect/etc/empire/amarelos_bandeira.tga"
						},
						{
							"name" : "EmpireFlag_C",
							"type" : "expanded_image",

							"x" : 0,
							"y" : 0,
							
							"x_scale" : 1.3,
							"y_scale" : 1.3,
							
							"horizontal_align" : "center",
							"vertical_align" : "center",

							"image" : "d:/ymir work/effect/etc/empire/azuis_bandeira.tga"
						},
					),

				},
				{
					"name" : "text_board",
					"type" : "bar",

					"x" : 10,
					"y" : 146,

					"width" : 189,
					"height" : 122,

					"children" :
					(
						{
							"name" : "prev_text_button",
							"type" : "button",

							"x" : 95,
							"y" : 95,

							"text" : uiScriptLocale.EMPIRE_PREV,

							"default_image" : ROOT_PATH + "Small_Button_01.sub",
							"over_image" : ROOT_PATH + "Small_Button_02.sub",
							"down_image" : ROOT_PATH + "Small_Button_03.sub",
						},
						{
							"name" : "next_text_button",
							"type" : "button",

							"x" : 140,
							"y" : 95,

							"text" : uiScriptLocale.EMPIRE_NEXT,

							"default_image" : ROOT_PATH + "Small_Button_01.sub",
							"over_image" : ROOT_PATH + "Small_Button_02.sub",
							"down_image" : ROOT_PATH + "Small_Button_03.sub",
						},
						{
							"name" : "right_line",
							"type" : "line",

							"x" : 189-1,
							"y" : -1,

							"width" : 0,
							"height" : 122,

							"color" : 0xffAAA6A1,
						},
						{
							"name" : "bottom_line",
							"type" : "line",

							"x" : 0,
							"y" : 122-1,

							"width" : 189,
							"height" : 0,

							"color" : 0xffAAA6A1,
						},
						{
							"name" : "left_line",
							"type" : "line",

							"x" : 0,
							"y" : 0,

							"width" : 0,
							"height" : 122-1,

							"color" : 0xff2A2521,
						},
						{
							"name" : "top_line",
							"type" : "line",

							"x" : 0,
							"y" : 0,

							"width" : 189,
							"height" : 0,

							"color" : 0xff2A2521,
						},
					),
				},

				## Buttons
				{
					"name" : "select_button",
					"type" : "button",

					"x" : 14,
					"y" : 277,

					"text" : uiScriptLocale.EMPIRE_SELECT,

					"default_image" : ROOT_PATH + "Large_Button_01.sub",
					"over_image" : ROOT_PATH + "Large_Button_02.sub",
					"down_image" : ROOT_PATH + "Large_Button_03.sub",
				},
				{
					"name" : "exit_button",
					"type" : "button",

					"x" : 105,
					"y" : 277,

					"text" : uiScriptLocale.EMPIRE_EXIT,

					"default_image" : ROOT_PATH + "Large_Button_01.sub",
					"over_image" : ROOT_PATH + "Large_Button_02.sub",
					"down_image" : ROOT_PATH + "Large_Button_03.sub",
				},

			),
		},
	),
}
