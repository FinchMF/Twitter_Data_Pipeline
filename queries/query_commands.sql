

CREATE DATABASE IF NOT EXISTS Twitter_Data
;

CREATE TABLE Tweets (

    tweet_id VARCHAR(100),
    created_at VARCHAR(30) NOT NULL,
    tweets VARCHAR (500),
    retweet_count INT,
    user_screenname VARCHAR(100),
    author_name VARCHAR(100),
    source VARCHAR(50),
    is_retweet BOOLEAN,
    hashtags VARCHAR(100),
    retrieved VARCHAR(30),
    word_search VARCHAR(15),
    city VARCHAR(15)

)
;

CREATE TABLE Sentiment (

    tweets VARCHAR(2000),
    sentiment VARCHAR(100)

)
;

INSERT INTO Tweets (

    tweet_id,
    created_at,
    tweets,
    retweet_count,
    user_screenname,
    author_name,
    source,
    is_retweet,
    retrieved,
    word_search,
    city
)

VALUES {}

;

INSERT INTO Sentiment (

    tweets,
    sentiment

)

VALUES {}

;
