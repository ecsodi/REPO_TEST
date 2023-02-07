import uiScriptLocale

ROOT = "d:/ymir work/ui/public/"

window = {
	"name" : "WhisperDialog",
	"style" : ("movable", "float","animation",),

	"x" : 0,
	"y" : 0,

	"width" : 300,
	"height" : 215,

	"children" :
	(
		
		{
			"name" : "board_emoticons",
			"type" : "thinboard",
			"style" : ("attach",),

			"x" : 0,
			"y" : 0,

			"width" : 50,
			"height" : 215,
			
			"children" :
			(
				{
					"name" : "emoticon_0",
					"type" : "button",

					"x" : 21,
					"y" : 9,

					"default_image" : "icon/emoticons/devil.tga",
					"over_image" : "icon/emoticons/devil.tga",
					"down_image" : "icon/emoticons/devil.tga",
				},
				
				{
					"name" : "emoticon_1",
					"type" : "button",

					"x" : 21,
					"y" : 9 + 25,

					"default_image" : "icon/emoticons/angel.tga",
					"over_image" : "icon/emoticons/angel.tga",
					"down_image" : "icon/emoticons/angel.tga",
				},
				
				{
					"name" : "emoticon_2",
					"type" : "button",

					"x" : 21,
					"y" : 9 + 50,

					"default_image" : "icon/emoticons/sunglasses.tga",
					"over_image" : "icon/emoticons/sunglasses.tga",
					"down_image" : "icon/emoticons/sunglasses.tga",
				},
				
				{
					"name" : "emoticon_3",
					"type" : "button",

					"x" : 21,
					"y" : 9 + 75,

					"default_image" : "icon/emoticons/heart.tga",
					"over_image" : "icon/emoticons/heart.tga",
					"down_image" : "icon/emoticons/heart.tga",
				},
				
				{
					"name" : "emoticon_4",
					"type" : "button",

					"x" : 21,
					"y" : 9 + 100,

					"default_image" : "icon/emoticons/tongue.tga",
					"over_image" : "icon/emoticons/tongue.tga",
					"down_image" : "icon/emoticons/tongue.tga",
				},
				
				{
					"name" : "emoticon_5",
					"type" : "button",

					"x" : 21,
					"y" : 9 + 125,

					"default_image" : "icon/emoticons/crying.tga",
					"over_image" : "icon/emoticons/crying.tga",
					"down_image" : "icon/emoticons/crying.tga",
				},
				
				{
					"name" : "emoticon_6",
					"type" : "button",

					"x" : 21,
					"y" : 9 + 150,

					"default_image" : "icon/emoticons/kiss.tga",
					"over_image" : "icon/emoticons/kiss.tga",
					"down_image" : "icon/emoticons/kiss.tga",
				},
				
				{
					"name" : "emoticon_7",
					"type" : "button",

					"x" : 21,
					"y" : 9 + 175,

					"default_image" : "icon/emoticons/smiley.tga",
					"over_image" : "icon/emoticons/smiley.tga",
					"down_image" : "icon/emoticons/smiley.tga",
				},
			),
		},
		{
			"name" : "board",
			"type" : "thinboard",
			"style" : ("attach",),

			"x" : 0,
			"y" : 0,

			"width" : 280,
			"height" : 215,

			"children" :
			(
				## Title
				{
					"name" : "name_slot",
					"type" : "image",
					"style" : ("attach",),

					"x" : 0,
					"y" : 10,

					"image" : "d:/ymir work/ui/minigame/catchking/challenge_text_bg.png",
					
					"horizontal_align" : "center",

					"children" :
					(
						{
							"name" : "titlename",
							"type" : "text",

							"x" : 0,
							"y" : 4,

							"text" : uiScriptLocale.WHISPER_NAME,
							
							"horizontal_align" : "center",
							"text_horizontal_align" : "center",
						},
						{
							"name" : "titlename_edit",
							"type" : "editline",

							"x" : 0,
							"y" : 4,

							"width" : 120,
							"height" : 17,

							"input_limit" : 30,

							"text" : uiScriptLocale.WHISPER_NAME,
							
							"horizontal_align" : "center",
						},
					),
				},


				{
					"name" : "acceptbutton",
					"type" : "button",

					"x" : 0,
					"y" : 40,

					"default_image" : "d:/ymir work/ui/public/acceptbutton00.sub",
					"over_image" : "d:/ymir work/ui/public/acceptbutton01.sub",
					"down_image" : "d:/ymir work/ui/public/acceptbutton02.sub",
					"horizontal_align" : "center",
				},
				
				{
					"name" : "minimizebutton",
					"type" : "button",

					"x" : 280 - 41,
					"y" : 12,

					"tooltip_text" : uiScriptLocale.MINIMIZE,

					"default_image" : "d:/ymir work/ui/public/minimize_button_01.sub",
					"over_image" : "d:/ymir work/ui/public/minimize_button_02.sub",
					"down_image" : "d:/ymir work/ui/public/minimize_button_03.sub",
				},
				{
					"name" : "closebutton",
					"type" : "button",

					"x" : 280 - 24,
					"y" : 12,

					"tooltip_text" : uiScriptLocale.CLOSE,

					"default_image" : "d:/ymir work/ui/public/close_button_01.sub",
					"over_image" : "d:/ymir work/ui/public/close_button_02.sub",
					"down_image" : "d:/ymir work/ui/public/close_button_03.sub",
				},

				## ScrollBar
				{
					"name" : "scrollbar",
					"type" : "thin_scrollbar",

					"x" : 280 - 25,
					"y" : 35,

					"size" : 280 - 160,
				},

				## Edit Bar
				{
					"name" : "editbar",
					"type" : "bar",

					"x" : 10,
					"y" : 200 - 60,

					"width" : 280 - 18,
					"height" : 50,

					"color" : 0x77000000,

					"children" :
					(
						{
							"name" : "chatline",
							"type" : "editline",

							"x" : 5,
							"y" : 5,

							"width" : 280 - 70,
							"height" : 40,

							"with_codepage" : 1,
							"input_limit" : 40,
							"limit_width" : 280 - 90,
							"multi_line" : 1,
						},
						{
							"name" : "sendbutton",
							"type" : "button",

							"x" : 280 - 80,
							"y" : 10,

							"text" : uiScriptLocale.WHISPER_SEND,

							"default_image" : "d:/ymir work/ui/public/xlarge_thin_button_01.sub",
							"over_image" : "d:/ymir work/ui/public/xlarge_thin_button_02.sub",
							"down_image" : "d:/ymir work/ui/public/xlarge_thin_button_03.sub",
						},
					),
				},
			),
		},
	),
}
