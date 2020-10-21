
import time
import pandas as pd

from utils import tw_utils as tw
from utils import sql_utils as sql
from utils import search_params as search 

from tweepy import TweepError




class Pipeline:

    def __init__(self, db):

        self.db = db
        self.queries = sql.read_sql('./queries/query_commands.sql')

    def set_database(self):

        SQL = sql.SQL_Cli(self.db)
        try:

            SQL.execute(self.queries[1])
            SQL.execute(self.queries[2])

            return print('[+] Tables Set')

        except:
            return print('[+] Tables Already Set')
          

    def pipe(self, tweet_data, sentiment_data):

        SQL = sql.SQL_Cli(self.db)
        
        for i, data in tweet_data.iterrows():
            print(data)
            values = (
                
                data['tweet_id'], data['time'],
                data['text'], data['retweet_count'],
                data['user_screenname'], data['user_name'], data['source'],
                data['is_retweet'], data['retrieved'],
                data['city'], data['word_searched']

                 )   
            SQL.insert(self.queries[3].format(values))
            print('[i] Inserted')

        for i, data in sentiment_data.iterrows():
            print(data)
            values = (

                data['text'], data['label']
               
                )
            SQL.insert(self.queries[4].format(values))
            print('[i] Inserted')

        return print('[+] Data Inserted')

    def retrieve(self, query):

        SQL = sql.SQL_Cli(self.db)
        res = SQL.fetch(query)

        return res


class Data_Collect:

    def __init__(self):

        self.locations, self.words, self.sentiments, self.dates = search.get_search_params()

    def fetch_twitter_data(self):

        date_search, location_search, word_search = {}, {}, {}

        for date in self.dates:
            print('\n')
            print(f'[+] retrieving between dates: {date[0]} and {date[1]}')

            for location, geocode in self.locations.items():
                print('\n')
                print(f'[+] retrieving from: {location}')
                print(f'{geocode}')

                for word in self.words:
                    print('\n')
                    print(f'[+] using search: {word}')

                    try:

                       tweets = tw.Twitter_cli().search(date, 200, geocode=geocode, search_query=word)

                       print(f'[i] {len(tweets)} found for {word}')
                    
                    except TweepError as e:
                        print(f'[i] {e}')
                        print(f' at {date} / {location} / {word}')
                        print('[i] Waiting for 15 min....')
                        time.sleep(900)
                        print('[i] waking back up...')
                        tweets = tw.Twitter_cli().search(date, 200, geocode=geocode, search_query=word)


                    word_search[word] =  tweets
                    print(f'[+] {word} key set')
                    print('\n')
                location_search[location] =  word_search
                print(f'[+] {location} key set')
                print('\n')
            date_search[date[0]] = location_search
            print(f'[+] {date[0]} key set')

        return date_search

    def fetch_sentiment_data(self):

        senti_dict = tw.Twitter_cli().sentiment_crawler(self.sentiments)

        return senti_dict

def prep_senti_data():

    sentiment_data = Data_Collect().fetch_sentiment_data()

    list_df = []
    for k, v in sentiment_data.items():
        for n in range(len(list(sentiment_data.keys()))):
            if k == list(sentiment_data.keys())[n]:
                df = pd.DataFrame(v, columns=['text'])
                df['label'] = list(sentiment_data.keys())[n]
                list_df.append(df)
    df = pd.concat(list_df)

    return df

def prep_twitter_data():

    twitter_data = Data_Collect().fetch_twitter_data()

    list_df = []

    for date, v in twitter_data.items():
        for num in range(len(list(twitter_data.keys()))):
            if date == list(twitter_data.keys())[num]:

                for city, word_list in v.items():
                    for n in range(len(list(v.keys()))):
                        if city == list(v.keys())[n]:

                            for word, tweets in word_list.items():
                                for x in range(len(word_list.keys())):
                                    if word == list(word_list.keys())[x]:

                                        df = pd.DataFrame(tweets)
                                        df['retrieved'] = date
                                        df['city'] = city
                                        df['word_searched'] = word
                                        list_df.append(df)
    df = pd.concat(list_df)

    return df


def run_pipeline():

    p = Pipeline('Twitter_Data')
    p.set_database()

    senti_data = prep_senti_data()
    twitter_data = prep_twitter_data()

    p.pipe(twitter_data, senti_data)

    return None


if __name__ == '__main__':

    run_pipeline()




