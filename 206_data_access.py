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

########################################################   Beginning of class movie ########################################################
class Movie():
    def __init__(self,movie_dict):
        self.title = movie_dict['Title']
        self.director = movie_dict['Director']
        self.rating = movie_dict['imdbRating']
        self.actors = movie_dict['Actors']
        self.num_languages = len(movie_dict['Language'])
        self.highest_paid_actor = (self.actors.split(" ")[0] +  " " + self.actors.split(" ")[1])[:-1]
        self.genre = movie_dict['Genre'].split(",")[0]

    def __str__(self):
        rstr = self.title + " Movie Data:"
        rstr += '\n' + "director: " + self.director
        rstr += '\n' + "imdb rating: " + self.rating
        rstr += '\n' + "actors: " + self.actors
        rstr += '\n' + "Number of Languages: " + str(self.num_languages)
        rstr += '\n' + "Highest Paid Actor " + self.highest_paid_actor
        rstr += '\n' + "Genre" + self.genre
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
            return CACHE_DICTION[self.director]

    def get_highest_paid_actor_tweets(self):
        if self.highest_paid_actor in CACHE_DICTION:
            return CACHE_DICTION[self.highest_paid_actor]
        else:
            resp = api.search_users(q = self.highest_paid_actor)
            user_id = resp[0]['id']
            CACHE_DICTION[self.highest_paid_actor] = api.user_timeline(user_id)
            return CACHE_DICTION[self.highest_paid_actor]

    def get_director_user_data(self):
        if self.director in CACHE_DICTION['director_data']:
            return CACHE_DICTION[director_data][self.director]
        else:
            resp = api.search_users(q = self.director)
            user_id = resp[0]['id']
            CACHE_DICTION['director_data'][self.director] = api.get_user(user_id)
            return CACHE_DICTION['director_data'][self.director]
    def get_highest_paid_actor_data(self):
        if self.highest_paid_actor in CACHE_DICTION['actors_data']:
            return CACHE_DICTION['actors_data'][self.highest_paid_actor]
        else:
            resp = api.search_users(q = self.highest_paid_actor)
            user_id = resp[0]['id']
            CACHE_DICTION['actors_data'][self.highest_paid_actor] = api.get_user(user_id)
            return CACHE_DICTION['actors_data'][self.highest_paid_actor]

    def get_highest_paid_actor(self):
        return self.highest_paid_actor
    def get_director(self):
        return self.director
    def get_actors(self):
        return self.actors
    def get_insert_tuple(self):
        return (self.title, self.director, self.rating, self.actors, self.num_languages, self.highest_paid_actor,self.genre)



########################################################   End of class Movie ########################################################


############################################################ Create a class Tweet ########################################################
class Tweet():
    def __init__(self,tweet_dict):
        self.content = tweet_dict['text']
        self.tweet_id = tweet['id_str']
        self.user_id = tweet['user']['id_str']
        self.time_posted = tweet['created_at']
        self.retweets = tweet['retweet_count']

    def get_insert_tuple(self):
        return (self.tweet_id, self.content, self.user_id, self.time_posted, self.retweets)

        
 ########################################################   End of class Tweet ########################################################

 ########################################################   Beginning of Helper Functions ########################################################
 
def get_user_neighborhood(tweet_dict):
        user_names = []
        user_mentions = [tweet['entities']['user_mentions'] for tweet in tweet_dict]
        for each in user_mentions:
            for mention in each:
             if mention['screen_name'] not in user_names:
                user_names.append(mention['screen_name'])
        return user_names


## write a function to get movie data from the omdb api
def get_omdb_data(movie_title):
    if movie_title in CACHE_DICTION:
        return CACHE_DICTION[movie_title]

    base_url = "http://www.omdbapi.com/?"
    param_dict = {"t":movie_title}
    response = requests.get(base_url, param_dict).json()

    CACHE_DICTION[movie_title] = response
    return response

