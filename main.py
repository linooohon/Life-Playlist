import os
from app import create_app, db
from app.settings import FLASK_ENV
# from flask_script import Manager
from flask_migrate import Migrate


app = create_app(FLASK_ENV)
migrates = Migrate(app=app, db=db)
# manager = Manager(app)

@app.cli.command()
def test():
    import unittest
    import sys

    # Test Case -> every text_xx method, 一個 method 就是一個 test case
    # Test Suite -> Test case 集合
    # Test Loader -> 加載 Test case 到 Test suite
    # Text Test Runner -> 執行 run ， 測試結果存在 Texttestresult
    # 把 tests 資料夾裡的 test_xx.py 裡的 text_xx 方法
    tests = unittest.TestLoader().discover("tests")
    result = unittest.TextTestRunner(verbosity=2).run(tests)    #verbosity=2 列印測試訊息更詳細
    if result.errors or result.failures:   #處理錯誤
        sys.exit(1)   #(0) 無錯誤退出 (1)有錯誤退出，1 告知這個程序是捕獲到異常，是非正常退出

if __name__ == '__main__':
    app.run(debug=True)
