# Database creation script

For the server to work you need to create a database 
which will store all information that server needs to operate.

First, you need to create a folder next to the server location 
called `database` and an sqlite database called `db.sqlite`:

````
/
|-- app/
|     |-- static/
|     |     `--  css
|     |            `-- style.css
|     |     `-- ...
|     |-- templates/
|     |     |-- account.html
|     |     `-- ...
|     |-- blog_app.py
|     `-- blog_app.wsgi
`-- database/
      `-- db.sqlite       
````

Then open the database and execute this setup script:

````
create table Posts
(
	ID INTEGER not null
		constraint Posts_pk
			primary key autoincrement,
	Title VARCHAR(256) not null,
	Tagline VARCHAR(512) not null,
	Image VARCHAR(512),
	Splash VARCHAR(512),
	Theme_Color CHARACTER(7),
	Link VARCHAR(512) not null,
	Author VARCHAR(256) not null,
	Date VARCHAR(30) not null,
	Content TEXT not null,
	Tags TEXT
);

create unique index Posts_ID_uindex
	on Posts (ID);

create table Users
(
	Username VARCHAR(255) not null,
	Password VARCHAR(255) not null,
	CookieID VARCHAR(255) not null,
	Email VARCHAR(255) not null,
	ID INTEGER not null
		constraint Users_pk
			primary key autoincrement
);

create unique index Users_CookieID_uindex
	on Users (CookieID);

create unique index Users_Email_uindex
	on Users (Email);

create unique index Users_ID_uindex
	on Users (ID);


create table Favourites
(
	User_ID INTEGER not null
		constraint Favourites_Users_ID_fk
			references Users,
	Post_ID INTEGER not null
		constraint Favourites_Posts_ID_fk
			references Posts,
	Date_Added TEXT default '1970-01-01 00:00:00' not null
);

create unique index Favourites_Post_ID_uindex
	on Favourites (Post_ID);
````