import uiScriptLocale
import localeInfo

WINDOW_X = 546
WINDOW_Y = 228

WORLDARD_PATCH = "Switchbot/design/"

window = {
	"name" : "Cambiador",

	"x" : SCREEN_WIDTH/2-(WINDOW_X/2),
	"y" : SCREEN_HEIGHT/2-(WINDOW_Y/2),

	"style" : ("movable", "float"),

	"width" : WINDOW_X,
	"height" : WINDOW_Y,

	"children" :
	(
		{
			"name" : "board",
			"type" : "board",

			"x" : 0,
			"y" : 0,

			"width" :WINDOW_X,
			"height" : WINDOW_Y,

			"children" :
			(
				## Title
				{
					"name" : "TitleBar",
					"type" : "titlebar",

					"x" : 8,
					"y" : 7,

					"width" : WINDOW_X-15,
					"color" : "yellow",

					"children" :
					(
						{ "name":"TitleName", "type":"text", "x":WINDOW_X/2, "y":3, "text":localeInfo.SWITCHBOT_TEXT_08, "text_horizontal_align":"center" },
					),
				},


				{
					"name" : "base",
					"type" : "image",

					"x" : 10,
					"y" : 32,

					"image" : WORLDARD_PATCH+"base.tga",
				},

				{
					"name" : "bar_img",
					"type" : "image",

					"x" : 13,
					"y" : 35,

					"image" : WORLDARD_PATCH+"barra_titulos.tga",

					"children":
					(
						{ "name":"titlte_item", "type":"text", "x":23, "y":4, "text": localeInfo.SWITCHBOT_TEXT_09, },
						{ "name":"title_bonus", "type":"text", "x":160, "y":4, "text": localeInfo.SWITCHBOT_TEXT_10, },
						{ "name":"presets_bonus", "type":"text", "x":405, "y":4, "text": localeInfo.SWITCHBOT_TEXT_11, },
					),
				},


				{
					"name" : "bg_slots",
					"type" : "image",

					"x" : 13,
					"y" : 57,

					"image" : WORLDARD_PATCH+"slot_item.tga",
				},
				{
					"name" : "slot_item",
					"type" : "slot",
					"x" : 13,
					"y" : 57,

					"width" : 72,
					"height" : 158,
							
					"slot" : (
						{"index":0, "x":20, "y":10, "width":32, "height":96},
						{"index":1, "x":20, "y":122, "width":32, "height":32},
					),
				},

				{
					"name" : "base_save",
					"type" : "image",

					"x" : 359,
					"y" : 57,

					"image" : WORLDARD_PATCH+"base_bonus_guardados.tga",
				},

				{
					"name" : "scrollbar",
					"type" : "scrollbar_new",

					"x" : 523,
					"y" : 57,

					"size" : 156,
				},
				{
					"name" : "save_button",
					"type" : "button",

					"x" : 86,
					"y" : 178,

					"text": localeInfo.SWITCHBOT_TEXT_12,

					"default_image" : WORLDARD_PATCH+"guardar_1.tga",
					"over_image" :  WORLDARD_PATCH+"guardar_2.tga",
					"down_image" : WORLDARD_PATCH+"guardar_3.tga",

				},

				{
					"name" : "change_button",
					"type" : "button",

					"x" : 206,
					"y" : 178,

					"text" : localeInfo.SWITCHBOT_TEXT_13,

					"default_image" : WORLDARD_PATCH+"empezar_1.tga",
					"over_image" :  WORLDARD_PATCH+"empezar_2.tga",
					"down_image" : WORLDARD_PATCH+"empezar_3.tga",
				},
			),
		},
	),
}