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

def reviewsByName(movie_name):
	movies = searchMovies(movie_name)
	movieID = movies[0]['id']
	return reviews(movieID)

def reviewText(review):
	page = ""
	try:
		page = urllib2.urlopen(review['links']['review']).read()
	except urllib2.HTTPError:
		return "404: " + review['publication']
	if review['publication'] == u'Village Voice':
		page = page[page.find("<div class='content_body'"):]
		page = page[len("<div class='content_body sm'><p>") : page.find("</div>")]
		return page

	if review['publication'] == u'Chicago Reader':
		tag = '<div class="filmShortBody" id="filmShortFull">'
		endtag = '<span class="byline"'
		page = page[page.find(tag) + len(tag) + 30 :]
		page = page[: page.find(endtag) - 44]
		return page

	if review['publication'] == u'Variety':
		tag = '<!-- Start Article Post Content -->'
		endtag = '\n<div'
		page = page[page.find(tag) + len(tag) + 50 :]
		page = page[: page.find(endtag)]
		return page
	
	print review
	return "Not handled: " + review['publication']

if __name__ == '__main__':
    movies = searchMovies("The Room")
    movieID = movies[0]['id']
    reviews = reviews(movieID)
    for review in reviews['reviews']:
    	print reviewText(review)
