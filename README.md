<h1 align="center">LIFE PLAYLIST</h1>
<h4 align="center">The playlist of your life</h4>

<h5 align="center">" You can tell a lot about a person by what's on their playlist. "</h5>

<!--
### Need to be done.
- Based on playlist, recommend a book, brand, movie, something else..
-->



<img width="50%" alt="Screen Shot 2021-08-30 at 8 29 13 PM" src="https://user-images.githubusercontent.com/65331756/131341050-0f14978b-1394-44f4-9ac1-09cc461530de.png">

<img width="30%" alt="Screen Shot 2021-08-30 at 8 29 34 PM" src="https://user-images.githubusercontent.com/65331756/131341061-31d18df3-5950-48cc-a5ba-be24c1ca1e42.png">




## Still in progress 🤧 ~~

```
- Sign up, and make your own life playlist.
- Dashboard
- If someone has one song same with yours, you both will receive an email, and you guys can have a talk 🤡.
```


## 1. Reason:
- Just for fun.
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
##### Backgroud Schedule:
- apscheduler
##### VM:
- Google Compute Engine
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
