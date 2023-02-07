import uiScriptLocale

window = {
	"name" : "OfflineShopWindow",

	"x" : 0,
	"y" : 0,

	"style" : ("float", "animation",),

	"width" : 345,
	"height" : 103,

	"children" :
	(
		{
			"name" : "board",
			"type" : "border_new",
			"style" : ("attach",),

			"x" : 0,
			"y" : 0,

			"width" : 345,
			"height" : 102,
			
			"children" :
			(
				## InfoBox
				{
					"name" : "InfoBox",
					"type" : "box",

					"x" : 10,
					"y" : 10,
					"width" : 186,
					"height" : 81,

					"color" : 0xFF6C6359,
				},
				## Box2
				{
					"name" : "Box2",
					"type" : "box",

					"x" : 202,
					"y" : 10,
					"width" : 131,
					"height" : 81,

					"color" : 0xFF6C6359,
					
					"children" : 
					(
						## LockButton
						{
							"name" : "LockButton",
							"type" : "button",

							"x" : 137 - 12,
							"y" : 16 - 10,

							"horizontal_align" : "right",
							
							"text" : uiScriptLocale.OFFLINE_SHOP_BUTTON_LOCK,

							"default_image" : "d:/ymir work/ui/shop/button_default_lock.tga",
							"over_image" : "d:/ymir work/ui/shop/button_over_lock.tga",
							"down_image" : "d:/ymir work/ui/shop/button_default_lock.tga",
						},
						## RenameButton
						{
							"name" : "RenameButton",
							"type" : "button",

							"x" : 137 - 12,
							"y" : 41 - 10,

							"horizontal_align" : "right",
							
							"text" : uiScriptLocale.OFFLINE_SHOP_BUTTON_RENAME,

							"default_image" : "d:/ymir work/ui/shop/button_default_rename.tga",
							"over_image" : "d:/ymir work/ui/shop/button_over_rename.tga",
							"down_image" : "d:/ymir work/ui/shop/button_default_rename.tga",
						},
						## CloseButton
						{
							"name" : "CloseButton",
							"type" : "button",

							"x" : 137 - 12,
							"y" : 66 - 10,

							"horizontal_align" : "right",
							
							"text" : uiScriptLocale.OFFLINE_SHOP_BUTTON_CLOSE,

							"default_image" : "d:/ymir work/ui/shop/button_default_close.tga",
							"over_image" : "d:/ymir work/ui/shop/button_over_close.tga",
							"down_image" : "d:/ymir work/ui/shop/button_default_close.tga",
							# "default_image" : "d:/ymir work/ui/public/canclebutton00.sub",
							# "over_image" : "d:/ymir work/ui/public/canclebutton01.sub",
							# "down_image" : "d:/ymir work/ui/public/canclebutton02.sub",
						},
					),
				},
				## ShopSign
				{
					"name" : "ShopSignSlot",
					"type" : "slotbar",

					"x" : 16,
					"y" : 17,

					"width" : 174,
					"height" : 17,

					"children" :
					(
						{
							"name" : "ShopSignText",
							"type" : "text",

							"x" : 3,
							"y" : 2,

							"horizontal_align" : "left",
							"text_horizontal_align" : "left",
							
							"text" : "",
						},
					),
				},
				## PositionInfoText
				{
					"name" : "PosInfoText",
					"type" : "text",
					
					"text" : "",
					
					"x" : 20 + 12,
					"y" : 44,
					
					"children" :
					(
						{
							"name" : "PointIcon",
							"type" : "image",

							"x" : -19,
							"y" : 1,

							"image" : "d:/ymir work/ui/shop/position_icon.sub",
						},
					),
				},
				## TimeLeftText
				{
					"name" : "TimeLeftText",
					"type" : "text",
					
					"text" : "",
					
					"x" : 20 + 12,
					"y" : 69,
					
					"children" :
					(
						{
							"name" : "HourglassImage",
							"type" : "image",

							"x" : -19,
							"y" : 1,

							"image" : "d:/ymir work/ui/shop/sandglass_icon.sub",
						},
					),
				},
			),
		},
	),
}
