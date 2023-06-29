SELECT *
FROM PortfolioProject..credits

SELECT *
FROM PortfolioProject..titles

--Change columns in tables from text to nvarchar(MAX) so they can be sorted alphabetically
ALTER TABLE PortfolioProject..credits
ALTER COLUMN id nvarchar(MAX)

ALTER TABLE PortfolioProject..credits
ALTER COLUMN name nvarchar(MAX)

ALTER TABLE PortfolioProject..credits
ALTER COLUMN character nvarchar(MAX)

ALTER TABLE PortfolioProject..credits
ALTER COLUMN role nvarchar(MAX)

ALTER TABLE PortfolioProject..titles
ALTER COLUMN title nvarchar(MAX)

ALTER TABLE PortfolioProject..titles
ALTER COLUMN id nvarchar(MAX)

ALTER TABLE PortfolioProject..titles
ALTER COLUMN type nvarchar(MAX)

ALTER TABLE PortfolioProject..titles
ALTER COLUMN description nvarchar(MAX)

ALTER TABLE PortfolioProject..titles
ALTER COLUMN genres nvarchar(MAX)

ALTER TABLE PortfolioProject..titles
ALTER COLUMN production_countries nvarchar(MAX)

--Looking at movie titles and credits
--Join credits to titles to figure out all actors in all movies and shows, order by actor name and remove any characters where the actor name is not known
SELECT *
FROM PortfolioProject..credits AS c
RIGHT JOIN PortfolioProject..titles AS t
ON c.id = t.id
WHERE c.name NOT LIKE '%?%' AND c.name IS NOT NULL
ORDER BY c.name ASC

--Create view joining both title and credit files
CREATE VIEW titlesandcredits AS
SELECT c.id, c.person_id, c.name, c.character, c.role, t.title, t.type, t.description, t.release_year, t.age_certification, t.runtime, t.genres, t.production_countries, t.seasons, t.imdb_id, t.imdb_score, t.imdb_votes, t.tmdb_popularity, t.tmdb_score
FROM PortfolioProject..credits AS c
RIGHT JOIN PortfolioProject..titles AS t
ON c.id = t.id

--Sort actors by average imdb score and sort by top actors for imdb scores
SELECT TOP 5 name, ROUND(AVG(imdb_score), 2) as average_imdb_score
FROM titlesandcredits
WHERE name NOT LIKE '%?%' AND name IS NOT NULL AND role = 'actor'
GROUP BY name
HAVING AVG(imdb_score) IS NOT NULL
ORDER BY AVG(imdb_score) DESC, name ASC

--Sort directors by average imdb score and sort by top directors for imdb scores
SELECT TOP 5 name, ROUND(AVG(imdb_score), 2) as average_imdb_score
FROM titlesandcredits
WHERE name NOT LIKE '%?%' AND name IS NOT NULL AND role = 'director'
GROUP BY name
HAVING AVG(imdb_score) IS NOT NULL
ORDER BY AVG(imdb_score) DESC, name ASC

--Looking at Netflix shows only
--Sort by top rated shows
SELECT TOP 5 title, ROUND(imdb_score,2) AS imdb_score
FROM PortfolioProject..titles
WHERE imdb_score IS NOT NULL AND type = 'SHOW'
ORDER BY imdb_score DESC, title ASC

--Looking at Netflix movies only
--Sort by top rated movies
SELECT TOP 5 title, ROUND(imdb_score, 2) AS imdb_score
FROM PortfolioProject..titles
WHERE imdb_score IS NOT NULL AND type = 'MOVIE'
ORDER BY imdb_score DESC, title ASC

--Looking at top actors/directors by show/movie rating on Netflix
SELECT TOP 5 name, role, ROUND(MAX(imdb_score),2) AS imdb_score
FROM titlesandcredits
WHERE imdb_score IS NOT NULL AND name IS NOT NULL AND name NOT LIKE '%?%'
GROUP BY name, role
ORDER BY imdb_score DESC

--Top rated movies or shows by actor sorted by rating
SELECT name, title, imdb_score
FROM titlesandcredits
WHERE imdb_score IS NOT NULL AND name IS NOT NULL AND name NOT LIKE '%?%' AND role = 'Actor'
ORDER BY name ASC, imdb_score DESC

--Top rated movies or shows by director sorted by rating
SELECT name, title, imdb_score
FROM titlesandcredits
WHERE imdb_score IS NOT NULL AND name IS NOT NULL AND name NOT LIKE '%?%' AND role = 'Director'
ORDER BY name ASC, imdb_score DESC

--Select all data and remove nulls and ? for visualization
SELECT *
FROM titlesandcredits
WHERE name NOT LIKE '%?%' AND imdb_score IS NOT NULL
