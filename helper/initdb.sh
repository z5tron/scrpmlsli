create table home (
  lid integer PRIMARY KEY,
  lat float,
  lon float,
  url text,
  dest text,
  accinitial integer,
  acclast integer
);

create table file (
  lid integer,
  dest text
);

