from urllib import quote_plus
from HTMLParser import HTMLParser
import urllib2
import json
import config
import re
import string

apiroot = "http://api.rottentomatoes.com/api/public/v1.0/"

# apinode includes arguments except for apikey
def getURL(apinode):
    url = apiroot + apinode + "&apikey=%s"%config.apikey
    return url

# get a list of movies for the query
def searchMovies(query):
	request = getURL("movies.json?q=%s"%cleanQuery(query))
	results = urllib2.urlopen(request)
	out = json.loads(results.read())
	return out

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
    results = urllib2.urlopen(getURL("movies/%s/reviews.json?review_type=top_critic"%movieID))
    out = json.loads(results.read())
    return out['reviews']

# get similar movies for a movie id
def similarMovies(movieID):
    results = urllib2.urlopen(getURL("movies/%s/similar.json?"%movieID))
    out = json.loads(results.read())
    return out

def reviewsByName(movie_name):
	movies = searchMovies(movie_name)['movies']
	movieID = movies[0]['id']
	return reviews(movieID)

def cleanQuery(query):
	print query.replace(' ', '%20')
	return query.replace(' ', '%20')

def reviewText(review):
	try:
		page = urllib2.urlopen(review['links']['review']).read()
	except urllib2.HTTPError:
		return "404: " + review['publication']

	if review['publication'] == u'Village Voice':
		page = page[page.find("<div class='content_body'"):]
		page = page[len("<div class='content_body sm'><p>") : page.find("</div>")]
		return cleanHTML(page)

	if review['publication'] == u'Chicago Reader':
		tag = '<div class="filmShortBody" id="filmShortFull">'
		endtag = '<span class="byline"'
		page = page[page.find(tag) + len(tag) + 30 :]
		page = page[: page.find(endtag) - 44]
		return cleanHTML(page)

	if review['publication'] == u'Variety':
		tag = '<!-- Start Article Post Content -->'
		endtag = '\n<div'
		page = page[page.find(tag) + len(tag) + 50 :]
		page = page[: page.find(endtag)]
		return cleanHTML(page)
	
	if review['publication'] == u'New Yorker':
		tag = '<p class="noindent">'
		endtag = '</p>'
		page = page[page.find(tag) + len(tag) :]
		page = page[: page.find(endtag)]
		return cleanHTML(page)

	if review['publication'] == u'CNN.com':
		tag = '<p ><b><b>(CNN)</b></b> -- '
		endtag = '<br /> </p><!'
		page = page[page.find(tag) + len(tag) :]
		page = page[: page.find(endtag)]
		return cleanHTML(page)
	
	if review['publication'] == u'The Wrap':
		tag = '<div style="font-weight:bold;font-size:16px;"><p>'
		endtag = '</div><!--content-area-->'
		page = page[page.find(tag) + len(tag) :]
		page = page[: page.find(endtag)]
		return stripWhitespace(cleanHTML(page))
	
	if review['publication'] == u'Passionate Moviegoer':
		return "Not handled on purpose: multiple reviews on same page."
	
	if review['publication'] == u'Time Out':
		tag = '<p class="date">'
		endtag = '<p class="articleAuthor module"'
		page = page[page.find(tag) + len(tag) + 23 :]
		page = page[: page.find(endtag) - 10]
		return stripWhitespace(cleanHTML(page))
	
	print review
	return "Not handled: " + review['publication']

def cleanHTML(text):
	old_text = ''
	text = string.replace(text, '<br />', ' ')
	while text != old_text:
		old_text = text
		text = re.sub('<[^<]+?>', '', text)
	parser = HTMLParser()
	return parser.unescape(text)

def stripWhitespace(text):
	return " ".join(text.split())

if __name__ == '__main__':
    movies = searchMovies("Toy Story 3")
    movieID = movies[0]['id']
    reviews = reviews(movieID)
    for review in reviews['reviews']:
    	if review['publication'] == u'Time Out':
    		print reviewText(review)
