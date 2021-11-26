from __future__ import print_function
import os
import os.path

import requests

from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow

from pydrive2.auth import GoogleAuth
from pydrive2.drive import GoogleDrive

SCOPES = ['https://www.googleapis.com/auth/drive']
BASE_PATH_FILE = str(os.path.abspath(os.getcwd()))
FILE_PATH_SECRETS = f'{BASE_PATH_FILE}/repository/client_secret.json'
FILE_PATH_CREDENTIALES = f'{BASE_PATH_FILE}/repository/credentials.json'
FILE_PATH_TOKEN = f'{BASE_PATH_FILE}/repository/token.json'

def drive_service():
    '''
        Logs in drive and return an instace of his service
    '''
    creds = None
    if os.path.exists(FILE_PATH_TOKEN):
        creds = Credentials.from_authorized_user_file(FILE_PATH_TOKEN, SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                FILE_PATH_CREDENTIALES, SCOPES)
            creds = flow.run_local_server(port=8080)
        # Save the credentials for the next run
        with open(FILE_PATH_TOKEN, 'w') as token:
            token.write(creds.to_json())

    service = build('drive', 'v3', credentials=creds)
    return service

def upload_file_drive(file_name):
    service = drive_service()
    file_metadata = {'name': file_name}
    media = MediaFileUpload(f'{BASE_PATH_FILE}/media/{file_name}', mimetype='image/jpg')
    file = service.files().create(body=file_metadata,
                                  media_body=media,
                                  fields='id').execute()
    list_files_uploaded(service)
    return file.get('id')

def list_files_uploaded(service = None):
    if service is None:
        service = drive_service()
    results = service.files().list(
        pageSize=10, fields="nextPageToken, files(id, name)").execute()
    items = results.get('files', [])

    if not items:
        print('No files found.')
    else:
        print('Files:')
        for item in items:
            print(u'{0} ({1})'.format(item['name'], item['id']))  