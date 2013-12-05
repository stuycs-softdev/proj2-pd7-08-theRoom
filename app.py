from flask import Flask
from flask import request, render_template, redirect, url_for
from document import doc
import db
import rottenapi
import reviewer
app = Flask(__name__)

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
	d['clean'] = rottenapi.cleanQuery

	return render_template('search.html', d=d)

@app.route('/movie/<movie_name>')
def movie(movie_name):
	a = db.Author()
	d = {'movie_name': movie_name}
	
	d['reviews'] = rottenapi.reviewsByName(movie_name)
	d['texts'] = []
	d['info'] = rottenapi.movieInfo(d['movie_name'])
	for review in d['reviews']:
		d['texts'].append(rottenapi.reviewText(review))
	for text in d['texts']:
		text.replace(". "," %s %s "%(doc.SQLes,doc.SQLss))
		text.replace("! "," %s %s "%(doc.SQLes,doc.SQLss))
		text.replace("? "," %s %s "%(doc.SQLes,doc.SQLss))
		data = text.split(" ")
		data.insert(0,doc.SQLss)
		data.append(doc.SQLes)
		i = 0
		while i < len(data) - 3:
			a.insert(data[i],data[i+1],data[i+2])
	d['review'] = reviewer.generateSentenceWithGrammar(a.everything())
	return render_template('movie.html', movieInfo=d)

if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
