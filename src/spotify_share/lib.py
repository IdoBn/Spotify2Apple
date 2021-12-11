import os
from typing import Any
import urllib.parse
import requests
import itertools
import base64
from datetime import datetime
from typing import Dict, Any


class NotSpotifyException(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)


class UnhandledSpotifyEntity(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)


class SpotifyNetworkException(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)


class SpotifyAPI:
    def __init__(self, client_id: str, client_secret: str, refresh_token: str) -> None:
        self._authorization = base64.b64encode(
            client_id.encode() + b":" + client_secret.encode()
        ).decode()
        self._refresh_token = refresh_token
        self._generate_access_token()

    def _generate_access_token(self) -> str:
        res = requests.post(
            "https://accounts.spotify.com/api/token",
            headers={"Authorization": f"Basic {self._authorization}"},
            data={"grant_type": "refresh_token", "refresh_token": self._refresh_token},
        )
        self._access_token = res.json()["access_token"]
        self._expiration_time = datetime.fromtimestamp(
            datetime.now().timestamp() + res.json()["expires_in"]
        )

    def get(self, route: str) -> Dict[str, Any]:
        if datetime.now() > self._expiration_time:
            self._generate_access_token()

        res_spotify = requests.get(
            route,
            headers={
                "Accept": "application/json",
                "Content-Type": "application/json",
                "Authorization": f"Bearer {self._access_token}",
            },
        )

        if res_spotify.status_code != 200:
            raise SpotifyNetworkException(res_spotify.status_code)

        return res_spotify


def _spotify_podcast_to_apple_podcast(spotify_api: SpotifyAPI, identifier: str) -> str:
    res_spotify = spotify_api.get(f"https://api.spotify.com/v1/episodes/{identifier}")

    search_term = f"{res_spotify.json()['show']['name']}+{res_spotify.json()['name']}"
    res = requests.get(
        f"https://itunes.apple.com/search?media=podcast&entity=podcastEpisode&limit=1&term={search_term}"
    )

    return res.json()["results"][0]["trackViewUrl"]


def _spotify_song_to_apple_song(spotify_api: SpotifyAPI, identifier: str) -> str:
    res_spotify = spotify_api.get(f"https://api.spotify.com/v1/tracks/{identifier}")

    search_term = "+".join(
        [
            res_spotify.json()["name"],
            res_spotify.json()["album"]["name"],
            *itertools.chain(
                [artist["name"] for artist in res_spotify.json()["album"]["artists"]]
            ),
        ]
    )
    res = requests.get(
        f"https://itunes.apple.com/search?media=music&limit=1&term={search_term}"
    )

    return res.json()["results"][0]["trackViewUrl"]


def _spotify_show_to_apple_show(spotify_api: SpotifyAPI, identifier: str) -> str:
    res_spotify = spotify_api.get(f"https://api.spotify.com/v1/shows/{identifier}")

    search_term = res_spotify.json()["name"]
    res = requests.get(
        f"https://itunes.apple.com/search?media=podcast&entity=podcast&limit=1&term={search_term}"
    )

    return res.json()["results"][0]["trackViewUrl"]


def spotify_to_apple(spotify_api: SpotifyAPI, url: str) -> str:
    parsed_url = urllib.parse.urlparse(url)
    if parsed_url.netloc != "open.spotify.com":
        raise NotSpotifyException(url)

    if parsed_url.path.startswith("/episode"):
        _, _track, identifier = parsed_url.path.split("/")
        return _spotify_podcast_to_apple_podcast(spotify_api, identifier)
    elif parsed_url.path.startswith("/track"):
        _, _track, identifier = parsed_url.path.split("/")
        return _spotify_song_to_apple_song(spotify_api, identifier)
    elif parsed_url.path.startswith("/show"):
        _, _track, identifier = parsed_url.path.split("/")
        return _spotify_show_to_apple_show(spotify_api, identifier)
    else:
        raise UnhandledSpotifyEntity(url)
