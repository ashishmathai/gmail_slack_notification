import imaplib
import email
from email.header import decode_header
from datetime import datetime, timedelta
import requests
import json

# UTC Time
now = datetime.utcnow()

# Function to convert string to datetime
def convert(date_time):
    format = "%a, %d %b %Y %H:%M:%S %z"
    datetime_str = datetime.strptime(date_time, format)
    return datetime_str

# Login details
CREDS = open("/path/to/file.txt", "r")
LINES = CREDS.readlines()
username = LINES[0]
password = LINES[1]
CREDS.close()

# IMAP SSL
imap = imaplib.IMAP4_SSL("imap.gmail.com")

# Authenticate
imap.login(username, password)
status, messages = imap.select("Inbox")		# Folder

# Number of latest mail to print
N = 1       
messages = int(messages[0])
for i in range(messages,  messages-N, -1):
    res, msg = imap.fetch(str(i), "(RFC822)")
    RAW_MAIL = msg[0][1].decode("utf-8")
    EMAIL_MSG = email.message_from_string(RAW_MAIL)
    print("====================================================================================================") 
    DATE_FROM_MAIL = EMAIL_MSG['Date']
    print(DATE_FROM_MAIL)
    print("====================================================================================================")
    for response in msg:
        if isinstance(response, tuple):
            msg = email.message_from_bytes(response[1])
            subject = decode_header(msg["Subject"])[0][0]
            if isinstance(subject, bytes):
                subject = subject.decode()
# Adding date time conversion and condition to print the mail
            from_ = msg.get("From")
            GDATE = msg['Date']
            print("====================================================================================================")
            print(GDATE)
            CONVERTED_GDATE = convert(msg['Date'])
            DATE_NOW = datetime.utcnow()
            SYS_TIME = DATE_NOW - timedelta(seconds=120)	# If required matches the mail time and utc now, chances are there to miss mails, due to seconds difference so, adding a 2 mins delay in utc now, so script will check for mail for 2 mins
            CURRENT_DATE_TIME = str(SYS_TIME)[:-10]
            TRIM_MAIL_DATE = str(CONVERTED_GDATE)[:-9]
            print("Trim mail date time      :", TRIM_MAIL_DATE)
            print("Current system date time :", CURRENT_DATE_TIME)
            print("====================================================================================================")

# Condition to check the mails withing 2 mins
            if TRIM_MAIL_DATE >= CURRENT_DATE_TIME:
                x = 1			# making #0001 condition True 				
                print("===========HI this is the Mail to print===========")
                print(GDATE)
                print("Subject:", subject)
                print("From:", from_)
                msg['Body'] = ''
                #if msg.is_multipart():
                if x == 1:		# #0001 condition
                    for part in msg.walk():
                        content_type = part.get_content_type()
                        content_disposition = str(part.get("Content-Disposition"))
                        try:
                            body = part.get_payload(decode=True).decode()
                        except:
                            pass
                        if content_type == "text/plain":
                            print(body)
                            data = json.dumps({"text": str(body),
                                               "attachments": [
                                                   {
                                                       "title": "<Title content>",
                                                       "fallback": "<fallback content>",
                                                       "callback_id": "<ID>",
                                                       "color": "#32CD32",  #3AA3E3 - Color Blue
                                                       "attachment_type": "default",
                                                       "actions": [
                                                           {
                                                               "name": "<name>",
                                                               "text": "<text>",
                                                               "type": "select",	# drop down
                                                               "data_source": "users",	# listing users in drop down
                                                               "user": "assignee"	# assigning for users
                                                           }
                                                        ]
                                                   }
                                               ]
                                               })
                            print(data)

                            headers = {
                                'Content-type': 'application/json',
                            }

                            response = requests.post('https://hooks.slack.com/services/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', headers=headers, data=data)     
                            print(type(data))					# get the data type
                            print(response.status_code, response.content)	# Getting response code for the code must be "200" and "OK"

                        elif  content_type == "text/html":
                            print(body)
                            data = json.dumps({"text": str(body),
                                               "attachments": [
                                                    {
                                                       "title": "<Title content>",
                                                       "fallback": "<fallback content>",
                                                       "callback_id": "<ID>",
                                                       "color": "#32CD32",  #3AA3E3 - Color Blue
                                                       "attachment_type": "default",
                                                       "actions": [
                                                           {
                                                               "name": "<name>",
                                                               "text": "<text>",
                                                               "type": "select",	# drop down
                                                               "data_source": "users",	# listing users in drop down
                                                               "user": "assignee"	# assigning for users
                                                           }
                                                        ]
                                                   }
                                               ]
                                               })
                            print(data)

                        elif content_type == "text/plain" and "attachment" not in content_disposition:
                            print(body)
                        else:
                            content_type = msg.get_content_type()
                            body = msg.get_payload(decode=True).decode()
                            print(body)
                        
            else:
                print("No new mails")
imap.close()
imap.logout()
