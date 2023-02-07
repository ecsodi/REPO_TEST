import item
import uiScriptLocale

COSTUME_START_INDEX = item.COSTUME_SLOT_START

HEIGHT_WINDOW = 230
WIDTH_WINDOW = 192
EQUIPMENT_START_INDEX = 180 + 810

window = {
		"name" : "CostumeWindow",
		"x" : SCREEN_WIDTH - 175 - WIDTH_WINDOW - 45,
		"y" : SCREEN_HEIGHT - 37 - 569,
		"style" : ("movable", "float",),
		"width" : WIDTH_WINDOW,
		"height" : HEIGHT_WINDOW,
		"children" :
		(
			{
				"name" : "board",
				"type" : "board",
				"style" : ("attach",),
				"x" : 0,
				"y" : 0,
				"width" : WIDTH_WINDOW,
				"height" : HEIGHT_WINDOW,
				"children" :
				(
					{
						"name" : "TitleBar",
						"type" : "titlebar",
						"style" : ("attach",),
						"x" : 6,
						"y" : 6,
						"width" : WIDTH_WINDOW - 15,
						"color" : "yellow",
						"children" :
						(
							{
								"name":"TitleName",
								"type":"text",
								"x": (WIDTH_WINDOW - 15) / 2,
								"y":3,
								"text":uiScriptLocale.COSTUME_WINDOW_TITLE,
								"text_horizontal_align":"center"
							},
						),
					},
					{
						"name" : "Costume_Base",
						"type" : "image",
						"x" : 13,
						"y" : 55,
						"image" : "d:/ymir work/ui/game/normal_interface/normal_costume.png",
						"children" :
						(
							{
								"name" : "CostumeSlot",
								"type" : "slot",
								"x" : 3,
								"y" : 3,
								"width" : WIDTH_WINDOW - 25,
								"height" : HEIGHT_WINDOW - 38,
								"slot" : (
											{"index":COSTUME_START_INDEX+0, "x":65, "y":45, "width":32, "height":64},
											{"index":COSTUME_START_INDEX+1, "x":65, "y": 9, "width":32, "height":32},
											{"index":item.COSTUME_SLOT_WEAPON, "x":17, "y":13, "width":32, "height":96},
											{"index":item.COSTUME_SLOT_PET, "x":17, "y":118, "width":32, "height":32},#cosmetic pet
											{"index":item.COSTUME_SLOT_MOUNT, "x":65, "y":118, "width":32, "height":32},#cosmetic mount
											{"index":1024, "x":115, "y":9, "width":32, "height":32},				# CROWN
											{"index":1028, "x":115, "y":45, "width":32, "height":32},				# SASH SKIN
								),
							},
						),
					},
					{
						"name" : "Buffi_Base",
						"type" : "image",
						"x" : 13,
						"y" : 55,
						"image" : "d:/ymir work/ui/game/normal_interface/buffi_costume.png",
						"children" :
						(
							{
								"name" : "BuffiSlot",
								"type" : "slot",
								"x" : 3,
								"y" : 3,
								"width" : 127,
								"height" : HEIGHT_WINDOW - 38,
								"slot" : (
										{"index":1026, "x":65, "y":45, "width":32, "height":64},				# BUFFI COSTUME
										{"index":1027, "x":65, "y": 9, "width":32, "height":32},				# BUFFI HAIR
										{"index":1025, "x":17, "y":13, "width":32, "height":64},				# BUFFI WEAP
								),
							},
						),
					},
					{
						"name" : "CostumeButton",
						"type" : "radio_button",

						"x" : 15,
						"y" : 30,

						"text" : "Costume",

						"default_image" : "d:/ymir work/ui/public/middle_button_01.sub",
						"over_image" : "d:/ymir work/ui/public/middle_button_02.sub",
						"down_image" : "d:/ymir work/ui/public/middle_button_03.sub",
					},
					{
						"name" : "BuffiButton",
						"type" : "radio_button",

						"x" : 115,
						"y" : 30,

						"text" : "Buffi",

						"default_image" : "d:/ymir work/ui/public/middle_button_01.sub",
						"over_image" : "d:/ymir work/ui/public/middle_button_02.sub",
						"down_image" : "d:/ymir work/ui/public/middle_button_03.sub",
					},
					
				),
			},
		),
	}

