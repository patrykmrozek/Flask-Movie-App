DROP TABLE IF EXISTS users;

CREATE TABLE users
(
    user_id TEXT PRIMARY KEY,
    password TEXT NOT NULL,
    is_admin INTEGER NOT NULL,
    pfp TEXT NOT NULL
);

INSERT INTO users (user_id, password, is_admin, pfp)
VALUES
    ("admin", "scrypt:32768:8:1$c7CQiVvKMTdptTyq$b5f5babc913b5981ff6298138c5e763c831d9d4139736112f5fe8931aa96ea25842e200d1878564ebbd24ad98df74b5ead59120fe792ede9d8a2f10db57e2ed6", 1, "pfp1.png");


DROP TABLE IF EXISTS movies;

CREATE TABLE movies
(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    year INTEGER NOT NULL,
    score REAL,
    director TEXT,
    poster TEXT,
    description TEXT
);


INSERT INTO movies (title, year, score, director, poster, description)
VALUES
    ("The Shawshank Redemption", 1994, 9.3, "Frank Darabont", "posters/shawshank-poster.png", "Framed in the 1940s for the double murder of his wife and her lover, 
    upstanding banker Andy Dufresne begins a new life at the Shawshank prison, where he puts his accounting skills to work for an amoral warden. 
    During his long stretch in prison, Dufresne comes to be admired by the other inmates for his integrity and unquenchable sense of hope."),

    ("The Godfather", 1972, 9.2, "Francis Ford Coppola", "posters/godfather-poster.png", "Spanning the years 1945 to 1955, a chronicle of the fictional Italian-American
    Corleone crime family. When organized crime family patriarch, Vito Corleone barely survives an attempt on his life, his youngest son, Michael steps in to
    take care of the would-be killers, launching a campaign of bloody revenge."),

    ("The Dark Knight", 2008, 9.0, "Christopher Nolan", "posters/batman-poster.png", "Batman raises the stakes in his war on crime. With the help of Lt. Jim Gordon and
    District Attorney Harvey Dent, Batman sets out to dismantle the remaining criminal organizations that plague the streets. The partnership proves to be effective,
    but they soon find themselves prey to a reign of chaos unleashed by a rising criminal mastermind known to the terrified citizens of Gotham as the Joker."),

    ("Pulp Fiction", 1994, 8.9, "Quentin Tarantino", "posters/pulpfiction-poster.png", "A burger-loving hit man, his philosophical partner, a drug-addled gangster’s moll and a
    washed-up boxer converge in this sprawling, comedic crime caper. Their adventures unfurl in three stories that ingeniously trip back and forth in time."),

    ("Schindler's List", 1993, 8.9, "Steven Spielberg", "posters/schindlers-poster.png", "The true story of how businessman Oskar Schindler saved over a thousand Jewish lives from the
    Nazis while they worked as slaves in his factory during World War II."),

    ("Forrest Gump", 1994, 8.8, "Robert Zemeckis", "posters/gump-poster.png", "A man with a low IQ has accomplished great things in his life and been present during significant
    historic events—in each case, far exceeding what anyone imagined he could do. But despite all he has achieved, his one true love eludes him."),

    ("The Matrix", 1999, 8.7, "The Wachowskis", "posters/matrix-poster.png", "Set in the 22nd century, The Matrix tells the story of a computer hacker who joins a group of underground
    insurgents fighting the vast and powerful computers who now rule the earth."),

    ("The Lord of the Rings: The Return of the King", 2003, 8.9, "Peter Jackson", "posters/lotr-poster.png", "Aragorn is revealed as the heir to the ancient kings as he,
    Gandalf and the other members of the broken fellowship struggle to save Gondor from Sauron’s forces. Meanwhile, Frodo and Sam take the ring closer to the heart
    of Mordor, the dark lord’s realm."),

    ("Inception", 2010, 8.8, "Christopher Nolan", "posters/inception-poster.png", "Cobb, a skilled thief who commits corporate espionage by infiltrating the subconscious of his
    targets is offered a chance to regain his old life as payment for a task considered to be impossible: “inception”, the implantation of another person’s idea into a
    target’s subconscious."),

    ("The Silence of the Lambs", 1991, 8.6, "Jonathan Demme", "posters/lamb-poster.png", "Clarice Starling is a top student at the FBI’s training academy. Jack Crawford wants
    Clarice to interview Dr. Hannibal Lecter, a brilliant psychiatrist who is also a violent psychopath, serving life behind bars for various acts of murder and cannibalism.");



DROP TABLE IF EXISTS movie_ratings;


CREATE TABLE movie_ratings
(
    rating_id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    movie_id INTEGER NOT NULL,
    user_rating INTEGER NOT NULL
);



DROP TABLE IF EXISTS movie_reviews;


CREATE TABLE movie_reviews
(   
    review_id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    movie_id INTEGER NOT NULL,
    user_review TEXT 
);


DROP TABLE IF EXISTS user_favourites;

CREATE TABLE user_favourites
(   
    user_id INTEGER NOT NULL,
    movie_id INTEGER NOT NULL
);