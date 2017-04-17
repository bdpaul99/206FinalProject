## Your name: Brendan Paul
## The option you've chosen:
# Option 2

# Put import statements you expect to need here!
import unittest
import itertools
import collections
import tweepy
import requests
import twitter_info # same deal as always...
import json
import sqlite3

##### TWEEPY SETUP CODE:
# Authentication information should be in a twitter_info file...
consumer_key = twitter_info.consumer_key
consumer_secret = twitter_info.consumer_secret
access_token = twitter_info.access_token
access_token_secret = twitter_info.access_token_secret
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

# Set up library to grab stuff from twitter with your authentication, and return it in a JSON format 
api = tweepy.API(auth, parser=tweepy.parsers.JSONParser())

##### END TWEEPY SETUP CODE

## Define a class Movie:
## The constructor should accept a dictionary that represents a movie.
## It should have these instance variables: Movie title, director, its IMDB rating, a list of actors, the number of languages in the movie, and the highest paid actor
class Movie():
    def __init__(self,movie_dict):
        self.title = movie_dict['Title']
        self.director = movie_dict['Director']
        self.rating = movie_dict['imdbRating']
        self.actors = movie_dict['Actors']
        self.num_languages = len(movie_dict['Language'])
        self.highest_paid_actor = (self.actors.split(" ")[0] +  " " + self.actors.split(" ")[1])[:-1]

    def __str__(self):
        rstr = self.title + " Movie Data:"
        rstr += '\n' + "director: " + self.director
        rstr += '\n' + "imdb rating: " + self.rating
        rstr += '\n' + "actors: " + self.actors
        rstr += '\n' + "Number of Languages: " + str(self.num_languages)
        rstr += '\n' + "Highest Paid Actor " + self.highest_paid_actor
        return rstr
    def get_movie_tweets(self):
        if self.title in CACHE_DICTION:
            return CACHE_DICTION[self.title]
        else:
            return api.search(q = self.title)

    # Define your function get_director_tweets here:
    def get_director_tweets(self):
        if self.director in CACHE_DICTION:

            return CACHE_DICTION[self.director]
        else:
            resp = api.search_users(q = self.director)
            user_id = resp[0]['id']
            CACHE_DICTION[self.director] = api.user_timeline(user_id)
            print(self.director)
            print(user_id)
            return CACHE_DICTION[self.director]

    def get_highest_paid_actor_tweets(self):
        if self.highest_paid_actor in CACHE_DICTION:
            return CACHE_DICTION[self.highest_paid_actor]
        else:
            resp = api.search_users(q = self.highest_paid_actor)
            user_id = resp[0]['id']
            CACHE_DICTION[self.highest_paid_actor] = api.user_timeline(user_id)
            print(self.highest_paid_actor)
            print(user_id)
            return CACHE_DICTION[self.highest_paid_actor]

    def get_director(self):
        return self.director
    def get_actors(self):
        return self.actors
    def get_insert_tuple(self):
        return (self.title, self.director, self.rating, self.actors, self.num_languages, self.highest_paid_actor)


CACHE_FNAME = "SI206_final_project.json"
# Put the rest of your caching setup here:
try:
    cache_file = open(CACHE_FNAME,'r')
    cache_contents = cache_file.read()
    cache_file.close()
    CACHE_DICTION = json.loads(cache_contents)
except:
    CACHE_DICTION = {}

## write a function to get movie data from the omdb api
def get_omdb_data(movie_title):
    if movie_title in CACHE_DICTION:
        return CACHE_DICTION[movie_title]

    base_url = "http://www.omdbapi.com/?"
    param_dict = {"t":movie_title}
    response = requests.get(base_url, param_dict).json()

    CACHE_DICTION[movie_title] = response
    return response
## Create a list of three omdb search terms, and turn them into movie instances 
movie_list = ["Tropic Thunder", "Super Troopers", "Step Brothers"]

## create three movie instances
m1 = Movie(get_omdb_data(movie_list[0]))
m2 = Movie(get_omdb_data(movie_list[1]))
m3 = Movie(get_omdb_data(movie_list[2]))


## add the movie instances to a list named movie_instance_list
movie_instance_list = [m1, m2, m3]





