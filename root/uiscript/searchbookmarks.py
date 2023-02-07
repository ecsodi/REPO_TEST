window = {
	"name" : "SearchBookmarks",
	
	"x" : (SCREEN_WIDTH + 520) / 2,
	"y" : SCREEN_HEIGHT / 4,
	
	"style" : ("float", "animation",),
	
	"width" : 230,
	"height" : 250,
	
	"children" :
	(
		{
			"name" : "Board",
			"type" : "board",
			
			"style" : ("attach",),
			
			"x" : 0,
			"y" : 0,
			
			"width" : 230,
			"height" : 250,
			
			"children" :
			(
				## TitleBar
				{
					"name" : "TitleBar",
					"type" : "titlebar",
					
					"style" : ("attach",),
					
					"x" : 8,
					"y" : 7,
					
					"width" : 215,
					
					"color" : "red",
					
					"children" :
					(
						{ "name" : "TitleName", "type" : "text", "x" : 0, "y" : -1, "text" : "Bookmarks", "all_align" : "center" },
					),
				},
			),
		},
	),
}
