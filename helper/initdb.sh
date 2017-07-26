create table item_list (
  rid integer,
  lid integer,
  mls integer,
  lat float,
  lon float,
  url text,
  price integer,
  tax integer,
  beds integer,
  baths float,
  lot: float,
  initial_access integer,
  last_access integer
);

create table list_html (
    rid integer,
    html text
);

create table photo (
  lid integer,
  mls integer,
  file text
);

