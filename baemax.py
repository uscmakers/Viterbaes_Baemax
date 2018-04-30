import logging
from random import randint
from flask import Flask, render_template
from flask_ask import Ask, statement, question, session

import healthchecker
import helper

#pymongo imports
from pymongo import MongoClient
import json

# pprint library is used to make the output look more pretty
from pprint import pprint

import globalvars

app = Flask(__name__)
ask = Ask(app, "/")
logging.getLogger("flask_ask").setLevel(logging.DEBUG)

baymax = healthchecker.HealthChecker()

baymax.start()
bodyLocations = baymax.getBigLocations()
bodySubLocations = baymax.getSubLocations(bodyLocations)

client = MongoClient("mongodb+srv://apetranik:lOgseLjFbC9X9Bks@baemax-s3so4.mongodb.net/test")
db=client.admin
db=client.test

for post in db.myperson.find().sort('activity', -1).limit(1):
	myActivity = post['activity']
	mySleep = post['sleep']
	myHR = post['heartrate']

@ask.launch

def startup():
	return question(render_template('welcome'))

@ask.intent("SpecificIntent", convert={'subloc': str})

def specific_found(subloc):
	if subloc in globalvars.specificlocs:		
		bodySubLocation = baymax.getUserInfo(bodySubLocations, subloc)
		globalvars.subloc = bodySubLocation
		symptoms = []
		sympString = ""
		if(bodySubLocation is not None):
		    symptoms = baymax.getSymptoms(bodySubLocation)
		    for symptom in symptoms:
		    	sympString = sympString + symptom["Name"] + ", "
		    return question(render_template('symptomcheck', sympString=sympString))
	return question(render_template('feelingbad'))

@ask.intent("SymptomIntent", convert={'symptom': str})

def get_symptoms(symptom):
	globalvars.mysymptoms.append(symptom)
	print(symptom)
	return question(render_template('more'))

@ask.intent("AMAZON.YesIntent")

def ask_symptom():
	return question(render_template('symptomPrompt'))

@ask.intent("AMAZON.NoIntent")

def diagnose_patient():
	for s in globalvars.mysymptoms:
		print(s)
	diagnosis = baymax.getDiagnosis(globalvars.mysymptoms, globalvars.subloc)
	# baymax.printDiagnosis(diagnosis)
	diag = baymax.mostLikelyDiagnosis(diagnosis)
	percent = baymax.percentDiagnosis(diagnosis)
	return question(render_template('diagnoseMe', percent=percent, diag=diag))
	# return statement(render_template('poo'))

@ask.intent("SickIntent")

def choose_location():
	return question(render_template('feelingbad'))

@ask.intent("SleepIntent")

def sleep_data():
	# time = randint(5, 9)
	time = mySleep
	return question(render_template('sleep', time=time))

@ask.intent("ActiveIntent")

def active_data():
	# steps = randint(1000, 30000)
	steps = myActivity
	if steps < 10000:
		msg = render_template('badmsg', steps=steps)
	else:
		msg = render_template('goodmsg', steps=steps)
	return question(msg)

@ask.intent("HRIntent")

def hr_data():
	# hr = randint(50, 80)
	hr = myHR
	return question(render_template('hr', hr=hr))

if __name__ == '__main__':
	app.run(debug=True)