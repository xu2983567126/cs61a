CREATE table newest AS
  select title, year
  from titles 
  order by year desc limit 10;


CREATE table dog_movies AS 
  select title, character 
  from titles as t join principals as p on t.tconst = p.tconst 
  where character like "%dog%";


CREATE table leads AS 
  SELECT name, count(*) AS lead_roles
  FROM principals as p JOIN names as n ON p.nconst = n.nconst
  WHERE p.ordering = 1
  GROUP BY name
  HAVING count(*) > 10;

CREATE table long_movies AS 
  SELECT (year / 10 * 10) || "s" AS decade, count(*) AS count
  FROM titles
  WHERE runtime > 180
  GROUP BY decade;

