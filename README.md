# youtube-live-notification

## Run on boot
Edit crontab `crontab -e` and add the following line

```@reboot python3 /path/to/youtube-live-notification/notification.py &```

## Youtube
https://developers.google.com/youtube/v3/docs/search/list
- Enable YouTube Data API v3 - https://console.developers.google.com/apis/library/youtube.googleapis.com
- Add Google API Credentials - https://console.developers.google.com/apis/credentials/
  - Create `OAuth client`, the download client secret and place in the project root dir. Rename to `client_secrets.json`

## Twilio account


## TODO
use OAuth playground? https://stackoverflow.com/questions/19766912/how-do-i-authorise-an-app-web-or-installed-without-user-intervention/19766913#19766913