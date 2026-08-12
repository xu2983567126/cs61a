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

-------------------------------------------------------------
-- PLEASE DO NOT CHANGE ANY SQL STATEMENTS ABOVE THIS LINE --
-------------------------------------------------------------

-- The size of each dog
CREATE TABLE size_of_dogs AS
  SELECT "REPLACE THIS LINE WITH YOUR SOLUTION";


-- All dogs with parents ordered by decreasing height of their parent
CREATE TABLE by_parent_height AS
  SELECT "REPLACE THIS LINE WITH YOUR SOLUTION";


-- Sentences about siblings that are the same size
CREATE TABLE sentences AS
  SELECT "REPLACE THIS LINE WITH YOUR SOLUTION";
  

-- [Optional] Filling out this helper table is recommended
CREATE TABLE siblings AS
  SELECT "REPLACE THIS LINE WITH YOUR SOLUTION";

-- Sentences about siblings that are the same size
CREATE TABLE sentences AS
  SELECT "REPLACE THIS LINE WITH YOUR SOLUTION";


-- Ways to stack 4 dogs to a height of at least 175, ordered by total height
CREATE TABLE stacks AS
  SELECT "REPLACE THIS LINE WITH YOUR SOLUTION";


-- Ways to stack 4 dogs to a height of at least 175, ordered by total height
CREATE TABLE stacks_helper(dogs, stack_height, last_height, n);

-- Add your INSERT INTOs here


CREATE TABLE stacks AS
  SELECT "REPLACE THIS LINE WITH YOUR SOLUTION";


-- Height range for each fur type where all of the heights differ by no more than 30% from the average height
CREATE TABLE low_variance AS
  SELECT "REPLACE THIS LINE WITH YOUR SOLUTION";


-- Heights and names of dogs that are above average in height among
-- dogs whose height has the same first digit.
CREATE TABLE above_average AS
  SELECT "REPLACE THIS LINE WITH YOUR SOLUTION";


-- non_parents is an optional, but recommended question
-- All non-parent relations ordered by height difference
CREATE TABLE non_parents as
  SELECT "REPLACE THIS LINE WITH YOUR SOLUTION";
