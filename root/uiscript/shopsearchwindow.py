import localeInfo
import ui

ROOT = "d:/ymir work/ui/game/shopsearchmgr/"
ROOT_GRAPH = ROOT + "graph/"

BORDER_X = 15
BORDER_TOP = 40
BORDER_BOTTOM = 20

MAIN_WIDTH = 800
MAIN_HEIGHT = 512

BOARD_WIDTH = BORDER_X * 2 + MAIN_WIDTH
BOARD_HEIGHT = BORDER_TOP + BORDER_BOTTOM + MAIN_HEIGHT

ITEM_PAGE_SKIP_BTN_WIDTH = 12
ITEM_PAGE_ONCE_BTN_WIDTH = 8
ITEM_PAGE_BTN_WIDTH = 34
ITEM_PAGE_BTN_SPACE = 3

# DESC_TEXT_COLOR = ui.GenerateColor(150, 150, 150)

window = {
	"name" : "ShopSearchBoard",

	"x" : 0,
	"y" : 0,

	"style" : ("movable", "float",),

	"width" : BOARD_WIDTH-16,
	"height" : BOARD_HEIGHT-15,

	"children" :
	(
		{
			"name" : "board",
			"type" : "board_with_titlebar",
			"style" : ("attach",),

			"x" : 0,
			"y" : 0,

			"width" : BOARD_WIDTH-16,
			"height" : BOARD_HEIGHT-15,

			"title" : localeInfo.SHOP_SEARCH_ITEM_TITLE,

			"children" :
			(
				{
					"name" : "main",
					"type" : "image",

					"x" : BORDER_X-11,
					"y" : BORDER_TOP-12,

					"image" : ROOT + "bg_new.png",
					"children" :
					(
						## Category Header
						{
							"name" : "category_header",
							"type" : "image",

							"x" : 1,
							"y" : 2,

							"image" : ROOT + "cat_title.tga",

							"children" :
							(
								{
									"name" : "category_title",
									"type" : "text",

									"x" : 77,
									"y" : 22,

									"text_vertical_align" : "center",

									"text" : localeInfo.SHOP_SEARCH_ITEM_CATEGORY_TITLE,
									"fontsize" : "LARGE",
								},
							),
						},
						## Category List
						{
							"name" : "category_list",
							"type" : "listboxex_shop",

							"x" : 3,
							"y" : 40,

							"width" : 192,
							"height" : 440,

							"itemsize_x" : 192,
							"itemsize_y" : 31,

							"itemstep" : 31,
							"viewcount" : 440 / 31,
						},
						## Category Scrollbar
						{
							"name" : "category_scroll_bg",
							"type" : "image",

							"x" : 192,
							"y" : 46,

							"image" : ROOT + "scrollbar_bg.tga",
							"children" :
							(
								{
									"name" : "category_scroll",
									"type" : "scrollbar_template",

									"x" : 1,
									"y" : 0,

									"middle_image_top" : ROOT + "scrollbar_top_btn.tga",
									"middle_image_center" : ROOT + "scrollbar_center_btn.tga",
									"middle_image_bottom" : ROOT + "scrollbar_bottom_btn.tga",

									"size" : 439,
									"bar_width" : 4,
								},
							),
						},
						## Sort Button
						{
							"name" : "sort_button",
							"type" : "button",

							"x" : 206+2,
							"y" : 7+2,
						},
						## Search Bar
						{
							"name" : "search_bg",
							"type" : "image",

							"x" : 457-446,
							"y" : 8,

							"image" : ROOT + "search_bg.png",
							"children" :
							(
								{
									"name" : "search_button",
									"type" : "button",

									"x" : 200-44,
									"y" : 6,

									"default_image" : ROOT + "search_btn_up.png",
									"over_image" : ROOT + "search_btn_over.png",
									"down_image" : ROOT + "search_btn_down.png",
								},
								{
									"name" : "search_line",
									"type" : "editline",

									"x" : 9,
									"y" : 7,

									"width" : 145,
									"height" : 15,

									"input_limit" : 30,

									"overlay" : localeInfo.SHOP_SEARCH_SEARCH_OVERLAY,
								},
							),
						},
						## Favourites Button
						{
							"name" : "fav_button",
							"type" : "button",

							"x" : 685,
							"y" : 7,

							"default_image" : ROOT + "fav_button_up.tga",
							"over_image" : ROOT + "fav_button_over.tga",
							"down_image" : ROOT + "fav_button_down.tga",

							"text" : localeInfo.SHOP_SEARCH_ITEM_FAVOURITE_BUTTON,
						},
						## Item List
						{
							"name" : "item_list",
							"type" : "pixellistbox",

							"x" : 210,
							"y" : 48,

							"width" : 570,
							"height" : 434,

							"vertical_space" : 3,

							"children" :
							(
								## Loading Image
								{
									"name" : "loading_image",
									"type" : "ani_image",

									"x" : -6,
									"y" : -6,

									"width" : 39,
									"height" : 39,

									"horizontal_align" : "center",
									"vertical_align" : "center",

									"delay" : 2.5,

									"images" : [ROOT + "loading_circle/frame_delay_%d.png" % (i + 1) for i in xrange(38)],
								},
								{ "name":"item_no_search_info", "type":"multi_text", "width":580, "x":0, "y":0, "text":localeInfo.SHOP_SEARCH_ITEM_NO_SEARCH_INFO, "outline":"1", },
								{
									"name" : "item_no_result_info",
									"type" : "text",

									"x" : 0,
									"y" : 0,

									"all_align" : 1,

									"text" : localeInfo.SHOP_SEARCH_ITEM_NO_RESULT_INFO,
								},
							),
						},
						## Item Scrollbar
						{
							"name" : "item_scrollbar_bg",
							"type" : "image",
							
							"x" : 789,
							"y" : 46,

							"image" : ROOT + "scrollbar_bg.tga",
							"children" :
							(
								{
									"name" : "item_scrollbar",
									"type" : "scrollbar_template",

									"x" : 1,
									"y" : 0,

									"middle_image_top" : ROOT + "scrollbar_top_btn.tga",
									"middle_image_center" : ROOT + "scrollbar_center_btn.tga",
									"middle_image_bottom" : ROOT + "scrollbar_bottom_btn.tga",

									"size" : 439,
									"bar_width" : 4,
								},
							),
						},
						## Item Count selection
						{
							"name" : "entry_count_1",
							"type" : "radio_button",

							"x" : 206,
							"y" : 494,

							"default_image" : ROOT + "pagenumber_default.png",
							"over_image" : ROOT + "pagenumber_hover.png",
							"down_image" : ROOT + "pagenumber_down.png",

							"text" : "50",

							"tooltip_text" : localeInfo.SHOP_SEARCH_ITEM_COUNT_PER_PAGE % 50,
						},
						{
							"name" : "entry_count_2",
							"type" : "radio_button",

							"x" : 206 + 36,
							"y" : 494,

							"default_image" : ROOT + "pagenumber_default.png",
							"over_image" : ROOT + "pagenumber_hover.png",
							"down_image" : ROOT + "pagenumber_down.png",

							"text" : "100",

							"tooltip_text" : localeInfo.SHOP_SEARCH_ITEM_COUNT_PER_PAGE % 100,
						},
						{
							"name" : "entry_count_3",
							"type" : "radio_button",

							"x" : 206 + 36 + 36,
							"y" : 494,

							"default_image" : ROOT + "pagenumber_default.png",
							"over_image" : ROOT + "pagenumber_hover.png",
							"down_image" : ROOT + "pagenumber_down.png",

							"text" : "150",

							"tooltip_text" : localeInfo.SHOP_SEARCH_ITEM_COUNT_PER_PAGE % 150,
						},
						## Item Page selection
						{
							"name" : "item_page_wnd",

							"x" : 206 + 36 + 36 + 60,
							"y" : 493,

							"width" : 375,
							"height" : 22,

							"children" :
							(
								{
									"name" : "item_page_button_wnd",

									"x" : -20,
									"y" : 0,

									"width" : ITEM_PAGE_BTN_WIDTH * 5 + ITEM_PAGE_BTN_SPACE * 4 + (ITEM_PAGE_SKIP_BTN_WIDTH * 2 + ITEM_PAGE_ONCE_BTN_WIDTH * 2 + ITEM_PAGE_BTN_SPACE * 4) + 22,
									"height" : 22,

									"horizontal_align" : "center",

									"children" :
									(
										{
											"name" : "item_first_page_btn",
											"type" : "button",

											"x" : -22+22,
											"y" : 0,

											"default_image" : ROOT + "content_first_page.dds",
											"over_image" : ROOT + "content_first_page_over.dds",
											"down_image" : ROOT + "content_first_page_down.dds",

											"vertical_align" : "center",

											"tooltip_text" : localeInfo.SHOP_SEARCH_ITEM_PAGE_FIRST_TOOLTIP,
										},
										{
											"name" : "item_previous_page_btn",
											"type" : "button",

											"x" : ITEM_PAGE_SKIP_BTN_WIDTH + ITEM_PAGE_BTN_SPACE-22+22,
											"y" : 0,

											"default_image" : ROOT + "content_previous_page.dds",
											"over_image" : ROOT + "content_previous_page_over.dds",
											"down_image" : ROOT + "content_previous_page_down.dds",

											"vertical_align" : "center",

											"tooltip_text" : localeInfo.SHOP_SEARCH_ITEM_PAGE_PREVIOUS_TOOLTIP,
										},
										{
											"name" : "item_page_btn1",
											"type" : "radio_button",

											"x" : ITEM_PAGE_SKIP_BTN_WIDTH + ITEM_PAGE_ONCE_BTN_WIDTH + ITEM_PAGE_BTN_SPACE * 2 + (ITEM_PAGE_BTN_WIDTH + ITEM_PAGE_BTN_SPACE) * 0+22,
											"y" : 0,

											"default_image" : ROOT + "content_page_button.tga",
											"over_image" : ROOT + "content_page_button_over.tga",
											"down_image" : ROOT + "content_page_button_down.tga",
										},
										{
											"name" : "item_page_btn2",
											"type" : "radio_button",

											"x" : ITEM_PAGE_SKIP_BTN_WIDTH + ITEM_PAGE_ONCE_BTN_WIDTH + ITEM_PAGE_BTN_SPACE * 2 + (ITEM_PAGE_BTN_WIDTH + ITEM_PAGE_BTN_SPACE) * 1+22,
											"y" : 0,

											"default_image" : ROOT + "content_page_button.tga",
											"over_image" : ROOT + "content_page_button_over.tga",
											"down_image" : ROOT + "content_page_button_down.tga",
										},
										{
											"name" : "item_page_btn3",
											"type" : "radio_button",

											"x" : ITEM_PAGE_SKIP_BTN_WIDTH + ITEM_PAGE_ONCE_BTN_WIDTH + ITEM_PAGE_BTN_SPACE * 2 + (ITEM_PAGE_BTN_WIDTH + ITEM_PAGE_BTN_SPACE) * 2+22,
											"y" : 0,

											"default_image" : ROOT + "content_page_button.tga",
											"over_image" : ROOT + "content_page_button_over.tga",
											"down_image" : ROOT + "content_page_button_down.tga",
										},
										{
											"name" : "item_page_btn4",
											"type" : "radio_button",

											"x" : ITEM_PAGE_SKIP_BTN_WIDTH + ITEM_PAGE_ONCE_BTN_WIDTH + ITEM_PAGE_BTN_SPACE * 2 + (ITEM_PAGE_BTN_WIDTH + ITEM_PAGE_BTN_SPACE) * 3+22,
											"y" : 0,

											"default_image" : ROOT + "content_page_button.tga",
											"over_image" : ROOT + "content_page_button_over.tga",
											"down_image" : ROOT + "content_page_button_down.tga",
										},
										{
											"name" : "item_page_btn5",
											"type" : "radio_button",

											"x" : ITEM_PAGE_SKIP_BTN_WIDTH + ITEM_PAGE_ONCE_BTN_WIDTH + ITEM_PAGE_BTN_SPACE * 2 + (ITEM_PAGE_BTN_WIDTH + ITEM_PAGE_BTN_SPACE) * 4+22,
											"y" : 0,

											"default_image" : ROOT + "content_page_button.tga",
											"over_image" : ROOT + "content_page_button_over.tga",
											"down_image" : ROOT + "content_page_button_down.tga",
										},
										{
											"name" : "item_next_page_btn",
											"type" : "button",

											"x" : ITEM_PAGE_SKIP_BTN_WIDTH + ITEM_PAGE_ONCE_BTN_WIDTH + ITEM_PAGE_BTN_SPACE * 2 + (ITEM_PAGE_BTN_WIDTH + ITEM_PAGE_BTN_SPACE) * 5+22,
											"y" : 0,

											"default_image" : ROOT + "content_next_page.dds",
											"over_image" : ROOT + "content_next_page_over.dds",
											"down_image" : ROOT + "content_next_page_down.dds",

											"vertical_align" : "center",

											"tooltip_text" : localeInfo.SHOP_SEARCH_ITEM_PAGE_NEXT_TOOLTIP,
										},
										{
											"name" : "item_last_page_btn",
											"type" : "button",

											"x" : ITEM_PAGE_SKIP_BTN_WIDTH + ITEM_PAGE_ONCE_BTN_WIDTH * 2 + ITEM_PAGE_BTN_SPACE * 3 + (ITEM_PAGE_BTN_WIDTH + ITEM_PAGE_BTN_SPACE) * 5+22,
											"y" : 0,

											"default_image" : ROOT + "content_last_page.dds",
											"over_image" : ROOT + "content_last_page_over.dds",
											"down_image" : ROOT + "content_last_page_down.dds",

											"vertical_align" : "center",

											"tooltip_text" : localeInfo.SHOP_SEARCH_ITEM_PAGE_LAST_TOOLTIP,
										},
									),
								},
							),
						},
					),
				},
				{
					"name" : "graph",
					"type" : "image",

					"x" : BORDER_X + 1,
					"y" : BORDER_TOP + 1,

					"children" :
					(
						{
							"name" : "graph_close",
							"type" : "button",

							"x" : 779,
							"y" : 50,

							"default_image" : ROOT_GRAPH + "delete_btn.tga",
							"over_image" : ROOT_GRAPH + "delete_btn_over.tga",
							"down_image" : ROOT_GRAPH + "delete_btn_down.tga",
						},
						{
							"name" : "graph_item_name",
							"type" : "text",

							"x" : 9,
							"y" : 51,

							# "color" : ui.GenerateColor(255, 199, 0),

							"text" : "Sword+9",
						},
						{
							"name" : "graph_time_weekly_button",
							"type" : "radio_button",

							"x" : 9,
							"y" : 101,

							"default_image" : ROOT_GRAPH + "unit_button.tga",
							"over_image" : ROOT_GRAPH + "unit_button_over.tga",
							"down_image" : ROOT_GRAPH + "unit_button_down.tga",

							"text" : localeInfo.SHOP_SEARCH_GRAPH_WEEKLY_BUTTON,
						},
						{
							"name" : "graph_time_monthly_button",
							"type" : "radio_button",

							"x" : 67,
							"y" : 101,

							"default_image" : ROOT_GRAPH + "unit_button.tga",
							"over_image" : ROOT_GRAPH + "unit_button_over.tga",
							"down_image" : ROOT_GRAPH + "unit_button_down.tga",

							"text" : localeInfo.SHOP_SEARCH_GRAPH_MONTHLY_BUTTON,
						},
						{
							"name" : "graph_refresh_button",
							"type" : "button",

							"x" : 124,
							"y" : 101,

							"default_image" : ROOT_GRAPH + "refresh_btn.tga",
							"over_image" : ROOT_GRAPH + "refresh_btn_over.tga",
							"down_image" : ROOT_GRAPH + "refresh_btn_down.tga",
						},
						{ "name":"graph_last_updated", "type":"multi_text", "width":250, "x":672-512, "y":101+6, "text":"2021.05.06 19:27 Last Update.", "outline":"1", },
						{
							"name" : "graph_average_price",
							"type" : "line_graph",

							"x" : 10,
							"y" : 135,

							"width" : 691,
							"height" : 219,

							"line_thickness" : 1,

							# "color" : ui.GenerateColor(255, 199, 0),

							"children" :
							(
								{
									"name" : "graph_average_price_cursor",
									"type" : "image",
									"style" : ("not_pick",),

									"x" : 0,
									"y" : 0,

									"image" : ROOT_GRAPH + "ellipse.tga",

									"children" :
									(
										{
											"name" : "graph_average_price_money_icon",
											"type" : "image",
											"style" : ("not_pick",),

											"x" : -16 - 7,
											"y" : 0,

											"vertical_align" : "center",

											"image" : "d:/ymir work/ui/game/windows/money_icon.sub",

											"children" :
											(
												{
													"name" : "graph_average_price_money",
													"type" : "extended_text",

													"x" : 0,
													"y" : 0,

													"vertical_align" : "center",
												},
											),
										},
									),
								},
							),
						},
						{
							"name" : "graph_sold_items",
							"type" : "bar_graph",

							"x" : 10+2,
							"y" : 355,

							"width" : 691,
							"height" : 74,

							# "color" : ui.GenerateColor(255, 199, 0),
						},
						{
							"name" : "graph_sold_x_description",

							"x" : 9,
							"y" : 438,

							"width" : 693,
							"height" : 20,

							"children" :
							(
								{
									"name" : "graph_x_unit_description",
									"type" : "text",

									"x" : 0,
									"y" : 15,

									"text" : localeInfo.SHOP_SEARCH_GRAPH_X_UNIT,
									# "color" : DESC_TEXT_COLOR,
								},
								{
									"name" : "graph_sold_monthly_x_description",

									"x" : 0, "y" : 0,
									"width" : 0, "height" : 0,

									"children" :
									[
										{
											"name" : "graph_sold_monthly_x_desc_%d" % i,
											"type" : "text",

											"x" : 46 * i,
											"y" : 0,

											"text" : "02/%02d" % (i * 2 + 1),
											# "color" : DESC_TEXT_COLOR,
										}
										for i in xrange(15)
									],
								},
								{
									"name" : "graph_sold_weekly_x_description",

									"x" : 0, "y" : 0,
									"width" : 0, "height" : 0,

									"children" :
									[
										{
											"name" : "graph_sold_weekly_desc_%d" % i,
											"type" : "text",

											"x" : 99 * i,
											"y" : 0,

											"text" : "02/%02d" % (i * 2 + 1),
											# "color" : DESC_TEXT_COLOR,
										}
										for i in xrange(7)
									],
								},
							),
						},
						{
							"name" : "graph_sold_y_desc_1",
							"type" : "text",

							"x" : 718,
							"y" : 414,

							"text" : "5",

							"text_vertical_align" : "center",
						},
						{
							"name" : "graph_sold_y_desc_2",
							"type" : "text",

							"x" : 718,
							"y" : 399,

							"text" : "10",

							"text_vertical_align" : "center",
						},
						{
							"name" : "graph_sold_y_desc_3",
							"type" : "text",

							"x" : 718,
							"y" : 384,

							"text" : "15",

							"text_vertical_align" : "center",
						},
						{
							"name" : "graph_sold_y_desc_4",
							"type" : "text",

							"x" : 718,
							"y" : 369,

							"text" : "20",

							"text_vertical_align" : "center",
						},
						{
							"name" : "graph_sold_y_desc_5",
							"type" : "text",

							"x" : 718,
							"y" : 354,

							"text" : "25",

							"text_vertical_align" : "center",
						},
						{
							"name" : "graph_y_unit_description",
							"type" : "text",

							"x" : 785,
							"y" : 438+15,

							"text_horizontal_align" : "right",

							"text" : localeInfo.SHOP_SEARCH_GRAPH_Y_UNIT,
							# "color" : DESC_TEXT_COLOR,
						},
						{
							"name" : "graph_price_y_desc_icon_1",
							"type" : "image",

							"x" : 774,
							"y" : 280-7,

							"image" : "d:/ymir work/ui/game/windows/money_icon.sub",

							"children" :
							(
								{
									"name" : "graph_price_y_desc_1",
									"type" : "text",

									"x" : -5,
									"y" : -1,

									"text_horizontal_align" : "right",
									"vertical_align" : "center",
									"text_vertical_align" : "center",

									"text" : "40.000.000",
								},
							),
						},
						{
							"name" : "graph_price_y_desc_icon_2",
							"type" : "image",

							"x" : 774,
							"y" : 206-7,

							"image" : "d:/ymir work/ui/game/windows/money_icon.sub",

							"children" :
							(
								{
									"name" : "graph_price_y_desc_2",
									"type" : "text",

									"x" : -5,
									"y" : -1,

									"text_horizontal_align" : "right",
									"vertical_align" : "center",
									"text_vertical_align" : "center",

									"text" : "80.000.000",
								},
							),
						},
						{
							"name" : "graph_price_y_desc_icon_3",
							"type" : "image",

							"x" : 774,
							"y" : 133-7,

							"image" : "d:/ymir work/ui/game/windows/money_icon.sub",

							"children" :
							(
								{
									"name" : "graph_price_y_desc_3",
									"type" : "text",

									"x" : -5,
									"y" : -1,

									"text_horizontal_align" : "right",
									"vertical_align" : "center",
									"text_vertical_align" : "center",

									"text" : "120.000.000",
								},
							),
						},
					),
				},
			),
		},
		{
			"name" : "turkish_style",
			"type" : "image",

			"x" : 31+180,
			"y" : 20+45,

			"image" : ROOT + "turkish_style.png",
		},
	),
}
