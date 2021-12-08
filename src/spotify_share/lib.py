import os
import urllib
import requests
import itertools

TOKEN = os.environ["SPOTIFY_TOKEN"]

class NotSpotifyException(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)

class NotSpotifyPodcastException(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)

def spotify_podcast_to_apple_podcast(url: str) -> str:
    parsed_url = urllib.parse.urlparse(url)
    if parsed_url.netloc != "open.spotify.com":
        raise NotSpotifyException(url)

    if not parsed_url.path.startswith("/episode"):
        raise NotSpotifyPodcastException(url)

    _, _episodes, identifier = parsed_url.path.split("/")
    res_spotify = requests.get(
        f"https://api.spotify.com/v1/episodes/{identifier}",
        headers={
            "Accept": "application/json", 
            "Content-Type": "application/json", 
            "Authorization": f"Bearer {TOKEN}"
        }
    )

    search_term = f"{res_spotify.json()['show']['name']}+{res_spotify.json()['name']}"
    res = requests.get(
        f"https://itunes.apple.com/search?media=podcast&entity=podcastEpisode&limit=1&term={search_term}"
    )

    return res.json()["results"][0]["trackViewUrl"]


def spotify_song_to_apple_song(url: str) -> str:
    parsed_url = urllib.parse.urlparse(url)
    if parsed_url.netloc != "open.spotify.com":
        raise NotSpotifyException(url)

    if not parsed_url.path.startswith("/track"):
        raise NotSpotifyPodcastException(url)

    _, _track, identifier = parsed_url.path.split("/")
    res_spotify = requests.get(
        f"https://api.spotify.com/v1/tracks/{identifier}",
        headers={
            "Accept": "application/json", 
            "Content-Type": "application/json", 
            "Authorization": f"Bearer {TOKEN}"
        }
    )

    search_term = "+".join([
        res_spotify.json()["name"],
        res_spotify.json()["album"]["name"],
        *itertools.chain([
            artist["name"] 
            for artist in res_spotify.json()["album"]["artists"]
        ])
    ])
    print(search_term)
    res = requests.get(
        f"https://itunes.apple.com/search?media=music&limit=1&term={search_term}"
    )

    return res.json()["results"][0]["trackViewUrl"]