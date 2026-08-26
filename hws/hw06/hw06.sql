CREATE TABLE parents (parent TEXT, child TEXT);

INSERT INTO parents VALUES
  ('ace', 'bella'),
  ('ace', 'charlie'),
  ('daisy', 'hank'),
  ('finn', 'ace'),
  ('finn', 'daisy'),
  ('finn', 'ginger'),
  ('ellie', 'finn');

CREATE TABLE dogs (name TEXT, fur TEXT, height INTEGER);

INSERT INTO dogs VALUES
  ('ace',     'long',  26),
  ('bella',   'short', 52),
  ('charlie', 'long',  47),
  ('daisy',   'long',  46),
  ('ellie',   'short', 35),
  ('finn',    'curly', 32),
  ('ginger',  'short', 28),
  ('hank',    'curly', 31);

CREATE TABLE sizes (size TEXT, min INTEGER, max INTEGER);

INSERT INTO sizes VALUES
  ('toy',      24, 28),
  ('mini',     28, 35),
  ('medium',   35, 45),
  ('standard', 45, 60);


-- All dogs with parents ordered by decreasing height of their parent
CREATE TABLE by_parent_height AS
  select child
  from parents as p join dogs as d on p.parent = d.name
  order by d.height desc;


-- The size of each dog
CREATE TABLE size_of_dogs AS
  select name, size
  from dogs as d join sizes as s
  where height > min and height <= max;


-- [Optional] Filling out this helper table is recommended
CREATE TABLE siblings AS
  select p1.child as c1, p2.child as c2
  from parents as p1, parents as p2
  where p1.parent = p2.parent and c1 < c2;

-- Sentences about siblings that are the same size
CREATE TABLE sentences AS
  SELECT "The two siblings, " || c1 || " and " || c2 || ", have the same size: " || d.size
    FROM (siblings as a join size_of_dogs as b on a.c1 = b.name) as d join size_of_dogs as e on d.c2 = e.name
    WHERE e.size = d.size;


-- Height range for each fur type where all of the heights differ by no more than 30% from the average height
CREATE TABLE low_variance AS
  SELECT fur, MAX(height) - MIN(height) AS height_range FROM dogs GROUP BY fur
      HAVING MIN(height) >= .7 * AVG(height) AND MAX(height) <= 1.3 * AVG(height);

