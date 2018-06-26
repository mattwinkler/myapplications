

import requests

"""
Example of using the requests library to query APIs.  
Good for situations where there isn't already an 
API built out for your specific use case.

Taken from Data Visualization with Python and JavaScript by Kyran Dale.  
Copy available here: http://shop.oreilly.com/product/0636920037057.do
"""


OECD_ROOT_URL = 'http://stats.oecd.org/sdmx-json/data'
REQUEST_DIMS = (('USA', 'AUS'), ('GDP', 'B1_GE'), 
	            ('CUR', 'VOBARSA'), ('Q'))

REQUEST_PARAMS = {'startTime': '2009-Q1', 'endTime': '2010-Q1'}


def make_oecd_request(dsname, dimensions, params=None, root_dir=OECD_ROOT_URL):
	"""Make URL for the OECD API and fetch data"""
	if not params:
		params = {}

	dim_args = ['+'.join(d) for d in dimensions]

	dim_str = '.'.join(dim_args)

	url = root_dir + '/' + dsname + '/' + dim_str + '/all'

	print('Requesting URL: ' + url)
	return requests.get(url, params=params)


def show_response_keys(response):
	if response.status_code == 200:
		json = response.json()
		print(json.keys())


def main():
	response = make_oecd_request('QNA', REQUEST_DIMS, REQUEST_PARAMS)
	show_response_keys(response)


if __name__ == '__main__':
	main()


