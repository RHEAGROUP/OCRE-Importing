import requests
import sys
import json
import re
from pprint import pprint
# -*- coding: utf-8 -*-

email_content_path = sys.argv[1]


def create_oder(user_body, order_data):
    headers = { 'X-App-Id': 'b18fb7d4-8ec2-448b-a72d-15f6da50412d',
            'X-App-Token': 'e10cc9fc-00df-4785-8c7c-a70ead2161a7',
            'Content-Type': 'application/json'}
    items = {'product_id': order_data['product_id'], 'quantity':1}
    satellite_data = order_data['Satellite data requested']
    # pprint (satellite_data)
    for key in satellite_data:
        order_data[key] = satellite_data[key]
    del order_data['Satellite data requested']
    del order_data['product_id']
    # pprint(order_data)
    body =  {'customer': user_body,
             'items': [items], 'metadata': order_data}
    response = requests.post('https://api.voucherify.io/v1/orders', headers = headers, data = json.dumps(body))
    print(response.content)


mapping =   {'Institutional Email': 'source_id',
            'Select service(s) requested from the following list': 'product_id',
            'Other (specify)': 'Other',
            'Other (please specify)': 'Other'}
user_info = ['University Name', 'Country (where the institution is based)', 'Position',
            'First Name','Last Name', 'Age', 'Gender', 'Institutional Email', 'Nationality',
            'Knowledge of the use of digital Earth Observation services', 'Knowledge of the use of cloud services',
            'Coding skills', 'Research domain or field', 'Work scope or title', 'Work description']
product_info = ['Satellite data requested', 'Value-added products', 'Please specify the land normalised indices',
                'Please specify the Copernicus land cover map', 'Please specify the surface motion products',
                'Please specify the water quality indices', 'Please specify atmosphere element concentration']
required_product_info= ['Select service(s) requested from the following list']
user_request_data= {}
product_request_data = {}
user_metadata = {}

with open(email_content_path) as f:
    lines = f.readlines()
    full_name = ''
    name_counter = 0
    last_entry = ''
    for line in lines:
        chunks = line.split(':',1)
        for i in range(len(chunks)):
            chunks[i] = chunks[i].rstrip()
            chunks[i] = chunks[i].lstrip()
        if chunks[0] in user_info:
            if chunks[0] in mapping:
                user_request_data[mapping[chunks[0]]] = chunks[1]
            elif chunks[0] == 'First Name' or chunks[0] == 'Last Name':
                name_counter = name_counter + 1
                full_name = full_name + chunks[1]
                if name_counter == 1:
                    full_name = full_name + ' '
            else:
                user_metadata[chunks[0]] = chunks[1]
        elif chunks[0] in required_product_info:
            if chunks[0] in mapping:
                product_request_data[mapping[chunks[0]]] = chunks[1]
            else:
                product_request_data[chunks[0]] = chunks[1]
            last_entry = chunks[0]
        elif chunks[0] in product_info:
            if chunks[0] == 'Satellite data requested':
                product_request_data[chunks[0]] = {}
            else:
                product_request_data[chunks[0]] = []
            last_entry = chunks[0]
        elif chunks[0][0] == u'\u2022':
            # element = ' '.join(chunks[0].split())
            if last_entry != 'Satellite data requested' :
                element = re.sub('[^A-Za-z0-9\- \+ \ ]+', '', chunks[0])
                product_request_data[last_entry].append(element)
            else:
                element = re.sub('[^A-Za-z0-9\- \+ \( \) \ ]+', '', chunks[0])
                if element in mapping:
                    product_request_data[last_entry][mapping[element]] = {}
                else:
                    product_request_data[last_entry][element] = {}
        else:
            if last_entry == 'Satellite data requested':
                details = chunks[1].split(':',1)
                if chunks[0] in mapping:
                    product_request_data[last_entry][mapping[chunks[0]]]['Area of interest'] = details[0]
                else:
                    product_request_data[last_entry][chunks[0]][details[0]] = details[1]
user_request_data['name'] = full_name
user_request_data['metadata'] = user_metadata
# pprint(user_request_data)
# print('---------')
# pprint(product_request_data)
create_oder(user_request_data, product_request_data)
