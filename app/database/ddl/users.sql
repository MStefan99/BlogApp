create table if not exists users
(
    username          text    not null,
    password          text    not null,
    cookieid          text    not null,
    email             text    not null,
    id                integer not null
        primary key autoincrement,
    verification_link text,
    verified          integer default 0 not null,
    recovery_link     text,
    verified_email    text
);

create unique index if not exists users_cookieid_uindex
    on users (cookieid);

create unique index if not exists users_recovery_link_uindex
    on users (recovery_link);

create unique index if not exists users_username_uindex
    on users (username);

create unique index if not exists users_verification_link_uindex
    on users (verification_link);

create unique index if not exists users_verified_email_uindex
    on users (verified_email);
