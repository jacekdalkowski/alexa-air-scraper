from pymongo import MongoClient
from lxml import html
import requests
import datetime
import pprint
import json

scrape_script_version = '1.0.0'

def is_float(value):
	try:
		float(value)
		return True
	except:
		return False

def save_air_data(air_data):
	mongo_client = MongoClient('mongodb://air-db:27017')
	airpolution_db = mongo_client['airpolution']
	airpolution_col = airpolution_db['airpolution']

	airpolution_col.update_one(
		{'app': 'cracow'}, 
		{'$set': {
			'air': air_data,
		 	'timestamp': datetime.datetime.utcnow() 
		}}, 
		upsert=True)

def fetch_air_data():
	#page = requests.get('http://powietrzewkrakowie.pl/')
	page = requests.get('http://powietrze.gios.gov.pl/pjp/current/station_details/table/10121/1/0')
	dom = html.fromstring(page.content)
	#quality = dom.xpath('//h3[1]/span/text()')
	quality = dom.xpath('//tr/td[1]/text()')
	quality = [q.replace('\t', '').replace('\r', '').replace('\n', '').replace(',', '.') for q in quality]
	del quality[-3:]
	quality = [q for q in quality if is_float(q)]

	latest_pm_10_level = quality[-1]
	if latest_pm_10_level and is_float(latest_pm_10_level):
		latest_pm_10_level_float = float(latest_pm_10_level)
		return {
			'timestamp': datetime.datetime.utcnow(),
			'pm_10': latest_pm_10_level_float
		}
	return None

def save_weather_data(weather_data):
	mongo_client = MongoClient('mongodb://air-db:27017')
	airpolution_db = mongo_client['airpolution']
	airpolution_col = airpolution_db['airpolution']

	airpolution_col.update_one(
		{'app': 'cracow'}, 
		{'$set': {
			'weather': weather_data,
		 	'timestamp': datetime.datetime.utcnow() 
		}}, 
		upsert=True)

def fetch_weather_data(city_id):
	url = 'http://api.openweathermap.org/data/2.5/forecast?id=' + city_id + '&APPID=01a36ac04b1772f77c02af558e929933'
	weather_data_response = requests.get(url)
	weather_data = json.loads(weather_data_response.content)
	weather_data['timestamp'] = datetime.datetime.utcnow()
	return weather_data

def save_scrape_status(state, timestamp, scrape_script_version):
	mongo_client = MongoClient('mongodb://air-db:27017')
	airpolution_db = mongo_client['airpolution']
	airpolution_col = airpolution_db['airpolution']

	airpolution_col.update_one(
		{'app': 'cracow'}, 
		{'$set': {
			'status': {
				'state': state,
				'timestamp': timestamp,
			 	'scrapeScriptVersion': scrape_script_version
			}
		}}, 
		upsert=True)


save_scrape_status('start', datetime.datetime.utcnow(), scrape_script_version)

air_data = fetch_air_data()
print 'air_data fetched: '
pprint.pprint(air_data)
save_air_data(air_data)

weather_data = fetch_weather_data('3094802')
print 'weather_data fetched: '
pprint.pprint(weather_data)
save_weather_data(weather_data)

save_scrape_status('finished', datetime.datetime.utcnow(), scrape_script_version)

