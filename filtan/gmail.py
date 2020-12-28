import pickle
import os
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request


class Gmail:
    def __init__(self, token_paths):
        self.user_id = 'me'
        self.scopes = ['https://mail.google.com/',
                       'https://www.googleapis.com/auth/gmail.labels',
                       'https://www.googleapis.com/auth/gmail.modify',
                       'https://www.googleapis.com/auth/gmail.settings.basic']
        self.pickle_path = token_paths['pickle_path']
        self.json_path = token_paths['json_path']
        self.service = build('gmail', 'v1', credentials=self.credential())

    def credential(self):
        creds = None
        if os.path.exists(self.pickle_path):
            with open(self.pickle_path, 'rb') as token:
                creds = pickle.load(token)

        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    self.json_path, self.scopes
                )
                creds = flow.run_local_server(port=0)
            with open(self.pickle_path, 'wb') as token:
                pickle.dump(creds, token)
        return creds

    def label_list(self):
        try:
            result = self.service.users().labels().list(userId=self.user_id).execute()
        except Exception as e:
            return str(e)
        labels = [label for label in result.get('labels', [])]
        return labels

    def filter_list(self):
        try:
            result = self.service.users().settings().filters().list(userId=self.user_id).execute()
        except Exception as e:
            return str(e)
        filters = [flt for flt in result.get('filter', [])]
        return filters

    def create_label(self, name):
        label_object = {
            'messageListVisibility': 'show',
            'name': name,
            'labelListVisibility': 'labelShow'
        }
        try:
            label = self.service.users().labels().create(userId=self.user_id, body=label_object).execute()
            return label
        except Exception as e:
            return str(e)

    def create_filter(self, filter_type, filter_txt, label_id):
        mail_filter = {
            'criteria': {
                filter_type: filter_txt
            },
            'action': {
                'addLabelIds': [label_id],
                'removeLabelIds': ['INBOX']
            }
        }
        try:
            result = self.service.users().settings().filters().create(userId=self.user_id, body=mail_filter).execute()
        except Exception as e:
            return str(e)
        return result
