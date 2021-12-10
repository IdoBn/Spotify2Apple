import os
import urllib.parse
import requests
import itertools

TOKEN = os.environ["SPOTIFY_TOKEN"]


class NotSpotifyException(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)


class UnhandledSpotifyEntity(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)


class SpotifyNetworkException(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)


def _spotify_podcast_to_apple_podcast(identifier: str) -> str:
    res_spotify = requests.get(
        f"https://api.spotify.com/v1/episodes/{identifier}",
        headers={
            "Accept": "application/json",
            "Content-Type": "application/json",
            "Authorization": f"Bearer {TOKEN}",
        },
    )

    if res_spotify.status_code != 200:
        raise SpotifyNetworkException(res_spotify.status_code)


    search_term = f"{res_spotify.json()['show']['name']}+{res_spotify.json()['name']}"
    res = requests.get(
        f"https://itunes.apple.com/search?media=podcast&entity=podcastEpisode&limit=1&term={search_term}"
    )

    return res.json()["results"][0]["trackViewUrl"]


def _spotify_song_to_apple_song(identifier: str) -> str:
    res_spotify = requests.get(
        f"https://api.spotify.com/v1/tracks/{identifier}",
        headers={
            "Accept": "application/json",
            "Content-Type": "application/json",
            "Authorization": f"Bearer {TOKEN}",
        },
    )

    if res_spotify.status_code != 200:
        raise SpotifyNetworkException(res_spotify.status_code)

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


def _spotify_show_to_apple_show(identifier: str) -> str:
    res_spotify = requests.get(
        f"https://api.spotify.com/v1/shows/{identifier}",
        headers={
            "Accept": "application/json",
            "Content-Type": "application/json",
            "Authorization": f"Bearer {TOKEN}",
        },
    )

    if res_spotify.status_code != 200:
        raise SpotifyNetworkException(res_spotify.status_code)

    search_term = res_spotify.json()['name']
    res = requests.get(
        f"https://itunes.apple.com/search?media=podcast&entity=podcast&limit=1&term={search_term}"
    )

    return res.json()["results"][0]["trackViewUrl"]


def spotify_to_apple(url: str) -> str:
    parsed_url = urllib.parse.urlparse(url)
    if parsed_url.netloc != "open.spotify.com":
        raise NotSpotifyException(url)

    if parsed_url.path.startswith("/episode"):
        _, _track, identifier = parsed_url.path.split("/")
        return _spotify_podcast_to_apple_podcast(identifier)
    elif parsed_url.path.startswith("/track"):
        _, _track, identifier = parsed_url.path.split("/")
        return _spotify_song_to_apple_song(identifier)
    elif parsed_url.path.startswith("/show"):
        _, _track, identifier = parsed_url.path.split("/")
        return _spotify_show_to_apple_show(identifier)
    else:
        raise UnhandledSpotifyEntity(url)