########################################################   End of Helper Functions ########################################################
########################################################  Beginning of Cache Pattern ########################################################
CACHE_FNAME = "SI206_final_project.json"
# Put the rest of your caching setup here:
try:
    cache_file = open(CACHE_FNAME,'r')
    cache_contents = cache_file.read()
    cache_file.close()
    CACHE_DICTION = json.loads(cache_contents)
except:
    CACHE_DICTION = {}

########################################################   End of Cache Pattern ########################################################
    

## Create a list of three omdb search terms, and turn them into movie instances 
movie_list = ["Tropic Thunder", "Super Troopers", "Step Brothers", "Fight Club", "Avatar"]

## create three movie instances



## add the movie instances to a list named movie_instance_list
movie_instance_list = [ Movie(get_omdb_data(m)) for m in movie_list ]









##  use your function to access data about a Twitter user to get information about each of the Users in the "neighborhood"
directors = [m.get_director() for m in movie_instance_list]

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

for m in movie_instance_list:
    for tweet in m.get_highest_paid_actor_tweets():
        t = Tweet(tweet)
        cur.execute(statement, t.get_insert_tuple())
    for tweet in m.get_director_tweets():
        t = Tweet(tweet)
        cur.execute(statement, t.get_insert_tuple())


## Add a Users table, the Users table should hold:
#       User ID (primary key)
#       User screen name
#       Number of favorites that user has ever made

cur.execute('DROP TABLE IF EXISTS Users')
cur.execute('CREATE TABLE Users(user_id TEXT PRIMARY KEY, screen_name TEXT, num_favs INTEGER, description TEXT, role TEXT)')
statement = statement = 'INSERT INTO Users Values (?, ?, ?, ?, ?)'
try:
    director_data = CACHE_DICTION['director_data']
    for director in director_data:
        cur.execute(statement, (director[user_id], director[screen_name], director[num_favs], director[description], "Director"))
except:
    CACHE_DICTION['director_data'] = {}
    for m in movie_instance_list:
        data = m.get_director_user_data()
        CACHE_DICTION['director_data'][m.get_director()] = data
        cur.execute(statement, (data['id'],data['screen_name'],data['favourites_count'],data['description'], "Director"))

## Add Actors to the Users table
try:
    actors_data = CACHE_DICTION['actors_data']
    for actor in actors_data:
        cur.execute(statement, (actor[user_id], actor[screen_name], actor[num_favs], actor[description], "Actor"))
except:
    CACHE_DICTION['actors_data'] = {}
    for m in movie_instance_list:
        data = m.get_highest_paid_actor_data()
        CACHE_DICTION['actors_data'][m.get_highest_paid_actor()] = data
        cur.execute(statement, (data['id'],data['screen_name'],data['favourites_count'],data['description'], "Actor"))
# 

conn.commit()
## Add a Movies table, the Movies table should hold:
#       ID (primary key) 
#       Title of the movie
#       Director of the movie 
#       Number of languages the movie has
#       IMDB rating of the movie
#       The top billed (first in the list) actor in the movie
#       Tweets about the Movie
cur.execute('DROP TABLE IF EXISTS MOVIES')
cur.execute('CREATE TABLE Movies(ID  INTEGER PRIMARY KEY, title TEXT,  director TEXT, rating REAL, actors TEXT, num_languages INTEGER,  top_billed_actor TEXT, genre TEXT)')
statement = 'INSERT INTO Movies VALUES (?, ?, ?, ?, ?, ?, ?,?)'
i = 1
for movie in movie_instance_list:
    t = movie.get_insert_tuple()
    print(t)
    cur.execute(statement, (i, t[0],t[1],t[2],t[3],t[4],t[5], t[6]))
    i+=1
    conn.commit()
## Load all of the items into the database


# use queries to find most common words in that appear in the tweets

# use queries to find the actor with the most favorites on twitter in the movies

# use queries to find the actor with the most retweets in the movies

# use queries to find the director with the most favorites in the movies

## write data to a text file -- a sort of "summary stats" page with a clear title about the movies




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
