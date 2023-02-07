import uiScriptLocale
NEW_PATH = "d:/ymir work/ui/game/new_login/"

window = {
	"name" : "LoginWindow",
	"sytle" : ("movable",),

	"x" : 0,
	"y" : 0,

	"width" : SCREEN_WIDTH,
	"height" : SCREEN_HEIGHT,

	"children" :
	(
		## Board
		{
			"name" : "BackGround", "type" : "expanded_image", "x" : 0, "y" : 0,
			"x_scale" : float(SCREEN_WIDTH) / 1920.0, "y_scale" : float(SCREEN_HEIGHT) / 1080.0,
			"image" : NEW_PATH + "loading.png",
		},
		
		{ 
			"name":"ErrorMessage", 
			"type":"text", "x":10, "y":10, 
			"text": uiScriptLocale.LOAD_ERROR, 
		},
		{
			"name" : "LoadingBoard",
			"type" : "window",
			"x" : float(SCREEN_WIDTH) / 2  - 330/2,
			"y" : float(SCREEN_HEIGHT) / 2 - 50,
			"width" : 268, 
			"height": 268,

			"children" :
			(
				{
					"name" : "LoadingAnimation",
					"type" : "ani_image",


					"x" : -50,
					"y" : -130,

					"delay" : 2,

					"images" :
					(
						"d:/ymir work/ui/game/load/1.png",
						"d:/ymir work/ui/game/load/2.png",
						"d:/ymir work/ui/game/load/3.png",
						"d:/ymir work/ui/game/load/4.png",
						"d:/ymir work/ui/game/load/5.png",
						"d:/ymir work/ui/game/load/6.png",
						"d:/ymir work/ui/game/load/7.png",
						"d:/ymir work/ui/game/load/8.png",
						"d:/ymir work/ui/game/load/9.png",
						"d:/ymir work/ui/game/load/10.png",
						"d:/ymir work/ui/game/load/11.png",
						"d:/ymir work/ui/game/load/12.png",
						"d:/ymir work/ui/game/load/13.png",
						"d:/ymir work/ui/game/load/14.png",
						# "d:/ymir work/ui/game/load/deimosloading_00011.png",
						# "d:/ymir work/ui/game/load/deimosloading_00012.png",
						# "d:/ymir work/ui/game/load/deimosloading_00013.png",
						# "d:/ymir work/ui/game/load/deimosloading_00014.png",
						# "d:/ymir work/ui/game/load/deimosloading_00015.png",
						# "d:/ymir work/ui/game/load/deimosloading_00016.png",
						# "d:/ymir work/ui/game/load/deimosloading_00017.png",
						# "d:/ymir work/ui/game/load/deimosloading_00018.png",
						# "d:/ymir work/ui/game/load/deimosloading_00019.png",
						# "d:/ymir work/ui/game/load/deimosloading_00020.png",
						# "d:/ymir work/ui/game/load/deimosloading_00021.png",
						# "d:/ymir work/ui/game/load/deimosloading_00022.png",
						# "d:/ymir work/ui/game/load/deimosloading_00020.png",
						# "d:/ymir work/ui/game/load/deimosloading_00021.png",
						# "d:/ymir work/ui/game/load/deimosloading_00022.png",
						# "d:/ymir work/ui/game/load/deimosloading_00023.png",
						# "d:/ymir work/ui/game/load/deimosloading_00024.png",
						# "d:/ymir work/ui/game/load/deimosloading_00025.png",
						# "d:/ymir work/ui/game/load/deimosloading_00026.png",
						# "d:/ymir work/ui/game/load/deimosloading_00027.png",
						# "d:/ymir work/ui/game/load/deimosloading_00028.png",
						# "d:/ymir work/ui/game/load/deimosloading_00029.png",
						# "d:/ymir work/ui/game/load/deimosloading_00030.png",
					)
				},
			),
		},
		{
			"name" : "GageBoard",
			"type" : "window",
			"x" : float(SCREEN_WIDTH) * 400 / 800.0 - 200,
			"y" : float(SCREEN_HEIGHT) * 500 / 600.0 ,
			"width" : 400, 
			"height": 80,

			"children" :
			(
				{
					"name" : "BackGage",
					"type" : "expanded_image",


					"x" : 320,
					"y" : -100,

					# "image" : "locale/ui/loading/gauge_full.dds",

				},
				{
					"name" : "FullGage",
					"type" : "expanded_image",

					"x" : 40,
					"y" : 25,

					# "image" : "locale/ui/loading/gauge_full.dds",
				},
			),
		},
	),
}
