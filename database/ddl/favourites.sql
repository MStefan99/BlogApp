create table favourites
(
	user_id integer not null
		constraint favourites_users_id_fk
			references users
				on delete cascade,
	post_id integer not null
		constraint favourites_posts_id_fk
			references posts
				on delete cascade,
	date_added text not null
);

create unique index favourites_user_id_post_id_uindex
	on favourites (user_id, post_id);