PRAGMA foreign_keys = ON;


DROP TABLE IF EXISTS Schedule;
DROP TABLE IF EXISTS Cinema;
DROP TABLE IF EXISTS Users;
DROP TABLE IF EXISTS UserRole;


CREATE TABLE UserRole (
    UserRole_ID  INTEGER PRIMARY KEY AUTOINCREMENT,
    name         TEXT NOT NULL UNIQUE,
    description  TEXT
);

INSERT INTO UserRole (name)
VALUES
    ('sysadmin'),
    ('cinema_admin'),
    ('buyer');

CREATE TABLE Users (
    User_ID       INTEGER PRIMARY KEY AUTOINCREMENT,
    UserRole_ID   INTEGER NOT NULL,
    Imya     TEXT NOT NULL,
    login         TEXT NOT NULL UNIQUE,
    passwordHash  TEXT NOT NULL,
    FOREIGN KEY (UserRole_ID) REFERENCES UserRole(UserRole_ID)
        ON UPDATE CASCADE
        ON DELETE RESTRICT
);

INSERT INTO Users (UserRole_ID, Imya, login, passwordHash)
VALUES
    (1, 'Semen',     'admin',       'hash1'),
    (2, 'Dana',      'cin_admin',   'hash2'),
    (3, 'Alexander', 'Pistoletov',  'hash3');

CREATE TABLE Cinema (
    Cinema_ID    INTEGER PRIMARY KEY AUTOINCREMENT,
    name         TEXT NOT NULL,
    description  TEXT,
    link         TEXT
);

INSERT INTO Cinema (name, description, link)
VALUES
    ('Пыльная радуга', 'Лучший кинотеатр forever', 'https://music.yandex.ru/artist/3033108');

CREATE TABLE Film (
    Film_ID INTEGER PRIMARY KEY AUTOINCREMENT,
    Film_name TEXT NOT NULL,
    Film_descr TEXT,
    Film_time INTEGER NOT NULL
);
INSERT INTO Film (Film_name, Film_descr, Film_time)
VALUES
    ('Бесславные ублюдки', 'Хороший фильм, добрый, поучительный', 153);

CREATE TABLE Schedule (
    Schedule_ID  INTEGER PRIMARY KEY AUTOINCREMENT,
    date_time DATETIME NOT NULL,
    Film_ID    INTEGER NOT NULL,
    Cinema_ID    INTEGER NOT NULL,
    admin_ID     INTEGER NOT NULL,
    FOREIGN KEY (Cinema_ID) REFERENCES Cinema(Cinema_ID)
        ON UPDATE CASCADE
        ON DELETE CASCADE,
    FOREIGN KEY (admin_ID) REFERENCES Users(User_ID)
        ON UPDATE CASCADE
        ON DELETE RESTRICT
    FOREIGN KEY (Film_ID) REFERENCES Film(Film_ID)
        ON UPDATE CASCADE
        ON DELETE CASCADE
);
INSERT INTO Schedule (date_time, Film_ID, Cinema_ID, admin_ID)
VALUES
    ('2026-10-15 14:30:00', 1, 1, 2);
