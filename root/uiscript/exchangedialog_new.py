import uiScriptLocale
 
ROOT = "d:/ymir work/ui/game/"
	
window = {
	"name" : "ExchangeDialog",
	"x" : 0,
	"y" : 0,
	"style" : ("movable", "float","animation",),
		"width" : 442,
		"height" : 335,
	"children" :
	(
		{		
			"name" : "ExchangeLogs",
			"type" : "thinboard",

			"x" : 20,
			"y" : 220,
			"width" : 402,
			"height" : 100,		
		},
		{
			"name" : "board",
			"type" : "board",
			"style" : ("attach",),
			"x" : 0,
			"y" : 0,
			"width" : 442,
			"height" : 235,
			"children" :
			(
				{
				    "name" : "TitleBar",
				    "type" : "titlebar",
									"style" : ("attach",),
				    "x" : 8,
				    "y" : 8,
				    "width" : 427,
				    "color" : "gray",
				    "children" :
				    (
						{ "name":"TitleName", "type":"text", "x":222, "y":3, "text":"Schimb", "text_horizontal_align":"center" },
				    ),
				},
			    {
					"name" : "Middle_Exchange_Button",
					"type" : "toggle_button",
					"x" : 205,
					"y" : 140,
				},
				{
					"name" : "Owner",
					"type" : "window",
					"x" : 241,
					"y" : 33,
					"width" : 200,
					"height" : 200,
					"children" :
					(
						## Face Slot
						{ "name" : "OwnerFaceImage", "type" : "image", "x" : 4, "y" : 4, "image" : "d:/ymir work/ui/game/windows/face_warrior.sub" },
						{ "name" : "OwnerFaceImageSlot", "type" : "image", "x" : 0, "y" : 0, "image" : "d:/ymir work/ui/game/windows/box_face.sub", },
						## Owner Name
						{
							"name" : "Owner_Level_Value",
							"type" : "text",
							"x" : 62,
							"y" : 0,
							"text": "Lv. 999",
							"r":0.0,
							"g":1.0,
							"b":0.0,
							"a":0.5,
							"text_horizontal_align" : "left",
						},
						{
							"name" : "Owner_Name_Value",
							"type" : "text",
							"x" : 102,
							"y" : 0,
							"text": "You",
							"r":1.0,
							"g":1.0,
							"b":1.0,
							"a":0.7,
							"text_horizontal_align" : "left",
						},	
						{
						    "name" : "Owner_Slot",
						    "type" : "grid_table",
						    "start_index" : 0,
							"x" : 0,
							"y" : 60,
							"x_count" : 6,
							"y_count" : 4,
						    "x_step" : 32,
						    "y_step" : 32,
						    "x_blank" : 0,
						    "y_blank" : 0,
						    "image" : "d:/ymir work/ui/public/Slot_Base.sub",
						},
						{
							"name" : "Owner_Overlay",
							"type" : "ani_image",
							"x" : 0,
							"y" : 60,
							"delay" : 5,
							"images" : (
								"d:/ymir work/ui/game/exchange/exchange_accepted_overlay.tga",
							),
						},
						{
						    "name" : "Owner_Money",
						    "type" : "button",
						    "x" : 60,
						    "y" : 35,
						    "default_image" : "d:/ymir work/ui/public/parameter_slot_03.sub",
						    "over_image" : "d:/ymir work/ui/public/parameter_slot_03.sub",
						    "down_image" : "d:/ymir work/ui/public/parameter_slot_03.sub",
						    "children" :
							(
								{
									"name" : "Owner_Money_Value",
									"type" : "text",
									"x" : 88,
									"y" : 2,
									"text" : "1234567",
									"text_horizontal_align" : "right",
								},
						    ),
						},
						{
						    "name" : "Owner_Yang_Text",
						    "type" : "text",
							"x" : 180,
						    "y" : 36,
							"text" : "Yang",
							"text_horizontal_align" : "right",
						},
					),
				},
				{
					"name" : "Target",
					"type" : "window",
					"x" : 10,
					"y" : 33,
					"width" : 200,
					"height" : 200,
					"children" :
					(
						## Face Slot
						{ "name" : "TargetFaceImage", "type" : "image", "x" : 4, "y" : 4, "image" : "d:/ymir work/ui/game/windows/face_warrior.sub" },
						{ "name" : "TargetFaceImageSlot", "type" : "image", "x" : 0, "y" : 0, "image" : "d:/ymir work/ui/game/windows/box_face.sub", },

						{
							"name" : "InfoParent",
							"x" : 57,
							"y" : 2,
							"width": 120,
							"height": 5,

							"children" :
							(
								{
									"name": "Target_Level",
									"type": "text",
									"text": "Lv. 999",
									"x":0,
									"y":-2,
									"r":0.0,
									"g":1.0,
									"b":0.0,
									"a":0.5,
								},

								{
									"name": "Target_Name",
									"type": "text",
									"text": "TargetPlayer",
									"x":40,
									"y":-2,
									"r":1.0,
									"g":1.0,
									"b":1.0,
									"a":0.7,
								},
							),
						},						
						{
						    "name" : "Target_Slot",
						    "type" : "grid_table",
						    "start_index" : 0,
							"x" : 0,
							"y" : 60,
						    "x_count" : 6,
						    "y_count" : 4,
						    "x_step" : 32,
						    "y_step" : 32,
						    "x_blank" : 0,
						    "y_blank" : 0,
						    "image" : "d:/ymir work/ui/public/Slot_Base.sub",
						},
						{
						    "name" : "Target_Money",
						    "type" : "image",
						    "x" : 60,
						    "y" : 35,
						    "image" : "d:/ymir work/ui/public/parameter_slot_03.sub",
						    "children" :
						    (
								{
									"name" : "Target_Money_Value",
									"type" : "text",
									"x" : 88,
									"y" : 2,
									"text" : "1234567",
									"text_horizontal_align" : "right",
								},
						    ),
						},
						{
						    "name" : "Target_Yang_Text",
						    "type" : "text",
						    "x" : 180,
						    "y" : 36,
						    "text" : "Yang",
						    "text_horizontal_align" : "right",
						},
 						{
							"name" : "Target_Overlay",
							"type" : "ani_image",
							"x" : 0,
							"y" : 60,
							"delay" : 5,
							"images" : (
								"d:/ymir work/ui/game/exchange/exchange_accepted_overlay.tga",
							),
						},				       
					),
				},
			),
		},
	),
}
