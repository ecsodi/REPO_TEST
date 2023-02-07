# SERVER_SETTINGS = {
	# "SERVER_NAME" : "Deimos.to",
	# "IP" : "188.212.101.143",
	# "CH1" :	30003,
	# "CH2" : 30007,	
	# "CH3" : 30010,	
	# "CH4" : 30013,	
	# "CH5" : 30015,	
	# "CH6" : 30017,	
	# "AUTH" : 30001,	
	# "MARK" : 13001,		
# }
# MARKADDR	= 13001
SERVER_SETTINGS = {
	"SERVER_NAME" : "Emerald",
	# "IP" : "146.59.68.207",
	"IP" : "188.212.103.134",
	"CH1" :	13001,
	"CH2" : 13101,
	"CH3" : 13201,
	"CH4" : 13301,
	"CH5" : 30015,	
	"CH6" : 30017,	
	"AUTH" : 11003,	
	"MARK" : 13099,		
}
MARKADDR	= 13001


TRANSLATE = {
	"Trebuie sa introduceti un nume si o parola" : "Trebuie sa introduceti un nume si o parola",
	"Fara succes" : "Fara succes",
}

CHANNELS_DICT_IMAGES = {
	0 : "d:/ymir work/ui/game/new_login/channel_off.png",
	1 : "d:/ymir work/ui/game/new_login/channel_on.png",
	2 : "d:/ymir work/ui/game/new_login/channel_busy.png",
	3 : "d:/ymir work/ui/game/new_login/channel_off.png",
}

CHANNELS_DICT = {
	1:{"key":11,"port":SERVER_SETTINGS["CH1"],"state":CHANNELS_DICT_IMAGES[0],},
	2:{"key":12,"port":SERVER_SETTINGS["CH2"],"state":CHANNELS_DICT_IMAGES[0],},
	3:{"key":13,"port":SERVER_SETTINGS["CH3"],"state":CHANNELS_DICT_IMAGES[0],},
	4:{"key":14,"port":SERVER_SETTINGS["CH4"],"state":CHANNELS_DICT_IMAGES[0],},
	5:{"key":15,"port":SERVER_SETTINGS["CH5"],"state":CHANNELS_DICT_IMAGES[0],},
	6:{"key":16,"port":SERVER_SETTINGS["CH6"],"state":CHANNELS_DICT_IMAGES[0],},
}


# MARKADDR_DICT = {
		# 10 : { "ip" :SERVER_SETTINGS["IP"], "tcp_port" : MARKADDR, "mark" : "10.tga", "symbol_path" : "10", }, #
		# 20 : { "ip" :SERVER_SETTINGS["IP"], "tcp_port" : MARKADDR, "mark" : "20.tga", "symbol_path" : "20", }, #
		# 30 : { "ip" :SERVER_SETTINGS["IP"], "tcp_port" : MARKADDR, "mark" : "30.tga", "symbol_path" : "30", }, #
		# 40 : { "ip" :SERVER_SETTINGS["IP"], "tcp_port" : MARKADDR, "mark" : "40.tga", "symbol_path" : "40", }, #
# }

MARKADDR_DICT = {
		10 : { "ip" :SERVER_SETTINGS["IP"], "tcp_port" : 29001, "mark" : "10.tga", "symbol_path" : "10", }, #
		20 : { "ip" :SERVER_SETTINGS["IP"], "tcp_port" : 29101, "mark" : "20.tga", "symbol_path" : "20", }, #
		30 : { "ip" :SERVER_SETTINGS["IP"], "tcp_port" : 29201, "mark" : "30.tga", "symbol_path" : "30", }, #
		40 : { "ip" :SERVER_SETTINGS["IP"], "tcp_port" : 29301, "mark" : "40.tga", "symbol_path" : "40", }, #
}

TESTADDR = { 'ip' : 'SERVER_SETTINGS["IP"]', 'tcp_port' : 50000, 'udp_port' : 50000, }