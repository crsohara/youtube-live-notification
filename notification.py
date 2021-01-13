#!/usr/bin/python3

# See instructions for running these code samples locally:
# https://developers.google.com/explorer-help/guides/code_samples#python
# https://stackoverflow.com/questions/58073119/youtube-data-api-v-3-fully-automated-oauth-flow-python

import os
import pickle
import json
import time
from twilio.rest import Client
from dotenv import load_dotenv
import google_auth_oauthlib.flow
import googleapiclient.discovery
import googleapiclient.errors

SCOPES = ["https://www.googleapis.com/auth/youtube.force-ssl"]
API_SERVICE_NAME = "youtube"
API_VERSION = "v3"

DIR = os.path.dirname(os.path.abspath(__file__))
dotenv_path = os.path.join(DIR, '.env')
print(dotenv_path)
load_dotenv(dotenv_path)

CLIENT_SECRETS_FILE = os.getenv('CLIENT_SECRETS_FILE')
CHANNEL_ID = os.getenv('CHANNEL_ID')

TWILIO_ACCOUNT_SID = os.getenv('TWILIO_ACCOUNT_SID')
TWILIO_AUTH_TOKEN = os.getenv('TWILIO_AUTH_TOKEN')

TWILIO_FROM = os.getenv('TWILIO_FROM')
TWILIO_TO = os.getenv('TWILIO_TO')

def message() :
    client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
    message = client.messages.create(
        from_ = TWILIO_FROM,
        body = 'FRANCIS IS LIVE',
        to = TWILIO_TO
    )
    # print(message.sid)

def main():
    # Disable OAuthlib's HTTPS verification when running locally.
    # *DO NOT* leave this option enabled in production.
    os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"
    youtube = get_authenticated_service()
    request = youtube.search().list(
        channelId=CHANNEL_ID,
        eventType="live",
        type="video",
        part="snippet"
    )

    response = request.execute()

    isLive = response['pageInfo']['totalResults']
    if isLive:
        message()

def get_authenticated_service():
    if os.path.exists("CREDENTIALS_PICKLE_FILE"):
        with open("CREDENTIALS_PICKLE_FILE", 'rb') as f:
            credentials = pickle.load(f)
    else:
        flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(
            CLIENT_SECRETS_FILE,
            SCOPES
        )
        credentials = flow.run_console()
        with open("CREDENTIALS_PICKLE_FILE", 'wb') as f:
            pickle.dump(credentials, f)

    return googleapiclient.discovery.build(
        API_SERVICE_NAME, API_VERSION,
        credentials=credentials
    )

# if __name__ == "__main__":
#     main()

try:
  while True:
    main()
    time.sleep(600) # Sleep for 10 minutes
except KeyboardInterrupt:
  print('Exiting')