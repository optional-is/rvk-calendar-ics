# coding: utf-8

import logging
import flask
import json
import flask_config
import urllib2
import datetime
from flask import request

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
	url="http://newevents.reykjavik.is/find?f=%s&lang=en"%(datetime.datetime.today().strftime("%Y-%m-%d"))

	req = urllib2.Request(url)
	response = urllib2.urlopen(req)
	ics = json.loads(response.read())
	
	ics_str = "BEGIN:VCALENDAR\r\n"
	ics_str += "VERSION:2.0\r\n"
	ics_str += "PRODID:-//optional/rvkcal//NONSGML v1.0//EN\r\n"
	

	tags = []
	if 'tags' in request.args:
		tags = request.args['tags'].split(',')
	
	for i in ics:
		ics_str += build_ics_entry(i,tags)
	
	ics_str += "END:VCALENDAR\r\n"

	
	# Return this with the right mimetype
	return flask.Response(response=ics_str,
	                    status=200,
	                    mimetype="text/x-calendar",
						headers={"Content-Disposition":"attachment;filename=rvk-calendar.ics"}
						)

def normalize_datetime(dt):
	new_dt = dt.replace(":","").replace("-","")
	return new_dt+'00Z'

def build_ics_entry(data,tags=[]):
	summary = data['language']['en']['title']
	description = data['language']['en']['text']
	show = False
	ics_str = ''
	

	for i in data['language']['en']['tags']:
		if i in tags:
			show = True
		
	if show or len(tags) == 0:
		ics_str += "BEGIN:VEVENT\r\n"
		ics_str += "UID:%s\r\n"%data['event_id']
		ics_str += "DTSTAMP:%s\r\n"%normalize_datetime(data['start'])
		ics_str += "DTSTART:%s\r\n"%normalize_datetime(data['start'])
		ics_str += "DTEND:%s\r\n"%normalize_datetime(data['end'])
		ics_str += "SUMMARY:%s\r\n"%summary
		ics_str += "END:VEVENT\r\n"


	return ics_str

if __name__ == '__main__':
	# Set up logging to stdout, which ends up in Heroku logs
	stream_handler = logging.StreamHandler()
	stream_handler.setLevel(logging.WARNING)
	app.logger.addHandler(stream_handler)

	app.debug = True
	app.run(host='0.0.0.0', port=flask_config.port)
