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

import os
import sys
import argparse
import google.auth
from googleapiclient.errors import HttpError
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request

class YoutubeUtil:
    def __init__(self, credentialJsonPath = "client_secret.json"):
        self.credentials = Credentials.from_authorized_user_file(credentialJsonPath)
        # YouTube Data API v3のサービスを作成
        self.youtube = build('youtube', 'v3', credentials=self.credentials)

    def parseTag(self, tags):
        tags = args.tags.split(',')
        if not tags:
            tags = ['']
        return tags

    DEF_PRIVACY_MAP={
        "public":"public",
        "unlisted":"unlisted",
        "private":"private",
    }

    def parsePrivacyStatus(self, privacyStatus):
        thePrivacy = privacyStatus.lower()
        privacyStatus = 'private'
        if thePrivacy in self.DEF_PRIVACY_MAP:
            privacyStatus = self.DEF_PRIVACY_MAP[thePrivacy]
        return privacyStatus

    def uploadVideo(self, videoPath, title="", description="", tags="", privacyStatus="private", categoryId="22", playListId="", isFamilySafe=False):
        if title == "":
            title=videoPath
        tags = self.parseTag(tags)
        privacyStatus = self.parsePrivacyStatus(privacyStatus)
        ytRating = "ytAgeRestricted"
        if isFamilySafe:
            ytRating = "ytRating:made_for_kids"

        theBody={
            "snippet": {
                "title": title,
                "description": description,
                "tags": tags,
                "categoryId": categoryId,
            },
            "status": {
                "privacyStatus": privacyStatus
            },
            #"contentDetails": {
            #    "contentRating": {
            #        "ytRating": ytRating
            #    }
            #}
        }
        if playListId!="":
            theBody["snippet"]["playlistId"] = playListId

        request = self.youtube.videos().insert(
            part="snippet,status",
            body=theBody,
            media_body=MediaFileUpload(videoPath, chunksize=-1, resumable=True)
        )
        response = None
        try:
            response = request.execute()
        except HttpError as e:
            print('An error occurred: %s' % e)

        return response

    def getPlayListId(self, playListTitle):
        request = self.youtube.search().list(
            part='id',
            q=playListTitle,
            type='playlist',
            fields='items(id(playlistId))'
        )
        response = None
        try:
            response = request.execute()
        except HttpError as e:
            print('An error occurred: %s' % e)

        playListId = None
        if None!=response and ('items' in response) and (len(response['items']) > 0):
            playListId = response['items'][0]['id']['playlistId']

        return playListId

    def createPlayList(self, playListTitle, privacyStatus="private"):
        request = self.youtube.playlists().insert(
            part="snippet,status",
            body={
                "snippet": {
                    "title": playListTitle
                },
                "status": {
                    "privacyStatus": privacyStatus
                }
            }
        )
        response = None
        try:
            response = request.execute()
        except HttpError as e:
            print('An error occurred: %s' % e)

        if None!=response and ("id" in response):
            return response["id"]

        return None

    def uploadVideoWithPlayList(self, videoPath, title="", description="", tags="", privacyStatus="private", categoryId="22", playListTitle="", playListId="", isFamilySafe=False):
        response = None
        if playListId=="":
            if playListTitle != "":
                playListId = self.getPlayListId(playListTitle)
                if playListId is None:
                    playListId = self.createPlayList(playListTitle)
                print("playListId="+playListId)
        response = self.uploadVideo(videoPath, title, description, tags, privacyStatus, categoryId, playListId, isFamilySafe)
        return response


if __name__=="__main__":
    parser = argparse.ArgumentParser(description="Upload video to YouTube")
    parser.add_argument('file', help="Path to video file")
    parser.add_argument("-s", "--title", action="store", help="Title of the video", required=True)
    parser.add_argument("-d", "--description", action="store", help="Description of the video", default="")
    parser.add_argument("-p", "--privacy", choices=["public", "unlisted", "private"], default="private")
    parser.add_argument("-t", "--tags", action="store", help="Tags for the video (Use , sepator)", default="")
    parser.add_argument("-l", "--playlist", type=str, help="Create playList with specified title (high cost)", default="")
    parser.add_argument("--playlistId", type=str, help="Specify PlayListId (low cost)", default="")

    args = parser.parse_args()

    youtube = YoutubeUtil("client_secret.json")
    response = youtube.uploadVideoWithPlayList(args.file, args.title, args.description, args.tags, args.privacy, "22", args.playlist, args.playlistId)
    print(response)
