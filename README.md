# Voucherify importing

This repository is a tool to create orders and update vouchers to voucherify

## How to use this system

### Create Orders

To create an order on Voucherify we need a txt file with the contents of the order. An example of an order content/structure (email_content.txt) was provided in this directory.
To run the script use: 

```sh
python3 create_orders_from_email.py <path to txt file with orders details> <voucherify_api_token> <voucherify_api_secret>
```

There is another way to create the orders. This method requires an email account to be setup and for the email containing the order details to be sent to that account. An infinite loop reads the inbox of the emails and if it find an email regarding 'OCRE', it processes it. To run this workflow run:

```sh
python3 watcher.py <email> <email_password> <voucherify_token> <voucherify_secret>
```

### Update Vouchers

To update existing vouchers we need a csv file containing the details of the vouchers. An example (data.csv) was provided in this directory.
To use this script run:

```sh
python3 update_vouchers.py <csv_path> <voucherify_token> <voucherify_secret> 
```

### Notify Order Feedback

An order needs to be accepted or rejected manually from Voucherify. When that's done, run:

```sh
python3 notify_feedback.py <email> <email_password> <voucherify_token> <voucherify_secret> 
```