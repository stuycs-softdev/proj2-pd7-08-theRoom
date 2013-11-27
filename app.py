from flask import Flask
from flask import request, render_template, redirect, url_for
import rottenapi

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def home():
	if request.method == "GET":
		return render_template('home.html')

	#POST, i.e. search
	search_request = request.form['search-request']
	return redirect(url_for('search', search_request=search_request))

@app.route('/search/<search_request>')
def search(search_request=None):
	if not search_request:
		return redirect('home')

	d = {'search_request': search_request}
	reviews = rottenapi.reviewsByName(search_request)
	d['reviews'] = reviews

	return render_template('search.html', d=d)

@app.route('/movie/<movie_name>')
def movie():
	d['movie_name'] = movie_name
	return render_template('movie.html', d=d)

if __name__ == '__main__':
	app.debug = True
	app.run(host='0.0.0.0', port=5000)
