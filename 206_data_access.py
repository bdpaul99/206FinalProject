## Your name: Brendan Paul
## The option you've chosen:
# Option 2

# Put import statements you expect to need here!
import unittest
import itertools
import re
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
        self.actors = (movie_dict['Actors'])
        self.num_languages = len(movie_dict['Language'])
        self.highest_paid_actor = (self.actors.split(" ")[0] +  " " + self.actors.split(" ")[1])[:-1]
        self.genre = movie_dict['Genre'].split(",")[0]

    def __str__(self):
        rstr = self.title + " Movie Data:"
        rstr += "\ndirector: " + self.director
        rstr += "\nimdb rating: " + self.rating
        rstr += "\nactors: " + self.actors
        rstr += "\nNumber of Languages: " + str(self.num_languages)
        rstr += "\nHighest Paid Actor: " + self.highest_paid_actor
        rstr += "\nGenre: " + self.genre + "\n\n"
        return rstr
    
    def get_movie_tweets(self):
        if (self.title + "_tweets") in CACHE_DICTION:
            return CACHE_DICTION[(self.title + "_tweets")]
        else:
            CACHE_DICTION[(self.title + "_tweets")] = api.search(q = self.title)
            return CACHE_DICTION[(self.title + "_tweets")]

    # Define your function get_director_tweets here:
    def get_director_tweets(self):
        director_string = self.director + "_tweets"
        if director_string  in CACHE_DICTION:

            return CACHE_DICTION[director_string]
        else:
            resp = api.search_users(q = self.director)
            user_id = resp[0]['id']
            CACHE_DICTION[director_string] = api.user_timeline(user_id)
            return CACHE_DICTION[director_string]

    def get_highest_paid_actor_tweets(self):
        actor_string = self.highest_paid_actor + "_tweets"

        if actor_string in CACHE_DICTION:
            return CACHE_DICTION[actor_string]
        else:
            resp = api.search_users(q = self.highest_paid_actor)
            user_id = resp[0]['id']
            CACHE_DICTION[actor_string] = api.user_timeline(user_id)
            return CACHE_DICTION[actor_string]

    def get_director_user_data(self):
        if self.director in CACHE_DICTION:
            return CACHE_DICTION[self.director]
        else:
            resp = api.search_users(q = self.director)
            user_id = resp[0]['id']

            CACHE_DICTION[self.director] = api.get_user(user_id)
            return CACHE_DICTION[self.director]
    def get_highest_paid_actor_data(self):
        if self.highest_paid_actor in CACHE_DICTION:
            return CACHE_DICTION[self.highest_paid_actor]
        else:
            resp = api.search_users(q = self.highest_paid_actor)
            user_id = resp[0]['id']
            CACHE_DICTION[self.highest_paid_actor] = api.get_user(user_id)
            return CACHE_DICTION[self.highest_paid_actor]

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
        self.tweet_id = tweet_dict['id_str']
        self.user_id = tweet_dict['user']['id_str']
        self.time_posted = tweet_dict['created_at']
        self.retweets = tweet_dict['retweet_count']
        self.favorites = tweet_dict['favorite_count']

    def get_insert_tuple(self):
        return (self.tweet_id, self.content, self.user_id, self.time_posted, self.retweets, self.favorites)

        
 ########################################################   End of class Tweet ########################################################

 ########################################################   Beginning of Helper Functions ########################################################
 ## write a function to get the neighborhood of a user
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

## write a function to get data about a user based on a screen_name
def get_user_data(screen_name):
        if screen_name in CACHE_DICTION:
            return CACHE_DICTION[screen_name]
        else:
            
            CACHE_DICTION[screen_name] = api.get_user(screen_name)
            return CACHE_DICTION[screen_name]

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
movie_list = ["Super Troopers", "Fury", "Step Brothers", "Fight Club", "Avatar", "The Usual Suspects"]



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
cur.execute('CREATE TABLE Tweets(tweet_id TEXT PRIMARY KEY, text TEXT, user_id TEXT, time_posted TIMESTAMP, retweets INTEGER, favorite_count INTEGER)')
statement = 'INSERT INTO Tweets VALUES (?, ?, ?, ?, ?, ?)'

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
cur.execute('CREATE TABLE Users(user_id TEXT PRIMARY KEY, real_name TEXT, screen_name TEXT, num_favs INTEGER, description TEXT, role TEXT)')
statement = statement = 'INSERT INTO Users Values (?, ?, ?, ?, ?, ?)'

for m in movie_instance_list:
    data = m.get_director_user_data()
    cur.execute(statement, (data['id'], m.get_director(), data['screen_name'],data['favourites_count'],data['description'], "Director"))


for m in movie_instance_list:
    data = m.get_highest_paid_actor_data()
    cur.execute(statement, (data['id'], m.get_highest_paid_actor() ,data['screen_name'],data['favourites_count'],data['description'], "Actor"))

## Add all the users in the Actors and Directors neighborhoods to the userts table
cur.execute('SELECT screen_name FROM Users')
screen_names = [name[0] for name in cur.fetchall()]

