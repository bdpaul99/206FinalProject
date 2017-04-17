## Your name: Brendan Paul
## The option you've chosen:
# Option 2

# Put import statements you expect to need here!
import unittest
import itertools
import collections
import tweepy
import twitter_info # same deal as always...
import json
import sqlite3

















# Write your test cases here.


## Remember to invoke all your tests...
class PartOne(unittest.TestCase):
    def test1(self):
        movie1 = Movie(movie_1dict)
        tweets = movie1.get_director_tweets()
        assert(len(tweets) >= 10)
    
    def test2(self):
        movie1 = Movie(movie_1dict)
        tweets = movie1.get_director_tweets()
        assert(type(tweets) == [])

    def test3(self):
        movie1 = Movie(movie_1dict)
        tweets = movie1.get_director_tweets()
        assert(type(tweets[0]) == {})
    def test4(self):
        movie1 = Movie(movie_1dict)
        assert(type(movie1.__str__()) == type(""))
    def test5(self):
        movie1 = Movie(movie_1dict)
        assert(type(movie1.get_director()) == type(""))
    def test6(self):
        movie1 = Movie(movie_1dict)
        assert(type(movie1.get_actors) == type([])))
    def test7(self):
        movie1 = Movie(Django_dict)
        assert(movie1.get_director() == "Quentin Tarantino")
    def test8(self):
        conn = sqlite3.connect('project3_tweets.db')
        cur = conn.cursor()
        cur.execute('SELECT * FROM Users');
        result = cur.fetchall()
        self.assertTrue(len(result)>10)


if __name__ == "__main__":
    unittest.main(verbosity=2)
