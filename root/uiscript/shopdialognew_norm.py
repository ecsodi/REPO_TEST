import uiScriptLocale

window = {
	"name" : "ShopDialog",

	"x" : SCREEN_WIDTH - 550,
	"y" : 10,

	"style" : ("movable", "float", "animation",),

	"width" : 368 - 23,
	"height" : 328,

	"children" :
	(
		{
			"name" : "board",
			"type" : "board",
			"style" : ("attach",),

			"x" : 0,
			"y" : 0,

			"width" : 368 - 23,
			"height" : 328,

			"children" :
			(
				## Title
				{
					"name" : "TitleBar",
					"type" : "titlebar",
					"style" : ("attach",),

					"x" : 8,
					"y" : 7,

					"width" : 368 - 23 - 15,
					"color" : "gray",

					"children" :
					(
						{ "name" : "TitleName", "type" : "text", "x" : 0, "y" : -1, "text" : uiScriptLocale.SHOP_TITLE, "all_align" : "center" },
					),
				},


				## Item Slot
				{
					"name" : "OffShopPanel",

					"x" : 12,
					"y" : 34,
					
					"width" : 322,
					"height" : 340,

					"children" :
					(
						{
							"name" : "CloseOffshop",
							"type" : "button",

							"x" : 45,
							"y" : 1,

							"horizontal_align" : "right",
							
							"default_image" : "d:/ymir work/ui/shop/btn_close_norm.png",
							"over_image" : "d:/ymir work/ui/shop/btn_close_over.png",
							"down_image" : "d:/ymir work/ui/shop/btn_close_down.png",
						},
						{
							"name" : "SearchShop",
							"type" : "button",

							"x" : 45 + 50,
							"y" : 1,

							"horizontal_align" : "right",
							
							"default_image" : "d:/ymir work/ui/shop/btn_search_normal.png",
							"over_image" : "d:/ymir work/ui/shop/btn_search_over.png",
							"down_image" : "d:/ymir work/ui/shop/btn_search_down.png",
						},
						{
							"name" : "LockButton",
							"type" : "button",

							"x" : 45 + (50*2),
							"y" : 1,

							"horizontal_align" : "right",
							
							"default_image" : "d:/ymir work/ui/shop/btn_lock_normal.png",
							"over_image" : "d:/ymir work/ui/shop/btn_lock_over.png",
							"down_image" : "d:/ymir work/ui/shop/btn_lock_down.png",
						},
						{
							"name" : "TotalNetworth",
							"type" : "text",

							"x" : 2,
							"y" : 69,

							"horizontal_align" : "left",
							"text_horizontal_align" : "left",

							# "text" : "Items total net worth: ",
						},
						{
							"name" : "LocationText",
							"type" : "text",

							"x" : 22,
							"y" : 31,

							"text" : "Locatie: ",
					
							"children" :
							(
								{
									"name" : "PointIcon",
									"type" : "image",

									"x" : -22,
									"y" : 1,

									"image" : "d:/ymir work/ui/shop/position_icon.sub",
								},
							),
						},
						{
							"name" : "TimeText",
							"type" : "image",

							"x" : 0,
							"y" : 310,

							"image" : "d:/ymir work/ui/shop/time_bg.png",

							"children" :
							(
								{
									"name" : "TimeText",
									"type" : "text",

									"x" : 33,
									"y" : 5,

									"text" : "Locatie: ",
								},
							),
						},

						{
							"name" : "MoneySlot",
							"type" : "button",

							"x" : 82,
							"y" : 310,

							"horizontal_align" : "center",

							"default_image" : "d:/ymir work/ui/shop/yang_bg.png",
							"over_image" : "d:/ymir work/ui/shop/yang_bg.png",
							"down_image" : "d:/ymir work/ui/shop/yang_bg.png",

							"children" :
							(
								{
									"name" : "Money",
									"type" : "text",

									"x" : 5,
									"y" : 5,

									"horizontal_align" : "right",
									"text_horizontal_align" : "right",

									"text" : "123456789",
								},
							),
						},
					),
				},


				## Item Slot
				{
					"name" : "ItemSlot",
					"type" : "grid_table",

					"x" : 12,
					"y" : 34,

					"start_index" : 0,
					"x_count" : 10,
					"y_count" : 8,
					"x_step" : 32,
					"y_step" : 32,

					"image" : "d:/ymir work/ui/public/Slot_Base.sub",
				},

				## Close
				{
					"name" : "CloseButton",
					"type" : "button",

					"x" : 0,
					"y" : 295,

					"horizontal_align" : "center",

					"text" : uiScriptLocale.PRIVATE_SHOP_CLOSE_BUTTON,

					"default_image" : "d:/ymir work/ui/public/large_button_01.sub",
					"over_image" : "d:/ymir work/ui/public/large_button_02.sub",
					"down_image" : "d:/ymir work/ui/public/large_button_03.sub",
				},
			),
		},
	),
}