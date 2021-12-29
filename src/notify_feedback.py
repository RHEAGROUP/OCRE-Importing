import requests
import json
import imaplib
import smtplib


class NotifyFeedback():

    def get_status(self, orderId):
        headers = { 'X-App-Id': sys.argv[3],
                'X-App-Token': sys.argv[4],
                'Content-Type': 'application/json'}
        response = requests.get('https://api.voucherify.io/v1/orders/{}'.format(self.orderId), headers = headers)
        order_metadata = json.loads(response.content)['metadata']
        try:
            order_status = order_metadata['Status']
            email = order_metadata['email']
            order_feedback_date = order_metadata['Feedback_submission_date']
            if order_status != 'Pending':
                if order_status == 'Approved':
                    self.send_email(email, 'Approved')
                else:
                    self.send_email(email, 'Rejected')
        except:
            print('Feedback date not found')  

    def send_email(self, email, decision):
        server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        gmail_user = sys.argv[1]
        gmail_password = sys.argv[2]
        server.ehlo()
        server.login(gmail_user, gmail_password)
        subject = 'OCRE Voucherify'
        if decision == 'Approved':
            body = 'Your voucherify request was approved'
        if decision == 'Rejected':
            body = 'Your voucherify request was denied'
        server.sendmail(gmail_user, email, body)
        server.close()


with open('order_list.txt', 'r') as orders:
    orders = orders.read()
    orders = orders.split('\n')
    notif = NotifyFeedback()
    for order in orders: 
        notif.get_status(order)