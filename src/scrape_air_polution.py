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

def save_air_data(air_data, city):
	mongo_client = MongoClient('mongodb://air-db:27017')
	airpolution_db = mongo_client['airpolution']
	airpolution_col = airpolution_db['airpolution']

	airpolution_col.update_one(
		{'app': city}, 
		{'$set': {
			'air': air_data,
		 	'timestamp': datetime.datetime.utcnow() 
		}}, 
		upsert=True)

def fetch_air_data_for_cracow():
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

def fetch_air_data_from_aqicn(url, city_id):
	page = requests.get(url, headers={
		'Cache-Control': 'no-cache',
		'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'
	})
	dom = html.fromstring(page.content)
	quality = dom.xpath('//div[@id="aqiwgtvalue"]/text()')[0]
	print "Quality " + city_id + ": " + quality
	updateTime = dom.xpath('//span[@id="aqiwgtutime"]/text()')[0]
	print "Quality " + city_id + " update time: " + updateTime
	if quality and is_float(quality):
		quality_float = float(quality)
		return {
			'timestamp': datetime.datetime.utcnow(),
			'pm_10': quality_float
		}
	return None

def fetch_air_data_for_nyc():
	return fetch_air_data_from_aqicn('http://aqicn.org/city/usa/newyork?a=213', 'NYC')

def fetch_air_data_for_la():
	return fetch_air_data_from_aqicn('http://aqicn.org/city/losangeles/los-angeles-north-main-street/', 'LA')

def fetch_air_data_for_vancouver():
	return fetch_air_data_from_aqicn('http://aqicn.org/city/vancouver', 'Vancouver')

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

def save_scrape_status(app, state, timestamp, scrape_script_version):
	mongo_client = MongoClient('mongodb://air-db:27017')
	airpolution_db = mongo_client['airpolution']
	airpolution_col = airpolution_db['airpolution']

	airpolution_col.update_one(
		{'app': app}, 
		{'$set': {
			'status': {
				'state': state,
				'timestamp': timestamp,
			 	'scrapeScriptVersion': scrape_script_version
			}
		}}, 
		upsert=True)


save_scrape_status('nyc', 'start', datetime.datetime.utcnow(), scrape_script_version)

air_data = fetch_air_data_for_nyc()
print 'air_data fetched for nyc: '
pprint.pprint(air_data)
save_air_data(air_data, 'nyc')

save_scrape_status('nyc', 'finished', datetime.datetime.utcnow(), scrape_script_version)





save_scrape_status('la', 'start', datetime.datetime.utcnow(), scrape_script_version)

air_data = fetch_air_data_for_la()
print 'air_data fetched for la: '
pprint.pprint(air_data)
save_air_data(air_data, 'la')

save_scrape_status('la', 'finished', datetime.datetime.utcnow(), scrape_script_version)





save_scrape_status('Vancouver', 'start', datetime.datetime.utcnow(), scrape_script_version)

air_data = fetch_air_data_for_vancouver()
print 'air_data fetched for Vancouver: '
pprint.pprint(air_data)
save_air_data(air_data, 'Vancouver')

save_scrape_status('Vancouver', 'finished', datetime.datetime.utcnow(), scrape_script_version)




save_scrape_status('cracow', 'start', datetime.datetime.utcnow(), scrape_script_version)

air_data = fetch_air_data_for_cracow()
print 'air_data fetched for cracow: '
pprint.pprint(air_data)
save_air_data(air_data, 'cracow')

weather_data = fetch_weather_data('3094802')
print 'weather_data fetched: '
pprint.pprint(weather_data)
save_weather_data(weather_data)

save_scrape_status('cracow', 'finished', datetime.datetime.utcnow(), scrape_script_version)









