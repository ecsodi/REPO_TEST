import uiScriptLocale
import localeInfo

WINDOW_WIDTH = 280
WINDOW_HEIGHT = 250

window = {
	"name" : "ValentineEventWindow",

	"x" : 0,
	"y" : 0,

	"style" : ("movable", "float", "animation",),

	"width" : WINDOW_WIDTH,
	"height" : WINDOW_HEIGHT,

	"children":
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
							"name" : "TitleName", 
							"type" : "text", 
							
							"x" : (WINDOW_WIDTH - 15) / 2, 
							"y" : 3, 
							
							"text" : "Valentine Event", 
							"text_horizontal_align":"center" 
						},
					),
				},
			),
		},
	),
}

