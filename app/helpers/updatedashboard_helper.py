import sys
import collections
import time
from app import db, sp
from app.model.models import Playlist, Dashboard
from youtubesearchpython import VideosSearch


def search_on_youtube(artist_and_song):
    videosSearch = VideosSearch(artist_and_song, limit=1)
    if videosSearch.result()['result'] == []:
        return 'None'
    else:
        return 'https://www.youtube.com/watch?v=' + videosSearch.result()['result'][0]['id']


def search_on_spotify(artist):
    r = sp.search(q=artist, limit=3, type='artist')
    if r['artists']['total'] == 0:
        return 'None'
    else:
        # make spotify uri
        id = r['artists']['items'][0]['id']
        uri = f"spotify:artist:{id}"
        return uri

    # for idx, track in enumerate(r['tracks']['items']):
    #     print(idx, track['name'], track['uri']) # uri 可以開啟 spotify 播到那首歌

    # lz_uri = 'spotify:artist:36QJpDe2go2KgaRleHCDTp'
    # results = sp.artist_top_tracks(lz_uri)
    # for track in results['tracks'][:10]:
    #     print('track    : ' + track['name'])
    #     print('audio    : ' + track['preview_url'])  #這個可以聽30秒
    #     print('cover art: ' + track['album']['images'][0]['url'])
    #     print()
    # results = sp.search(q='weezer', limit=20)
    # print(results)


def fetch_spotify_youtube():
    print(time.strftime("%A, %d. %B %Y %I:%M:%S %p"))
    print('call spotify and youtube api')
    try:
        all_playlist = Playlist.query.all()
        print("query is fine")

        count_songs_preset_list = []
        dashboard_top10_list_duplicate = []
        # loop db all playlist, i == each row
        for i in all_playlist:
            whole_name = i.artist + i.song
            # to lower, strip away blank, split() to list make sure no blank
            whole_name_list = whole_name.lower().strip().split()
            whole_name_string = ''.join(whole_name_list)  # list t0 string
            count_songs_preset_list.append(whole_name_string)

            # get top10 most songs to tuple, but here still in lower case and no blank between artist and song
            playlist_tupleList = collections.Counter(
                count_songs_preset_list).most_common(10)

        # get correct artist and correct song which is showed in playlist_tupleList, and append to List, so here is not only 10 items in List, it will be duplicated.
        for i in range(0, len(all_playlist)):
            for j in range(0, len(playlist_tupleList)):
                if ''.join((all_playlist[i].artist + all_playlist[i].song).lower().strip().split()) == playlist_tupleList[j][0]:
                    dashboard_top10_list_duplicate.append(all_playlist[i])

        final_pre_list = []
        final_lower_list = []
        final_list = []
        # pre-process, make sure no blank in artist and song
        for i in dashboard_top10_list_duplicate:
            i.artist = i.artist.strip()
            i.song = i.song.strip()
            final_pre_list.append(i)

        # 過濾重複的 item, 所以只要是在小寫清單有的話, 就不再把真正 user 填的字串放到 final_list
        for i in final_pre_list:
            artist_and_song_lowerstring = ''.join(
                (i.artist + i.song).lower().strip().split())
            if artist_and_song_lowerstring not in final_lower_list:
                final_lower_list.append(artist_and_song_lowerstring)
                final_list.append(i)

        # clean all data in table first
        Dashboard.query.delete()
        # use Youtbue API and Spotify API
        for i in final_list:
            # find song's url on youtube
            artist_and_song = i.artist + i.song
            i.youtube_url = search_on_youtube(artist_and_song)
            # find artist's page on spotify
            i.spotify_uri = search_on_spotify(i.artist)

            # update db
            new_top10_data = Dashboard(
                dashboard_artist=i.artist, dashboard_song=i.song, artist_spotify_uri=i.spotify_uri, song_youtube_url=i.youtube_url)
            db.session.add(new_top10_data)
            db.session.commit()
        print("update to db success")
    except:
        print("Unexpected error when execute spotify youtube api:",
              sys.exc_info()[0])
