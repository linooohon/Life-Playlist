# from app.model.models import Playlist, Dashboard
# from app.repo.repo import Repo
# import json



# def update_dashboard_url():
#     dashboard_data = Dashboard.query.all()
#     dashboard_raw_list = []
#     for i in dashboard_data:
#         item = {
#             "dashboard_artist": i.dashboard_artist,
#             "artist_genres": i.artist_genres
#         }
#         dashboard_raw_list.append(item)
#         print(i.artist_genres)
#         # call cloud function(dashboard_raw_list) -> compare_thesoundsofspotify_playlist_and_dashboard_raw_list(dashboard_raw_list)

# # cloud function
# def update_thesoundsofspotify_playlist():
#     """monthly update thesoundsofspotify_playlist to gcp data storage
#     """

# # cloud function
# # def compare_thesoundsofspotify_playlist_and_dashboard_raw_list(request):
