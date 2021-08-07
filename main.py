import sys
import atexit
import unittest
from apscheduler.schedulers.background import BackgroundScheduler

from flask_migrate import Migrate

from app import create_app, db
from app.settings import FLASK_ENV
from app.helpers.updatedashboard_helper import fetch_spotify_youtube


app = create_app(FLASK_ENV)
migrates = Migrate(app=app, db=db)

@app.cli.command()
def test():
    # Test Case -> every text_xx method, 一個 method 就是一個 test case
    # Test Suite -> Test case 集合
    # Test Loader -> 加載 Test case 到 Test suite
    # Text Test Runner -> 執行 run ， 測試結果存在 Texttestresult
    # 把 tests 資料夾裡的 test_xx.py 裡的 text_xx 方法
    tests = unittest.TestLoader().discover("tests")
    result = unittest.TextTestRunner(verbosity=2).run(tests)    #verbosity=2 列印測試訊息更詳細
    if result.errors or result.failures:   #處理錯誤
        sys.exit(1)   #(0) 無錯誤退出 (1)有錯誤退出，1 告知這個程序是捕獲到異常，是非正常退出


def dashboard_background_update():
    with app.app_context():
        fetch_spotify_youtube()
    
# https://apscheduler.readthedocs.io/en/stable/modules/triggers/interval.html?highlight=days
scheduler = BackgroundScheduler()
scheduler.add_job(func=dashboard_background_update,
                  trigger="interval", seconds=10)
scheduler.start()

# Shut down the scheduler when exiting the app
atexit.register(lambda: scheduler.shutdown())


if __name__ == '__main__':
    app.run(debug=True, use_reloader=False)
