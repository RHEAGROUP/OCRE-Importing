# from imap_tools import MailBox, AND
import imaplib
import email
from create_orders_from_email import get_email_contents
import time
import sys

with imaplib.IMAP4_SSL(host="imap.gmail.com", port=imaplib.IMAP4_SSL_PORT) as imap_ssl:
    resp_code, response = imap_ssl.login(sys.argv[1], sys.argv[2])
    while True:
        resp_code, mail_count = imap_ssl.select(mailbox="INBOX", readonly=True)
        resp_code, mails = imap_ssl.search(None, "UnSeen (SUBJECT 'OCRE')")
        for mail_id in mails[0].decode().split()[-10:]:
            resp_code, mail_data = imap_ssl.fetch(mail_id, '(RFC822)') ## Fetch mail data.
            message = email.message_from_bytes(mail_data[0][1]) ## Construct Message from mail data
            for part in message.walk():
                if part.get_content_type() == "text/plain":
                    get_email_contents(email=part.get_payload(), token=sys.argv[3], secret_token=sys.argv[4])
        time.sleep(30)