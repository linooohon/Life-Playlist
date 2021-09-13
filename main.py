import sys
import unittest
from apscheduler.schedulers.background import BackgroundScheduler
from werkzeug.serving import is_running_from_reloader
from flask_migrate import Migrate

from app import create_app, db
from app.settings import FLASK_ENV
from app.helpers.updatedashboard_helper import fetch_spotify_youtube
from app.helpers.sendsoulmate_helper import check_same_song_lover
from app.helpers.updateuserplaylist_helper import update_user_playlist
from app.helpers.background_helper import BackgroundHelper

app = create_app(FLASK_ENV)
migrates = Migrate(app=app, db=db)


@app.cli.command()
def test():
    """[summary]
    Test Case -> every text_xx method, 一個 method 就是一個 test case
    Test Suite -> Test case 集合
    Test Loader -> 加載 Test case 到 Test suite
    Text Test Runner -> 執行 run ， 測試結果存在 Texttestresult
    把 tests 資料夾裡的 test_xx.py 裡的 text_xx 方法
    """
    tests = unittest.TestLoader().discover("tests")
    result = unittest.TextTestRunner(verbosity=2).run(
        tests)  # verbosity=2 列印測試訊息更詳細
    if result.errors or result.failures:  # 處理錯誤
        sys.exit(1)  # (0) 無錯誤退出 (1)有錯誤退出，1 告知這個程序是捕獲到異常，是非正常退出

trigger_background_job = BackgroundHelper(app)


# [Legacy - testing]
# def dashboard_background_update():
#     with app.app_context():
#         fetch_spotify_youtube()
# def soulmate_email_background_sending():
#     with app.app_context():
#         check_same_song_lover()
# def user_playlist_background_update():
#     with app.app_context():
#         update_user_playlist()


# dashboard_scheduler = BackgroundScheduler()
# dashboard_scheduler.add_job(func=dashboard_background_update,
#                             trigger="interval", days=1)
# dashboard_scheduler.start()

# email_sending_scheduler = BackgroundScheduler({'apscheduler.timezone': 'UTC'})
# email_sending_scheduler.add_job(func=soulmate_email_background_sending,
#                                 trigger="interval", days=1, start_date='2021-9-12 00:00:00')
# email_sending_scheduler.start()

# search_userplaylist_scheduler = BackgroundScheduler(
#     {'apscheduler.timezone': 'UTC'})
# search_userplaylist_scheduler.add_job(
#     func=user_playlist_background_update, trigger="interval", days=1, start_date='2021-9-13 13:00:00')
# search_userplaylist_scheduler.start()


if __name__ == '__main__':
    app.run(debug=True, use_reloader=False)
    # app.run(debug=True)
