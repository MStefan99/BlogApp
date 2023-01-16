FROM debian:buster-slim

RUN apt-get update
RUN apt-get install curl apache2 python3 python3-pip libapache2-mod-wsgi-py3 sqlite3 -y
RUN curl -sL https://deb.nodesource.com/setup_14.x | bash -
RUN apt-get install nodejs -y
RUN npm install less --global

COPY app/ /var/www/blog/
COPY docker-setup/apache-config/ /etc/apache2/

RUN a2enmod wsgi
RUN a2dissite 000-default

WORKDIR /var/www/blog/
RUN sqlite3 database/db.sqlite "$(cat database/ddl/users.sql \
database/ddl/posts.sql \
database/ddl/favourites.sql)"
RUN chmod 777 -R database
RUN pip3 install -r requirements.txt
RUN echo "import sys\n\
sys.path.insert(0, '/var/www/blog/')\n\
\n\
from blog_app import app as application\n" > blog_app.wsgi
WORKDIR /var/www/blog/static/css
RUN ls -lahR ..
RUN for file in *.less; do lessc $file $(basename $file | sed s/\.less/.css/g) ; done

RUN a2ensite blog

ENTRYPOINT service apache2 start && tail -F .
