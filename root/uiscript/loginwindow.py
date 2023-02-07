import uiScriptLocale

SERVER_BOARD_HEIGHT = 220 + 180
SERVER_LIST_HEIGHT = 171 + 180
SERVER_BOARD_WEIGHT = 375 

ID_LIMIT_COUNT = 19
PW_LIMIT_COUNT = 16

PATH_REWORK = "d:/ymir work/ui/game/login_rework/"


NEW_PATH = "d:/ymir work/ui/game/new_login/"
NEW_LOGIN_PATH = "d:/ymir work/ui/game/new_login/login/"
NEW_LOGIN_ACCOUNT_PATH = "d:/ymir work/ui/game/new_login/account/"
NEW_LOGIN_CHANNELS_PATH = "d:/ymir work/ui/game/new_login/channels/"
NEW_LOGIN_FLAGS_PATH = "d:/ymir work/ui/game/new_login/flags/"

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
			"name" : "bg1", "type" : "expanded_image", "x" : 0, "y" : 0,
			"x_scale" : float(SCREEN_WIDTH) / 1920.0, "y_scale" : float(SCREEN_HEIGHT) / 1080.0,
			"image" : PATH_REWORK + "bg.png",
		},
		{
			"name" : "LoginExitButton",
			"type" : "button",
	
			"x" : SCREEN_WIDTH - 45,
			"y" : 20,
	
			"default_image" : PATH_REWORK + "leave_1.png",
			"over_image" : PATH_REWORK + "leave_2.png",
			"down_image" : PATH_REWORK + "leave_3.png",
		},
		
		## LoginBoard
		{
			"name" : "LoginBoard",
			"type" : "image",

			"x" : 0, 
			"y" : 100,
			
			"vertical_align" : "center",
			"horizontal_align" : "center",
			
			"image" : PATH_REWORK + "login_panel.png",

			"children" :
			(
				{
					"name" : "ID_EditLine_Back",
					"type" : "image",
					
					"vertical_align" : "center",
					"horizontal_align" : "center",
					
					"x" : 0,
					"y" : -75,

					"image" : PATH_REWORK + "placeholder_login.png",
					
					"children" :
					(
						{
							"name" : "ID_EditLine",
							"type" : "editline_new",
							"info_msg":"Username",

							"x" : 35,
							"y" : 10,
			
							"width" : 225,
							"height" : 29,
			
							"input_limit" : ID_LIMIT_COUNT,
							"enable_codepage" : 0,
			
							"r" : 0.996,
							"g" : 0.804,
							"b" : 0.643,
							"a" : 1.0,
						},
					),
				},
				{
					"name" : "Password_EditLine_Back",
					"type" : "image",

					"x" : 0,
					"y" : -25,
					
					"vertical_align" : "center",
					"horizontal_align" : "center",
					
					"image" : PATH_REWORK + "placeholder_pw.png",
					
					"children" :
					(
						{
							"name" : "Password_EditLine",
							"type" : "editline_new",
							"info_msg":"Password",

							"x" : 35,
							"y" : 10,
		
							"width" : 225,
							"height" : 29,
		
							"input_limit" : PW_LIMIT_COUNT,
							"secret_flag" : 1,
							"enable_codepage" : 0,
							
							"r" : 0.996,
							"g" : 0.804,
							"b" : 0.643,
							"a" : 1.0,
						},
					),
				},
				{
					"name" : "SaveAccountButton",
					"type" : "button",

					"x" : -110,
					"y" : 20,
					
					"vertical_align" : "center",
					"horizontal_align" : "center",

					"default_image" : PATH_REWORK + "save_1.png",
					"over_image" : PATH_REWORK + "save_2.png",
					"down_image" : PATH_REWORK + "save_1.png",
					
					"children" :
					(
						{
							"name" : "TextLineSave",
							"type" : "text",

							"x" : 23,
							"y" : 0,
							
							"r" : 0.996,
							"g" : 0.804,
							"b" : 0.643,
							"a" : 1.0,
							
							"text" : uiScriptLocale.SAVE_ACCOUNT,

						},
					),
				},
				{
					"name" : "LoginButton",
					"type" : "button",

					"x" : 0,
					"y" : 70,
					
					"vertical_align" : "center",
					"horizontal_align" : "center",
					
					"default_image" : PATH_REWORK + "login_button1.png",
					"over_image" : PATH_REWORK + "login_button2.png",
					"down_image" : PATH_REWORK + "login_button3.png",
				},
				
				{
					"name" : "RegButton",
					"type" : "button",
					"x" : 0, "y": 115,
					
					"default_image" : PATH_REWORK + "register_norm.png",
					"over_image" : PATH_REWORK + "register_over.png",
					"down_image" : PATH_REWORK + "register_norm.png",
					
					"vertical_align" : "center",
					"horizontal_align" : "center",
				},
								
				{
					"name" : "CommButton",
					"type" : "button",
					"x" : 0, "y": 127,
					"default_image" : PATH_REWORK + "comunitate_norm.png",
					"over_image" : PATH_REWORK + "comunitate_over.png",
					"down_image" : PATH_REWORK + "comunitate_norm.png",
					"vertical_align" : "center",
					"horizontal_align" : "center",
				},
				
			),
		},

		## AccountBoard
		{
			"name" : "AccountBoard",
			"type" : "image",

			"x" : -368, 
			"y" : 119,

			"vertical_align" : "center",
			"horizontal_align" : "center",
			
			"image" : PATH_REWORK + "account_panel.png",

			"children" :
			(
				{
					"name" : "SlotLine1_Button",
					"type" : "button",
					
					"x" : 0, "y": -75,

					"default_image" : PATH_REWORK + "account_placeholder.png",
					"over_image" : PATH_REWORK + "account_placeholder_over.png",
					"down_image" : PATH_REWORK + "account_placeholder.png",
					
					"vertical_align" : "center",
					"horizontal_align" : "center",
					
					"children" :
					(
						{
							"name" : "SlotLine1_Text",
							"type" : "text",
		
							"x" : 0,
							"y" : 0,
							
							"text" : uiScriptLocale.ACCOUNT_SAVED,
							
							"all_align" : 1,
						},
						{
							"name" : "SlotLine1_Button_Delete",
							"type" : "button",
							"x" : 110, "y": 0,
							
							"vertical_align" : "center",
							"horizontal_align" : "center",
							
							"default_image" : PATH_REWORK +  "delete_1.png",
							"over_image" : PATH_REWORK +  "delete_2.png",
							"down_image" : PATH_REWORK +  "delete_1.png",
						},
					),
				},	
				{
					"name" : "SlotLine2_Button",
					"type" : "button",
					
					"x" : 0, "y": -40,

					"default_image" : PATH_REWORK + "account_placeholder.png",
					"over_image" : PATH_REWORK + "account_placeholder_over.png",
					"down_image" : PATH_REWORK + "account_placeholder.png",
					
					"vertical_align" : "center",
					"horizontal_align" : "center",
					
					"children" :
					(
						{
							"name" : "SlotLine2_Text",
							"type" : "text",
		
							"x" : 0,
							"y" : 0,
							
							"text" : uiScriptLocale.ACCOUNT_SAVED,
							
							"all_align" : 1,
						},
						{
							"name" : "SlotLine2_Button_Delete",
							"type" : "button",
							"x" : 110, "y": 0,							
							"vertical_align" : "center",
							"horizontal_align" : "center",
							
							"default_image" : PATH_REWORK +  "delete_1.png",
							"over_image" : PATH_REWORK +  "delete_2.png",
							"down_image" : PATH_REWORK +  "delete_1.png",
						},
					),
				},	
				{
					"name" : "SlotLine3_Button",
					"type" : "button",
					
					"x" : 0, "y": -5,

					"default_image" : PATH_REWORK + "account_placeholder.png",
					"over_image" : PATH_REWORK + "account_placeholder_over.png",
					"down_image" : PATH_REWORK + "account_placeholder.png",
					
					"vertical_align" : "center",
					"horizontal_align" : "center",
					
					"children" :
					(
						{
							"name" : "SlotLine3_Text",
							"type" : "text",
		
							"x" : 0,
							"y" : 0,
							
							"text" : uiScriptLocale.ACCOUNT_SAVED,
							
							"all_align" : 1,
						},
						{
							"name" : "SlotLine3_Button_Delete",
							"type" : "button",
							"x" : 110, "y": 0,							
							"vertical_align" : "center",
							"horizontal_align" : "center",
							
							"default_image" : PATH_REWORK +  "delete_1.png",
							"over_image" : PATH_REWORK +  "delete_2.png",
							"down_image" : PATH_REWORK +  "delete_1.png",
						},
					),
				},
				{
					"name" : "SlotLine4_Button",
					"type" : "button",
					
					"x" : 0, "y": 30,

					"default_image" : PATH_REWORK + "account_placeholder.png",
					"over_image" : PATH_REWORK + "account_placeholder_over.png",
					"down_image" : PATH_REWORK + "account_placeholder.png",
					
					"vertical_align" : "center",
					"horizontal_align" : "center",
					
					"children" :
					(
						{
							"name" : "SlotLine4_Text",
							"type" : "text",
		
							"x" : 0,
							"y" : 0,
							
							"text" : uiScriptLocale.ACCOUNT_SAVED,
							
							"all_align" : 1,
						},
						{
							"name" : "SlotLine4_Button_Delete",
							"type" : "button",
							"x" : 110, "y": 0,							
							"vertical_align" : "center",
							"horizontal_align" : "center",
							
							"default_image" : PATH_REWORK +  "delete_1.png",
							"over_image" : PATH_REWORK +  "delete_2.png",
							"down_image" : PATH_REWORK +  "delete_1.png",
						},
					),
				},	
				{
					"name" : "SlotLine5_Button",
					"type" : "button",
					
					"x" : 0, "y": 65,

					"default_image" : PATH_REWORK + "account_placeholder.png",
					"over_image" : PATH_REWORK + "account_placeholder_over.png",
					"down_image" : PATH_REWORK + "account_placeholder.png",
					
					"vertical_align" : "center",
					"horizontal_align" : "center",
					
					"children" :
					(
						{
							"name" : "SlotLine5_Text",
							"type" : "text",
		
							"x" : 0,
							"y" : 0,
							
							"text" : uiScriptLocale.ACCOUNT_SAVED,
							
							"all_align" : 1,
						},
						{
							"name" : "SlotLine5_Button_Delete",
							"type" : "button",
							"x" : 110, "y": 0,							
							"vertical_align" : "center",
							"horizontal_align" : "center",
							
							"default_image" : PATH_REWORK +  "delete_1.png",
							"over_image" : PATH_REWORK +  "delete_2.png",
							"down_image" : PATH_REWORK +  "delete_1.png",
						},
					),
				},	
				{
					"name" : "SlotLine6_Button",
					"type" : "button",
					
					"x" : 0, "y": 100,

					"default_image" : PATH_REWORK + "account_placeholder.png",
					"over_image" : PATH_REWORK + "account_placeholder_over.png",
					"down_image" : PATH_REWORK + "account_placeholder.png",
					
					"vertical_align" : "center",
					"horizontal_align" : "center",
					
					"children" :
					(
						{
							"name" : "SlotLine6_Text",
							"type" : "text",
		
							"x" : 0,
							"y" : 0,
							
							"text" : uiScriptLocale.ACCOUNT_SAVED,
							
							"all_align" : 1,
						},
						{
							"name" : "SlotLine6_Button_Delete",
							"type" : "button",
							"x" : 110, "y": 0,							
							"vertical_align" : "center",
							"horizontal_align" : "center",
							
							"default_image" : PATH_REWORK +  "delete_1.png",
							"over_image" : PATH_REWORK +  "delete_2.png",
							"down_image" : PATH_REWORK +  "delete_1.png",
						},
					),
				},	
			),
		},
		

		## AccountBoard
		{
			"name" : "ChannelBoard",
			"type" : "image",

			"x" : 365, 
			"y" : 119,

			"vertical_align" : "center",
			"horizontal_align" : "center",
			
			"image" : PATH_REWORK + "select_channel.png",

			"children" :
			(
				{
					"name" : "Ch1Button",
					"type" : "button",

					"x" : 0, "y": -75,

					"default_image" : PATH_REWORK + "canal1.png",
					"over_image" : PATH_REWORK + "canal1_1.png",
					"down_image" : PATH_REWORK + "canal1.png",

					"vertical_align" : "center",
					"horizontal_align" : "center",
					"children" :
					(
						{
							"name" : "on_ch1_img",
							"type" : "image",

							"x" : 130, "y": 0,							
							"vertical_align" : "center",
							"horizontal_align" : "center",
							
							"image" : NEW_PATH + "channel_off.png",
						},
					),
				},
				{
					"name" : "Ch2Button",
					"type" : "button",

					"x" : 0, "y": -40,

					"default_image" : PATH_REWORK + "canal2.png",
					"over_image" : PATH_REWORK + "canal2_1.png",
					"down_image" : PATH_REWORK + "canal2.png",

					"vertical_align" : "center",
					"horizontal_align" : "center",
					"children" :
					(
						{
							"name" : "on_ch2_img",
							"type" : "image",

							"x" : 130, "y": 0,							
							"vertical_align" : "center",
							"horizontal_align" : "center",
							
							"image" : NEW_PATH + "channel_off.png",
						},
					),
				},
				{
					"name" : "Ch3Button",
					"type" : "button",

					"x" : 0, "y": -5,

					"default_image" : PATH_REWORK + "canal3.png",
					"over_image" : PATH_REWORK + "canal3_1.png",
					"down_image" : PATH_REWORK + "canal3.png",

					"vertical_align" : "center",
					"horizontal_align" : "center",
					"children" :
					(
						{
							"name" : "on_ch3_img",
							"type" : "image",

							"x" : 130, "y": 0,							
							"vertical_align" : "center",
							"horizontal_align" : "center",
							
							"image" : NEW_PATH + "channel_off.png",
						},
					),
				},
				{
					"name" : "Ch4Button",
					"type" : "button",

					"x" : 0, "y": 30,

					"default_image" : PATH_REWORK + "canal4.png",
					"over_image" : PATH_REWORK + "canal4_1.png",
					"down_image" : PATH_REWORK + "canal4.png",

					"vertical_align" : "center",
					"horizontal_align" : "center",
					"children" :
					(
						{
							"name" : "on_ch4_img",
							"type" : "image",

							"x" : 130, "y": 0,							
							"vertical_align" : "center",
							"horizontal_align" : "center",
							
							"image" : NEW_PATH + "channel_off.png",
						},
					),
				},
				{
					"name" : "Ch5Button",
					"type" : "button",

					"x" : 0, "y": 65,
					
					"default_image" : PATH_REWORK + "canal5.png",
					"over_image" : PATH_REWORK + "canal5_1.png",
					"down_image" : PATH_REWORK + "canal5.png",

					"vertical_align" : "center",
					"horizontal_align" : "center",
					"children" :
					(
						{
							"name" : "on_ch5_img",
							"type" : "image",

							"x" : 130, "y": 0,							
							"vertical_align" : "center",
							"horizontal_align" : "center",
							
							"image" : NEW_PATH + "channel_off.png",
						},
					),
				},
				{
					"name" : "Ch6Button",
					"type" : "button",

					"x" : 0, "y": 100,

					"default_image" : PATH_REWORK + "canal6.png",
					"over_image" : PATH_REWORK + "canal6_1.png",
					"down_image" : PATH_REWORK + "canal6.png",

					"vertical_align" : "center",
					"horizontal_align" : "center",
					"children" :
					(
						{
							"name" : "on_ch6_img",
							"type" : "image",

							"x" : 130, "y": 0,							
							"vertical_align" : "center",
							"horizontal_align" : "center",
							
							"image" : NEW_PATH + "channel_off.png",
						},
					),
				},

			),
		},
		
		
	),
}
