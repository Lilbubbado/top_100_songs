import requests
from bs4 import BeautifulSoup
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from pprint import pprint

SPOTIFY_ID = 'id'
SPOTIFY_SECRET = 'secret'
REDIRECT_URI = 'http://example.com'
SCOPE = 'user-library-read'
date = input('When would you like to go back to? (YYYY-MM-DD): ')
year = date[0:4]

# SCRAPING THE BILLBOARD TOP 100 WEBSITE FOR THE LIST OF SONGS FROM ANY GIVEN DATE
response = requests.get(url=f"https://www.billboard.com/charts/hot-100/{date}/")
web_page = response.text

soup = BeautifulSoup(web_page, "html.parser")

song_tags = soup.select(selector='li h3', class_='c-title', id='title-of-a-story')
artist_tags = soup.select(selector='div ul li li span', class_='a-no-trucate a-font-primary-s lrv-u-font-size-14@mobile-max u-line-height-normal@mobile-max u-letter-spacing-0021 lrv-u-display-block a-truncate-ellipsis-2line u-max-width-330 u-max-width-230@tablet-only u-font-size-20@tablet')

numbers = [str(i) for i in range(0, 101)]


artist_list = []
for artist in artist_tags:
    artist_string = artist.get_text().strip()
    try:
        int(artist_string)
    except ValueError:
        if artist_string != '-':
            artist_list.append(artist_string.split()[0])
print(artist_list)
print(len(artist_list))


song_list = []
for song in song_tags[:100]:
    song_title = song.get_text().strip()
    if song_title != 'Songwriter(s):' and song_title != 'Producer(s):' and song_title != 'Imprint/Promotion Label:':
        song_list.append(song_title)
# print(song_list)
# print(len(song_list))



# AUTHENTICATING SPOTIFY
spotify = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=SPOTIFY_ID,
                                                    client_secret=SPOTIFY_SECRET,
                                                    redirect_uri=REDIRECT_URI,
                                                    cache_path="token.txt",
                                                    scope=SCOPE))


user = spotify.current_user()['display_name']
print(user)

# ADDING THE SONG IDs TO A LIST
spotify_songs = []
for i in range(0, 100):
    track = (spotify.search(q=f'track: {song_list[i]} artist: {artist_list[i]}', limit=1, type='track'))
    # Track URI-spotify_songs[index]['tracks']['items'][0]['uri']
    spotify_songs.append(track['tracks']['items'][0]['uri'])
print(spotify_songs)

# CREATING THE NEW PLAYLIST FOR THE SONGS
playlist = spotify.user_playlist_create(user=user, name=f'{date} Billboard 100', public=False, description=f'An album of the Billboard Top 100 Songs for {date}.')
playlist_id = playlist['id']
# ADDING THE SONGS TO THE PLAYLIST
spotify.playlist_add_items(playlist_id=playlist_id, items=spotify_songs)