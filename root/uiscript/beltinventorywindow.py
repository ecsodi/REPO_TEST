import uiScriptLocale
import item

EQUIPMENT_START_INDEX = 180

window = {
	"name" : "BeltInventoryWindow",

	## 600 - (width + 오른쪽으로 부터 띄우기 24 px)
	"x" : SCREEN_WIDTH - 176 - 148,
	"y" : SCREEN_HEIGHT - 37 - 565 + 209 + 32,
#	"x" : -148,
#	"y" : 241,
	"width" : 148,
	"height" : 139,

	"type" : "image",
	"image" : "d:/ymir work/ui/game/belt_inventory/bg1.tga",
	

	"children" :
	(
		## Expand Buttons
		{
			"name" : "ExpandBtn",
			"type" : "button",

			"x" : 2,
			"y" : 15,

			"default_image" : "d:/ymir work/ui/game/belt_inventory/btn_expand_normal1.tga",
			"over_image" : "d:/ymir work/ui/game/belt_inventory/btn_expand_over1.tga",
			"down_image" : "d:/ymir work/ui/game/belt_inventory/btn_expand_downkj.tga",
			"disable_image" : "d:/ymir work/ui/game/belt_inventory/btn_expand_disabledk.tga",
		},

		
		## Belt Inventory Layer (include minimize button)
		{
			"name" : "BeltInventoryLayer",
#			"type" : "board",
#			"style" : ("attach", "float"),

			"x" : 5,
			"y" : 0,

			"width" : 148,
			"height" : 139,

			"children" :
			(
				## Minimize Button
				{
					"name" : "MinimizeBtn",
					"type" : "button",

					"x" : 2,
					"y" : 15,

					"width" : 10,

					"default_image" : "d:/ymir work/ui/game/belt_inventory/btn_minimize_normall.tga",
					"over_image" : "d:/ymir work/ui/game/belt_inventory/btn_minimize_overl.tga",
					"down_image" : "d:/ymir work/ui/game/belt_inventory/btn_minimize_downl.tga",
					"disable_image" : "d:/ymir work/ui/game/belt_inventory/btn_minimize_disablked.tga",
				},

				## Real Belt Inventory Board
				{
					"name" : "BeltInventoryBoard",
					"type" : "board",
					"style" : ("attach", "float"),

					"x" : 10,
					"y" : 0,

					"width" : 138,
					"height" : 139,

					"children" :
					(
						## Belt Inventory Slots
						{
							"name" : "BeltInventorySlot",
							"type" : "grid_table",

							"x" : 5,
							"y" : 5,

							"start_index" : item.BELT_INVENTORY_SLOT_START,
							"x_count" : 4,
							"y_count" : 4,
							"x_step" : 32,
							"y_step" : 32,

							"image" : "d:/ymir work/ui/public/Slokt_Base.sub"
						},
					),
				},
			)
		},

	),
}
