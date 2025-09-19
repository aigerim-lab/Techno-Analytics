Select * from events where genreid=1
Order by date;



Select genreid, 
Count(*) 
From artists
Group by genreid;



Select locationid,
Count(*)
From users
Group by locationid;



Select id,name,date
from events 
Order by date Desc
Limit 5;



Select a.username, b.name As favourite_artist
From favoriteartists fa 
Join users a On fa.userid=a.id
Join artists b On fa.artistid=b.id;




SELECT e.name AS event_name, l.name AS location_name
FROM events e
INNER JOIN locations l ON e.locationid = l.id;




SELECT u.username, c.name AS country_name
FROM users u
LEFT JOIN locations l ON u.locationid = l.id
LEFT JOIN countries c ON l.countryid = c.id;



SELECT a.name AS artist_name, g.name AS genre_name
FROM artists a
RIGHT JOIN genres g ON a.genreid = g.id;


SELECT e.name AS event_name, g.name AS genre_name
FROM events e
LEFT JOIN genres g ON e.genreid = g.id;


SELECT u.username, g.name AS favorite_genre
FROM favoritegenres fg
INNER JOIN users u ON fg.userid = u.id
INNER JOIN genres g ON fg.genreid = g.id;
