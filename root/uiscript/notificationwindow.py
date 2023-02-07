ROOT_DIR = "d:/ymir work/ui/game/ranking/"

window = {
	"name" : "NotificationWindow",
	"style" : ("float",),
	"x" : -100,
	"y" : 600,
	"width" : 273,
	"height" : 90,
	"children" :
	(
		{
			"name" : "line",
			"type" : "image",
			# "style" : ("attach",),
			"x" : 0,
			"y" : 0,
			"image" : ROOT_DIR + "main.png",
			"children" : 
			(
				{
					"name" : "Player_Name",
					"type" : "text",
					"x" : 77,
					"y" : 47,
					"text" : "",
					"color" : 0xffffdd9b,
				},
				{
					"name" : "Status_Text",
					"type" : "text",
					"x" : 77,
					"y" : 46 + 13,
					"text" : "",
					"color" : 0xff9bd1ff,
				},
				{
					"name" : "faceIMG",
					"type" : "image",
					"style" : ("attach",),
					"x" : 4,
					"y" : 26,
					"image" : ROOT_DIR + "shaman_w.tga",
				},
			),
		},
	),
}