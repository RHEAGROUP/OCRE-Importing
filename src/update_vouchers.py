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
            if counter == 0:
                properties = row
            else:
                body = {}
                for i in range(len(properties)):
                    if properties[i] == 'Usage':
                        body[properties[i]] = int(row[i])
                    else:
                        body[properties[i]] = row[i]
                data = {'metadata': body}
                update_vouchers(data)
            counter += 1
        
def update_vouchers(body):
    response = requests.put('https://api.voucherify.io/v1/vouchers/'+body['metadata']['Code'], headers = headers, data = json.dumps(body))
    print(response.content)    

if __name__ == "__main__":
    prepare_body(csv_path)