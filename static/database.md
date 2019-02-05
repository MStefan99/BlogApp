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
create table Credentials
(
    Login VARCHAR(255) not null
        constraint Credentials_pk
            primary key,
    Password VARCHAR(255) not null,
    CookieID VARCHAR(255) not null,
    Email VARCHAR(255),
    Admin BOOLEAN default FALSE not null
);

create unique index Credentials_CookieID_uindex
    on Credentials (CookieID);

create unique index Credentials_Email_uindex
    on Credentials (Email);

create unique index Credentials_Login_uindex
    on Credentials (Login);
````