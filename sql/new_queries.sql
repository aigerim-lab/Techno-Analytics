-- name: q1_users_by_country(Pie Chart)
SELECT c.name AS country, COUNT(u.id) AS user_count
FROM users u
JOIN locations l ON u.locationid = l.id
JOIN countries c ON l.countryid = c.id
GROUP BY c.name;

-- name: q2_events_by_genre(Bar Chart)
SELECT g.name AS genre, COUNT(e.id) AS event_count
FROM events e
JOIN genres g ON e.genreid = g.id
GROUP BY g.name;

-- name: q3_top_artists_by_events(Horizontal Bar Chart)
SELECT a.name AS artist, COUNT(ea.eventid) AS event_count
FROM eventartists ea
JOIN artists a ON ea.artistid = a.id
GROUP BY a.name
ORDER BY event_count DESC
LIMIT 10;

-- name: q4_events_by_month (Line Chart)
SELECT DATE_TRUNC('month', e.date) AS month, COUNT(*) AS event_count
FROM events e
GROUP BY month
ORDER BY month;

-- name: q5_rating_distribution
SELECT eh.rate
FROM eventhistory eh
WHERE eh.rate IS NOT NULL;





-- name: q6_rating_vs_attendance
SELECT eh.userid, AVG(eh.rate) AS avg_rating, COUNT(eh.eventid) AS attended_events
FROM eventhistory eh
WHERE eh.hasattended = 1
GROUP BY eh.userid;

-- name: q7_fav_genres_per_user
SELECT u.username, COUNT(fg.genreid) AS fav_genres
FROM favoritegenres fg
JOIN users u ON fg.userid = u.id
GROUP BY u.username;

-- name: q8_fav_artists_by_country
SELECT c.name AS country, COUNT(fa.artistid) AS fav_artists
FROM favoriteartists fa
JOIN users u ON fa.userid = u.id
JOIN locations l ON u.locationid = l.id
JOIN countries c ON l.countryid = c.id
GROUP BY c.name;

-- name: q9_avg_rating_by_genre
SELECT g.name AS genre, AVG(eh.rate) AS avg_rating
FROM eventhistory eh
JOIN events e ON eh.eventid = e.id
JOIN genres g ON e.genreid = g.id
WHERE eh.rate IS NOT NULL
GROUP BY g.name;

-- name: q10_artist_popularity_by_country
SELECT a.name AS artist, c.name AS country, COUNT(eh.id) AS attendance
FROM eventhistory eh
JOIN events e ON eh.eventid = e.id
JOIN eventartists ea ON ea.eventid = e.id
JOIN artists a ON ea.artistid = a.id
JOIN locations l ON e.locationid = l.id
JOIN countries c ON l.countryid = c.id
WHERE eh.hasattended = 1
GROUP BY a.name, c.name
ORDER BY attendance DESC;

