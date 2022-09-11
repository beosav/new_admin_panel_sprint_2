-- psql -h 127.0.0.1 -U postgres -f movies_database.sql

create extension if not exists "uuid-ossp";

create schema content;
set search_path to content, public;
grant all privileges on database movies_database to app;
alter role app set search_path to content, public;


create table if not exists content.film_work (
    id uuid primary key,
    title text not null,
    description text,
    creation_date date,
    rating float,
    certificate TEXT,
    file_path TEXT,
    type text not null,
    created timestamp with time zone default now(),
    modified timestamp with time zone default now()


    
        
);

create table if not exists content.person (
    id uuid primary key,
    full_name text not null,
    birth_date DATE,
    created timestamp with time zone default now(),
    modified timestamp with time zone default now()
);

create table if not exists content.genre (
    id uuid primary key,
    name text not null,
    description text,
    created timestamp with time zone default now(),
    modified timestamp with time zone default now()
);

create table if not exists content.person_film_work (
    id uuid primary key,
    person_id uuid not null,
    film_work_id uuid not null,
    role text not null,
    created timestamp with time zone default now(),
	unique(film_work_id, person_id, role)
);

create table if not exists content.genre_film_work (
    id uuid primary key,
    genre_id uuid not null,
    film_work_id uuid not null,
    created timestamp with time zone default now(),
    modified timestamp with time zone default now()
);


create index film_work_idx
on content.film_work(title, rating, creation_date, rating, type);

create index person_idx
on content.person(full_name);

create index genre_name_idx
on content.genre(name);

create unique index person_film_work_idx
on content.person_film_work(person_id, film_work_id, role);

create index genre_film_work_idx
on content.genre_film_work(film_work_id, genre_id);

create type gender as enum ('male', 'female');
alter table person add column "gender" gender null;
alter table person_film_work alter column role drop not null; 