# fidap client
import base64
from typing import List, Any, TypeVar, Dict

import pandas as pd
import requests
from python_http_client import exceptions

from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail, Attachment, FileType, FileName, FileContent, Disposition

endpoint = 'http://fidap.ngrok.io/api'
_T = TypeVar('_T', bound=Dict[str, Any])
SENDGRID_API_KEY = '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'


def sql(sql):
    return api({'func': 'sql', 'sql': sql})


def api(json: _T):
    response = requests.post(endpoint, json=json)
    df = pd.read_json(response.json()['result'])
    return df


def send_email(json: _T, emails: List[str]) -> None:
    send_grid_client = SendGridAPIClient(SENDGRID_API_KEY)
    from_email = 'ashish.singal@gmail.com'
    content = '<strong>Text Email from Fidap<strong>'
    subject = 'Fidap.co Sending with Twilio SendGrid is Fun'
    df = pd.read_json(json)
    data = df.to_csv()
    data = data.encode('ascii')
    attachment = Attachment(
        FileContent(base64.b64encode(data).decode()),
        FileName('text.csv'),
        FileType('text/csv'),
        Disposition('attachment')
    )

    for email in emails:
        mail = Mail(from_email=from_email, to_emails=email, subject=subject, html_content=content)
        mail.attachment = attachment
        try:
            send_grid_client.send(mail)
        except exceptions.BadRequestsError as e:
            print(e.body)
