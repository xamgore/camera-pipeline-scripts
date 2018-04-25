import os
import pickle
from os import path
from google_auth_oauthlib.flow import InstalledAppFlow as get_auth_token
from googleapiclient.discovery import build as get_client
from os.path import join, dirname


class YoutubeClient(object):
    CREDENTIALS_FILE = join(dirname(__file__), 'credentials.pickle')
    CLIENT_SECRET = join(dirname(__file__), 'client_secret.json')


    def __init__(self, scopes):
        self.__client = YoutubeClient.__get_youtube_client(scopes)


    def fetch_links_to_all_videos(self):
        return [
            f'youtu.be/{video}?list={list}'
            for list in self.playlists()
            for video in self.videos_in(list)
        ]


    def fetch_thumbnails_of_new_videos(self):
        return [video for list in self.playlists() for video in self.videos_in(list)]


    def upload_thumbnail(self, video_id, file_path):
        self.__client.thumbnails().set(videoId=video_id, media_body=file_path).execute()


    def get_uploads_playlist(self):
        """
        :return: a list of playlists "upload" for each channel of the user
        """

        uploads = []
        req = self.__client.channels().list(mine=True, part='contentDetails', maxResults=50,
                                            fields='items/contentDetails/relatedPlaylists/uploads')

        while req:
            res = req.execute()
            uploads.extend(i['contentDetails']['relatedPlaylists']['uploads'] for i in res['items'])
            req = self.__client.playlists().list_next(req, res)

        return uploads


    def playlists(self):
        """
        Fetch all playlists, which belong to the authorized user.

        :return: a list of playlists' ids
        """

        playlists = []
        req = self.__client.playlists().list(mine=True, part='id', maxResults=50, fields='items/id')

        while req:
            res = req.execute()
            # the response format is described at goo.gl/GQVTJo
            playlists.extend(item['id'] for item in res['items'])
            req = self.__client.playlists().list_next(req, res)

        return playlists


    def videos_in(self, playlist_id):
        """
        Fetch all videos, which are stored in the playlist

        :param playlist_id: the unique id of the playlist, from YoutubeClient.playlists method
        :return: a list of videos' ids
        """

        req = self.__client.playlistItems().list(
            playlistId=playlist_id, part='contentDetails', maxResults=50,
            fields='items/contentDetails/videoId')

        videos = []

        while req:
            res = req.execute()
            # the response format is described at goo.gl/RAfUj7
            videos.extend(item['contentDetails']['videoId'] for item in res['items'])
            req = self.__client.playlistItems().list_next(req, res)

        return videos


    @staticmethod
    def __get_youtube_client(scopes):
        token = YoutubeClient.__load_refresh_token()

        if not token:
            authorizer = get_auth_token \
                .from_client_secrets_file(YoutubeClient.CLIENT_SECRET, scopes)

            token = authorizer.run_local_server(port=34343) \
                if 'DISPLAY' in os.environ else authorizer.run_console()

            YoutubeClient.__save_refresh_token(token)

        return get_client('youtube', 'v3', credentials=token)


    @staticmethod
    def __load_refresh_token():
        if path.exists(YoutubeClient.CREDENTIALS_FILE):
            with open(YoutubeClient.CREDENTIALS_FILE, 'rb') as f:
                return pickle.load(f)
        return None


    @staticmethod
    def __save_refresh_token(credentials):
        with open(YoutubeClient.CREDENTIALS_FILE, 'wb') as f:
            pickle.dump(credentials, f)
