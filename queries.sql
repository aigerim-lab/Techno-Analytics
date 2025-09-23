-- 1. Shows all events where genre = 1, ordered by date
Select * from events where genreid=1
Order by date;


-- 2. Count of artists in each genre by combining together
Select genreid, 
Count(*) 
From artists
Group by genreid;


-- 3. Count users by locationid and group them together
Select locationid,
Count(*)
From users
Group by locationid;


-- 4. Show the 5 most recent events
Select id,name,date
from events 
Order by date Desc
Limit 5;


--5. Show users with their favorite artists
Select a.username, b.name As favourite_artist
From favoriteartists fa 
Join users a On fa.userid=a.id
Join artists b On fa.artistid=b.id;



--6. Show event names with their location names
SELECT e.name AS event_name, l.name AS location_name
FROM events e
INNER JOIN locations l ON e.locationid = l.id;



-- 7. Show users with their country names
SELECT u.username, c.name AS country_name
FROM users u
LEFT JOIN locations l ON u.locationid = l.id
LEFT JOIN countries c ON l.countryid = c.id;


-- 8. Show artists with their genre names
SELECT a.name AS artist_name, g.name AS genre_name
FROM artists a
RIGHT JOIN genres g ON a.genreid = g.id;

-- 9. Show events with their genres
SELECT e.name AS event_name, g.name AS genre_name
FROM events e
LEFT JOIN genres g ON e.genreid = g.id;

-- 10. Show users and their favorite genres
SELECT u.username, g.name AS favorite_genre
FROM favoritegenres fg
INNER JOIN users u ON fg.userid = u.id
INNER JOIN genres g ON fg.genreid = g.id;
