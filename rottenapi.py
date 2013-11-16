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


if __name__ == '__main__':
    print searchMovies("The Room")
