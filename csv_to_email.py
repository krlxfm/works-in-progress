import os
import sys
import csv
import time
from email.mime.text import MIMEText
import ssl
import smtplib

from email_credentials import EMAIL, PASSWORD, PORT, SMTP_SERVER
# PORT for local server is 25, for Gmail is 465
# SMTP server may be something like 'smtp.gmail.com'


def get_credentials_filename():
    credentials_filename = 'show_credentials.csv'
    if len(sys.argv) > 1:
        credentials_filename = sys.argv[1]
    assert(os.path.exists(credentials_filename))
    return credentials_filename

def main():
    credentials_filename = get_credentials_filename()

    context = ssl.create_default_context()

    with smtplib.SMTP_SSL(SMTP_SERVER, PORT, context=context) as server:
        server.login(EMAIL, PASSWORD)

        with open(credentials_filename, newline='') as infile:
            reader = csv.reader(infile)
            for row in reader:
                name, start_date, start_time, end_date, end_time, login, password, emails = row
                if start_date == 'startDate':
                    continue

                recipient_list = emails.split(':')

                msg = MIMEText(f'''Welcome to a new and exciting term for KRLX!\nWe are very excited to hear you live on air for {name}.\nBelow, you will find your login credentials for streaming.\n\nlogin: {login}\npassword: {password}\n\n<3 KRLX IT''')
                msg['Subject'] = f'KRLX Credentials for {name}'
                msg['From'] = EMAIL
                msg['To'] = ', '.join(recipient_list)

                server.sendmail(EMAIL, recipient_list, msg.as_string())

if __name__ == '__main__':
    main()