for movie in movie_instance_list:
    direct_tweets = movie.get_director_tweets()
    actor_tweets = movie.get_highest_paid_actor_tweets()
    direct_neighbors = get_user_neighborhood(direct_tweets)
    actor_neighbors = get_user_neighborhood(actor_tweets)
    all_neighbors = direct_neighbors + actor_neighbors
    for neighbor in all_neighbors:
        if neighbor not in screen_names:
            try:
                data = get_user_data(neighbor)
                screen_names.append(neighbor)
                cur.execute(statement, (data['id'], data['name'] ,data['screen_name'],data['favourites_count'],data['description'], "Neighbor"))
            except:
                print("User", neighbor, "could not be added, has been suspended on twitter")
    

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
    
    cur.execute(statement, (i, t[0],t[1],t[2],t[3],t[4],t[5], t[6]))
    i+=1
    conn.commit()


################################################################################
## Sort the actors tweets by how many retweets they recieved
cur.execute('SELECT Users.real_name, Tweets.text, Tweets.retweets FROM Users INNER JOIN Tweets ON Users.user_id = Tweets.user_id WHERE Users.role= "Actor"')
actor_tweet_tuples = cur.fetchall()

sorted_actor_tweet_tuples = sorted(actor_tweet_tuples, key = lambda x: x[2], reverse = True)

lame_actor_tweets = list(filter(lambda x: x[2] < 10 ,actor_tweet_tuples))



###########################################################################
## Find out which movies director got the most retweets overall
cur.execute('SELECT Movies.title, Tweets.retweets FROM Users INNER JOIN Tweets INNER JOIN Movies ON Users.user_id = Tweets.user_id AND Movies.director = Users.real_name')
movies_retweets_tuple = cur.fetchall()
c = collections.Counter()
for t in movies_retweets_tuple:
    c.update({t[0]: t[1]})

#####################################################################
## Create a Dictionary with Hastags as the keys (using collections container and regular expressions) and the number of times they occur as the value
cur.execute('SELECT Tweets.text FROM Tweets')
tweets_list = list(cur.fetchall())
tweets_list = [tweet[0] for tweet in tweets_list]
c2 = collections.Counter()
for tweet in tweets_list:
    hashtags_list = re.findall(r'(?:(?<=\s)|^)#(\w*[A-Za-z_]+\w*)', tweet)
    
    for tag in hashtags_list:
        c2[tag] += 1

#######################################################################
## write data to a text file -- a sort of "summary stats" page with a clear title about the movies
w = open(CACHE_FNAME, 'w')
w.write(json.dumps(CACHE_DICTION))
w.close()

out = open('outfile.txt', 'w', encoding = "utf-8")
out.write("SI 206 FINAL PROJECT: TWEEPY x OMDB\n\n")
out.write("Here are the six movies I collected data on: "+ "Super Troopers, "+ "Fury, "+ "Step Brothers, "+ "Fight Club, "+ "Avatar, "+ " and The Usual Suspects\n\n")
for movie in movie_instance_list:
    
    out.write(movie.__str__())
out.write("\nHeres the most retweeted Actor tweet that I found:\n")
out.write(sorted_actor_tweet_tuples[0][0] +  ": " + sorted_actor_tweet_tuples[0][1])
out.write("\nThis tweet got " + str(sorted_actor_tweet_tuples[0][2]) + " retweets")
out.write("\nNot all actor tweets were this poular though...there were " + str(len(lame_actor_tweets)) + " Actor tweets with less than ten retweets!")

out.write("\n\nEach of these movies has active directors on Twitter... Heres the count of retweets each Movie's director had for the tweets I collected:")
for t in c.items():
    out.write("\n" + t[0] + ": " + str(t[1]))

out.write("\n\nTotal Count for each Hashtag that appeared in the Tweets")
for each in c2.items():
    out.write("\n#" + each[0] + ": " + str(each[1]))
# Write your test cases here.


