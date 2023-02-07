import uiScriptLocale
import localeInfo
window = {
	"name" : "DragonSoulRefineWindow",

	## ��ȥ�� â �ٷ� ����
	"x" : SCREEN_WIDTH - 176 - 287 - 10 - 287 - 5,
	"y" : SCREEN_HEIGHT - 37 - 565,

	"style" : ("movable", "float","animation",),

	"width" : 250,
	"height" : 160,

	"children" :
	(
		{
			"name" : "board",
			"type" : "board",
			"style" : ("attach",),

			"x" : 0,
			"y" : 0,

			"width" : 250,
			"height" : 160,

			"children" :
			(
				## Base BackGroud Image
				{
					"name" : "DragonSoulRefineWindowBaseImage",
					"type" : "expanded_image",
					"x" : 25,
					"y" : 40,

					"image" : "d:/ymir work/ui/dragonsoul/dragon_soul_refine_bg.tga",
				},

				## Title
				{
					"name" : "TitleBar",
					"type" : "titlebar",
					"style" : ("attach",),

					"x" : 5,
					"y" : 7,

					"width" : 250 - 15,
					"color" : "yellow",

					"children" :
					(
						{ 
							"name":"TitleName", 
							"type":"text", 
							"x":(250 - 15) / 2, 
							"y":3, 
							"text":uiScriptLocale.DRAGONSOUL_REFINE_WINDOW_TITLE, 
							"text_horizontal_align":"center" 
						},
					),
				},
				
				## Refine Slot
				{
					"name" : "RefineSlot",
					"type" : "grid_table",

					"image" : "d:/ymir work/ui/pet/skill_button/skill_enable_button.sub", 

					"x" : 40,
					"y" : 45,

					"start_index" : 0,
					"x_count" : 2,
					"y_count" : 1,
					"x_step" : 41,
					"y_step" : 32,
				},

				## Result Slot
				{
					"name" : "ResultSlot",
					"type" : "grid_table",

					"x" : 173,
					"y" : 45,

					"start_index" : 0,
					"x_count" : 1,
					"y_count" : 1,
					"x_step" : 32,
					"y_step" : 32,
				},
				
				## Grade Button
				{
					"name" : "GradeButton",
					"type" : "toggle_button",

					"x" : 5,
					"y" : 85,

					"default_image" : "d:/ymir work/ui/dragonsoul/button_01.tga",
					"over_image" : "d:/ymir work/ui/dragonsoul/button_02.tga",
					"down_image" : "d:/ymir work/ui/dragonsoul/button_03.tga",

					"children" :
					(
						{
							"name" : "GradeSlotTitle",
							"type" : "text",
							"x" : 0,
							"y" : 0,
							"all_align" : "center",
							"text" : uiScriptLocale.GRADE_SELECT,
							"color" : 0xFFF1E6C0,
						},
					),
				},

				## Step Button
				{
					"name" : "StepButton",
					"type" : "toggle_button",

					"x" : 80+5,
					"y" : 85,

					"default_image" : "d:/ymir work/ui/dragonsoul/button_01.tga",
					"over_image" : "d:/ymir work/ui/dragonsoul/button_02.tga",
					"down_image" : "d:/ymir work/ui/dragonsoul/button_03.tga",

					"children" :
					(
						{
							"name" : "StepSlotTitle",
							"type" : "text",
							"x" : 0,
							"y" : 0,
							"all_align" : "center",
							"text" : uiScriptLocale.STEP_SELECT,
							"color" : 0xFFF1E6C0,
						},
					),
				},

				## Refine Button
				{
					"name" : "StrengthButton",
					"type" : "toggle_button",

					"x" : 80*2+5,
					"y" : 85,

					"default_image" : "d:/ymir work/ui/dragonsoul/button_01.tga",
					"over_image" : "d:/ymir work/ui/dragonsoul/button_02.tga",
					"down_image" : "d:/ymir work/ui/dragonsoul/button_03.tga",

					"children" :
					(
						{
							"name" : "RefineSlotTitle",
							"type" : "text",
							"x" : 0,
							"y" : 0,
							"all_align" : "center",
							"text" : uiScriptLocale.STRENGTH_SELECT,
							"color" : 0xFFF1E6C0,
						},
					),
				},
				## Base BackGroud Image
				{
					"name" : "MoneyBar",
					"type" : "expanded_image",
					"x" : 14,
					"y" : 107,

					"image" : "d:/ymir work/ui/public/parameter_slot_06.sub",
					
					"children" :
					(
						{
							"name":"Money_Slot",
							"type" : "text",

							"x":5,
							"y":0,

							"horizontal_align" : "right",
							"text_horizontal_align" : "right",

							"text" : "123456789",
						},
					),
				},


				## Do Refine Button
				{
					"name" : "DoRefineButton",
					"type" : "button",

					"x" : 150,
					"y" : 130,

					"default_image" : "d:/ymir work/ui/dragonsoul/l_button01.tga",
					"over_image" : "d:/ymir work/ui/dragonsoul/l_button02.tga",
					"down_image" : "d:/ymir work/ui/dragonsoul/l_button03.tga",

					"children" :
					(
						{ 
							"name" : "DoRefineButtonTitle", 
							"type" : "text", 
							"x" : 0, 
							"y" : 0, 
							"text" : uiScriptLocale.DO_REFINE, 
							"all_align" : "center",
						},
					),
				},
				
				{
					"name" : "refine_all_button",
					"type" : "button",

					"x" : 10,
					"y" : 130,

					"text" : "Rafinare totala",

					"default_image" : "d:/ymir work/ui/dragonsoul/l_button01.tga",
					"over_image" : "d:/ymir work/ui/dragonsoul/l_button02.tga",
					"down_image" : "d:/ymir work/ui/dragonsoul/l_button03.tga",
				},
			),
		},
	),
}

