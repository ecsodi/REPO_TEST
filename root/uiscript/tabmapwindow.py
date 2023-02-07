import uiScriptLocale
WINDOW_HEIGHT = 453
WINDOW_WIDTH = 690

window = {
	"name" : "TabMapWindow",

	"x" : 0,
	"y" : 0,

	"style" : ("movable", "float",),

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
			"height" : WINDOW_HEIGHT,

			"children" :
			(
				## Title
				{
					"name" : "TitleBar",
					"type" : "titlebar",
					"style" : ("attach",),

					"x" : 8,
					"y" : 7,

					"width" : WINDOW_WIDTH - 15,
					"color" : "yellow",

					"children" :
					(
						{ 
							"name": "TitleName", 
							"type": "text", 
							"x": 0, 
							"y": 3, 
							"text": "Teleporter", 
							"horizontal_align": "center", 
							"text_horizontal_align": "center" 
						},
					),
				},
			),
		},
	),
}
