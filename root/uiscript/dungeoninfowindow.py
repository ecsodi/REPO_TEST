import app
import uiScriptLocale

BOARD_WIDTH = 515
BOARD_HEIGHT = 420

INNER_RIGHT_BOARD_WIDTH = 190
INNER_RIGHR_BOARD_HEIGH = 265

INNER_RIGHT_BOARD_X = INNER_RIGHT_BOARD_WIDTH + 4
INNER_RIGHR_BOARD_Y = INNER_RIGHR_BOARD_HEIGH

ROOT = "d:/ymir work/ui/game/dungeon_info/"

window = {
	"name" : "DungeonInfoWindow",
	"style" : ("movable", "float",),

	"x" : 0,
	"y" : 0,

	"width" : BOARD_WIDTH,
	"height" : BOARD_HEIGHT,

	"children" :
	(
		## Main Window Board
		{
			"name" : "Board",
			"type" : "board",
			"style" : ("attach", "ltr"),

			"x" : 0,
			"y" : 0,

			"width" : BOARD_WIDTH,
			"height" : BOARD_HEIGHT,

			"children" :
			(
				## Main Window Title Bar
				{
					"name" : "TitleBar",
					"type" : "titlebar",
					"style" : ("attach",),

					"x" : 6,
					"y" : 7,

					"width" : BOARD_WIDTH - 13,

					"children" :
					(
						{
							"name" : "TitleText",
							"type" : "text",

							"x" : 0,
							"y" : -2,

							"text" : uiScriptLocale.DUNGEON_INFO_1,
							"all_align" : "center"
						},
					),
				},

				{
					## Board Container
					"name" : "BoardContainer",
					"type" : "window",
					"style" : ("attach",),

					"x" : 0,
					"y" : 32,

					"width" : 450,
					"height" : 543,
					
					"image" : ROOT + "inner_bg.jpg",
					"horizontal_align" : "center",

					"children" :
					(
						## Dungeon Title Name ( Background Image )
						{
							"name" : "TitleBackgroundImage",
							"type" : "image",
							"style" : ("attach",),

							"x" : 0,
							"y" : 3,
							"horizontal_align" : "center",

							"image" : ROOT + "title_bg.png",

							"children" : (
								## Dungeon Title Name ( Text )
								{
									"name" : "TitleNameText",
									"type" : "text",

									"x" : 10,
									"y" : 2,
									"text_horizontal_align" : "left",

									"text" : "",
									"fontname" : "Verdana:17",
									"color" : 0xFFC1C1C1,
									"outline" : 1,
								},


							),
						},

						## Dungeon Preview / Render Image ( Render / Image )
						{
							"name" : "PreviewBackgroundImg",
							"type" : "image",
							"style" : ("attach",),

							"x" : 170,
							"y" : 5,
							"horizontal_align" : "right",

							"image" : ROOT + "preview_bg.jpg",

							"children" : (
								## Dungeon Preview Name ( Text )
								{
									"name" : "PreviewNameText",
									"type" : "text",

									"x" : INNER_RIGHT_BOARD_X / 2,
									"y" : 2,
									"text_horizontal_align" : "center",

									"text" : "",
									"fontname" : "Verdana:17",
									"color" : 0xFFC1C1C1,
									"outline" : 1,
								},
							),
						},
						## Dungeon Preview ( Render )
						{
							"name" : "PreviewRender",
							"type" : "render_target",

							"x" : 170,
							"y" : 30,
							"horizontal_align" : "right",

							"width" : INNER_RIGHT_BOARD_WIDTH,
							"height" : INNER_RIGHR_BOARD_HEIGH - 55,

							"index" : 2,

							"children" : (
								## Teleport (Warp) ( Button )
								{
									"name" : "WarpButton",
									"type" : "button",

									"x" : 190,
									"y" : 20,
									
									"horizontal_align" : "right",
									"vertical_align" : "bottom",
									
									"tooltip_text" : "Teleportare",
									"tooltip_x" : 0,
									"tooltip_y" : -20,

									"default_image" : "d:/ymir work/ui/minigame/miniboss/btn_enter1.sub",
									"over_image" : "d:/ymir work/ui/minigame/miniboss/btn_enter2.sub",
									"down_image" : "d:/ymir work/ui/minigame/miniboss/btn_enter3.sub",
								},
							),
						},

						# {
							# "name" : "ScrollButton",
							# "type" : "expanded_image",

							# "x" : 130,
							# "y" : 26,

							# "width" : 32,
							# "height" : 128,

							# "vertical_align" : "bottom",

							# "image" : ROOT + "scroll_down.png",
						# },

						{
							"name" : "ScrollBar",
							"type" : "scrollbar",

							"x" : 240,
							"y" : 15,

							"size" : 350,
						},

						# Dungeon Button List ( ThinBoard )
						{
							"name" : "ButtonListThinBoard",
							"type" : "image",

							"x" : -25,
							"y" : 1,
							"image" : "ranking/ranking_border.png",

						},

						## Dungeon Information Window
						{
							"name" : "InformationWindow",
							"type" : "window",

							"x" : INNER_RIGHT_BOARD_X,
							"y" : INNER_RIGHR_BOARD_HEIGH,
							"horizontal_align" : "right",

							"width" : INNER_RIGHT_BOARD_WIDTH,
							"height" : INNER_RIGHR_BOARD_HEIGH + 15,

							"children" : (

								## Dungeon Required Items
								{
									"name" : "RequiredItemBackgroundImg",
									"type" : "image",
									"style" : ("attach",),

									"x" : 166,
									"y" : -20,

									"image" : ROOT + "item_slots_bg.jpg",
									"horizontal_align" : "right",

									"children" : (
										## Dungeon Required Items ( Text )
										{
											"name" : "RequiredItemText",
											"type" : "text",

											"x" : 12,
											"y" : 18,

											"text" : "Iteme",
										},
										## Dungeon Required Items ( Slots )
										{
											"name" : "RequiredItemSlot",
											"type" : "slot",

											"x" : 57,
											"y" : 10,

											"width" : 130,
											"height" : 32,

											"image" : "d:/ymir work/ui/pet/skill_button/skill_enable_button.sub",

											"slot" : (
												{ "index" : 0, "x" : 0, "y" : 0, "width" : 32, "height" : 32 },
												{ "index" : 1, "x" : 32 + 12, "y" : 0, "width" : 32, "height" : 32 },
												{ "index" : 2, "x" : 64 + 23, "y" : 0, "width" : 32, "height" : 32 },
											),
										},
									)
								},

								{
									"name" : "MyPointsWindow",
									"type" : "window",

									"x" : INNER_RIGHT_BOARD_X - 3,
									"y" : -85 + 30,
									"horizontal_align" : "right",

									"width" : INNER_RIGHT_BOARD_WIDTH,
									"height" : 0,

									"children" : (
													# Personal Stats
													{
														"name" : "DungeonInfoPersonalStats",
														"type" : "text",
	
														"x" : 0,
														"y" : -5,
														"all_align" : "center",
	
														"text" : uiScriptLocale.DUNGEON_INFO_1,
	
														"fontname" : "Verdana:16",
														"outline" : 1,
													},
									),
								},
								####################################################
								####################################################

								{
									"name" : "InformationThinBoard",
									"type" : "thinboard",

									"x" : 166,
									"y" : 55,

									"width" : INNER_RIGHT_BOARD_WIDTH,
									"height" : 55,

									"horizontal_align" : "right",

									"children" : (
										## Dungeon Type
										{
											"name" : "TypeText", "type" : "text", "x" : 10, "y" : 8,
											"text" : "",
										},
										## Dungeon Level Limit
										{
											"name" : "LevelLimitText", "type" : "text", "x" : 10, "y" : 8 + 15 * 1,
											"text" : "",
										},
										## Dungeon Party Limit ( Members )
										{
											"name" : "MemberLimitText", "type" : "text", "x" : 10, "y" : 8 + 15 * 2,
											"text" : "",
										},
										## Dungeon Duration
										{
											"name" : "DurationText", "type" : "text", "x" : 10, "y" : 8 + 15 * 3,
											"text" : "",
										},
										## Dungeon Cooldown
										{
											"name" : "CooldownText", "type" : "text", "x" : 10, "y" : 8 + 15 * 2,
											"text" : "",
										},
										## Dungeon Location Map Name
										{
											"name" : "LocationText", "type" : "text", "x" : 10, "y" : 8 + 15 * 5,
											"text" : "",
										},
										## Dungeon Entrace Map Name
										{
											"name" : "EntraceText", "type" : "text", "x" : 10, "y" : 8 + 15 * 6,
											"text" : "",
										},
									)
								},
								
								## Dungeon Element Icon ( Image )
								{
									"name" : "ElementalImage",
									"type" : "image",
									"style" : ("attach",),

									"x" : 25, #0,
									"y" : 85,
									"horizontal_align" : "center",

									"image" : "d:/ymir work/ui/game/12zi/element/dark.sub",
								},
							),
						},

						## Help ToolTip Button
						{
							"name" : "HelpToolTipButton",
							"type" : "button",

							"x" : 440,
							"y" : 9,

							"default_image" : "d:/ymir work/ui/pattern/q_mark_01.tga",
							"over_image" : "d:/ymir work/ui/pattern/q_mark_02.tga",
							"down_image" : "d:/ymir work/ui/pattern/q_mark_02.tga",
						},
					),
				},
			)
		},
	)
}
