import urllib2
from urllib import quote_plus
import json
import config

apiroot = "http://api.rottentomatoes.com/api/public/v1.0/"

# apinode includes arguments except for apikey
def getURL(apinode):
    url = apiroot + apinode + "&apikey=%s"%config.apikey
    return url

# get a list of movies for the search_str
def searchMovies(search_str):
    results = urllib2.urlopen(getURL("movies.json?q=%s&page_limit=%d&page=%d"%(quote_plus(search_str),10,1)))
    out = json.loads(results.read())
    return out['movies']

# get movie info for a movie id
def movieInfo(movieID):
    results = urllib2.urlopen(getURL("movies/%s.json?"%movieID))
    out = json.loads(results.read())
    return out

# get cast info for a movie id
def castInfo(movieID):
    results = urllib2.urlopen(getURL("movies/%s/cast.json?"%movieID))
    out = json.loads(results.read())
    return out

# get reviews for a movie id
def reviews(movieID):
    results = urllib2.urlopen(getURL("movies/%s/reviews.json?"%movieID))
    out = json.loads(results.read())
    return out

# get similar movies for a movie id
def similarMovies(movieID):
    results = urllib2.urlopen(getURL("movies/%s/similar.json?"%movieID))
    out = json.loads(results.read())
    return out


if __name__ == '__main__':
    movies = searchMovies("The Room")
    print "Movies:",movies
    movieID = movies[0]['id']
    print "MovieID:",movieID
    movieInfo = movieInfo(movieID)
    print "MovieInfo:",movieInfo
    castInfo = castInfo(movieID)
    print "CastInfo:",castInfo
    reviews = reviews(movieID)
    print "Reviews:",reviews
    similar = similarMovies(movieID)
    print "Similar:",similar
