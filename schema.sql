CREATE TABLE USER
(user_id INTEGER NOT NULL,
username VARCHAR(20),
email VARCHAR(40),
password VARCHAR(15),
register_date VARCHAR(16),
PRIMARY KEY (user_id));

CREATE TABLE PHOTO
(photo_id INTEGER NOT NULL,
photo_path VARCHAR(150),
upload_date VARCHAR(16),
uploaded_by INTEGER NOT NULL,
PRIMARY KEY (photo_id),
FOREIGN KEY (uploaded_by) REFERENCES USER(user_id));

CREATE TABLE ALBUM
(album_id INTEGER NOT NULL,
name VARCHAR(25),
owner VARCHAR(25), first_photo VARCHAR(80),
PRIMARY KEY (album_id),
FOREIGN KEY (owner) REFERENCES USER(user_id));

CREATE TABLE PHOTO_LIKES
(photo_id INTEGER,
liked_by INTEGER,
liked_date VARCHAR(16),
FOREIGN KEY (photo_id) REFERENCES PHOTO(photo_id),
FOREIGN KEY (liked_by) REFERENCES USER(user_id));

CREATE TABLE PHOTO_TAGS
(photo_id INTEGER NOT NULL,
tag VARCHAR(40),
FOREIGN KEY (photo_id) REFERENCES PHOTO(photo_id));

CREATE TABLE ALBUM_PHOTOS
(album_id INTEGER,
photo_id INTEGER,
FOREIGN KEY (album_id) REFERENCES ALBUM(album_id),
FOREIGN KEY (photo_id) REFERENCES PHOTO(photo_id))
;


