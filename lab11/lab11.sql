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
  SELECT (year / 10 * 10) || 's' AS decade, COUNT(*) AS count
  FROM titles
  WHERE runtime > 180
  GROUP BY decade;

