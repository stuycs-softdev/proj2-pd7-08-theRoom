from flask import Flask
from flask import request, render_template, redirect, url_for
import rottenapi
import reviewer

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
	movies = rottenapi.searchMovies(search_request)
	d['movies'] = movies

	return render_template('search.html', d=d)

@app.route('/movie/<movie_id>')
def movie(movie_id):
	movieInfo = rottenapi.movieInfo(movie_id)
	castInfo = rottenapi.castInfo(movie_id)
    print rottenapi.reviews(movie_id)
	reviews = [rottenapi.reviewText(r) for r in rottenapi.reviews(movie_id)]


	similarMovies = rottenapi.similarMovies(movie_id)
	return render_template('movie.html', movieInfo=movieInfo, castInfo=castInfo, reviews=reviews, similarMovies=similarMovies)

if __name__ == '__main__':
	app.debug = True
	app.run(host='0.0.0.0', port=5000)
