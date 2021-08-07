<h1 align="center">LIFE PLAYLIST</h1>
<h5 align="center">The playlist of your life</h5>

### todo item
<!--

<done>
- 計算出 dashboard 的前 10 名 並且給予 youtube 和 spotify 的連結 api 

- 根據個人寫入的資料，顯示出他可能會感興趣的歌手
<done>
- 人生歌單限定只能新增 10 首，如果有人的人生歌單, 與另一個人有 3 首一樣，就會推薦彼此的個人 email 和 名字給對方。 

-->

## 1. Reason:
## 2. Tools:
##### Web Server:
- uWSGI
- Nginx
##### Testing:
- Unittest
##### Flask:
- Flask_Login
- Flask_Migrate
- Flask_SQLAlchemy
- Flask_Caching
- Flask-Mail
##### Spotify API:
- spotipy

## 3. Develop with Docker environment:
1. edit `.env` file:
```
FLASK_ENV=development_docker
```
2. run:
```
$ docker-compose up
```
#### Migrate in Docker environment:
```
$ docker ps
$ docker exec -it <CONTAINER ID> bash
$ flask db init
$ flask db migrate -m "init db"
$ flask db upgrade
```


## 4. Run testing:
1. Go to the path which is same as `main.py`.
2. Then you can run,
```
$ flask test
```
