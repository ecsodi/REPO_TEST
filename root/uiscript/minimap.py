ROOT = "d:/ymir work/ui/minimap/"
ROOT_NEW = "minimap/"

WINDOW_WIDTH = 210
WINDOW_HEIGHT = 124

window = {
	"name" : "MiniMap",

	"x" : SCREEN_WIDTH - WINDOW_WIDTH - 25,
	"y" : 0,

	"width" : WINDOW_WIDTH,
	"height" : WINDOW_HEIGHT,

	"children" :
	(
		## OpenWindow
		{
			"name" : "OpenWindow",
			"type" : "window",

			"x" : 0,
			"y" : 0,

			"width" : WINDOW_WIDTH,
			"height" : WINDOW_HEIGHT,

			"children" :
			(
				{
					"name" : "OpenWindowBGI",
					"type" : "image",
					"x" : 0,
					"y" : 7,
					# "image" : ROOT + "minimap.sub",
					"image" : "minimap/minimap.png",
				},
				## MiniMapWindow
				{
					"name" : "MiniMapWindow",
					"type" : "window",

					"x" : 0,
					"y" : 0,

					"width" : WINDOW_WIDTH,
					"height" : WINDOW_HEIGHT - 4,
				},
				## ScaleUpButton
				{
					"name" : "ScaleUpButton",
					"type" : "button",

					"x" : 6,
					"y" : 94,

					"default_image" : ROOT_NEW + "plus_default.png",
					"over_image" : ROOT_NEW + "plus_default.png",
					"down_image" : ROOT_NEW + "plus_default.png",
				},
				## ScaleDownButton
				{
					"name" : "ScaleDownButton",
					"type" : "button",

					"x" : 6,
					"y" : 112,

					"default_image" : ROOT_NEW + "minus_default.png",
					"over_image" : ROOT_NEW + "minus_default.png",
					"down_image" : ROOT_NEW + "minus_default.png",
				},
				## MiniMapHideButton
				{
					"name" : "MiniMapHideButton",
					"type" : "button",

					"x" : 191,
					"y" : 8,

					"default_image" : ROOT_NEW + "x_default.png",
					"over_image" : ROOT_NEW + "x_default.png",
					"down_image" : ROOT_NEW + "x_default.png",
				},

				# Timer Button
				{
					"name" : "TimerWindow",
					"type" : "button",

					"x" : 191,
					"y" : 112,
					"tooltip_text" : "Dungeon Info",

					"default_image" : ROOT_NEW + "d_default.png",
					"over_image" : ROOT_NEW + "d_default.png",
					"down_image" : ROOT_NEW + "d_default.png",
				},
				
				# Biologist Button
				{
					"name" : "BiologistMission",
					"type" : "button",

					"x" : 171,
					"y" : 112,
					"tooltip_text" : "Biolog",

					"default_image" : ROOT_NEW + "b_default.png",
					"over_image" : ROOT_NEW + "b_default.png",
					"down_image" : ROOT_NEW + "b_default.png",
				},
				## AtlasShowButton
				{
					"name" : "AtlasShowButton",
					"type" : "button",

					"x" : 6,
					"y" : 8,

					"default_image" : ROOT_NEW + "m_Default.png",
					"over_image" : ROOT_NEW + "m_Default.png",
					"down_image" : ROOT_NEW + "m_Default.png",
				},
				## ServerInfo
				{
					"name" : "ServerInfo",
					"type" : "text",
					
					"text_horizontal_align" : "center",

					"outline" : 1,

					"x" : 70 + 35,
					"y" : 140,

					"text" : "",
				},
				## PositionInfo
				{
					"name" : "PositionInfo",
					"type" : "text",
					
					"text_horizontal_align" : "center",

					"outline" : 1,

					"x" : 70 + 35,
					"y" : 160 + 20,

					"text" : "",
				},

				## Clock Info
				{
					"name" : "Clock",
					"type" : "text",
					
					"text_horizontal_align" : "center",

					"outline" : 1,

					"x" : 70 + 35,
					"y" : 160,

					"text" : "",
				},
				
				## ObserverCount
				{
					"name" : "ObserverCount",
					"type" : "text",
					
					"text_horizontal_align" : "center",

					"outline" : 1,

					"x" : 70 + 35,
					"y" : 180,

					"text" : "",
				},
			),
		},
		
		{
			"name" : "MastWindow",
			"type" : "thinboard",

			"x" : 12,
			"y" : 160,

			"width" : 105,
			"height" : 37,
			"children" :
			(
				{
					"name" : "MastText",
					"type" : "text",

					"text_horizontal_align" : "center",

					"x" : 55,
					"y" : 8,

					"text" : "Catarg",
				},
				{
					"name" : "MastHp",
					"type" : "gauge",

					"x" : 10,
					"y" : 23,

					"width" : 85,
					"color" : "red",
					
					"tooltip_text" : "HP:  5000000 / 5000000",
				},
			),
		},
		
		{
			"name" : "CloseWindow",
			"type" : "window",

			"x" : 0,
			"y" : 0,

			"width" : 132,
			"height" : 48,

			"children" :
			(
				## ShowButton
				{
					"name" : "MiniMapShowButton",
					"type" : "button",

					"x" : 100,
					"y" : 4,

					"default_image" : ROOT + "minimap_open_default.sub",
					"over_image" : ROOT + "minimap_open_default.sub",
					"down_image" : ROOT + "minimap_open_default.sub",
				},
			),
		},
	),
}
