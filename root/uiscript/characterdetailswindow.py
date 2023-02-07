import localeInfo

MAINBOARD_WIDTH = 230
MAINBOARD_HEIGHT = 364

window = {
	"name" : "CharacterDetailsWindow",
	"style" : ("float","animation",),
	
	"x" : 274,
	"y" : (SCREEN_HEIGHT - 398) / 2,

	"width" : MAINBOARD_WIDTH,
	"height" : MAINBOARD_HEIGHT,
	
	"children" :
	(
		## MainBoard
		{
			"name" : "MainBoard",
			"type" : "board",
			"style" : ("attach","ltr"),
			
			"x" : 0,
			"y" : 0,

			"width" : MAINBOARD_WIDTH,
			"height" : MAINBOARD_HEIGHT,
			
			"children" :
			(
				# bard
				{
					"name" : "bibi",
					"type" : "border_a",
					"style" : ("attach",),
					
					"x" : 6,
					"y" : 31,

					"width" : MAINBOARD_WIDTH - 15,
					"height" : MAINBOARD_HEIGHT - 40,
				},
			
				{
					"name" : "TitleBar",
					"type" : "titlebar",
					"style" : ("attach",),

					"x" : 6,
					"y" : 7,

					"width" : MAINBOARD_WIDTH - 13,
					
					"children" :
					(
						{ "name" : "TitleName", "type" : "text", "x" : 0, "y" : 0, "text": localeInfo.DETAILS_TITLE, "all_align":"center" },
					),
				},
				{
					"name" : "ScrollBar",
					"type" : "scrollbar",

					"x" : 20,
					"y" : 34,
					"size" : MAINBOARD_HEIGHT - 46,
					"horizontal_align" : "right",
				},
			),
		},
	),
}