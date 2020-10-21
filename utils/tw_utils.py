from tweepy import API
from tweepy import Cursor
from tweepy import OAuthHandler
from tweepy import TweepError

import time
from datetime import datetime, date, timedelta

import config 

class Twitter_Credentials:

    def __init__(self):

        self.creds = config.twitter_credentials()

    def authenticate(self):

        auth = OAuthHandler(self.creds['consumer_key'], self.creds['consumer_secret_key'])
        auth.set_access_token(self.creds['access_token'], self.creds['access_secret_token'])

        return auth

class Twitter_cli:

    def __init__(self, twitter_user=None):

        self.auth = Twitter_Credentials().authenticate()
        self.client = API(self.auth)
        self.twitter_user = twitter_user

    def get_client_api(self):
        return self.client

    def check_twitter_user_exists(self, username):
        
        try:
            self.client.get_user(username)
            return True
        except Exception:
            return False

    def search(self, dates, num_tw, only_text=False, geocode=None, search_query=None):

        tweets = Cursor(self.client.search,
                        q=search_query,
                        tweet_mode='extended',
                        lang='en',
                        since=dates[0],
                        until=dates[1],
                        geocode=geocode,
                        include_retweets=True).items(num_tw)
        
        list_of_tweets = []

        if only_text:

            for tweet in tweets:

                tweet_dict = {

                    'text': tweet.full_text
                }
                
                list_of_tweets.append(tweet_dict)

        else:

            for tweet in tweets:

                tweet_dict = {

                    'tweet_id': tweet.id_str,
                    'time': tweet.created_at,
                    'text': tweet.full_text,
                    'retweet_count': tweet.retweet_count,
                    'user_screenname': tweet.author.screen_name,
                    'user_name': tweet.author.name,
                    'location': tweet.coordinates,
                    'source': tweet.source,
                    'is_retweet': tweet.retweeted
                }

                list_of_tweets.append(tweet_dict)

        for tweet in list_of_tweets:
            for k, v in tweet.items():

                if k == 'time':
                    v = v.strftime('%m/%d/%Y, %H:%M:%S')
                    tweet['time'] = v

        return list_of_tweets

    
    def sentiment_crawler(self, classes):

        senti_dict = {}

        for cl in classes:

            print(f'starting crawl: {cl}')

            tweets = []
            count = 0

            try:
                for tweet in Cursor(self.client.search,
                                    q=f'#{cl}',
                                    lang='en',
                                    since='2020-01-01',
                                    tweet_mode='extended',
                                    count=200).pages(200):

                    for t in tweet:

                        text = t.full_text.replace('&amp;', '&').replace(',','').replace('RT', '')
                        print(text)
                        tweets.append(text)
                        time.sleep(1e-3)
                        
                    print(count)
                    count += 1

                senti_dict[f'{cl}'] = tweets

            except TweepError as e:
                print(e)
                print(f'[i] raised on: {cl}')
                print('[i] waiting 15min...')
                time.sleep(900)
                print('[i] Waking back up...')
                for tweet in Cursor(self.client.search,
                                    q=f'#{cl}',
                                    lang='en',
                                    since='2020-01-01',
                                    tweet_mode='extended',
                                    count=10).pages(2):

                    for t in tweet:

                        text = t.full_text.replace('&amp;', '&').replace(',','').replace('RT', '')
                        print(text)
                        tweets.append(text)
                        time.sleep(1e-3)
                        
                    print(count)
                    count += 1

                senti_dict[f'{cl}'] = tweets


        return senti_dict

                    