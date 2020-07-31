import imaplib
import email
from email.header import decode_header
from datetime import datetime, timedelta
import requests
import json


#now = datetime.now()
now = datetime.utcnow()
print(now)
# Function to convert string to datetime
def convert(date_time):
    format = "%a, %d %b %Y %H:%M:%S %z"
    datetime_str = datetime.strptime(date_time, format)
    return datetime_str

#EMAIL_FOLDER = "07 Punchh/Campaigns"

# Login details
CREDS = open("/media/ashish/Personal1/Study/git/Mail_Automation/nclouds_creds.txt", "r")
#CREDS = open("/media/ashish/Personal1/Study/git/Mail_Automation/haad_credes.txt", "r")
LINES = CREDS.readlines()
username = LINES[0]
password = LINES[1]
CREDS.close()

# IMAP SSL
imap = imaplib.IMAP4_SSL("imap.gmail.com")
# Authenticate
imap.login(username, password)
status, messages = imap.select("Inbox")
#status, messages = imap.search(None, '(SUBJECT "Upcoming Mass Campaigns")')
#print(messages)


N = 1       # Number of latest mail to print
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
            #SYS_TIME = now.strftime("%a, %d %b %Y %H:%M:%S %z")        # Gmail Date Time Format
            DATE_NOW = datetime.utcnow()
            SYS_TIME = DATE_NOW - timedelta(seconds=120)
            CURRENT_DATE_TIME = str(SYS_TIME)[:-10]
            TRIM_MAIL_DATE = str(CONVERTED_GDATE)[:-9]
            print("Trim mail date time      :", TRIM_MAIL_DATE)
            print("Current system date time :", CURRENT_DATE_TIME)
            print("====================================================================================================")
            #CURRENT_DATE_TIME = "2020-07-29 07:51"
            #print(CURRENT_DATE_TIME)
            x = 1
# Condition to check the mails withing 2 mins
            if TRIM_MAIL_DATE >= CURRENT_DATE_TIME:
                x = 1
                print("===========HI this is the Mail to print===========")
                print(GDATE)
                print("Subject:", subject)
                print("From:", from_)
                msg['Body'] = ''
                #if msg.is_multipart():
                #if msg.is_multipart():
                if x == 1:
                    for part in msg.walk():
                        content_type = part.get_content_type()
                        content_disposition = str(part.get("Content-Disposition"))
                        try:
                            body = part.get_payload(decode=True).decode()
                            #body = mail.to_json
                        except:
                            print("Here")
                            pass
                    #if content_type == "text/plain" and "attachment" not in content_disposition:
                        if content_type == "text/plain":
                            print("Printing here 001")
                            print(body)
                            data = json.dumps({"text": str(body),
                                               "attachments": [
                                                   {
                                                       "title": "Campaign Status check?",
                                                       "fallback": "No one Acked the Campaigns",
                                                       "callback_id": "Campaigns",
                                                       "color": "#32CD32",  #3AA3E3 - Color Blue
                                                       "attachment_type": "default",
                                                       "actions": [
                                                           {
                                                               "name": "check",
                                                               "text": "Checked by",
                                                               "type": "select",
                                                               "data_source": "users",
                                                               "user": "assignee"
                                                           }
                                                        ]
                                                   }
                                               ]
                                               })

                            #data = "[{\"status\": \"existing\",\"userlogged\": \"kapilrajput22@gmail.com\",\"incident-no\": \"219\",\"note\": \"This is to validated Add notes Feature\"},{\"status\": \"existing\",\"userlogged\": \"kapilrajput22@gmail.com\",\"incident-no\": \"220\",\"note\": \"This is to validated Add notes Feature\"},{\"status\": \"existing\",\"userlogged\": \"kapilrajput22@gmail.com\",\"incident-no\": \"222\",\"note\": \"This is to validated Add notes Feature\"}]"
                            print(data)

                            headers = {
                                'Content-type': 'application/json',
                            }
                            response = requests.post('https://hooks.slack.com/services/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', headers=headers, data=data)     #json.dumps(str(body))

                            #print(type(data))
                            print(response.status_code, response.content)

                        elif  content_type == "text/html":
                            print("Printing here 0010")
                            print(body)
                            data = json.dumps({"text": str(body),
                                               "attachments": [
                                                   {
                                                       "title": "Campaign Status check?",
                                                       "fallback": "No one Acked the Campaigns",
                                                       "callback_id": "Campaigns",
                                                       "color": "#32CD32",  #3AA3E3 - Color Blue
                                                       "attachment_type": "default",
                                                       "actions": [
                                                           {
                                                               "name": "check",
                                                               "text": "Checked by",
                                                               "type": "select",
                                                               "data_source": "users",
                                                               "user": "assignee"
                                                           }
                                                        ]
                                                   }
                                               ]
                                               })

                            #data = "[{\"status\": \"existing\",\"userlogged\": \"kapilrajput22@gmail.com\",\"incident-no\": \"219\",\"note\": \"This is to validated Add notes Feature\"},{\"status\": \"existing\",\"userlogged\": \"kapilrajput22@gmail.com\",\"incident-no\": \"220\",\"note\": \"This is to validated Add notes Feature\"},{\"status\": \"existing\",\"userlogged\": \"kapilrajput22@gmail.com\",\"incident-no\": \"222\",\"note\": \"This is to validated Add notes Feature\"}]"
                            print(data)

                        elif content_type == "text/plain" and "attachment" not in content_disposition:
                            print("Printing here 002")
                            print(body)
                        #else:
                        #    content_type = msg.get_content_type()
                        #    body = msg.get_payload(decode=True).decode()
                        #    print("Printing  003")
                        #    print(body)
                        print("=" * 100)
            else:
                print("No new mails")
print("here 003")
imap.close()
imap.logout()


# REF
# https://github.com/slackapi/python-message-menu-example
# https://towardsdatascience.com/python-and-slack-a-natural-match-60b136883d4d
#
