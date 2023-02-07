import uiScriptLocale
import localeInfo

BOARD_X = 512
BOARD_Y = 305

window = {
	"name" : "RefineDialog",
	"style" : ("movable", "float", "animation",),

	"x" : SCREEN_WIDTH - 700,
	"y" : 70 * 500 / SCREEN_HEIGHT,

	"width" : BOARD_X,
	"height" : BOARD_Y,

	"children" :
	(
		{
			"name" : "Board",
			"type" : "board",
			"style" : ("attach",),

			"x" : 0,
			"y" : 0,

			"width" : BOARD_X,
			"height" : BOARD_Y,

			"children" :
			(
				{
					"name" : "TitleBar",
					"type" : "titlebar",
					"style" : ("attach",),

					"x" : 8,
					"y" : 8,

					"width" : BOARD_X - 15,
					"color" : "red",

					"children" :
					(
						{
							"name" : "TitleName",
							"type" : "text",
							"text" : uiScriptLocale.REFINE_TTILE,
							"horizontal_align" : "center",
							"text_horizontal_align" : "center",
							"x" : 0,
							"y" : 3,
						},
					),
				},
				{
					"name" : "board1",
					"type" : "border_a",
					"style" : ("attach",),
					

					"x" : 7,
					"y" : 32,
					
					"width" : 497,
					"height" : 210,
				},
				{
					"name" : "board2",
					"type" : "border_a",
					"style" : ("attach",),
					
					"x" : 7,
					"y" : 245,
					
					"width" : 497,
					"height" : 53,
				},

				{
					"name" : "Background",
					"type" : "image",
					"style" : ("attach",),

					"x" : 7,
					"y" : 32,
					"image" : "d:/ymir work/ui/game/normal_interface/bg_1.png",
				},
				{
					"name" : "BackgroundDown",
					"type" : "image",
					"style" : ("attach",),

					"x" : 7,
					"y" : 245,
					"image" : "d:/ymir work/ui/game/normal_interface/bg_2.png",
					
					"children" :
					(
						{
							"name" : "Cost",
							"type" : "text",
							"x" : 15,
							"y" : 4,
							"text" : "",
						},
						{
							"name": "SuccessPercentage",
							"type":  "text",
							"x": 15,
							"y": 24,
							"text": "",
						},
						{
							"name" : "AcceptButton",
							"type" : "button",
							"x" : 170,
							"y" : 15,
							"text" : uiScriptLocale.OK,
							"default_image" : "d:/ymir work/ui/game/myshop_deco/select_btn_01.sub",
							"over_image" : "d:/ymir work/ui/game/myshop_deco/select_btn_02.sub",
							"down_image" : "d:/ymir work/ui/game/myshop_deco/select_btn_03.sub",
						},
						{
							"name" : "CancelButton",
							"type" : "button",

							"x" : 330,
							"y" : 15,

							"text" : uiScriptLocale.CANCEL,
							"default_image" : "d:/ymir work/ui/game/myshop_deco/select_btn_01.sub",
							"over_image" : "d:/ymir work/ui/game/myshop_deco/select_btn_02.sub",
							"down_image" : "d:/ymir work/ui/game/myshop_deco/select_btn_03.sub",
						},
					),
				},
			),
		},
	),
}