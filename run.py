# coding: utf-8

import logging
import flask
import json
import flask_config

app = flask.Flask(__name__)
app.static_folder = "public"
app.SEND_FILE_MAX_AGE_DEFAULT = 0
	
@app.route('/')
def home():
	"""Returns html that is useful for understanding, debugging and extending
	the charting API"""

	return file('public/home.html').read()

@app.route('/ics', methods=['GET'])
def ics():
	"""Returns ics file based on the week and any language and category filters"""
	
	# Fetch the JSON
	
	# Return this with the right mimetype
	return file('public/rvk-calendar.ics').read()

if __name__ == '__main__':
	# Set up logging to stdout, which ends up in Heroku logs
	stream_handler = logging.StreamHandler()
	stream_handler.setLevel(logging.WARNING)
	app.logger.addHandler(stream_handler)

	app.debug = True
	app.run(host='0.0.0.0', port=flask_config.port)
