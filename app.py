from flask import Flask
from flask import request, render_template, redirect, url_for
from document import doc
import db
import rottenapi
import reviewer
app = Flask(__name__)
REVIEW_LENGTH = 20 #sentences

@app.route('/', methods=['GET', 'POST'])
def home():
	d = {'search_request': ""}

	if request.method == "GET":
		return render_template('home.html', d=d)

	#POST, i.e. search
	search_request = request.form['search_request']
	return redirect(url_for('search', search_request=search_request))

@app.route('/search/<search_request>', methods=['GET', 'POST'])
def search(search_request=None):
	if not search_request:
		return redirect('home')

	if request.method == 'POST':
		search_request = request.form['search_request']

	d = {'search_request': search_request}
	movies = rottenapi.searchMovies(search_request)
	d['movies'] = movies
	#d['clean'] = rottenapi.cleanQuery
	#return d['search_request']
	return render_template('search.html', d=d)

@app.route('/movie/<movie_name>')
def movie(movie_name):
	
	a = db.Author()
	d = {'movie_name': movie_name}
	
	d['reviews'] = rottenapi.reviewsByName(movie_name)
	d['texts'] = []
	d['info'] = rottenapi.movieInfo(d['movie_name'])
	for review in d['reviews']:
		print "trying to read here"
		text = rottenapi.reviewText(review)
		if text is not None:
			d['texts'].append(text)
		else:
			print "couldnt read that one"
	print "Done reading"
	for text in d['texts']:
		saveText(text,a)
	
	d['review'] = ""
	
	i = 0
	while i < REVIEW_LENGTH:
		print "writing"
		d['review'] += " " + reviewer.generateSentenceWithGrammar(a.getPairs(doc.SQLss),a.getCorpus) + "."
		i += 1
	return render_template('movie.html', movieInfo=d)

@app.route('/debug/')
def debug():
	a = db.Author()
	a.reset()
	a.init()
	saveText("The quick Brown Fox jumped. Fire baby, fire.",a)
	saveText("When i ran to the quick supermarket I saw an explosive donkey making honking noises at my family whowere on fire because the Brown Fox had shot them.",a)
	return reviewer.generateSentenceWithGrammar(a.everything())

def saveText(text,a):
	text = text.replace(". "," %s %s "%(doc.SQLes,doc.SQLss))
	text = text.replace("! "," %s %s "%(doc.SQLes,doc.SQLss))
	text = text.replace("? "," %s %s "%(doc.SQLes,doc.SQLss))
	text = text.replace("\\n"," ")
	text = text.replace("\\t"," ")
	text = text.replace("\\r"," ")
	text = text.replace("\n"," ")
	text = text.replace("\t"," ")
	text = text.replace("\r"," ")
	text = text.replace("\\x"," ")
	text = text.replace("\\u2019","'")
	text = text.replace("\u2019","'")
	text = text.replace("\u"," ")
	text = text.replace("\\u"," ")
	data = text.split(" ")
	data.insert(0,doc.SQLss)
	data.append(doc.SQLes)
	i = 0
	print "not looping yet..."
	while i < len(data) - 3:
		print "LOOOOOOOOOOOOOOOOOOOOP"
		a.insert(data[i],data[i+1],data[i+2])
		i+= 1
	a.insert(data[i],data[i+1],doc.SQLes)
	a.insert(data[i+1],doc.SQLes,doc.SQLes)
	a.save()
	print "saved"
if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
