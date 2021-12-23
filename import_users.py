import requests
import sys
import csv
import json


headers = { 'X-App-Id': sys.argv[2],
            'X-App-Token': sys.argv[3],
            'Content-Type': 'application/json'}

csv_path = sys.argv[1]

def prepare_body(csv_file):
    with open(csv_path) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        counter = 0
        for row in csv_reader:
            product_flag = 0
            if counter == 0:
                properties = row
            else:
                user_body = {}
                order_body = {}
                for i in range(len(properties)):
                    if properties[i] == 'Product':
                        product_flag = 1
                    if product_flag:
                        if properties[i] == 'Product':
                            product = row[i]
                        else:
                            order_body[properties[i]] = row[i]
                    else:
                        if properties[i] == 'Name':
                            user_name = row[i]
                        elif properties[i] == 'Email':
                            sourceId = row[i]
                        else:
                            user_body[properties[i]] = row[i]
                order_data = {"product_id": product, "quanitity": 1}
                user_data = {'source_id': sourceId, 'name': user_name, 'metadata': user_body}
                create_oder(user_data,order_data, order_body)
            counter += 1
        
def add_user(body):
    response = requests.post('https://api.voucherify.io/v1/customers', headers = headers, data = json.dumps(body))
    return    

def create_oder(user_body, order_data, order_body):
    body =  {'customer': user_body,
             'items': [order_data], 'metadata': order_body}
    response = requests.post('https://api.voucherify.io/v1/orders', headers = headers, data = json.dumps(body))


if __name__ == "__main__":
    prepare_body(csv_path)