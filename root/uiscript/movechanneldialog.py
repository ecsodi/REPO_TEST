import localeInfo

window = {
	"name" : "MoveChannelDialog",
	"style" : ("movable", "float", "ltr", "animation"),
	
	"x" : (SCREEN_WIDTH/2) - (190/2),
	"y" : (SCREEN_HEIGHT/2) - 100,	

	"width" : 0,
	"height" : 0,
	
	"children" :
	(
		## MainBoard
		{
			"name" : "MoveChannelBoard",
			"type" : "board",
			"style" : ("attach", "ltr"),

			"x" : 0,
			"y" : 0,

			"width" : 0,
			"height" : 0,
			
			"children" :
			(
				## Title Bar
				{
					"name" : "MoveChannelTitle",
					"type" : "titlebar",
					"style" : ("attach",),

					"x" : 6, "y" : 7, "width" : 190 - 13,
					
					"children" :
					(
						{ "name" : "TitleName", "type" : "text", "x" : 0, "y" : 0, "text": "Schimba Canal", "all_align":"center" },
					),
				},

				# {
					# "name" : "BoardThin",
					# "type" : "thinboard_circle",	#_circle
					# "x" : 7, "y" : 30, "width" : 0, "height" : 0,
				# },
			
				{
					"name" : "BlackBoard",
					"type" : "thinboard_circle",	#_circle
					"x" : 13, "y" : 36, "width" : 0, "height" : 0,
				},
				
				{
					"name" : "AcceptButton",
					"type" : "button",
					
					"x" : 15,
					"y" : 30,

					"vertical_align" : "bottom",
					
					"width" : 61,
					"height" : 21,


					"default_image" : "d:/ymir work/ui/public/acceptbutton00.sub",
					"over_image" : "d:/ymir work/ui/public/acceptbutton01.sub",
					"down_image" : "d:/ymir work/ui/public/acceptbutton02.sub",	
				},
				{
					"name" : "CancelButton",
					"type" : "button",

					"x" : 115,
					"y" : 30,

					"vertical_align" : "bottom",
					
					"width" : 61,
					"height" : 21,


					"default_image" : "d:/ymir work/ui/public/canclebutton00.sub",
					"over_image" : "d:/ymir work/ui/public/canclebutton01.sub",
					"down_image" : "d:/ymir work/ui/public/canclebutton02.sub",
				},	
			),
		}, ## MainBoard End
	),
}
