import app
import dbg
import constInfo
import uiScriptLocale

constInfo.BOT_DATA_LIST_GENERAL = []

filename2 = "locale/bot_general.txt"
	
handle2 = app.OpenTextFile(filename2)
count3 = app.GetTextFileLineCount(handle2)
for i in xrange(count3):
	line = app.GetTextFileLine(handle2, i)
	tokens = line.split("\t")
	TOKEN_QUESTION = 0
	TOKEN_ANSWER = 1
	LIMIT_TOKEN_COUNT = 2

	if len(tokens) < LIMIT_TOKEN_COUNT:
		dbg.TraceError("General Strange token count [%d/%d] [%s]" % (len(tokens), LIMIT_TOKEN_COUNT, line))
		continue

	question = tokens[TOKEN_QUESTION]
	answer = tokens[TOKEN_ANSWER]

	appendingData = {
		"QUESTION":question,
		"ANSWER":answer
	}

	constInfo.BOT_DATA_LIST_GENERAL.append(appendingData)
	constInfo.ANSWER[question]=answer

app.CloseTextFile(handle2)