import uiScriptLocale

window = {
	"name" : "SearchShop",

	"x" : (SCREEN_WIDTH - 520) / 2,
	"y" : SCREEN_HEIGHT / 4,
	
	"style" : ("movable", "float", "animation",),
	
	"width" : 520,
	"height" : 100,
	
	"children" :
	(
		{
			"name" : "Board",
			"type" : "board",
			
			"style" : ("attach",),
			
			"x" : 0,
			"y" : 0,
			
			"width" : 520,
			"height" : 100,
			
			"children" :
			(
				## TitleBar
				{
					"name" : "TitleBar",
					"type" : "titlebar",
					
					"style" : ("attach",),
					
					"x" : 8,
					"y" : 7,
					
					"width" : 505,
					
					"color" : "red",
					
					"children" :
					(
						{ "name" : "TitleName", "type" : "text", "x" : 0, "y" : -1, "text" : uiScriptLocale.SEARCH_SHOP_TITLE, "all_align" : "center" },
					),
				},
				## SearchBox
				{
					"name" : "SearchBox",
					"type" : "box",

					"x" : 15,
					"y" : 35,
					
					"width" : 488,
					"height" : 50,

					"color" : 0xFF6C6359,
					
					"children" :
					(
						## NameBox
						{
							"name" : "NameBox",
							"type" : "box",

							"x" : 10,
							"y" : 15,
							
							"width" : 210,
							"height" : 20,

							"color" : 0xFF6C6359,
							
							"children" : 
							(
								## NameBar
								{
									"name" : "NameBar",
									"type" : "bar",

									"x" : 1,
									"y" : 1,
									
									"width" : 209,
									"height" : 19,
								},
								## InputName
								{
									"name" : "InputName",
									"type" : "editline",
									
									"x" : 3,
									"y" : 3,
									
									"width" : 210,
									"height" : 18,
									
									"text_horizontal_align" : "left",
									
									"input_limit" : 24,
								},
								## SearchButton
								{
									"name" : "SearchButton",
									"type" : "button",
									
									"x" : 19,
									"y" : 1,
									
									"horizontal_align" : "right",
									
									"default_image" : "d:/ymir work/ui/shop/search/search_button.tga",
									"over_image" : "d:/ymir work/ui/shop/search/search_button_hover.tga",
									"down_image" : "d:/ymir work/ui/shop/search/search_button.tga",
								},
							),
						},
						## PriceBox
						{
							"name" : "PriceBox",
							"type" : "box",

							"x" : 245,
							"y" : 15,
							
							"width" : 140,
							"height" : 20,

							"color" : 0xFF6C6359,
							
							"children" : 
							(
								## PriceBar
								{
									"name" : "PriceBar",
									"type" : "bar",

									"x" : 1,
									"y" : 1,
									
									"width" : 139,
									"height" : 19,
								},
								## InputPrice
								{
									"name" : "InputPrice",
									"type" : "editline",
									
									"x" : 3,
									"y" : 3,
									
									"width" : 139,
									"height" : 18,
									
									"text_horizontal_align" : "left",
									
									"only_number" : 1,
									"input_limit" : 10,
								},
							),
						},
						## SortButton
						{
							"name" : "SortButton",
							"type" : "toggle_button",

							"x" : 400,
							"y" : 15,

							"default_image" : "d:/ymir work/ui/shop/search/ascending.tga",
							"over_image" : "d:/ymir work/ui/shop/search/ascending.tga",
							"down_image" : "d:/ymir work/ui/shop/search/descending.tga",
						},
						## SaveButton
						{
							"name" : "SaveButton",
							"type" : "button",

							"x" : 430,
							"y" : 15,

							"default_image" : "d:/ymir work/ui/shop/search/star.tga",
							"over_image" : "d:/ymir work/ui/shop/search/star.tga",
							"down_image" : "d:/ymir work/ui/shop/search/star.tga",
						},
						## ListButton
						{
							"name" : "ListButton",
							"type" : "button",

							"x" : 460,
							"y" : 15,

							"default_image" : "d:/ymir work/ui/shop/search/list.tga",
							"over_image" : "d:/ymir work/ui/shop/search/list.tga",
							"down_image" : "d:/ymir work/ui/shop/search/list.tga",
						},
					),
				},
				## ItemsBox
				{
					"name" : "ItemsBox",
					"type" : "box",

					"x" : 15,
					"y" : 93,
					
					"width" : 488,
					"height" : 0,

					"color" : 0xFF6C6359,
					
					"children" :
					(
						{
							"name" : "ItemBarList",
							"type" : "listboxex",
							
							"x" : 6,
							"y" : 6,
							
							"width" : 480,
							"height" : 300,
							
							"itemstep" : 30,
							"viewcount" : 10,
						},
						{
							"name" : "ScrollBar",
							"type" : "scrollbar",

							"x" : 469,
							"y" : 5,
							"size" : 305,
						},
					),
				},
				{
					"name" : "FirstButton",
					"type" : "button",
					
					"x" : 225,
					"y" : 25,
					
					"default_image" : "d:/ymir work/ui/privatesearch/private_first_prev_btn_01.sub",
					"over_image" : "d:/ymir work/ui/privatesearch/private_first_prev_btn_02.sub",
					"down_image" : "d:/ymir work/ui/privatesearch/private_first_prev_btn_02.sub",
				},
				{
					"name" : "PrevButton",
					"type" : "button",
					
					"x" : 240,
					"y" : 25,
					
					"default_image" : "d:/ymir work/ui/privatesearch/private_prev_btn_01.sub",
					"over_image" : "d:/ymir work/ui/privatesearch/private_prev_btn_02.sub",
					"down_image" : "d:/ymir work/ui/privatesearch/private_prev_btn_02.sub",
				},
				{
					"name" : "NextButton",
					"type" : "button",
					
					"x" : 270,
					"y" : 25,
					
					"default_image" : "d:/ymir work/ui/privatesearch/private_next_btn_01.sub",
					"over_image" : "d:/ymir work/ui/privatesearch/private_next_btn_02.sub",
					"down_image" : "d:/ymir work/ui/privatesearch/private_next_btn_02.sub",
				},
				{
					"name" : "LastButton",
					"type" : "button",
					
					"x" : 282,
					"y" : 25,
					
					"default_image" : "d:/ymir work/ui/privatesearch/private_last_next_btn_01.sub",
					"over_image" : "d:/ymir work/ui/privatesearch/private_last_next_btn_02.sub",
					"down_image" : "d:/ymir work/ui/privatesearch/private_last_next_btn_02.sub",
				},
				{
					"name" : "PageText",
					"type" : "text",

					"x" : 258,
					"y" : 27,

					"text" : "1",
				},
			),
		},
	),
}
