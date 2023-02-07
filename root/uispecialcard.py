import thenewui as ui
import net
import grp
import wndMgr
import item
import uiToolTip
import uiScriptLocale

COLOR_BG = grp.GenerateColor(0.0, 0.0, 0.0, 0.0)
POSITIONS = [-200, 0, 200]

PHASE_OPENING = 1
PHASE_OPEN = 2
PHASE_CLOSE = 3

TEST_IMAGES = [30041, 30041, 30041]

class SpecialCardReward(ui.Bar):
	def __init__(self):
		ui.Bar.__init__(self, "TOP_MOST")
		self.WindowPhase = 0

		self.BackgroundAlpha = 0.0
		self.ImagesAlpha = 0.0
		self.CoverAlpha = [1.0, 1.0, 1.0]

		self.BackgroundCards = []
		self.CoverCards = []
		self.CardButtons = []

		self.ItemImages = []
		self.ItemIndex = 0

		self.Selected = False
		self.SelectedID = 0
		self.ShowOther = False

		self.BuildWindow()

	def __del__(self):
		ui.Bar.__del__(self)

	def BuildWindow(self):
		self.SetSize(wndMgr.GetScreenWidth(), wndMgr.GetScreenHeight())
		self.SetColor(COLOR_BG)

		self.SelectRewardText = ui.ExpandedImageBox()
		self.SelectRewardText.SetParent(self)
		self.SelectRewardText.LoadImage("d:/ymir work/ui/game/new_gui/special_cards/desc.tga")
		self.SelectRewardText.SetWindowHorizontalAlignCenter()
		self.SelectRewardText.SetWindowVerticalAlignCenter()
		self.SelectRewardText.SetPosition(0, -140)
		self.SelectRewardText.SetAlpha(0.0)
		self.SelectRewardText.Show()

		for x in xrange(3):
			bgCard = ui.ExpandedImageBox()
			bgCard.SetParent(self)
			bgCard.LoadImage("d:/ymir work/ui/game/new_gui/special_cards/background_card.tga")
			bgCard.SetWindowHorizontalAlignCenter()
			bgCard.SetWindowVerticalAlignCenter()
			bgCard.SetPosition(POSITIONS[x], 20)
			bgCard.Hide()
			self.bgCard = bgCard
			self.BackgroundCards.append(self.bgCard)

			coverCard = ui.ExpandedImageBox()
			coverCard.SetParent(self)
			coverCard.LoadImage("d:/ymir work/ui/game/new_gui/special_cards/card_01.tga")
			coverCard.SetWindowHorizontalAlignCenter()
			coverCard.SetWindowVerticalAlignCenter()
			coverCard.SetPosition(POSITIONS[x], 20)
			coverCard.SetAlpha(0.0)
			coverCard.Show()
			self.coverCard = coverCard
			self.CoverCards.append(self.coverCard)

			cardButton = ui.Button()
			cardButton.SetParent(self)
			cardButton.SetUpVisual("d:/ymir work/ui/game/new_gui/special_cards/card_01.tga")
			cardButton.SetOverVisual("d:/ymir work/ui/game/new_gui/special_cards/card_02.tga")
			cardButton.SetDownVisual("d:/ymir work/ui/game/new_gui/special_cards/card_02.tga")
			cardButton.SetWindowHorizontalAlignCenter()
			cardButton.SetWindowVerticalAlignCenter()
			cardButton.SetPosition(POSITIONS[x], 20)
			cardButton.SetEvent(ui.__mem_func__(self.SelectReward), x)
			cardButton.Hide()
			self.cardButton = cardButton
			self.CardButtons.append(self.cardButton)

			itemImage = SpecialImage()
			itemImage.SetParent(bgCard)
			itemImage.LoadItem(TEST_IMAGES[x])
			itemImage.SetWindowHorizontalAlignCenter()
			itemImage.SetWindowVerticalAlignCenter()
			itemImage.Show()
			self.itemImage = itemImage
			self.ItemImages.append(self.itemImage)

		self.ShowOtherButton = ui.Button()
		self.ShowOtherButton.SetParent(self)
		self.ShowOtherButton.SetUpVisual("d:/ymir work/ui/public/xlarge_button_01.sub")
		self.ShowOtherButton.SetOverVisual("d:/ymir work/ui/public/xlarge_button_02.sub")
		self.ShowOtherButton.SetDownVisual("d:/ymir work/ui/public/xlarge_button_03.sub")
		self.ShowOtherButton.SetWindowHorizontalAlignCenter()
		self.ShowOtherButton.SetWindowVerticalAlignCenter()
		self.ShowOtherButton.SetPosition(0, 160)
		self.ShowOtherButton.SetText(uiScriptLocale.OPTION_COUNTRYFLAG_ON + " tot")
		self.ShowOtherButton.SetEvent(ui.__mem_func__(self.OtherRewards))
		self.ShowOtherButton.Hide()

		self.CloseButton = ui.Button()
		self.CloseButton.SetParent(self)
		self.CloseButton.SetUpVisual("d:/ymir work/ui/public/xlarge_button_01.sub")
		self.CloseButton.SetOverVisual("d:/ymir work/ui/public/xlarge_button_02.sub")
		self.CloseButton.SetDownVisual("d:/ymir work/ui/public/xlarge_button_03.sub")
		self.CloseButton.SetWindowHorizontalAlignCenter()
		self.CloseButton.SetWindowVerticalAlignCenter()
		self.CloseButton.SetPosition(0, 190)
		self.CloseButton.SetText(uiScriptLocale.CLOSE)
		self.CloseButton.SetEvent(ui.__mem_func__(self.Close))
		self.CloseButton.Hide()

	def SelectReward(self, index):
		for x in xrange(3):
			self.CardButtons[x].Hide()
		self.SelectedID = index
		self.Selected = True
		self.ShowOtherButton.Show()
		self.CloseButton.Show()
		net.SendChatPacket("/get_card_reward " + str(index))

	def ShowElements(self):
		for x in xrange(3):
			self.BackgroundCards[x].Show()
			self.CardButtons[x].Show()
		pass

	def AddItem(self, itemVnum):
		self.ItemImages[self.ItemIndex].LoadItem(int(itemVnum))
		self.ItemImages[self.ItemIndex].SetWindowHorizontalAlignCenter()
		self.ItemImages[self.ItemIndex].SetWindowVerticalAlignCenter()
		self.ItemIndex += 1

	def OtherRewards(self):
		self.ShowOther = True

	def ResetWindow(self):
		self.WindowPhase = 0
		self.BackgroundAlpha = 0.0
		self.ImagesAlpha = 0.0
		self.CoverAlpha = [1.0, 1.0, 1.0]
		self.Selected = False
		self.SelectedID = 0
		self.ItemIndex = 0
		self.ShowOther = False
		self.ShowOtherButton.Hide()
		self.CloseButton.Hide()
		self.SelectRewardText.SetAlpha(0.0)
		self.SetColor(grp.GenerateColor(0.0, 0.0, 0.0, self.BackgroundAlpha))
		for x in xrange(3):
			self.BackgroundCards[x].Hide()
			self.CoverCards[x].SetAlpha(0.0)
			self.CardButtons[x].Hide()
			self.CoverCards[x].Show()

	def OnUpdate(self):
		if self.WindowPhase == PHASE_OPENING:
			if self.BackgroundAlpha < 0.6:
				self.BackgroundAlpha += 0.03
				self.SetColor(grp.GenerateColor(0.0, 0.0, 0.0, self.BackgroundAlpha))

			if self.ImagesAlpha < 1.0:
				self.ImagesAlpha += 0.04
				for x in xrange(3):
					self.CoverCards[x].SetAlpha(self.ImagesAlpha)
					self.SelectRewardText.SetAlpha(self.ImagesAlpha)
			else:
				self.WindowPhase = PHASE_OPEN
				self.ShowElements()

		if self.ShowOther:
			for x in xrange(3):
				if self.CoverAlpha[x] > 0.0:
					self.CoverAlpha[x] -= 0.05
					self.CoverCards[x].SetAlpha(self.CoverAlpha[x])
				else:
					self.CoverCards[x].Hide()

		if self.Selected:
			if self.CoverAlpha[self.SelectedID] > 0.0:
				self.CoverAlpha[self.SelectedID] -= 0.05
				self.CoverCards[self.SelectedID].SetAlpha(self.CoverAlpha[self.SelectedID])
			else:
				self.CoverCards[self.SelectedID].Hide()

	def Open(self):
		self.WindowPhase = PHASE_OPENING
		self.Show()

	def Close(self):
		self.ResetWindow()
		self.Hide()


class SpecialImage(ui.Window):
	def __init__(self):
		ui.Window.__init__(self)

		self.SetSize(32, 96)
		self.Show()

		self.itemImage = ui.ImageBox()
		self.itemImage.SetParent(self)
		self.itemImage.Show()

		self.itemToolTip = uiToolTip.ItemToolTip()

	def __del__(self):
		ui.Window.__del__(self)

	def LoadItem(self, itemVnum):
		item.SelectItem(int(itemVnum))
		self.itemToolTip.ClearToolTip()
		self.itemToolTip.SetItemToolTip(int(itemVnum))
		self.itemToolTip.HideToolTip()

		self.itemImage.LoadImage(item.GetIconImageFileName())
		self.SetSize(self.itemImage.GetWidth(), self.itemImage.GetHeight())

	def __ShowToolTip(self):
		self.itemToolTip.ShowToolTip()

	def __HideToolTip(self):
		self.itemToolTip.HideToolTip()

	def OnUpdate(self):
		if self.itemImage.IsIn():
			self.itemToolTip.ShowToolTip()
		else:
			self.itemToolTip.HideToolTip()
