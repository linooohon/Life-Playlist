<h1 align="center">LIFE PLAYLIST</h1>
<h4 align="center">The playlist of your life</h4>

<h5 align="center">" You can tell a lot about a person by what's on their playlist. "</h5>

<!--
### Need to be done.
- Based on playlist, recommend a book, brand, movie, something else..
-->

<div align="center">
<img width="30%" alt="Screen Shot 2022-01-05 at 7 42 23 PM" src="https://user-images.githubusercontent.com/65331756/148212293-fcf3996c-a778-48c8-b039-29d652784c42.png">
</div>

<div align="center">
<img width="60%" alt="Screen Shot 2022-01-05 at 7 49 55 PM" src="https://user-images.githubusercontent.com/65331756/148213161-5c23e8aa-5e0b-42ee-bc45-fef4b05e0e22.png">
</div>

## Still in progress 🤧 ~~

```
- Dashboard
- Sign up, and make your own life playlist.
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
1. Under the path which is same as `main.py`.
2. Then you can run,
```
$ flask test
```
