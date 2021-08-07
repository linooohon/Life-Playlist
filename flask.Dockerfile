FROM python:3.7.2-stretch
LABEL owner="linooohon"
LABEL version="1.0"
LABEL description="flasklifeplaylist_image"
ENV PYTHONUNBUFFERED 1
#設定工作目錄之後的 RUN CMD ENTRYPOINT COPY ADD 都會在這個底下執行
WORKDIR /app 

#將 <來源path> 放到 <目標path底下>
ADD . /app
COPY * /app
RUN echo flask.Dockerfile RUN command start && echo $HOME
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
RUN ["echo", "flask.Dockerfile RUN command end"]
CMD ["uwsgi", "wsgi.ini"] #run when container is starting