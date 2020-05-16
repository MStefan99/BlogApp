create table users
(
    username          text    not null,
    password          text    not null,
    cookieid          text    not null,
    email             text    not null,
    id                integer not null
        constraint users_pk
            primary key autoincrement,
    verification_link text,
    verified          integer default 0 not null,
    recovery_link     text,
    verified_email    text
);

create unique index users_cookieid_uindex
    on users (cookieid);

create unique index users_recovery_link_uindex
    on users (recovery_link);

create unique index users_username_uindex
    on users (username);

create unique index users_verification_link_uindex
    on users (verification_link);

create unique index users_verified_email_uindex
    on users (verified_email);