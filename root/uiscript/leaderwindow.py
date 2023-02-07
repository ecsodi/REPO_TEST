import uiScriptLocale

window = {
	"name" : "leaderswindow",

	"x" : SCREEN_WIDTH - 170,
	"y" : SCREEN_HEIGHT - 400 - 50,

	"style" : ("movable", "float",),

	"width" : 170+100,
	"height" : 300,

	"children" :
	(

		{
			"name" : "board",
			"type" : "board_with_titlebar",
			"style" : ("attach", ),

			"x" : 0,
			"y" : 0,
			"show_crown" : 1,

			"width" : 170+100,
			"height" : 300,
			"title" : "[Info List] - Lideri Breasla Online",
		},
		{
			"name" : "board_stanga",
			"type" : "new_board",
			
			"x" : 7,
			"y" : 35,
			
			"width" : 254,
			"height" : 255,
		},
		{
			"name" : "ScrollBar",
			"type" : "scrollbar",

			"x" : 27,
			"y" : 40,
			"size" : 220,
			"horizontal_align" : "right",
		},

		#{
		#	"name" : "ok",
		#	"type" : "button",
        #
		#	"x" : 80,
		#	"y" : 265,
        #
		#	"width" : 61,
		#	"height" : 21,
        #
		#	"text" : "Ok",
        #
		#	"default_image" : "d:/ymir work/ui/public/small_button_01.sub",
		#	"over_image" : "d:/ymir work/ui/public/small_button_02.sub",
		#	"down_image" : "d:/ymir work/ui/public/small_button_03.sub",
		#},
		#
		#{
		#	"name" : "savasgonder",
		#	"type" : "button",
        #
		#	"x" : 145,
		#	"y" : 265,
        #
		#	"width" : 61,
		#	"height" : 21,
        #
		#	"text" : "Lupta",
        #
		#	"default_image" : "d:/ymir work/ui/public/small_button_01.sub",
		#	"over_image" : "d:/ymir work/ui/public/small_button_02.sub",
		#	"down_image" : "d:/ymir work/ui/public/small_button_03.sub",
		#},
		{
			"name" : "cancel",
			"type" : "button",

			"x" : 115+100,
			"y" : 265,

			"width" : 41,
			"height" : 21,

			"text" : "Anuleaza",

			"default_image" : "d:/ymir work/ui/public/small_button_01.sub",
			"over_image" : "d:/ymir work/ui/public/small_button_02.sub",
			"down_image" : "d:/ymir work/ui/public/small_button_03.sub",
		},

		{
			"name" : "refresh",
			"type" : "button",

			"x" : 15,
			"y" : 265,

			"width" : 41,
			"height" : 21,

			"text" : "Refresh",

			"default_image" : "d:/ymir work/ui/public/small_button_01.sub",
			"over_image" : "d:/ymir work/ui/public/small_button_02.sub",
			"down_image" : "d:/ymir work/ui/public/small_button_03.sub",
		},
	)
}