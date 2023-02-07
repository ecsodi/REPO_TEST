import uiScriptLocale

window = {
	"name" : "PopupDialog",
	"style" : ("float","animation",),

    "x": SCREEN_WIDTH / 2 - 125,
    "y": SCREEN_HEIGHT / 2 - 52,

	"width" : 280,
	"height" : 75,

	"children" :
	(
		{
			"name" : "board",
			"type" : "board",

			"x" : 0,
			"y" : 0,

			"width" : 280,
			"height": 75,

			"children" :
			(
				{
					"name" : "message",
					"type" : "text",

					"x" : 0,
					"y" : 25,

					"text" : uiScriptLocale.MESSAGE,

					"horizontal_align" : "center",
					"text_horizontal_align" : "center",
					"text_vertical_align" : "center",
				},
				{
					"name" : "Time",
					"type" : "text",

					"x" : 0,
					"y" : 45,

					"text" : "",

					"horizontal_align" : "center",
					"text_horizontal_align" : "center",
					"text_vertical_align" : "center",
				},
				{
					"name" : "accept",
					"type" : "button",

					"x" : 0,
					"y" : 40,

					"width" : 61,
					"height" : 21,

					"horizontal_align" : "center",
					"text" : uiScriptLocale.OK,

					"default_image" : "d:/ymir work/ui/public/middle_button_01.sub",
					"over_image" : "d:/ymir work/ui/public/middle_button_02.sub",
					"down_image" : "d:/ymir work/ui/public/middle_button_03.sub",
				},
			),
		},
	),
}
