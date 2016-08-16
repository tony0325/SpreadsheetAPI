#!/usr/bin/env python
# -*- coding: UTF-8 -*-

from __future__ import print_function
import httplib2
import os
import random
import datetime
import time

from apiclient import discovery
import oauth2client
from oauth2client import client
from oauth2client import tools

try:
    import argparse
    flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
except ImportError:
    flags = None

# If modifying these scopes, delete your previously saved credentials
# at ~/.credentials/sheets.googleapis.com-python-quickstart.json
SCOPES = 'https://www.googleapis.com/auth/spreadsheets'
CLIENT_SECRET_FILE = 'client_secret.json'
APPLICATION_NAME = 'Google Sheets API Python Quickstart'


def get_credentials():
    """Gets valid user credentials from storage.

    If nothing has been stored, or if the stored credentials are invalid,
    the OAuth2 flow is completed to obtain the new credentials.

    Returns:
        Credentials, the obtained credential.
    """
    home_dir = os.path.expanduser('~')
    credential_dir = os.path.join(home_dir, '.credentials')
    if not os.path.exists(credential_dir):
        os.makedirs(credential_dir)
    credential_path = os.path.join(credential_dir,
                                   'sheets.googleapis.com-python-quickstart.json')

    store = oauth2client.file.Storage(credential_path)
    credentials = store.get()
    if not credentials or credentials.invalid:
        flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
        flow.user_agent = APPLICATION_NAME
        if flags:
            credentials = tools.run_flow(flow, store, flags)
        else: # Needed only for compatibility with Python 2.6
            credentials = tools.run(flow, store)
        print('Storing credentials to ' + credential_path)
    return credentials


def main():
    """Shows basic usage of the Sheets API.

    Creates a Sheets API service object and prints the names and majors of
    students in a sample spreadsheet:
    https://docs.google.com/spreadsheets/d/1BxiMVs0XRA5nFMdKvBdBZjgmUUqptlbs74OgvE2upms/edit
    """
    credentials = get_credentials()
    http = credentials.authorize(httplib2.Http())
    discoveryUrl = ('https://sheets.googleapis.com/$discovery/rest?'
                    'version=v4')
    service = discovery.build('sheets', 'v4', http=http,
                              discoveryServiceUrl=discoveryUrl)

    spreadsheetId = '1b1PhUtSRn5snNOJwITrghV3i8SzyDR1g-ByI8othweY'
    rangeName = 'Class Data!A:E'
    values = service.spreadsheets().values()
    #r = values.append(spreadsheetId=spreadsheetId, range=rangeName, body=dict(range=rangeName, values=[[datetime.datetime.now().isoformat()] + [random.random() for _ in xrange(4)]]),
    #    valueInputOption='RAW', insertDataOption='INSERT_ROWS').execute()
    #print(r)
    while True:
        r = values.append(spreadsheetId=spreadsheetId, range=rangeName, body=dict(range=rangeName, values=[[datetime.datetime.now().isoformat()] + [1] + [2] + [3] + [4]]),
            valueInputOption='RAW', insertDataOption='INSERT_ROWS').execute()
        print('rangeName=' + rangeName)
        print(r)
        print('Update successfully')
        time.sleep(3600)

if __name__ == '__main__':
    main()
