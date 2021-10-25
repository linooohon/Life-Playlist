import sys
import collections
import time
import random
import json
import pkgutil
from google.cloud import bigquery
# from google.cloud import bigquery_storage_v1beta1.reader.ReadRowsIterable
from google.oauth2 import service_account
from app.settings import GCP_PROJECT_NAME


from datetime import datetime
from threading import current_thread
from youtubesearchpython import VideosSearch

from app import db, sp
from app.model.models import Playlist, Dashboard
from app.repo.repo import Repo


def search_on_youtube(artist_and_song):
    videosSearch = VideosSearch(artist_and_song, limit=1)
    if videosSearch.result()['result'] == []:
        return 'None'
    else:
        return 'https://www.youtube.com/watch?v=' + videosSearch.result()['result'][0]['id']


def search_on_spotify(artist):
    """Fetch Spotify API

    Get artist spotify page:
        - method (1)
        id = r['artists']['items'][0]['id']
        uri = f"spotify:artist:{id}"

        - method (2)
        uri = r['artists']['items'][0]['uri']

    """
    r = sp.search(q=artist, limit=3, type='artist')
    if r['artists']['total'] == 0:
        return 'None', 'None', 'None'
    else:
        uri = r['artists']['items'][0]['uri']
        pic_url = r['artists']['items'][0]['images'][0]['url']
        genres = r['artists']['items'][0]['genres']
        return uri, pic_url, genres


def get_dashboard_artistandgenres_list():
    dashboard_data = Dashboard.query.all()
    dashboard_raw_list = []
    for i in dashboard_data:
        item = {
            "dashboard_artist": i.dashboard_artist,
            "artist_genres": i.artist_genres
        }
        dashboard_raw_list.append(item)
        # print(i.artist_genres)
    return dashboard_raw_list


def compare_genres_and_find_uri(dashboard_list_, total_df_list_):
    total_list = []
    for i in dashboard_list_:
        pair_list = []
        total_list.append(pair_list)
        for j in total_df_list_:
            for genre in i['artist_genres']:
                concat_genre = 'the sound of ' + genre
                if concat_genre == j[2].lower():
                    uri, name = j[1], j[2]
                    data = {
                        "uri": uri,
                        "name": name,
                        "genre": genre
                    }
                    pair_list.append(data)

    print(total_list)
    return total_list


def insert_genres_uri(total_list):
    dashboard_data = Dashboard.query.all()
    try:
        for index, item in enumerate(dashboard_data):
            item.artist_genres_spotify_uri = total_list[index]
            db.session.commit()
            print("update to db success")
    except Exception as ex:
        print(f"Fail: {ex}")
        return False
    return True


def get_thesoundsofspotify_playlist_bigquery_data():
    service_account_info = pkgutil.get_data("app", "config/client_secret.json")
    credentials = service_account.Credentials.from_service_account_info(
        json.loads(service_account_info.decode()))
    # print("111111")
    # with open('client_secret.json', newline='') as jsonfile:
    # client_secret_list = json.load(jsonfile)     ##或者這樣 client_secret_list = json.loads(jsonfile.read())
    # credentials = service_account.Credentials.from_service_account_info(client_secret_list)
    client = bigquery.Client(project=GCP_PROJECT_NAME, credentials=credentials)
    # print(client)
    # print("22222")
    # # Download a table.
    # table_id = "my-app-324417.demo.demo_table_name"
    # table = bigquery.TableReference.from_string(table_id)
    # print(table)
    # rows = client.list_rows(
    #     table,
    #     selected_fields=[
    #         bigquery.SchemaField("index", "INT64"),
    #         bigquery.SchemaField("uri", "STRING"),
    #         bigquery.SchemaField("name", "STRING"),
    #     ],
    # )
    # for i in rows:
    #     print(i)
    # print(type(rows))
    # dataframe = rows.to_dataframe()
    # print("123")
    # print(dataframe)
    # total_df_list_ = dataframe.values.tolist()
    # print(total_df_list_)
    # return ["123"]

    sql = """
        SELECT *
        FROM `my-app-324417.demo.demo_table_name`
    """
    query_job = client.query(sql)
    df = query_job.to_dataframe()
    # print(df)
    try:
        total_df_list_ = df.values.tolist()
    except Exception as ex:
        print(ex)
    # print(total_df_list_)
    return total_df_list_

    # print("Query results:")
    # print(df)
    # print("\nGet 1st row values")
    # print(df.iloc[0])


def update_thesoundsofspotify_playlist_uri_to_dashboard_db():
    total_df_list_ = get_thesoundsofspotify_playlist_bigquery_data()
    # print("1")
    dashboard_list_ = get_dashboard_artistandgenres_list()
    # print("2")
    total_list = compare_genres_and_find_uri(dashboard_list_, total_df_list_)
    # print("3")
    if insert_genres_uri(total_list):
        return "update dashboard genres uri successful."


def fetch_spotify_youtube(dashboard_update_logger):
    # logging.basicConfig(
    #     filename="dashboard_update.log", level=logging.INFO)
    # print(time.strftime("%A, %d. %B %Y %I:%M:%S %p"))
    # print('call spotify and youtube api')
    current_time = str(datetime.utcnow())
    try:
        repo = Repo(Playlist)
        all_playlist = repo.get_all()
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
            time.sleep(random.randrange(1, 3))
            # find song's url on youtube
            artist_and_song = i.artist + i.song
            i.youtube_url = search_on_youtube(artist_and_song)
            # find artist's page on spotify
            i.spotify_uri, i.spotify_image_url, i.genres = search_on_spotify(
                i.artist)

            data_dict = {
                "dashboard_artist": i.artist,
                "dashboard_song": i.song,
                "artist_spotify_uri": i.spotify_uri,
                "artist_spotify_image_url": i.spotify_image_url,
                "song_youtube_url": i.youtube_url,
                "artist_genres": i.genres
            }
            # update db
            repo = Repo(Dashboard)
            repo.insert_data(data_dict)
        print("update to db success")
        dashboard_update_logger.info(
            f"SUCCESS, fetch spotify and youtube api, finished updated dashboard -> time: {current_time} / UTC+0")
        update_thesoundsofspotify_playlist_uri_to_dashboard_db()
        dashboard_update_logger.info(
            f"SUCCESS, update dashboard genres uri successful. -> time: {current_time} / UTC+0")
    except:
        dashboard_update_logger.info(
            f"FAIL, fetch spotify and youtube api, updating dashboard have some problem -> time: {current_time} / UTC+0")
        print("Unexpected error when execute spotify youtube api:",
              sys.exc_info()[0])











# [Legacy]

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
