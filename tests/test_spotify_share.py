from spotify_share import __version__
from spotify_share import lib


def test_version():
    assert __version__ == "0.1.0"


def test_spotify_to_apple_track():
    s = "https://open.spotify.com/track/2dxjKgT0li4qBI3QwuN9Ih?si=Q1174anXTXyaTGmVs7P5oQ&nd=1"
    res = lib.spotify_to_apple(s)
    assert (
        res
        == "https://music.apple.com/us/album/touch-the-sky-feat-lupe-fiasco/1440668749?i=1440669048&uo=4"
    )


def test_spotify_to_apple_episode():
    s = "https://open.spotify.com/episode/1HSwBvdcg3wzboD56sTVy0?si=EGYpo8CwQAe2UO9xGMunGA&utm_source=native-share-menu&nd=1"
    res = lib.spotify_to_apple(s)
    assert (
        res
        == "https://podcasts.apple.com/us/podcast/%D7%A4%D7%A8%D7%A7-488-%D7%90%D7%91%D7%99%D7%A9%D7%99-%D7%A1%D7%90%D7%9D-%D7%91%D7%99%D7%98%D7%95%D7%9F-%D7%95%D7%94%D7%9E%D7%98%D7%94%D7%95%D7%95%D7%A8%D7%A1/id1019124387?i=1000543666048&uo=4"
    )


def test_spotify_to_apple_moshe():
    s = "https://open.spotify.com/show/5NoPOwKd4iGBa9exY6bFeV?si=UYbiKqSRRma4u529PK1i8A"
    res = lib.spotify_to_apple(s)
    assert (
        res
        == "https://podcasts.apple.com/us/podcast/%D7%94%D7%A7%D7%A6%D7%91%D7%99%D7%99%D7%94-the-butcher-shop/id1578164732?uo=4"
    )
