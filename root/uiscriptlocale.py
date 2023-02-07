import app

OPTION_SHADOW = "SHADOW"
CODEPAGE = str(app.GetDefaultCodePage())

def LoadLocaleFile(srcFileName, localeDict):
	localeDict["CUBE_INFO_TITLE"] = "Recipe"
	localeDict["CUBE_REQUIRE_MATERIAL"] = "Requirements"
	localeDict["CUBE_REQUIRE_MATERIAL_OR"] = "or"

	try:
		lines = open(srcFileName, "r").readlines()
	except IOError:
		import dbg
		dbg.LogBox("LoadUIScriptLocaleError(%(srcFileName)s)" % locals())
		app.Abort()

	for line in lines:
		tokens = line[:-1].split("\t")

		if len(tokens) >= 2:
			localeDict[tokens[0]] = tokens[1]
		else:
			print len(tokens), lines.index(line), line

name = app.GetLocalePath()

LOGIN_PATH = "locale/ui/login/"
EMPIRE_PATH = "locale/ui/empire/"
GUILD_PATH = "locale/ui/guild/"
SELECT_PATH = "locale/ui/select/"
WINDOWS_PATH = "locale/ui/windows/"
MAPNAME_PATH = "locale/ui/mapname/"
EMPIRE_NEW_PATH = "locale/ui/selectempire/"

JOBDESC_WARRIOR_PATH = "%s/jobdesc_warrior.txt" % (name)
JOBDESC_ASSASSIN_PATH = "%s/jobdesc_assassin.txt" % (name)
JOBDESC_SURA_PATH = "%s/jobdesc_sura.txt" % (name)
JOBDESC_SHAMAN_PATH = "%s/jobdesc_shaman.txt" % (name)
if app.ENABLE_WOLFMAN_CHARACTER:
	JOBDESC_WOLFMAN_PATH = "%s/jobdesc_wolfman.txt" % (name)

EMPIREDESC_A = "%s/empiredesc_a.txt" % (name)
EMPIREDESC_B = "%s/empiredesc_b.txt" % (name)
EMPIREDESC_C = "%s/empiredesc_c.txt" % (name)

if app.ENABLE_MINIGAME_RUMI_EVENT:
	CARDS_DESC = "%s/mini_game_okey_desc.txt" % (name)

if app.ENABLE_FISH_EVENT:
	FISH_EVENT_DESC_FILE_NAME = "%s/fish_event_desc.txt" % (name)
	LOCALE_INTERFACE_FILE_NAME = "%s/locale_interface.txt" % (name)

TRIVIA_EVENT_DESC_FILE_NAME = "%s/trivia_event_desc.txt" % (name)

LoadLocaleFile(LOCALE_INTERFACE_FILE_NAME, locals())