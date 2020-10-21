from datetime import datetime, timedelta

def set_locations():

    locations = {
        
        'manhattan':'40.758896,-73.985130,4mi',
        'brooklyn': '40.650002,-73.949997,4mi',
        'detroit': '42.331429,-83.045753,4mi'

          }

    return locations


def set_word_list():

    words = [
        
        'trump',
        'covid-19',
        'biden'
        
        ]

    return words

def set_sentiment_list():

    sentiments = {

        'happy',
        'sad',
        'love',
        'anxiety'
    }

    return sentiments

def set_dates():

    deltas = {

        'today': datetime.today().strftime('%Y-%m-%d'),
        'yesterday': (datetime.today() - timedelta(days=1)).strftime('%Y-%m-%d'),
        'two_days_ago': (datetime.today() - timedelta(days=2)).strftime('%Y-%m-%d')
    }

    dates = [

        [deltas['yesterday'], deltas['today']],
        [deltas['two_days_ago'], deltas['yesterday']]
    ]

    return dates

def get_search_params():

    locations = set_locations()
    words = set_word_list()
    sentiments = set_sentiment_list()
    dates = set_dates()

    return locations, words, sentiments, dates