## Remember to invoke all your tests...
class PartOne(unittest.TestCase):
    def test_ctor_1(self):
        movie1 = Movie(get_omdb_data("Super Troopers"))
        assert(movie1.title == "Super Troopers")
    
    def test_ctor_2(self):
        movie1 = Movie(get_omdb_data("Fury"))
        assert(movie1.get_director() == "David Ayer")

    def test_str_1(self):
        movie1 = Movie(get_omdb_data("Super Troopers"))
        assert(type(movie1.__str__()) == type(""))
    
    def test_str_2(self):
        movie = Movie(get_omdb_data("Fury"))
        assert("Fury" in movie.__str__())
    
    def test_get_movie_tweets_1(self):
        movie = Movie(get_omdb_data("Fury"))
        assert(type(movie.get_movie_tweets()["statuses"]) == list)
    
    def test_get_movie_tweets_2(self):
        movie = Movie(get_omdb_data("Fury"))
        assert(type({}) == type(movie.get_movie_tweets()))
    
    def test_get_director_tweets_1(self):
        movie1 = Movie(get_omdb_data("Super Troopers"))
        tweets = movie1.get_director_tweets()
        assert(type(tweets) == type([]))
    
    def test_get_director_tweets_2(self):
        movie1 = Movie(get_omdb_data("Super Troopers"))
        tweets = movie1.get_director_tweets()
        assert(type(tweets[0])) == type({})
    
    def test_get_highest_paid_actor_tweets_1(self):
        movie = Movie(get_omdb_data("Fury"))
        assert(type([]) == type(movie.get_highest_paid_actor_tweets()))
    
    def test_get_highest_paid_actor_tweets_2(self):
        movie = Movie(get_omdb_data("Fury"))
        assert("id" in movie.get_highest_paid_actor_tweets()[0])
    
    def test_get_director_user_data_1(self):
        movie = Movie(get_omdb_data("Tropic Thunder"))
        data = movie.get_director_user_data()
        assert('favourites_count' in data.keys())
    
    def test_get_director_user_data_2(self):
        movie = Movie(get_omdb_data("Avatar"))
        data = movie.get_director_user_data()
        assert(data['screen_name'] == "JimCameron")
    
    def test_get_highest_paid_actor_data_1(self):
        movie = Movie(get_omdb_data("Fury"))
        data = movie.get_highest_paid_actor_data()
        assert(data['id'] == 2240466994)
    
    def test_get_highest_paid_actor_data_2(self):
        movie = Movie(get_omdb_data("Fury"))
        data = movie.get_highest_paid_actor_data()
        assert(data['favourites_count'] == 136)
    
    def test_get_highest_paid_actor_1(self):
        movie = Movie(get_omdb_data("Fury"))
        assert("Brad Pitt" == movie.get_highest_paid_actor())
    
    def test_get_highest_paid_actor_2(self):
        movie = Movie(get_omdb_data("The Usual Suspects"))
        assert(type(movie.get_highest_paid_actor()) == type(""))
    
    def test_get_director_1(self):
        movie1 = Movie(get_omdb_data("Super Troopers"))
        assert(type(movie1.get_director()) == type(""))
   
    def test_get_director_2(self):
        movie1 = Movie(get_omdb_data("Django Unchained"))
        assert(movie1.get_director() == "Quentin Tarantino")
    
    def test_get_actors_1(self):
        movie1 = Movie(get_omdb_data("Super Troopers"))
        assert(type(movie1.get_actors()) == type(""))
    
    def test_get_actors_2(self):
        movie1 = Movie(get_omdb_data("Fight Club"))
        assert("Edward Norton" in movie1.get_actors())
    
    def test_get_insert_tuple_1(self):
        movie1 = Movie(get_omdb_data("Fight Club"))
        assert(type(movie1.get_insert_tuple()) == tuple)
    
    def test_get_insert_tuple_2(self):
        movie1 = Movie(get_omdb_data("Fight Club"))
        assert(len(movie1.get_insert_tuple()) == 7)
    
    def test_tweet_class_ctor_1(self):
        movie1 = Movie(get_omdb_data("Step Brothers"))
        tweets = movie1.get_highest_paid_actor_tweets()
        t = Tweet(tweets[0])
        assert(type(t.content) == type(""))
    
    def test_tweet_class_ctor_2(self):
        movie1 = Movie(get_omdb_data("Step Brothers"))
        tweets = movie1.get_highest_paid_actor_tweets()
        t = Tweet(tweets[0])
        assert(type(t.retweets) == type(3))
    
    def test_tweet_class_get_insert_1(self):
        movie1 = Movie(get_omdb_data("Step Brothers"))
        tweets = movie1.get_highest_paid_actor_tweets()
        t = Tweet(tweets[0])
        assert(len(t.get_insert_tuple()) == 6)
    
    def test_tweet_class_get_insert_2(self):
        movie1 = Movie(get_omdb_data("Step Brothers"))
        tweets = movie1.get_highest_paid_actor_tweets()
        t = Tweet(tweets[0])
        assert(type(t.get_insert_tuple()) == tuple)
    
    def test_get_user_neighborhood_1(self):
        movie1 = Movie(get_omdb_data("Avatar"))
        tweets = movie1.get_highest_paid_actor_tweets()
        assert(type(get_user_neighborhood(tweets) == list))
    
    def test_get_user_neighborhood_2(self):
        movie1 = Movie(get_omdb_data("Avatar"))
        tweets = movie1.get_highest_paid_actor_tweets()
        assert(len(get_user_neighborhood(tweets)) >= 5)
    
    def test_get_omdb_data_1(self):
        movie1 = get_omdb_data("Avatar")
        assert("James Cameron" == movie1['Director'])
    
    def test_get_omdb_data_2(self):
        movie1 = get_omdb_data("Avatar")
        assert(type(movie1) == dict)
    
    def test_get_user_data_1(self):
        data = get_user_data("RedHourBen")
        assert(type(data) == dict)
    
    def test_get_user_data_2(self):
        data = get_user_data("RedHourBen")
        assert('favourites_count' in data.keys())


if __name__ == "__main__":
    unittest.main(verbosity=2)
