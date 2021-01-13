# youtube-live-notification

## Run on boot
Edit crontab `crontab -e` and add the following line

```@reboot python3 /path/to/youtube-live-notification/notification.py &```

## Youtube
- Enable YouTube Data API v3 - `https://console.developers.google.com/apis/library/youtube.googleapis.com`
- Add Google API Credentials - `https://console.developers.google.com/apis/credentials/`
  - Create `OAuth client`, the download client secret and place in the project root dir. Rename to `client_secrets.json`

## Twilio account
