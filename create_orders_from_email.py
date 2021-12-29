# -*- coding: utf-8 -*-

import requests
import sys
import json
import re
from pprint import pprint

def create_oder(user_body, order_data, token, secret_token):
    headers = { 'X-App-Id': token,
            'X-App-Token': secret_token,
            'Content-Type': 'application/json'}
    items = {'product_id': order_data['product_id'], 'quantity':1}
    satellite_data = order_data['Satellite data requested']
    for key in satellite_data:
        order_data[key] = satellite_data[key]
    del order_data['Satellite data requested']
    del order_data['product_id']
    order_data['Status'] = 'Pending'
    order_data['Feedback_submission_date'] = ''
    body =  {'customer': user_body,
             'items': [items], 'metadata': order_data}
    response = requests.post('https://api.voucherify.io/v1/orders', headers = headers, data = json.dumps(body))
    if response.status_code != 401:
        id = json.loads(response.content)['id']
        with open('order_list.txt','a') as orders:
            orders.write(id+'\n')


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

#
def get_email_contents(email='',path='', token='', secret_token=''):
    if path != '':
        dot = u'\u2022'
        with open(path) as f:
            lines = f.readlines()
    else:
        dot = '*'
        lines = email.splitlines()
    full_name = ''
    name_counter = 0
    last_entry = ''
    for i in range(len(lines) - 1):
        line = lines[i]
        if line[len(line)-1] == '=':
            line = line[:len(line)-1]
            line = line + lines[i+1]
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
        elif chunks[0][0] == dot:
            if last_entry != 'Satellite data requested' :
                element = re.sub('[^A-Za-z0-9\- \+ \ ]+', '', chunks[0])
                element = element.strip()
                product_request_data[last_entry].append(element)
            else:
                element = re.sub('[^A-Za-z0-9\- \+ \( \) \ ]+', '', chunks[0])
                element = element.strip()
                if element in mapping:
                    product_request_data[last_entry][mapping[element]] = {}
                else:
                    product_request_data[last_entry][element] = {}
        else:
            if last_entry == 'Satellite data requested':
                details = chunks[1].split(':',1)
                if chunks[0] in mapping:
                    product_request_data[last_entry][mapping[chunks[0]]]['Area of interest'] = details[0].strip()
                else:
                    product_request_data[last_entry][chunks[0]][details[0]] = details[1].strip()
    user_request_data['name'] = full_name
    user_request_data['metadata'] = user_metadata
    create_oder(user_request_data, product_request_data, token, secret_token)

if __name__ == "__main__":
    get_email_contents(path=sys.argv[1], token=sys.argv[2, secret_token=sys.argv[3]])
