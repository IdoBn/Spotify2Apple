import urllib
import requests
from spotify_share import __version__
from spotify_share import lib

import pytest


def test_version():
    assert __version__ == '0.1.0'


def test_spotify_api_tracks():
    res = requests.get(
        "https://api.spotify.com/v1/tracks/2dxjKgT0li4qBI3QwuN9Ih",
        headers={
            "Accept": "application/json", 
            "Content-Type": "application/json", 
            "Authorization": f"Bearer {lib.TOKEN}"
        }
    )

    assert res.json()["name"] == "Touch The Sky"


def test_spotify_api_episodes():
    res = requests.get(
        "https://api.spotify.com/v1/episodes/1HSwBvdcg3wzboD56sTVy0",
        headers={
            "Accept": "application/json", 
            "Content-Type": "application/json", 
            "Authorization": f"Bearer {lib.TOKEN}"
        }
    )

    assert res.json()["name"] == "פרק #488 - אבישי סאם ביטון והמטהוורס"


def test_apple_search_api():
    res = requests.get(
        f"https://itunes.apple.com/search?media=podcast&entity=podcastEpisode&limit=1&term=Geekonomy.net - גיקונומי+פרק #488 - אבישי סאם ביטון והמטהוורס"
    )

    assert res.json()["results"][0]["trackName"] == "פרק #488 - אבישי סאם ביטון והמטהוורס"


def test_convert_spotify_share_to_podcast():
    s = "https://open.spotify.com/episode/1HSwBvdcg3wzboD56sTVy0?si=EGYpo8CwQAe2UO9xGMunGA&utm_source=native-share-menu&nd=1"
    url = urllib.parse.urlparse(s)
    assert url.netloc == "open.spotify.com"
    path = url.path
    assert path == "/episode/1HSwBvdcg3wzboD56sTVy0"
    identifier = path.split("/")[-1]
    res = requests.get(
        f"https://api.spotify.com/v1/episodes/{identifier}",
        headers={
            "Accept": "application/json", 
            "Content-Type": "application/json", 
            "Authorization": f"Bearer {lib.TOKEN}"
        }
    )
    assert res.json()["name"] == "פרק #488 - אבישי סאם ביטון והמטהוורס"
    assert res.json()["show"]["name"] == "Geekonomy.net - גיקונומי"

    search_term = f"{res.json()['show']['name']}+{res.json()['name']}"

    res = requests.get(
        f"https://itunes.apple.com/search?media=podcast&entity=podcastEpisode&limit=1&term={search_term}"
    )

    assert res.json()["results"][0]["trackName"] == "פרק #488 - אבישי סאם ביטון והמטהוורס"


def test_spotify_podcast_to_apple_podcast_raises_on_bad_url():
    b1 = "a.com"
    with pytest.raises(lib.NotSpotifyException, match="a.com"):
        lib.spotify_podcast_to_apple_podcast(b1)

    b2 = "https://open.spotify.com/v1/tracks/2dxjKgT0li4qBI3QwuN9Ih"
    with pytest.raises(
        lib.NotSpotifyPodcastException, 
        match="https://open.spotify.com/v1/tracks/2dxjKgT0li4qBI3QwuN9Ih"
    ):
        lib.spotify_podcast_to_apple_podcast(b2)

    

def test_spotify_podcast_to_apple_podcast():
    s = "https://open.spotify.com/episode/1HSwBvdcg3wzboD56sTVy0?si=EGYpo8CwQAe2UO9xGMunGA&utm_source=native-share-menu&nd=1"
    res = lib.spotify_podcast_to_apple_podcast(s)
    assert res == "https://podcasts.apple.com/us/podcast/%D7%A4%D7%A8%D7%A7-488-%D7%90%D7%91%D7%99%D7%A9%D7%99-%D7%A1%D7%90%D7%9D-%D7%91%D7%99%D7%98%D7%95%D7%9F-%D7%95%D7%94%D7%9E%D7%98%D7%94%D7%95%D7%95%D7%A8%D7%A1/id1019124387?i=1000543666048&uo=4"


def test_spotify_song_to_apple_song():
    s = "https://open.spotify.com/track/2dxjKgT0li4qBI3QwuN9Ih?si=Q1174anXTXyaTGmVs7P5oQ&nd=1"
    res = lib.spotify_song_to_apple_song(s)
    assert res == "https://music.apple.com/us/album/touch-the-sky-feat-lupe-fiasco/1440668749?i=1440669048&uo=4"


