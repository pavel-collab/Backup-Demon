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

# скопировать все файлы с текущей дериктории в контейнер
COPY . /usr/src/app/
# команды, выполняющиеся при запуске контейнера
# CMD ["python", "RunDemod.py"]