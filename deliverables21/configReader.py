import ConfigParser

def readConfigFile(sect):
	dict1 = {}
	config=ConfigParser.ConfigParser()
	config.read("key.conf")
	options = config.options(sect)
	for option in options:
		try: 
			dict1[option]=config.get(sect,option)
		except:
			print "read error"
	return dict1

