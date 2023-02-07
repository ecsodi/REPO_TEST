import uiScriptLocale

IMAGE_PATH = "d:/ymir work/ui/wheelg/wheel_of_fright/"
WINDOW_WIDTH = 444
WINDOW_HEIGHT = 448

window = {
	"name" : "ReactEventWindow",

	"x" : (SCREEN_WIDTH - WINDOW_WIDTH) / 2,
	"y" : (SCREEN_HEIGHT - WINDOW_HEIGHT) / 2,

	"style" : ("movable", "float", "animation",),

	"width" : WINDOW_WIDTH,
	"height" : WINDOW_HEIGHT,

	"children" :
	(
		{
			"name" : "background",
			"type" : "image",

			"style" : ("movable", "attach",),

			"x" : 0,
			"y" : 0,

			"image" : IMAGE_PATH + "bg.tga",

			"children" :
			(
				{
					"name" : "TitleBar",
					"type" : "titlebar",
					"style" : ("attach",),

					"x" : 6,
					"y" : 5,

					"width" : WINDOW_WIDTH - 10,
					"color" : "red",

					"children" :
					(
						{
							"name" : "TitleName",
							"type" : "text",
							"text" : uiScriptLocale.CHRISTMAS_WHEEL,
							"horizontal_align" : "center",
							"text_horizontal_align" : "center",
							"x" : 0,
							"y" : 3,
						},
					),
				},
				{
					"name" : "WheelBoard",
					"type" : "image",

					"x" : 0,
					"y" : 13,

					"horizontal_align" : "center",
					"vertical_align" : "center",

					"image" : IMAGE_PATH + "rad_bg.tga",
				},
				{
					"name" : "Slice1",
					"type" : "image",
					"x" : 0,
					"y" : 13,
					"horizontal_align" : "center",
					"vertical_align" : "center",
					"image" : IMAGE_PATH + "rad_1.tga",
				},
				{
					"name" : "Slice2",
					"type" : "image",
					"x" : 0,
					"y" : 13,
					"horizontal_align" : "center",
					"vertical_align" : "center",
					"image" : IMAGE_PATH + "rad_2.tga",
				},
				{
					"name" : "Slice3",
					"type" : "image",
					"x" : 0,
					"y" : 13,
					"horizontal_align" : "center",
					"vertical_align" : "center",
					"image" : IMAGE_PATH + "rad_3.tga",
				},
				{
					"name" : "Slice4",
					"type" : "image",
					"x" : 0,
					"y" : 13,
					"horizontal_align" : "center",
					"vertical_align" : "center",
					"image" : IMAGE_PATH + "rad_4.tga",
				},
				{
					"name" : "Slice5",
					"type" : "image",
					"x" : 0,
					"y" : 13,
					"horizontal_align" : "center",
					"vertical_align" : "center",
					"image" : IMAGE_PATH + "rad_5.tga",
				},
				{
					"name" : "Slice6",
					"type" : "image",
					"x" : 0,
					"y" : 13,
					"horizontal_align" : "center",
					"vertical_align" : "center",
					"image" : IMAGE_PATH + "rad_6.tga",
				},
				{
					"name" : "Slice7",
					"type" : "image",
					"x" : 0,
					"y" : 13,
					"horizontal_align" : "center",
					"vertical_align" : "center",
					"image" : IMAGE_PATH + "rad_7.tga",
				},
				{
					"name" : "Slice8",
					"type" : "image",
					"x" : 0,
					"y" : 13,
					"horizontal_align" : "center",
					"vertical_align" : "center",
					"image" : IMAGE_PATH + "rad_8.tga",
				},
				{
					"name" : "Slice9",
					"type" : "image",
					"x" : 0,
					"y" : 13,
					"horizontal_align" : "center",
					"vertical_align" : "center",
					"image" : IMAGE_PATH + "rad_9.tga",
				},
				{
					"name" : "Slice10",
					"type" : "image",
					"x" : 0,
					"y" : 13,
					"horizontal_align" : "center",
					"vertical_align" : "center",
					"image" : IMAGE_PATH + "rad_10.tga",
				},
				{
					"name" : "ItemSlots",
					"type" : "slot",

					"style" : ("movable", "attach",),

					"x" : WINDOW_WIDTH / 2 - 16 - 118,
					"y" : WINDOW_HEIGHT / 2 - 16 + 13 - 124,

					"width" : 240 + 118,
					"height" : 240 + 124,

					"slot" :
					(
						{ "index" : 0, "x" : 118+0, 	"y" :	124+ -124, "width" : 32, "height" : 32 },
						{ "index" : 1, "x" : 118+73, 	"y" :	124+ -101, "width" : 32, "height" : 32 },
						{ "index" : 2, "x" : 118+118, 	"y" :	124+ -38, "width" : 32, "height" : 32 },
						{ "index" : 3, "x" : 118+118, 	"y" :	124+ 38, "width" : 32, "height" : 32 },
						{ "index" : 4, "x" : 118+73, 	"y" :	124+ 101, "width" : 32, "height" : 32 },
						{ "index" : 5, "x" : 118+0, 	"y" :	124+ 124, "width" : 32, "height" : 32 },
						{ "index" : 6, "x" : 118+-73, 	"y" :	124+ 101, "width" : 32, "height" : 32 },
						{ "index" : 7, "x" : 118+-118, 	"y" :	124+ 38, "width" : 32, "height" : 32 },
						{ "index" : 8, "x" : 118+-118, 	"y" :	124+ -38, "width" : 32, "height" : 32 },
						{ "index" : 9, "x" : 118+-73, 	"y" :	124+ -100, "width" : 32, "height" : 32 },
					),
				},
				{
					"name" : "WheelPointer",
					"type" : "expanded_image",

					"x" : 0,
					"y" : 13,

					"horizontal_align" : "center",
					"vertical_align" : "center",

					"image" : IMAGE_PATH + "rad_pointer.tga",
				},
				{
					"name" : "WheelStartButton",
					"type" : "button",

					"x" : 0,
					"y" : 13,

					"horizontal_align" : "center",
					"vertical_align" : "center",

					"default_image" : IMAGE_PATH + "rad_pointer.tga",
					"over_image" : IMAGE_PATH + "rad_pointer_hover.tga",
					"down_image" : IMAGE_PATH + "rad_pointer_down.tga",
				},
				{
					"name" : "InfoButton",
					"type" : "button",

					"x" : 38,
					"y" : 32,

					"horizontal_align" : "right",

					"default_image" : "d:/ymir work/ui/game/eqchanger/info_normal.tga",
					"over_image" : "d:/ymir work/ui/game/eqchanger/info_hover.tga",
					"down_image" : "d:/ymir work/ui/game/eqchanger/info_normal.tga",
				},
			),
		},
	),
}
