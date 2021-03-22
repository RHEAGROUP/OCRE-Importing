import requests
import sys
import csv
import json

# TODO TEST THIS WITH REAL FORM DATA
# PUT THIS ON JUPYTER
# ADD FEEDBACK FOR ACCEPTING/REJECTING ORDER

headers = { 'X-App-Id': '19b239b9-49f7-4d64-80a5-cca573f8de24',
            'X-App-Token': 'f59c0e69-b45b-41d3-9a12-90d6fb05038d',
            'Content-Type': 'application/json'}

csv_path = sys.argv[1]

def prepare_body(csv_file):
    with open(csv_path) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        counter = 0
        for row in csv_reader:
            if counter == 0:
                properties = row
            else:
                user_body = {}
                order_body = {}
                for i in range(len(properties)):
                    if i > 5:
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
    print(body)
    response = requests.post('https://api.voucherify.io/v1/orders', headers = headers, data = json.dumps(body))


if __name__ == "__main__":
    prepare_body(csv_path)