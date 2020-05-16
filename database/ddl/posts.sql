create table posts
(
    id          integer not null
        constraint posts_pk
            primary key autoincrement,
    title       text    not null,
    tagline     text    not null,
    image       text,
    splash      text,
    theme_color text    not null,
    link        text    not null,
    author      text    not null,
    content     text    not null,
    date        text    not null,
    tags        text
);