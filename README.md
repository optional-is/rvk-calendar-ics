# RVK Calendar ICS

This is a showcase project intended to demonstrate some of the things you can do with the calender API.

This has two parts, a scraper and converter. The scraper fetchs the data from the Calendar API and the converter converts it from JSON into an ICS file which can be using in outlook or other calendaring apps.

You can also automatically deploy to Heroku by clicking the button
[![Deploy](https://www.herokucdn.com/deploy/button.png)](https://heroku.com/deploy)

If you want to run this locally, you will need to setup a virtual enviornment

virtualenv --distribute venv

Then install all the dependancies

pip install -r requirements.txt

Then after everything is installed, you can start the server with:

python run.py
