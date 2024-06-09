PRAGMA foreign_keys = OFF;

DROP TABLE IF EXISTS pages;

DROP TABLE IF EXISTS videos;

DROP TABLE IF EXISTS video_insights;

PRAGMA foreign_keys = ON;

CREATE TABLE pages (
    id INTEGER PRIMARY KEY NOT NULL,
    name TEXT NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE videos (
    id INTEGER PRIMARY KEY NOT NULL,
    page_id INTEGER NOT NULL,
    title TEXT NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (page_id)
    REFERENCES pages (id)
    ON UPDATE CASCADE
    ON DELETE CASCADE
);

CREATE TABLE video_insights (
    id INTEGER PRIMARY KEY NOT NULL,
    video_id INTEGER NOT NULL,
    likes INTEGER NOT NULL DEFAULT 0,
    views INTEGER NOT NULL DEFAULT 0,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (video_id)
    REFERENCES videos (id)
    ON UPDATE CASCADE
    ON DELETE CASCADE
);