# Voucherify importing

This repository is a tool to create orders and update vouchers to voucherify

## How to use this system

### Create Orders

To create an order on Voucherify we need a txt file with the contents of the order. An example of an order content/structure (email_content.txt) was provided in this directory.
To run the script use: 

```sh
python3 create_orders_from_email.py <path to txt file with orders details>
```

### Update Vouchers

To update existing vouchers we need a csv file containing the details of the vouchers. An example (data.csv) was provided in this directory.
To use this script run:

```sh
python3 update_vouchers.py <path to csv with the voucher details>
```
