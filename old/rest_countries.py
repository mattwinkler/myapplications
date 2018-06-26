

import requests
from pymongo import MongoClient

""" Taken from example in Data Visualization with Python and Javascript by Kyran Dale
Available here: http://shop.oreilly.com/product/0636920037057.do

Requests to the REST countries API look like:
https://restcountries.eu/rest/v1/<field>/<name>?<params>

"""

REST_EU_ROOT_URL = 'https://restcountries.eu/rest/v1'
MONGO_DB_NAME = 'nobel_prize'
MONGO_COLL_NAME = 'country_data'


def REST_country_request(field='all', name=None, params=None):
	"""Build request from inputs and query REST countries API"""
	headers = {'User-Agent': 'Mozilla/5.0'}

	if not params:
		params = {}

	if field == 'all':
		return requests.get(REST_EU_ROOT_URL + '/all')

	url = '%s/%s/%s'%(REST_EU_ROOT_URL, field, name)
	print('Requesting URL: ' + url)

	response = requests.get(url, params=params, headers=headers)
    
    # check the response status before returning it:
	if not response.status_code == 200:
		raise Exception('Request failed with status code ' \
			+ str(response.status_code))

	return response


def get_mongo_database(db_name, host='localhost', port=27017, username=None, password=None):
	""" Get the database from MongoDB with/out authentication"""
	# Make connection:
	if username and password:
		mongo_uri = 'mongodb://%s:%s@%s/%s'%\
		(username, password, host, db_name)
		conn = MongoClient(mongo_uri)

	else:
		conn = MongoClient(host, port)

	return conn[db_name]



def main():
    # (demo) getting all the countries that use USD and uploading to MongoDB:
	
	# Mongo DB connection:
	db_conn = get_mongo_database(MONGO_DB_NAME)
	col = db_conn[MONGO_COLL_NAME]

	# Get the data:
	response = REST_country_request('currency', 'usd')

	# make sure mongodb is running (e.g. `mongod`) before executing the below
	#col.insert(response.json())

	res = col.find({'currencies': {'$in': ['USD']}})
	print(list(res))


if __name__ == '__main__':
	main()



