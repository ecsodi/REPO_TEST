import uiScriptLocale
ROOT = "d:/ymir work/ui/public/"

window = {
	"name" : "SystemDialog",
	"style" : ("float","animation",),
	"x" : (SCREEN_WIDTH  - 200) /2,
	"y" : (SCREEN_HEIGHT - 288) /2,
	"width" : 200,
	"height" : 178+ 59,
	"children" :
	(
		{
			"name" : "board",
			"type" : "thinboard",
			"x" : 0,
			"y" : 0,
			"width" : 200,
			"height" : 178+ 59,
			"children" :
			(
				{
					"name" : "wikipedia_button",
					"type" : "button",
					"x" : 10,
					"y" : 17,
					"text" : "|Ed:/ymir work/ui/wiki/wikibutton_small.tga|e Deimos Wikipedia",
					"default_image" : ROOT + "XLarge_Button_01.sub",
					"over_image" : ROOT + "XLarge_Button_02.sub",
					"down_image" : ROOT + "XLarge_Button_03.sub",
				},
				{
					"name" : "system_option_button",
					"type" : "button",
					"x" : 10,
					"y" : 47,
					"text" : uiScriptLocale.SYSTEMOPTION_TITLE,
					"default_image" : ROOT + "XLarge_Button_01.sub",
					"over_image" : ROOT + "XLarge_Button_02.sub",
					"down_image" : ROOT + "XLarge_Button_03.sub",
				},
				{
					"name" : "change_button",
					"type" : "button",
					"x" : 10,
					"y" : 47 + 30,
					"text" : uiScriptLocale.SYSTEM_CHANGE,
					"default_image" : ROOT + "XLarge_Button_01.sub",
					"over_image" : ROOT + "XLarge_Button_02.sub",
					"down_image" : ROOT + "XLarge_Button_03.sub",
				},
				{
					"name" : "logout_button",
					"type" : "button",
					"x" : 10,
					"y" : 47 + (30 *2),
					"text" : uiScriptLocale.SYSTEM_LOGOUT,
					"default_image" : ROOT + "XLarge_Button_01.sub",
					"over_image" : ROOT + "XLarge_Button_02.sub",
					"down_image" : ROOT + "XLarge_Button_03.sub",
				},
				{
					"name" : "exit_button",
					"type" : "button",
					"x" : 10,
					"y" : 47 + (30 *3),
					"text" : uiScriptLocale.SYSTEM_EXIT,
					"default_image" : ROOT + "XLarge_Button_01.sub",
					"over_image" : ROOT + "XLarge_Button_02.sub",
					"down_image" : ROOT + "XLarge_Button_03.sub",
				},
                {
                    "name" : "change_ch_button",
                    "type" : "button",

                    "x" : 10,
                    "y" : 47 + (30 * 4),

                    "text" : "Schimbare Canal",

                    "default_image" : ROOT + "XLarge_Button_01.sub",
                    "over_image" : ROOT + "XLarge_Button_02.sub",
                    "down_image" : ROOT + "XLarge_Button_03.sub",
                    "disable_image" : ROOT + "XLarge_Button_03.sub",
                },
				{
					"name" : "cancel_button",
					"type" : "button",
					"x" : 10,
					"y" : 47 + (30 *5),
					"text" : uiScriptLocale.CANCEL,
					"default_image" : ROOT + "XLarge_Button_01.sub",
					"over_image" : ROOT + "XLarge_Button_02.sub",
					"down_image" : ROOT + "XLarge_Button_03.sub",
				},
			),
		},
	),
}

