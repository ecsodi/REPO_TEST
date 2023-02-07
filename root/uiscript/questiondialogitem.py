import uiScriptLocale
import app

window = {
	"name" : "QuestionDialog",
	"style" : ("movable", "float", "animation",),

	"x" : SCREEN_WIDTH/2 - 125,
	"y" : SCREEN_HEIGHT/2 - 52,

	"width" : 240,
	"height" : 115,
	"children" :
	(
		{
			"name" : "board",
			"type" : "board",

			"x" : 0,
			"y" : 0,

			"width" : 240,
			"height" : 115,

			"children" :
			(
				{
					"name" : "message",
					"type" : "text",

					"x" : -15,
					"y" : 45,

					"horizontal_align" : "center",
					"text" : uiScriptLocale.MESSAGE,

					"text_horizontal_align" : "center",
					"text_vertical_align" : "center",
				},
				{
					"name" : "accept",
					"type" : "button",

					"x" : -60,
					"y" : 62,

					"text" : uiScriptLocale.ASK_DROP_TEXT,

					"default_image" : "d:/ymir work/ui/switchbot/btn_small_01.sub",
					"over_image" : "d:/ymir work/ui/switchbot/btn_small_02.sub",
					"down_image" : "d:/ymir work/ui/switchbot/btn_small_03.sub",
				},
				{
					"name" : "cancel",
					"type" : "button",

					"x" : 20,
					"y" : 62,

					"text" : uiScriptLocale.CANCEL,

					"default_image" : "d:/ymir work/ui/switchbot/btn_small_01.sub",
					"over_image" : "d:/ymir work/ui/switchbot/btn_small_02.sub",
					"down_image" : "d:/ymir work/ui/switchbot/btn_small_03.sub",
				},
				{
					"name" : "destroy",
					"type" : "button",

					"x" : -20,
					"y" : 85,

					"text" : uiScriptLocale.DESTROY,

					"default_image" : "d:/ymir work/ui/switchbot/btn_small_01.sub",
					"over_image" : "d:/ymir work/ui/switchbot/btn_small_02.sub",
					"down_image" : "d:/ymir work/ui/switchbot/btn_small_03.sub",
				},	
			),
		},
	),
}
