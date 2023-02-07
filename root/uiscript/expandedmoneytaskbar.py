import uiScriptLocale
import app

ROOT = "d:/ymir work/ui/game/"

BOARD_ADD_X = 10
BOARD_ADD_X += 65

BOARD_X = SCREEN_WIDTH - (140 + BOARD_ADD_X)
BOARD_WIDTH = (140 + BOARD_ADD_X)
BOARD_HEIGHT = 40

window = {
	"name" : "ExpandedMoneyTaskbar",
	
	"x" : BOARD_X - 25,
	"y" : SCREEN_HEIGHT - 65,

	"width" : BOARD_WIDTH,
	"height" : BOARD_HEIGHT,

	"style" : ("float","animation",),

	"children" :
	[
		{
			"name" : "ExpanedMoneyTaskBar_Board",
			"type" : "board",

			"x" : 0,
			"y" : 0,

			"width" : BOARD_WIDTH + 20,
			"height" : BOARD_HEIGHT,

			"children" :
			[
				## Print
				# {
					# "name":"Money_Icon",
					# "type":"image",
					
					# "x":18 + BOARD_ADD_X,
					# "y":11,

					# "image":"d:/ymir work/ui/game/windows/money_icon.sub",
				# },
				{
					"name":"Money_Slot",
					"type":"button",

					"x":42 + BOARD_ADD_X - 13,
					"y":10,

					#"horizontal_align":"center",

					"default_image" : "d:/ymir work/ui/public/yang_slot.png",
					"over_image" : "d:/ymir work/ui/public/yang_slot.png",
					"down_image" : "d:/ymir work/ui/public/yang_slot.png",

					"children" :
					(
						{
							"name" : "Money",
							"type" : "text",

							"x" : 5,
							"y" : 1,

							"horizontal_align" : "right",
							"text_horizontal_align" : "right",

							"text" : "9,999,999,999",
						},
					),
				},
				
				{
					"name":"Gaya1_Slot",
					"type":"button",

					"x": -108 + BOARD_ADD_X - 15,
					"y":10,

					"default_image" : "d:/ymir work/ui/public/gaya_slot.png",
					"over_image" : "d:/ymir work/ui/public/gaya_slot.png",
					"down_image" : "d:/ymir work/ui/public/gaya_slot.png",

					"children" :
					(
						{
							"name" : "gaya_blue",
							"type" : "text",

							"x" : 3,
							"y" : 1,

							"horizontal_align" : "right",
							"text_horizontal_align" : "right",

							"text" : "1234567",
						},
					),
				},

				# {
					# "name":"Gaya2_Slot",
					# "type":"button",

					# "x": -185 + BOARD_ADD_X,
					# "y":10,

					# "default_image" : "d:/ymir work/ui/public/gaya_slot.png",
					# "over_image" : "d:/ymir work/ui/public/gaya_slot.png",
					# "down_image" : "d:/ymir work/ui/public/gaya_slot.png",

					# "children" :
					# (
						# {
							# "name" : "gaya_green",
							# "type" : "text",

							# "x" : 3,
							# "y" : 1,

							# "horizontal_align" : "right",
							# "text_horizontal_align" : "right",

							# "text" : "1234567",
						# },
					# ),
				# },
				
				{
					"name":"Money_Icon",
					"type":"image",
					
					"x":25 + BOARD_ADD_X - 15,
					"y":10,

					"image":"d:/ymir work/ui/game/windows/money_icon.sub",
				},
				{
					"name":"Gaya_Leaders_Icon",
					"type":"image",
					
					"x": -51 + BOARD_ADD_X - 15,
					"y":13,

					"image":"d:/ymir work/ui/gemshop/gemshop_gemicon.sub",
				},
				# {
					# "name":"Gaya_Metin_Icon",
					# "type":"image",
					
					# "x": -129 + BOARD_ADD_X,
					# "y":12,

					# "image":"d:/ymir work/ui/public/gaya_coin.png",
				# },

			],
		},
	],
}
