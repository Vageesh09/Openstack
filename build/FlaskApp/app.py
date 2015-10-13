# from flask import Flask
# app=Flask(__name__)

# @app.route("/")
# def main():
# 	return 'welcome'

# if __name__ == "__main__":
# 	app.run()

from flask import Flask
from flask import render_template
import os
import json

app=Flask(__name__)

@app.route("/")
def index():
	#return 'welcome'
	return render_template("index.html")


@app.route("/test")
def tets():
	data = {
		"hello":"world",
		"number":3
	}
	return str(data)

@app.route("/status")
def status():




	

if __name__ == "__main__":
	port = int(os.environ.get('PORT',8008))

	if port == 8008:
		app.debug = True

	app.run(host = '0.0.0.0',port = port)