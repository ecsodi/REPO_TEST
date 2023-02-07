import uiScriptLocale
import item
import app
import constInfo

SLOT_SASH = item.COSTUME_SLOT_START
COSTUME_START_INDEX = item.COSTUME_SLOT_START

EQUIPMENT_START_INDEX = 180 + 810

window = {
	"name" : "InventoryWindow",

	"x" : SCREEN_WIDTH - 213,
	"y" : SCREEN_HEIGHT - 37 - 569,

    "style" : ("movable", "float", "not_pick", "animation",),

	"width" : 213,
	"height" : 547,

	"children" :
	(
		## Inventory, Equipment Slots
		{
			"name" : "board",
			"type" : "board",
			"style" : ("attach",),

			"x" : 29,
			"y" : 0,

			"width" : 176,
			"height" : 547,


			"children" :
			(

				## Title
				{
					"name" : "TitleBar",
					"type" : "titlebar",
					"style" : ("attach",),

					"x" : 6,
					"y" : 7,

					"width" : 176 - 15,
					"color" : "yellow",
					
					"children" :
					(
						{ "name":"TitleName", "type":"text", "x":79, "y":3, "text":uiScriptLocale.INVENTORY_TITLE, "text_horizontal_align":"center" },
					),
				},
				## Equipment Slot
				{
					"name" : "Equipment_Base",
					"type" : "image",

					"x" : 10,
					"y" : 33,
					
					"image" : "d:/ymir work/ui/game/normal_interface/new_equipment_bg.tga",

					"children" :
					(
										# {"index":EQUIPMENT_START_INDEX+9, "x":3, "y":66, "width":32, "height":32}, // NOT USED
										# {"index":EQUIPMENT_START_INDEX+4, "x":3, "y":3, "width":32, "height":96}, // NOT USED

						{
							"name" : "EquipmentSlot",
							"type" : "slot",

							"x" : 3,
							"y" : 3,

							"width" : 178,
							"height" : 182,

							"slot" : (
										{"index":EQUIPMENT_START_INDEX+0, "x":39, "y":37, "width":32, "height":64},
										{"index":EQUIPMENT_START_INDEX+1, "x":39, "y":2, "width":32, "height":32},
										{"index":EQUIPMENT_START_INDEX+2, "x":39, "y":145, "width":32, "height":32},
										{"index":EQUIPMENT_START_INDEX+3, "x":75, "y":67, "width":32, "height":32},
										{"index":EQUIPMENT_START_INDEX+5, "x":114, "y":67, "width":32, "height":32},
										{"index":EQUIPMENT_START_INDEX+6, "x":114, "y":35, "width":32, "height":32},
										{"index":EQUIPMENT_START_INDEX+7, "x":3, "y":144, "width":32, "height":32},
										{"index":EQUIPMENT_START_INDEX+8, "x":74, "y":144, "width":32, "height":32},		# Exp Ring
										{"index":EQUIPMENT_START_INDEX+10, "x":74, "y":35, "width":32, "height":32},		# Thief Gloves
										{"index":EQUIPMENT_START_INDEX+31, "x":3, "y":106, "width":32, "height":32}, # amuleta
										{"index":EQUIPMENT_START_INDEX+32, "x":74, "y":106, "width":32, "height":32}, # inel
										{"index":1013, "x":39, "y":106, "width":32, "height":32},
										{"index":item.COSTUME_SLOT_SASH, "x":114, "y":3, "width":32, "height":32},#pendant

									),
						},
						## CostumeButton
						{
							"name" : "CostumeButton",
							"type" : "button",

							"x" : 117 - 39,
							"y" : 4,

							"tooltip_text" : uiScriptLocale.COSTUME_TITLE,

							"default_image" : "d:/ymir work/ui/game/taskbar_norm/costume_Button_01.tga",
							"over_image" : "d:/ymir work/ui/game/taskbar_norm/costume_Button_02.tga",
							"down_image" : "d:/ymir work/ui/game/taskbar_norm/costume_Button_03.tga",
						},
						
						{
							"name" : "SpecialStorageButton",
							"type" : "button",

							"x" : 117,
							"y" : 148,

							"default_image" : "d:/ymir work/ui/game/taskbar_norm/mall_button_01.tga",
							"over_image" : "d:/ymir work/ui/game/taskbar_norm/mall_button_02.tga",
							"down_image" : "d:/ymir work/ui/game/taskbar_norm/mall_button_03.tga",
						},
						
						## Dragon Soul Button
						{
							"name" : "DSSButton",
							"type" : "button",

							"x" : 114,
							"y" : 107,

							"default_image" : "d:/ymir work/ui/game/normal_interface/dss_inventory_button_01.tga",
							"over_image" : "d:/ymir work/ui/game/normal_interface/dss_inventory_button_02.tga",
							"down_image" : "d:/ymir work/ui/game/normal_interface/dss_inventory_button_03.tga",
						},
					),
				},

				# {
					# "name" : "Inventory_Tab_01",
					# "type" : "radio_button",

					# "x" : 17,
					# "y" : 27 + 191,

					# "default_image" : "d:/ymir work/ui/game/comp/renewal_inventory/page_1.png",
					# "over_image" : "d:/ymir work/ui/game/comp/renewal_inventory/page_2.png",
					# "down_image" : "d:/ymir work/ui/game/comp/renewal_inventory/page_3.png",
					# "tooltip_text" : uiScriptLocale.INVENTORY_PAGE_BUTTON_TOOLTIP_1,
				# },
				# {
					# "name" : "Inventory_Tab_02",
					# "type" : "radio_button",

					# "x" : 17 + 39,
					# "y" : 27 + 191,

					# "default_image" : "d:/ymir work/ui/game/comp/renewal_inventory/page_1.png",
					# "over_image" : "d:/ymir work/ui/game/comp/renewal_inventory/page_2.png",
					# "down_image" : "d:/ymir work/ui/game/comp/renewal_inventory/page_3.png",
					# "tooltip_text" : uiScriptLocale.INVENTORY_PAGE_BUTTON_TOOLTIP_2,
				# },
				
				# {
					# "name" : "Inventory_Tab_03",
					# "type" : "radio_button",

					# "x" : 17 + 39 + 39,
					# "y" : 27 + 191,

					# "default_image" : "d:/ymir work/ui/game/comp/renewal_inventory/page_1.png",
					# "over_image" : "d:/ymir work/ui/game/comp/renewal_inventory/page_2.png",
					# "down_image" : "d:/ymir work/ui/game/comp/renewal_inventory/page_3.png",
					# "tooltip_text" : uiScriptLocale.INVENTORY_PAGE_BUTTON_TOOLTIP_3,
				# },
				
				# {
					# "name" : "Inventory_Tab_04",
					# "type" : "radio_button",

					# "x" : 17 + 39 + 39 + 39,
					# "y" : 27 + 191,

					# "default_image" : "d:/ymir work/ui/game/comp/renewal_inventory/page_1.png",
					# "over_image" : "d:/ymir work/ui/game/comp/renewal_inventory/page_2.png",
					# "down_image" : "d:/ymir work/ui/game/comp/renewal_inventory/page_3.png",
					# "tooltip_text" : uiScriptLocale.INVENTORY_PAGE_BUTTON_TOOLTIP_4,
				# },

				## Item Slot
				{
					"name" : "ItemSlot",
					"type" : "grid_table",

					"x" : 8,
					"y" : 246,

					"start_index" : 0,
					"x_count" : 5,
					"y_count" : 9,
					"x_step" : 32,
					"y_step" : 32,

					"image" : "d:/ymir work/ui/public/Slot_Base.sub"
				},
			),
		},
		{
			"name" : "SwitchbotBtn",
			"type" : "button",

			"x" : 0,
			"y" : 20,

			"default_image" : "d:/ymir work/ui/game/normal_interface/sidebutton_normal.png",
			"over_image" : "d:/ymir work/ui/game/normal_interface/sidebutton_hover.png",
			"down_image" : "d:/ymir work/ui/game/normal_interface/sidebutton_down.png",
			
			"children" :
			(
				{
					"name" : "SwitchImage",
					"type" : "text",

					"x" : 0,
					"y" : -3,

					"all_align" : "center",

					"text" : "|Ed:/ymir work/ui/game/comp/renewal_inventory/switchbot.png|e",
				},
			),
		},
		{
			"name" : "MallButton",
			"type" : "button",

			"x" : 0,
			"y" : 20 + 38,

			"default_image" : "d:/ymir work/ui/game/normal_interface/sidebutton_normal.png",
			"over_image" : "d:/ymir work/ui/game/normal_interface/sidebutton_hover.png",
			"down_image" : "d:/ymir work/ui/game/normal_interface/sidebutton_down.png",
			
			"children" :
			(
				{
					"name" : "MallImage",
					"type" : "text",

					"x" : 0,
					"y" : -3,

					"all_align" : "center",

					"text" : "|Ed:/ymir work/ui/game/comp/renewal_inventory/safebox.png|e",
				},
			),
		},
		{
			"name" : "ShopSearchButton",
			"type" : "button",

			"x" : 0,
			"y" : 20 + (38* 2),

			"default_image" : "d:/ymir work/ui/game/normal_interface/sidebutton_normal.png",
			"over_image" : "d:/ymir work/ui/game/normal_interface/sidebutton_hover.png",
			"down_image" : "d:/ymir work/ui/game/normal_interface/sidebutton_down.png",
			
			"children" :
			(
				{
					"name" : "SearchImage",
					"type" : "text",

					"x" : 0,
					"y" : -3,

					"all_align" : "center",

					"text" : "|Ed:/ymir work/ui/game/comp/renewal_inventory/shop_search.png|e",
				},
			),
		},
		{
			"name" : "RewardButton",
			"type" : "button",

			"x" : 0,
			"y" : 20 + (38* 3),

			"default_image" : "d:/ymir work/ui/game/normal_interface/sidebutton_normal.png",
			"over_image" : "d:/ymir work/ui/game/normal_interface/sidebutton_hover.png",
			"down_image" : "d:/ymir work/ui/game/normal_interface/sidebutton_down.png",
			
			"children" :
			(
				{
					"name" : "RewardImage",
					"type" : "text",

					"x" : 0,
					"y" : -3,

					"all_align" : "center",

					"text" : "|Ed:/ymir work/ui/game/comp/renewal_inventory/icon_challenges.png|e",
				},
			),
		},
		
	),
}

