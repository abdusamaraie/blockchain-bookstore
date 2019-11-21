DROP TABLE IF EXISTS Users;
Create table IF NOT EXISTS Users (
    userId integer primary key autoincrement,
    name text not null,
    email text not null,
    password text not null
);

DROP TABLE IF EXISTS Items;
Create Table IF NOT EXISTS Items(
itemId integer primary key autoincrement,
userId integer ,
name text not null,
disc text not null,
pictureURL text not null,
FOREIGN KEY (userId) REFERENCES Users(userId)
);



