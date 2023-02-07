import uiScriptLocale
import app

ROOT = "d:/ymir work/ui/game/"

LOCALE_PATH = "locale/"

Y_ADD_POSITION = 0

window = {
	"name" : "TaskBar",

	"x" : 0,
	"y" : SCREEN_HEIGHT - 37,

	"width" : SCREEN_WIDTH,
	"height" : 37,

	"children" :
	(
		## Board
		{
			"name" : "Base_Board_01",
			"type" : "expanded_image",

			"x" : 263,
			"y" : 0,

			"rect" : (0.0, 0.0, float(SCREEN_WIDTH - 263 - 256) / 256.0, 0.0),

			"image" : "d:/ymir work/ui/game/normal_interface/TaskBar_Base.tga"
		},

		## Gauge
		{
			"name" : "Gauge_Board",
			"type" : "image",

			"x" : 0,
			"y" : -10 + Y_ADD_POSITION,

			"image" : ROOT + "TaskBar_Norm/gauge.sub",

			"children" :
			(
				{
					"name" : "RampageGauge",
					"type" : "ani_image",

					"x" : 8,
					"y" : 4,
					"width"  : 40,
					"height" : 40,

					"delay" : 6,
					## icon_name
					"images" :
					(
						LOCALE_PATH + "ui/Mall/eye_green_0000.sub",
						LOCALE_PATH + "ui/Mall/eye_green_0001.sub",
						LOCALE_PATH + "ui/Mall/eye_green_0002.sub",
						LOCALE_PATH + "ui/Mall/eye_green_0003.sub",
						LOCALE_PATH + "ui/Mall/eye_green_0004.sub",
						LOCALE_PATH + "ui/Mall/eye_green_0005.sub",
						LOCALE_PATH + "ui/Mall/eye_green_0006.sub",
						LOCALE_PATH + "ui/Mall/eye_green_0007.sub",
						LOCALE_PATH + "ui/Mall/eye_green_0008.sub",
						LOCALE_PATH + "ui/Mall/eye_green_0009.sub",
						LOCALE_PATH + "ui/Mall/eye_green_0011.sub",
						LOCALE_PATH + "ui/Mall/eye_green_0012.sub",
						LOCALE_PATH + "ui/Mall/eye_green_0013.sub",
						LOCALE_PATH + "ui/Mall/eye_green_0014.sub",
						LOCALE_PATH + "ui/Mall/eye_green_0015.sub",
						LOCALE_PATH + "ui/Mall/eye_green_0016.sub",
						LOCALE_PATH + "ui/Mall/eye_green_0015.sub",
						LOCALE_PATH + "ui/Mall/eye_green_0014.sub",
						LOCALE_PATH + "ui/Mall/eye_green_0013.sub",
						LOCALE_PATH + "ui/Mall/eye_green_0012.sub",
						LOCALE_PATH + "ui/Mall/eye_green_0011.sub",
						LOCALE_PATH + "ui/Mall/eye_green_0010.sub",
						LOCALE_PATH + "ui/Mall/eye_green_0009.sub",
						LOCALE_PATH + "ui/Mall/eye_green_0008.sub",
						LOCALE_PATH + "ui/Mall/eye_green_0007.sub",
						LOCALE_PATH + "ui/Mall/eye_green_0006.sub",
						LOCALE_PATH + "ui/Mall/eye_green_0005.sub",
						LOCALE_PATH + "ui/Mall/eye_green_0004.sub",
						LOCALE_PATH + "ui/Mall/eye_green_0003.sub",
						LOCALE_PATH + "ui/Mall/eye_green_0002.sub",
						LOCALE_PATH + "ui/Mall/eye_green_0001.sub",
					)
				},
				{
					"name" : "RampageGauge2",
					"type" : "ani_image",

					"x" : 8,
					"y" : 4,
					"width"  : 40,
					"height" : 40,

					"delay" : 6,
					## icon_name
					"images" :
					(
						LOCALE_PATH + "ui/Mall/eye_green_0000.sub",
						LOCALE_PATH + "ui/Mall/eye_green_0001.sub",
						LOCALE_PATH + "ui/Mall/eye_green_0002.sub",
						LOCALE_PATH + "ui/Mall/eye_green_0003.sub",
						LOCALE_PATH + "ui/Mall/eye_green_0004.sub",
						LOCALE_PATH + "ui/Mall/eye_green_0005.sub",
						LOCALE_PATH + "ui/Mall/eye_green_0006.sub",
						LOCALE_PATH + "ui/Mall/eye_green_0007.sub",
						LOCALE_PATH + "ui/Mall/eye_green_0008.sub",
						LOCALE_PATH + "ui/Mall/eye_green_0009.sub",
						LOCALE_PATH + "ui/Mall/eye_green_0011.sub",
						LOCALE_PATH + "ui/Mall/eye_green_0012.sub",
						LOCALE_PATH + "ui/Mall/eye_green_0013.sub",
						LOCALE_PATH + "ui/Mall/eye_green_0014.sub",
						LOCALE_PATH + "ui/Mall/eye_green_0015.sub",
						LOCALE_PATH + "ui/Mall/eye_green_0016.sub",
						LOCALE_PATH + "ui/Mall/eye_green_0015.sub",
						LOCALE_PATH + "ui/Mall/eye_green_0014.sub",
						LOCALE_PATH + "ui/Mall/eye_green_0013.sub",
						LOCALE_PATH + "ui/Mall/eye_green_0012.sub",
						LOCALE_PATH + "ui/Mall/eye_green_0011.sub",
						LOCALE_PATH + "ui/Mall/eye_green_0010.sub",
						LOCALE_PATH + "ui/Mall/eye_green_0009.sub",
						LOCALE_PATH + "ui/Mall/eye_green_0008.sub",
						LOCALE_PATH + "ui/Mall/eye_green_0007.sub",
						LOCALE_PATH + "ui/Mall/eye_green_0006.sub",
						LOCALE_PATH + "ui/Mall/eye_green_0005.sub",
						LOCALE_PATH + "ui/Mall/eye_green_0004.sub",
						LOCALE_PATH + "ui/Mall/eye_green_0003.sub",
						LOCALE_PATH + "ui/Mall/eye_green_0002.sub",
						LOCALE_PATH + "ui/Mall/eye_green_0001.sub",
					)
				},				
				{
					"name" : "RampageGauge3",
					"type" : "ani_image",

					"x" : 8,
					"y" : 4,
					"width"  : 40,
					"height" : 40,

					"delay" : 10,
					"images" :
					(
						LOCALE_PATH + "ui/Mall/eye_red_0000.sub",
						LOCALE_PATH + "ui/Mall/eye_red_0001.sub",
						LOCALE_PATH + "ui/Mall/eye_red_0002.sub",
						LOCALE_PATH + "ui/Mall/eye_red_0003.sub",
						LOCALE_PATH + "ui/Mall/eye_red_0004.sub",
						LOCALE_PATH + "ui/Mall/eye_red_0005.sub",
						LOCALE_PATH + "ui/Mall/eye_red_0006.sub",
						LOCALE_PATH + "ui/Mall/eye_red_0007.sub",
						LOCALE_PATH + "ui/Mall/eye_red_0008.sub",
						LOCALE_PATH + "ui/Mall/eye_red_0009.sub",
						LOCALE_PATH + "ui/Mall/eye_red_0011.sub",
						LOCALE_PATH + "ui/Mall/eye_red_0012.sub",
						LOCALE_PATH + "ui/Mall/eye_red_0013.sub",
						LOCALE_PATH + "ui/Mall/eye_red_0014.sub",
						LOCALE_PATH + "ui/Mall/eye_red_0015.sub",
						LOCALE_PATH + "ui/Mall/eye_red_0016.sub",
						LOCALE_PATH + "ui/Mall/eye_red_0015.sub",
						LOCALE_PATH + "ui/Mall/eye_red_0014.sub",
						LOCALE_PATH + "ui/Mall/eye_red_0013.sub",
						LOCALE_PATH + "ui/Mall/eye_red_0012.sub",
						LOCALE_PATH + "ui/Mall/eye_red_0011.sub",
						LOCALE_PATH + "ui/Mall/eye_red_0010.sub",
						LOCALE_PATH + "ui/Mall/eye_red_0009.sub",
						LOCALE_PATH + "ui/Mall/eye_red_0008.sub",
						LOCALE_PATH + "ui/Mall/eye_red_0007.sub",
						LOCALE_PATH + "ui/Mall/eye_red_0006.sub",
						LOCALE_PATH + "ui/Mall/eye_red_0005.sub",
						LOCALE_PATH + "ui/Mall/eye_red_0004.sub",
						LOCALE_PATH + "ui/Mall/eye_red_0003.sub",
						LOCALE_PATH + "ui/Mall/eye_red_0002.sub",
						LOCALE_PATH + "ui/Mall/eye_red_0001.sub",
					)
				},
				{
					"name" : "RampageGauge4",
					"type" : "ani_image",

					"x" : 8,
					"y" : 4,
					"width"  : 40,
					"height" : 40,

					"delay" : 10,
					"images" :
					(
						LOCALE_PATH + "ui/Mall/eye_red_0000.sub",
						LOCALE_PATH + "ui/Mall/eye_red_0001.sub",
						LOCALE_PATH + "ui/Mall/eye_red_0002.sub",
						LOCALE_PATH + "ui/Mall/eye_red_0003.sub",
						LOCALE_PATH + "ui/Mall/eye_red_0004.sub",
						LOCALE_PATH + "ui/Mall/eye_red_0005.sub",
						LOCALE_PATH + "ui/Mall/eye_red_0006.sub",
						LOCALE_PATH + "ui/Mall/eye_red_0007.sub",
						LOCALE_PATH + "ui/Mall/eye_red_0008.sub",
						LOCALE_PATH + "ui/Mall/eye_red_0009.sub",
						LOCALE_PATH + "ui/Mall/eye_red_0011.sub",
						LOCALE_PATH + "ui/Mall/eye_red_0012.sub",
						LOCALE_PATH + "ui/Mall/eye_red_0013.sub",
						LOCALE_PATH + "ui/Mall/eye_red_0014.sub",
						LOCALE_PATH + "ui/Mall/eye_red_0015.sub",
						LOCALE_PATH + "ui/Mall/eye_red_0016.sub",
						LOCALE_PATH + "ui/Mall/eye_red_0015.sub",
						LOCALE_PATH + "ui/Mall/eye_red_0014.sub",
						LOCALE_PATH + "ui/Mall/eye_red_0013.sub",
						LOCALE_PATH + "ui/Mall/eye_red_0012.sub",
						LOCALE_PATH + "ui/Mall/eye_red_0011.sub",
						LOCALE_PATH + "ui/Mall/eye_red_0010.sub",
						LOCALE_PATH + "ui/Mall/eye_red_0009.sub",
						LOCALE_PATH + "ui/Mall/eye_red_0008.sub",
						LOCALE_PATH + "ui/Mall/eye_red_0007.sub",
						LOCALE_PATH + "ui/Mall/eye_red_0006.sub",
						LOCALE_PATH + "ui/Mall/eye_red_0005.sub",
						LOCALE_PATH + "ui/Mall/eye_red_0004.sub",
						LOCALE_PATH + "ui/Mall/eye_red_0003.sub",
						LOCALE_PATH + "ui/Mall/eye_red_0002.sub",
						LOCALE_PATH + "ui/Mall/eye_red_0001.sub",
					)
				},
				
				{
					## ??? ??? ?? ???
					"name" : "HPGauge_Board",
					"type" : "window",

					"x" : 59,
					"y" : 14,

					"width" : 95,
					"height" : 11,

					"children" :
					(
						{
							"name" : "HPRecoveryGaugeBar",
							"type" : "bar",

							"x" : 0,
							"y" : 0,
							"width" : 95,
							"height" : 13,
							"color" : 0x55ff0000,
						},
						{
							"name" : "HPGauge",
							"type" : "ani_image",

							"x" : 0,
							"y" : 0,

							"delay" : 6,

							"images" :
							(
								"D:/Ymir Work/UI/Pattern/HPGauge/01.tga",
								"D:/Ymir Work/UI/Pattern/HPGauge/02.tga",
								"D:/Ymir Work/UI/Pattern/HPGauge/03.tga",
								"D:/Ymir Work/UI/Pattern/HPGauge/04.tga",
								"D:/Ymir Work/UI/Pattern/HPGauge/05.tga",
								"D:/Ymir Work/UI/Pattern/HPGauge/06.tga",
								"D:/Ymir Work/UI/Pattern/HPGauge/07.tga",
							),
						},	
					),
				},
				{
					"name" : "SPGauge_Board",
					"type" : "window",

					"x" : 59,
					"y" : 24,

					"width" : 95,
					"height" : 11,

					"children" :
					(
						{
							"name" : "SPRecoveryGaugeBar",
							"type" : "bar",

							"x" : 0,
							"y" : 0,
							"width" : 95,
							"height" : 13,
							"color" : 0x550000ff,
						},
						{
							"name" : "SPGauge",
							"type" : "ani_image",

							"x" : 0,
							"y" : 0,

							"delay" : 6,

							"images" :
							(
								"D:/Ymir Work/UI/Pattern/SPGauge/01.tga",
								"D:/Ymir Work/UI/Pattern/SPGauge/02.tga",
								"D:/Ymir Work/UI/Pattern/SPGauge/03.tga",
								"D:/Ymir Work/UI/Pattern/SPGauge/04.tga",
								"D:/Ymir Work/UI/Pattern/SPGauge/05.tga",
								"D:/Ymir Work/UI/Pattern/SPGauge/06.tga",
								"D:/Ymir Work/UI/Pattern/SPGauge/07.tga",
							),
						},
					),
				},
				{
					"name" : "STGauge_Board",
					"type" : "window",

					"x" : 59,
					"y" : 38,

					"width" : 95,
					"height" : 6,

					"children" :
					(
						{
							"name" : "STGauge",
							"type" : "ani_image",

							"x" : 0,
							"y" : 0,

							"delay" : 6,

							"images" :
							(
								"D:/Ymir Work/UI/Pattern/STGauge/01.tga",
								"D:/Ymir Work/UI/Pattern/STGauge/02.tga",
								"D:/Ymir Work/UI/Pattern/STGauge/03.tga",
								"D:/Ymir Work/UI/Pattern/STGauge/04.tga",
								"D:/Ymir Work/UI/Pattern/STGauge/05.tga",
								"D:/Ymir Work/UI/Pattern/STGauge/06.tga",
								"D:/Ymir Work/UI/Pattern/STGauge/07.tga",
							),
						},
					),
				},

			),
		},
		{
			"name" : "EXP_Gauge_Board",
			"type" : "image",

			"x" : 158,
			"y" : 0 + Y_ADD_POSITION,

			"image" : ROOT + "TaskBar_Norm/exp_gauge.sub",

			"children" :
			(
				{
					"name" : "EXPGauge_01",
					"type" : "expanded_image",

					"x" : 5,
					"y" : 9,

					"image" : ROOT + "TaskBar_Norm/EXP_Gauge_Point.sub",
				},
				{
					"name" : "EXPGauge_02",
					"type" : "expanded_image",

					"x" : 30,
					"y" : 9,

					"image" : ROOT + "TaskBar_Norm/EXP_Gauge_Point.sub",
				},
				{
					"name" : "EXPGauge_03",
					"type" : "expanded_image",

					"x" : 55,
					"y" : 9,

					"image" : ROOT + "TaskBar_Norm/EXP_Gauge_Point.sub",
				},
				{
					"name" : "EXPGauge_04",
					"type" : "expanded_image",

					"x" : 80,
					"y" : 9,

					"image" : ROOT + "TaskBar_Norm/EXP_Gauge_Point.sub",
				},
			),
		},

		{
			"name" : "ManageExpButton",
			"type" : "button",

			"x" : 270,
			"y" : 3 + Y_ADD_POSITION,

			"default_image" : ROOT + "TaskBar_Norm/Character_Button_01.sub",
			"over_image" : ROOT + "TaskBar_Norm/Character_Button_02.sub",
			"down_image" : ROOT + "TaskBar_Norm/Character_Button_03.sub",
		},

		## Mouse Button
		{
			"name" : "LeftMouseButton",
			"type" : "button",

			"x" : SCREEN_WIDTH/2 - 128,
			"y" : 3 + Y_ADD_POSITION,

			"default_image" : ROOT + "TaskBar_Norm/Mouse_Button_Move_01.sub",
			"over_image" : ROOT + "TaskBar_Norm/Mouse_Button_Move_02.sub",
			"down_image" : ROOT + "TaskBar_Norm/Mouse_Button_Move_03.sub",
		},
		{
			"name" : "RightMouseButton",
			"type" : "button",

			"x" : SCREEN_WIDTH/2 + 128 + 66 + 11,
			"y" : 3 + Y_ADD_POSITION,

			"default_image" : ROOT + "TaskBar_Norm/Mouse_Button_Move_01.sub",
			"over_image" : ROOT + "TaskBar_Norm/Mouse_Button_Move_02.sub",
			"down_image" : ROOT + "TaskBar_Norm/Mouse_Button_Move_03.sub",
		},

		## Button
		{
			"name" : "CharacterButton",
			"type" : "button",

			"x" : SCREEN_WIDTH - 144,
			"y" : 3 + Y_ADD_POSITION,

			"tooltip_text" : uiScriptLocale.TASKBAR_CHARACTER,

			"default_image" : ROOT + "TaskBar_Norm/Character_Button_01.sub",
			"over_image" : ROOT + "TaskBar_Norm/Character_Button_02.sub",
			"down_image" : ROOT + "TaskBar_Norm/Character_Button_03.sub",
		},
		{
			"name" : "InventoryButton",
			"type" : "button",

			"x" : SCREEN_WIDTH - 110,
			"y" : 3 + Y_ADD_POSITION,

			"tooltip_text" : uiScriptLocale.TASKBAR_INVENTORY,

			"default_image" : ROOT + "TaskBar_Norm/Inventory_Button_01.sub",
			"over_image" : ROOT + "TaskBar_Norm/Inventory_Button_02.sub",
			"down_image" : ROOT + "TaskBar_Norm/Inventory_Button_03.sub",
		},
		{
			"name" : "MessengerButton",
			"type" : "button",

			"x" : SCREEN_WIDTH - 76,
			"y" : 3 + Y_ADD_POSITION,

			"tooltip_text" : uiScriptLocale.TASKBAR_MESSENGER,

			"default_image" : ROOT + "TaskBar_Norm/Community_Button_01.sub",
			"over_image" : ROOT + "TaskBar_Norm/Community_Button_02.sub",
			"down_image" : ROOT + "TaskBar_Norm/Community_Button_03.sub",
		},
		{
			"name" : "SystemButton",
			"type" : "button",

			"x" : SCREEN_WIDTH - 42,
			"y" : 3 + Y_ADD_POSITION,

			"tooltip_text" : uiScriptLocale.TASKBAR_SYSTEM,

			"default_image" : ROOT + "TaskBar_Norm/System_Button_01.sub",
			"over_image" : ROOT + "TaskBar_Norm/System_Button_02.sub",
			"down_image" : ROOT + "TaskBar_Norm/System_Button_03.sub",
		},

		## ENABLE_EXPANDED_MONEY_TASKBAR
		{
			"name" : "ExpandMoneyButton",
			"type" : "button",

			"x" : SCREEN_WIDTH - 178,
			"y" : 3 + Y_ADD_POSITION,
			"tooltip_text" : uiScriptLocale.TASKBAR_MONEY_EXPAND,

			"default_image" : ROOT + "TaskBar_Norm/Ex_gemshop_button_01.tga",
			"over_image" : ROOT + "TaskBar_Norm/Ex_gemshop_button_02.tga",
			"down_image" : ROOT + "TaskBar_Norm/Ex_gemshop_button_03.tga",
		},
		## ENABLE_EXPANDED_MONEY_TASKBA

		## OfflineShop
		{
			"name" : "OfflineShop",
			"type" : "button",

			"x" : SCREEN_WIDTH - 212,
			"y" : 3 + Y_ADD_POSITION,
			
			"tooltip_text" : "Magazin Privat",

			"default_image" : "d:/ymir work/ui/game/normal_interface/private_button_01.tga",
			"over_image" : "d:/ymir work/ui/game/normal_interface/private_button_02.tga",
			"down_image" : "d:/ymir work/ui/game/normal_interface/private_button_03.tga",
		},
		## OfflineShop

		## QuickBar
		{
			"name" : "quickslot_board",
			"type" : "window",

			"x" : SCREEN_WIDTH/2 - 128 + 32 + 10,
			"y" : 0 + Y_ADD_POSITION,

			"width" : 256 + 14 + 2 + 11,
			"height" : 37,

			"children" :
			(
				{
					"name" : "ChatButton",
					"type" : "button",

					"x" : 128,
					"y" : 1,
					"tooltip_text" : uiScriptLocale.TASKBAR_CHAT,

					"default_image" : ROOT + "TaskBar_Norm/Chat_Button_01.sub",
					"over_image" : ROOT + "TaskBar_Norm/Chat_Button_02.sub",
					"down_image" : ROOT + "TaskBar_Norm/Chat_Button_03.sub",
				},
				{
					"name" : "quick_slot_1",
					"type" : "grid_table",

					"start_index" : 0,

					"x" : 0,
					"y" : 3,

					"x_count" : 4,
					"y_count" : 1,
					"x_step" : 32,
					"y_step" : 32,

					"image" : "d:/ymir work/ui/public/Slot_Base.sub",
					"image_r" : 1.0,
					"image_g" : 1.0,
					"image_b" : 1.0,
					"image_a" : 1.0,

					"children" :
					(
						{ "name" : "slot_1", "type" : "image", "x" : 3, "y" : 3, "image" : "d:/ymir work/ui/game/TaskBar_Norm/1.sub", },
						{ "name" : "slot_2", "type" : "image", "x" : 35, "y" : 3, "image" : "d:/ymir work/ui/game/TaskBar_Norm/2.sub", },
						{ "name" : "slot_3", "type" : "image", "x" : 67, "y" : 3, "image" : "d:/ymir work/ui/game/TaskBar_Norm/3.sub", },
						{ "name" : "slot_4", "type" : "image", "x" : 99, "y" : 3, "image" : "d:/ymir work/ui/game/TaskBar_Norm/4.sub", },
					),
				},
				{
					"name" : "quick_slot_2",
					"type" : "grid_table",

					"start_index" : 4,

					"x" : 128 + 14,
					"y" : 3,

					"x_count" : 4,
					"y_count" : 1,
					"x_step" : 32,
					"y_step" : 32,

					"image" : "d:/ymir work/ui/public/Slot_Base.sub",
					"image_r" : 1.0,
					"image_g" : 1.0,
					"image_b" : 1.0,
					"image_a" : 1.0,

					"children" :
					(
						{ "name" : "slot_5", "type" : "image", "x" : 3, "y" : 3, "image" : "d:/ymir work/ui/game/TaskBar_Norm/f1.sub", },
						{ "name" : "slot_6", "type" : "image", "x" : 35, "y" : 3, "image" : "d:/ymir work/ui/game/TaskBar_Norm/f2.sub", },
						{ "name" : "slot_7", "type" : "image", "x" : 67, "y" : 3, "image" : "d:/ymir work/ui/game/TaskBar_Norm/f3.sub", },
						{ "name" : "slot_8", "type" : "image", "x" : 99, "y" : 3, "image" : "d:/ymir work/ui/game/TaskBar_Norm/f4.sub", },
					),
				},
				{
					"name" : "QuickSlotBoard",
					"type" : "window",

					"x" : 128+14+128+2,
					"y" : 0,
					"width" : 11,
					"height" : 37,
					"children" :
					(
						{
							"name" : "QuickSlotNumberBox",
							"type" : "image",							
							"x" : 1,
							"y" : 15,
							"image" : ROOT + "TaskBar_Norm/QuickSlot_Button_Board.sub",
						},
						{
							"name" : "QuickPageUpButton",
							"type" : "button",
							"tooltip_text" : uiScriptLocale.TASKBAR_PREV_QUICKSLOT,
							"x" : 1,
							"y" : 9,
							"default_image" : ROOT + "TaskBar_Norm/QuickSlot_UpButton_01.sub",
							"over_image" : ROOT + "TaskBar_Norm/QuickSlot_UpButton_02.sub",
							"down_image" : ROOT + "TaskBar_Norm/QuickSlot_UpButton_03.sub",
						},

						{ 
							"name" : "QuickPageNumber", 
							"type" : "image", 							
							"x" : 3, "y" : 15, "image" : "d:/ymir work/ui/game/TaskBar_Norm/1.sub", 
						},
						{
							"name" : "QuickPageDownButton",
							"type" : "button",
							"tooltip_text" : uiScriptLocale.TASKBAR_NEXT_QUICKSLOT,

							"x" : 1,
							"y" : 24,

							"default_image" : ROOT + "TaskBar_Norm/QuickSlot_DownButton_01.sub",
							"over_image" : ROOT + "TaskBar_Norm/QuickSlot_DownButton_02.sub",
							"down_image" : ROOT + "TaskBar_Norm/QuickSlot_DownButton_03.sub",
						},
	
					),
				},
			),
		},

	),
}
