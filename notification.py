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
import google.auth.transport.requests
import google_auth_oauthlib.flow
import googleapiclient.discovery
import googleapiclient.errors

import logging
from logging.handlers import RotatingFileHandler

SCOPES = ["https://www.googleapis.com/auth/youtube.force-ssl"]
API_SERVICE_NAME = "youtube"
API_VERSION = "v3"

DIR = os.path.dirname(os.path.abspath(__file__))
dotenv_path = os.path.join(DIR, '.env')
load_dotenv(dotenv_path)

CLIENT_SECRETS_FILE = os.getenv('CLIENT_SECRETS_FILE')
CHANNEL_ID = os.getenv('CHANNEL_ID')

TWILIO_ACCOUNT_SID = os.getenv('TWILIO_ACCOUNT_SID')
TWILIO_AUTH_TOKEN = os.getenv('TWILIO_AUTH_TOKEN')

TWILIO_FROM = os.getenv('TWILIO_FROM')
TWILIO_TO = os.getenv('TWILIO_TO')

prevStreamId = ''

def setupLogger() :
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)

    handler = RotatingFileHandler(os.path.join(DIR, 'notification.log'), maxBytes=2000, backupCount=2)

    # Create formatters and add it to handlers
    f_format = logging.Formatter('%(asctime)s_%(levelname)s_%(message)s')
    handler.setFormatter(f_format)

    # Add handlers to the logger
    logger.addHandler(handler)
    return logger

def message(message) :
    client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
    message = client.messages.create(
        from_ = TWILIO_FROM,
        body = message,
        to = TWILIO_TO
    )

def main():
    # Disable OAuthlib's HTTPS verification when running locally.
    # *DO NOT* leave this option enabled in production.
    os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"
    youtube = get_authenticated_service()
    # yt 'search' costs 100 units, max 10,000/day
    request = youtube.search().list(
        channelId=CHANNEL_ID,
        eventType="live",
        type="video",
        part="snippet"
    )

    response = request.execute()

    isLive = response['pageInfo']['totalResults']
    items = response['items']

    if isLive and len(items):
        logger.info(isLive)
        streamId = items[0]['id']['videoId']
        if streamId != prevStreamId:
            logger.info(isLive)
            prevStreamId = streamId
            message('FRANCIS IS LIVE')

def get_authenticated_service():
    if os.path.exists(os.path.join(DIR,"CREDENTIALS_PICKLE_FILE")):
        with open(os.path.join(DIR,"CREDENTIALS_PICKLE_FILE"), 'rb') as f:
            credentials = pickle.load(f)
            # Refresh token so we don't have to check if it's expired
            request = google.auth.transport.requests.Request()
            credentials.refresh(request)
    else:
        flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(
            os.path.join(DIR, CLIENT_SECRETS_FILE),
            SCOPES
        )
        credentials = flow.run_console()

    with open(os.path.join(DIR,"CREDENTIALS_PICKLE_FILE"), 'wb') as f:
        pickle.dump(credentials, f)

    return googleapiclient.discovery.build(
        API_SERVICE_NAME, API_VERSION,
        credentials=credentials
    )

logger = setupLogger()

try:
  while True:
    main()
    time.sleep(1200) # Sleep for 20 minutes
except Exception as exc:
    message('THERE WAS AN ERROR OF SOME SORT...')
    logger.error('EXCEPTION: ' + exc)
except KeyboardInterrupt:
  print('Exiting...')