pageName = ["I", "II", "III", "IV", "V"]
tooltipName = [uiScriptLocale.INVENTORY_PAGE_BUTTON_TOOLTIP_1, uiScriptLocale.INVENTORY_PAGE_BUTTON_TOOLTIP_2, uiScriptLocale.INVENTORY_PAGE_BUTTON_TOOLTIP_3, uiScriptLocale.INVENTORY_PAGE_BUTTON_TOOLTIP_4, "V"]
for i in xrange(4):
	window["children"][0]["children"] += ( \
		{
			"name" : "Inventory_Tab_0%d" % (i+1),
			"type" : "radio_button",
			"x" : 7+3+39*i,
			"y" : 30 + 191,
			"default_image" : "d:/ymir work/ui/game/windows/tab_button_large_half_01.sub",
			"over_image" : "d:/ymir work/ui/game/windows/tab_button_large_half_02.sub",
			"down_image" : "d:/ymir work/ui/game/windows/tab_button_large_half_03.sub",
			"tooltip_text" : tooltipName[i],

			"children" :
			(
				{
					"name" : "Inventory_Tab_0%d_Print" % (i+1),
					"type" : "text",
					"x" : 0,
					"y" : 0,
					"all_align" : "center",
					"text" : pageName[i],
				},
			),
		},
	)
