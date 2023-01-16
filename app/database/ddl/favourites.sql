create table if not exists favourites
(
    user_id    integer not null
        references users
            on delete cascade,
    post_id    integer not null
        references posts
            on delete cascade,
    date_added text    not null
);

create unique index if not exists favourites_user_id_post_id_uindex
    on favourites (user_id, post_id);
