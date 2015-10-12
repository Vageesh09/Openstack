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

app=Flask(__name__)

@app.route("/")
def index():
	#return 'welcome'
	return render_template("index.html")


@app.route("/test")
def tets():
	return 'welcome1'


@app.route("/vmstats")
def tets():
	return 'welcome1'

if __name__ == "__main__":
	port = int(os.environ.get('PORT',8008))

	if port == 8008:
		app.debug = True

	app.run(host = '0.0.0.0',port = port)