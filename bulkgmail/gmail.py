'''
Send email through gmail, with Jinja templating support.
'''

import sys
import base64
from os.path import join, exists
from email.mime.text import MIMEText

from gmail import GMail, Message
from jinja2 import Environment, FileSystemLoader

from .util import FP_TEMPLATES

#
#  Filepaths
#

FP_BODY = join(FP_TEMPLATES, 'body.txt')
FP_SUBJECT = join(FP_TEMPLATES, 'subject.txt')

if not exists(FP_BODY):
    raise(Exception(f'please make a "body.txt" file in the "{FP_TEMPLATES}"" folder'))

if not exists(FP_SUBJECT):
    raise(Exception(f'please make a "subject.txt" file in the "{FP_TEMPLATES}"" folder'))

#
#  Init
#

JENV = Environment(loader=FileSystemLoader(FP_TEMPLATES))

# NOTE: If modifying these scopes, delete the file token.json.
SCOPES = 'https://www.googleapis.com/auth/gmail.send'


def get_gmail(email, password):
    return GMail(email, password)


def send(gmail, to, context):
    # render templates
    body_tmpl = JENV.get_template('body.txt')
    body = body_tmpl.render(context)
    subject_tmpl = JENV.get_template('subject.txt')
    subject = subject_tmpl.render(context)
    # build mime email message
    msg = Message(subject, to=to, text=body)
    # Call the Gmail API
    try:
        sent_msg = gmail.send(msg)
        print(f'Message id {sent_msg["id"]} successfully sent to "{to}"')
        return sent_msg
    except Exception as error:
        print(f'Error when sending to "{to}":\n{error}\n')
