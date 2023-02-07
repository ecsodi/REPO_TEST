import uiScriptLocale

window = {
	"name" : "QuestionDialog",
	"style" : ("movable", "float","animation",),

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
					"name" : "message2",
					"type" : "text",

					"x" : -15,
					"y" : 25,

					"horizontal_align" : "center",
					"text" : uiScriptLocale.DROP_ITEM,

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
				{
					"name" : "ItemSlot",
					"type" : "slot",
				
					"x" : 200,
					"y" : 9,
				
					"width" : 32,
					"height" : 200,
					
					"horizontal_align" : "center",
					
					"image" : "d:/ymir work/ui/public/Slot_Base.sub",
				
					"slot" : (
						{"index":0, "x":0, "y":0, "width":32, "height":32},
						{"index":1, "x":0, "y":33, "width":32, "height":32},
						{"index":2, "x":0, "y":66, "width":32, "height":32},
					),
				},
			),
		},
	),
}
