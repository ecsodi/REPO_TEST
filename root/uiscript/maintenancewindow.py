import uiScriptLocale

BOARD_WIDTH = 200
BOARD_HEIGHT = 32

window = {
	"name" : "MaintenanceWindow",

	"x" : (SCREEN_WIDTH - BOARD_WIDTH) / 2,
	"y" : 0,

	"style" : ("float",),

	"width" : BOARD_WIDTH,
	"height" : BOARD_HEIGHT,

	"children" :
	(
		{
			"name" : "board",
			"type" : "thinboard",

			"x" : 0,
			"y" : 0,

			"width" : BOARD_WIDTH,
			"height" : BOARD_HEIGHT,

			"children" :
			(
				{
					"name" : "desc",
					"type" : "extended_text",

					"x" : 0,
					"y" : 5,

					"horizontal_align" : "center",
				},
			),
		},
	),
}
