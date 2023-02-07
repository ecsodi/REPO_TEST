import uiScriptLocale

FLAGS = "d:/ymir work/ui/kingdoms_war/"

window = {
	"name" : "KingdomsWarWindow",
	"x" : 80,
	"y" : 20,
	"style" : ("float",),
	"width" : 115,
	"height" : 109 + 33 + 33,
	"children" :
	(
		{
			"name" : "board",
			"type" : "thinboard",
			"x" : 0,
			"y" : 0,
			"width" : 115,
			"height" : 109 + 33 + 33,
			"children" :
			(
				{
					"name" : "ShinsooFlag",
					"type" : "image",
					"x" : 10,
					"y" : 10,
					"image" : FLAGS + "flag_shinsoo.tga",
				},
				{
					"name" : "ShinsooKills",
					"type" : "text",
					"x" : 10 + 40,
					"y" : 10 + (23 / 2) - 6,
					"text" : "0",
				},
				{
					"name" : "ChunjoFlag",
					"type" : "image",
					"x" : 10,
					"y" : 10 + 23 + 10,
					"image" : FLAGS + "flag_chunjo.tga",
				},
				{
					"name" : "ChunjoKills",
					"type" : "text",
					"x" : 10 + 40,
					"y" : 10 + 23 + 10 + (23 / 2) - 6,
					"text" : "0",
				},
				{
					"name" : "JinnoFlag",
					"type" : "image",
					"x" : 10,
					"y" : 10 + 23 + 10 + 23 + 10,
					"image" : FLAGS + "flag_jinno.tga",
				},
				{
					"name" : "JinnoKills",
					"type" : "text",
					"x" : 10 + 40,
					"y" : 10 + 23 + 10 + 23 + 10 + (23 / 2) - 6,
					"text" : "0",
				},
				{
					"name" : "DeathsFlag",
					"type" : "image",
					"x" : 10,
					"y" : 10 + 23 + 10 + 23 + 10 + 23 + 10,
					"image" : FLAGS + "flag_dead.tga",
				},
				{
					"name" : "DeathsT",
					"type" : "text",
					"x" : 10 + 40,
					"y" : 10 + 23 + 10 + 23 + 10 + 23 + 10 + (23 / 2) - 6,
					"text" : "0/0",
				},
				{
					"name" : "Clock",
					"type" : "image",
					"x" : 10,
					"y" : 10 + 23 + 10 + 23 + 10 + 23 + 10 + 23 + 10,
					"image" : FLAGS + "clock.tga",
				},
				{
					"name" : "ClockT",
					"type" : "text",
					"x" : 10 + 40,
					"y" : 10 + 23 + 10 + 23 + 10 + 23 + 10 + 23 + 10 + (23 / 2) - 6,
					"text" : "0 min(s) left",
				},
			),
		},
	),
}
