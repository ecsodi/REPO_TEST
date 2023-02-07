import uiScriptLocale

window = {
	"name" : "PopupDialog",
	"style" : ("float",),

	"x" : SCREEN_WIDTH/2 - 250,
	"y" : SCREEN_HEIGHT/2 - 40,

	"width" : 280,
	"height" : 105,

	"children" :
	(
		{
			"name" : "board",
			"type" : "board",

			"x" : 0,
			"y" : 0,

			"width" : 280,
			"height" : 105,

			"children" :
			(
				{
					"name" : "testWindow",
					"type" : "window",

					"x" : 0,
					"y" : 38 - 15,
					
					"width" : 0,
					"height" : 32,
					
					"horizontal_align" : "center",
					
					"children":
					(
						{
							"name" : "firstText",
							"type" : "text",
		
							"x" : 0,
							"y" : 15,
		
							"text" : uiScriptLocale.MESSAGE,

							"text_vertical_align" : "center",
						},
						{
							"name" : "itemImage",
							"type" : "image",
		
							"x" : 0,
							"y" : 0,
						},
						{
							"name" : "itemImage2",
							"type" : "image",
		
							"x" : 0,
							"y" : 0,
						},
						{
							"name" : "secondText",
							"type" : "text",
		
							"x" : 0,
							"y" : 15,
		
							"text" : uiScriptLocale.MESSAGE,

							"text_vertical_align" : "center",
						},
						{
							"name" : "questionText",
							"type" : "text",
		
							"x" : 0,
							"y" : 15,
		
							"text" : uiScriptLocale.MESSAGE,

							"text_vertical_align" : "center",
						},
						
					),
				},
				{
					"name" : "accept",
					"type" : "button",

					"x" : -40,
					"y" : 63,

					"width" : 61,
					"height" : 21,

					"horizontal_align" : "center",

                    "default_image" : "d:/ymir work/ui/public/acceptbutton00.sub",
                    "over_image" : "d:/ymir work/ui/public/acceptbutton01.sub",
                    "down_image" : "d:/ymir work/ui/public/acceptbutton02.sub",
				},

				{
					"name" : "cancel",
					"type" : "button",

					"x" : 40,
					"y" : 63,

					"width" : 61,
					"height" : 21,

					"horizontal_align" : "center",

					"default_image" : "d:/ymir work/ui/public/canclebutton00.sub",
					"over_image" : "d:/ymir work/ui/public/canclebutton01.sub",
					"down_image" : "d:/ymir work/ui/public/canclebutton02.sub",
				},
				
			),
		},
	),
}