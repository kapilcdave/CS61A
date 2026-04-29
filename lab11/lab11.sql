CREATE table newest AS
  SELECT title, year
  FROM titles
  ORDER BY year DESC
  LIMIT 10;


CREATE TABLE dog_movies AS 
  SELECT titles.title, principals.character
  FROM titles JOIN principals ON titles.tconst = principals.tconst
  WHERE principals.character LIKE '%dog%';

    
CREATE table leads AS 
  SELECT names.name, COUNT(*) AS lead_roles
  FROM names JOIN principals ON names.nconst = principals.nconst
  WHERE principals.ordering = 1
  GROUP BY principals.nconst
  HAVING COUNT(*) > 10;


CREATE table long_movies AS 
  SELECT "REPLACE THIS LINE WITH YOUR SOLUTION";

