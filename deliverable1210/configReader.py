import ConfigParser

def readConfigFile(filename,sect):
	dict1 = {}
	config=ConfigParser.ConfigParser()
	config.read(filename)
	options = config.options(sect)
	for option in options:
		try: 
			dict1[option]=config.get(sect,option)
		except:
			print "Config Parser : read error... Check configReader.py file or key.conf File"
	return dict1

