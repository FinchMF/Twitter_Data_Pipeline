# Twitter_Data_Pipeline

## PIPELINE FILE STRUCTURE
    .
    ├── README.md
    ├── __pycache__
    │   ├── config.cpython-37.pyc
    │   ├── pipline.cpython-37.pyc
    │   └── sql_params.cpython-37.pyc
    ├── bash
    │   ├── end_sql.sh
    │   └── start_sql.sh
    ├── config.py
    ├── execute.sh
    ├── pipline.py
    ├── queries
    │   └── query_commands.sql
    ├── requirements.txt
    ├── sql_params.py
    └── utils
        ├── __init__.py
        ├── __pycache__
        │   ├── __init__.cpython-37.pyc
        │   ├── search_params.cpython-37.pyc
        │   ├── sql_utils.cpython-37.pyc
        │   └── tw_utils.cpython-37.pyc
        ├── search_params.py
        ├── sql_utils.py
        └── tw_utils.py

Note that in this repo, there are two files excluded:

* config.py
* sql_params.py

<br/><br/>
## PIPELINE STRUCTURE

* Access MySQL Server
* Creates Database and Tables
* Makes requests to Twitter API
* Ingests requests results to into respective table


        - MySQL
            - Start Server
                 - Creates Database
                    - Creates Two tables: Tweets and Sentiment
        |
        |
        |
        - Request Twitter API
            - Search One: query API by Date, Keyword and Location
            - Search Two: query API by Hashtag
        |
        |
        |
        - Ingest 
            - Search One into Tweets table
            - Search Two into Sentiment table
        |
        |
        |
        - MySQL
            - Stop Server

<br/><br/>
## API REQUEST DETAIL

### Credentials
In order to make requests to Twitter's API, we use Tweepy. To allow the pipeline to work seamlessly, in the top directory create a config.py file with the following structure:

    def twitter_credentials():

        creds = {

            'consumer_key': <your consumer_key>,
            'consumer_secret_key': <your consumer_secret_key>,
            'access_token': <your access_token>,
            'access_secret_token': <your access_secret_token>
            
                }

        return creds

If you already have API keys from Twitter, then place them here. If you do not already have API keys from Twitter. Head to your developers account and make the request. 

[link to Twitter API Key Tutorial](https://developer.twitter.com/en/docs/authentication/oauth-1-0a/obtaining-user-access-tokens)

<br/><br/>
### What Data is Retrieved

The data ingested into the Tweets tables are Tweet gathered by:
* Date 
* Location
* Keyword

To review the Date, Location and Keyword search parameters, look at:
* search_params.py

<br/><br/>

The data model per row in Tweets table is:

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


<br/><br/>
The data ingested into the Sentiment table is gathered by searching for tweets with emotions as hashtags. 

<br/><br/>
The data model per row in Sentiments table is:

    tweets VARCHAR(2000),
    sentiment VARCHAR(100)

<br/><br/>

## SQL DETAILS
### Credentials
In order to create the SQL database and table, in the top directory, create sql_params.py with the following file structure:

    def sql_credentials():

        creds = {

            'user': <your user name>,
            'password': <your password>

            }

        return creds

<br/><br/>
## HOW TO USE PIPELINE

    git clone https://github.com/FinchMF/Twitter_Data_Pipeline.git

    pip install -r requirements.txt

    $ bash execute.sh