import os

FILE_NAME = "shop/price_list.txt"
PRICE_DICT = {}


def read_prices():
	if not os.path.exists(os.path.dirname(FILE_NAME)):
		os.makedirs(os.path.dirname(FILE_NAME))

	try:
		f = old_open(FILE_NAME, "r")
	except IOError:
		f = old_open(FILE_NAME, "w+")

	lines = [line.rstrip('\n') for line in f]

	f.close()

	for line in lines:
		PRICE_DICT[int(line.split("\t")[0])] = int(line.split("\t")[1])


def write_price_list():
	f = old_open(FILE_NAME, "w")

	for index, price in PRICE_DICT.iteritems():
		f.write("%d\t%d\n" % (index, price))

	f.close()
