import uiScriptLocale
import localeInfo

BOARD_WIDTH = 350
BOARD_HEIGHT = 485

window = {
	"name" : "ModelPreviewWindow",
	"style" : ("movable", "float", "animation",),
	
	"x" : 114,
	"y" : 132,

	"width" : BOARD_WIDTH,
	"height" : BOARD_HEIGHT,
	
	"children" :
	(
		## MainBoard
		{
			"name" : "Board",
			"type" : "board",
			"style" : ("attach","ltr"),

			"x" : 0,
			"y" : 0,

			"width" : BOARD_WIDTH,
			"height" : BOARD_HEIGHT,
			
			"children" :
			(
				## Title Bar
				{
					"name" : "TitleBar",
					"type" : "titlebar",
					"style" : ("attach",),

					"x" : 6, "y" : 7, "width" : BOARD_WIDTH - 13,
					
					"children" :
					(
						{ "name" : "TitleName", "type" : "text", "x" : BOARD_WIDTH / 2, "y" : 3, "text": "Previzualizare", "text_horizontal_align":"center" },
					),
				},
				
				{
					"name" : "RenderTarget",
					"type" : "render_target_v2",
							
					"x" : 7,
					"y" : 30,
							
					"width" : 336,
					"height" : 448, #306
							
					"index" : 66,
					
					"children" : 
					(
						{
							"name" : "MouseTipText",
							"type" : "text",
							
							"horizontal_align" : "right",
							"vertical_align" : "bottom",
							"text_horizontal_align" : "right",
							"text_vertical_align" : "bottom",
							
							"x" : 15,
							"y" : 15,
							
							"text" : "|Eicon/emoji/m_wheel.tga|e Zoom",
						},	
						{
							"name" : "MouseTipText2",
							"type" : "text",
							
							"horizontal_align" : "right",
							"vertical_align" : "bottom",
							"text_horizontal_align" : "right",
							"text_vertical_align" : "bottom",
							
							"x" : 125,
							"y" : 15,
							
							"text" : "|Eicon/emoji/m_left.tga|e to rotate camera",
						},
					),
				},
				
				#{
				#	"name" : "ObjectRotationButton",
				#	"type" : "drag_button",
				#	
				#	"x" : 7,
				#	"y" : 30,
				#			
				#	"width" : 336,
				#	"height" : 448,
				#},
			),
		}, ## MainBoard End
	),
}
