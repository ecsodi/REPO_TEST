import uiScriptLocale

window = {
	"name" : "CostumeWindow",
	"x" : SCREEN_WIDTH - 175 - 140,
	"y" : SCREEN_HEIGHT - 37 - 565,
	"style" : ("movable", "float",),
	"width" : 140,
	"height" : 240,
	"children" :
	(
		{
			"name" : "board",
			"type" : "board",
			"style" : ("attach",),
			"x" : 0,
			"y" : 0,
			"width" : 140,
			"height" : 240,
			"children" :
			(
				{
					"name" : "TitleBar",
					"type" : "titlebar",
					"style" : ("attach",),

					"x" : 6,
					"y" : 6,

					"width" : 130,
					"color" : "yellow",

					"children" :
					(
						{ "name":"TitleName", "type":"text", "x":60, "y":3, "text":uiScriptLocale.COSTUME_WINDOW_TITLE, "text_horizontal_align":"center" },
					),
				},
				
				{
					"name" : "TitleBarEffect",
					"type" : "horizontalbar",
					"style" : ("attach",),
					"x" : 13,
					"y" : 166,
					"width" : 114,
					"children" :
					(
						{
							"name" : "TitleName",
							"type" : "text",
							"x" : 0,
							"y" : -1,
							"text" : uiScriptLocale.SPECIAL_EFFECTS_TITLE,
							"all_align" : "center",
						},
					),
				},
				
				{
					"name" : "EffectSlots_Base",
					"type" : "image",
					"x" : 13,
					"y" : 167 + 16,
					"image" : "d:/ymir work/ui/effect_slot_bg.jpg",
				},
				
				{
					"name" : "Costume_Base",
					"type" : "image",
					"x" : 13,
					"y" : 38,
					"image" : "d:/ymir work/ui/costume_bg.tga",
					"children" :
					(
						{
							"name" : "CostumeSlot",
							"type" : "slot",
							"x" : 3,
							"y" : 3,
							"width" : 127,
							"height" : 236 + 11,
							"slot" : (
										{"index":19, "x":61, "y":45, "width":32, "height":64},
										{"index":20, "x":61, "y": 8, "width":32, "height":32},
										{"index":21, "x":52, "y":4+145, "width":32, "height":32},
										{"index":22, "x":0, "y":5+145, "width":32, "height":32},
										{"index":23, "x":52, "y":4+197, "width":32, "height":32},
										{"index":24, "x":1, "y": 5+197, "width":32, "height":32},
							),
						},
					),
				},
			),
		},
	),
}

