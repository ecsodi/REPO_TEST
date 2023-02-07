import uiScriptLocale
import item
import app

WINDOW_WIDTH = 198
WINDOW_HEIGHT = 465-30

window = {
	"name" : "ExpandedInventoryWindow",

	"x" : SCREEN_WIDTH - (WINDOW_WIDTH * 2) - 20,
	"y" : SCREEN_HEIGHT - 37 - 565,

	"style" : ("movable", "float","animation",),

	"width" : WINDOW_WIDTH,
	"height" : WINDOW_HEIGHT,
	
	"children" :
	(
		## Inventory Slots
		{
			"name" : "board",
			"type" : "board",
			"style" : ("attach",),

			"x" : 0,
			"y" : 0,

			"width" : WINDOW_WIDTH,
			"height" : WINDOW_HEIGHT,

			"children" :
			(
				## Title
				{
					"name" : "TitleBar",
					"type" : "titlebar",
					"style" : ("attach",),

					"x" : 8,
					"y" : 7,

					"width" : WINDOW_WIDTH - 15,
					"color" : "yellow",

					"children" :
					(
						{ 
							"name":"TitleName", 
							"type":"text", 
							
							"x": (WINDOW_WIDTH - 15) / 2, 
							"y":3, 
							
							"text":uiScriptLocale.INVENTORY_TITLE, 
							"text_horizontal_align":"center" 
						},
					),
				},

				{
					"name" : "SortInventoryBtn",
					"type" : "button",
					
					"x" : WINDOW_WIDTH - 48,
					"y" : 7,
					
					"tooltip_text" : "Aranjare Iteme",
					
					"default_image" : "d:/ymir work/ui/game/comp/storage/rearrange_1.png",
					"over_image" : "d:/ymir work/ui/game/comp/storage/rearrange_2.png",
					"down_image" : "d:/ymir work/ui/game/comp/storage/rearrange_3.png",
				},

				{
					"name" : "boardunder",
					"type" : "border_a",
					"style" : ("attach",),
					
					# "image" : "d:/ymir work/ui/game/comp/storage/special_inventory.png",

					"x" : 10,
					"y" : 32,
					
					"width" : 178,
					"height" : 310,
					
					"children":
					(
						{
							"name" : "ItemSlot",
							"type" : "grid_table",
				
							"x" : 5,
							"y" : 5,
				
							"start_index" : 0,
							"x_count" : 5,
							"y_count" : 9,
							"x_step" : 34,
							"y_step" : 34,
				
							"image" : "d:/ymir work/ui/public/Slot_Base.sub"
						},

						{
							"name" : "AnimWareHouse",
							"type" : "ani_image",
							
							"x" : 185,
							"y" : 190,
							
							"delay" : 8,
						},
					),
				},
				
				{
					"name" : "boardbuttons",
					"type" : "border_a",
					"style" : ("attach",),
					
					# "image" : "d:/ymir work/ui/game/comp/storage/special_inventory2.png",

					"x" : 10,
					"y" : 346,
					
					"width" : 178,
					"height" : 80,
					
					"children" :
					(

						## Button
						{
							"name" : "SkillBookButton",
							"type" : "radio_button",
							"x" : 5,
							"y" : 9,
							
							"tooltip_text" : "Carti",
							
							"default_image" : "d:/ymir work/ui/game/normal_interface/books_1.png",
							"over_image" : "d:/ymir work/ui/game/normal_interface/books_2.png",
							"down_image" : "d:/ymir work/ui/game/normal_interface/books_3.png",
						},
						{
							"name" : "StoneButton",
							"type" : "radio_button",
							
							"x" : 5 + 44 * 1,
							"y" : 9,
							
							"tooltip_text" : "Pietre",

							"default_image" : "d:/ymir work/ui/game/normal_interface/stones_1.png",
							"over_image" : "d:/ymir work/ui/game/normal_interface/stones_2.png",
							"down_image" : "d:/ymir work/ui/game/normal_interface/stones_3.png",
						},
						{
							"name" : "UpgradeItemsButton",
							"type" : "radio_button",
							
							"x" : 5 + 44 * 2,
							"y" : 9,
							
							"tooltip_text" : "Materiale",

							"default_image" : "d:/ymir work/ui/game/normal_interface/upgrades_1.png",
							"over_image" : "d:/ymir work/ui/game/normal_interface/upgrades_2.png",
							"down_image" : "d:/ymir work/ui/game/normal_interface/upgrades_3.png",
						},
						{
							"name" : "BoxButton",
							"type" : "radio_button",
							
							"x" : 5 + 44 * 3,
							"y" : 9,
							
							"tooltip_text" : "General",
							
							"default_image" : "d:/ymir work/ui/game/normal_interface/general_1.png",
							"over_image" : "d:/ymir work/ui/game/normal_interface/general_2.png",
							"down_image" : "d:/ymir work/ui/game/normal_interface/general_3.png",
						},
						
						{
							"name" : "Inventory_Page_01",
							"type" : "radio_button",
				
							"x" : 5,
							"y" : 53,
							
							"text" : "I",

							"default_image" : "d:/ymir work/ui/game/normal_interface/page_1.png",
							"over_image" : "d:/ymir work/ui/game/normal_interface/page_2.png",
							"down_image" : "d:/ymir work/ui/game/normal_interface/page_3.png",
						},
						{
							"name" : "Inventory_Page_02",
							"type" : "radio_button",
				
							"x" : 5 + (34 * 1),
							"y" : 53,
							
							"text" : "II",
							
							"default_image" : "d:/ymir work/ui/game/normal_interface/page_1.png",
							"over_image" : "d:/ymir work/ui/game/normal_interface/page_2.png",
							"down_image" : "d:/ymir work/ui/game/normal_interface/page_3.png",
						},
						{
							"name" : "Inventory_Page_03",
							"type" : "radio_button",
				
							"x" : 5 + (34 * 2),
							"y" : 53,
							
							"text" : "III",

							"default_image" : "d:/ymir work/ui/game/normal_interface/page_1.png",
							"over_image" : "d:/ymir work/ui/game/normal_interface/page_2.png",
							"down_image" : "d:/ymir work/ui/game/normal_interface/page_3.png",
						},
						{
							"name" : "Inventory_Page_04",
							"type" : "radio_button",
				
							"x" : 5 + (34 * 3),
							"y" : 53,
							
							"text" : "IV",

							"default_image" : "d:/ymir work/ui/game/normal_interface/page_1.png",
							"over_image" : "d:/ymir work/ui/game/normal_interface/page_2.png",
							"down_image" : "d:/ymir work/ui/game/normal_interface/page_3.png",
						},
						{
							"name" : "Inventory_Page_05",
							"type" : "radio_button",
				
							"x" : 5 + (34 * 4),
							"y" : 53,
							
							"text" : "V",
							
							"default_image" : "d:/ymir work/ui/game/normal_interface/page_1.png",
							"over_image" : "d:/ymir work/ui/game/normal_interface/page_2.png",
							"down_image" : "d:/ymir work/ui/game/normal_interface/page_3.png",
						},

					),
				},
			),
		},
	),
}
