# Usage
Build:
```bash
docker build . --platform=linux/amd64 --tag 857256614217.dkr.ecr.eu-west-2.amazonaws.com/my-first-ecr-repo:0.1
```

# Goals
Create a bot that accepts a link from spotify.
1. If the link is to a song it returns a link to that song on apple music
2. If the link is of a podcast it returns that link on overcast.fm

## Spotify
Here are the spotify APIs that we need:
* In case of song (or "track")
    ```python
    res = requests.get(
        "https://api.spotify.com/v1/tracks/2dxjKgT0li4qBI3QwuN9Ih",
        headers={
            "Accept": "application/json", 
            "Content-Type": "application/json", 
            "Authorization": "Bearer BQB-..."
        }
    )

    assert res.json()["name"] == "Touch The Sky"
    ```

* In case of podcast (or "episode")
    ```python
    res = requests.get(
        "https://api.spotify.com/v1/episodes/1HSwBvdcg3wzboD56sTVy0",
        headers={
            "Accept": "application/json", 
            "Content-Type": "application/json", 
            "Authorization": "Bearer BQB-..."
        }
    )

    assert res.json()["name"] == "פרק #488 - אבישי סאם ביטון והמטהוורס"
    ```

## Apple Music
They have a search api but need nimrod to wakeup to give me creds to it...

## Overcast[.]fm
We can incorporate the itunes api and the overcast[.]fm api to make this simpler.
1. Use the itunes api to search for the podcast itunes identifier: ```https://itunes.apple.com/search\?term\=geekonomy```
2. Query overcast: ```curl -vvv https://overcast.fm/itunes1019124387 -H "Cookie: o=..." --location-trusted```. This will return a bunch of html that will need to be parsed for the exact podcast episode name. We can use ```beautifulsoup``` for this...

## Apple Podcasts
I think I will also cover apple podcasts because I might want to switch to their app as well...
We can search for the podcast via itunes using the following snippet:
```python
res = requests.get(
    f"https://itunes.apple.com/search?media=podcast&entity=podcastEpisode&limit=1&term=Geekonomy.net - גיקונומי+פרק #488 - אבישי סאם ביטון והמטהוורס"
)
```

## Spotify -> Apple Podcast flow
