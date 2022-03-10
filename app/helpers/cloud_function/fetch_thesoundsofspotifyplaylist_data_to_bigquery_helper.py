# https://us-west1-lifeplaylistforfun.cloudfunctions.net/update_thesoundsofspotify_playlist_to_bigquery
import requests
from datetime import datetime
from .get_google_id_token import get_google_id_token

def fetch_thesoundsofspotifyplaylist_data_to_bigquery_helper(thesoundsofspotifyplaylist_update_to_bigquery_logger):
    try:
        calling_utc_time = str(datetime.utcnow())
        print(calling_utc_time)
        thesoundsofspotifyplaylist_update_to_bigquery_logger.info(
            f"Start, fetch_thesoundsofspotifyplaylist_data_to_bigquery_helper -> time: {calling_utc_time} / UTC+0")
        # param 代時間，只是送一個 para 觸發 cloud function
        param = {"run": calling_utc_time}
        print(param)
        url = 'https://us-west1-lifeplaylistforfun.cloudfunctions.net/update_thesoundsofspotify_playlist_to_bigquery'
        response_ = requests.post(
            url,  json=param, headers={"Authorization": "Bearer {}".format(get_google_id_token())})

        # response_ = requests.get(
        #     'https://asia-east1-my-app-324417.cloudfunctions.net/update_thesoundsofspotify_playlist_to_bigquery')
        print(response_.json())
        finished_time = str(datetime.utcnow())
        thesoundsofspotifyplaylist_update_to_bigquery_logger.info(
            f"Finished, fetch_thesoundsofspotifyplaylist_data_to_bigquery_helper -> time: {finished_time} / UTC+0")
    except Exception as ex:
        time = str(datetime.utcnow())
        print(
            f"Failed, fetch_thesoundsofspotifyplaylist_data_to_bigquery_helper is failed -> time: {time} / UTC+0, the error is ==={ex}===")
        thesoundsofspotifyplaylist_update_to_bigquery_logger.error(
            f"Failed, fetch_thesoundsofspotifyplaylist_data_to_bigquery_helper is failed -> time: {time} / UTC+0, the error is ==={ex}===")
