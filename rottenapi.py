from urllib import quote_plus
from HTMLParser import HTMLParser
import urllib2
import json
import config
import re
import string
import socket

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
	return query.replace(' ', '%20')

def reviewText(review):
	try:
		print "lets open this baby up"
		link = review['links']['review'].replace(" ","%20")
		page = urllib2.urlopen(link,None,1).read()
	except urllib2.HTTPError:
		return None
	except KeyError:
		return None
	except urllib2.URLError:
		return None
	except socket.timeout:
		return None
	print "alright what do we have here"
	if review['publication'] == u'Village Voice':
		print "its the voice"
		page = page[page.find("<div class='content_body'"):]
		page = page[len("<div class='content_body sm'><p>") : page.find("</div>")]
		page = cleanHTML(page)
		page = page.encode("ascii","ignore")
		return page

	if review['publication'] == u'Chicago Reader':
		
		tag = '<div class="filmShortBody" id="filmShortFull">'
		endtag = '<span class="byline"'
		page = page[page.find(tag) + len(tag) + 30 :]
		page = page[: page.find(endtag) - 44]
		page = cleanHTML(page)
		page = page.encode("ascii","ignore")
		return page

	if review['publication'] == u'Variety':
		tag = '<!-- Start Article Post Content -->'
		endtag = '\n<div'
		page = page[page.find(tag) + len(tag) + 50 :]
		page = page[: page.find(endtag)]
		page = cleanHTML(page)
		page = page.encode("ascii","ignore")
		return page
	
	if review['publication'] == u'New Yorker':
		tag = '<p class="noindent">'
		endtag = '</p>'
		page = page[page.find(tag) + len(tag) :]
		page = page[: page.find(endtag)]
		page = cleanHTML(page)
		page = page.encode("ascii","ignore")
		return page

	if review['publication'] == u'CNN.com':
		tag = '<p ><b><b>(CNN)</b></b> -- '
		endtag = '<br /> </p><!'
		page = page[page.find(tag) + len(tag) :]
		page = page[: page.find(endtag)]
		page = cleanHTML(page)
		page = page.encode("ascii","ignore")
		return page
	
	if review['publication'] == u'The Wrap':
		tag = '<div style="font-weight:bold;font-size:16px;"><p>'
		endtag = '</div><!--content-area-->'
		page = page[page.find(tag) + len(tag) :]
		page = page[: page.find(endtag)]
		cleanHTML(page)
		page = page.encode("ascii","ignore")
		return stripWhitespace(page)
	
	#if review['publication'] == u'Passionate Moviegoer':
	#	return "Not handled on purpose: multiple reviews on same page."
	
	if review['publication'] == u'Time Out':
		tag = '<p class="date">'
		endtag = '<p class="articleAuthor module"'
		page = page[page.find(tag) + len(tag) + 23 :]
		page = page[: page.find(endtag) - 10]
		cleanHTML(page)
		page = page.decode("UTF-8","ignore")
		page = page.encode("ascii","ignore")
		return stripWhitespace(page)
	
	#if review['publication'] == u'Newsday':
	#	return "Not handled on purpose: no solid tag."

	#if review['publication'] == u'Richard Roeper.com':
	#	return "Not handled on purpose: video reviews."
	
	#if review['publication'] == u'Wall Street Journal':
	#	return "Not handled on purpose: no solid tag."

	#if review['publication'] == u'San Francisco Chronicle':
	#	return "Not handled on purpose: redirect."

	#if review['publication'] == u'Film.com':
	
	return None

def cleanHTML(text):
	old_text = ''
	text = string.replace(text, '<br />', ' ')
	while text != old_text:
		old_text = text
		text = re.sub('<[^<]+?>', '', text)
	parser = HTMLParser()
	text = text.decode("UTF-8","ignore")
	return parser.unescape(text)

def stripWhitespace(text):
	return " ".join(text.split())

if __name__ == '__main__':
    movies = searchMovies("Toy Story 3")
    movieID = movies[0]['id']
    reviews = reviews(movieID)
    for review in reviews['reviews']:
    	print reviewText(review)
