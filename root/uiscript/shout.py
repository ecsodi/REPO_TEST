import uiScriptLocale
import item
import app
import localeInfo

BOARD_WIDTH = 500 
BOARD_HEIGTH = 145

window = {
	"name" : "shout",

	"x" : 0,
	"y" : 0,

	"style" : ("movable", "float", "animation",),

	"width" : BOARD_WIDTH,
	"height" : BOARD_HEIGTH,

	"children" :
	(
		{
			"name" : "board",
			"type" : "board_with_titlebar",

			"x" : 0,
			"y" : 0,
			"width" : 500,
			"height" : BOARD_HEIGTH,
					
			"title" : "Auto-Mesaj",
					
			"children" : 
			(
				{
					"name" : "board_circle",
					"type" : "thinboard_circle",

					"x" : 15,
					"y" : 35,
					"width" : 470,
					"height" : 60,
							
					"children" :
							
					(
						{
							"name" : "infotext",
							"type" : "text",
							"x" : 0,
							"y" : 5,
							"text" : "Scrieti mesajul care urmeaza sa fie trimis",
							'horizontal_align': 'center',
							'text_horizontal_align': 'center',
						},
								
						{
							"name" : "SlotBarr",
							"type" : "slotbar",
							"x" : 10,
							"y" : 25,
							"width" : 450,
							"height" : 20,

							"children" :
							(
								{
									"name" : "CommentValue",
									"type" : "editline",
									"x" : 2,
									"y" : 3,
									"width" : 440,
									"height" : 65,
									"input_limit" : 74,
									"text" : "",
								},
							),
						},
								
					),
				},
						
				{
					"name" : "alttextbutton",
					"type" : "thinboard_circle",

					"x" : 15,
					"y" : 90,
					"width" : 470,
					"height" : 40,
							
					"children" :
							
					(
						{
							"name" : "start",
							"type" : "button",
							"x" : 5,
							"y" : 8,
							"default_image" : "d:/ymir work/ui/game/myshop_deco/select_btn_01.sub",
							"over_image" : "d:/ymir work/ui/game/myshop_deco/select_btn_02.sub",
							"down_image" : "d:/ymir work/ui/game/myshop_deco/select_btn_03.sub",
							"disable_image" : "d:/ymir work/ui/switchbot/btn_big_03.sub",
							"text" : localeInfo.SWITCHBOT_START,
						},	
								
						{
							"name" : "stop",
							"type" : "button",
							"x" : 5+155,
							"y" : 8,
							"default_image" : "d:/ymir work/ui/game/myshop_deco/select_btn_01.sub",
							"over_image" : "d:/ymir work/ui/game/myshop_deco/select_btn_02.sub",
							"down_image" : "d:/ymir work/ui/game/myshop_deco/select_btn_03.sub",
							# "disable_image" : "d:/ymir work/ui/switchbot/btn_big_03.sub",
							"text" : localeInfo.SWITCHBOT_STOP,
						},
								
						{
							"name" : "clear",
							"type" : "button",
							"x" : 5+310,
							"y" : 8,
							"default_image" : "d:/ymir work/ui/game/myshop_deco/select_btn_01.sub",
							"over_image" : "d:/ymir work/ui/game/myshop_deco/select_btn_02.sub",
							"down_image" : "d:/ymir work/ui/game/myshop_deco/select_btn_03.sub",
							"disable_image" : "d:/ymir work/ui/switchbot/btn_big_03.sub",
							"text" : localeInfo.SWITCHBOT_CLEAR_ATTR,
						},					
					),
				},					
			),
		},
	),
}
