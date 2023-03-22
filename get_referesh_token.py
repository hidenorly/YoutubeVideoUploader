#!/usr/bin/env python3

#   Copyright 2023 hidenorly
#
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.

from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
import os
import google.auth
from google.auth.transport.requests import Request
import json

with open('client_secret_downloaded.json', 'r') as f:
    json_data = json.load(f)

client_config = {
    "installed": {
        "client_id": json_data["installed"]["client_id"],
        "client_secret": json_data["installed"]["client_secret"],
        "redirect_uris": ["urn:ietf:wg:oauth:2.0:oob"],
        "auth_uri": "https://accounts.google.com/o/oauth2/auth",
        "token_uri": "https://accounts.google.com/o/oauth2/token"
    }
}
SCOPES = ["https://www.googleapis.com/auth/youtube.upload", "https://www.googleapis.com/auth/youtube.readonly"]

# Get authorized token
flow = InstalledAppFlow.from_client_config(client_config, scopes=SCOPES)
credentials = flow.run_local_server(port=0)

# get referesh token and print out. You need to fill it in your client_secrect.json
refresh_token = credentials.refresh_token
print('Refresh token:', refresh_token)

#{ # remove "installed":{}
#    "client_id":"xxxxx0oe.apps.googleusercontent.com",
#    "project_id":"xxxx",
#    "auth_uri":"https://accounts.google.com/o/oauth2/auth",
#    "token_uri":"https://oauth2.googleapis.com/token",
#    "auth_provider_x509_cert_url":"https://www.googleapis.com/oauth2/v1/certs",
#    "client_secret":"xxxx",
#    "refresh_token":"xxxx"  # you need to fill the print out here
#}
