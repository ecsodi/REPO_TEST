window = {
	"name" : "bonus_special_object",
	"type" : "window",

	"x" : 0,
	"y" : 0,

	"width" : 210,
	"height" : 20,
	
	"children" :
	[
		{
			"name" : "bonus_name",
			"type" : "text",

			"x":10,
			"y":1,
			
			"text" : "teste bonus",
			"align" : "left",

			"horizontal_align" : "left",
		},
		{
			"name":"slot_base",
			"type":"image",
			
			"x":60,
			"y":0,
			
			"horizontal_align" : "right",
			"vertical_align" : "center",
			
			"image":"d:/ymir work/ui/public/Parameter_Slot_01.sub",
			"children" :
			[
				{
					"name" : "bonus_value",
					"type" : "text",

					"x":0,
					"y":2,
			
					"horizontal_align" : "center",
					"text_horizontal_align" : "center",
					
					"text" : "1231",
				},
			],
		},
	],
}