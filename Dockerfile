FROM ubuntu:20.04
# команда, которую надо выполнить (до запуска самого контейнера)
RUN mkdir -p /usr/src/app/
RUN apt-get update
RUN apt-get install -y python3
RUN apt-get install -y pip
RUN apt-get install -y vim
# выполнение всех команд с указанного каталога
WORKDIR /usr/src/app/

# переменной окружения указываем часовую зону
ENV TZ Europe/Moscow

# скопировать файлы с текущей дериктории в контейнер
COPY RunDemod.py /usr/src/app/RunDemod.py
COPY Demon.py /usr/src/app/Demon.py
COPY YaDbackup.py /usr/src/app/YaDbackup.py
COPY YD_API.py /usr/src/app/YD_API.py
COPY config.json /usr/src/app/config.json
COPY token /usr/src/app/token
# команды, выполняющиеся при запуске контейнера
# CMD ["python", "RunDemod.py"]