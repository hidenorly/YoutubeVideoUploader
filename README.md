# YoutubeVideoUploader

```
usage: youtube_uploader.py [-h] -s TITLE [-d DESCRIPTION] [-p {public,unlisted,private}] [-t TAGS] [-l PLAYLIST] [--playlistId PLAYLISTID] file

Upload video to YouTube

positional arguments:
  file                  Path to video file

optional arguments:
  -h, --help            show this help message and exit
  -s TITLE, --title TITLE
                        Title of the video
  -d DESCRIPTION, --description DESCRIPTION
                        Description of the video
  -p {public,unlisted,private}, --privacy {public,unlisted,private}
  -t TAGS, --tags TAGS  Tags for the video (Use , sepator)
  -l PLAYLIST, --playlist PLAYLIST
                        Create playList with specified title (high cost)
  --playlistId PLAYLISTID
                        Specify PlayListId (low cost)
```

# How to setup

## pip

```
pip install google-api-python-client
```

## Enable Youtube API

1. Login to Google Cloud Console. Click create project.

2. Choose the project. Click API and Service/Dashboard

3. Enable "YouTube Data API v3"

4. Click to API Service -> Authenticate information

5. Create authentication info. and choose OAuth Client ID.

7. Choose desktop app of the app category.

8. Download the auth info. as ```client_secret_downloaded.json```

9. Set the scope
 ```https://www.googleapis.com/auth/youtube.upload```
 ```https://www.googleapis.com/auth/youtube```
 ```https://www.googleapis.com/auth/youtube.readonly```
 ```https://www.googleapis.com/youtube/v3/search```
 
 ## Get refersh token

```
python3 get_referesh_token.py
```

You need to allow permission to the app on browser.
Note that you need to login with your account which you want to upload to.
And then token is output.

You need to set the refresh_token to ```client_secret.json``` based on ```client_secret_downloaded.json```
But don't forget to remove "installed":{}. The ```client_secret.json``` only requires the following:

```
{ # Don't forget to remove "installed":{}
    "client_id":"xxxxx0oe.apps.googleusercontent.com",
    "project_id":"xxxx",
    "auth_uri":"https://accounts.google.com/o/oauth2/auth",
    "token_uri":"https://oauth2.googleapis.com/token",
    "auth_provider_x509_cert_url":"https://www.googleapis.com/oauth2/v1/certs",
    "client_secret":"xxxx",
    "refresh_token":"xxxx"  # you need to fill the print out here
}
```

 ## Now you can upload .mp4,etc. to youtube.

```
python3 youtube_uploader.py movie.mp4 -s "test title" -d "my test video" -p private -t "test,uploader"
```

Note that ```client_secret.json``` is required by get_referesh_token.py with the downloaded client secret
