import app
import dbg
import constInfo
import uiScriptLocale

constInfo.BOT_DATA_LIST_INFO = []
filename = "locale/bot_info.txt"

handle = app.OpenTextFile(filename)
count = app.GetTextFileLineCount(handle)
for i in xrange(count):
	line = app.GetTextFileLine(handle, i)
	tokens = line.split("\t")
	TOKEN_QUESTION = 0
	TOKEN_ANSWER = 1
	LIMIT_TOKEN_COUNT = 2

	if len(tokens) < LIMIT_TOKEN_COUNT:
		dbg.TraceError("Info Strange token count [%d/%d] [%s]" % (len(tokens), LIMIT_TOKEN_COUNT, line))
		continue

	question = tokens[TOKEN_QUESTION]
	answer = tokens[TOKEN_ANSWER]

	appendingData = {
		"QUESTION":question,
		"ANSWER":answer
	}

	constInfo.BOT_DATA_LIST_INFO.append(appendingData)
	constInfo.ANSWER[question]=answer

app.CloseTextFile(handle)

