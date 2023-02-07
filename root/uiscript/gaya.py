import uiScriptLocale
BUTTON_ROOT = "d:/ymir work/ui/public/"
ROOT_PATH = "d:/ymir work/ui/game/windows/"
GEM_PATH = "d:/ymir work/ui/gemshop/"
GEM_ICON = "d:/ymir work/ui/gemshop/gemshop_gemicon.sub"
BUTTON_PATH = "d:/ymir work/ui/game/shopsearchp2p/"
BOARD_WIDTH = 167
BOARD_HEIGHT = 300
window = {
	"name" : "GemShopWindow",

	"x" : 0,
	"y" : 0,

	"style" : ("movable", "float","animation",),

	"width" : BOARD_WIDTH,
	"height" : BOARD_HEIGHT,

	"children" :
	(
		{
			"name" : "board",
			"type" : "board",
			"style" : ("attach",),

			"x" : 0,
			"y" : 0,

			"width" : BOARD_WIDTH,
			"height" : BOARD_HEIGHT,
		
			"children" :
			(
				## Title
				{
					"name" : "TitleBar",
					"type" : "titlebar",
					"style" : ("attach",),

					"x" : 6,
					"y" : 7,

					"width" : BOARD_WIDTH-13,
					"color" : "yellow",

					"children" :
					(
						{ "name":"TitleName", "type":"text", "x":BOARD_WIDTH / 2 - 5, "y":3, "text": "Gaya's Shop", "text_horizontal_align":"center" },
					),
				},

				{ 
					"name":"gemshopbackimg", 
					"type":"image", 
					"x":14,
					"y":31, 
					"image": "d:/ymir work/ui/gemshop_rework/gemshop_rework.png",
				},

				{
					"name" : "ItemSlot",
					"type" : "slot",
			
					"x" : 0,
					"y" : 38,
			
					"width" : 168,
					"height" : 200,
					# "image" : "d:/ymir work/ui/public/Slot_Base.sub",
			
					"slot" : (
						{"index":0, "x":22, "y":0, "width":32, "height":32},  # slot_1
						{"index":1, "x":67, "y":0, "width":32, "height":32},  # slot_2
						{"index":2, "x":112, "y":0, "width":32, "height":32},  # slot_3

						{"index":3, "x":22, "y":58, "width":32, "height":32},  # slot_4
						{"index":4, "x":67, "y":58, "width":32, "height":32},  # slot_5
						{"index":5, "x":112, "y":58, "width":32, "height":32},  # slot_6

						{"index":6, "x":22, "y":116, "width":32, "height":32},  # slot_7
						{"index":7, "x":67, "y":116, "width":32, "height":32},  # slot_8
						{"index":8, "x":112, "y":116, "width":32, "height":32},  # slot_9

						{"index":9, "x":22, "y":175, "width":32, "height":32},  # slot_10
						{"index":10, "x":67, "y":175, "width":32, "height":32},  # slot_11
						{"index":11, "x":112, "y":175, "width":32, "height":32},  # slot_12
					),
				},

				{ "name":"slot_1_price", "type":"text", "x" : 19+25, "y":75, "text":"999", "text_horizontal_align":"center" },
				{ "name":"slot_1_Icon", "type":"image", "x":19, "y":77, "image":GEM_ICON, },	
				
				{ "name":"slot_2_price", "type":"text", "x" : 64+25, "y":75, "text":"2", "text_horizontal_align":"center" },
				{ "name":"slot_2_Icon", "type":"image", "x":64, "y":77, "image":GEM_ICON, },	
				
				{ "name":"slot_3_price", "type":"text", "x" : 109+25, "y":75, "text":"33", "text_horizontal_align":"center" },
				{ "name":"slot_3_Icon", "type":"image", "x":109, "y":77, "image":GEM_ICON, },	
								
				{ "name":"slot_4_price", "type":"text", "x" : 19+25, "y":133, "text":"4", "text_horizontal_align":"center" },
				{ "name":"slot_4_Icon", "type":"image", "x":19, "y":135, "image":GEM_ICON, },	
				
				{ "name":"slot_5_price", "type":"text", "x" : 64+25, "y":133, "text":"5", "text_horizontal_align":"center" },
				{ "name":"slot_5_Icon", "type":"image", "x":64, "y":135, "image":GEM_ICON, },	
				
				{ "name":"slot_6_price", "type":"text", "x" : 109+25, "y":133, "text":"6", "text_horizontal_align":"center" },
				{ "name":"slot_6_Icon", "type":"image", "x":109, "y":135, "image":GEM_ICON, },	
				
				{ "name":"slot_7_price", "type":"text", "x" : 19+25, "y":191, "text":"7", "text_horizontal_align":"center" },
				{ "name":"slot_7_Icon", "type":"image", "x":19, "y":193, "image":GEM_ICON, },	
				
				{ "name":"slot_8_price", "type":"text", "x" : 64+25, "y":191, "text":"8", "text_horizontal_align":"center" },
				{ "name":"slot_8_Icon", "type":"image", "x":64, "y":193, "image":GEM_ICON, },	
				
				{ "name":"slot_9_price", "type":"text", "x" : 109+25, "y":191, "text":"9", "text_horizontal_align":"center" },
				{ "name":"slot_9_Icon", "type":"image", "x":109, "y":193, "image":GEM_ICON, },	

				{ "name":"slot_10_price", "type":"text", "x" : 19+25, "y":249, "text":"10", "text_horizontal_align":"center" },
				{ "name":"slot_10_Icon", "type":"image", "x":19, "y":251, "image":GEM_ICON, },	

				{ "name":"slot_11_price", "type":"text", "x" : 64+25, "y":249, "text":"11", "text_horizontal_align":"center" },
				{ "name":"slot_11_Icon", "type":"image", "x":64, "y":251, "image":GEM_ICON, },	

				{ "name":"slot_12_price", "type":"text", "x" : 109+25, "y":249, "text":"12", "text_horizontal_align":"center" },
				{ "name":"slot_12_Icon", "type":"image", "x":109, "y":251, "image":GEM_ICON, },	

				{
					"name" : "PageCount",
					"type" : "image",

					"x" : 53,
					"y" : 269,
					
					"image" : "d:/ymir work/ui/gemshop_rework/gemshop_count_page.png"
				},

				{ "name":"TextPage", "type":"text", "x" : (BOARD_WIDTH / 2), "y":BOARD_HEIGHT - 27, "text":"0 / 1", "text_horizontal_align":"center" },
				
				{
					"name" : "PrevButton",
					"type" : "button",

					"x" : 13,
					"y" : 270,
					
					"default_image" : BUTTON_PATH + "btn_first_prev_default.dds",
					"over_image" 	: BUTTON_PATH + "btn_first_prev_hover.dds",
					"down_image" 	: BUTTON_PATH + "btn_first_prev_down.dds",
				},
				
				{
					"name" : "NextButton",
					"type" : "button",

					"x" : 135,
					"y" : 270,
					
					"default_image" : BUTTON_PATH + "btn_last_next_default.dds",
					"over_image" 	: BUTTON_PATH + "btn_last_next_hover.dds",
					"down_image" 	: BUTTON_PATH + "btn_last_next_down.dds",
				},
			),
		},
	),
	# "children" :
	# (
		# {
			# "name" : "board",
			# "type" : "board",
			# "style" : ("attach",),

			# "x" : 300,
			# "y" : 300,

			# "width" : BOARD_WIDTH,
			# "height" : BOARD_HEIGHT,
		
			# "children" :
			# (
				# Title
				# {
					# "name" : "TitleBar",
					# "type" : "titlebar",
					# "style" : ("attach",),

					# "x" : 6,
					# "y" : 6,

					# "width" : BOARD_WIDTH-13,					
					# "color" : "yellow",

					# "children" :
					# (
						# { "name":"TitleName", "type":"text", "x":BOARD_WIDTH / 2 - 5, "y":3, "text": "Gaya's Shop", "text_horizontal_align":"center" },
					# ),
				# },
			# ),
		# },
	# ),
}

