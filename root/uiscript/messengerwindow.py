import uiScriptLocale

BUTTON_START_X_POS = -60
BUTTON_X_STEP = 30

window = {
	"name" : "MessengerWindow",

	"x" : SCREEN_WIDTH - 200 - 33,
	"y" : SCREEN_HEIGHT - 400 - 50,

	"style" : ("movable", "float", "animation",),

	"width" : 170 + 33,
	"height" : 300,

	"children" :
	(

		{
			"name" : "board",
			"type" : "board_with_titlebar",

			"x" : 0,
			"y" : 0,

			"width" : 170 + 33,
			"height" : 300,
			"title" : uiScriptLocale.MESSENGER_TITLE,
		},
		{
			"name" : "Board_Name",
			"type" : "border_new",
		
			"x" : 10,
			"y" : 256,
			
			"width" : 172,
			"height" : 30,
		},
		{
			"name" : "Board_Name2",
			"type" : "border_new",
		
			"x" : 10,
			"y" : 31,
			
			"width" : 172,
			"height" : 220,
		},
		{
			"name" : "AddFriendButton",
			"type" : "button",

			"x" : BUTTON_START_X_POS + BUTTON_X_STEP*0+40,
			"y" : 50,
			"horizontal_align" : "center",
			"vertical_align" : "bottom",
			"tooltip_text" : uiScriptLocale.MESSENGER_ADD_FRIEND,
			"tooltip_x" : 0,
			"tooltip_y" : 35,

			"default_image" : "d:/ymir work/ui/game/comp/mes/add_friend.png",
			"over_image" : "d:/ymir work/ui/game/comp/mes/add_friend_over.png",
			"down_image" : "d:/ymir work/ui/game/comp/mes/add_friend.png",
			"disable_image" : "d:/ymir work/ui/game/comp/mes/add_friend_disable.png",
		},
		{
			"name" : "WhisperButton",
			"type" : "button",

			"x" : BUTTON_START_X_POS + BUTTON_X_STEP*1+40,
			"y" : 50,
			"horizontal_align" : "center",
			"vertical_align" : "bottom",
			"tooltip_text" : uiScriptLocale.MESSENGER_WHISPER,
			"tooltip_x" : 0,
			"tooltip_y" : 35,

			"default_image" : "d:/ymir work/ui/game/comp/mes/write_pm.png",
			"over_image" : "d:/ymir work/ui/game/comp/mes/write_pm_over.png",
			"down_image" : "d:/ymir work/ui/game/comp/mes/write_pm.png",
			"disable_image" : "d:/ymir work/ui/game/comp/mes/write_pm_disable.png",
		},
		{
			"name" : "RemoveButton",
			"type" : "button",

			"x" : BUTTON_START_X_POS + BUTTON_X_STEP*3+40,
			"y" : 50,
			"horizontal_align" : "center",
			"vertical_align" : "bottom",
			"tooltip_text" : uiScriptLocale.MESSENGER_DELETE_FRIEND,
			"tooltip_x" : 0,
			"tooltip_y" : 35,
			
			"default_image" : "d:/ymir work/ui/game/comp/mes/delete_friend.png",
			"over_image" : "d:/ymir work/ui/game/comp/mes/delete_friend_over.png",
			"down_image" : "d:/ymir work/ui/game/comp/mes/delete_friend.png",
			"disable_image" : "d:/ymir work/ui/game/comp/mes/delete_friend_disable.png",
		},
		{
			"name" : "GuildButton",
			"type" : "button",

			"x" : BUTTON_START_X_POS + BUTTON_X_STEP*4+40,
			"y" : 50,
			"horizontal_align" : "center",
			"vertical_align" : "bottom",
			"tooltip_text" : uiScriptLocale.MESSENGER_OPEN_GUILD,
			"tooltip_x" : 0,
			"tooltip_y" : 35,
			"default_image" : "d:/ymir work/ui/game/comp/mes/write_pm.png",
			"over_image" : "d:/ymir work/ui/game/comp/mes/write_pm_over.png",
			"down_image" : "d:/ymir work/ui/game/comp/mes/write_pm.png",
			"disable_image" : "d:/ymir work/ui/game/comp/mes/write_pm_disable.png",
		},

	), ## end of main window
}
