import uiScriptLocale
ROOT_PATH = "d:/ymir work/ui/game/stats_board/bonus/"
window = {
	"name" : "BonusList",
	"style" : ("movable", "float", "animation",),

	"x" : 0,
	"y" : 0,

	"width": 250,
	"height": 410,

	"children" : (
		{
			"name" : "Bonus_Page",
			"type" : "board_with_titlebar",
			"style" : ("attach",),

			"x" : 0,
			"y" : 0,

			"width" : 250,
			"height" : 410,

			"title" : uiScriptLocale.CHARACTER_BONUS_TITLE,

			"children" :
			(
				
				{
					"name": "BonusBoard",
					"type": "image",

					"x": 10,
					"y": 32 + 7,

					"image": "d:/ymir work/ui/game/stats_board/frame.png",
					"children": (
					
						{
							"name": "bonus_button_01",
							"type": "image",

							"x": 4,
							"y": 32 + 7,

							"image": ROOT_PATH + "title.png",

							"children": (
								{
									"name" : "bonus_button_text_01",
									"type" : "text",

									"x": 7,
									"y": 5,

									"text" : uiScriptLocale.CHARACTER_BONUS_OFFENSIVE,
								},
							),
						},
						{
							"name" : "bonus_list_01",
							"type" : "listboxex",

							"x" : 6,
							"y" : 32 + 29 + 7,

							"width" : 269,
							"height" : 181+60,
						},
						{
							"name" : "bonus_scrollbar_01",
							"type" : "scrollbar",

							"x" : 214,
							"y" : 42,

							"size" : 177+67,

						},
						{
							"name": "bonus_button_02",
							"type": "image",

							"x": 4,
							"y": 66 + 7,

							"image": ROOT_PATH + "title.png",

							"children": (
								{
									"name": "bonus_button_text_02",
									"type": "text",

									"x": 7,
									"y": 5,

									"text": uiScriptLocale.CHARACTER_BONUS_DEFENSIVE,
								},
							),
						},
						{
							"name" : "bonus_list_02",
							"type" : "listboxex",

							"x" : 6,
							"y" : 66 + 29 + 7,

							"width" : 269,
							"height" : 181+60,
						},
						{
							"name" : "bonus_scrollbar_02",
							"type" : "scrollbar",

							"x" : 214,
							"y" : 42,

							"size" : 177+67,

						},

						{
							"name": "bonus_button_03",
							"type": "image",

							"x": 4,
							"y": 100 + 7,

							"image": ROOT_PATH + "title.png",

							"children" : (
								{
									"name": "bonus_button_text_03",
									"type": "text",

									"x": 7,
									"y": 5,

									"text": uiScriptLocale.CHARACTER_BONUS_REST,
								},
							),
						},
						{
							"name" : "bonus_list_03",
							"type" : "listboxex",

							"x" : 6,
							"y" : 100 + 29 + 7,

							"width" : 269,
							"height" : 181+60,
						},
						{
							"name" : "bonus_scrollbar_03",
							"type" : "scrollbar",

							"x" : 214,
							"y" : 42,

							"size" : 177+67,

						},

					),
				},
			),
		},
	),
}