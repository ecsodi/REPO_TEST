import dbg
import thenewui as ui
import systemSetting
import net
import chat
import app
import localeInfo
import constInfo
import ShapeSkin as chrmgr
import CacheEffect as player
import background

blockMode = 0

class OptionDialog(ui.ScriptWindow):

	def __init__(self):
		ui.ScriptWindow.__init__(self)
		self.__Initialize()
		self.__Load()

	def __del__(self):
		ui.ScriptWindow.__del__(self)

	def __Initialize(self):
		self.tilingMode = 0
		self.titleBar = 0
		self.tilingApplyButton = 0
		self.cameraModeButtonList = []
		self.fogModeButtonList = []
		self.tilingModeButtonList = []
		self.ctrlShadowQuality = 0
		self.fovSlider = 0

	def Destroy(self):
		self.ClearDictionary()

		self.__Initialize()

	def __Load_LoadScript(self, fileName):
		try:
			pyScriptLoader = ui.PythonScriptLoader()
			pyScriptLoader.LoadScriptFile(self, fileName)
		except:
			import exception
			exception.Abort("System.OptionDialog.__Load_LoadScript")

	def __Load_BindObject(self):
		try:
			GetObject = self.GetChild
			self.titleBar = GetObject("titlebar")
			self.cameraModeButtonList.append(GetObject("camera_short"))
			self.cameraModeButtonList.append(GetObject("camera_long"))
			self.fogModeButtonList.append(GetObject("fog_level0"))
			self.fogModeButtonList.append(GetObject("fog_level1"))
			self.fogModeButtonList.append(GetObject("fog_level2"))
			self.tilingModeButtonList.append(GetObject("tiling_cpu"))
			self.tilingModeButtonList.append(GetObject("tiling_gpu"))
			self.tilingApplyButton=GetObject("tiling_apply")
			#self.ctrlShadowQuality = GetObject("shadow_bar")
			self.fovSlider = GetObject("fov_bar")
		except:
			import exception
			exception.Abort("OptionDialog.__Load_BindObject")

	def __Load(self):
		self.__Load_LoadScript("uiscript/systemoptiondialog.py")
		self.__Load_BindObject()

		self.SetCenterPosition()

		self.titleBar.SetCloseEvent(ui.__mem_func__(self.Close))

#		self.ctrlShadowQuality.SetSliderPos(float(systemSetting.GetShadowLevel()) / 5.0)
#		self.ctrlShadowQuality.SetEvent(ui.__mem_func__(self.OnChangeShadowQuality))

		self.fovSlider.SetSliderPos(float(systemSetting.GetFieldOfView() * 2))
		self.fovSlider.SetEvent(ui.__mem_func__(self.OnChangeFOV))

		self.cameraModeButtonList[0].SAFE_SetEvent(self.__OnClickCameraModeShortButton)
		self.cameraModeButtonList[1].SAFE_SetEvent(self.__OnClickCameraModeLongButton)

		self.fogModeButtonList[0].SAFE_SetEvent(self.__OnClickFogModeLevel0Button)
		self.fogModeButtonList[1].SAFE_SetEvent(self.__OnClickFogModeLevel1Button)
		self.fogModeButtonList[2].SAFE_SetEvent(self.__OnClickFogModeLevel2Button)

		self.tilingModeButtonList[0].SAFE_SetEvent(self.__OnClickTilingModeCPUButton)
		self.tilingModeButtonList[1].SAFE_SetEvent(self.__OnClickTilingModeGPUButton)

		self.tilingApplyButton.SAFE_SetEvent(self.__OnClickTilingApplyButton)

		self.__SetCurTilingMode()

		self.__ClickRadioButton(self.fogModeButtonList, constInfo.GET_FOG_LEVEL_INDEX())
		self.__ClickRadioButton(self.cameraModeButtonList, constInfo.GET_CAMERA_MAX_DISTANCE_INDEX())

	def __OnClickTilingModeCPUButton(self):
		self.__NotifyChatLine(localeInfo.SYSTEM_OPTION_CPU_TILING_1)
		self.__NotifyChatLine(localeInfo.SYSTEM_OPTION_CPU_TILING_2)
		self.__NotifyChatLine(localeInfo.SYSTEM_OPTION_CPU_TILING_3)
		self.__SetTilingMode(0)

	def __OnClickTilingModeGPUButton(self):
		self.__NotifyChatLine(localeInfo.SYSTEM_OPTION_GPU_TILING_1)
		self.__NotifyChatLine(localeInfo.SYSTEM_OPTION_GPU_TILING_2)
		self.__NotifyChatLine(localeInfo.SYSTEM_OPTION_GPU_TILING_3)
		self.__SetTilingMode(1)

	def __OnClickTilingApplyButton(self):
		self.__NotifyChatLine(localeInfo.SYSTEM_OPTION_TILING_EXIT)
		if 0==self.tilingMode:
			background.EnableSoftwareTiling(1)
		else:
			background.EnableSoftwareTiling(0)

		net.ExitGame()


	def __ClickRadioButton(self, buttonList, buttonIndex):
		try:
			selButton=buttonList[buttonIndex]
		except IndexError:
			return

		for eachButton in buttonList:
			eachButton.SetUp()

		selButton.Down()


	def __SetTilingMode(self, index):
		self.__ClickRadioButton(self.tilingModeButtonList, index)
		self.tilingMode=index

	def __SetCameraMode(self, index):
		constInfo.SET_CAMERA_MAX_DISTANCE_INDEX(index)
		self.__ClickRadioButton(self.cameraModeButtonList, index)

	def __SetFogLevel(self, index):
		constInfo.SET_FOG_LEVEL_INDEX(index)
		self.__ClickRadioButton(self.fogModeButtonList, index)

	def __OnClickCameraModeShortButton(self):
		self.__SetCameraMode(0)

	def __OnClickCameraModeLongButton(self):
		self.__SetCameraMode(1)

	def __OnClickFogModeLevel0Button(self):
		self.__SetFogLevel(0)

	def __OnClickFogModeLevel1Button(self):
		self.__SetFogLevel(1)

	def __OnClickFogModeLevel2Button(self):
		self.__SetFogLevel(2)

	def OnChangeShadowQuality(self):
		pos = self.ctrlShadowQuality.GetSliderPos()
		systemSetting.SetShadowLevel(int(pos / 0.2))

	def OnChangeFOV(self):
		pos = self.fovSlider.GetSliderPos() / 2
		systemSetting.SetFieldOfView(pos)

	def OnCloseInputDialog(self):
		self.inputDialog.Close()
		self.inputDialog = None
		return True

	def OnCloseQuestionDialog(self):
		self.questionDialog.Close()
		self.questionDialog = None
		return True

	def OnPressEscapeKey(self):
		self.Close()
		return True

	def Show(self):
		ui.ScriptWindow.Show(self)

	def Close(self):
		self.__SetCurTilingMode()
		self.Hide()

	def __SetCurTilingMode(self):
		if background.IsSoftwareTiling():
			self.__SetTilingMode(0)
		else:
			self.__SetTilingMode(1)

	def __NotifyChatLine(self, text):
		chat.AppendChat(chat.CHAT_TYPE_INFO, text)

