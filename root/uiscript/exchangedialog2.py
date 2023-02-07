#ExchangeDialog.py ~ 24 Slot Item
#Developed by Samuel
import uiScriptLocale
 
ROOT = "d:/ymir work/ui/game/"
 
window = {
        "name" : "ExchangeDialog",
 
        "x" : 0,
        "y" : 0,
 
        "style" : ("movable", "float","animation",),
 
        "width" : 400,
        "height" : 200,
 
        "children" :
        (
                {
                        "name" : "board",
                        "type" : "board",
                        "style" : ("attach",),
 
                        "x" : 0,
                        "y" : 0,
 
                        "width" : 400,
                        "height" : 200,
 
                        "children" :
                        (
                                ## Title
                                {
                                        "name" : "TitleBar",
                                        "type" : "titlebar",
                                        "style" : ("attach",),
 
                                        "x" : 8,
                                        "y" : 8,
 
                                        "width" : 384,
                                        "color" : "gray",
 
                                        "children" :
                                        (
                                                { "name":"TitleName", "type":"text", "x":192, "y":3, "text":uiScriptLocale.EXCHANGE_TITLE, "text_horizontal_align":"center" },
                                        ),
                                },
 
                                ## MiddleBar
                                {
                                        "name" : "Middle_Bar",
                                        "type" : "image",
 
                                        "x" : 200,
                                        "y" : 31,
 
                                        "image" : ROOT + "windows/middlebar.sub",
                                },
 
                                ## Owner
                                {
                                        "name" : "Owner",
                                        "type" : "window",
 
                                        "x" : 200,
                                        "y" : 33,
 
                                        "width" : 200,
                                        "height" : 150,
 
                                        "children" :
                                        (
                                                {
                                                        "name" : "Owner_Slot",
                                                        "type" : "grid_table",
 
                                                        "start_index" : 0,
 
                                                        "x" : 0,
                                                        "y" : 0,
 
                                                        "x_count" : 6,
                                                        "y_count" : 4,
                                                        "x_step" : 32,
                                                        "y_step" : 32,
                                                        "x_blank" : 0,
                                                        "y_blank" : 0,
 
                                                        "image" : "d:/ymir work/ui/public/Slot_Base.sub",
                                                },
                                                {
                                                        "name" : "Owner_Money",
                                                        "type" : "button",
 
                                                        "x" : 0,
                                                        "y" : 136,
 
                                                        #"image" : "d:/ymir work/ui/public/parameter_slot_02.sub",
 
                                                        "default_image" : "d:/ymir work/ui/public/parameter_slot_02.sub",
                                                        "over_image" : "d:/ymir work/ui/public/parameter_slot_02.sub",
                                                        "down_image" : "d:/ymir work/ui/public/parameter_slot_02.sub",
 
                                                        "children" :
                                                        (
                                                                {
                                                                        "name" : "Owner_Money_Value",
                                                                        "type" : "text",
 
                                                                        "x" : 59,
                                                                        "y" : 2,
 
                                                                        "text" : "1234567",
 
                                                                        "text_horizontal_align" : "right",
                                                                },
                                                        ),
                                                },
                                                {
                                                        "name" : "Owner_Accept_Light",
                                                        "type" : "button",
 
                                                        "x" : 62,
                                                        "y" : 135,
 
                                                        "default_image" : "d:/ymir work/ui/game/windows/accept_button_off.sub",
                                                        "over_image" : "d:/ymir work/ui/game/windows/accept_button_off.sub",
                                                        "down_image" : "d:/ymir work/ui/game/windows/accept_button_on.sub",
                                                },
                                                {
                                                        "name" : "Owner_Accept_Button",
                                                        "type" : "toggle_button",
 
                                                        "x" : 85,
                                                        "y" : 135,
 
                                                        "text" : uiScriptLocale.EXCHANGE_ACCEPT,
 
                                                        "default_image" : "d:/ymir work/ui/public/small_button_01.sub",
                                                        "over_image" : "d:/ymir work/ui/public/small_button_02.sub",
                                                        "down_image" : "d:/ymir work/ui/public/small_button_03.sub",
                                                },
                                        ),
                                },
 
                                ## Target
                                {
                                        "name" : "Target",
                                        "type" : "window",
 
                                        "x" : 10,
                                        "y" : 33,
 
                                        "width" : 200,
                                        "height" : 150,
 
                                        "children" :
                                        (
                                                {
                                                        "name" : "Target_Slot",
                                                        "type" : "grid_table",
 
                                                        "start_index" : 0,
 
                                                        "x" : 0,
                                                        "y" : 0,
 
                                                        "x_count" : 6,
                                                        "y_count" : 4,
                                                        "x_step" : 32,
                                                        "y_step" : 32,
                                                        "x_blank" : 0,
                                                        "y_blank" : 0,
 
                                                        "image" : "d:/ymir work/ui/public/Slot_Base.sub",
                                                },
                                                {
                                                        "name" : "Target_Money",
                                                        "type" : "image",
 
                                                        "x" : 0,
                                                        "y" : 135,
 
                                                        "image" : "d:/ymir work/ui/public/parameter_slot_02.sub",
 
                                                        "children" :
                                                        (
                                                                {
                                                                        "name" : "Target_Money_Value",
                                                                        "type" : "text",
 
                                                                        "x" : 59,
                                                                        "y" : 2,
 
                                                                        "text" : "1234567",
 
                                                                        "text_horizontal_align" : "right",
                                                                },
                                                        ),
                                                },
                                                {
                                                        "name" : "Target_Accept_Light",
                                                        "type" : "button",
 
                                                        "x" : 62,
                                                        "y" : 135,
 
                                                        "default_image" : "d:/ymir work/ui/game/windows/accept_button_off.sub",
                                                        "over_image" : "d:/ymir work/ui/game/windows/accept_button_off.sub",
                                                        "down_image" : "d:/ymir work/ui/game/windows/accept_button_on.sub",
                                                },
                                        ),
                                },
                        ),
                },
        ),
}