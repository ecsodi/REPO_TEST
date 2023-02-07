WINDOW_WIDTH = 410
WINDOW_HEIGHT = 440

RENDER_TARGET_INDEX = 66

window = {
	"name" : "RenderTargetWindow",

	"x" : 0,
	"y" : 0,

	"style" : ("movable", "float",),

	"width" : WINDOW_WIDTH,
	"height" : WINDOW_HEIGHT,

	"children":
	(
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
							"name" : "TitleName",
							"type" : "text",

							"x" : (WINDOW_WIDTH - 15) / 2,
							"y" : 3,

							"text" : "Preview",
							"text_horizontal_align":"center"
						},
					),
				},

				# RenderView
				{
					"name" : "RenderTarget",
					"type" : "render_target",
					"style" : ("attach",),

					"x" : 10,
					"y" : 30,

					"width" : 390,
					"height" : 400,

					"index" : RENDER_TARGET_INDEX,
					"children" :
					(
						{
							"name" : "MoveUp",
							"type" : "button",

							"x" : 110,
							"y" : 375,

							"tooltip_text" : "Move Up",

							"default_image" : "d:/ymir work/ui/game/monster_card/button/up_camera/up_camera_button_default.sub",
							"over_image" : "d:/ymir work/ui/game/monster_card/button/up_camera/up_camera_button_over.sub",
							"down_image" : "d:/ymir work/ui/game/monster_card/button/up_camera/up_camera_button_down.sub",
						},

						{
							"name" : "MoveDown",
							"type" : "button",

							"x" : 130,
							"y" : 375,

							"tooltip_text" : "Move Down",

							"default_image" : "d:/ymir work/ui/game/monster_card/button/down_camera/down_camera_button_default.sub",
							"over_image" : "d:/ymir work/ui/game/monster_card/button/down_camera/down_camera_button_over.sub",
							"down_image" : "d:/ymir work/ui/game/monster_card/button/down_camera/down_camera_button_down.sub",
						},
						{
							"name" : "RotateLeft",
							"type" : "button",

							"x" : 150,
							"y" : 375,

							"tooltip_text" : "Left Rotate",

							"default_image" : "d:/ymir work/ui/game/monster_card/button/left_rotation/left_rotation_button_default.sub",
							"over_image" : "d:/ymir work/ui/game/monster_card/button/left_rotation/left_rotation_button_over.sub",
							"down_image" : "d:/ymir work/ui/game/monster_card/button/left_rotation/left_rotation_button_down.sub",
						},

						{
							"name" : "RotateRight",
							"type" : "button",

							"x" : 170,
							"y" : 375,

							"tooltip_text" : "Right Rotate",

							"default_image" : "d:/ymir work/ui/game/monster_card/button/right_rotation/right_rotation_button_default.sub",
							"over_image" : "d:/ymir work/ui/game/monster_card/button/right_rotation/right_rotation_button_over.sub",
							"down_image" : "d:/ymir work/ui/game/monster_card/button/right_rotation/right_rotation_button_down.sub",
						},

						{
							"name" : "Refresh",
							"type" : "button",

							"x" : 190,
							"y" : 375,

							"tooltip_text" : "Refresh",

							"default_image" : "d:/ymir work/ui/game/monster_card/button/mv_reset/mv_reset_button_default.sub",
							"over_image" : "d:/ymir work/ui/game/monster_card/button/mv_reset/mv_reset_button_over.sub",
							"down_image" : "d:/ymir work/ui/game/monster_card/button/mv_reset/mv_reset_button_down.sub",
						},

						{
							"name" : "DoEmotion",
							"type" : "button",

							"x" : 210,
							"y" : 375,

							"tooltip_text" : "Emotion",

							"default_image" : "d:/ymir work/ui/game/monster_card/button/mv_reset/mv_reset_button_default.sub",
							"over_image" : "d:/ymir work/ui/game/monster_card/button/mv_reset/mv_reset_button_over.sub",
							"down_image" : "d:/ymir work/ui/game/monster_card/button/mv_reset/mv_reset_button_down.sub",
						},

						{
							"name" : "ZoomIn",
							"type" : "button",

							"x" : 230,
							"y" : 375,

							"tooltip_text" : "Zoom In",

							"default_image" : "d:/ymir work/ui/game/monster_card/button/zoomin/zoomin_rotation_button_default.sub",
							"over_image" : "d:/ymir work/ui/game/monster_card/button/zoomin/zoomin_rotation_button_over.sub",
							"down_image" : "d:/ymir work/ui/game/monster_card/button/zoomin/zoomin_rotation_button_down.sub",
						},

						{
							"name" : "ZoomOut",
							"type" : "button",

							"x" : 250,
							"y" : 375,

							"tooltip_text" : "Zoom Out",

							"default_image" : "d:/ymir work/ui/game/monster_card/button/zoomout/zoomin_rotation_button_default.sub",
							"over_image" : "d:/ymir work/ui/game/monster_card/button/zoomout/zoomin_rotation_button_over.sub",
							"down_image" : "d:/ymir work/ui/game/monster_card/button/zoomout/zoomin_rotation_button_down.sub",
						},
					),
				},
			),
		},
	),
}