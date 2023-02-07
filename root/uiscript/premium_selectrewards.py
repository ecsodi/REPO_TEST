import uiScriptLocale

window = {
	"name" : "PremiumSelectReward", "x" : 0, "y" : 0, "style" : ("movable", "float",), "width" : 350, "height" : 160,
	"children" :
	(
		{
			"name" : "Board", "type" : "board_with_titlebar", "x" : 0, "y" : 0, "width" : 350, "height" : 160, "title" : "Alege recompensa premium",
			"children" :
			(
				{ "name":"reward_1", "type":"image", "style" : ("attach",), "x" : 6, "y" : 40, "image" : "d:/ymir work/ui/game/premium_system/count_reward.tga", },
				{ "name":"reward_2", "type":"image", "style" : ("attach",), "x" : 6, "y" : 70, "image" : "d:/ymir work/ui/game/premium_system/count_reward.tga", },
				{ "name":"reward_3", "type":"image", "style" : ("attach",), "x" : 6, "y" : 100, "image" : "d:/ymir work/ui/game/premium_system/count_reward.tga", },

				{ "name":"line_1", "type":"image", "style" : ("attach",), "x" : 6, "y" : 40, "image" : "d:/ymir work/ui/game/premium_system/bar_.tga", },
				{ "name":"line_2", "type":"image", "style" : ("attach",), "x" : 6, "y" : 70, "image" : "d:/ymir work/ui/game/premium_system/bar_.tga", },
				{ "name":"line_3", "type":"image", "style" : ("attach",), "x" : 6, "y" : 100, "image" : "d:/ymir work/ui/game/premium_system/bar_.tga", },

				{ "name" : "count_1", "type" : "text", "x" : 32, "y" : 43, "text" : "1", },
				{ "name" : "count_2", "type" : "text", "x" : 32, "y" : 73, "text" : "2", },
				{ "name" : "count_3", "type" : "text", "x" : 32, "y" : 103, "text" : "3", },	
				
				{ "name" : "TextLine_1", "type" : "text", "x" : 60, "y" : 42, "text" : "", },
				{ "name" : "TextLine_2", "type" : "text", "x" : 60, "y" : 73, "text" : "", },
				{ "name" : "TextLine_3", "type" : "text", "x" : 60, "y" : 103, "text" : "", },
				{ "name" : "AcceptButton", "type" : "button", "x" : 145, "y" : 129, "text" : "", "default_image" : "d:/ymir work/ui/game/premium_system/acceptbutton00.tga", "over_image" : "d:/ymir work/ui/game/premium_system/acceptbutton01.tga", "down_image" : "d:/ymir work/ui/game/premium_system/acceptbutton02.tga",
				},
			),
		},
	),
}