# ## Create a class Tweet
class Tweet():
    def __init__(self,tweet_dict):
        self.content = tweet_dict['text']
        self.tweet_id = tweet['id_str']
        self.user_id = tweet['user']['id_str']
        self.time_posted = tweet['created_at']
        self.retweets = tweet['retweet_count']

    def get_insert_tuple(self):
        return (self.tweet_id, self.content, self.user_id, self.time_posted, self.retweets)





## call two twitter functions, and cache the data


## create a database file
conn = sqlite3.connect('final_project.db')
cur = conn.cursor()

## Add a tweets table, the tweets table should hold 
#       Tweet text
#       Tweet ID (primary key)
#       The user who posted the tweet (represented by a reference to the users table)
#       The movie search this tweet came from (represented by a reference to the movies table)
#       Number favorites
#       Number retweets
cur.execute('DROP TABLE IF EXISTS Tweets')
cur.execute('CREATE TABLE Tweets(tweet_id TEXT PRIMARY KEY, text TEXT, user_id TEXT, time_posted TIMESTAMP, retweets INTEGER)')
statement = 'INSERT INTO Tweets VALUES (?, ?, ?, ?, ?)'


for tweet in m1.get_director_tweets():
    t = Tweet(tweet)
    cur.execute(statement, t.get_insert_tuple())

for tweet in m2.get_director_tweets():
    t = Tweet(tweet)
    cur.execute(statement,t.get_insert_tuple())
## Add a Users table, the Users table should hold:
#       User ID (primary key)
#       User screen name
#       Number of favorites that user has ever made
#       The users in the neighborhood of that u
cur.execute('DROP TABLE IF EXISTS Users')
cur.execute('CREATE TABLE Users(user_id TEXT PRIMARY KEY, screen_name TEXT, num_favs INTEGER, description TEXT, neighborhood TEXT)')

## Add a Movies table, the Movies table should hold:
#       ID (primary key) 
#       Title of the movie
#       Director of the movie 
#       Number of languages the movie has
#       IMDB rating of the movie
#       The top billed (first in the list) actor in the movie
#       Tweets about the Movie
cur.execute('DROP TABLE IF EXISTS MOVIES')
cur.execute('CREATE TABLE Movies(ID  INTEGER PRIMARY KEY, title TEXT,  director TEXT, rating REAL, actors TEXT, num_languages INTEGER,  top_billed_actor TEXT)')
statement = 'INSERT INTO Movies VALUES (?, ?, ?, ?, ?, ?, ?)'
i = 1
for movie in movie_instance_list:
    t = movie.get_insert_tuple()
    print(t)
    cur.execute(statement, (i, t[0],t[1],t[2],t[3],t[4],t[5]))
    i+=1
    conn.commit()
## Load all of the items into the database





w = open(CACHE_FNAME, 'w')
w.write(json.dumps(CACHE_DICTION))
w.close()

# Write your test cases here.


## Remember to invoke all your tests...
class PartOne(unittest.TestCase):
    def test1(self):
        movie1 = Movie(get_omdb_data("Super Troopers"))
        tweets = movie1.get_director_tweets()
        assert(len(tweets) >= 10)
    
    def test2(self):
        movie1 = Movie(get_omdb_data("Super Troopers"))
        tweets = movie1.get_director_tweets()
        assert(type(tweets) == type([]))

    def test3(self):
        movie1 = Movie(get_omdb_data("Super Troopers"))
        tweets = movie1.get_director_tweets()

        assert(type(tweets[0])) == type({})
    def test4(self):
        movie1 = Movie(get_omdb_data("Super Troopers"))
        assert(type(movie1.__str__()) == type(""))
    def test5(self):
        movie1 = Movie(get_omdb_data("Super Troopers"))
        assert(type(movie1.get_director()) == type(""))
    def test6(self):
        movie1 = Movie(get_omdb_data("Super Troopers"))
        assert(type(movie1.get_actors()) == type(""))
    def test7(self):
        movie1 = Movie(get_omdb_data("Django Unchained"))
        assert(movie1.get_director() == "Quentin Tarantino")
    def test8(self):
        conn = sqlite3.connect('final_project.db')
        cur = conn.cursor()
        cur.execute('SELECT * FROM Tweets');
        result = cur.fetchall()
        self.assertTrue(len(result)>10)


if __name__ == "__main__":
    unittest.main(verbosity=2)
