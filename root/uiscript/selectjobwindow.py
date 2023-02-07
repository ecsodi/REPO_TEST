import uiScriptLocale

window = {
	"name" : "SelectDialog",
	"style" : ("movable", "float",),

	"x" : 0,
	"y" : 0,
						
	"width" : 300,
	"height" : 235,

	"children" :
	(
		{
			"name" : "Board",
			"type" : "board",
			"style" : ("attach",),

			"x" : 0,
			"y" : 0,

			"width" : 300,
			"height" : 235,

			"children" :
			(		
				{
					"name" : "TitleBar",
					"type" : "titlebar",
					"style" : ("attach",),

					"x" : 61,
					"y" : 7,

					"width" : 232,
					"color" : "red",
					
					"children":
					(
						{ "name" : "TitleName", "type":"text", "x":0, "y":-1, "text":"Alegere competente", "all_align":"center" },
					),
				},	
				
				{
					"name" : "InfoTextSlot",
					"type" : "image",
					"x" : 110,
					"y" : 34,
					"image" : "d:/ymir work/ui/public/Parameter_Slot_05.sub",

					"children" :
					(
						{
							"name" : "InfoText",
							"type": "text",
							"text": "Tiger - Sef",
							"x":0,
							"y":0,
							"r":1.0,
							"g":1.0,
							"b":1.0,
							"a":1.0,
							"all_align" : "center",
						},
					),
				},
				
				{ "name" : "RaceImage", "type" : "image", "x" : 11, "y" : 11, "image" : "d:/ymir work/ui/game/windows/face_warrior.sub" },
				{ "name" : "RaceSlot", "type" : "image", "x" : 7, "y" : 7, "image" : "d:/ymir work/ui/game/windows/box_face.sub", },
						
				{
					"name" : "FirstSkillSlotBack",
					"type" : "grid_table",
					
					"x" : 15,
					"y" : 65,
					
					"start_index" : 0,
					
					"x_count" : 6,
					"y_count" : 1,
					
					"x_step" : 40,
					"y_step" : 40,
					
					"x_blank" : 6,
					"y_blank" : 1,
					
					"image" : "d:/ymir work/ui/skill_slot_job_1.tga",
				},
				{
					"name" : "FirstSkillSlot",
					"type" : "grid_table",
					
					"x" : 15 + 4,
					"y" : 65 + 4,
					
					"start_index" : 0,
					
					"x_count" : 6,
					"y_count" : 1,
					
					"x_step" : 40,
					"y_step" : 40,
					
					"x_blank" : 6,
					"y_blank" : 1,
				},
				
				{
					"name" : "SecondSkillSlotBack",
					"type" : "grid_table",
					
					"x" : 15,
					"y" : 150,
					
					"start_index" : 0,
					
					"x_count" : 6,
					"y_count" : 1,
					
					"x_step" : 40,
					"y_step" : 40,
					
					"x_blank" : 6,
					"y_blank" : 1,
					
					"image" : "d:/ymir work/ui/skill_slot_job_2.tga",
				},
				{
					"name" : "SecondSkillSlot",
					"type" : "grid_table",
					
					"x" : 15 + 4,
					"y" : 150 + 4,
					
					"start_index" : 0,
					
					"x_count" : 6,
					"y_count" : 1,
					
					"x_step" : 40,
					"y_step" : 40,
					
					"x_blank" : 6,
					"y_blank" : 1,
				},
				
				{
					"name" : "SelectButtonFirst",
					"type" : "button",
					
					"x" : 0,
					"y" : 110,
					
					"horizontal_align" : "center",
					
					"default_image" : "d:/ymir work/ui/public/XLarge_Button_01.sub",
					"over_image" : "d:/ymir work/ui/public/XLarge_Button_02.sub",
					"down_image" : "d:/ymir work/ui/public/XLarge_Button_03.sub",
				},
				
				{
					"name" : "SelectButtonSecond",
					"type" : "button",
					
					"x" : 0,
					"y" : 197,
					
					"horizontal_align" : "center",
					
					"default_image" : "d:/ymir work/ui/public/XLarge_Button_01.sub",
					"over_image" : "d:/ymir work/ui/public/XLarge_Button_02.sub",
					"down_image" : "d:/ymir work/ui/public/XLarge_Button_03.sub",
				},				
			),
		},
	),
}