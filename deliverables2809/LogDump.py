import logging
import datetime
import configReader

def dumpLog(logString):
	logDict = configReader.readConfigFile("key.conf","logdetails")
	LOG_FILENAME = logDict['createvmlog']
	logging.basicConfig(filename=LOG_FILENAME,level=logging.DEBUG)
	print datetime.datetime.now()
	logging.debug( str(datetime.datetime.now()) + " " + logString)
	return 0;

def dumpLogd(logString):
	logDict = configReader.readConfigFile("key.conf","logdetails")
	LOG_FILENAME = logDict['deamonlog']
	logging.basicConfig(filename=LOG_FILENAME,level=logging.DEBUG)
	logging.debug( str(datetime.datetime.now()) + " " + logString)
	return 0;
