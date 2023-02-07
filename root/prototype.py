import dbg
import app
import localeInfo
import wndMgr
import systemSetting
import mouseModule
import networkModule
import constInfo
import cfg

if constInfo.ENABLE_PASTE_FEATURE:
	try:
		import thenewui as ui
		ui.EnablePaste(True)
	except:
		import exception
		exception.Abort("Failed to ENABLE_PASTE_FEATURE")

def GetFont():
	font = ""
	try:
		font = cfg.Get(cfg.SAVE_GENERAL, "FONT")
	except IOError:
		pass
	return font
	
def RunApp():
	app.SetHairColorEnable(constInfo.HAIR_COLOR_ENABLE)
	app.SetArmorSpecularEnable(constInfo.ARMOR_SPECULAR_ENABLE)
	app.SetWeaponSpecularEnable(constInfo.WEAPON_SPECULAR_ENABLE)

	app.SetMouseHandler(mouseModule.mouseController)
	wndMgr.SetMouseHandler(mouseModule.mouseController)
	wndMgr.SetScreenSize(systemSetting.GetWidth(), systemSetting.GetHeight())
	
	if GetFont() == "0":
		localeInfo.UI_DEF_FONT = "Tahoma:12"
		localeInfo.UI_DEF_FONT_LARGE = "Tahoma:14"
		localeInfo.UI_DEF_FONT_SMALL = "Tahoma:9"
		
	
	if GetFont() == "1":
		localeInfo.UI_DEF_FONT = "Georgia:14"
		localeInfo.UI_DEF_FONT_LARGE = "Georgia:16"
		localeInfo.UI_DEF_FONT_SMALL = "Georgia:14"
		
	if GetFont() == "2":
		localeInfo.UI_DEF_FONT = "Arial:12"
		localeInfo.UI_DEF_FONT_LARGE = "Arial:14"
		localeInfo.UI_DEF_FONT_SMALL = "Arial:9"
		
	if GetFont() == "3":
		localeInfo.UI_DEF_FONT = "Verdana:12"
		localeInfo.UI_DEF_FONT_LARGE = "Verdana:14"
		localeInfo.UI_DEF_FONT_SMALL = "Verdana:9"
		
	if GetFont() == "4":
		localeInfo.UI_DEF_FONT = "Andale Mono:12"
		localeInfo.UI_DEF_FONT_LARGE = "Andale Mono:14"
		localeInfo.UI_DEF_FONT_SMALL = "Andale Mono:9"

	try:
		app.Create(localeInfo.APP_TITLE, systemSetting.GetWidth(), systemSetting.GetHeight(), 1)
	except RuntimeError, msg:
		msg = str(msg)
		if "CREATE_DEVICE" == msg:
			dbg.LogBox("Sorry, Your system does not support 3D graphics,\r\nplease check your hardware and system configeration\r\nthen try again.")
		else:
			dbg.LogBox("Metin2.%s" % msg)
		return

	app.SetCamera(1500.0, 30.0, 0.0, 180.0)

	if not mouseModule.mouseController.Create():
		return

	mainStream = networkModule.MainStream()
	mainStream.Create()
	mainStream.SetLogoPhase()

	app.Loop()

	mainStream.Destroy()
	del mouseModule.mouseController

RunApp()